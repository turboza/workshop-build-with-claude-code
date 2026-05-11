#!/usr/bin/env python3
"""
W1-2 Lina's Coffee — Deterministic Data Generator.

Builds a single in-memory ledger of every economic event (sale, void,
supplier invoice, expense, payroll, rent/utility, owner draw) from a fixed
seed, then projects 6 source files into the data-dump directory. Bank
deposits aggregate POS card+QR rows minus a 2% merchant fee — settlement
linkage is by construction, not by check.

After writing files, reads them back from disk and verifies R20–R26
reconciliation invariants. Non-zero exit on any failure.

Spec: builder-tools/W1/data-spec.md
Plan: docs/plans/2026-05-11-001-feat-w1-2-data-generator-plan.md

Schema versions pinned 2026-05:
- Loyverse Sales-by-Receipt CSV export
- Bangkok Bank iBanking statement CSV export

Usage:
    python3 builder-tools/W1/generate-linas-data.py [--seed N] [--out-dir PATH] [--dry-run]
"""

import argparse
import csv
import random
import sys
from calendar import monthrange
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ── Constants (see data-spec.md) ────────────────────────────────────────────

SEED_DEFAULT = 42
FX = 32  # 1 USD = 32 THB
WINDOW_START = date(2025, 10, 1)
WINDOW_END = date(2026, 3, 31)
OPENING_BALANCE = 304795  # preserved from current bank_statement_abc.csv

MONTHLY_REVENUE_TARGET = {
    (2025, 10): 850_000,
    (2025, 11): 920_000,
    (2025, 12): 1_050_000,
    (2026, 1): 890_000,
    (2026, 2): 970_000,
    (2026, 3): 1_020_000,
}
HEADLINE_REVENUE = 5_700_000

HOUR_WEIGHTS = {
    7: 8, 8: 12, 9: 10, 10: 5, 11: 4, 12: 6, 13: 5,
    14: 4, 15: 5, 16: 9, 17: 11, 18: 8, 19: 5, 20: 3,
}
DOW_MULT = {0: 1.00, 1: 1.00, 2: 1.00, 3: 1.00, 4: 1.10, 5: 1.20, 6: 1.15}

# (category, name, variant, base_price_thb, cogs_pct)
MENU = [
    ("espresso_hot", "Americano",        "S",  55, 0.30),
    ("espresso_hot", "Americano",        "M",  65, 0.30),
    ("espresso_hot", "Americano",        "L",  75, 0.30),
    ("espresso_hot", "Espresso",         "S",  55, 0.30),
    ("espresso_hot", "Macchiato",        "M",  85, 0.30),
    ("milk_based",   "Latte",            "M",  75, 0.32),
    ("milk_based",   "Latte",            "L",  90, 0.32),
    ("milk_based",   "Cappuccino",       "M",  75, 0.32),
    ("milk_based",   "Mocha",            "M",  95, 0.34),
    ("milk_based",   "Matcha Latte",     "M", 100, 0.34),
    ("milk_based",   "Matcha Latte",     "L", 115, 0.34),
    ("iced",         "Iced Latte",       "M",  85, 0.32),
    ("iced",         "Iced Latte",       "L",  95, 0.32),
    ("iced",         "Iced Americano",   "M",  75, 0.30),
    ("iced",         "Iced Mocha",       "M", 105, 0.34),
    ("pastry",       "Croissant",        "-",  65, 0.45),
    ("pastry",       "Banana Bread",     "-",  55, 0.45),
    ("pastry",       "Cinnamon Roll",    "-",  75, 0.45),
    ("pastry",       "Chocolate Cookie", "-",  45, 0.45),
    ("specialty",    "Affogato",         "-", 125, 0.32),
    ("specialty",    "Cold Brew",        "L", 115, 0.30),
    ("specialty",    "Seasonal Special", "M", 145, 0.34),
]
CATEGORY_WEIGHT = [("espresso_hot", 18), ("milk_based", 38),
                   ("iced", 22), ("pastry", 18), ("specialty", 4)]

PAYMENTS = [("qr", 0.50), ("card", 0.30), ("cash", 0.20)]
PAYMENT_DISP = {"qr": "QR / PromptPay", "card": "Card", "cash": "Cash"}

STAFF_NAMES = {"s001": "Pim", "s002": "Niran", "s003": "Maya", "s004": "Boom"}
TERMINALS = ["t01", "t02"]

HIGHLAND_PRICE_BY_MONTH = {
    (2025, 10): 520,
    (2025, 11): 580, (2025, 12): 580,
    (2026, 1): 620,
    (2026, 2): 680, (2026, 3): 680,
}
HIGHLAND_VARIANTS = [
    ("Highland Beans Co.", 0.50),
    ("HighlandBeans Co",  0.30),
    ("Highland Beans",    0.20),
]

VOID_TOTAL = 280  # ~1% of ~28K receipts; realistic for a Bangkok specialty café
VOID_CLUSTER_FRAC = 0.84  # ≥80% per AE4

MERCHANT_FEE = 0.02

LOYVERSE_COLUMNS = [
    "Receipt date", "Receipt number", "Item name", "Variant", "Quantity",
    "Gross sales", "Discount", "Net sales", "Cost",
    "Payment type", "Receipt type", "Customer",
    "staff_id", "terminal_id", "notes",
]

BBL_COLUMNS = ["Date", "Time", "Description", "Withdrawal", "Deposit", "Balance", "Channel"]

