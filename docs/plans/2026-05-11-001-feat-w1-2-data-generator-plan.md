---
date: 2026-05-11
type: feat
status: completed
origin: docs/brainstorms/2026-05-11-w1-2-data-generator-requirements.md
---

## Implementation notes (2026-05-11)

- **U3 row count.** Planning estimate of 1,800–2,200 POS rows under-counted: hitting ฿5.7M at ~฿95–฿130 avg ticket over 182 days requires ~250 tx/day → ~46K rows. Generator emits 43,843 sale + 280 void rows; revenue and all other invariants still pass. The test-scenario bound in U3 is wrong, not the generator.
- **U6 invariants.** Generator runs 9 checks, not the 7 listed in the plan — adds AE4 (void cluster ≥80% on Maya/t02/Tue-Wed/16–18) and AE5 (Highland price arc 520→580→620→680) as direct disk-read assertions alongside R20–R26. All 9 pass on `--seed 42`.
- **U8 audit outcome.** No W1-3 prose changes required. The plan recommended moving from "~75% cost ratio" to "~86%" based on R20+R26 implying ~86% total expense; on inspection, R26 is fixed-floor only (payroll + rent/util over 6 months), not total expense. The `consolidated.csv` carries bookkeeper-tracked expenses only (~30% of revenue) and W1-3's own line 78 already documents that the ฿700K/mo expense baseline is a narrative anchor, not a CSV-derived figure. Leak patterns (void cluster on Maya, Highland 520→680, scaled dead-zone framing, scaled loyalty abuse) remain empirically supportable against the new data.
- **AE2 determinism.** Verified across processes: `--seed 42 --out-dir /tmp/a` and `--out-dir /tmp/b` produce byte-identical output.


# feat: W1-2 Lina's Coffee — Deterministic Data Generator

## Summary

Build a single Python generator at `builder-tools/W1/generate-linas-data.py` that emits all W1-2 source files from one internal ledger with a fixed seed. The generator enforces mathematical reconciliation across POS, bank statement, expenses, suppliers, payroll, and rent/utilities so finance-pro learners trust the numbers. Drop the redundant `monthly_revenue.txt`, simplify `consolidate-template.py`, and audit W1-3 for hardcoded numbers that must move in lockstep.

---

## Problem Frame

The current hand-crafted data in `lesson-modules/W1/1-2-linas-coffee/data-dump/` has three credibility-breaking inconsistencies (see origin: `docs/brainstorms/2026-05-11-w1-2-data-generator-requirements.md`):

1. POS sums to ~฿36K but `monthly_revenue.txt` claims ฿5.7M (avg ฿70 × 520 sample rows ≠ headline)
2. Bank statement net change is +฿175K, not the +฿800K the workshop claims
3. `expenses_2025.csv` switches schema mid-file across three "tabs"

The W1-2 workshop script papers this over with a "Do not sum both types together" warning (`lesson-modules/W1/1-2-linas-coffee/CLAUDE.md` lines 587–591). Cleaning the data lets that warning disappear and makes both W1-2 and W1-3 numerically coherent.

Cross-workshop dependency surfaced during planning: W1-3 hardcodes specific numbers (avg revenue ฿950K/mo, fixed floor ฿810K, four leak amounts totaling ~฿756K/yr, supplier price 520→680). The generator must hit these landmarks so W1-3 doesn't break when it re-consumes the regenerated `consolidated.csv`.

---

## Requirements Traceability

Origin requirements covered by this plan:

- **R1–R6** (generator interface): U2
- **R7–R13** (output files): U3, U4, U5
- **R14–R16** (schemas): U3 (POS/Loyverse), U4 (bank/Bangkok Bank)
- **R17–R19** (seeded patterns: price creep, void cluster, vendor variants): U3, U5
- **R20–R26** (reconciliation invariants): U6
- **R27–R28** (builder-side data-spec.md): U1
- **R29–R31** (workshop script + consolidate template ripple): U7
- **R32** (W1-3 dashboard data refresh): U8

Acceptance examples covered: AE1, AE2 → U6; AE3 → U4, U6; AE4 → U3; AE5 → U5; AE6 → U7.

Deferred-to-planning questions from origin are resolved in Key Technical Decisions below.

---

## Output Structure

