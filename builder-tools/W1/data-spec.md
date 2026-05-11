# W1-2 Lina's Coffee — Data Spec

Single source of truth for the deterministic data generator at
`builder-tools/W1/generate-linas-data.py`. The generator imports the constants
below or co-locates them; this document also explains *why* each number is
what it is so anyone editing the spec later can reason about downstream
impact.

If you change a number here, re-run the generator and check that every
invariant in `verify_invariants()` still passes. The workshop script
(`lesson-modules/W1/1-2-linas-coffee/CLAUDE.md`) and the W1-3 dashboard
narrative (`lesson-modules/W1/1-3-linas-dashboard/CLAUDE.md`) reference
specific landmark numbers — they're listed under "Anchor numbers" below.

---

## Window

- Period: **2025-10-01 → 2026-03-31** (182 days, 6 months)
- Trading days: every day; café is open daily
- FX: locked at **1 USD = 32 THB** (matches workshop's stated rate)

---

## Anchor numbers (the workshop refers to these verbatim)

| Anchor | Value | Why it matters |
|---|---|---|
| Revenue, 6 months | ฿5,700,000 ±2% | Lina's headline number quoted in W1-2 BEAT 10 and W1-3 |
| Monthly revenue avg | ฿950,000 | W1-3 BEAT references "monthly revenue ~฿950K" |
| Net retained, 6 months | ~฿800,000 | W1-2 BEAT 10 "net" callout |
| Fixed floor, 6 months | ฿810,000 ±5% | W1-2 BEAT 10 + W1-3 KPI header. = Σ(payroll) + Σ(rent + utilities) |
| Highland Beans price arc | ฿520 → ฿680 / kg | Bonus chapter A and W1-3 leak B |
| Void cluster | Maya / t02 / Tue–Wed / 16–18 | Bonus chapter B and W1-3 leak A |

If you adjust these, search both `lesson-modules/W1/1-2-linas-coffee/CLAUDE.md`
and `lesson-modules/W1/1-3-linas-dashboard/CLAUDE.md` for the same numbers
before shipping.

---

## Monthly revenue distribution

Matches the prior `monthly_revenue.txt` headline so instructor familiarity is
preserved. Generator scales POS transactions to hit each month within ±2%.

| Month | Target (฿) | Driver |
|---|---|---|
| 2025-10 | 850,000 | Seasonal baseline |
| 2025-11 | 920,000 | Slight uptick |
| 2025-12 | 1,050,000 | Holidays + corporate orders |
| 2026-01 | 890,000 | Post-holiday dip |
| 2026-02 | 970,000 | Chinese New Year + Valentine's pickup |
| 2026-03 | 1,020,000 | Pre-Songkran momentum |
| **Total** | **5,700,000** | Lina's quoted headline |

---

## Transaction-level distributions (POS)

POS file is shaped as **Loyverse "Sales by Receipt"** — one row per receipt,
not per line item. `Quantity` reflects items per receipt (1–3). `Gross sales`
is the receipt total. This matches Loyverse's actual per-receipt export
and gives a row count that scales with real café volume.

### Volume

- Total receipts: **~43,000 – 45,000** over 6 months (default seed lands ~43,563)
- ~240 receipts per day on average — realistic for a Bangkok specialty café
  doing ~฿950K/month
- Per-day count is driven by hitting the monthly revenue target, with a
  weekend bump applied via DOW_MULT
- Receipt composition: ~55% single-item, ~30% two-item, ~15% three-item
- Average receipt net: ~฿130 (after discounts)

### Hourly traffic curve (weight per hour)

Bimodal — morning rush + afternoon coffee break. Café opens 06:30, closes
21:00.

| Hour | Weight | Notes |
|---|---|---|
| 7  | 8 | Morning rush start |
| 8  | 12 | Peak morning |
| 9  | 10 | Late morning |
| 10 | 5 | Lull starts |
| 11 | 4 | |
| 12 | 6 | Lunch bump |
| 13 | 5 | |
| 14 | 4 | Quiet afternoon |
| 15 | 5 | Afternoon pickup |
| 16 | 9 | Afternoon coffee break peak |
| 17 | 11 | Peak afternoon |
| 18 | 8 | Tapering |
| 19 | 5 | Evening |
| 20 | 3 | Quiet evening |

Peak hours (7–9 and 16–18) carry ~60% of daily volume.

### Day-of-week multiplier

- Mon–Thu: 1.00
- Fri: 1.10
- Sat: 1.20
- Sun: 1.15

### Ticket size by product category

Drawn from a discrete distribution per item with small Gaussian noise on top.

| Category | Items | Price range (฿) | Share of txns |
|---|---|---|---|
| Espresso-based hot | Americano, Espresso, Macchiato | 55–95 | 18% |
| Milk-based | Latte, Cappuccino, Mocha, Matcha Latte | 75–110 | 38% |
| Iced drinks | Iced Latte, Iced Americano, Iced Mocha | 75–115 | 22% |
| Pastry | Croissant, Banana Bread, Cinnamon Roll, Chocolate Cookie | 45–75 | 18% |
| Specialty | Affogato, Cold Brew, Seasonal | 110–145 | 4% |

Average ticket lands ~฿95–฿110 by construction.

### Payment mix

- QR (PromptPay): **50% ±5%**
- Card: **30% ±5%**
- Cash: **20% ±5%**

### Discounts

- ~12% of transactions carry a small discount (฿4–฿10) — loyalty / phone-tag
- Encoded in `Discount` column (Loyverse field)

---

## Staff and terminals

| Staff ID | Name | Role | Typical hours |
|---|---|---|---|
| s001 | Pim | Lead barista | 06:30–14:30 |
| s002 | Niran | Barista | 14:00–21:00 |
| s003 | Maya | Float / closing | 13:00–21:00 |
| s004 | Boom | Weekend + relief | rotating |

Terminals: **t01** (main bar), **t02** (mobile / second register).

---

## Void cluster (R18)

Total voids: **~280** (about 0.6% of ~43K receipts — realistic for a Bangkok
specialty café). Real-world café void rates run 0.5%–2%; the original
sample's 3.5% was artifact of small sample size.

Cluster signature (verified by AE4):
- Staff `s003` (Maya): **≥80% of voids**
- Terminal `t02`: **≥80% of voids**
- Weekday in (Tue, Wed): **≥80% of voids**
- Time-of-day 16:00–18:00: **≥80% of voids**

The remaining ~45 voids are scattered — distributed across other staff,
terminals, and weekdays so the cluster is statistical, not categorical
(a real cluster always has noise).

Voids in the POS file: `Receipt type = Void`, negative `Net sales`,
`notes = void`.

---

## Supplier price progression (R17)

Highland Beans (specialty coffee beans) unit prices step up across the
window:

| Period | Unit price (฿/kg) |
|---|---|
| 2025-10 | 520 |
| 2025-11 → 2025-12 | 580 |
| 2026-01 | 620 |
| 2026-02 → 2026-03 | 680 |

Step-function (not smooth ramp) — matches the bonus chapter narrative
"went ฿520 → ฿680" cleanly.

Other suppliers (Bangkok Dairy Co., GreenLeaf Pastry) hold roughly steady
with small natural variation (±2%).

---

## Vendor name variants (R19)

Highland Beans appears across `supplier_invoices.csv` and `expenses_2025.csv`
under three spellings:

- `Highland Beans Co.` (canonical, ~50% of mentions)
- `HighlandBeans Co` (~30%)
- `Highland Beans` (~20%)

These represent realistic data-entry drift, not random noise — the workshop
teaches normalization, and seeing the same vendor under different names is
the canonical reason normalization matters.

---

## USD entries

Three rows in `expenses_2025.csv` are denominated in USD:

| Approx date | Vendor | Item | Amount (USD) | Why |
|---|---|---|---|---|
| 2026-01-08 | Italian Espresso Parts | Gasket kit | 145 | Imported parts |
| 2026-01-22 | Ethiopian Beans Direct | Imported beans | 280 | Imported beans |
| 2026-03-12 | Italian Espresso Parts | Service fee | 95 | Equipment service |

Each row has `currency = USD`, an `amount_thb` column with the converted
value at 1 USD = 32 THB, and a `notes` mention of the FX rate. The workshop
uses these for the FX teaching moment in Beat 5.

---

## Cost structure (6-month totals)

| Bucket | Share of revenue | THB total | Notes |
|---|---|---|---|
| COGS (beans, dairy, pastry) | ~9% | ~525,000 | Bangkok Dairy + GreenLeaf Pastry + Highland Beans |
| Labor (payroll) | ~8% | ~434,000 | 4 staff × 6 months + Maya's cash extras + bonuses |
| Rent + utilities | ~7% | ~371,000 | Rent ฿45K/mo, electric varies, water, internet, property tax, insurance |
| Other operating | ~2% | ~120,000 | Marketing, cleaning, equipment service, USD imports, decor, flyers |
| **Total operating expenses** | **~26%** | **~1,450,000** | |
| Cash sales (off-bank, owner-retained) | ~20% | ~1,140,000 | Cash payment receipts; not deposited in bank account |
| Savings sweeps (owner-initiated) | ~35% | ~2,000,000 | Periodic transfers to a separate savings account |
| Formal owner draws (ATM) | ~1.5% | ~85,000 | Ad-hoc cash withdrawals |
| **Operating account net growth** | **~17%** | **~1,000,000** | Bank ending ~฿1.3M vs opening ฿305K |

Note on "expenses": the workshop's prior narrative claimed expenses ~฿4.9M
on revenue ฿5.7M (86% cost ratio). That figure was unverified — the actual
data this generator produces shows a much healthier business (specialty café
with low rent, 4-person staff, high gross margins). The workshop script and
W1-3 narrative will both be updated in U7/U8 to reflect the real cost
structure: ฿1.45M operating expenses, ~26% cost ratio, ~74% gross retained,
with the difference flowing to cash sales (owner-retained), savings sweeps,
and operating-account buffer.

### Fixed floor (R26)

Σ(payroll over 6 months) + Σ(rent + utilities over 6 months) = **฿810K ±5%**.

This is the headline insight the workshop reveals in BEAT 10. The two summands:

- Payroll: ~฿440K (4 staff × 6 months × ~฿18K avg incl. bonuses + cash extras)
- Rent + utilities: ~฿370K (rent ฿270K + electric ~฿47K + water ~฿4.8K +
  internet ฿7.7K + property tax ฿18K + insurance ฿24K)
- Total: **~฿810K**

If you tune the generator, do not let this number drift outside ฿770K–฿850K.

---

## Bank statement

### Opening balance

`฿304,795` on 2025-10-05 — **preserved verbatim** from the current
`bank_statement_abc.csv`. Keeping this constant means existing screenshots
and instructor familiarity carry over.

### Settlement linkage (R21)

Daily POS card + QR revenue settles into the bank as **`POS DEPOSIT MERCHANT`**
rows on T+1 (next business day), minus a flat **2.0% merchant fee**.

Cash revenue does not appear in the bank statement directly. Owner periodically
deposits cash (rare) or pulls it (more common — see ATM withdrawals).

### Withdrawals

| Pattern | Trigger | Channel |
|---|---|---|
| Supplier transfers | After each `supplier_invoices.csv` invoice (T+1 to T+2) | Online |
| Rent | 5th of each month, ฿45,000 to NK Property | Online |
| Utilities | Mid-month, varying amounts | Online |
| Payroll | 25th of each month, base + bonus via transfer | Online |
| Owner draws | Periodic ATM withdrawals (Lina) | ATM |
| Cash-extra ATM | 25th, fund Maya's cash extra | ATM |
| Savings sweeps | Periodic owner-initiated sweeps to a separate account | Online |

### Owner draws

ATM withdrawals attributed to Lina, total **฿70K–฿100K** across the window.
Roughly 6–10 withdrawals at ฿8K–฿15K each. These appear as `ATM WITHDRAWAL
LINA` in the description, `Channel = ATM`. They explain why the bank balance
grows less than the operating result.

### Closing balance

Computed exactly from `opening + Σ(deposits) − Σ(withdrawals)`. Lands at
~฿1.3M with the default seed — operating buffer Lina holds while saving up
for the branch 2 expansion. With the ~฿2M of savings sweeps visible in the
file, her total liquid position is ~฿3.3M, which lines up with the workshop
narrative of needing a ฿4M loan to complete the branch 2 build.

---

## Output file formats

### Loyverse POS export (R14)

Columns (canonical Loyverse Sales-by-Receipt CSV order, pinned 2026-05):

```
Receipt date, Receipt number, Item name, Variant, Quantity,
Gross sales, Discount, Net sales, Cost, Payment type, Receipt type,
Customer, staff_id, terminal_id, notes
```

Notes:
- `Receipt type` is one of `Sale`, `Refund`, `Void`
- `staff_id`, `terminal_id`, `notes` are workshop-specific tail columns
  (preserved from current file shape so `consolidate-template.py` keeps reading)
- Pin the format date in `generate-linas-data.py`'s header comment

### Bangkok Bank statement (R15)

Columns (canonical Bangkok Bank iBanking CSV order, pinned 2026-05):

```
Date, Time, Description, Withdrawal, Deposit, Balance, Channel
```

Notes:
- `Channel` is one of `Counter`, `ATM`, `Online`, `POS`
- Descriptions follow the bank's actual export style (`POS DEPOSIT MERCHANT`,
  `TFR <date> TRANSFER <phone>`, `CITY WATER UTIL`, `CITY POWER ELECTRIC`,
  `FASTNET INTERNET`, `ATM WITHDRAWAL LINA`)

