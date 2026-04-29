---
type: knowledge
created: 2026-04-28
scope: reusable-across-weeks
purpose: log format and recap synthesis rules used by all workshops
---

# Workshop Journaling & Recap Spec

How each workshop produces a structured log, and how `/done-X-Y` and `/recap-workshop` use that log. Voice rules in [workshop-ta-core.md](workshop-ta-core.md). Command structure in [workshop-slash-command-patterns.md](workshop-slash-command-patterns.md).

---

## Why structured journaling (not native transcripts)

Decided 2026-04-28. Reasons:
- Native Claude Code transcripts are noisy, hash-pathed, OS-specific, and not Cursor-portable
- A curated log lives in the repo, gets committed, becomes a learning artifact
- `/recap-workshop` needs structured input — can't reliably synthesize from raw chat
- Cohort progress reporting needs queryable structure

Trade-off: Claude must be instructed to write entries at specific beats. Built into every workshop SCRIPT.md.

---

## File location and naming

Per-workshop: `workshops/W{n}-{x}-{slug}/workshop-log.md`

Examples:
- `workshops/W1-2-linas-coffee/workshop-log.md`
- `workshops/W1-3-linas-dashboard/workshop-log.md`

Per-session recap: `workshops/W{n}-recap-{YYYY-MM-DD}.md`

---

## Log file format

```markdown
---
workshop: W1-2 Lina's Coffee — Messy to Organized
learner: <name from local config or anonymous>
started: 2026-MM-DDTHH:MM
status: in-progress | checkpointed | completed
---

# Workshop Log

## Step 1 — Reading Lina's email
[short note about what happened]

## Decision — Schema columns
Picked: date, type, category, vendor, description, amount_thb, amount_usd, currency, source_file, notes
Why: matched Lina's mental model (where money goes + when)

## Action — Consolidated 6 files
Output: data/consolidated.csv (1,038 rows)
Notes: merged 3 spellings of Doi Chaang; excluded 8 voided POS entries

## Question raised
Learner asked: "what if we want to break out branch 1 vs branch 2?"
Resolution: noted for W1-3 dashboard

## Stuck moment
Learner re-typed command 3x with no progress on USD conversion
Resolution: re-explained pre-computed columns; moved on

## Insight surfaced
Top spend category: Coffee Beans ฿890,000 (~$27,800), 15% of total

---

## Summary (written by /done-X-Y)
[populated when /done is called — see below]

---

## Post-done exploration
[appended if learner keeps working after /done]
```

---

## Entry types (what Claude writes when)

| Marker | When | What goes in it |
|---|---|---|
| `## Step N — <title>` | At each major beat in the script | One sentence, what happened |
| `## Decision — <topic>` | At every decision point | What was picked + why (one line) |
| `## Action — <verb>` | After Claude executes mechanics | Output file + key numbers |
| `## Question raised` | Learner asks something off-script | Question + how it was handled |
| `## Stuck moment` | Detected stuck (or `/help-im-stuck` called) | What was stuck, what unstuck it |
| `## Insight surfaced` | A meaningful number / pattern revealed | The insight in plain language |

The script tells Claude: *"After this step, append to the log: `## Action — Consolidated 6 files` followed by output file path and row count."*

---

## `/done-X-Y` behavior — the critical command

When called, Claude:

### 1. Reads the log

Pulls all entries above the `## Summary` marker.

### 2. Classifies the state

- **Completed:** all script beats written + success-point hit
- **Checkpoint-completed:** success point hit, mid-bonus-chapter
- **Checkpoint-incomplete:** success point not hit, but real progress made
- **Aborted:** very early stop (rare — handle with extra warmth)

### 3. Writes the Summary block

```markdown
## Summary
**Status:** Checkpoint-incomplete (4 of 6 files consolidated)
**Real progress:**
- Decided on a 10-column schema that fits Lina's mental model
- Successfully merged 4 of 6 files (POS, expenses, bank, suppliers)
- Caught the Doi Chaang vendor name typos and merged 3 spellings
- Surfaced first insight: top spend is Coffee Beans (15% of total)

**Where we left off:** payroll and rent files still to merge — same shape as the others, ~5 min when you come back to it.

**Files produced:**
- data/consolidated.csv (partial, 4 of 6 sources)
- notes-for-lina.md (draft summary)

**Closed at:** 2026-MM-DDTHH:MM
```