```
workshop/
├── builder-tools/W1/
│   ├── generate-linas-data.py        # NEW — the generator
│   ├── data-spec.md                  # NEW — distributions, sources, seeded patterns
│   └── consolidate-template.py       # MODIFIED — drop revenue_summary branch
├── lesson-modules/W1/1-2-linas-coffee/
│   ├── CLAUDE.md                     # MODIFIED — BEAT 2 file table, BEAT 10 warning
│   └── data-dump/                    # REGENERATED (was 7 files, now 6)
│       ├── pos_export_oct2025-mar2026.csv   # ~2K rows, Loyverse schema
│       ├── expenses_2025.csv         # single coherent schema
│       ├── bank_statement_abc.csv    # Bangkok Bank schema
│       ├── supplier_invoices.csv
│       ├── staff_payroll.csv
│       └── rent_utilities.txt
│       # monthly_revenue.txt — DELETED
└── lesson-modules/W1/1-3-linas-dashboard/
    ├── CLAUDE.md                     # AUDITED (may need number tweaks)
    └── data/consolidated.csv         # REGENERATED via the new pipeline
```

The per-unit `**Files:**` sections remain authoritative.

---

## High-Level Technical Design

*This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

**Single-ledger architecture:** the generator builds one complete in-memory record of every economic event (sale, expense, payroll, transfer, owner draw) keyed by timestamp, then projects each output file as a different view of that ledger. Reconciliation is invariant-by-construction rather than invariant-by-check — the bank deposits literally point at the same POS rows they're settling.

```
                ┌──────────────────────────────────┐
                │   Spec (data-spec.md targets)    │
                │   - revenue ฿5.7M ±2%            │
                │   - ratios (COGS/labor/rent/...) │
                │   - seeded patterns              │
                └────────────┬─────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  build_ledger(seed)          │
              │  → List[Event]               │
              │    (sales, expenses, payroll,│
              │     transfers, owner_draws)  │
              └────┬─────┬──────┬─────┬──────┘
                   │     │      │     │
       ┌───────────┘     │      │     └───────────┐
       ▼                 ▼      ▼                 ▼
  project_pos()  project_bank()  project_expenses()  project_*()
       │                 │              │                  │
       ▼                 ▼              ▼                  ▼
  pos_export.csv   bank_statement.csv  expenses.csv  suppliers/payroll/rent
                             │
                             ▼
                ┌──────────────────────────────┐
                │  verify_invariants(ledger,   │
                │                    files)    │
                │  R20–R26 — exits non-zero    │
                │  on any breach               │
                └──────────────────────────────┘
```

The "settlement linkage" between POS card+QR rows and bank `POS_DEPOSIT` rows is what makes invariant R21 hold to the baht: bank deposits are computed by aggregating POS card+QR amounts by deposit batch (typical T+1 settlement window) minus a flat ~2% merchant fee. The ledger holds the link; the projections read it.

---

## Implementation Units

### U1. Author `data-spec.md` — single source of truth for distributions and patterns

**Goal:** Produce the builder-side spec that drives every downstream decision in the generator. The generator imports specific constants from this spec (or co-locates them); the spec also serves as the human-readable rationale for "why these numbers".

**Requirements:** R27, R28

**Dependencies:** none (first unit)

**Files:**
- `builder-tools/W1/data-spec.md` (create)

**Approach:**

Capture in plain markdown:
- Window: Oct 2025–Mar 2026 (6 months, 182 days)
- Revenue target: ฿5,700,000 ±2%; monthly distribution Oct/Nov/Dec/Jan/Feb/Mar ≈ 850/920/1050/890/970/1020 (฿K)
- Avg ticket: ฿95–฿130 with sub-distributions by product category (espresso ~ ฿55–฿95, milk-based ~ ฿75–฿100, pastry ~ ฿45–฿65)
- Hourly traffic: bimodal — morning peak 7–9am, afternoon peak 4–6pm, lunch lull, evening drop-off; weekend bump ~+15%
- Cost ratios over 6 months: COGS ~30% (~฿1.71M), labor ~28% (~฿1.60M), rent+util ~9% (~฿513K), other operating ~5% (~฿285K), net retained ~14% (~฿800K). Cross-check: payroll+rent_util fixed floor = ฿810K ±5% (R26).
- Payment mix: ~50% QR (PromptPay), ~30% card, ~20% cash
- Void rate: ~3.5% of transactions; ≥80% concentrated on staff `s003` (Maya) + terminal `t02` + Tue/Wed + 16:00–18:00 window (R18)
- Supplier price progression: Highland Beans 520 → 580 (Nov) → 620 (Jan) → 680 (Feb) THB/kg (R17)
- Vendor name variants: `Highland Beans Co.`, `HighlandBeans Co`, `Highland Beans` (R19)
- USD entries: ~3 in expenses (Italian Espresso Parts, Ethiopian Beans Direct, Imported beans) at FX 1 USD = 32 THB
- Owner draws: ~฿70K–฿100K total via ATM withdrawals across the window
- W1-3 anchor numbers the generator must preserve: monthly revenue avg ฿950K, fixed floor ฿810K, void/price-creep/dead-zone/loyalty leak patterns visible (amounts are scaled estimates in W1-3, not direct sums)
- Sources cited: Bank of Thailand SME benchmark series (cost-ratio anchors), Loyverse public CSV export format docs, Bangkok Bank iBanking statement format. Version-pin retrieval date.

