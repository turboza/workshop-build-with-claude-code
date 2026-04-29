---
description: "Wrap up the active workshop — reconstruct log, summarize, acknowledge"
---

**Important — tool discipline:**

- DO NOT use `TodoWrite` — `workshop-log.md` is the tracking system
- DO NOT use `Agent`, `WebFetch`, `WebSearch`, `EnterPlanMode`
- The only tools you need: `Read`, `Bash`, `Write`, `Edit`

---

## Step 1 — Identify the active workshop

**First, look in the current conversation.** You almost certainly already know which workshop is active:

- A `/start-X-Y` command was used earlier in this session
- You've been reading/writing files in a specific `lesson-modules/W{n}/{x-y}-{slug}/` folder
- The workshop's CLAUDE.md is in your context

If any of those are true: **you already know. Use it.** No globbing, no asking.

**If you genuinely don't know** (cold session, no prior workshop activity in context):

1. Run: `find lesson-modules -name "workshop-log.md" -type f`
2. For each match, check the frontmatter `status:` field
3. Filter to `status: in-progress`
4. Then:
   - **No matches:** *"I don't see an active workshop in this session. Did you start one? Try `/start-1-2` or whichever you want to wrap up."* — stop here
   - **One match:** use it
   - **Multiple matches:** ask the learner — *"I see a few workshops still open: W1-2 and W1-3. Which one are we wrapping up?"* — wait for answer

**Even if you think you know, if there's any doubt: ask.** Better than silently picking wrong.

---

## Step 2 — Say what you're doing

> "Wrapping up [workshop name, e.g. 'W1-2 — Lina's Coffee']. One sec — let me look back through what we did."

If you asked them to clarify in Step 1, skip this and go straight to reading.

---

## Step 3 — Reconstruct the log from conversation memory

**This is the v2.4 shift: the log was empty during the workshop. You now write the full log in one shot, by reading our conversation.**

Read these:

1. `shared-context/workshop-rules.md` (voice rules + §10 logging schema + `/done` behavior)
2. The active `workshop-log.md` (will likely just have frontmatter)
3. The workshop's own `CLAUDE.md` — at the bottom there may be a **`## When /done runs`** section with workshop-specific closing rituals (e.g. W1-2's "Send to Lina"). If it exists, follow it after writing the summary.

Then **walk through your conversation chronologically** and write log entries for what actually happened. Use the schema from §10:

- `## Step N — <title>` for each major beat that happened
- `## Decision — <topic>` for each decision point
- `## Action — <verb>` for each significant mechanic Claude executed
- `## Question raised` if learner asked something off-script
- `## Stuck moment` if learner got stuck
- `## Insight surfaced` for each meaningful number/pattern revealed

**Content rules — factual, never interpretive:**

- ✅ "Learner spotted Oct revenue: ~฿850K"
- ✅ "Decision — Categories: 6 default categories accepted"
- ❌ "Learner mistakenly read Nov first" (interpretive)
- ❌ "Learner seemed unsure" (interpretive)

**Skip setup beats** — comfort checks, environment checks, "have you used Cursor before" don't go in the log.

Write the entries to the log file using `Write` (replacing the empty body) or `Edit`. Single shot.

---

## Step 4 — Classify state

- **Completed:** all major Step entries present + success-point hit + bonus chapters done
- **Checkpoint-completed:** success point hit, mid-bonus
- **Checkpoint-incomplete:** success point not hit, but real progress made
- **Aborted:** very early stop

---

## Step 5 — Append the Summary block

Append a `## Summary` block at the bottom of the log with:
- Status (one of the four above)
- Real progress in 3–5 specific bullets — the actual decisions, files, insights. Never generic.
- Where they left off, in concrete terms (never "we ran out of time" — say "the X is the same shape, ~5 min when you come back")
- Files produced (with paths)
- Closed-at timestamp

Update the frontmatter `status:` field to `checkpointed` (or `completed` if all bonus done).

---

## Step 6 — Speak to the learner (bullet list)

Use voice rules. Lead with brief affirmation OK ("Great" / "Nice"), then **a bullet list** of 3+ specific named accomplishments. Acknowledge effort warmly even if incomplete.

Example shape:

```
Nice. Specifically what just happened today:

- you designed columns from scratch
- picked categories that cover all 7 files cleanly
- ran the merge of 762 rows from 7 different formats into one
- surfaced the ฿810K fixed-floor number that's going straight to the bank
- wrote Lina something she can actually send

The columns design is the hard part — the rest is the same shape every time.
You did the hard part.
```

For incomplete state, name what *did* happen + reframe what's left:

```
Quick wrap. We got:

- columns locked
- 4 of 6 files merged
- the Highland Beans typos caught

The other 2 files are the same shape — 5-minute lift when you come back.
```

---

## Step 7 — Silently commit the work

Run `git add . && git commit -m "<workshop ID>: <one-line summary>"`. If the repo isn't initialized, run `git init` first, also silently. **Don't surface this as a teaching moment** — no "let's commit your work!" framing. Just save the snapshot.

If the commit fails for some reason, ignore quietly. The summary stands.

---

## Step 8 — Workshop-specific closing ritual

If the workshop's own `CLAUDE.md` has a **`## When /done runs`** section, execute that now. This is where workshop-specific moments live (e.g., W1-2's "Send to Lina" voice memo).

If the workshop has no closing-ritual section, skip this step.

---

## Step 9 — Offer reflection (skippable)

> "Two questions if you've got 3 minutes — totally skippable: what surprised you in the data? what would you do differently next time?"

If they answer, append to log under `## Reflection`.

---

## Step 10 — Tell them what's next

Pull this from the workshop's `CLAUDE.md` if specified, or use the default:

> "Your work is saved. When you're ready for the next workshop, just type `/start-X-Y`."

---

## Important — do NOT close the conversation

If the learner keeps working after `/done`, new entries go under a `## Post-done exploration` section in the log. The summary stands.
