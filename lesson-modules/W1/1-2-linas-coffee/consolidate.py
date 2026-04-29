"""
Consolidate Lina's 6 data files into a single CSV.
Output: data/consolidated.csv
"""

import csv
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DUMP = os.path.join(BASE, "data-dump")
OUT  = os.path.join(BASE, "data", "consolidated.csv")

FX = 32  # 1 USD = 32 THB

COLUMNS = ["date", "type", "category", "vendor", "description",
           "amount_thb", "amount_usd", "currency", "source_file", "notes"]

DOI_VARIANTS = {"doichaang co.", "doi chang coffee", "doi chaang coffee"}

def norm_doi(name):
    return "Doi Chaang Coffee" if name.strip().lower() in DOI_VARIANTS else name.strip()

def thb_usd(thb):
    return round(thb / FX, 2)

def usd_thb(usd):
    return round(usd * FX, 2)

rows = []

# ── 1. POS export ──────────────────────────────────────────────────────────────
with open(os.path.join(DUMP, "pos_export_oct2025-mar2026.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        price = float(r["price_thb"])
        discount = float(r["discount_thb"] or 0)
        net = price - discount if price >= 0 else price  # keep void negative
        is_void = r["notes"].strip().lower() == "void"
        note = "void" if is_void else ""
        rows.append({
            "date": r["timestamp"][:10],
            "type": "income",
            "category": "Sales",
            "vendor": "",
            "description": r["product"].strip(),
            "amount_thb": round(net, 2),
            "amount_usd": thb_usd(net),
            "currency": "THB",
            "source_file": "pos_export_oct2025-mar2026.csv",
            "notes": note,
        })

# ── 2. Expenses ────────────────────────────────────────────────────────────────
EXPENSE_CAT = {
    "กาแฟ": "Coffee Beans",
    "coffee beans": "Coffee Beans",
    "dairy": "Dairy & Pastry",
    "pastry": "Dairy & Pastry",
    "maintenance": "Other",
    "marketing": "Other",
    "other": "Other",
}

with open(os.path.join(DUMP, "expenses_2025.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cur = r["currency"].strip().upper()
        if cur == "USD":
            amt_usd = float(r["amount"])
            amt_thb = usd_thb(amt_usd)
        else:
            amt_thb = float(r["amount_thb"])
            amt_usd = thb_usd(amt_thb)
        raw_cat = r.get("category_raw", "").strip().lower()
        cat = EXPENSE_CAT.get(raw_cat, "Other")
        # infer category from description if category_raw is blank
        if not raw_cat:
            desc = r["item"].lower()
            if "bean" in desc or "doi chaang" in desc or "doi chang" in desc or "bunna" in desc:
                cat = "Coffee Beans"
            elif "milk" in desc or "dairy" in desc or "pastry" in desc:
                cat = "Dairy & Pastry"
            elif "marketing" in desc or "ig ads" in desc or "flyer" in desc:
                cat = "Other"
            elif "cleaning" in desc:
                cat = "Other"
            else:
                cat = "Other"
        vendor = norm_doi(r["item"].split(",")[0]) if "doi" in r["item"].lower() else ""
        rows.append({
            "date": r["date"].strip(),
            "type": "expense",
            "category": cat,
            "vendor": vendor,
            "description": r["item"].strip(),
            "amount_thb": -abs(amt_thb),
            "amount_usd": -abs(amt_usd),
            "currency": cur,
            "source_file": "expenses_2025.csv",
            "notes": r.get("notes", "").strip(),
        })

# ── 3. Supplier invoices ────────────────────────────────────────────────────────
with open(os.path.join(DUMP, "supplier_invoices.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        amt = float(r["total_thb"])
        vendor = norm_doi(r["vendor"])
        item = r["item"].strip().lower()
        if "coffee" in item or "bean" in item:
            cat = "Coffee Beans"
        elif "milk" in item or "dairy" in item:
            cat = "Dairy & Pastry"
        elif "pastry" in item:
            cat = "Dairy & Pastry"
        else:
            cat = "Other"
        rows.append({
            "date": r["date"].strip(),
            "type": "expense",
            "category": cat,
            "vendor": vendor,
            "description": r["item"].strip(),
            "amount_thb": -abs(amt),
            "amount_usd": -thb_usd(amt),
            "currency": "THB",
            "source_file": "supplier_invoices.csv",
            "notes": f"inv {r['invoice_no']}",
        })

# ── 4. Payroll ──────────────────────────────────────────────────────────────────
with open(os.path.join(DUMP, "staff_payroll.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        month = r["month"].strip()          # e.g. 2025-10
        date = month + "-01"               # first of month as date
        amt = float(r["total_paid_thb"])
        cash_note = r.get("cash_note", "").strip()
        cash_extra = r.get("cash_extra_thb", "").strip()
        note = f"cash extra ฿{cash_extra} ({cash_note})" if cash_extra and cash_extra != "0" else ""
        rows.append({
            "date": date,
            "type": "expense",
            "category": "Payroll",
            "vendor": "",
            "description": f"Payroll — {r['name'].strip()} ({r['staff_id'].strip()})",
            "amount_thb": -abs(amt),
            "amount_usd": -thb_usd(amt),
            "currency": "THB",
            "source_file": "staff_payroll.csv",
            "notes": note,
        })

# ── 5. Rent & utilities (parsed from text) ─────────────────────────────────────
MONTHS = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]
ELECTRIC = {
    "2025-10": 7200, "2025-11": 6800, "2025-12": 8400,
    "2026-01": 7900, "2026-02": 7600, "2026-03": 9100,
}
for m in MONTHS:
    date = m + "-05"  # rent paid 5th
    # Rent
    rows.append({
        "date": date,
        "type": "expense",
        "category": "Rent & Utilities",
        "vendor": "NK Property",
        "description": "Monthly rent",
        "amount_thb": -45000,
        "amount_usd": -thb_usd(45000),
        "currency": "THB",
        "source_file": "rent_utilities.txt",
        "notes": "",
    })
    # Electricity
    elec = ELECTRIC.get(m, 0)
    rows.append({
        "date": m + "-15",
        "type": "expense",
        "category": "Rent & Utilities",
        "vendor": "",
        "description": "Electricity",
        "amount_thb": -elec,
        "amount_usd": -thb_usd(elec),
        "currency": "THB",
        "source_file": "rent_utilities.txt",
        "notes": "",
    })
    # Water (~800/month)
    rows.append({
        "date": m + "-15",
        "type": "expense",
        "category": "Rent & Utilities",
        "vendor": "",
        "description": "Water",
        "amount_thb": -800,
        "amount_usd": -thb_usd(800),
        "currency": "THB",
        "source_file": "rent_utilities.txt",
        "notes": "avg",
    })
    # Internet
    rows.append({
        "date": m + "-15",
        "type": "expense",
        "category": "Rent & Utilities",
        "vendor": "TOT",
        "description": "Internet",
        "amount_thb": -1290,
        "amount_usd": -thb_usd(1290),
        "currency": "THB",
        "source_file": "rent_utilities.txt",
        "notes": "",
    })

# Annual: insurance (October) and property tax (November)
rows.append({
    "date": "2025-10-01",
    "type": "expense",
    "category": "Rent & Utilities",
    "vendor": "",
    "description": "Insurance (annual)",
    "amount_thb": -24000,
    "amount_usd": -thb_usd(24000),
    "currency": "THB",
    "source_file": "rent_utilities.txt",
    "notes": "annual",
})
rows.append({
    "date": "2025-11-01",
    "type": "expense",
    "category": "Rent & Utilities",
    "vendor": "",
    "description": "Property tax (annual)",
    "amount_thb": -18000,
    "amount_usd": -thb_usd(18000),
    "currency": "THB",
    "source_file": "rent_utilities.txt",
    "notes": "annual",
})

# ── Write output ───────────────────────────────────────────────────────────────
rows.sort(key=lambda r: r["date"])

os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. {len(rows)} rows → {OUT}")