Include a "How to regenerate" stub pointing at U2.

**Patterns to follow:** match the prose style of existing `lesson-modules/W1/*/CLAUDE.md` scripts — concrete numbers, plain English, no jargon. Use markdown tables for distributions.

**Test scenarios:** none — pure documentation. The spec's correctness is validated indirectly by U6's invariants.

**Verification:** A reader who has never seen this workshop can answer "why is the void cluster on Tuesday/Wednesday late afternoon?" by reading this file alone.

---

### U2. Build the ledger engine and CLI entrypoint

**Goal:** Construct the deterministic in-memory ledger of all economic events, with a fixed-seed RNG and a runnable CLI. No output files produced yet — that's U3–U5.

**Requirements:** R1, R2, R3, R4

**Dependencies:** U1 (consumes the targets from `data-spec.md`)

**Files:**
- `builder-tools/W1/generate-linas-data.py` (create — ledger module + CLI skeleton; projections stubbed for now)

**Approach:**

Single Python file, stdlib only (`random`, `csv`, `datetime`, `argparse`, `dataclasses`, `pathlib`).

Sketch:

```
@dataclass class Event:
    timestamp, kind, amount_thb, currency, vendor, staff, terminal,
    payment_method, category, notes, source_view  # which file(s) project it

def build_ledger(rng) -> list[Event]:
    events = []
    events += generate_sales(rng)        # ~2K POS rows w/ seeded void cluster
    events += generate_supplier_orders(rng)  # ~65 rows w/ price progression
    events += generate_expense_lines(rng)    # ~50 rows w/ USD entries, vendor variants
    events += generate_payroll(rng)          # 24 rows
    events += generate_rent_utilities(rng)   # fixed monthlies + annuals
    events += generate_owner_draws(rng)      # ATM withdrawals
    events += derive_bank_deposits(events)   # from card+QR settlement batches
    return sorted(events, key=lambda e: e.timestamp)

CLI: --seed (default 42), --out-dir (default lesson-modules/W1/1-2-linas-coffee/data-dump/)
```

RNG strategy: single `random.Random(seed)` instance threaded through `generate_*` helpers. Verified deterministic across CPython 3.9–3.13 (resolves origin Deferred question on RNG).

Idempotency: U2 also implements the "older than 5 minutes + looks hand-edited" heuristic in R5 as a stderr warning gate, not a hard block.

**Execution note:** Test-first for the ledger contract — write a single integration test that asserts `len(build_ledger(seed=42)) == len(build_ledger(seed=42))` and that every event has the seven required fields before writing the body.

**Patterns to follow:**
- Header comment shape from existing `builder-tools/W1/consolidate-template.py` lines 1–13
- stdlib-only philosophy from same file (no pandas, no third-party deps)

**Test scenarios:**
- Determinism: `build_ledger(rng=random.Random(42))` returns an event list whose lengths, timestamps, amounts, and string fields are identical across two invocations in the same Python process.
- Determinism across processes: invoking `python3 generate-linas-data.py --seed 42 --out-dir /tmp/a` and `--out-dir /tmp/b` produces byte-identical output files (covers AE2).
- Seed honored: `--seed 7` produces a meaningfully different ledger than `--seed 42` (different first event amount).
- CLI defaults: invoking with no args resolves `--out-dir` to `lesson-modules/W1/1-2-linas-coffee/data-dump/` relative to the script's location.
- Idempotency warning: re-running into a populated out-dir where one file has been hand-edited prints a stderr warning naming that file, but proceeds with the regeneration.
- stdlib-only: `python3 -c "import generate_linas_data"` works in a venv with no extra packages installed.

**Verification:** Running `python3 builder-tools/W1/generate-linas-data.py --seed 42 --dry-run` (a flag added for development) prints "Ledger: N events" and exits 0 without writing files. N is stable across runs.

---

### U3. Project the POS file (Loyverse schema) with seeded void cluster

**Goal:** Emit `pos_export_oct2025-mar2026.csv` (~1,800–2,200 rows) using Loyverse-style columns from the ledger, with the bonus-chapter-B void cluster honored.

