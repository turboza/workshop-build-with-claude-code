---
date: 2026-05-11
topic: w1-2-data-realism
focus: make Lina's Coffee data realistic for finance-pro learners without raising complexity
mode: repo-grounded
---

# Ideation: W1-2 Lina's Coffee — Data Realism

## Grounding Context

**Current state of `lesson-modules/W1/1-2-linas-coffee/data-dump/`:**

| File | Reality check |
|---|---|
| `monthly_revenue.txt` | Lina's headline ฿850K–฿1.05M/mo, total ~฿5.7M |
| `pos_export_oct2025-mar2026.csv` | Only ~520 rows over 6 months — sums to ~฿36K. avg ฿70/txn × 520 ≠ ฿5.7M. **Credibility crack.** |
| `expenses_2025.csv` | 40 rows in a contrived "3 tabs jammed together" shape with mid-file behavior changes |
| `bank_statement_abc.csv` | Balance Oct→Mar: ฿304K → ฿479K = **+฿175K net**, not the +฿800K the workshop claims |
| `supplier_invoices.csv` | Looks realistic — Highland Beans price creep 520→680/kg is well-seeded |
| `staff_payroll.csv` | Realistic — 4 staff × 6 months, cash extras for Maya |
| `rent_utilities.txt` | Realistic |

**Core problem:** The data doesn't internally reconcile. `CLAUDE.md` (the workshop script) at lines 587–591 has to warn *"Do not sum both types together — that double-counts."* That warning is a paper-over for the inconsistency between `monthly_revenue.txt` (฿5.7M) and the POS sample (~฿36K). Clean, internally-consistent data would let the warning disappear and the workshop would get **simpler**.

**Related W1 files:**
- `builder-tools/W1/consolidate-template.py` — the merge script the workshop copies in (currently encodes the `revenue_summary` vs `revenue` split to prevent double-counting)
- `lesson-modules/W1/1-3-linas-dashboard/data/consolidated.csv` — W1-3 consumes the same shape; a generator compounds across both workshops

## Topic Axes

- **A.** Data realism — magnitudes & ratios that finance pros recognize
- **B.** Internal consistency — POS ↔ bank ↔ expenses ↔ headline all tie out
- **C.** Sourcing approach — real dataset vs deterministic generator vs hand-edit
- **D.** Pedagogical impact — does the workshop script get simpler?
- **E.** File shape & schema authenticity — do columns look like real POS/bank exports?

## Ranked Ideas

### 1. Make POS the single source of truth; delete `monthly_revenue.txt`
**Description:** Generate POS at realistic volume (~1,800–2,200 transactions over 6 months; ~10–15/day; avg ticket ~฿95–฿130; bimodal hours 7–9am / 4–6pm) summing to the same ~฿5.7M Lina quotes. Delete `monthly_revenue.txt`. The headline becomes derivable.
**Axis:** B + D
**Basis:** `direct:` `1-2-linas-coffee/CLAUDE.md` lines 587–591 — *"Do not sum both types together — that double-counts. The script tags them differently exactly to prevent this."* The warning exists only because the data is inconsistent.
**Rationale:** Eliminates the workshop's biggest credibility crack and simultaneously simplifies the script — the `type=revenue_summary` vs `type=revenue` split in `consolidate-template.py` goes away.
**Downsides:** Larger CSV (~2K rows vs 520) — lands inside the existing ReprEng viewer beat ("real exports are this big").
**Confidence:** 90%
**Complexity:** Medium
**Status:** Unexplored

### 2. Build a deterministic generator in `builder-tools/W1/`
**Description:** One Python script (`generate-linas-data.py`) with a fixed seed that emits all source files from one ledger. Documented distributions: ticket size, hourly traffic curve, void rate (~3–4%), COGS ratio (~30%), labor ratio (~30%), rent/utilities (~10–12%), FX, supplier price drift. Re-runnable.
**Axis:** C
**Basis:** `reasoned:` Current `data-dump/` was hand-crafted — that's why inconsistencies leaked (bank balance doesn't tie, POS is "sample"). A generator forces mathematical consistency because every number flows from one ledger. `builder-tools/W1/` already exists and contains `consolidate-template.py`, so this is the natural home.
**Rationale:** Compounds across W1-2 *and* W1-3 (same `consolidated.csv` feeds the dashboard). Lets you vary scenarios per cohort without hand-edit churn. Documented seed = stable for instructor support.
**Downsides:** ~1 day to build the first time. After that, it's the foundation.
**Confidence:** 85%
**Complexity:** Medium
**Status:** Explored

### 3. Reconcile bank statement to POS deposits and document owner draws
**Description:** Bank deposits should roughly match POS card+QR revenue minus merchant fees (~2%). Net cash growth = revenue − expenses − owner draws (ATM withdrawals). Currently Oct→Mar shows +฿175K but the workshop claims net ~฿800K. Make the math tie.
**Axis:** B
**Basis:** `direct:` `bank_statement_abc.csv` opening 2025-10-05 ฿304,795, closing 2026-03-29 ฿479,565 = +฿174,770. Workshop script line 594 states net ~฿800K. A finance pro reconciles these in 15 seconds and loses trust.
**Rationale:** "Does the bank tie to the P&L?" is the #1 thing a CFO/accountant looks at. If it does, they relax. Cheap to fix once a generator exists.
**Downsides:** Slightly more cash-flow logic in the generator. Worth it.
**Confidence:** 90%
**Complexity:** Low (once generator exists)
**Status:** Unexplored