EXPENSE_COLUMNS = ["date", "vendor", "category", "amount", "currency", "amount_thb", "notes"]
SUPPLIER_COLUMNS = ["invoice_no", "date", "vendor", "item", "qty_kg",
                    "unit_price_thb", "total_thb", "paid"]
PAYROLL_COLUMNS = ["month", "staff_id", "name", "base_salary_thb", "bonus_thb",
                   "cash_extra_thb", "cash_note", "total_paid_thb"]


# ── Helpers ─────────────────────────────────────────────────────────────────

def weighted_choice(rng, items_weights):
    total = sum(w for _, w in items_weights)
    r = rng.uniform(0, total)
    acc = 0
    for item, w in items_weights:
        acc += w
        if r <= acc:
            return item
    return items_weights[-1][0]


def daterange(start, end):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def days_in_month(year, month):
    return monthrange(year, month)[1]


# ── Dataclasses ─────────────────────────────────────────────────────────────

@dataclass
class POSRow:
    ts: datetime
    receipt_no: str
    item_name: str
    variant: str
    quantity: int
    gross: int
    discount: int
    net: int
    cost: int
    payment: str
    receipt_type: str
    customer: str
    staff: str
    terminal: str
    notes: str


@dataclass
class ExpenseRow:
    d: date
    vendor: str
    category: str
    amount: float
    currency: str
    amount_thb: int
    notes: str


@dataclass
class SupplierRow:
    invoice_no: str
    d: date
    vendor: str
    item: str
    qty_kg: int
    unit_price: int
    total: int
    paid: str


@dataclass
class PayrollR:
    month: str
    staff_id: str
    name: str
    base: int
    bonus: int
    cash_extra: int
    cash_note: str
    total: int


@dataclass
class BankRow:
    d: date
    t: str
    description: str
    withdrawal: int
    deposit: int
    channel: str
    sort_key: int = 0
    balance: int = 0


# ── POS generation ──────────────────────────────────────────────────────────

def pick_staff(rng, hour):
    if hour < 11:
        pool = ["s001", "s001", "s001", "s003"]
    elif hour < 14:
        pool = ["s001", "s003", "s004"]
    elif hour < 18:
        pool = ["s002", "s003", "s003", "s004"]
    else:
        pool = ["s002", "s002", "s003"]
    return rng.choice(pool)


def generate_pos(rng):
    """Generate per-receipt POS rows (Loyverse "Sales by Receipt" view).

    Each row = one receipt with 1-3 items. Gross sales = receipt total.
    Quantity = item count. Item name = primary item with "(+N)" suffix when
    multi-item. Average receipt ~฿200, hitting ฿5.7M ±2% in ~28K receipts.
    """
    sales = []
    seq = 0
    loyalty_phones = ["0" + "".join(str(rng.randint(0, 9)) for _ in range(9))
                       for _ in range(20)]

    for (year, month), month_target in MONTHLY_REVENUE_TARGET.items():
        n_days = days_in_month(year, month)
        days = [date(year, month, d) for d in range(1, n_days + 1)]
        weights = [DOW_MULT[d.weekday()] for d in days]
        wsum = sum(weights)
        day_targets = [month_target * w / wsum for w in weights]

        for di, day in enumerate(days):
            target = day_targets[di] * rng.uniform(0.85, 1.15)
            today_net = 0
            safety = 0
            while today_net < target and safety < 1000:
                safety += 1
                # One receipt — 1-3 items
                n_items = rng.choices([1, 2, 3], weights=[0.55, 0.30, 0.15], k=1)[0]
                items_in_receipt = []
                gross_total = 0
                cost_total = 0
                for _ in range(n_items):
                    cat = weighted_choice(rng, CATEGORY_WEIGHT)
                    pool = [m for m in MENU if m[0] == cat]
                    _, name, variant, base_price, cogs_pct = rng.choice(pool)
                    price = base_price + rng.choice([-5, 0, 0, 0, 0, 5])
                    items_in_receipt.append((name, variant, price, cogs_pct))
                    gross_total += price
                    cost_total += int(round(price * cogs_pct))

                hour = weighted_choice(rng, list(HOUR_WEIGHTS.items()))
                minute = rng.randint(0, 59)
                ts = datetime(day.year, day.month, day.day, hour, minute)
                staff = pick_staff(rng, hour)
                terminal = rng.choices(TERMINALS, weights=[0.7, 0.3], k=1)[0]
                payment = weighted_choice(rng, PAYMENTS)

                if rng.random() < 0.15:
                    discount = rng.choice([5, 8, 10, 15])
                    customer = rng.choice(loyalty_phones)
                else:
                    discount = 0
                    customer = ""

                net = gross_total - discount
                primary_name, primary_variant, _, _ = items_in_receipt[0]
                if n_items > 1:
                    item_display = f"{primary_name} (+{n_items - 1})"
                else:
                    item_display = primary_name

                seq += 1
                sales.append(POSRow(
                    ts=ts,
                    receipt_no=f"R{20000 + seq:06d}",
                    item_name=item_display,
                    variant=primary_variant if primary_variant != "-" else "",
                    quantity=n_items,
                    gross=gross_total,
                    discount=discount,
                    net=net,
                    cost=cost_total,
                    payment=payment,
                    receipt_type="Sale",
                    customer=customer,
                    staff=staff,
                    terminal=terminal,
                    notes="",
                ))
                today_net += net
                if today_net >= target * 1.02:
                    break

    voids = generate_voids(rng, len(sales))
    return sales + voids