**Requirements:** R7, R14, R16, R18

**Dependencies:** U2

**Files:**
- `builder-tools/W1/generate-linas-data.py` (modify — add `project_pos()`)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/pos_export_oct2025-mar2026.csv` (regenerate)

**Approach:**

Columns (resolves origin Deferred question on exact Loyverse format): `Receipt date`, `Receipt number`, `Item name`, `Variant`, `Quantity`, `Gross sales`, `Discount`, `Net sales`, `Cost`, `Payment type`, `Receipt type`, `Customer`, plus workshop-specific tail `staff_id`, `terminal_id`, `notes`. Version-pin the Loyverse format date in a header comment.

The void cluster lives in `generate_sales()` (U2) — `project_pos()` is a faithful CSV writer with no extra logic. The cluster is generated as ~70 void events placed in the ledger at Tue/Wed 16:00–18:00, staff `s003`, terminal `t02`, with `Receipt type=Void` and negative `Net sales`. Roughly 17/20 voids match the cluster signature per AE4.

**Patterns to follow:** Existing `pos_export_oct2025-mar2026.csv` column ordering for `staff_id`, `terminal_id`, `notes` tail (preserves backward compatibility with `consolidate-template.py` reads).

**Test scenarios:**
- Row count: 1,800 ≤ count ≤ 2,200 for default seed.
- Schema: header row matches the documented Loyverse column list exactly.
- Revenue total: Σ(`Net sales` where `Receipt type=Sale`) is within ±2% of ฿5,700,000 (covers R20).
- **Covers AE4.** Filter rows where `Receipt type=Void`: ≥80% land on staff `s003`, terminal `t02`, weekday in (Tue, Wed), and time-of-day 16:00–18:00.
- Total void count: 60 ≤ voids ≤ 90 (~3.5% of ~2K rows).
- Payment mix: QR ≈ 50% ±5%, card ≈ 30% ±5%, cash ≈ 20% ±5%.
- Hourly distribution: peak hour count in 7–9 and 16–18 windows is each ≥2× the count in the 10–14 lull window.

**Verification:** Opening `pos_export_oct2025-mar2026.csv` in the ReprEng CSV viewer (the workshop's installed extension) shows a coherent table that looks like a real Loyverse export.

---

### U4. Project the bank statement (Bangkok Bank schema) with deposit linkage

**Goal:** Emit `bank_statement_abc.csv` (~120 rows) using Bangkok Bank-style columns. Deposits settle POS card+QR revenue minus fees; withdrawals reflect supplier transfers, rent, utilities, payroll, owner draws.

**Requirements:** R9, R15, R16, R21, R23, R24, R25

**Dependencies:** U2

**Files:**
- `builder-tools/W1/generate-linas-data.py` (modify — add `project_bank()` and `derive_bank_deposits()`)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/bank_statement_abc.csv` (regenerate)

**Approach:**

Columns (resolves origin Deferred question on exact Bangkok Bank format): `Date`, `Time`, `Description`, `Withdrawal`, `Deposit`, `Balance`, `Channel`. Version-pin the iBanking CSV format date in a header comment.

`derive_bank_deposits()` aggregates POS card+QR events into daily settlement batches (T+1 typical) minus a 2.0% merchant fee. This produces `POS DEPOSIT MERCHANT` rows whose totals equal Σ(POS card+QR) × 0.98 to the baht.

Withdrawals come from:
- Supplier transfers (`TFR <date> TRANSFER <last 10 of phone>`) tied to supplier invoices
- Rent (`TFR ... NK PROPERTY`) on the 5th of each month
- Utilities (`CITY WATER UTIL`, `CITY POWER ELECTRIC`, `FASTNET INTERNET`) at the recorded amounts in `rent_utilities.txt`
- Payroll (`PAYROLL ...` or `TFR ...` on the 25th)
- Owner draws (`ATM WITHDRAWAL LINA`, channel=ATM)

Opening balance: ฿304,795 (preserved from current file to avoid breaking instructor familiarity). Closing balance = opening + Σ(deposits) − Σ(withdrawals), recomputed exactly.

**Patterns to follow:** existing `bank_statement_abc.csv` descriptor strings (`POS DEPOSIT MERCHANT`, `TFR <date> TRANSFER <phone>`, `CITY WATER UTIL`) for visual consistency with the current workshop screenshots.

