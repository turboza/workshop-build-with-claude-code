# Claude Code Course — Workshop Materials

This is the workshop project. Learners clone this repo and run interactive workshops by typing slash commands inside Claude Code.

---

## What's in here

```
workshop/
├── README.md                 # Learner entry point — "how to start"
├── CLAUDE.md                 # This file — repo-level project memory
├── .claude/
│   ├── SCRIPT_INSTRUCTIONS.md   # How Claude runs a workshop script
│   ├── settings.json            # Minimal permissions
│   └── commands/                # Slash commands: start-1-1, start-1-2, start-1-3, done, wrap-up, help-im-stuck
├── shared-context/           # Reusable rules across all workshops
│   └── workshop-rules.md            # Consolidated: voice + journaling + FX + slash commands + Cursor basics
└── lesson-modules/
    └── W1/
        ├── CLAUDE.md                # W1 session agenda (used by /wrap-up)
        ├── 1-1-pomodoro/
        │   ├── CLAUDE.md            # Workshop script (beats, voice, /done ritual)
        │   └── workshop-log.md      # Auto-generated at /done
        ├── 1-2-linas-coffee/
        │   ├── CLAUDE.md            # Workshop script
        │   ├── data-dump/           # 7 messy source files
        │   ├── data/                # Output: consolidated.csv
        │   └── workshop-log.md      # Auto-generated at /done
        └── 1-3-linas-dashboard/
            ├── CLAUDE.md            # Workshop script
            ├── data/                # consolidated.csv (default, ships with repo)
            └── workshop-log.md      # Auto-generated at /done
```

Each workshop folder follows the same shape. Instructor runs `/wrap-up` at end of class day to collect the week's logs into a reflection file.

---

## Delivery context — Cursor (VSCode extension), not Claude Code CLI

All learners use **Cursor** (the VSCode extension). There is no `claude` CLI command. This means:

- Learners open the workshop folder in Cursor and interact via Composer/chat
- Slash commands work via Cursor's Composer command palette
- "Open the terminal" = Cursor's integrated terminal (`Ctrl + \``)
- Never write "run `claude`" in any script or instruction — always say "open Cursor" / "open Composer"

---

## How a workshop runs

1. Learner opens this folder in Cursor
2. Opens Composer and types `/start-1-2` (or whichever workshop)
3. Claude announces "Starting W1-2 — one sec" then reads `shared-context/workshop-rules.md` + the workshop's `CLAUDE.md` (2 file reads, not 5)
4. Claude begins in character — Beat 1 starts
5. Workshop produces real artifacts in the workshop folder, all committed to git
6. End-of-workshop: learner types `/done` to checkpoint

---

## Never read CSVs or Excel files whole

**Hard rule.** A single CSV/XLSX can be 100K–millions of tokens and will blow the context window in one Read call. Always preview first:

- **Shape:** `wc -l <file>` for row count
- **Header + first rows:** `head -5 <file>`
- **Last rows:** `tail -5 <file>`
- **Column names only:** `head -1 <file>`
- **Sample a column:** `cut -d, -f3 <file> | head -20`
- **XLSX:** convert to CSV first (`in2csv`, `xlsx2csv`, or a one-line Python script) then preview as above — never Read the binary

Only Read the whole file if it's known to be small (<200 lines) AND you've confirmed shape with `wc -l` first. Applies to W1-2 (`data-dump/`, `data/consolidated.csv`), W1-3 (`data/consolidated.csv`), and any future workshop with data files.

---

## Voice — the most important rule

Claude is a **co-learner, not a teacher**. The learner types prompts; Claude switches between coach mode (suggest what to try) and work mode (respond to the actual prompt). Mirror the learner's tone before redirecting. Full rules in `shared-context/workshop-rules.md`.

Banned standalone praise: "Look at you!", "Prepare to be amazed", "Trust me", "Amazing!" / "Great job!" alone. Brief lead-ins ("Great", "Nice") are fine **when something specific follows**. Never imply the learner is at fault when stuck.

---

## Cursor compatibility

Slash commands are Claude Code only. For learners using Cursor:
- Open the workshop's `CLAUDE.md` in Composer
- Say: *"please run this workshop with me — follow the markers, and read shared-context/workshop-rules.md first"*
- All script content is portable; only the slash auto-load is lost

---

## Building / editing workshops

This workshop project is updated from the design repo at `working-docs/` (the symlinked Obsidian vault).

Workflow:
1. Develop scripts and data in the design repo's `weeks/W{n}/` and `knowledge/workshop-*` files
2. Copy the updated files into this repo when ready for learner use
3. Commit + tag in this repo so each cohort has a stable version

Keep `shared-context/workshop-rules.md` in this repo in sync with the design repo's knowledge files (especially `knowledge/workshop-story-builder-v2.md` for the builder workflow).

---

## What's currently built

- ✅ Repo scaffold (`.claude/`, `shared-context/`, `lesson-modules/W1/`)
- ✅ Consolidated `shared-context/workshop-rules.md` (single file, replaces 5)
- ✅ Slash commands: `start-1-1`, `start-1-2`, `start-1-3`, `done`, `wrap-up`, `help-im-stuck`
- ✅ W1-1 Pomodoro — full script, Vercel deploy beat, bonus chapters
- ✅ W1-2 Lina's Coffee — full v2 script, data generated, ready to dry-run
- ✅ W1-3 Lina's Dashboard — full script, Plan Mode beat, Chart.js dashboard, branch-2 projection
- ✅ `lesson-modules/W1/CLAUDE.md` — W1 session agenda for `/wrap-up`
- ⬜ W2–W8 `lesson-modules/W{n}/CLAUDE.md` session agendas (needed for `/wrap-up` mirror-back)
- ⬜ Form URLs for W2–W8 in `wrap-up.md`

See `workshop-1-2-and-1-3-spec.md` in the design repo for the full plan.
