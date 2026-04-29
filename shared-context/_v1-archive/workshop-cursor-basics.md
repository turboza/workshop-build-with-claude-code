---
type: knowledge
created: 2026-04-28
scope: reusable-across-weeks
purpose: Cursor + Claude Code + git basics taught progressively across W1
---

# Cursor / Claude Code / Git Basics

The minimum tool literacy learners need across W1 to work confidently. Each basic gets a 30-second teach-the-keystroke moment, then is immediately used in the work. Distributed across all three W1 workshops.

Voice rules in [workshop-ta-core.md](workshop-ta-core.md). Workshops reference this file when introducing a new basic.

---

## Distribution across W1

| Basic | Where introduced | Why there |
|---|---|---|
| Folder structure / sidebar navigation | W1-1 (Pomodoro) | First contact with the project |
| Open files in Cursor | W1-1 | Need to look at what Claude wrote |
| `@filename` references in Claude prompt | W1-1 (intro) → W1-2 (used heavily) | Tying messages to files |
| Terminal panel inside Cursor | W1-1 | Where they type slash commands |
| Permission prompts (read vs write) | W1-1 | Foundational mental model |
| `git status` / `git add` / `git commit` (in Cursor source control panel) | W1-1 (first commit) | No CLI memorization needed |
| Reverting a change in Cursor | W1-1 | Safety net before going further |
| Folder-tree summary | W1-2 | When data files multiply |
| `/clear` to reset conversation | W1-3 | When Claude gets confused |
| Multi-file edits | W1-3 | Dashboard touches multiple files |

---

## W1-1 introductions

### Folder structure / sidebar

> "Look at the left side of Cursor — that tree is your project. Click any file to peek at it. Right now we're in `workshops/W1-1-pomodoro/`. Everything we make today shows up there."

### Permission prompts

> "When Claude wants to write or change a file, you'll see a popup. That's not friction — that's your seatbelt. Read it, then say yes or no. Most of the time you'll say yes; the prompt is so you stay in charge."

### `@filename` (intro only in W1-1, heavy use in W1-2)

> "Want to point me at a specific file in your message? Type `@` and start typing the filename — Cursor will autocomplete. That tells me 'look at this file when answering.'"

### Git in Cursor (no CLI)

The plan: learners use the Cursor source control panel (the branch icon on the left sidebar). No memorizing `git add` / `git commit -m`. Just:

1. Click the source control icon
2. See changed files listed
3. Type a commit message in the text box
4. Click the "✓ Commit" button

> "This is your save point. We'll commit at the end of every workshop. Three steps: source control icon, type a message, click commit. That's it."

For learners who want CLI later, mention briefly that the same thing can be done with `git add . && git commit -m "..."`. But CLI is **not required** in W1.

### Reverting a change in Cursor

> "If you accidentally break something — totally normal, happens to everyone — Cursor's source control panel has a discard button next to each changed file. Click it, the file goes back to the last commit. This is why we commit often: the further back you can go, the safer you are to experiment."

Demo this once in W1-1 by deliberately breaking the Pomodoro app and reverting. Builds the muscle.

---

## W1-2 introductions

### Folder-tree summary

When the data dump arrives in W1-2, the workshop folder has 6+ files plus subfolders. Claude introduces:

> "When you want to see what's in a folder fast, ask me — `summarize what's in this folder` — and I'll list the files with one-line descriptions. Try it now: type that with `@workshops/W1-2-linas-coffee/data/`."

This becomes a learner reflex by W1-3.

### Heavy `@` usage

W1-2 is where `@` references pay off — pointing Claude at specific files in the data dump. The pattern:

> "Read `@data/pos_export_oct2025-mar2026.csv` and tell me what columns are in it."

Claude reinforces this by always asking via `@` when it needs the learner to point at something.

---

## W1-3 introductions

### `/clear` — reset the conversation

> "If our conversation gets long and I start losing the thread — repeating myself, missing what we already decided — you can type `/clear` and we start fresh. Your *files* stick around; only the chat resets. Think of it like closing and reopening the chat window. Sometimes that's the cleanest fix."

Frame as a tool, not a punishment. Used proactively when Claude starts drifting.

This connects to the W3.2 pedagogy rule: *"Two failed corrections → /clear"* — but in W1 we just plant the seed.

### Multi-file edits

The dashboard touches `dashboard.html`, `dashboard.css`, and possibly a small data file. Claude shows that one prompt can change multiple files coherently:

> "I'm going to update the chart styles — that touches both `dashboard.html` and `dashboard.css`. You'll see two file changes in the source control panel after."

---

## The "Cursor + Claude Code" duality

Many learners may use Cursor's chat instead of Claude Code CLI. Both work for these workshops because:

- Workshop SCRIPT.md files are plain markdown — can be pasted into Cursor's Composer with one instruction
- Slash commands are Claude-Code-only; Cursor users invoke the same workshop via *"please run the W1-2 workshop from `weeks/W1/scripts/workshop-1-2-script.md`"*
- All other tooling (file editing, terminal, git, `@` references) is shared

The instructor mentions this duality at the start of each session for learners using Cursor.

---

## What we skip in W1

To avoid overload:
- ❌ CLI git commands (use Cursor panel)
- ❌ Branches, merges, push to GitHub (W3)
- ❌ Multiple windows / panels (W2)
- ❌ Extensions / settings tweaks (W2 if needed)
- ❌ Custom keyboard shortcuts
- ❌ MCP, hooks, subagents (W7+)

---

## When this file changes

Update when:
- A basic proves more confusing than expected (move to a different week, or rethink the introduction)
- A new shared tool basic emerges (e.g. terminal multiplexing in W4+)
- Cursor / Claude Code change their UI in a way that breaks a description here

Then update [CLAUDE.md](../CLAUDE.md).
