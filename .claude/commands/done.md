---
description: "Wrap up the active workshop — write summary, acknowledge progress"
---

**Important — tool discipline:**

- DO NOT use `TodoWrite` — `workshop-log.md` is the tracking system
- DO NOT use `Agent`, `WebFetch`, `WebSearch`, `EnterPlanMode`
- The only tools you need: `Read`, `Bash`, `Write`, `Edit`

---

## Step 1 — Identify the active workshop

**First, look in the current conversation.** You almost certainly already know which workshop is active because:

- A `/start-X-Y` command was used earlier in this session
- You've been reading/writing files in a specific `lesson-modules/W{n}/{x-y}-{slug}/` folder
- You've been writing to a specific `workshop-log.md`

If any of those are true: **you already know the answer. Use it.** No globbing, no asking.

**If you genuinely don't know** (cold session, no prior workshop activity in context):

1. Run: `find lesson-modules -name "workshop-log.md" -type f`
2. For each match, check the frontmatter `status:` field
3. Filter to `status: in-progress`
4. Then:
   - **No matches:** say *"I don't see an active workshop in this session. Did you start one? Try `/start-1-2` or whichever you want to wrap up."* — stop here.
   - **One match:** use it.
   - **Multiple matches:** ask the learner — *"I see a few workshops still open: W1-2 and W1-3. Which one are we wrapping up?"* — wait for answer.

**Even if you think you know, if there's any doubt: ask.** Better than silently picking wrong.

---

## Step 2 — Say what you're doing

> "Wrapping up [workshop name, e.g. 'W1-2 — Lina's Coffee']. One sec — let me look back through what we did."

If you asked them to clarify in Step 1, skip this and go straight to reading.

---

## Step 3 — Read what's needed

1. Read `shared-context/workshop-rules.md` (voice rules + §10 journaling/done behavior).
2. Read the active `workshop-log.md`.
3. Read the workshop's own `CLAUDE.md` — at the bottom there may be a **`## When `/done` runs`** section with workshop-specific closing rituals (e.g. "send to Lina"). If it exists, follow it after writing the summary.

---

## Step 4 — Classify state

- **Completed:** all major Step entries present + success-point marker + bonus chapters done
- **Checkpoint-completed:** success point hit, mid-bonus
- **Checkpoint-incomplete:** success point not hit, but real progress made
- **Aborted:** very early stop

---

## Step 5 — Write the summary block

Tell the learner first:

> "Logging the wrap-up summary."

Then append a `## Summary` block to the log with:
- Status (one of the four above)
- Real progress in 3–5 specific bullets — name the actual decisions, files, insights. Never generic.
- Where they left off, in concrete terms (never "we ran out of time" — say "the X file is the same shape, ~5 min when you come back")
- Files produced (with paths)
- Closed-at timestamp

Update the log frontmatter `status:` field to `checkpointed` (or `completed` if all bonus done).

---

## Step 6 — Speak to the learner

Use voice rules. Lead with brief affirmation OK ("Great" / "Nice"), then **specific named progress**. Acknowledge effort warmly even if incomplete. 3–4 sentences.

Examples (adapt — don't paste verbatim):

- *"Great — quick wrap on what we got done. Schema is locked, four of the six files are merged, and we already caught the Highland Beans typos. The last two are the same shape — 5-minute lift when you come back."*
- *"Nice. You designed the columns, picked categories, ran the merge, surfaced the fixed-floor insight, and wrote Lina something she can send. Honestly the hard part is the columns — the rest is the same shape every time."*

---

## Step 7 — Workshop-specific closing ritual

If the workshop's own `CLAUDE.md` has a **`## When `/done` runs`** section, execute that now. This is where workshop-specific moments live (e.g., W1-2's "Send to Lina" voice memo).

If the workshop has no closing-ritual section, skip this step.

---

## Step 8 — Offer reflection (skippable)

> "Two questions if you've got 3 minutes — totally skippable: what surprised you in the data? what would you do differently next time?"

If they answer, append to log under `## Reflection`.

---

## Step 9 — Tell them what's next

Pull this from the workshop's `CLAUDE.md` if specified, or use the default:

> "Your work is saved. When you're ready for the next workshop, just type `/start-X-Y`."

---

## Important — do NOT close the conversation

If the learner keeps working after `/done`, new entries go under a `## Post-done exploration` section in the log. The summary stands.
