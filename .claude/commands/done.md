---
description: "Wrap up the active workshop — write summary, acknowledge progress"
---

**Important — tool discipline:**

- DO NOT use `TodoWrite` — `workshop-log.md` is the tracking system
- DO NOT use `Agent`, `WebFetch`, `WebSearch`, `EnterPlanMode`
- The only tools you need: `Read`, `Bash`, `Write`, `Edit`

**First, say to the learner:**

> "Wrapping up. One sec — let me look back through what we did."

**Then:**

1. Find the active workshop log:

   ```bash
   find lesson-modules -name "workshop-log.md" -type f
   ```

   For each match, check the frontmatter `status:` field. The active log is the one with `status: in-progress` (or most recent if multiple).

   If no `in-progress` log found, ask: *"Hmm, I don't see an active workshop. Did you start one? Try `/start-1-2` or whichever workshop you want."*

2. Read `shared-context/workshop-rules.md` (voice rules + §10 journaling/done behavior).

3. Read the active `workshop-log.md`.

4. Classify the state:
   - **Completed:** all major Step entries present + success-point marker + bonus chapters done
   - **Checkpoint-completed:** success point hit, mid-bonus
   - **Checkpoint-incomplete:** success point not hit, but real progress made
   - **Aborted:** very early stop

5. **Tell the learner you're updating the log:**

   > "Logging the wrap-up summary."

   Then append a `## Summary` block with:
   - Status (one of the four above)
   - Real progress in 3-5 specific bullets — name the actual decisions, files, insights. Never generic.
   - Where they left off, in concrete terms (never "we ran out of time" — say "the X file is the same shape, ~5 min when you come back")
   - Files produced (with paths)
   - Closed-at timestamp

6. Update the log frontmatter `status:` field to `checkpointed` (or `completed` if all bonus done).

7. Speak to the learner using voice rules. Lead with brief affirmation OK ("Great" / "Nice"), then **specific named progress**. Acknowledge effort warmly even if incomplete. 3-4 sentences.

   Examples (adapt — don't paste verbatim):
   - *"Great — quick wrap on what we got done. Schema is locked, four of the six files are merged, and we already caught the Highland Beans typos. The last two are the same shape — 5-minute lift when you come back."*
   - *"Nice. You designed the schema, picked categories, ran the merge, surfaced the fixed-floor insight, and wrote Lina something she can send. Honestly the hard part is the schema — the rest is the same shape every time."*

8. **Send to Lina (always-on, ~30 seconds):**

   Then say:

   > "One more thing — want to 'send' the summary to Lina and see what she'd say back? (Not real — just for the win.)"

   If learner says yes / sure / why not:

   - Look at the workshop output (`linas-bank-summary.md`, `data/consolidated.csv`, headline insights from log)
   - Generate Lina's reaction as a **highlighted voice memo block** the learner can read like they're listening to it. Format like:

     ```
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     🍵 Lina — voice memo (0:42)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     "Oh my god — okay so I just opened it. Wait. ฿810K
     fixed floor? That's… honestly that's the number I've
     been trying to figure out for a year. And the bank
     summary — I can literally send this. You — thank you.
     Seriously. Friday is going to be so much less scary.

     Okay I have to get back to the bar but — coffee on me
     forever. I'll see you in W1-3 to actually build the
     dashboard, yeah?"

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ```

   Use Lina's voice from the workshop CLAUDE.md:
   - Warm, fast, mixes Thai/English casual ("okay so", "honestly", "wait", "hmm")
   - Self-deprecating-but-touched
   - Specific to what was actually built (reference the real numbers / files)
   - 3-5 sentences, ~40 sec read
   - 🍵 emoji as her signature

   **For incomplete state:** still send a Lina reaction, but warmer/less wow — *"hey, I saw what you've got so far — that schema thing is more than I had two days ago. Don't worry about Friday, send me what's there when you come back to it."*

9. **Offer reflection** (skippable):

   > "Two questions if you've got 3 minutes — totally skippable: what surprised you in the data? what would you do differently next time?"

   If they answer, append to log under `## Reflection`.

10. Tell them what's next:

    > "Next up is W1-3 — building the dashboard. Type `/start-1-3` whenever you're ready. Or take the break — your work is saved."

11. **Do NOT close the conversation.** If the learner keeps working, new entries go under a `## Post-done exploration` section in the log. The summary stands.
