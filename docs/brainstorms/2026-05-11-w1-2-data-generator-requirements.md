---
date: 2026-05-11
topic: w1-2-data-generator
---

# W1-2 Lina's Coffee — Deterministic Data Generator

## Summary

Build a single Python generator at `builder-tools/W1/generate-linas-data.py` that emits all source files for the W1-2 workshop from one internal ledger with a fixed seed. The generator enforces mathematical reconciliation across POS, bank statement, expenses, suppliers, and payroll so finance-pro learners trust the numbers and the workshop script can drop its current "don't double-count" warning.

---

## Problem Frame

The current `lesson-modules/W1/1-2-linas-coffee/data-dump/` was hand-crafted. Three inconsistencies leak through:

1. **POS sums to ~฿36K but the headline claims ฿5.7M.** Avg ฿70/txn × 520 sample rows doesn't approach the figure in `monthly_revenue.txt`. A financial professional notices in seconds and the workshop loses credibility.
2. **Bank statement net change is +฿175K, not +฿800K.** The opening/closing balances don't tie to the P&L the workshop later claims.
3. **`expenses_2025.csv` switches schema mid-file.** Three "tabs" jammed into one CSV with shifting column behavior; not how any real spreadsheet looks.

The W1-2 workshop script (`lesson-modules/W1/1-2-linas-coffee/CLAUDE.md` lines 587–591) papers this over with an explicit warning to learners: *"Do not sum both types together — that double-counts. The script tags them differently exactly to prevent this."* That warning exists only because the data is inconsistent. Hand-editing CSVs to fix this is fragile and the inconsistencies will drift back the next time anything changes.

---

## Assumptions

*This requirements doc was authored without synchronous user confirmation. The items below are agent inferences that fill gaps in the input — un-validated bets that should be reviewed before planning proceeds.*

