---
workshop: W1-1 Your First Ship — Pomodoro
status: checkpointed
started: 2026-05-06T00:00:00
closed: 2026-05-06T00:00:00
---

# Workshop Log

## Step 1 — Workspace orientation

Learner confirmed Cursor layout (left sidebar, right work area). Oriented to file tree and chat panel.

## Step 2 — Model check

Learner ran `/model` and switched to Sonnet. Confirmed on correct model before building.

## Step 3 — Engineer framing

Learner received the "you don't need to be an engineer" framing — describe → ask back → plan → build → review → iterate → ship.

## Step 4 — Project folder created

Learner prompted: "create a new folder called pomodoro for our project." Folder created at `lesson-modules/W1/1-1-pomodoro/pomodoro/`.

## Step 5 — Requirements gathering via AskUserQuestion

Learner sent describe prompt. Claude used AskUserQuestion for 6 questions across 2 batches.

## Decision — Timer preset

Classic 25/5 selected.

## Decision — Vibe

"Surprise me" selected. Claude chose deep terracotta and cream, Fraunces serif.

## Decision — App name

"Tomato" selected. Used in page title and heading.

## Decision — Ring

Animated SVG ring selected (yes).

## Decision — Sound

Soft chime selected (yes, browser audio API).

## Decision — Mobile

Mobile-friendly selected (yes).

## Step 6 — Plan reviewed

Claude proposed 7-bullet plan. Learner asked "what's SVG?" — explained as "the animated ring." Learner approved plan.

## Step 7 — First build

`index.html` written to `pomodoro/` folder. Single file, inlined CSS/JS, Fraunces + Inter Tight fonts, terracotta/cream palette, animated SVG ring, soft chime, session dots, responsive.

## Step 8 — Opened in browser

Learner found `index.html` in sidebar (needed one redirect — initially opened as code file). Confirmed timer running.

## Micro-praise — success point

Named: described in own words, asked clarifying questions, reviewed plan, app running in browser.

## Step 9 — First commit

Learner committed via source control panel with message `pomodoro v1`.

## Step 10 — Iteration: todo list

Learner chose to add a todo list with a focused item. Claude built it.

## Stuck moment — todo dot interaction

Learner reported clicking dot caused strikethrough instead of focus highlight. Identified UX confusion: dot click = done, body click = focus was not intuitive. Learner proposed: dot = mark done (larger), body click = set as focused. Claude implemented the swap.

## Action — Updated index.html

Dot enlarged to 18px, interactions swapped: dot click marks done, task body click sets focus. Learner confirmed "great."

## Step 11 — Second commit

Learner committed with message `added todo list`.

## Step 12 — Deployed to Vercel

Learner opened terminal, ran `cd lesson-modules/W1/1-1-pomodoro/pomodoro` then `vercel --prod --yes`. Deployed successfully. Learner confirmed deployment done.

## Insight surfaced

Learner reflection on shipping: "it's easy." Acknowledged the real skill is knowing what you want and being clear about it, not the code.

## Summary

**Status:** checkpoint-completed (core loop complete, bonus chapters not done)

- set model to Sonnet and oriented to the Cursor workspace
- described a pomodoro timer, answered 6 design questions, reviewed a plan
- shipped `index.html` — Tomato timer, terracotta/cream, animated SVG ring, soft chime, session dots
- iterated: added todo list with focus/done interactions, fixed UX based on own feedback
- deployed live to Vercel with `vercel --prod --yes` — real public URL in under 30 min

**Files produced:**
- `lesson-modules/W1/1-1-pomodoro/pomodoro/index.html`

**Where they left off:** core workshop complete. Bonus chapters A (undo/revert) and B (add another feature) available when ready — each is the same loop, ~3–10 min.

**Closed at:** 2026-05-06