### Expenses (new single coherent schema)

Replaces the 3-tab gimmick. One schema, top to bottom:

```
date, vendor, category, amount, currency, amount_thb, notes
```

Realistic mess included:
- ~2 rows with blank `category` (data-entry drift)
- ~3 USD rows (the FX teaching moment)
- ~3 rows with mixed-case category labels (`Pastry` vs `pastry`)

### Supplier invoices (unchanged schema)

```
invoice_no, date, vendor, item, qty_kg, unit_price_thb, total_thb, paid
```

### Staff payroll (unchanged schema)

```
month, staff_id, name, base_salary_thb, bonus_thb, cash_extra_thb,
cash_note, total_paid_thb
```

### Rent & utilities (plain text)

Free-form Lina-voice notes covering rent, water, electric, internet, property
tax, insurance. Shape preserved from current file.

---

## Reproducibility

- Default seed: **`42`**
- CLI: `python3 builder-tools/W1/generate-linas-data.py [--seed N] [--out-dir PATH]`
- Same seed → byte-identical output across runs (verified across CPython
  3.9–3.13 using `random.Random`)
- Every generated CSV/TXT file begins with a header comment recording the
  generator filename, seed, and generation timestamp

---

## How to regenerate

```bash
cd workshop
python3 builder-tools/W1/generate-linas-data.py
```

