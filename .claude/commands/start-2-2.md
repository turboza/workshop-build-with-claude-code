---
description: "Workshop 2-2: Newsletter Subscribe (Resend)"
---

**Important — tool discipline:**

- DO NOT use `TodoWrite`
- DO NOT look for, create, or reference `workshop-log.md` — W2 workshops have no log file
- DO NOT use `Agent`, `WebSearch`
- `WebFetch` is allowed only for resend.com documentation if a learner question requires it
- `EnterPlanMode` / `ExitPlanMode` are allowed (use sparingly — only if learner asks or seems uncertain about scope)
- The tools you need: `Read`, `Bash`, `Write`, `Edit`, `EnterPlanMode`, `ExitPlanMode`

**First, say to the learner:**

> "Starting W2-2 — Newsletter Subscribe. One sec while I get oriented."

**Then silently:**

1. Read `shared-context/workshop-rules.md` — voice, journaling, slash command shapes.
2. Read `shared-context/resend-contacts-api.md` — Resend SDK gotchas and current API shape.
3. Read `lesson-modules/W2/2-2-newsletter-subscribe/CLAUDE.md` — the workshop guide.
4. Find the learner's project: run `ls ../course-workspace/` to list what's there. If a `website-*` folder exists, that's their W2-1 project — capture the absolute path with `cd ../course-workspace/<name> && pwd`. If nothing exists or the folder is empty, note that W2-1 may not be done.
5. Run the **Handoff** section in the workshop guide — generate the continuation prompt using the project path found above (or ask the learner to point you at their project if it wasn't found). Do not start the objectives in THIS window. The workshop runs in the project window from there.