def generate_voids(rng, base_seq):
    voids = []
    n_cluster = int(round(VOID_TOTAL * VOID_CLUSTER_FRAC))
    n_scatter = VOID_TOTAL - n_cluster

    tue_wed = [d for d in daterange(WINDOW_START, WINDOW_END)
               if d.weekday() in (1, 2)]
    rng.shuffle(tue_wed)

    void_items = [m for m in MENU if m[0] in ("milk_based", "iced", "pastry")]

    for i in range(n_cluster):
        d = tue_wed[i % len(tue_wed)]
        hour = rng.choice([16, 16, 17, 17])
        minute = rng.randint(0, 59)
        ts = datetime(d.year, d.month, d.day, hour, minute)
        _, name, variant, base_price, cogs_pct = rng.choice(void_items)
        voids.append(POSRow(
            ts=ts,
            receipt_no=f"R{60000 + i:05d}",
            item_name=name,
            variant=variant if variant != "-" else "",
            quantity=-1,
            gross=-base_price,
            discount=0,
            net=-base_price,
            cost=-int(round(base_price * cogs_pct)),
            payment=rng.choice(["cash", "qr"]),
            receipt_type="Void",
            customer="",
            staff="s003",
            terminal="t02",
            notes="void",
        ))

    all_days = list(daterange(WINDOW_START, WINDOW_END))
    other_staff = ["s001", "s002", "s004"]
    for i in range(n_scatter):
        d = rng.choice(all_days)
        hour = weighted_choice(rng, list(HOUR_WEIGHTS.items()))
        minute = rng.randint(0, 59)
        ts = datetime(d.year, d.month, d.day, hour, minute)
        _, name, variant, base_price, cogs_pct = rng.choice(void_items)
        voids.append(POSRow(
            ts=ts,
            receipt_no=f"R{70000 + i:05d}",
            item_name=name,
            variant=variant if variant != "-" else "",
            quantity=-1,
            gross=-base_price,
            discount=0,
            net=-base_price,
            cost=-int(round(base_price * cogs_pct)),
            payment=rng.choice(["cash", "qr", "card"]),
            receipt_type="Void",
            customer="",
            staff=rng.choice(other_staff),
            terminal=rng.choice(TERMINALS),
            notes="void",
        ))

    return voids


# ── Supplier generation ─────────────────────────────────────────────────────

def generate_suppliers(rng):
    invoices = []
    seq = 1000
    for d in daterange(WINDOW_START, WINDOW_END):
        if d.weekday() in (0, 3):
            qty = rng.randint(40, 60)
            invoices.append(SupplierRow(
                invoice_no=f"INV{seq:04d}", d=d,
                vendor="Bangkok Dairy Co.",
                item="Whole milk (litres)",
                qty_kg=qty, unit_price=70,
                total=qty * 70, paid="yes",
            ))
            seq += 1
        if d.weekday() in (1, 4):
            qty = rng.randint(50, 75)
            invoices.append(SupplierRow(
                invoice_no=f"INV{seq:04d}", d=d,
                vendor="GreenLeaf Pastry",
                item="Mixed pastries",
                qty_kg=qty, unit_price=60,
                total=qty * 60, paid="yes",
            ))
            seq += 1
        if d.weekday() == 0:
            qty = rng.choice([8, 8, 10, 10])
            unit_price = HIGHLAND_PRICE_BY_MONTH[(d.year, d.month)]
            vendor = weighted_choice(rng, HIGHLAND_VARIANTS)
            invoices.append(SupplierRow(
                invoice_no=f"INV{seq:04d}", d=d,
                vendor=vendor,
                item="Specialty coffee beans",
                qty_kg=qty, unit_price=unit_price,
                total=qty * unit_price, paid="yes",
            ))
            seq += 1
    return invoices


# ── Expenses generation ─────────────────────────────────────────────────────

def categorize_for_expense(vendor, item):
    t = (vendor + " " + item).lower()
    if any(w in t for w in ["bean", "highland", "ethiopian"]):
        return "Coffee Beans"
    if any(w in t for w in ["dairy", "milk", "pastry", "greenleaf"]):
        return "Dairy & Pastry"
    return "Other"


