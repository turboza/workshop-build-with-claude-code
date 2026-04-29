---
workshop: W1-2 Lina's Coffee — Messy to Organized
status: checkpointed
started: 2026-04-29T00:00:00
---

# Workshop Log

## Step 1 — Met Lina
Lina's situation: branch 2 expansion, bank Friday, 6 messy files, accountant quit Feb.

## Step 2 — Surveyed the data dump
6 files summarized: POS (voids, size inconsistency), expenses (mixed Thai/English categories), bank statement (bank codes), supplier invoices (vendor name variants), payroll (cash extras), rent_utilities (plain text).
Taught: read-before-write

## Step 3 — Opened POS file
What learner spotted: negative prices (voids)

## Step 4 — Learned @file references
Used @pos_export to get column list and 3 observations: size inconsistency, two terminals/four staff, void rows.

## Decision — Schema columns
Picked: date, type, category, vendor, description, amount_thb, amount_usd, currency, source_file, notes
Why: matched Lina's mental model (where money goes + when)

## Decision — Categories
Picked: Sales, Coffee Beans, Dairy & Pastry, Payroll, Rent & Utilities, Other
Why: covers all 6 files cleanly; learner approved defaults

## Action — Consolidated 6 files
Output: data/consolidated.csv (673 rows)
Notes: Python script; vendor names normalized (3 Doi Chaang variants → 1); void POS rows flagged in notes column; rent/utilities parsed from plain text

## Insight surfaced
Top costs: Payroll ฿440,000 + Rent & Utilities ฿371,540 = ฿811,540 (~$25,360) fixed floor before any COGS.

## Action — Wrote bank summary
Output: linas-bank-summary.md — plain-language summary Lina can send to K-Bank before Friday.

---

## Summary
**Status:** Checkpoint-completed (success point hit + bonus chapters done)

**Real progress:**
- Designed a 10-column schema from scratch — date, type, category, vendor, description, dual currency, source file, notes
- Picked 6 categories that cover all of Lina's spend without overlap
- Built a Python consolidation script and ran it — 673 rows from 6 different file formats into one CSV
- Caught and normalized 3 vendor name variants for Doi Chaang Coffee
- Surfaced the key insight: payroll + rent = ฿811,540 fixed floor every 6 months, before a single bean is bought
- Wrote a plain-language bank summary Lina can send before Friday

**Files produced:**
- `data/consolidated.csv` (673 rows, all 6 sources)
- `consolidate.py` (reusable script)
- `linas-bank-summary.md` (ready to send)

**Where we left off:** git not initialized yet — one step when you come back to it.

**Closed at:** 2026-04-29T00:00:00
