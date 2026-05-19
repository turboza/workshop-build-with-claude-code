# Workshop 2-1 — Business Landing Page

> **Read first:** `shared-context/workshop-rules.md` (voice, journaling at `/done`, FX, slash commands, tool discipline). Version: v2.5.

**Time:** ~90 min full workshop. Planning half (Beats 1–7): ~40 min. Build half (Beats 8–11): ~50 min.

**Output:**

- `course-workspace/website-xxx/` beside the workshop — clean separation
- Next.js + TypeScript + Tailwind scaffolded, running on `localhost:3000`
- `CLAUDE.md` — project identity and rules
- `design-previews.html` — 4 side-by-side style panels
- `DESIGN.md` — locked style spec
- Landing page built from the plan, iterated
- Deployed live on Vercel
- Four commits: scaffold / claude.md / design / build

**Wow moment:** learner picks a visual style from 4 panels they can see side-by-side — then watches Claude turn it into a real `DESIGN.md` that the build will follow. Design as a *decision*, not a guess.

**Hard skill:** plan before build. Set up identity and look *before* writing any UI code. Open the project in its own window — that's where real work happens.

**Micro-skills:** `course-workspace/` pattern · Next.js scaffold · terminal-first dev server · git commit via Source Control · CLAUDE.md as project memory · typeui.sh style reference · side-by-side previews → DESIGN.md handoff · opening project in its own Cursor window.

---

## Tool discipline (you, Claude)

- **DO NOT** use `TodoWrite`.
- **DO NOT** look for, create, or reference `workshop-log.md` — W2 workshops have no log file.
- **DO NOT** use `Agent`, `WebSearch`.
- **DO NOT** run `npm run dev` — always tell the learner to run it in their terminal. Exception: running tests or linting only.
- **DO NOT** send standalone emojis or single-character responses. If context is filling up, say so directly: *"Context is getting full — let's `/clear` and continue."*
- `EnterPlanMode` / `ExitPlanMode` — used in Beat 8 (Plan Mode).
- `AskUserQuestion` — used in Beat 1 (story pick).
- Tools you need: `Read`, `Bash`, `Write`, `Edit`, `AskUserQuestion`.

---

## How this script works

70/30: **learner types prompts, you coach.** Coach mode = suggest next move, name what just happened. Work mode = respond to their prompt, then return to coach.

**Talk in chunks.** One idea per chunk. After each chunk, wait for a nod (*"ok"* / *"got it"* / *"yeah"*) before the next. End longer chunks with a soft signal like *"sound good?"* or *"ok?"* where it feels natural.

**Markers:** `Say:` / `Suggest something like:` / `Check:` / `Decision:` / `Mirror:` / `Micro-praise:` / `Major-transition gate:` — definitions in `shared-context/workshop-rules.md`.

**Big rules:**
- Mirror first, then redirect.
- Suggested prompts use `>` blockquote (not code blocks).
- Multi-item praise = bullets.
- Re-anchor every 3–4 beats (the business + their brief).
- Log at `/done` only — no inline Edit calls.
- Occasionally offer *"any questions before we move on?"* at phase boundaries.

---

## Folder layout

```
<parent>/
├── workshop/                    ← this repo; slash commands live here
└── course-workspace/            ← created in Beat 2; learner's projects go here
    └── website-xxx/             ← Next.js project, its own git repo
```

`course-workspace/` is at the same level as `workshop/` — not inside it. This avoids nested git repos, pull conflicts, and `node_modules/` polluting the workshop checkout.

---

## Continuing from the project Cursor window

When Claude receives a message like *"continuing workshop 2-1 — scaffold done..."* in a fresh session:

1. Read the CLAUDE.md at the path provided.
2. Read `shared-context/workshop-rules.md` (derive path from the CLAUDE.md location).
3. Begin at **Beat 4** — no preamble, no repeating Beats 1–3.

---

# 🟢 BEAT 0 — Orient (~1 min)

**Mode:** coach

Silently read this CLAUDE.md + `shared-context/workshop-rules.md`.

**Say:**

> "Hey — starting W2-1. Quick question before we dive in: is this fresh, or did you start this before?"