**Test scenarios:**
- Row count: 100 ≤ count ≤ 140.
- Schema: header row matches the documented Bangkok Bank column list exactly.
- **Covers AE3.** Closing balance equals opening balance + Σ(`Deposit`) − Σ(`Withdrawal`) to the baht (covers R25).
- **Covers AE3.** Σ(`Deposit` where `Description` starts with `POS DEPOSIT`) is within ±2% of (POS card-revenue + POS QR-revenue) × 0.98 (covers R21).
- Payroll outflows: Σ(`Withdrawal` rows tagged payroll) within ±2% of Σ(`staff_payroll.total_paid_thb`) (covers R23).
- Rent/util outflows: Σ(rent + utilities rows) within ±2% of the totals derivable from `rent_utilities.txt` (covers R24).
- ATM withdrawals total: ฿70K ≤ total ≤ ฿100K (owner draws).
- Balance never goes negative.
- Date range: every row date is in [2025-10-01, 2026-03-31].

**Verification:** A finance pro reading the bank statement can reconcile it to the POS file in ~1 minute and see no discrepancy beyond the 2% merchant fee.

---

### U5. Project expenses, suppliers, payroll, rent/utilities files

**Goal:** Emit the four remaining files. Single coherent schema for `expenses_2025.csv` (replaces the 3-tab gimmick). Preserves Highland Beans price progression and vendor name variants.

**Requirements:** R8, R10, R11, R12, R13, R17, R19

**Dependencies:** U2

**Files:**
- `builder-tools/W1/generate-linas-data.py` (modify — add `project_expenses()`, `project_suppliers()`, `project_payroll()`, `project_rent_utilities()`)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/expenses_2025.csv` (regenerate, new schema)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/supplier_invoices.csv` (regenerate, current schema)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/staff_payroll.csv` (regenerate, current schema)
- `lesson-modules/W1/1-2-linas-coffee/data-dump/rent_utilities.txt` (regenerate, current shape)

**Approach:**

`expenses_2025.csv` new single-coherent schema: `date`, `vendor`, `category`, `amount`, `currency`, `amount_thb`, `notes` (drop the `tab` column entirely; drop the mid-file behavior change). Realistic mess: ~2 rows with blank `category` (data-entry drift), ~3 rows in USD (imported parts/beans) with FX note in `notes`, ~3 rows with mixed-case category labels (`Pastry` vs `pastry`).

`supplier_invoices.csv` keeps current schema. Highland Beans rows use the three-variant spelling distributed across the file. Price progression encoded as step function (resolves origin Deferred question — matches the bonus chapter A narrative "went 520 → 680" cleanly; smooth ramp would obscure the inflection points).

`staff_payroll.csv` and `rent_utilities.txt` keep their current schemas/shapes. Payroll cash extras stay on Maya (s003) at ฿2,000–฿2,500/mo. Rent_utilities preserves the current monthly variation pattern for electric.

All four files get a header comment line (`#` for txt, leading-comment-row for CSV per origin R13) with generator name, seed, and timestamp.

**Patterns to follow:** existing files' column orderings, vendor descriptors, and `notes` conventions preserved where the schema is unchanged.

**Test scenarios:**
- `expenses_2025.csv` no longer has a `tab` column; header is exactly `date,vendor,category,amount,currency,amount_thb,notes`.
- USD entries: exactly 3 rows with `currency=USD`, each with non-empty `notes` mentioning the FX rate.
- Vendor variants: across `supplier_invoices.csv` + `expenses_2025.csv`, the literal strings `Highland Beans Co.`, `HighlandBeans Co`, and `Highland Beans` all appear at least once.
- **Covers AE5.** Reading Highland Beans rows in date order from `supplier_invoices.csv`, `unit_price_thb` progresses through 520 → 580 → 620 → 680 with inflections in November and February (covers R17).
- Payroll: 24 rows, 4 staff × 6 months. Cash extras on s003 (Maya) every month.
- Rent/util: `rent_utilities.txt` lists rent ฿45K/mo, water average, internet ฿1,290/mo flat, electric varying Oct–Mar, plus annual property tax and insurance.
- Σ(supplier `total_thb` for coffee categories) within ±5% of the corresponding expense lines in `expenses_2025.csv` (covers R22).

**Verification:** Opening `expenses_2025.csv` in the ReprEng viewer shows a clean single-schema table — no mid-file behavior change.

---

### U6. Reconciliation invariants and report

**Goal:** After all files are written, recompute every invariant from the files themselves (not the in-memory ledger) and print a reconciliation report. Non-zero exit on any breach.

**Requirements:** R6, R20–R26

**Dependencies:** U3, U4, U5

