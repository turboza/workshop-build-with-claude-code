"""
W1-2 consolidation template — Lina's Coffee.

Copied into the workshop folder at Beat 8. Adapt COLUMNS and category
keywords if the learner picked anything non-default; otherwise run as-is.

Output: data/consolidated.csv

Two row types share the revenue side intentionally:
  - type='revenue'         → POS transaction-level rows (sum these for totals)
  - type='revenue_summary' → monthly_revenue.txt headline rows (reference only,
                              NOT summed — avoids double-count with POS detail)
"""

import csv
import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DUMP = os.path.join(BASE, "data-dump")
OUT_DIR = os.path.join(BASE, "data")
OUT_FILE = os.path.join(OUT_DIR, "consolidated.csv")

FX = 32  # 1 USD = 32 THB (locked constant)

COLUMNS = [
    "date", "type", "category", "vendor_or_party",
    "description", "amount_thb", "amount_usd",
    "currency_original", "source_file", "notes"
]

CATEGORIES = ["Sales", "Coffee Beans", "Dairy & Pastry", "Payroll", "Rent & Utilities", "Other"]


def thb_to_usd(thb):
    return round(float(thb) / FX, 2)


def usd_to_thb(usd):
    return round(float(usd) * FX, 2)


def categorize(text):
    t = text.lower()
    if any(w in t for w in ["equipment service", "cleaning", "marketing", "ig ads",
                             "flyer", "decor", "atm withdraw", "transfer"]):
        return "Other"
    if any(w in t for w in ["bean", "ethiopian", "highland"]):
        return "Coffee Beans"
    if any(w in t for w in ["milk", "dairy", "pastry", "greenleaf", "bangkok dairy"]):
        return "Dairy & Pastry"
    if any(w in t for w in ["salary", "payroll", "bonus", "wage"]):
        return "Payroll"
    if any(w in t for w in ["rent", "electric", "water", "internet", "utility", "utilities",
                             "property tax", "insurance", "fastnet", "nk property",
                             "city power", "city water"]):
        return "Rent & Utilities"
    return "Other"


rows = []


# ── 1. monthly_revenue.txt ──────────────────────────────────────────────────
MONTH_MAP = {
    "Oct 2025": "2025-10-01", "Nov 2025": "2025-11-01", "Dec 2025": "2025-12-01",
    "Jan 2026": "2026-01-01", "Feb 2026": "2026-02-01", "Mar 2026": "2026-03-01",
}
with open(os.path.join(DATA_DUMP, "monthly_revenue.txt"), encoding="utf-8") as f:
    for line in f:
        for label, d in MONTH_MAP.items():
            if line.startswith(label):
                m = re.search(r"฿([\d,]+)", line)
                if m:
                    thb = float(m.group(1).replace(",", ""))
                    rows.append({
                        "date": d, "type": "revenue_summary", "category": "Sales",
                        "vendor_or_party": "Lina's Coffee (summary)",
                        "description": f"Monthly revenue headline — {label}",
                        "amount_thb": thb, "amount_usd": thb_to_usd(thb),
                        "currency_original": "THB",
                        "source_file": "monthly_revenue.txt",
                        "notes": "headline figure — not summed (avoids double-count with POS)"
                    })
rev_count = len(rows)
print(f"monthly_revenue.txt    : {rev_count} rows")