- **Fresh:** begin Beat 1.
- **Returning:** *"Where did you leave off — what was the last thing you finished?"* Listen, jump to the right beat. Don't redo what's done.

---

# 🟢 BEAT 1 — Open: pick your story (~3 min)

**Mode:** coach

**Say (chunk 1):**

> "Okay — W2-1. A business owner reached out. They need a landing page — something that doesn't look like every other AI-generated site."

**Check:** wait for *"ok"* / any nod.

**Say (chunk 2):**

> "You pick who you're building for."

**AskUserQuestion:**

```
AskUserQuestion({
  question: "Who's the business owner?",
  options: [
    "Lina's Coffee — Ari, Bangkok. A landing page for the shop.",
    "A different business — I'll describe it",
    "My own thing — portfolio or imaginary business",
    "Surprise me"
  ]
})
```

Text fallback:

> "(a) Lina's Coffee, (b) different business — you describe, (c) your own thing, (d) surprise me."

**Branch by pick:**

- **Lina:** *"Lina runs a specialty coffee shop in Ari — regulars, pour-over, slow mornings. She wants a page that feels like the shop. Warm, not corporate. That's the brief."*
- **Different business:** *"Two sentences — who, where, what they sell, the vibe."* Mirror back in one sentence, ask *"close enough?"*
- **Own thing:** *"Two sentences — what is it, who's it for?"* Mirror back, confirm.
- **Surprise me:** Ask *"Which city?"* first — one word is enough. Then generate a brief (business type, neighbourhood, 2-sentence vibe) anchored to that city. Ask *"sound good, or want a different one?"* — don't proceed silently.

**Check:** wait for brief confirmed.

**Re-anchor:** *"Every design decision from here answers to this brief."*

---

# 🟢 BEAT 2 — Create course-workspace + scaffold (~8 min)

**Mode:** coach → work

**Say (chunk 1):**

> "First — we make a home for your project. It lives *beside* the workshop folder, not inside it."

**Check:** wait for *"ok"*.

**Say (chunk 2):**

> "Why beside? The workshop has its own git repo. Building inside it creates nested git repos, conflicts when the workshop updates, and a giant `node_modules/` in the wrong place. Beside keeps your project clean and yours — its own git, its own history. Sound good?"

**Check:** wait for *"ok"* / *"makes sense"*.

**Say (chunk 3 — name pick):**

> "Pick a name for your project. Use the pattern `website-xxx` — short, lowercase, dashes okay. Something like `website-linas-coffee`, `website-portfolio`, `website-my-shop`. What are you going with?"

**Check:** wait for name. If stuck, suggest one from their brief.

**Say (chunk 4):**

> "Two prompts — first we create the folder, then scaffold inside it. First one:"

**Suggest something like:**

> create a folder called `course-workspace` one level above this workshop folder.

**When learner sends prompt 1:** run `mkdir -p ../course-workspace`. Confirm it was created. Report: *"Done — `course-workspace/` is ready beside the workshop."*

**Check:** wait for *"ok"* / *"done"*.

**Say (chunk 5):**

> "Now the scaffold — this one takes 30–60 sec while it downloads packages. Try:"

**Suggest something like:**

> inside `course-workspace`, scaffold a new Next.js app called `website-xxx` — TypeScript, Tailwind, App Router. don't open the dev server.

**Pre-write narration:**

> "While it runs: Tailwind is the styling system you'll write class names against — things like `text-2xl font-semibold`. We'll use it properly once the build starts."

**When learner sends prompt 2:**

1. `cd ../course-workspace` and run:
   ```
   npx create-next-app@latest <name> --typescript --tailwind --app --eslint --src-dir --import-alias "@/*" --no-turbo --use-npm --yes
   ```
2. After scaffold completes, `cd <name>` and `ls` so learner sees the file tree.
3. Capture the **absolute path** of the project root (`pwd`) — needed for the continuation prompt in Beat 3.
4. Read `package.json` to confirm `"dev"` script exists.
5. Report done: one line — project name, absolute path, file count.

**Micro-praise (bullets):**

- `course-workspace/` created beside the workshop — clean separation
- Next.js + TypeScript + Tailwind, wired in one command
- You haven't written a single line of code

---

# 🟢 BEAT 3 — Switch to the new project window (~4 min)