**Files:**
- `builder-tools/W1/generate-linas-data.py` (modify — add `verify_invariants()` and reporting block)

**Approach:**

Read back every generated file via `csv.DictReader` and compute:
1. Σ(POS Net sales where Sale) → must be ฿5.7M ±2% (R20)
2. Σ(POS card+QR) × 0.98 ↔ Σ(bank POS_DEPOSIT) within ±1% (R21)
3. Σ(supplier total_thb for coffee/dairy/pastry) ↔ corresponding expense category sums within ±5% (R22)
4. Σ(payroll total_paid_thb) ↔ bank payroll outflows within ±2% (R23)
5. Σ(rent + utilities from rent_utilities.txt) ↔ bank rent+util outflows within ±2% (R24)
6. Bank closing = opening + Σ(deposits) − Σ(withdrawals) exactly (R25)
7. Σ(payroll) + Σ(rent+utilities) over 6 months → ฿810K ±5% (R26)

Each invariant prints `[OK]` or `[FAIL]` with computed vs expected values. After all checks, print one-line summary (e.g., `7/7 invariants passed. Wrote 6 files to .../data-dump/`). Exit code = number of failed invariants.

**Patterns to follow:** Report output style from existing `consolidate-template.py` lines 282–289 (45-char rule, padded labels, comma-formatted numbers).

**Test scenarios:**
- **Covers AE1.** Fresh run with default seed: all 7 invariants `[OK]`, exit 0.
- Tampering detection: manually edit one row in `pos_export_oct2025-mar2026.csv` to a wildly wrong amount, re-run only the `verify_invariants()` step → R20 or R21 reports `[FAIL]` and exit code > 0.
- Read-back independence: invariants compute from files on disk, not from `build_ledger()`'s in-memory ledger (this protects against the "script computes from itself" trap).
- Report format: each invariant line includes "expected", "actual", "tolerance" so the failure is debuggable without reading code.

**Verification:** `python3 builder-tools/W1/generate-linas-data.py; echo "exit=$?"` prints the report and `exit=0` for an unmodified run.

---

### U7. Update workshop script and `consolidate-template.py` ripple

**Goal:** Drop the `monthly_revenue.txt` row from BEAT 2's file table, remove the "Two revenue types — don't double-count" warning from BEAT 10, and remove the `type=revenue_summary` branch from `consolidate-template.py`. These edits are small but load-bearing — they're the reason this work exists.

**Requirements:** R29, R30, R31

**Dependencies:** U3, U4, U5, U6 (so the generated data exists before script edits go in)

**Files:**
- `lesson-modules/W1/1-2-linas-coffee/CLAUDE.md` (modify — BEAT 2 file table at lines ~220–228; BEAT 10 warning at lines ~587–591; the `revenue_summary` reference at line ~590)
- `builder-tools/W1/consolidate-template.py` (modify — remove lines ~66–88 monthly_revenue.txt section; remove `revenue_summary` from the report at lines ~278, ~285)

**Approach:**

`CLAUDE.md` BEAT 2 table: drop row 1 (`monthly_revenue.txt`), update POS row to "~2,000 transactions (full window)". Renumber rows 2–7 to 1–6.

`CLAUDE.md` BEAT 10: replace the entire "Two revenue types — read carefully" subsection with a single line: "Revenue is the sum of `type=revenue` rows. The headline ฿5.7M Lina quotes is exactly that sum." Update the example Insight 1 to reference the POS-derived number directly. Update example Insight 3 if its specifics depended on the removed warning context.

`consolidate-template.py`: delete the entire "1. monthly_revenue.txt" section (lines ~66–88) and its `MONTH_MAP` constant. Renumber the subsequent file section headings (2→1, 3→2, etc.). Drop the `revenue_summary = sum(...)` calculation and the corresponding report line. Update the docstring at lines 9–13 to reflect single-typed revenue.

**Patterns to follow:** Existing script's `Say:` / `Suggest something like:` markers — keep voice consistent with the rest of the workshop.

**Test scenarios:**
- **Covers AE6.** BEAT 2 file table lists exactly 6 files (no `monthly_revenue.txt` row).
- BEAT 10 contains no occurrence of "double-count" or "revenue_summary" or "Two revenue types".
- `consolidate-template.py` contains no occurrence of "revenue_summary" or "monthly_revenue.txt".
- Running the updated `consolidate-template.py` against the regenerated `data-dump/` produces `consolidated.csv` with a single `type=revenue` value summing to ฿5.7M ±2%.
- The /done command flow in BEAT 12 still works — the "🍵 Lina voice memo" still references ฿810K fixed floor (preserved by R26).
- No broken `@filename` references in the script — every `@data-dump/X` mention has X in the new file list.