# ── 2. pos_export_oct2025-mar2026.csv ───────────────────────────────────────
pos_count = 0
with open(os.path.join(DATA_DUMP, "pos_export_oct2025-mar2026.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ts = r["timestamp"]
        d = ts[:10] if ts else ""
        price = float(r["price_thb"] or 0)
        discount = float(r["discount_thb"] or 0)
        net = price - discount
        void = r.get("notes", "").strip().lower() == "void"
        rows.append({
            "date": d,
            "type": "refund" if void else "revenue",
            "category": "Sales",
            "vendor_or_party": "Customer",
            "description": f"{r['product']} {r.get('size','')}: terminal {r['terminal_id']} staff {r['staff_id']}".strip(),
            "amount_thb": net,
            "amount_usd": thb_to_usd(net),
            "currency_original": "THB",
            "source_file": "pos_export_oct2025-mar2026.csv",
            "notes": "void" if void else ""
        })
        pos_count += 1
print(f"pos_export             : {pos_count} rows")


# ── 3. expenses_2025.csv ────────────────────────────────────────────────────
exp_count = 0
with open(os.path.join(DATA_DUMP, "expenses_2025.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if not r.get("date"):
            continue
        cur = r.get("currency", "THB").strip().upper()
        amt_raw = float(r.get("amount", 0) or 0)
        if cur == "USD":
            thb = usd_to_thb(amt_raw)
            usd = amt_raw
        else:
            thb = float(r.get("amount_thb", amt_raw) or amt_raw)
            usd = thb_to_usd(thb)
        cat_raw = r.get("category_raw", "").strip()
        item = r.get("item", "").strip()
        cat = categorize(cat_raw or item)
        rows.append({
            "date": r["date"].strip(), "type": "expense", "category": cat,
            "vendor_or_party": item,
            "description": item,
            "amount_thb": -thb, "amount_usd": -usd,
            "currency_original": cur,
            "source_file": "expenses_2025.csv",
            "notes": r.get("notes", "").strip()
        })
        exp_count += 1
print(f"expenses_2025.csv      : {exp_count} rows")


# ── 4. bank_statement_abc.csv ───────────────────────────────────────────────
bank_count = 0
with open(os.path.join(DATA_DUMP, "bank_statement_abc.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if not r.get("date"):
            continue
        debit = float(r.get("debit_thb", 0) or 0)
        credit = float(r.get("credit_thb", 0) or 0)
        desc = r.get("description", "").strip()
        if debit > 0:
            thb = -debit
        else:
            thb = credit
        rows.append({
            "date": r["date"].strip(), "type": "transfer",
            "category": categorize(desc),
            "vendor_or_party": desc,
            "description": desc,
            "amount_thb": thb, "amount_usd": thb_to_usd(thb),
            "currency_original": "THB",
            "source_file": "bank_statement_abc.csv", "notes": ""
        })
        bank_count += 1
print(f"bank_statement_abc.csv : {bank_count} rows")


# ── 5. supplier_invoices.csv ────────────────────────────────────────────────
sup_count = 0
with open(os.path.join(DATA_DUMP, "supplier_invoices.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if not r.get("date"):
            continue
        thb = float(r.get("total_thb", 0) or 0)
        vendor = r.get("vendor", "").strip()
        item = r.get("item", "").strip()
        rows.append({
            "date": r["date"].strip(), "type": "expense",
            "category": categorize(vendor + " " + item),
            "vendor_or_party": vendor,
            "description": item,
            "amount_thb": -thb, "amount_usd": -thb_to_usd(thb),
            "currency_original": "THB",
            "source_file": "supplier_invoices.csv",
            "notes": f"inv {r.get('invoice_no','')} paid={r.get('paid','')}"
        })
        sup_count += 1
print(f"supplier_invoices.csv  : {sup_count} rows")


# ── 6. staff_payroll.csv ────────────────────────────────────────────────────
pay_count = 0
with open(os.path.join(DATA_DUMP, "staff_payroll.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        month = r.get("month", "").strip()
        if not month:
            continue
        d = month + "-25"
        total = float(r.get("total_paid_thb", 0) or 0)
        cash_note = r.get("cash_note", "").strip()
        rows.append({
            "date": d, "type": "expense", "category": "Payroll",
            "vendor_or_party": r.get("name", "").strip(),
            "description": f"Salary {r.get('name','').strip()} {month}",
            "amount_thb": -total, "amount_usd": -thb_to_usd(total),
            "currency_original": "THB",
            "source_file": "staff_payroll.csv",
            "notes": "cash extra" if cash_note else ""
        })
        pay_count += 1
print(f"staff_payroll.csv      : {pay_count} rows")


# ── 7. rent_utilities.txt ───────────────────────────────────────────────────
MONTHS = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]
ELEC = {"2025-10": 7200, "2025-11": 6800, "2025-12": 8400,
        "2026-01": 7900, "2026-02": 7600, "2026-03": 9100}
rent_util_entries = [
    ("Rent", "NK Property", 45000, "Rent & Utilities"),
    ("Water", "Water Authority", 800, "Rent & Utilities"),
    ("Internet", "FastNet", 1290, "Rent & Utilities"),
]
ru_count = 0
for mo in MONTHS:
    d = mo + "-05"
    for desc, vendor, thb, cat in rent_util_entries:
        rows.append({
            "date": d, "type": "expense", "category": cat,
            "vendor_or_party": vendor,
            "description": desc,
            "amount_thb": -thb, "amount_usd": -thb_to_usd(thb),
            "currency_original": "THB",
            "source_file": "rent_utilities.txt", "notes": ""
        })
        ru_count += 1
    elec = ELEC.get(mo, 0)
    rows.append({
        "date": d, "type": "expense", "category": "Rent & Utilities",
        "vendor_or_party": "Electric Authority",
        "description": "Electric",
        "amount_thb": -elec, "amount_usd": -thb_to_usd(elec),
        "currency_original": "THB",
        "source_file": "rent_utilities.txt", "notes": ""
    })
    ru_count += 1
rows.append({
    "date": "2025-11-01", "type": "expense", "category": "Rent & Utilities",
    "vendor_or_party": "Revenue Dept", "description": "Property tax",
    "amount_thb": -18000, "amount_usd": -thb_to_usd(18000),
    "currency_original": "THB", "source_file": "rent_utilities.txt", "notes": "annual"
})
rows.append({
    "date": "2025-10-01", "type": "expense", "category": "Rent & Utilities",
    "vendor_or_party": "Insurer", "description": "Insurance",
    "amount_thb": -24000, "amount_usd": -thb_to_usd(24000),
    "currency_original": "THB", "source_file": "rent_utilities.txt", "notes": "annual"
})
ru_count += 2
print(f"rent_utilities.txt     : {ru_count} rows")


# ── Write output ────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
rows.sort(key=lambda r: r["date"])

with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)

total = len(rows)
revenue = sum(r["amount_thb"] for r in rows if r["type"] == "revenue")
revenue_summary = sum(r["amount_thb"] for r in rows if r["type"] == "revenue_summary")
expenses = sum(r["amount_thb"] for r in rows if r["type"] == "expense")
net = revenue + expenses

print(f"\n{'-'*45}")
print(f"Total rows merged      : {total}")
print(f"Revenue (POS detail)   : THB {revenue:,.0f}")
print(f"Revenue (headline ref) : THB {revenue_summary:,.0f}  (not summed - reference only)")
print(f"Expenses (THB)         : THB {expenses:,.0f}")
print(f"Net (THB)              : THB {net:,.0f}  (approx. ${net/FX:,.0f} USD)")
print(f"Output                 : data/consolidated.csv")
print(f"{'-'*45}")