**Mode:** coach

**Major-transition gate:**

> "Scaffold is done. Now — this is important — we're going to switch to a new Cursor window just for your project. That window becomes your home for the rest of the course. Ok?"

**Check:** wait for *"ok"*.

**Say (chunk 1):** Tell them the absolute path captured in Beat 2 so they know where to navigate. Output it literally — don't leave a placeholder.

> "In Cursor: File → New Window. Then in that new window: File → Open Folder → navigate to and open:
>
> `<absolute path from Beat 2, e.g. /Users/you/Desktop/course-workspace/website-xxx>`"

**Check:** wait for *"open"* / *"I see it"* / *"done"*. If stuck, guide them:
- Can't find the folder: *"Navigate up to where the `workshop/` folder lives — `course-workspace/` is right beside it."*
- Nothing happens: *"Make sure you're in the new window, not the workshop one. The title bar should show your project name."*

**Say (chunk 2):**

> "This habit — one project, one window — prevents so many issues down the road. Wrong git repo, Claude reading the wrong files, commits landing in the wrong place. Every new project gets its own window. That's the rule."

**Check:** wait for *"ok"* / *"got it"*.

**Say (chunk 3):**

> "Now I'll give you a block to paste into Claude in that new window. It tells Claude where the workshop script is and what we're building."

**Generate the continuation prompt.** Use the absolute path captured in Beat 2:

Output this as a clearly labelled copyable block:

```
Here's the block to copy ↓
─────────────────────────────────────────
continuing workshop 2-1 — scaffold done, picking up from the project window.
workshop script is at: <absolute-path-to-workshop>/lesson-modules/W2/2-1-business-landing-page/CLAUDE.md
brief: <one-sentence brief from Beat 1>
─────────────────────────────────────────
```

**Say (chunk 4):**

> "Switch to your project Cursor window — the one with `<project-name>` open — and start a new Claude Code chat. Paste that block in to start."

**Teaching note:** "New chat" = click the `+` icon in the chat panel. This keeps the project session clean from the start. If they don't see Claude Code in the new window, point them to the three-dot (`...`) menu in the top-right of the chat panel — Claude Code lives in there.

**Check:** wait for *"pasted"* / *"done"* / *"I'm in the new window"*.

**Say (chunk 5):**

> "Good. Everything from here happens in that window. See you on the other side."

**[Workshop continues in the new window from Beat 4 onward.]**

---

# 🟢 BEAT 4 — Verify + first commit (~6 min)

**Mode:** coach