**Verification:** Doing a full dry-run of the W1-2 workshop script start-to-finish never produces a contradictory or impossible instruction.

---

### U8. Audit and refresh W1-3 dashboard data dependencies

**Goal:** Regenerate `lesson-modules/W1/1-3-linas-dashboard/data/consolidated.csv` from the new pipeline and audit `1-3-linas-dashboard/CLAUDE.md` for hardcoded numbers that may need to move with the new data. This resolves origin Deferred-to-Planning question 4.

**Requirements:** R32

**Dependencies:** U7 (consolidate-template.py must be updated first)

**Files:**
- `lesson-modules/W1/1-3-linas-dashboard/data/consolidated.csv` (regenerate)
- `lesson-modules/W1/1-3-linas-dashboard/CLAUDE.md` (audit; modify only if numbers diverge meaningfully)

**Approach:**

Step 1: Run the new pipeline (`generate-linas-data.py` then `consolidate.py`) to produce a fresh `consolidated.csv`, copy it to W1-3's `data/`.

Step 2: Audit `1-3-linas-dashboard/CLAUDE.md` for numerical references. Known anchors from grep:
- Monthly revenue ฿950K avg (line 74) — generator hits ~฿950K/mo avg by construction; verify within ±2%
- Monthly expense ฿700K (line 75, 78) — derives from cost-ratio target; if the new pipeline produces ฿810K/mo avg expense (consistent with ~86% cost ratio implied by R20+R26), W1-3's "฿700K/mo at 75% cost ratio" prose needs reconciling. Two options: (a) update W1-3 prose to the ~86% ratio actually produced, or (b) deliberately tune the generator's "other operating" bucket downward to land at 75% cost ratio. Recommend (a) — the W1-3 narrative survives the change, and the higher cost ratio is more honest for an independent Bangkok café.
- Fixed floor ฿810K (lines 272, 374) — preserved by R26
- Leak amounts ฿216K / ฿144K / ฿300K / ฿96K (lines 64–67, 394–397) — these are *scaled estimates* extrapolated from the sample data, not direct sums. W1-3 already notes "patterns from sample, scaled to full revenue volume" — the scaling logic should still hold because the patterns themselves (void cluster, price creep) are preserved. Verify the scaling commentary still reads sensibly.
- Highland Beans 520→680 (line 65) — preserved by R17
- Branch-2 inputs: ฿950K rev, ฿700K exp, ฿4M loan (line 276) — same reconcile as above

Step 3: Apply only the prose adjustments required. Do not touch W1-3 numbers that still hold.

**Test scenarios:**
- The regenerated `1-3-linas-dashboard/data/consolidated.csv` row count and totals are consistent with the W1-3 narrative within ±2% on every named number, OR the narrative has been updated to match the new totals.
- No reference in `1-3-linas-dashboard/CLAUDE.md` claims a number that the consolidated CSV cannot back up.
- The 4 leak patterns (void cluster, supplier price creep, dead-zone hours, loyalty discount abuse) are still empirically visible in the new `consolidated.csv` under the same filters W1-3 uses.

**Verification:** Dry-running the W1-3 workshop's BEAT-equivalent leak-card section produces numbers that match the W1-3 script.

---

## Key Technical Decisions

- **Single-ledger architecture over per-file independent generators.** Reconciliation invariant-by-construction (bank deposits literally reference POS rows) is more robust than invariant-by-check. Cost is slightly more upfront design; payoff is the invariants in U6 don't have to do real math, just verification.
- **stdlib only (no pandas, no faker).** Matches the workshop's "no extra setup" feel and avoids dependency drift across cohorts. CPython 3.9–3.13 compatible with `random.Random(seed)`. Resolves origin Deferred question on RNG.
- **Step-function supplier price progression, not smooth ramp.** Resolves origin Deferred question. Matches the bonus chapter A narrative ("went ฿520 → ฿680") cleanly; inflection points stay legible.
- **Loyverse + Bangkok Bank exact column orderings looked up and version-pinned at implementation time.** Origin Deferred — implementer downloads a sample of each at U3/U4 start and pins the format date in a header comment. Future schema drift is a separate maintenance task (acknowledged in origin Scope Boundaries).
- **Default seed `42`, printed in every output file's header comment.** Trivial choice, but documented so anyone investigating a generated file can regenerate it.
- **Preserve `bank_statement_abc.csv` opening balance ฿304,795 and existing descriptor strings.** Keeps continuity with current workshop screenshots and instructor familiarity. The closing balance becomes a derived quantity.
- **Cost-ratio reconciliation: prefer ~86% cost ratio in U8 audit, not 75%.** W1-3 currently says "~75% cost ratio" but its quoted numbers (฿800K net on ฿5.7M revenue) imply ~86%. Update W1-3 prose; the higher ratio is more honest for an independent Bangkok café.
- **Reconciliation invariants read from disk, not from in-memory ledger.** Prevents the "script computes from itself and always passes" failure mode. The verification step is a true cross-check.