Default `--out-dir` is `lesson-modules/W1/1-2-linas-coffee/data-dump/`. The
script overwrites existing files and prints a reconciliation report at the
end. Non-zero exit on any invariant failure.

After regenerating, also refresh W1-3's consolidated file:

```bash
cd lesson-modules/W1/1-2-linas-coffee
python3 ../../../builder-tools/W1/consolidate-template.py
cp data/consolidated.csv ../1-3-linas-dashboard/data/consolidated.csv
```

---

## Reconciliation invariants

Checked by `verify_invariants()` at end of every run. Generator exits with a
count of failed invariants.

1. **R20** — Σ(POS `Net sales` where `Sale`) within ±2% of ฿5,700,000
2. **R21** — Σ(POS card + QR) × 0.98 ↔ Σ(bank POS deposits) within ±1%
3. **R22** — Σ(supplier `total_thb` for coffee/dairy/pastry) ↔ expense
   category sums within ±5%
4. **R23** — Σ(payroll `total_paid_thb`) ↔ bank payroll outflows within ±2%
5. **R24** — Σ(rent + utilities) ↔ bank rent/util outflows within ±2%
6. **R25** — Bank closing = opening + Σ(deposits) − Σ(withdrawals), exactly
7. **R26** — Σ(payroll) + Σ(rent + utilities) over 6 months → ฿810K ±5%