### 4. Replace the "3 tabs in one CSV" with one coherent expenses file
**Description:** `expenses_2025.csv` currently has `tab` as the first column and shifts behavior mid-file (Q4-2025 fills `category_raw`; Jan-2026 leaves it blank; Feb-Mar-2026 uses different vendor formatting). Replace with one clean schema with realistic mess: occasional blank category, ~3 USD entries (imported parts), 2–3 vendor-name spelling variants, mixed case.
**Axis:** A + E
**Basis:** `direct:` Reading `expenses_2025.csv` lines 1–41 shows three different patterns in the same file. No real spreadsheet looks like this.
**Rationale:** Real-world mess is systematic (one accountant's quirks across the file), not three pasted-together schemas. Teaching point survives.
**Downsides:** Loses the "three tabs" Easter egg — wasn't load-bearing.
**Confidence:** 80%
**Complexity:** Low
**Status:** Unexplored

### 5. Match real Thai POS + bank export schemas (Loyverse + Bangkok Bank)
**Description:** Use Loyverse's actual receipt-export columns for POS (`Receipt date`, `Receipt number`, `Item name`, `Variant`, `Quantity`, `Gross sales`, `Discount`, `Net sales`, `Cost`, `Tax`, `Payment type`, `Receipt type`). Use Bangkok Bank's actual statement columns (`Date`, `Time`, `Description`, `Withdrawal`, `Deposit`, `Balance`, `Channel`).
**Axis:** E + A
**Basis:** `external:` Loyverse is the dominant POS in Bangkok specialty cafés (public CSV export spec). Bangkok Bank publishes their iBanking CSV format. 5 minutes to look up; one column-rename per file in the generator.
**Rationale:** Tiny effort, big "this is real" payoff. Finance-pro learners who try this at work hit the same shapes.
**Downsides:** Slight risk of column names changing in future Loyverse versions — version-pin in a comment.
**Confidence:** 75%
**Complexity:** Low
**Status:** Unexplored

### 6. Document every messy thing in a builder-side spec
**Description:** Write `builder-tools/W1/data-spec.md` listing each piece of mess and what it represents: vendor-name variants (data-entry drift), USD entries (imported equipment), supplier price creep (Highland Beans 520→680), void cluster (Maya/t02/Tue-Wed evenings), Maya's cash extras (informal incentive), ATM withdrawals (owner draws).
**Axis:** A
**Basis:** `direct:` Bonus chapter A is supplier price creep; bonus chapter B is void cluster (line 698: *"~85% on terminal t02, mostly Tue/Wed evenings, mostly staff s003 (Maya)"*). These patterns currently live implicitly across the CSVs.
**Rationale:** Compounds with idea #2 (the generator needs a spec to generate from). Makes "find the pattern" beats reliable.
**Downsides:** None real — just documentation.
**Confidence:** 85%
**Complexity:** Low
**Status:** Unexplored

### 7. Skip "find a real dataset"; adopt realistic-distributions playbook
**Description:** Direct answer to the user's "should we search for actual dataset" question. **No** — (a) real Thai café data has privacy/licensing problems, (b) public datasets like Maven's *Coffee Shop Sales* are US prices/format and need full rewriting, (c) the value is realistic *distributions*, not real rows.
**Axis:** C
**Basis:** `reasoned:` "Real-enough + clean = simpler" is correct, but "real-enough" means distributions match reality (ticket sizes, hourly traffic, COGS ratios, void rates), not that rows are scraped from a real café.
**Rationale:** Saves a week of dataset hunting and licensing checks. Bank of Thailand SME benchmarks + public Loyverse export examples is all the "reality" needed.
**Downsides:** Requires trusting the distributions — cite sources in `data-spec.md`.
**Confidence:** 90%
**Complexity:** Low (it's a decision, not a build)
**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Scale revenue 10× (฿57M/yr) | Out of scope — user said "don't increase complexity"; ฿5.7M is correct magnitude for a single-branch Bangkok specialty café |
| 2 | Add a data-dictionary file inside `data-dump/` | Breaks the workshop's read-each-file pedagogy in Beat 2; spec belongs builder-side (covered by #6) |
| 3 | Cross-domain analogy framing (poker training, etc.) | Interesting framing but actionable move is already #2 + #7 |
| 4 | Split POS schema match and bank schema match into separate ideas | Merged into #5 — same work, same teaching value |
| 5 | Reduce file count from 7 to 5–6 as its own move | Naturally falls out of #1 (drop `monthly_revenue.txt`) — no separate work needed |

## Shortest Path

Ideas **1 + 2 + 3** are the load-bearing trio. Build the generator (#2), have it enforce reconciliation (#3), let it eliminate the redundant headline file (#1). #4, #5, #6 are polish that ride on the generator. #7 is the meta-answer to the dataset question.