### 4. Speaks aloud to the learner — TA voice rules apply

For an incomplete state, **never** say "we didn't finish" or "ran out of time." Say:

> "Quick wrap on what we got done — schema is locked, 4 of the 6 files are merged, and we already caught the Doi Chaang typos. The last 2 files are the same shape as what we just did, so when you come back to this it's a 5-minute lift. The coffee bean number we surfaced is real — that goes to Lina."

### 5. Offers reflection (if time remains, optional)

> "Two reflection questions if you've got 3 minutes — totally skippable:
> - what surprised you in the data?
> - what would you do differently next time?"

If learner answers, Claude appends to log under `## Reflection`. If skipped, no problem.

### 6. Tells learner what's next

> "Next up is W1-3 — the dashboard. Type `/start-1-3` whenever you're ready. Or take the break."

### 7. Marks log status: `checkpointed`

Status field in frontmatter updates. `/recap-workshop` reads this.

### 8. Allows continued work

If learner keeps typing, new entries go under `## Post-done exploration`. Summary stands.

---

## Re-entry protection

If learner types `/start-X-Y` and a log for that workshop already exists *without* a `## Summary` block (i.e. not checkpointed), Claude says:

> "Looks like we started this one before and didn't wrap up. Want to `/done-X-Y` first to checkpoint where we got to, then start fresh? Or pick up from where we left off?"

This protects against losing prior progress and forces explicit continuation.

---

## `/recap-workshop` — end-of-session synthesis

Run at the end of the 3-hour W1 session. Reads all workshop logs from the day.

### Inputs read

- `workshops/W1-1-pomodoro/workshop-log.md`
- `workshops/W1-2-linas-coffee/workshop-log.md`
- `workshops/W1-3-linas-dashboard/workshop-log.md`

(Or whichever exist; some learners may have only completed 2.)

### Output: `workshops/W1-recap-{YYYY-MM-DD}.md`

```markdown
---
session: W1
date: 2026-MM-DD
learner: <name>
workshops_completed: 3
workshops_checkpointed: 0
---

# Session 1 Recap — Meet Claude Code

## What you actually built today
- A working Pomodoro + todo app on localhost (W1-1)
- A consolidated 6-file data sheet for Lina's Coffee (W1-2)
- A 5-section dashboard with branch-2 projections + leak alerts (W1-3)

## Decisions you made
- Schema for the consolidated CSV (10 columns, dual currency)
- 6 expense categories
- Which leak to investigate first
- Dashboard color scheme + filters

## Insights you surfaced
- ฿756,000/year (~$23,600) in fixable leaks across 4 patterns
- Branch 2 break-even moves from month 7 → month 4 if leaks fixed first
- Tuesday-evening void cluster on one till

## What surprised you / what's still confusing
[pulled from log Question raised + Reflection sections]

## Reflection prompts for the form
1. One thing you'll try on your own this week?
2. One question you want answered in W2?
3. On a scale of 1-5, how confident are you to keep going?

## Snippet for the post-session form
[~80-word ready-to-paste summary covering: what built, what learned, what next]
```

### Voice rules apply

The recap is warm but not over-the-top. It names real artifacts and real decisions. No generic "you did great today!"

---

## Cohort dashboard pipeline (future)

Logs are markdown but parseable. Future: a script reads all `workshops/*/workshop-log.md` files across the cohort and aggregates:
- Common stuck moments (helps refine the script)
- Workshop completion rates
- Most surfaced insights
- Reflection patterns

Don't build now. Logs format is forward-compatible.

---

## When this file changes

Update when:
- New entry types prove useful in dry-runs
- Recap output format needs new sections (e.g. peer-share notes)
- Cohort dashboard pipeline is built and needs schema lock-in

Then update [CLAUDE.md](../CLAUDE.md).
