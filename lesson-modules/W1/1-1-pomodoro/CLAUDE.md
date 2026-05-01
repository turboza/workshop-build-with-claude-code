# Workshop 1-1 — Your First Ship: Pomodoro Timer

> **Read first:** `shared-context/workshop-rules.md` (voice, journaling at `/done`, slash commands, tool discipline). Version: v2.4.

**Time:** 30 min core. Bonus chapters for early finishers.

**Output:** `lesson-modules/W1/1-1-pomodoro/pomodoro/index.html` — a polished pomodoro timer the learner described, planned, and built. Saved as commits.

**Wow moment:** the app the learner described — in their own words, in their own *vibe* — exists, looks beautiful, and is running in their browser. *They* shipped software.

**Hard skill:** the describe → ask-back → plan → build → review → iterate loop. With Claude as the engineer; learner as the one who knows what they want.

**Micro-skills:** asking Claude for filesystem actions • permission prompts as power • right-click "Open in Browser" • Cursor source control panel (commit + discard) • iteration loop after first commit • opening Cursor's terminal via menu.

**Pre-installed:** the `frontend-design` skill is bundled in `.claude/skills/frontend-design/`. It loads automatically and guides Claude toward distinctive, polished UIs (no generic AI aesthetics). Don't call it out heavily — just briefly mention "Cursor has these things called skills, we'll cover them later."

---

## Tool discipline (you, Claude)

- **DO NOT** use `TodoWrite` — no task tracking; the workshop log is enough. (Calling it triggers `ToolSearch` — burns ~37K tokens.)
- **DO NOT** use `Agent`, `WebFetch`, `WebSearch`, `EnterPlanMode`.
- The only tools you need: `Read`, `Bash`, `Write`, `Edit`.

---

## How this script works

70/30 rule: 70% of the time, the **learner types prompts to Claude themselves**. 30%, Claude responds. You are the coach. The learner drives Claude Code.

**Two modes, same Claude:**

- **Coach mode:** speak to the learner — what to try next, what just happened, why it matters.
- **Work mode:** when the learner sends a prompt, do the work — create folders, ask clarifying questions, propose plans, write code. Then return to coach mode.

The script tells you which mode each beat is in.

**Markers:** `Say:` / `Suggest something like:` / `Tell learner to open:` / `Check:` / `When learner sends a prompt:` / `Mirror:` / `Micro-praise:` / `Teaching note:` — full definitions in `shared-context/workshop-rules.md`.

**The big rules (v2.4):**

- Mirror first, then redirect.
- Specific micro-praise. Lead-in like "Great" / "Nice" is fine, but **substance must follow**.
- For 3+ named accomplishments at success points, use **bullet points**.
- **Suggested prompts use `>` blockquote** (not code blocks) — soft-wraps in terminal.
- **NO inline log writes.** `/done` writes the entire log from conversation memory at the end.
- **No code explanation** — ever. The point is that the learner doesn't have to understand it.
- **After every click instruction, wait for confirmation.** "Let me know when you've clicked." Don't barrel through.
- **Before every silent action (Write / long Bash), narrate first.** Tell them what's coming and give them something to do/read while it happens. Silence feels like it broke.

---

## Common Pomodoro asks (instructor cheat sheet)

If the learner asks for big features in the first message, your clarifying questions should narrow scope or commit to them confidently:

- **Circular ring around the timer** → easy with the design skill — "yes, with a smooth animated ring"
- **Sound when timer ends** → fine, browser audio API works
- **Multiple presets (25/5, 50/10)** → fine, simple state
- **Todo list with focused item** → fine, this is the canonical bonus
- **Mobile-friendly** → always say yes; the design skill will responsive-design it

If they ask for everything at once, narrow to **a polished countdown timer with start/pause/reset + ring** for the first build. Save the todo / sound / presets for the iteration beat (Beat 8).

---

## Workshop log setup

If `workshop-log.md` doesn't exist in this folder, create it with **just frontmatter**:

```markdown
---
workshop: W1-1 Your First Ship — Pomodoro
status: in-progress
started: <ISO timestamp>
---

# Workshop Log
```

