---
description: "End-of-session reflection — pulls today's logs, runs a short interview, writes one file the learner pastes into the feedback form"
---

**Important — tool discipline:**

- DO NOT use `TodoWrite` — this is a single-pass flow, no task tracking
- DO NOT use `Agent`, `WebFetch`, `WebSearch`, `EnterPlanMode`
- The only tools you need: `Read`, `Bash`, `Write` — all interview questions are plain conversational text

---

## Step 1 — Find today's workshop logs

Run: `find lesson-modules -name "workshop-log.md" -type f`

For each match, read the frontmatter `closed:` date. Keep the ones closed today (or, if none today, the most recent session date — a single calendar day's worth).

Group the kept logs by week (path is `lesson-modules/W{n}/...`).

- **No logs found at all:** *"I don't see any workshop logs yet. Run `/done` after a workshop first, then come back."* — stop here.
- **Logs from one week only:** that's the week. Continue.
- **Logs from multiple weeks:** ask which week to wrap up. Wait for answer.

---

## Step 2 — Confirm the week

Say:

> *"Looks like today was Week {n} — wrapping that up?"*

If yes, continue. If no, ask which week and adjust.

---

## Step 3 — Read the agenda + log summaries

Read these in parallel:

1. `lesson-modules/W{n}/CLAUDE.md` — pull the `## Session agenda` bullets
2. Each of today's `workshop-log.md` files — pull the `## Summary` block (and `## Reflection` block if present)

If `lesson-modules/W{n}/CLAUDE.md` doesn't exist or has no `## Session agenda` section, fall back to listing the workshops by name from the logs only — don't invent lecture content.

---

## Step 4 — Mirror back what happened

Speak to the learner. Use voice rules from `shared-context/workshop-rules.md`. Lead with the agenda (so lectures and discussions are acknowledged, not just builds), then the build-specific bullets pulled from the log summaries.

Example shape:

```
Wrapping up Week {n}. Quick look back at today:

We covered:
- {agenda bullet 1}
- {agenda bullet 2}
- ...

What you actually built:
- {one bullet per workshop, pulled from its Summary block — name the artifact + the standout moment}
- ...

That's a real day. A few quick questions before we close — should take ~5 min.
```

Keep the bullets concrete. Pull verbatim from the log summaries — don't editorialize.

---

## Step 5 — Interview

Six questions. Keep moving — if the learner gives a one-liner, accept it and continue. If they write a paragraph, ask one natural follow-up ("oh — say more about {their thing}?") then move on.

**Q1 — Lectures & discussions** (plain chat)

Ask conversationally:

> *"Beyond the workshops, today also had {2–3 lecture/discussion items from the agenda}. Anything from those that stuck with you — or surprised you?"*

Skippable — if they say "not really" or leave it blank, move on.

**Q2 — Satisfaction** (plain chat)

> *"How was today overall — 1 (rough) to 5 (great)? Just drop a number."*

**Q3 — Favorite moment** (plain chat)

Anchor with concrete options pulled from their own log summaries:

> *"Favorite moment today — the {workshop 1-1 standout}? The {workshop 1-2 standout}? The {workshop 1-3 standout}? Or something else?"*

They can pick one, name something else, or write a paragraph. All fine.

If they give a short answer, reflect it back with a light invitation: *"{their word} — say more if you want."* If they move on or keep it short, move to Q4 immediately. Never ask twice.

**Q4 — Friction** (plain chat)

> *"Anything that felt fuzzy, slow, or frustrating? Even small stuff — the best feedback is the thing you almost didn't mention."*

If they give a short answer, reflect it back: *"{their thing} — anything behind that?"* If they move on, move on. Never ask twice.

**Q5 — Application** (plain chat)

> *"Where might you use Claude Code this week — work, side project, something at home? Even a half-formed idea counts."*

**Q6 — Open mic** (plain chat)

> *"Anything else for Turbo or the organizers? Skip if nothing."*

Optional — accept a blank reply or "nope" and move on.

---

## Step 6 — Compile the wrap-up file

Write to `lesson-modules/W{n}/W{n}-wrap-up.md`. If a file already exists, overwrite it (single file per week is the convention).

Schema:

```markdown
# Week {n} Wrap-up — {YYYY-MM-DD}

## Today's session

**What we covered:**
- {agenda bullets verbatim from W{n}/CLAUDE.md}

**What I built:**
- {one bullet per workshop — name + 1-line standout, pulled from log summaries}

## Reflection

**How it went (1–5):** {Q2 answer}

**What stuck from the lectures/discussions**
{Q1 verbatim, or "—" if skipped}

**Favorite moment**
{Q3 verbatim}

**What was fuzzy or frustrating**
{Q4 verbatim}

**Where I'll use this**
{Q5 verbatim}

**Anything else**
{Q6 verbatim, or "—" if skipped}

---

## Appendix — workshop summaries

### Workshop {X-Y} — {workshop name}
{paste the ## Summary block from this workshop's log, including files produced + where left off}

### Workshop {X-Y} — {workshop name}
{...}
```

Use `Write` to create the file in one shot.

---

## Step 7 — Hand off to the form

**Always surface the form link explicitly** — never assume the learner knows where it is or will ask.

Look up the form URL for the detected week from the table below, then say:

```
Done. Your wrap-up is at: lesson-modules/W{n}/W{n}-wrap-up.md

To submit:
1. Open the file (cmd+click the path above) and skim — edit anything you don't want to share
2. Open the feedback form: {form URL}
3. Copy the whole file → paste into the "Reflection & Feedback Note" field

Thanks for showing up today.
```

**Form URL lookup (per week):**

- W1: `https://docs.google.com/forms/d/e/1FAIpQLSfKRsJeFFo1NSe02HwXxyjeKJIZMIg6snHKDKgqT_TpZ3tVvw/viewform?usp=pp_url&entry.1696846533=Week+1`
- W2–W8: not yet wired — say *"The form for Week {n} isn't set up yet — send your wrap-up file to Turbo directly."*

---

## Step 8 — Silently commit

Run `git add . && git commit -m "W{n} wrap-up"`. If it fails (no git, nothing to commit), ignore quietly. The file stands.

Don't surface this as a teaching moment.

---

## Important — do NOT close the conversation

If the learner keeps talking after the wrap-up file is written, just respond normally. The wrap-up file stands.
