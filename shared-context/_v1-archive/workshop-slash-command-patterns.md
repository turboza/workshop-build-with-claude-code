---
type: knowledge
created: 2026-04-28
scope: reusable-across-weeks
sources: [workshop-ta-core.md, workshop-ta-pattern-carl-teardown.md]
---

# Workshop Slash Command Patterns

The reusable spec for every slash command used in workshops. New workshops in W2-W8 should follow these patterns. Voice and coaching rules are in [workshop-ta-core.md](workshop-ta-core.md).

---

## The standard set

| Command | Purpose | When called |
|---|---|---|
| `/start-X-Y` | Begin a workshop | Learner ready to start workshop X.Y |
| `/done-X-Y` | Checkpoint a workshop (regardless of completion) | End of workshop time, OR learner moves on |
| `/help-im-stuck` | Formal unstick | Anytime learner feels stuck |
| `/recap-workshop` | End-of-session synthesis across all workshops | Final 10 min of the 3-hour session |
| `/instructor-status` | Read learner state for triage (instructor uses) | When a learner raises hand |

Plus per-week creative commands as needed (e.g. `/review-my-progress` — folded into `/recap-workshop` for W1).

---

## Architecture: thin shim + rich context

Borrowed from Carl's course teardown. Each `.claude/commands/start-X-Y.md` is a tiny redirector (~10 lines) that points Claude at the rich context files.

```markdown
---
description: Start Workshop X-Y
---

Silently read these files to understand how to run this workshop:

1. knowledge/workshop-ta-core.md — your voice and coaching rules
2. knowledge/workshop-journaling-and-recap-spec.md — how to log the session
3. knowledge/workshop-fx-reference.md — currency conversion table (if currency-related)
4. weeks/W{n}/scripts/workshop-X-Y-script.md — the actual workshop script

Once read, begin Workshop X-Y. Do not narrate that you read these files.
The learner just sees the workshop start.
```

Why this pattern:
- Slash command file stays trivial — easy to maintain, version, copy across weeks
- Updating voice rules in one place (`workshop-ta-core.md`) updates every workshop
- Cursor users can paste the same script files into Composer with a single instruction

---

## `/start-X-Y` — begin a workshop

**What Claude does on invocation:**

1. Reads core rules + this workshop's script
2. Checks if a prior workshop log exists in the same session (e.g. `/start-1-3` checks for `workshop-1-2-log.md`). If yes, reads it and references at least one prior decision in the opening.
3. Checks if the *current* workshop already has a log. If yes — the learner started this workshop before without `/done`-ing it. Claude says: *"Looks like we started this one already and didn't wrap up. Want to `/done-X-Y` first to checkpoint, then start fresh? Or pick up where we left off?"*
4. Begins the script with the scenario hook.

**The learner experience:** they type `/start-1-2`, Claude reads files silently, then opens with the scenario.

---

## `/done-X-Y` — checkpoint, regardless of completion

This is the most important command in the system. See [workshop-journaling-and-recap-spec.md](workshop-journaling-and-recap-spec.md) for full spec.

**Two trigger paths:**

1. **Instructor calls time** — *"Everyone, type `/done-1-2` now."*
2. **Learner self-triggers** — they want to move on, or feel finished

**What `/done-X-Y` does:**

1. Reads the current `workshop-X-Y-log.md`
2. Identifies what was actually accomplished (decisions, files produced, key moments)
3. Writes a structured **Summary block** to the bottom of the log
4. Acknowledges progress in the [TA voice](workshop-ta-core.md) — specific, named, proportional, no fake praise
5. Offers reflection (optional, time-permitting): 2-3 questions the learner can answer or skip
6. Marks the log as "checkpointed" (a marker that `/recap-workshop` looks for)
7. Tells the learner what's next: *"Next up: workshop 1-3. Type `/start-1-3` whenever you're ready."*

**Critical: `/done` does NOT block further work.** If time remains, the learner can keep exploring. New entries go under a "Post-done exploration" section. The summary stands; the work continues.

**When called on incomplete state:**
- Names the real progress in concrete terms
- Does not say "we didn't finish" — says "we got through X and Y; Z is the next piece when you come back to it"
- The summary is written from where they actually are, not where the script ended

---

## `/help-im-stuck` — formal unstick

**Default behavior:**

1. Claude takes a breath: *"All good — let's slow down for a sec."*
2. Recaps where they are in 1-2 sentences (read from workshop log)
3. Asks: *"What's feeling off? Pick one if it fits, or tell me in your own words: (a) I'm not sure what to type, (b) something errored and I don't get it, (c) I lost the thread of what we're doing, (d) something else."*
4. Branches based on answer:
   - (a) → re-prompts the exact next thing to type
   - (b) → reads the error, explains, suggests the fix
   - (c) → re-grounds in the scenario and current goal in plain language
   - (d) → open dialogue
5. Logs the stuck-moment to the workshop log (so instructor can see patterns later)

**Voice rule:** never imply it's the learner's fault. Default attribution is to the script or the explanation, not the learner.

---

## `/recap-workshop` — end-of-session synthesis

Runs at the end of the 3-hour session. Reads all workshop logs from the day (W1-2, W1-3, etc.) and produces:

1. **Session highlights** — top 3 concrete things accomplished
2. **Decisions made** — schemas chosen, leaks found, dashboards built
3. **Reflection prompts** — 3-4 questions the learner answers in the form
4. **What surprised you / what's still confusing** — from the logs
5. **A snippet for the progress report** — formatted text the learner pastes into the post-session form

The output is a markdown file: `workshops/W1-recap-YYYY-MM-DD.md`. Learner reads it, fills the form, optional commit.

See [workshop-journaling-and-recap-spec.md](workshop-journaling-and-recap-spec.md) for the data shape.

---

## `/instructor-status` — triage surface

Run by the **instructor** on a learner's machine when they raise a hand.

**What it does:**

1. Reads the most recent workshop log in the project
2. Extracts: which workshop, current step, last 5 actions, any error markers, any stuck-events
3. Outputs a 4-line summary the instructor reads in 20 sec:

```
Workshop: 1-2 (Messy → Organized)
Step: 4 of 7 (consolidating files)
Recent: chose 6-category schema; merged 3 vendor name spellings
Stuck signal: tried twice to convert dates, both failed
```

4. Optionally suggests 1-2 things the instructor can ask: *"Possible nudge: 'have you checked the date format in `expenses_2025.xlsx`?'"*

**No magic.** It's just a log reader. Built for W1 because the journaling system already produces the data.

---

## How to write a new `/start-X-Y` for W2+

1. Copy the W1 template in `.claude/commands/start-1-2.md`
2. Update the workshop script reference path
3. Confirm voice rules ([workshop-ta-core.md](workshop-ta-core.md)) and journaling ([workshop-journaling-and-recap-spec.md](workshop-journaling-and-recap-spec.md)) are loaded
4. Add any week-specific context files (e.g. `workshop-fx-reference.md` if currency, `workshop-cursor-basics.md` if introducing new tool basics)
5. Test on a dry-run learner before live class

---

## When this file changes

Update this file when a new command pattern proves useful across multiple weeks (e.g. `/show-the-goal`, `/peer-share`). Then update [CLAUDE.md](../CLAUDE.md).