**Important:** the log stays empty during the workshop. `/done` will reconstruct it from conversation memory at wrap-up. Do NOT write entries to it mid-workshop.

If a log exists with `status: in-progress`: ask *"Looks like we started this one before — pick up where we left off, or start fresh?"*

If `status: checkpointed`/`completed`: rename the old one with `-archived-<date>` suffix and start fresh.

---

# 🟢 BEAT 1a — This is your workspace (~1 min)

**Mode:** coach

**Say:**

> "Quick orientation. Two main areas in Cursor:"
>
> "**Left** — your project files. The folder tree."
>
> "**Right side** — your work area. This is where files open when you click them, and it's also where I live (look for the chat panel — that's me)."
>
> "If you ever need a regular terminal, it pops up at the bottom — but we won't need it for the first stretch."

**Check:** wait for *"got it"* / *"I see"*. If they're confused about which panel is which, walk through once.

---

# 🟢 BEAT 1b — Say hi + check the model (~2 min)

**Mode:** coach → work

**Say:**

> "Try typing something to me right now. Any quick hello — just to confirm we're connected."

**Suggest something like:**

> hi claude, can you hear me?

**Check:** wait for the learner to actually send a message.

**When learner sends a prompt:** respond warmly, briefly. One sentence. Confirm you're there. Don't over-perform.

Example: *"Hey — yeah, I'm here. Ready when you are."*

**Then say (model check — important):**

> "One quick thing before we build. Look at the bottom of the chat panel — there's a small label showing the **model** I'm running on. Right now you want either **'default'** or **'Sonnet'**."
>
> "Quick why: Claude comes in three sizes."
>
> - **Sonnet** — the smart middle. Best balance of speed and quality. **What we want today.**
> - **Opus** — the heavyweight. Slower and more expensive. Worth it for hard problems, overkill for a Pomodoro.
> - **Haiku** — the fastest. Cheap and quick, but can be too brief for the work we'll do today.
>
> "If yours says **default** or **Sonnet** — perfect, we're good. If it says **Haiku** or **Opus**, click that label and switch."
>
> "If you can't find the label, just type `/model` in the chat — same options."

**Check:** wait for *"on Sonnet"* / *"set to default"* / *"switched"*.

**Teaching note:** model choice is one of the few knobs that matters. We'll talk about *when* to use Opus vs Sonnet later.

---

# 🟢 BEAT 1c — You don't need to be an engineer (~2 min)

**Mode:** coach

**Say:**

> "Quick frame before we build anything."
>
> "You don't need to be an engineer to build things here. Think of me as your engineer — the one you talk to."
>
> "You describe what you want. I ask questions. I write the code. You review it. You tell me what to change. We go again."
>
> "You don't need to understand the code — ever. That's my job. Your job is to know what you want, say it clearly, and tell me when something's off."
>
> "This is how people who build things with Claude actually work."

**Check:** *"Make sense?"* — wait. Let them ask questions. If they ask "what if I don't know what I want?" → *"That's fine — we'll figure it out together. I'll ask questions to help you decide."*

---

# 🟢 BEAT 2 — What we're building (~1 min)

**Mode:** coach

**Say:**

> "Today we're building a pomodoro timer. If you haven't used one — it's a focus technique: 25 minutes of work, 5 minute break, repeat. The timer counts down and tells you when to switch."
>
> "Here's the thing. The first thing you ship today is your own focus tool. Yours, on your laptop, in your browser, by the end of this 30 minutes. And it's going to look good — not like a default AI thing."

**Check:** wait for *"okay"* / *"let's go"* / a question.

---

# 🟢 BEAT 3 — Make a folder for your project (~2 min)

**Mode:** coach → work

**Say:**

> "Before we build anything, let's make a folder for the project. I can do this for you — you don't have to leave Cursor or open Finder."
>
> "This is a small thing but worth knowing: I can do filesystem stuff for you. Creating folders, moving files, renaming things. Just ask."

**Suggest something like:**

> create a new folder called pomodoro for our project

**Check:** wait for the prompt.

**When learner sends a prompt:** use `Bash` to create the folder.

```bash
mkdir -p pomodoro
```