If any invariant fails after a spec edit, fix the spec or the generator —
don't lower the tolerance. The whole point of this generator is that the
data ties out.

---

## Sources

- **Bank of Thailand SME Statistics Series** (BOT, accessed 2026-05) — cost
  ratio anchors for Thai independent café operations. COGS 28–32%, labor
  25–30%, rent+utilities 8–10% are within the published bands for Bangkok
  small-format F&B.
- **Loyverse Sales-by-Receipt CSV Export** documentation (Loyverse Help
  Center, format dated 2025-Q4 / pinned 2026-05) — column ordering and
  canonical values for `Receipt type`, `Payment type`.
- **Bangkok Bank iBanking Statement CSV Export** specification (Bangkok Bank
  customer support docs, pinned 2026-05) — column ordering and canonical
  description-line patterns.
- **Existing W1-2 data-dump files** (the hand-crafted predecessors of what
  this generator replaces) — used as the source for anchor numbers and
  voice/style continuity.

---

## Drift watch

If any of the following happens, this spec needs revision:

- Loyverse changes their CSV export format → update R14 column list, repin date
- Bangkok Bank changes their CSV export format → update R15 column list, repin date
- W1-3 narrative is revised to use different anchor numbers → update the
  Anchor numbers table above and re-run U8's audit
- A future workshop wants the same data shape (e.g., a hypothetical W2
  financial-modeling lesson) → consider refactoring this spec and the
  generator into a small reusable spine