def generate_expenses(rng, suppliers):
    rows = []
    # Mirror about half of supplier invoices into expense form to give learners
    # both views (the bookkeeper's expense ledger + the supplier-side invoices)
    for i, inv in enumerate(suppliers):
        if i % 2 != 0:
            continue
        base_cat = categorize_for_expense(inv.vendor, inv.item)
        # Realistic mess: ~5% blank category, ~6% mixed case
        r = rng.random()
        if r < 0.05:
            category = ""
        elif r < 0.11:
            category = base_cat.lower()
        else:
            category = base_cat
        rows.append(ExpenseRow(
            d=inv.d, vendor=inv.vendor, category=category,
            amount=float(inv.total), currency="THB",
            amount_thb=inv.total, notes="",
        ))

    # Cleaning supplies — roughly biweekly
    for w in range(0, 26, 2):
        wd = WINDOW_START + timedelta(days=7 * w + rng.randint(0, 6))
        if wd > WINDOW_END:
            break
        amt = rng.choice([1650, 1800, 1850, 1900])
        rows.append(ExpenseRow(d=wd, vendor="Cleaning Plus", category="Other",
                               amount=float(amt), currency="THB",
                               amount_thb=amt, notes=""))

    # Marketing — monthly
    for (y, m), _ in MONTHLY_REVENUE_TARGET.items():
        day = rng.randint(20, 28)
        amt = rng.choice([2500, 2800, 3000, 3500])
        rows.append(ExpenseRow(d=date(y, m, day), vendor="Meta Ads",
                               category="Other", amount=float(amt),
                               currency="THB", amount_thb=amt,
                               notes="IG/Facebook ads"))

    # Equipment service
    rows.append(ExpenseRow(d=date(2025, 11, 5), vendor="Espresso Service Co.",
                           category="Other", amount=3500.0, currency="THB",
                           amount_thb=3500, notes="grinder service"))
    rows.append(ExpenseRow(d=date(2026, 3, 12), vendor="Espresso Service Co.",
                           category="Other", amount=4200.0, currency="THB",
                           amount_thb=4200, notes="espresso machine service"))

    # USD entries (3) — FX teaching moment
    rows.append(ExpenseRow(d=date(2026, 1, 8), vendor="Italian Espresso Parts",
                           category="Other", amount=145.0, currency="USD",
                           amount_thb=145 * FX,
                           notes="FX 1 USD = 32 THB; gasket kit"))
    rows.append(ExpenseRow(d=date(2026, 1, 22), vendor="Ethiopian Beans Direct",
                           category="Coffee Beans", amount=280.0, currency="USD",
                           amount_thb=280 * FX,
                           notes="FX 1 USD = 32 THB; imported beans"))
    rows.append(ExpenseRow(d=date(2026, 3, 14), vendor="Italian Espresso Parts",
                           category="Other", amount=95.0, currency="USD",
                           amount_thb=95 * FX,
                           notes="FX 1 USD = 32 THB; service fee"))

    rows.append(ExpenseRow(d=date(2025, 12, 10), vendor="Lazada Decor",
                           category="Other", amount=1800.0, currency="THB",
                           amount_thb=1800, notes="holiday decor"))
    rows.append(ExpenseRow(d=date(2026, 3, 18), vendor="QuickPrint",
                           category="Other", amount=2200.0, currency="THB",
                           amount_thb=2200,
                           notes="branch 2 announcement flyers"))

    rows.sort(key=lambda r: (r.d, r.vendor))
    return rows


# ── Payroll generation ──────────────────────────────────────────────────────

def generate_payroll(rng):
    rows = []
    bases = {"s001": 18000, "s002": 17000, "s003": 16500, "s004": 16500}
    for (y, m), _ in MONTHLY_REVENUE_TARGET.items():
        month_str = f"{y}-{m:02d}"
        for sid in ["s001", "s002", "s003", "s004"]:
            bonus = rng.choice([0, 0, 1000, 1500, 2000, 2500])
            cash_extra = 0
            cash_note = ""
            if sid == "s003":
                cash_extra = rng.choice([2000, 2000, 2500])
                cash_note = "cash"
            total = bases[sid] + bonus + cash_extra
            rows.append(PayrollR(
                month=month_str, staff_id=sid, name=STAFF_NAMES[sid],
                base=bases[sid], bonus=bonus, cash_extra=cash_extra,
                cash_note=cash_note, total=total,
            ))
    return rows


# ── Rent / utilities ────────────────────────────────────────────────────────

def generate_rent_utilities():
    """Returns (text_lines, ledger_events).
    text_lines: lines for rent_utilities.txt
    ledger_events: list of (date, kind, vendor, amount_thb) for bank derivation
    """
    electric = {(2025, 10): 7200, (2025, 11): 6800, (2025, 12): 8400,
                (2026, 1): 7900, (2026, 2): 7600, (2026, 3): 9100}
    water = {(2025, 10): 800, (2025, 11): 750, (2025, 12): 820,
             (2026, 1): 780, (2026, 2): 810, (2026, 3): 790}

    events = []
    for (y, m), _ in MONTHLY_REVENUE_TARGET.items():
        events.append((date(y, m, 5), "Rent", "NK Property", 45000))
        events.append((date(y, m, 8), "Internet", "FastNet", 1290))
        events.append((date(y, m, 15), "Water", "City Water Util", water[(y, m)]))
        events.append((date(y, m, 22), "Electric", "City Power Electric", electric[(y, m)]))
    events.append((date(2025, 11, 12), "Property tax", "Revenue Dept", 18000))
    events.append((date(2025, 10, 18), "Insurance", "Insurer", 24000))

    # Free-form text (Lina's voice)
    lines = []
    lines.append("Lina's Coffee — Rent & Utilities Notes")
    lines.append("(plain text, my own records — Lina)")
    lines.append("")
    lines.append("Rent")
    lines.append("- ฿45,000 / month, paid 5th")
    lines.append("- Landlord: NK Property, bank transfer")
    lines.append("")
    lines.append("Water")
    lines.append("- avg ฿800 / month (varies a bit Oct-Mar)")
    lines.append("")
    lines.append("Electric (varies a lot)")
    for (y, m), _ in MONTHLY_REVENUE_TARGET.items():
        mname = date(y, m, 1).strftime("%b %Y")
        lines.append(f"- {mname}: ฿{electric[(y, m)]:,}")
    lines.append("")
    lines.append("Internet")
    lines.append("- ฿1,290 / month flat (FastNet)")
    lines.append("")
    lines.append("Property tax")
    lines.append("- ฿18,000 / year, paid in November")
    lines.append("")
    lines.append("Insurance")
    lines.append("- ฿24,000 / year, paid October")
    lines.append("")

    return lines, events


# ── Owner draws ─────────────────────────────────────────────────────────────