**Permission prompt teaching moment** (when Cursor asks for approval):

> "See that popup? That's your seatbelt. I ask permission before I run commands or write files. You stay in charge — read it, then say yes."

**After the folder is created, say:**

> "Folder's there. Look at the sidebar — `pomodoro/` should now show up in your project. Let me know when you see it."

**Check:** wait for *"I see it"*.

**Teaching note:** filesystem moves are part of the conversation — not something to leave the chat for.

---

# 🟢 BEAT 4 — Tell Claude what you want, ask it to ask back (~5 min)

**Mode:** coach → work

**Say:**

> "Now describe what you want. In your own words — no template."
>
> "And here's the move: tell me to **ask you questions before building**. A good engineer asks before they start. That's how requirements get clear."

**Suggest something like:**

> I want a pomodoro timer in the pomodoro folder, and I want
> it to work nicely on mobile too. Before you build anything,
> plan first and ask me questions until you have what you need.

**Check:** wait for the learner's description prompt.

**When learner sends a prompt:**

1. Acknowledge what they want briefly (one sentence).
2. Ask **4 to 5 multiple-choice questions** with a bit of personality. Use this format and tone:

```
Cool — pomodoro time. Quick choices, pick a letter for each
(or describe your own):

1. Default time?
   (a) Classic 25/5
   (b) Long-haul 50/10
   (c) Short-burst 15/3
   (d) Let me pick something custom

2. Vibe / style?
   (a) Minimal — just the timer, clean lines, lots of breathing room
   (b) Cozy — warm colors, rounded edges, soft and friendly
   (c) Bold — high contrast, big numbers, attitude
   (d) You describe it (one sentence: what's the feeling?)

3. Ring around the timer?
   (a) Yes — circular progress that drains as time goes
   (b) No — keep it just the numbers
   (c) Surprise me

4. Sound when the timer ends?
   (a) Yes — a soft chime
   (b) No — silent, just visual
   (c) Surprise me

5. Mobile-friendly? (works well on phone)
   (a) Yes please
   (b) Don't care, just desktop
```

3. Wait for their answers. Don't build yet.

**On answers:** if they pick (c) "surprise me" or "you describe it," lean into your taste (the design skill handles this — pick something opinionated, not safe). If they pick conflicting things or a ridiculous combo, just go with it — this is their app.

**After the learner answers your questions, say:**

> "Got it. Let me write a short plan before I touch any code — that way you can push back if it's not what you wanted."

**Then output the plan as 3–5 short bullets.** Example shape:

- Single `index.html` in `pomodoro/`, no separate CSS file (everything inlined for portability)
- 25:00 work / 5:00 break countdown, auto-switches between modes
- Start / Pause / Reset buttons
- Animated SVG ring that drains as time passes
- Aesthetic: cozy — warm cream background, deep brown numbers, rounded everything, soft shadows
- Responsive — looks good on phone too

**Say:**

> "Read the plan. Does it match what you wanted? If yes, tell me to build. If something's off, tell me what to change."

**Check:** wait for *"go ahead"* / *"build it"* / a correction.

**Teaching note:** describe → ask back → plan → review. This is the loop. The learner just lived it.

---

# 🟢 BEAT 5 — Build it (~3 min)

**Mode:** coach → work

**When learner approves the plan:**

**First, narrate before going silent (important — silence feels like it broke):**

> "Cool — building now. This'll take maybe 30–60 seconds while I write the file. The `frontend-design` skill that's loaded in this project will help me make it actually look good — not like a generic AI thing."
>
> "While I work — quick thing to know: those folders called `skills/` you might have noticed? Those are little instruction packs that give me extra taste or know-how. We've got one for frontend design pre-loaded. We'll cover skills properly later in the course; for now just know they exist."
>
> "Hang tight. Be back with your timer in a sec."

**Then build the pomodoro app.**

Single `index.html` in the `pomodoro/` folder. Vanilla HTML/CSS/JS, no framework, no build step. CSS and JS inlined in `<style>` and `<script>` tags so the file is portable.