---

## System-Wide Impact

- **W1-2 workshop script gets shorter.** BEAT 2's table loses a row; BEAT 10 loses the "don't double-count" warning subsection; `consolidate-template.py` loses ~25 lines and a constant.
- **W1-3 workshop inherits the same consistent data.** Same `consolidated.csv` shape; numbers tie. Audit step in U8 ensures the narrative survives.
- **Instructor familiarity preserved.** All file names, the headline ฿5.7M, fixed-floor ฿810K, void-cluster Maya/t02/Tue-Wed, Highland Beans 520→680 — the touchstones the workshop refers to verbally — survive verbatim.
- **No learner-facing behavior change.** Learners still see "messy" data in BEAT 2 and clean output in BEAT 9; the mess is now systematic and realistic instead of contrived.
- **Future scenarios.** The single-ledger design leaves `--scenario` as a plausible v2 (good month / bad month / two-branch) without rework.

---

## Scope Boundaries

- Out: W1-1 (pomodoro) and any other workshop's data — this generator is W1-2 only.
- Out: `--scenario` flag for good/bad/two-branch variants — explicitly deferred.
- Out: Loyverse or Bangkok Bank API integration — match the export schemas only.
- Out: separate pytest test suite for the generator — the disk-read invariants in U6 serve as self-verification.
- Out: automated regeneration on `git pull` — generation is a builder-side step.

### Deferred to Follow-Up Work

- `--scenario` flag exploration once the v1 generator has shipped one cohort.
- Auto-detect Loyverse / Bangkok Bank schema drift (e.g., a small `verify-schemas.py` that downloads current samples and diffs against the pinned format date).
- Backport: if a future workshop wants the same shape (e.g., a hypothetical W2 financial-modeling lesson), refactor `data-spec.md` and `generate-linas-data.py` to a small reusable spine.

---

## Dependencies / Assumptions

- Python 3.9+ on the builder's machine (`python3` is already the workshop's pinned interpreter).
- Loyverse and Bangkok Bank publish their CSV export schemas; the implementer downloads samples at U3/U4 start and pins the format date.
- Bank of Thailand SME benchmark figures (referenced in U1) are publicly available as of 2026-05.
- W1-3's narrative survives a cost-ratio adjustment from 75% → ~86% (covered in U8 audit; if the user disagrees, U8 reverts to the alternative "tune the generator to 75%" path).
- The workshop git repository's CSV files are not gitignored — generated outputs are committed deliberately so each cohort sees the same data.

---

## Risks and Mitigations

- **Risk: U8 reveals W1-3 has more hardcoded numbers than the grep surfaced.** Mitigation: U8 lists known anchors but also instructs a fresh grep over `1-3-linas-dashboard/CLAUDE.md` for `฿`, `K`, `%` before declaring done.
- **Risk: Loyverse or Bangkok Bank schema changed since 2025 and the implementer pins an outdated format.** Mitigation: version-pin the retrieval date in a code comment; document in U1 spec; treat schema drift as a separate maintenance task.
- **Risk: The implementer over-engineers `data-spec.md` into a long document.** Mitigation: this is a builder reference, not a polished doc — target 1-2 screens of content.
- **Risk: Determinism breaks across Python minor versions due to `random` algorithm changes.** Mitigation: `random.Random` is documented stable across Python 3.x. If breakage is observed, pin Python version in the header comment alongside the seed.

---

## Outstanding Questions

### Resolve Before Implementation

- None. All resolutions captured in Key Technical Decisions above.

### Deferred to Implementation

- [Affects U3, U4][Needs research] Exact current Loyverse CSV export column order and exact current Bangkok Bank iBanking CSV export column order — implementer downloads samples at unit start, pins format date.
- [Affects U8][Technical] If the cost-ratio reconciliation in U8 surfaces other W1-3 narrative drift the planning-time grep missed, decide whether to scope into this plan or punt to a follow-up.
- [Affects U2][Technical] Final shape of the `Event` dataclass — fields listed are illustrative; implementer may add/rename based on what projections actually need.