- POS transaction volume: ~1,800–2,200 rows over 6 months (~10–15/day), avg ticket ฿95–฿130, bimodal hours 7–9am and 4–6pm with weekend bump.
- Revenue total: ฿5.7M ±2% (preserves Lina's quoted headline so downstream workshop beats still hit familiar numbers).
- Cost ratios: COGS ~30%, labor ~28%, rent+util ~9%, other ~6%, net margin ~15%.
- Seasonality: Dec +~20% (holiday + corporate orders), Feb +~5%, Mar +~8%.
- Void rate ~3.5%, concentrated on staff `s003` (Maya) / terminal `t02` / Tue–Wed 16:00–18:00 — preserves the bonus chapter B "find the void cluster" beat.
- Highland Beans supplier price progression 520 → 580 → 620 → 680 THB/kg across Oct–Mar — preserves bonus chapter A "spot the price creep" beat.
- 3 vendor-name spelling variants for Highland Beans (`Highland Beans Co.`, `HighlandBeans Co`, `Highland Beans`) distributed across supplier and expense files.
- ~3 USD-denominated expense rows (imported equipment parts, imported beans) to preserve the FX teaching moment in Beat 5.
- Owner draws: ATM withdrawals total ~฿70K–฿100K over 6 months, plausible Bangkok small-business owner pattern.
- Final file count: 6 (drops `monthly_revenue.txt`).
- Python stdlib only (no pandas, no third-party deps) — matches the workshop's "no extra setup" feel for the builder side too.
- Default seed: `42`. The seed value appears in a header comment in every generated file so anyone investigating later can regenerate.

---

## Actors

- A1. **Workshop builder (you)**: runs the generator before publishing a workshop cohort; reviews the printed reconciliation report; edits `data-spec.md` when seeded patterns change.
- A2. **Workshop learner (finance pro)**: reads the generated files during the W1-2 workshop; expects numbers that reconcile to what a real Bangkok coffee shop would look like.
- A3. **Workshop instructor**: relies on patterns being consistently present (void cluster, price creep, vendor variants) so the bonus chapters work every cohort.

---

## Requirements

**Generator interface**
- R1. Single Python file at `builder-tools/W1/generate-linas-data.py`, runnable as `python3 generate-linas-data.py [--seed N] [--out-dir PATH]`.
- R2. Default `--seed 42`. Default `--out-dir lesson-modules/W1/1-2-linas-coffee/data-dump/`.
- R3. Uses Python stdlib only (no pandas, no faker, no third-party deps).
- R4. Deterministic: same seed → byte-identical output.
- R5. Idempotent: re-running overwrites existing files. Warns to stderr if `--out-dir` contains files older than 5 minutes that look hand-edited (heuristic: differs from what generator would produce with the same seed).
- R6. Prints a reconciliation report to stdout at the end (see R20–R26).

**Output files (drop `monthly_revenue.txt`; emit these 6 files):**
- R7. `pos_export_oct2025-mar2026.csv` — ~1,800–2,200 transactions Oct 2025–Mar 2026, Loyverse-shaped columns (see R14).
- R8. `expenses_2025.csv` — ~50 rows, single coherent schema (date, vendor, category, amount, currency, amount_thb, notes) with realistic mess: occasional blank category, ~3 USD entries, mixed-case category labels.
- R9. `bank_statement_abc.csv` — Bangkok Bank-shaped columns (see R15), ~120 rows covering Oct 2025–Mar 2026.
- R10. `supplier_invoices.csv` — ~65 rows, current schema preserved.
- R11. `staff_payroll.csv` — 24 rows (4 staff × 6 months), current schema preserved.
- R12. `rent_utilities.txt` — plain text, current shape preserved.
- R13. Every generated CSV/txt begins with a header comment (`#` or `--`) recording the generator filename, seed, and generation timestamp so anyone investigating can regenerate.

**File schemas**
- R14. POS file uses Loyverse-style columns: `Receipt date`, `Receipt number`, `Item name`, `Variant`, `Quantity`, `Gross sales`, `Discount`, `Net sales`, `Cost`, `Payment type`, `Receipt type` (`Sale`/`Refund`/`Void`), `Customer`, plus workshop-specific extras `staff_id`, `terminal_id` retained from current file.
- R15. Bank file uses Bangkok Bank-style columns: `Date`, `Time`, `Description`, `Withdrawal`, `Deposit`, `Balance`, `Channel` (`Counter`/`ATM`/`Online`/`POS`).
- R16. Column names should be straight from the actual export specs; version-pin in a comment at top of `generate-linas-data.py` so a future Loyverse format change is traceable.

**Seeded patterns (must survive every regeneration)**
- R17. Highland Beans price progression: 520 → 580 → 620 → 680 THB/kg across Oct/Nov/Jan/Feb. Visible in `supplier_invoices.csv` and as line-item amounts in `expenses_2025.csv`.
- R18. Void cluster on POS: ~17 of ~20 voids on Maya (`s003`) / terminal `t02` / Tue or Wed / 16:00–18:00 window.
- R19. Vendor-name spelling variants: Highland Beans appears as `Highland Beans Co.`, `HighlandBeans Co`, and `Highland Beans` across at least two files.

**Reconciliation invariants (printed at end of run; non-zero exit if any fails)**
- R20. Σ(POS `Net sales` where `Receipt type=Sale`) is within ±2% of ฿5,700,000.
- R21. Σ(POS card+QR payments) − merchant fees (~2%) is within ±2% of Σ(bank deposits where Channel=POS).
- R22. Σ(supplier `total_thb`) is consistent with the corresponding category rows in `expenses_2025.csv` (Coffee Beans, Dairy & Pastry) within ±5%.
- R23. Σ(payroll `total_paid_thb`) appears as outflows in `bank_statement_abc.csv` within ±2% of payroll total (cash extras for Maya may show as ATM withdrawals rather than transfers — invariant accepts either).
- R24. Σ(rent + utilities) per `rent_utilities.txt` matches monthly outflows visible in the bank statement within ±2%.
- R25. Bank closing balance = opening balance + Σ(deposits) − Σ(withdrawals), exactly (no rounding drift).
- R26. "Fixed floor" (Σ payroll + Σ rent/utilities over 6 months) lands at ฿810K ±5% — preserves the workshop's headline insight in BEAT 10.

**Builder-side spec**
- R27. Write `builder-tools/W1/data-spec.md` (separate file, also generated or hand-maintained — author's choice) documenting each seeded pattern, its purpose in the workshop, and which file(s) it lives in. Sections at minimum: revenue distribution, void cluster, supplier price creep, vendor name variants, USD entries, owner draws, fixed-floor calculation.
- R28. `data-spec.md` cites sources for distribution choices (Bank of Thailand SME benchmarks, public Loyverse export documentation) so the "is this realistic?" question has a paper trail.

**Workshop-script ripple changes (in scope; minimal edits)**
- R29. Update `lesson-modules/W1/1-2-linas-coffee/CLAUDE.md` BEAT 2 file table to list 6 files (remove `monthly_revenue.txt` row, update POS row count to ~2K).
- R30. Update BEAT 10 to remove the "Two revenue types — read carefully… Do not sum both types together" warning, since `revenue_summary` rows no longer exist.
- R31. Update `builder-tools/W1/consolidate-template.py` to drop the `type=revenue_summary` branch; revenue is single-typed.
- R32. Update `lesson-modules/W1/1-3-linas-dashboard/data/consolidated.csv` to be the output of the new pipeline so W1-3 inherits the consistent data.

---

## Acceptance Examples

- AE1. **Covers R4, R5.** Given the generator has never been run, when the workshop builder runs `python3 generate-linas-data.py`, then 6 files appear in `data-dump/`, the reconciliation report prints to stdout with all invariants passing, and the script exits 0.
- AE2. **Covers R4.** Given the generator was run yesterday with seed 42, when run again today with seed 42, then every output file is byte-identical to yesterday's output.
- AE3. **Covers R20, R21, R25.** Given a fresh run, when the builder opens the generated `bank_statement_abc.csv`, then the closing balance equals opening + deposits − withdrawals to the baht, and the deposit total matches POS card+QR revenue minus ~2% merchant fees.
- AE4. **Covers R18.** Given a fresh run, when the builder filters POS rows where `Receipt type=Void`, then ≥80% land on staff `s003`, terminal `t02`, weekday in (Tue, Wed), and time-of-day 16:00–18:00 — preserving bonus chapter B's promised cluster.
- AE5. **Covers R17.** Given a fresh run, when the builder reads supplier invoices for Highland Beans in chronological order, then unit prices progress through 520 → 580 → 620 → 680 THB/kg with the inflection points in Nov and Feb.
- AE6. **Covers R29, R30, R31.** Given the new data is in place, when a learner runs through the W1-2 workshop, then the BEAT 10 output produces a single revenue total derived from POS alone (no `revenue_summary` rows to skip) and the "don't double-count" warning is no longer needed in the script.

---

## Success Criteria

- A financial professional running the workshop does not flinch at any number — totals, ratios, and balances all tie out under casual reconciliation.
- The W1-2 workshop script gets **shorter**, not longer: the double-counting warning is gone, the consolidate template has one fewer branch, and the file table in BEAT 2 has one fewer row.
- Re-running the generator for the next cohort takes <30 seconds and produces identical output every time.
- The instructor can point to `data-spec.md` to explain why every "mess" in the data is there, and what real-world phenomenon it represents.
- A planner picking up `ce-plan` from this doc has enough product specification to write a build plan without re-asking what should be in each file or which invariants must hold.

---

## Scope Boundaries

- Out: generating data for W1-1 (pomodoro) or any other workshop. This generator is W1-2 only; W1-3 reuses the W1-2 consolidated.csv but does not need its own generator.
- Out: multiple scenarios (good month / bad month, single-branch / two-branch). A `--scenario` flag is a plausible v2 addition but is not required for the first version.
- Out: a Loyverse or Bangkok Bank API integration. Match the export schemas; don't try to be the actual product.
- Out: a test suite for the generator. The reconciliation invariants printed at end of run (R20–R26) serve as self-verification; if any invariant fails, the script exits non-zero.
- Out: regeneration on every `git pull`. Generation is a builder-side step run by you when you change the spec, not a learner-side step.
- Out: synchronising the script with future Loyverse / Bangkok Bank schema changes automatically. R16 records the version pinned; future schema drift is a separate maintenance task.

---

## Key Decisions

- **Single ledger drives all files**: the generator constructs a complete in-memory ledger of every transaction (sales, expense, transfer, owner draw) first, then projects different views of that ledger into each file. This is what makes reconciliation invariant-by-construction rather than invariant-by-check.
- **Loyverse + Bangkok Bank schemas chosen** over generic "looks like a POS export" / "looks like a bank statement": Loyverse is dominant in Bangkok specialty cafés and Bangkok Bank publishes their iBanking CSV format. Tiny effort, big "this is real" payoff for learners who try this at work.
- **Drop `monthly_revenue.txt`** rather than try to make POS sum to its claimed value while keeping both files. Two sources of truth was the root problem; one source of truth fixes it permanently.
- **Reconciliation as exit code**, not just printed report: makes the generator fail-loud if a future spec edit breaks an invariant, which protects the cohort handoff.
- **Synthetic-from-distribution** over real-dataset hunting: idea #7 from the ideation doc. Real Thai café data has privacy/licensing problems; public datasets are US-priced. What we want is realistic distributions, not real rows.

---

## Dependencies / Assumptions

- Python 3.9+ available on the builder's machine (workshop targets `python3` already, so this is a no-cost dependency).
- Bank of Thailand SME benchmark figures and Loyverse/Bangkok Bank export specs are publicly documented as of 2026-05; cite specific versions in `data-spec.md`.
- W1-3 (`lesson-modules/W1/1-3-linas-dashboard/`) consumes `consolidated.csv` produced from the new data via the existing W1-2 consolidate pipeline. W1-3 script edits are out of scope here but the dashboard team should review whether the new richer POS data changes any of W1-3's pre-baked observations.

---

## Outstanding Questions

### Resolve Before Planning

- None. All product decisions resolved in this doc; remaining unknowns are implementation choices for `ce-plan`.

### Deferred to Planning

- [Affects R3][Technical] Best stdlib RNG strategy for reproducibility across CPython 3.9–3.13: `random.Random(seed)` is sufficient but verify no NumPy-derived helpers sneak in.
- [Affects R14–R16][Needs research] Confirm exact column ordering in current Loyverse CSV export and current Bangkok Bank iBanking CSV export (download a sample of each and pin in `data-spec.md`).
- [Affects R17][Technical] Decide whether supplier price progression is encoded as a step function (cliff increases) or a smooth ramp (gradual). Step function is simpler and matches the current data; verify the bonus chapter narrative still works.
- [Affects R32][Technical] W1-3's `consolidated.csv` was committed to the repo with specific row contents the W1-3 script may reference verbatim. Audit `1-3-linas-dashboard/CLAUDE.md` for any hardcoded numbers before swapping the file.
