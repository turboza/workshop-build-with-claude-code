---
workshop: W1-2 Lina's Coffee — Messy to Organized
status: checkpointed
started: 2026-04-28T00:00:00
---

# Workshop Log

## Step 1 — Read Lina's email
Learner asked for a summary rather than the full read. Got the short version: bank meeting Friday, accountant quit, 6 files of scattered data, Lina wants to know if branch 2 actually makes sense.

## Step 2 — Surveyed data dump
Read all 6 files: POS (~500 rows, voided transactions), expenses (3 tabs, mixed Thai/English categories), bank statement (K-Bank, debit/credit format), supplier invoices (Doi Chaang spelled multiple ways), payroll (5 staff, some cash extras), rent/utilities (plain text file). Noted the mess is between files, not within them. Decision pending on schema-first vs file-first approach — learner typed /done before picking.

## Summary
**Status:** Checkpoint-incomplete — surveyed all 6 files, no consolidation yet

**Real progress:**
- Got oriented: understood Lina's situation and Friday deadline
- Opened and read all 6 source files — POS, expenses, bank statement, supplier invoices, payroll, rent/utilities
- Spotted the key messiness: vendor name variations (Doi Chaang spellings), mixed Thai/English categories, voided POS rows, plain text rent file
- Reached the schema decision point — the next step is picking a shape, then merging

**Where we left off:** schema-first vs file-first decision — either path converges to the same place. When you come back, pick one and we'll be into the merge within 2 minutes.

**Files produced:** none yet — consolidation hadn't started

**Closed at:** 2026-04-28T00:00:00