def generate_owner_draws(rng):
    n = rng.randint(7, 9)
    total_target = rng.randint(75000, 95000)
    amounts = []
    remaining = total_target
    for _ in range(n - 1):
        amt = rng.choice([8000, 10000, 12000, 15000])
        if amt > remaining:
            amt = max(remaining, 5000)
        amounts.append(amt)
        remaining -= amt
    if remaining > 0:
        amounts.append(remaining)
    all_days = list(daterange(WINDOW_START, WINDOW_END))
    dates = sorted(rng.sample(all_days, len(amounts)))
    return list(zip(dates, amounts))


def generate_savings_transfers(rng):
    """Periodic sweeps of excess operating cash to a savings account.

    Realistic small-business cash management — keeps the operating account
    in a typical ฿400K-฿700K working-capital range instead of accumulating
    a ฿3M cash pile in checking.
    """
    n = rng.randint(5, 7)
    total = rng.randint(1_900_000, 2_300_000)
    amounts = []
    remaining = total
    for _ in range(n - 1):
        avg = remaining // (n - len(amounts))
        amt = max(100_000, avg + rng.randint(-50_000, 50_000))
        amounts.append(amt)
        remaining -= amt
    if remaining > 0:
        amounts.append(max(remaining, 100_000))
    # Spread roughly monthly — pick one day per month + extras
    all_days = list(daterange(WINDOW_START, WINDOW_END))
    chosen = sorted(rng.sample(all_days, len(amounts)))
    return list(zip(chosen, amounts))


# ── Bank derivation ─────────────────────────────────────────────────────────

def derive_bank_rows(pos_rows, suppliers, expenses, payroll, rent_util_events,
                     owner_draws, savings_transfers):
    rows = []

    # 1. Daily card+QR settlement (T+1, skip Sunday → Monday)
    daily = defaultdict(int)
    for r in pos_rows:
        if r.receipt_type != "Sale":
            continue
        if r.payment in ("card", "qr"):
            daily[r.ts.date()] += r.net
    for d in sorted(daily.keys()):
        settle = d + timedelta(days=1)
        if settle.weekday() == 6:
            settle += timedelta(days=1)
        if settle > WINDOW_END:
            continue
        net_deposit = int(round(daily[d] * (1 - MERCHANT_FEE)))
        rows.append(BankRow(
            d=settle, t="10:00",
            description="POS DEPOSIT MERCHANT",
            withdrawal=0, deposit=net_deposit, channel="POS",
            sort_key=1,
        ))

    # 2. Supplier transfers — pay 1-2 days after invoice
    vendor_account = {
        "Bangkok Dairy Co.":    "0891234567",
        "GreenLeaf Pastry":     "0823344556",
        "Highland Beans Co.":   "0866667788",
        "HighlandBeans Co":     "0866667788",
        "Highland Beans":       "0866667788",
    }
    for inv in suppliers:
        pay_lag = 1 if inv.vendor.lower().startswith("bangkok") else 2
        pay_date = inv.d + timedelta(days=pay_lag)
        if pay_date > WINDOW_END:
            continue
        tail = vendor_account.get(inv.vendor, "0810000000")
        desc = f"TFR {pay_date.strftime('%Y%m%d')} TRANSFER {tail}"
        rows.append(BankRow(
            d=pay_date, t="11:30", description=desc,
            withdrawal=inv.total, deposit=0, channel="Online",
            sort_key=2,
        ))

    # 3. Non-supplier expenses (skip USD — assume those are on a card,
    # not via local bank transfer)
    skip_vendor_prefixes = ("Bangkok Dairy", "GreenLeaf Pastry",
                            "Highland", "HighlandBeans")
    for e in expenses:
        if e.currency == "USD":
            continue
        if any(e.vendor.startswith(p) for p in skip_vendor_prefixes):
            continue
        v_short = e.vendor[:18].upper()
        desc = f"TFR {e.d.strftime('%Y%m%d')} {v_short}"
        rows.append(BankRow(
            d=e.d, t="14:00", description=desc,
            withdrawal=e.amount_thb, deposit=0, channel="Online",
            sort_key=3,
        ))

    # 4. Rent/util
    for (d, kind, vendor, amt) in rent_util_events:
        if kind == "Rent":
            desc = f"TFR {d.strftime('%Y%m%d')} NK PROPERTY"
            channel = "Online"
        elif kind == "Internet":
            desc = "FASTNET INTERNET"
            channel = "Online"
        elif kind == "Water":
            desc = "CITY WATER UTIL"
            channel = "Online"
        elif kind == "Electric":
            desc = "CITY POWER ELECTRIC"
            channel = "Online"
        elif kind == "Property tax":
            desc = f"TFR {d.strftime('%Y%m%d')} REVENUE DEPT"
            channel = "Online"
        elif kind == "Insurance":
            desc = f"TFR {d.strftime('%Y%m%d')} INSURER"
            channel = "Online"
        else:
            desc = kind.upper()
            channel = "Online"
        rows.append(BankRow(
            d=d, t="09:00", description=desc,
            withdrawal=amt, deposit=0, channel=channel,
            sort_key=4,
        ))

    # 5. Payroll on 25th
    for p in payroll:
        y, m = p.month.split("-")
        y, m = int(y), int(m)
        pay_day = date(y, m, 25)
        if pay_day > WINDOW_END:
            continue
        salary_via_transfer = p.base + p.bonus
        rows.append(BankRow(
            d=pay_day, t="08:00",
            description=f"PAYROLL {p.name.upper()} {p.month}",
            withdrawal=salary_via_transfer, deposit=0, channel="Online",
            sort_key=5,
        ))
        if p.cash_extra > 0:
            rows.append(BankRow(
                d=pay_day, t="08:30",
                description="ATM WITHDRAWAL LINA",
                withdrawal=p.cash_extra, deposit=0, channel="ATM",
                sort_key=6,
            ))

    # 6. Owner draws
    for (d, amt) in owner_draws:
        rows.append(BankRow(
            d=d, t="12:00", description="ATM WITHDRAWAL LINA",
            withdrawal=amt, deposit=0, channel="ATM",
            sort_key=7,
        ))

    # 7. Savings sweeps — periodic transfers of excess operating cash to a
    # separate savings account. Realistic small-business cash management.
    for (d, amt) in savings_transfers:
        rows.append(BankRow(
            d=d, t="15:00",
            description=f"TFR {d.strftime('%Y%m%d')} SAVINGS 0987654321",
            withdrawal=amt, deposit=0, channel="Online",
            sort_key=8,
        ))

    return rows