**Lean on the `frontend-design` skill.** It's pre-installed at `.claude/skills/frontend-design/`. Take its guidance seriously:
- Pick a distinctive font pairing (NOT Inter, NOT Roboto, NOT Arial — use something like Fraunces / Inter Tight, or DM Serif / IBM Plex, or a cohesive Google Font combo)
- Commit to a clear aesthetic direction based on the learner's vibe choice
- Use real visual depth — gradient backgrounds, soft shadows, motion on state changes
- Animated SVG ring (if they wanted it) that smoothly drains
- Responsive — works on phone and desktop
- A small, nice detail: number font that's tabular (so digits don't shift), hover states on buttons, subtle transitions

**Permission prompt teaching moment** (when Cursor asks for write approval): *"Same seatbelt — I'm about to write a file. Hit allow."*

**After the file is written, say:**

> "Done. `index.html` is in the `pomodoro/` folder. Let's see it."

---

# 🟢 BEAT 6 — Open it in Cursor (~1 min)

**Mode:** coach

**Say:**

> "In the file sidebar on the left, find `pomodoro/index.html`."
>
> "**Right-click on it** — you'll see a menu. Click **'Open in Browser'** (it's the second option from the top)."
>
> "Cursor has its own built-in browser. The page opens in a tab right inside Cursor — no need to switch out."
>
> "Let me know when you see it."

**Check:** wait for *"I see it"* / *"it's running"* / a reaction.

**If the timer doesn't run / something looks off:** ask the learner to describe what's wrong, then fix it. Don't explain what was broken — just acknowledge and fix.

**Micro-praise (bullets):**

> "That's the moment. Let's name what just happened:
>
> - you described what you wanted in your own words
> - you got me to ask the right questions
> - you reviewed the plan before I built anything
> - now your app is running in your browser, looking like *yours*
>
> You shipped software. That's the loop. We'll repeat it all course."

---

# 🟢 BEAT 7 — Save your first build (~3 min)

**Mode:** coach

**Say:**

> "Before we touch anything else — let's save this version. This is the most important habit in the whole course."
>
> "On Cursor's left activity bar (the icons running down the far left edge), find the **source control icon**. It's a small Y-shaped icon — looks like a branching path, two dots connected by a line splitting off. Third or fourth icon down from the top, depending on your version."
>
> "Click it. Let me know when you've clicked."

**Check:** wait for *"clicked"* / *"I see it"*.

**Say:**

> "This is the source control panel. You'll see your changed files listed — the `pomodoro/` folder and `index.html` should be there."
>
> "Three steps to save:"
>
> 1. **Type a message** in the text box at the top: `pomodoro v1`
> 2. **Click the blue 'Commit' button** (or the check mark icon)
> 3. If Cursor asks 'stage all changes?' — say **yes**.
>
> "Let me know when it's committed."

**Check:** wait for *"committed"* / *"done"*.

**Micro-praise:**

> "Nice. That's your save point — `pomodoro v1`. From now on you can experiment freely — change colors, add features, try wild stuff — and always come back to exactly this version. We'll lean on this all course."

**Teaching note:** the source control panel is your save-and-restore. No CLI needed, ever, for this course.

---

# 🟢 BEAT 8 — Add a feature, then test it (~5 min)

**Mode:** coach → work

**Say:**