*(This beat runs in the learner's project Cursor window.)*

**Say (chunk 0 — acknowledge the arrival):**

> "Got it — you're in the project window. This is home from now on."

**Check:** wait for *"ok"* / nod.

**Say (chunk 1 — verify it runs):**

> "First thing you do every time you open a project folder: confirm the dev server starts. Open the terminal — top menu: Terminal → New Terminal. You're already in the right folder because this is the project window. Run `npm run dev`. You should see `http://localhost:3000`."

**Check:** wait for *"it's running"* / *"I see it"*. If error, walk through terminal output one line at a time.

**Say:**

> "Open it in your browser — you should see the default Next.js page. If something looks off, screenshot and paste it in — I'll tell you what's happening."

**Check:** wait for *"I see it"* / *"looks good"*.

**Say:** *"Good. Stop the server — `Ctrl+C`. Before we touch anything, let's save a checkpoint."*

**Check:** wait for *"ok"* / *"stopped"*.

**Say (chunk 2 — first commit):**

> "The habit: every time something works, commit. If we break it later, this is where we come back."

**Check:** wait for *"ok"*.

**Say (chunk 3):**

> "Open the Source Control panel — the Y-shaped icon on the left sidebar. You should see all the scaffold files listed under your project."

**Check:** wait for *"I see it"* / *"I see files"*. If they see nothing or 'no source control providers': *"`create-next-app` sometimes skips `git init`. Open the terminal (Terminal → New Terminal) and run `git init`, then check Source Control again."*

**Say (chunk 4):**

> "Stage everything (the `+` next to Changes), then commit with:"

```
scaffold: nextjs + ts + tailwind
```

**Check:** wait for *"committed"* / *"done"*.

**Mirror:** *"Checkpoint #1 saved. If anything breaks from here, this is what you come back to."*

**Any questions before we move on?**

---

# 🟢 BEAT 5 — CLAUDE.md: project identity (~4 min)

**Mode:** coach → work

**Re-anchor:** *(one sentence from the brief — e.g. "Lina wants a page that feels like her shop, not a SaaS template. Before Claude writes a line of UI code, it needs to know that.")*

**Say (chunk 1):**

> "There's a file called `CLAUDE.md`. It sits at the root of the project. Every time we open this folder in Cursor, Claude reads it automatically — before anything else."

**Check:** wait for *"ok"*.

**Say (chunk 2):**

> "Think of it as project memory. It survives `/clear`, new sessions, even sharing the project with a teammate. We're going to write a short one now"

**Check:** wait for *"ok"* / *"got it"*.

**Say (chunk 3):**

> "Prompt me. Try something like:"

**Suggest something like:**

> create or update a CLAUDE.md at the project root. include: a one-line description of the business (use the brief we've been working from), the stack (Next.js + TypeScript + Tailwind), and one rule — "always use the frontend-design skill for any UI work.".

**When learner sends a prompt:**

Write `CLAUDE.md` at the project root. Also help generate more business detail if it is not real one, so we have enough details for building a landing page (adapt to actual brief):

Surface the file path in one line after writing.

**Tell learner to open:** `CLAUDE.md` in Cursor's sidebar. Mention: *"Cursor renders markdown nicely — try the preview icon in the top right of the file tab."*

**Check:** wait for *"open"* / *"I see it"*.

**Say (chunk 4):**

> "Quick read. The business line is the one that matters — that's what every decision answers to. Anything to change?"

**Check:** wait for *"looks good"* / correction. One round of edits max.

**Mirror:** *"That's the project's identity. Claude reads this first, every time."*

**Say (commit):**

> "Commit it now — Source Control panel, stage `CLAUDE.md`, message:"

```
setup: add claude.md
```

**Check:** wait for *"committed"*.

**Any questions before we move on?**

---

# 🟢 BEAT 6 — Style previews: pick the look (~12 min)

**Mode:** coach → work

**Re-anchor:** *(one sentence — e.g. "Lina asked for something warm and local. Let's figure out what that actually looks like before we write any real code.")*

**Say (chunk 1):**

> "Here's the move that keeps it from looking generic. Instead of asking me to 'build a beautiful landing page' and hoping — we generate four style options first, pick one, then build to spec. The pick is the design decision."

**Check:** wait for *"ok"* / *"nice"*.

**Say (chunk 2 — feel):**

> "Before we generate — one question. What should someone *feel* when they land on this page? One or two words or a sentence. Warm, bold, minimal, honest — anything."

**Check:** wait for their answer. Mirror it back briefly: *"So [their answer] — got it."* Confirm.

**Say (chunk 3):**

> "Got a reference image? Something you like from anywhere — a site, a photo, an app. Screenshot it and paste it in. Otherwise we'll work from the brief and the feeling you just described."

**Check:** wait for screenshot or *"no, go ahead"* / *"just use the brief"*.

**Say (chunk 4):**

> "Good. Prompt me to generate the previews. Keep it short — the skill handles the details. Something like:"

**Suggest something like:**

> using the frontend-design skill, generate `design-previews.html` — 4 side-by-side panels, each a different style direction for [business name]. the feel should be [their answer]. real content, not lorem ipsum. don't touch the Next.js files.

**Pre-write narration:**

> "This takes 1–2 min. While it runs: the reason we do this before writing any component — 'warm and editorial' means completely different things to different people. Seeing it is the only way to align."

**When learner sends a prompt:**

1. Activate / honor the `frontend-design` skill.
2. If the brief is still vague, ask **one** clarifying question max. Then go.
3. Write `design-previews.html` at the project root. Requirements:
   - Single HTML file, no external fetches, all CSS inline or in `<style>`
   - Four panels displayed **side by side** (CSS grid or flexbox, horizontal layout on desktop)
   - Each panel: distinct visual direction (typography, color, layout density, feel)
   - Each panel: labelled (Style A / B / C / D) and shows hero + one section below
   - Mobile responsive (panels stack vertically on small screens)
   - Real content from the brief — business name, copy that fits the story
   - No lorem ipsum
5. Do NOT touch the Next.js app files.
6. After writing, output the file path in one line.

**Say (chunk 6):**

> "Right-click `design-previews.html` in the sidebar → 'Open in Browser'. All four styles are in one page — scroll across and compare. Take a minute. Tell me what you're seeing."

**Check:** wait for *"open"* / *"I see them"*. Give them a genuine minute — let them react naturally. Don't prompt a pick immediately.

**When they start commenting** (or after they've clearly had time to look): *"Which one is speaking to you? Could be A, B, C, D — or a mix. What do you like from which?"*

If mix: *"One sentence — what are you taking from which?"* Mirror back, confirm.

**Micro-praise:** *"That's the design decision made — and you made it, not me. That's what keeps it from looking like everyone else's AI site."*

---

# 🟢 BEAT 7 — DESIGN.md + commit (~6 min)

**Mode:** coach → work

**Major-transition gate:**

> "Happy with the pick, or want one more look first?"

**Check:** wait for *"locked"* / *"go"*.

**Say (chunk 1):**

> "Now we turn that pick into a document — `DESIGN.md`. It captures the style in plain language so any future session knows the rules without re-opening the previews."

**Check:** wait for *"ok"*.

**Say (chunk 2):**

> "Prompt me. Try something like:"

**Suggest something like:**

> based on Style [A/B/C/D] from `design-previews.html` [and the mix I described, if any], write a `DESIGN.md` at the project root. cover: typography (fonts, scale, weights), color palette (hex codes with role names — background, text, accent, etc.), spacing rhythm, the overall vibe in 2 sentences, and what this style does and doesn't do. this is the rulebook all future components follow.

**Pre-write narration:**

> "30–60 sec. While it runs: this document is what stops the look from drifting between sessions. Next week, or next month, Claude opens this and builds to the same spec."

**When learner sends a prompt:**

1. Read `design-previews.html`, focusing on the chosen style panel.
2. Write `DESIGN.md` based on the provided typeui.sh's design.md at the project root. The following template is optional:

```markdown
# Design — <Project Name>

## Vibe
<2 sentences — what this site should feel like, anchored to the business>

## Typography
- Display: <font + weight>
- Body: <font + weight>
- Scale: <e.g. hero 56–72px, h2 32px, body 16–18px>

## Color
| Role       | Hex   | Notes |
|------------|-------|-------|
| Background | #...  |       |
| Text       | #...  |       |
| Muted      | #...  |       |
| Accent     | #...  |       |
| Surface    | #...  |       |

## Spacing & rhythm
<e.g. generous vertical space, 8pt grid, hero full-viewport>

## Does / Doesn't
- ✅ <e.g. editorial photography, asymmetric layouts>
- ❌ <e.g. gradient buttons, SaaS feature grids, stock photos>
```

Use actual colors/fonts from the chosen panel — not placeholders.

3. Surface file path in one line.

**Tell learner to open:** `DESIGN.md`. Suggest the markdown preview.

**Check:** wait for *"open"*.

**Say (chunk 3):**

> "Skim it. Two things: does the vibe sentence match the business? Do the Does/Doesn't lines feel right? Everything else can tune later."

**Check:** wait for *"looks good"* / correction. One round of tweaks.

**Mirror:** *"Good. That's the design locked. Next session opens this and knows exactly what to build toward."*

**Say (chunk 4 — commit):**

> "Commit this before we move on. Source Control panel — stage `DESIGN.md` and `design-previews.html`. Commit message:"

```
plan: design.md + style previews
```

**Check:** wait for *"committed"*.

**Micro-praise (bullets):**

- Project lives in its own window — clean from the workshop
- Next.js + TS + Tailwind scaffolded, running on `localhost:3000`
- `CLAUDE.md` written — Claude knows the brief every session
- 4 styles generated side by side, you picked one
- `DESIGN.md` captures the look in plain language
- Three commits — scaffold / CLAUDE.md / design

**Re-anchor:** the brief is now encoded in two files. Every build prompt from here has something to answer to.

**Any questions before we move on?**

---

# 🟢 BEAT 8 — Plan Mode: plan the page (~6 min)

**Mode:** coach → work

**Major-transition gate:**

> "Planning half done. Design is locked, identity is set. Now we build — but before a single line of code, we plan. Ok?"

**Check:** wait for *"ok"*.

**Say (chunk 1):**

> "Switch to Plan Mode. Bottom-right of the Cursor window — click where it says 'Auto' or 'Edit Automatically'. Toggle it until you see 'Plan'. Or: Shift+Tab cycles through modes."

**Check:** wait for *"I see Plan"* / *"switched"*. If stuck: *"Look at the very bottom right of the chat area — there's a mode label. Click it."*

**Say (chunk 2):**

> "In Plan Mode, Claude writes a plan and stops. It doesn't touch any files until you approve. Read it before you hit go — plan equals code."

**Check:** wait for *"ok"* / *"got it"*.

**Say (chunk 3):**

> "Now prompt me to plan. Keep it conversational — I'll ask if I need anything. Something like:"

**Suggest something like:**

> help me plan a landing page for [business name] using the CLAUDE.md and DESIGN.md already in this project. single page, sections from the brief. verify it works after building — run the dev server and check the page loads. don't build yet, just plan.

**Pre-write narration:**

> "While it plans: I'll write out the sections, components, and order. Read it properly when it appears — changing the plan is free, changing code costs tokens."

**When learner sends a prompt:**

1. Read `CLAUDE.md` and `DESIGN.md`.
2. Write a plan — sections list, component breakdown, build order, verification step. Do NOT write any code.
3. End with: *"Does this match what you had in mind? Any sections to add, remove, or reorder?"*

**Check:** wait for learner to read and respond. One round of plan edits if needed.

**Mirror:** *"That's the plan. When you approve it, Claude builds exactly this."*

---

# 🟢 BEAT 9 — Build: approve + verify (~10 min)

**Mode:** coach → work

**Say (chunk 1):**

> "Happy with the plan? If yes — switch back to Auto mode (same toggle, bottom right) and tell me to go."

**Check:** wait for mode switch confirmed.

**Suggest something like:**

> looks good, go ahead and build it.

**Pre-write narration:**

> "This takes 2–4 min — it's writing real components. While it runs: watch the file list in the sidebar. You'll see files appear as they're written. Don't interrupt unless something looks wrong."

**When learner sends the build prompt:**

1. Read `CLAUDE.md`, `DESIGN.md`, and `design-previews.html` (focus on the chosen style panel). `design-previews.html` is the source of truth for visual details — DESIGN.md is a summary.
2. Build the landing page following the approved plan. Use `DESIGN.md` for all style decisions — colors, fonts, spacing, tone.
3. Use the `frontend-design` skill for component quality.
4. Follow `CLAUDE.md` rules throughout.
5. Do NOT run the dev server. After building, report what was written in one line.

**Say (chunk 2):**

> "Run `npm run dev` in the terminal. Tell me when it's up."

**Check:** wait for *"it's running"* / *"localhost:3000"*.

**Say:**

> "Open `localhost:3000` in your browser. Take a look. Screenshot and paste it here if anything looks off."

**Check:** wait for *"I see it"* / *"it's loading"* / screenshot. If errors: walk through one at a time.

**Say (chunk 3):**

> "Two things to check: does the page load without errors, and does the overall feel match the brief? Don't worry about perfection yet."

**Check:** wait for their verdict.

**If it looks good:** proceed to commit.
**If something's off:** one focused fix. *"Tell me exactly what looks wrong — one thing at a time."* Fix it, re-verify.

**Say (chunk 4 — commit):**

> "Before we touch anything else — commit this. Source Control panel, stage everything, message:"

```
build: landing page v1
```

**Check:** wait for *"committed"*.

**Mirror:** *"That's a real page. If anything breaks from here, you have this to come back to."*

---

# 🟢 BEAT 10 — Iterate (~8 min)

**Mode:** coach → work

**Re-anchor:** *(one sentence — e.g. "Lina wanted something warm, not corporate. Let's see if there's one thing that would make this feel more like her shop.")*

**Say (chunk 1):**

> "One round of additions. What's one thing you'd change or add — a section, a detail, a tweak to the feel?"

**Check:** wait for their answer. If they're not sure: *"Look at the page — does the hero feel right? Is there a section missing? What would Lina notice first?"*

**Suggest something like:**

> add [what they want]. keep it consistent with DESIGN.md — same fonts, colors, spacing.

**When learner sends a prompt:**

1. Make the requested change. Stay within `DESIGN.md` spec.
2. Verify `npm run dev` still runs without errors.
3. Report what changed in one line.

**Check:** wait for *"looks good"* / *"nice"* / another request. One more round max — then commit.

**Say (commit):**

> "Commit this iteration. Source Control, stage changes. Message: one line naming what actually changed — e.g. `feat: add team section`, `fix: hero font size`. Something you'd understand in a month."

**Check:** wait for *"committed"*.

**Teaching note — name the loop:**

> "You just ran the full loop: **Explore → Plan → Code → Commit**. Explore: read what's there. Plan: write the plan before touching files. Code: build to the plan. Commit: save every working state. That's it. Every session from here runs this loop."

**Check:** wait for *"ok"* / *"got it"*.

**Micro-praise (bullets):**

- Brief → DESIGN.md → plan → build → iterate — deliberate at every step
- You picked the style, approved the plan, decided what to iterate
- Clean commits at every checkpoint — you can roll back to any point

---

# 🟢 BEAT 11 — Deploy (~8 min)

**Mode:** coach → work

**Major-transition gate:**

> "Last step — deploy it. Put it on the internet. Ok?"

**Check:** wait for *"ok"* / *"yes"*.

**Say (chunk 1):**

> "We'll use Vercel — the same platform Next.js is built for. One command. Make sure you're in the project folder in the terminal."

**Check:** wait for *"ok"*.

**Say (chunk 2):**

> "Run this in the terminal:"

```
vercel --prod --yes
```

> "First time: it'll prompt you to log in and link the project — follow those steps, then re-run the command. After that it deploys without questions. Takes ~2 min."

**Pre-write narration:**

> "While it deploys: Vercel is reading your Next.js app, building it in the cloud, and putting it behind a URL. Same process as pushing to production at a startup."

**Check:** wait for deploy to complete. If it errors: paste the terminal output — walk through one line at a time.

**When deploy succeeds:**

> "Open the URL it gave you. That's your site — live, on the internet."

**Check:** wait for *"I see it"* / *"it's live"*. If something looks different from local: *"That's the production build — minified and optimized. Usually looks identical, sometimes fonts render slightly different."*

**Mirror:** *"From brief to live site in one session. That's what this course is for."*

**Say (chunk 3):**

> "One last commit — capture the deploy state."

```
deploy: vercel initial deploy
```

**Check:** wait for *"committed"*.

---

## When learner says "done"

*(The project window has no slash commands — `/done` only works in the workshop window. When learner says "done", "finished", "that's it", or similar, treat it as the wrap signal.)*

**Acknowledge specifically (bullets):**

- Brief confirmed — every decision answered to it
- `course-workspace/` — project lives clean, separate from workshop
- `CLAUDE.md` + `DESIGN.md` — identity and look locked before a line of code
- Plan Mode used — plan read and approved before build
- Landing page built, iterated, committed
- Deployed to Vercel — live URL
- Loop: brief → design → plan → build → verify → commit → deploy

**End with:**

> "That's W2-1 — and it's worth pausing on what you actually did. You started with a blank folder and ended with a real business page, live on the internet, with a URL you can send to anyone right now. Brief, design, plan, build, deploy — first time through that loop is always the hardest. You've got the reps now.
>
> Everything from here is a variation: different brief, different tools, same loop. It gets faster every time.
>
> Take the break."

Then: *"If you want to keep going — what feels most missing from the page right now? Tell me and I'll suggest one next move."*

---

## If learner says they're stuck

1. **Mirror first** — *"yeah, this part trips people up."*
2. Recap where they are in 1–2 sentences from conversation memory.
3. Offer 3 specific next moves: *"Three options: (a)... (b)... (c)..."*
4. If Claude is the blocker (looping, bad output): suggest `/clear` + re-read this file fresh. Don't retry the same prompt.