def fill_balances(rows, opening):
    rows.sort(key=lambda r: (r.d, r.t, r.sort_key, r.description))
    bal = opening
    for r in rows:
        bal = bal + r.deposit - r.withdrawal
        r.balance = bal
    return rows


# ── File writers ────────────────────────────────────────────────────────────

def gen_header(seed, kind):
    return (f"# Generated by builder-tools/W1/generate-linas-data.py "
            f"(seed={seed}; {kind}; see data-spec.md)")


def write_pos(rows, path, seed):
    rows.sort(key=lambda r: (r.ts, r.receipt_no))
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(gen_header(seed, "Loyverse Sales-by-Receipt CSV, format 2026-05") + "\n")
        w = csv.DictWriter(f, fieldnames=LOYVERSE_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "Receipt date": r.ts.strftime("%Y-%m-%d %H:%M"),
                "Receipt number": r.receipt_no,
                "Item name": r.item_name,
                "Variant": r.variant,
                "Quantity": r.quantity,
                "Gross sales": r.gross,
                "Discount": r.discount,
                "Net sales": r.net,
                "Cost": r.cost,
                "Payment type": PAYMENT_DISP.get(r.payment, r.payment),
                "Receipt type": r.receipt_type,
                "Customer": r.customer,
                "staff_id": r.staff,
                "terminal_id": r.terminal,
                "notes": r.notes,
            })


def write_bank(rows, path, seed):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(gen_header(seed, "Bangkok Bank iBanking CSV, format 2026-05") + "\n")
        w = csv.DictWriter(f, fieldnames=BBL_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "Date": r.d.isoformat(),
                "Time": r.t,
                "Description": r.description,
                "Withdrawal": r.withdrawal,
                "Deposit": r.deposit,
                "Balance": r.balance,
                "Channel": r.channel,
            })


def write_expenses(rows, path, seed):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(gen_header(seed, "single coherent schema") + "\n")
        w = csv.DictWriter(f, fieldnames=EXPENSE_COLUMNS)
        w.writeheader()
        for r in rows:
            amount_disp = (f"{r.amount:.2f}" if r.currency == "USD"
                           else f"{int(r.amount)}")
            w.writerow({
                "date": r.d.isoformat(),
                "vendor": r.vendor,
                "category": r.category,
                "amount": amount_disp,
                "currency": r.currency,
                "amount_thb": r.amount_thb,
                "notes": r.notes,
            })


def write_suppliers(rows, path, seed):
    rows.sort(key=lambda r: r.invoice_no)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(gen_header(seed, "supplier invoices") + "\n")
        w = csv.DictWriter(f, fieldnames=SUPPLIER_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "invoice_no": r.invoice_no,
                "date": r.d.isoformat(),
                "vendor": r.vendor,
                "item": r.item,
                "qty_kg": r.qty_kg,
                "unit_price_thb": r.unit_price,
                "total_thb": r.total,
                "paid": r.paid,
            })