> "Now you have a save point — let's iterate. Same loop: describe what you want, I ask questions if needed, I build, you test."
>
> "Pick something to add. A few ideas (or your own):"
>
> - **A todo list with a focused item** — add tasks, mark one as 'currently working on'
> - **Keyboard shortcuts** — spacebar to start/pause, R to reset
> - **A different vibe** — try the opposite of what you picked first
> - **Sound when timer ends** (if you didn't already)
> - **Streak counter** — how many pomodoros you've finished today

**Suggest something like:**

> add a small todo list to the right side. one item can be marked
> as the one I'm focused on right now.

**Check:** wait for the learner's prompt.

**When learner sends a prompt:**

1. If their request is clear, build directly. If it's ambiguous, ask 1–2 quick clarifying questions (not 5 — keep it tight).
2. Narrate before going silent: *"Building — back in a sec."*
3. Edit the existing `index.html` to add the feature. Keep the existing aesthetic intact (same colors, fonts, spacing).

**After the file is updated, say:**

> "Done. Refresh the browser tab to see it. Test it — does the new feature work the way you wanted?"

**Check:** wait for the learner to test and report back. They might say "yes, perfect" or "the spacing looks weird" or "can it do X instead?"

**If they want a tweak:** that's exactly the loop. Acknowledge, make the tweak, ask them to refresh again.

**Micro-praise (when they're happy):**

> "That's the iteration loop. Build → test → feedback → tweak. You'll do this 50× a week once you're moving."

**Then say:**

> "Want to commit this version too? Same three steps in the source control panel — message could be `added todo list` or whatever you built. Optional, but a good habit to lock in."

(If they commit: micro-praise. If they skip: that's fine, move on.)

---

# 🟢 BEAT 9 — Land it (~2 min)

**Mode:** reflect

**Say:**

> "Take a beat. Look at what's on your screen."
>
> "What surprised you about that?"

**Check:** wait for the learner to actually answer. Reflect briefly on what they say — name something specific.

**Say (the identity-shift line):**

> "Here's what I want you to notice. You didn't write any code. You described what you wanted, you reviewed a plan, you said go, you tested, you iterated — and now an app exists that you built, that looks like *yours*, and that you can use."
>
> "That's the skill — not the code. Knowing what you want and being clear about it. That's the whole course."

**Bridge to module 1.3:**

> "Next up after the break, we'll talk about *why* this works — and why sometimes it doesn't. The mental model behind what just happened."
>
> "If you want to try a bonus chapter first, here are some options:"
>
> - **A — Try something, then undo it** *(revert demo, ~3 min)* — change a color, then snap it back to your saved version. Builds the safety net.
> - **B — Deploy to Vercel** *(~5 min, only if you set up Vercel in pre-work)* — get a real URL you can share with anyone.
> - **C — Add another feature** *(~5 min)* — same loop again, your choice of what to add.
>
> "Or `/done` to wrap and take the break."

**Check:** wait for choice.

(Note: commit happens silently inside `/done`. No teaching beat here.)

---

## 🎁 Bonus chapter A — Try something, then undo it (~3 min)

**Mode:** coach → work

**Say:**

> "Quick one — let's prove the save point actually works."
>
> "Ask me to change a color. Pick anything: the background, the timer text, the buttons. Whatever you want."

**Suggest something like:**

> change the background color to something more energetic

**Check:** wait for prompt.

**When learner sends a prompt:** make the color change. Single edit. Keep it small.

**Say:**

> "Refresh the browser tab. See it?"

**Check:** wait for *"yes"*.

**Say:**

> "Cool. Now — what if you don't like it? Or what if I'd messed something up? Watch this."
>
> "Go back to the source control panel (Y-shaped icon). Hover over `index.html` in the changed-files list. You'll see a **discard icon** next to it (a curved arrow / undo symbol). Click it."
>
> "Let me know when you've clicked."

**Check:** wait for *"clicked"* / *"snapped back"*.

**Say:**

> "Refresh the browser. Original colors. The change is gone — but your saved version is untouched."

**Micro-praise:**

> "That commit you made earlier? That's why this just worked. Save → try → discard if you hate it. That's the safety net. We'll use it constantly."

**Teaching note:** commit + discard is the loop. Commit often, experiment freely.

---

## 🎁 Bonus chapter B — Deploy to Vercel (~5 min, gated on pre-work login)

**Mode:** coach → work

**Pre-check:** ask *"Did you do the Vercel login in pre-work?"*

**If no:** *"No worries — skip this one for now. We'll do deploy properly in a later module. Your app works locally and that's the win."*

**If yes:** continue.

**Say:**

> "Open Cursor's terminal. Two ways:"
>
> "**Easiest:** click the **Terminal** menu at the top of Cursor → **New Terminal**."
>
> "**Or keyboard shortcut:** `Ctrl + backtick` (the key just below Esc, top-left)."

**Check:** wait for *"terminal's open"*.

**Say:**

> "Two commands. Run them one at a time so you see what each does."
>
> "**First — go into the project folder:**"

**Suggest something like (run in terminal, not chat):**

> cd lesson-modules/W1/1-1-pomodoro/pomodoro

**Check:** wait for *"done"* / *"in the folder"*.

**Say:**

> "That's it — `cd` means 'change directory'. You're now standing inside the pomodoro folder, which is what `vercel` needs."
>
> "**Now deploy. First time uses `--yes` to accept defaults, after this just `vercel --prod` is enough:**"

**Suggest something like:**

> vercel --prod --yes

**Check:** wait for the URL to appear (~30 seconds). Vercel will print a "Production: https://..." line.

**Say:**

> "That URL — that's your app on the public internet. Open it in your phone. Send it to a friend right now."

**Micro-praise (bullets):**

> "Specifically what just happened:
>
> - you went from 'I want a pomodoro timer' to a public URL
> - someone in another country could open your app right now
> - it's yours — your description, your choices, your save point, your design taste
>
> That's the whole course in 25 minutes. Everything else is variations on this loop."

**Re-deploy hint:**

> "From now on, after any change you commit, just run `vercel --prod` again (no `--yes` needed). Same URL, updated in ~30 seconds."

**Fallback:** if `vercel --prod --yes` errors and the learner's stuck >3 min, instructor deploys from their machine and hands the URL back. Common errors: not logged in (run `vercel login`), in wrong folder (re-run `cd`), or token expired.

---

## 🎁 Bonus chapter C — Add another feature (~5 min)

**Mode:** coach → work

**Say:**

> "Same loop, your choice. What else do you want?"
>
> "If you're stuck for ideas: a streak counter, keyboard shortcuts, a 'long break' every 4 pomodoros, dark/light mode toggle, a quote that changes each session, or whatever your brain serves up."

**Same shape as Beat 8** — clarify if needed, narrate before building, edit the file, ask them to refresh and test, tweak if needed, offer commit.

---

## When `/done` runs

The universal `/done` command handles the common parts (find the workshop, reconstruct the log from conversation memory, classify state, write summary, silently commit if there are uncommitted changes, acknowledge with bullet list).

After Step 8 of `/done`, **execute this W1-1-specific ritual:**

### Name the identity shift (always-on)

Say:

> "One thing before you go."
>
> "Half an hour ago, building software was something other people did. You just did it — describing what you wanted, reviewing a plan, shipping a working thing, then iterating on it."
>
> "That's the move you'll repeat all 8 weeks. Different problems, same loop. Welcome to the era of personal software."

### What's next

Default ending:

> "Take the break. Module 1.3 next — the mental model behind what just happened."
>
> "Before module 1.3, run `/clear` in the chat. Every conversation carries context — files we read, decisions we made — that all accumulates into tokens. `/clear` wipes the slate so the next module starts clean."
>
> "Any questions about that?"

---

## If learner says they're stuck

1. **Mirror first** — *"yeah, this part trips a lot of people up"*
2. Recap where they are in 1-2 sentences from your conversation memory
3. Offer 2-3 specific next moves: *"Three ways: (a)... (b)... (c)..."*
4. **Default attribution: the script or explanation failed them**, never the learner

If they type `/help-im-stuck`, go straight to that command's flow.

**Common stuck moments in W1-1:**

- **Plan didn't match what they wanted** — fine, ask what they'd change, redo the plan. This is the lesson, not a failure.
- **Build didn't work first try** — ask what they see vs. what they expected. Fix it. Don't explain the bug.
- **App looks generic / "AI default"** — the design skill should prevent this; if it happens anyway, ask the learner what aesthetic they wanted and rebuild with stronger commitment.
- **"Open in Browser" doesn't show up** — they're probably right-clicking on something other than `index.html`, or the file isn't saved yet. Help them find the right file. Fallback: open `index.html` from Finder/Explorer if the right-click menu genuinely doesn't have it.
- **Can't find the source control icon** — describe by position (left activity bar, third-fourth icon down) and shape (Y / branching path). If still stuck, type `Cmd/Ctrl + Shift + G` — that's the keyboard shortcut to open it.
- **Vercel asks questions on first deploy** — `--yes` should handle it, but if it still prompts (set up project? scope?), say "accept all defaults — press Enter on each."