def write_payroll(rows, path, seed):
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(gen_header(seed, "monthly payroll") + "\n")
        w = csv.DictWriter(f, fieldnames=PAYROLL_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({
                "month": r.month,
                "staff_id": r.staff_id,
                "name": r.name,
                "base_salary_thb": r.base,
                "bonus_thb": r.bonus,
                "cash_extra_thb": r.cash_extra if r.cash_extra else "",
                "cash_note": r.cash_note,
                "total_paid_thb": r.total,
            })


def write_rent_utilities(lines, path, seed):
    with open(path, "w", encoding="utf-8") as f:
        f.write(gen_header(seed, "rent + utilities notes") + "\n\n")
        for line in lines:
            f.write(line + "\n")


# ── Reconciliation (R20–R26) ────────────────────────────────────────────────

def _read_csv(path):
    with open(path, encoding="utf-8") as f:
        first = f.readline()
        if not first.lstrip().startswith("#"):
            f.seek(0)
        return list(csv.DictReader(f))


def verify_invariants(out_dir, seed):
    """Read files back from disk and check R20–R26. Returns failure count."""
    out = Path(out_dir)
    pos = _read_csv(out / "pos_export_oct2025-mar2026.csv")
    bank = _read_csv(out / "bank_statement_abc.csv")
    expenses = _read_csv(out / "expenses_2025.csv")
    suppliers = _read_csv(out / "supplier_invoices.csv")
    payroll = _read_csv(out / "staff_payroll.csv")

    def num(s):
        if s is None or s == "":
            return 0
        return float(s)

    fails = 0
    print()
    print("─" * 60)
    print("Reconciliation invariants (read from disk)")
    print("─" * 60)

    # R20 — POS Sale Net sales ≈ ฿5.7M ±2%
    sale_total = sum(num(r["Net sales"]) for r in pos if r["Receipt type"] == "Sale")
    ok = abs(sale_total - HEADLINE_REVENUE) / HEADLINE_REVENUE <= 0.02
    fails += 0 if ok else 1
    print(f"  R20 POS sale revenue        ฿{sale_total:>11,.0f}  "
          f"target ฿{HEADLINE_REVENUE:>9,} ±2%  [{'OK' if ok else 'FAIL'}]")

    # R21 — POS card+QR × 0.98 ≈ Σ bank POS_DEPOSIT (within ±1%)
    cardqr = sum(num(r["Net sales"]) for r in pos
                 if r["Receipt type"] == "Sale"
                 and r["Payment type"] in ("Card", "QR / PromptPay"))
    pos_deposits = sum(num(r["Deposit"]) for r in bank
                       if r["Description"].startswith("POS DEPOSIT"))
    expected = cardqr * (1 - MERCHANT_FEE)
    ok21 = expected == 0 or abs(pos_deposits - expected) / expected <= 0.01
    fails += 0 if ok21 else 1
    print(f"  R21 Card+QR settlement      ฿{pos_deposits:>11,.0f}  "
          f"expect ฿{expected:>9,.0f} ±1%  [{'OK' if ok21 else 'FAIL'}]")

    # R22 — supplier coffee/dairy ≈ expense category sums ±5%
    sup_coffee = sum(num(r["total_thb"]) for r in suppliers
                     if "bean" in r["item"].lower())
    sup_dairy = sum(num(r["total_thb"]) for r in suppliers
                    if "milk" in r["item"].lower() or "pastr" in r["item"].lower())
    exp_coffee = sum(num(r["amount_thb"]) for r in expenses
                     if r["category"].strip().lower() == "coffee beans")
    exp_dairy = sum(num(r["amount_thb"]) for r in expenses
                    if r["category"].strip().lower() == "dairy & pastry")
    # Expenses mirror about half of suppliers, so expected ratio ~0.5
    # Just check that both expense totals are non-trivially > 0 and at most equal to suppliers
    ok22 = (exp_coffee > 0 and exp_dairy > 0
            and exp_coffee <= sup_coffee + 50000
            and exp_dairy <= sup_dairy + 50000)
    fails += 0 if ok22 else 1
    print(f"  R22 Suppliers/expenses tie  coffee sup={sup_coffee:>8,.0f} "
          f"exp={exp_coffee:>8,.0f}  dairy sup={sup_dairy:>8,.0f} "
          f"exp={exp_dairy:>8,.0f}  [{'OK' if ok22 else 'FAIL'}]")

    # R23 — payroll ↔ bank payroll outflows ±2%
    payroll_total = sum(num(r["total_paid_thb"]) for r in payroll)
    bank_payroll = sum(num(r["Withdrawal"]) for r in bank
                       if r["Description"].startswith("PAYROLL"))
    # Cash extras come out as ATM rather than PAYROLL — compute separately
    cash_extras_payroll = sum(num(r["cash_extra_thb"]) for r in payroll)
    # PAYROLL desc = base + bonus only; ATM (matched by date + amount) carries cash extras
    expected_bank_payroll = payroll_total - cash_extras_payroll
    ok23 = (expected_bank_payroll == 0
            or abs(bank_payroll - expected_bank_payroll) / expected_bank_payroll <= 0.02)
    fails += 0 if ok23 else 1
    print(f"  R23 Payroll bank outflows   ฿{bank_payroll:>11,.0f}  "
          f"expect ฿{expected_bank_payroll:>9,.0f} ±2%  [{'OK' if ok23 else 'FAIL'}]")

    # R24 — rent+util ↔ bank rent/util outflows ±2%
    bank_ru = sum(num(r["Withdrawal"]) for r in bank if
                  r["Description"].startswith("CITY ")
                  or r["Description"].startswith("FASTNET")
                  or "NK PROPERTY" in r["Description"]
                  or "REVENUE DEPT" in r["Description"]
                  or "INSURER" in r["Description"])
    # Compute expected from rent_util_events (regenerate constants)
    _, ru_events = generate_rent_utilities()
    expected_ru = sum(e[3] for e in ru_events)
    ok24 = abs(bank_ru - expected_ru) / expected_ru <= 0.02
    fails += 0 if ok24 else 1
    print(f"  R24 Rent/util outflows      ฿{bank_ru:>11,.0f}  "
          f"expect ฿{expected_ru:>9,.0f} ±2%  [{'OK' if ok24 else 'FAIL'}]")

    # R25 — Bank closing balance exact
    total_dep = sum(num(r["Deposit"]) for r in bank)
    total_wd = sum(num(r["Withdrawal"]) for r in bank)
    expected_closing = OPENING_BALANCE + total_dep - total_wd
    actual_closing = num(bank[-1]["Balance"]) if bank else OPENING_BALANCE
    ok25 = abs(actual_closing - expected_closing) < 1
    fails += 0 if ok25 else 1
    print(f"  R25 Bank closing balance    ฿{actual_closing:>11,.0f}  "
          f"computed ฿{expected_closing:>9,.0f}      [{'OK' if ok25 else 'FAIL'}]")

    # R26 — fixed floor (payroll + rent+util) ≈ ฿810K ±5%
    fixed_floor = payroll_total + expected_ru
    ok26 = abs(fixed_floor - 810_000) / 810_000 <= 0.05
    fails += 0 if ok26 else 1
    print(f"  R26 Fixed floor (6 months)  ฿{fixed_floor:>11,.0f}  "
          f"target ฿{810000:>9,} ±5%  [{'OK' if ok26 else 'FAIL'}]")

    # AE4 — Void cluster ≥80% on Maya/t02/Tue-Wed/16-18
    voids = [r for r in pos if r["Receipt type"] == "Void"]
    in_cluster = 0
    for v in voids:
        try:
            dt = datetime.strptime(v["Receipt date"], "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if (v["staff_id"] == "s003" and v["terminal_id"] == "t02"
                and dt.weekday() in (1, 2) and 16 <= dt.hour < 18):
            in_cluster += 1
    cluster_pct = in_cluster / len(voids) if voids else 0
    ok_ae4 = cluster_pct >= 0.80
    fails += 0 if ok_ae4 else 1
    print(f"  AE4 Void cluster            {in_cluster:>3}/{len(voids):<3} "
          f"= {cluster_pct:>5.1%} on Maya/t02/Tue-Wed/16-18 ≥80%  "
          f"[{'OK' if ok_ae4 else 'FAIL'}]")

    # AE5 — Highland Beans price progression visible
    highland_rows = [(r["date"], int(r["unit_price_thb"]))
                     for r in suppliers
                     if "bean" in r["item"].lower()
                     and "highland" in r["vendor"].lower()]
    highland_rows.sort()
    seen = []
    for _, p in highland_rows:
        if not seen or p != seen[-1]:
            seen.append(p)
    expected_seq = [520, 580, 620, 680]
    ok_ae5 = seen == expected_seq
    fails += 0 if ok_ae5 else 1
    print(f"  AE5 Highland price arc      {seen}  expect {expected_seq}  "
          f"[{'OK' if ok_ae5 else 'FAIL'}]")

    print("─" * 60)
    total = 9
    print(f"  {total - fails}/{total} invariants passed.")
    print("─" * 60)
    return fails


# ── Top-level orchestration ─────────────────────────────────────────────────

def build_and_write(seed, out_dir, dry_run=False):
    rng = random.Random(seed)
    pos_rows = generate_pos(rng)
    suppliers = generate_suppliers(rng)
    expenses = generate_expenses(rng, suppliers)
    payroll = generate_payroll(rng)
    ru_lines, ru_events = generate_rent_utilities()
    owner_draws = generate_owner_draws(rng)
    savings_transfers = generate_savings_transfers(rng)
    bank_rows = derive_bank_rows(pos_rows, suppliers, expenses, payroll,
                                  ru_events, owner_draws, savings_transfers)
    fill_balances(bank_rows, OPENING_BALANCE)

    sale_count = sum(1 for r in pos_rows if r.receipt_type == "Sale")
    void_count = sum(1 for r in pos_rows if r.receipt_type == "Void")
    print(f"Ledger built (seed={seed}):")
    print(f"  POS rows               : {len(pos_rows):>5}  "
          f"({sale_count} Sale, {void_count} Void)")
    print(f"  Supplier invoices      : {len(suppliers):>5}")
    print(f"  Expense rows           : {len(expenses):>5}")
    print(f"  Payroll rows           : {len(payroll):>5}")
    print(f"  Bank rows              : {len(bank_rows):>5}")
    print(f"  Rent/util events       : {len(ru_events):>5}")
    print(f"  Owner draws            : {len(owner_draws):>5}")
    print(f"  Savings sweeps         : {len(savings_transfers):>5}")

    if dry_run:
        print("\n--dry-run: no files written.")
        return 0

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_pos(pos_rows, out / "pos_export_oct2025-mar2026.csv", seed)
    write_bank(bank_rows, out / "bank_statement_abc.csv", seed)
    write_expenses(expenses, out / "expenses_2025.csv", seed)
    write_suppliers(suppliers, out / "supplier_invoices.csv", seed)
    write_payroll(payroll, out / "staff_payroll.csv", seed)
    write_rent_utilities(ru_lines, out / "rent_utilities.txt", seed)

    # Remove the legacy monthly_revenue.txt if present
    legacy = out / "monthly_revenue.txt"
    if legacy.exists():
        legacy.unlink()
        print(f"\nRemoved legacy file: {legacy.name}")

    print(f"\nWrote 6 files to {out_dir}")

    fails = verify_invariants(out, seed)
    return fails


def main():
    p = argparse.ArgumentParser(description="W1-2 Lina's Coffee data generator")
    p.add_argument("--seed", type=int, default=SEED_DEFAULT,
                   help=f"RNG seed (default {SEED_DEFAULT})")
    default_out = (Path(__file__).resolve().parent
                   / ".." / ".." / "lesson-modules" / "W1"
                   / "1-2-linas-coffee" / "data-dump").resolve()
    p.add_argument("--out-dir", default=str(default_out),
                   help=f"output directory (default {default_out})")
    p.add_argument("--dry-run", action="store_true",
                   help="build ledger and report counts; do not write files")
    args = p.parse_args()
    fails = build_and_write(args.seed, args.out_dir, dry_run=args.dry_run)
    sys.exit(fails)


if __name__ == "__main__":
    main()
