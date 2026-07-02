# Proselon

**An AI developmental editor that runs your book's development for you** — from premise to published, as plain files on your own computer.

Proselon is a free, open writing system for novelists who want to *finish a book worth reading*. You bring the story; the AI acts as your developmental editor — interviewing you about your vision, organizing your ideas into structured planning documents, and drafting prose in your voice through a disciplined, multi-pass editorial process. It is **not** a one-click book generator: you are the creative decision-maker, you approve every step, and nothing happens without your say-so.

It runs on the **Claude or ChatGPT subscription you already pay for**, and your whole manuscript stays as Markdown files on your own disk — no cloud, no lock-in, no monthly fee for the tool itself.

> **Real books, really published.** Proselon has been used to write and publish full-length novels on Kindle. This is a craft tool for finishing real work — not a slop machine.

Learn more, read the method, and join the waitlist for the upcoming Proselon app at **[proselon.com](https://proselon.com)**.

## What You Need

Proselon runs on an AI subscription you may already have — there's no separate fee for the tool itself. You need **one** of:

- A **Claude** subscription (any paid plan) — Proselon uses it through Claude Code
- A **ChatGPT** subscription (Plus or Pro) — Proselon uses it through Codex, the part of ChatGPT that works with the files on your computer

If you have both, Proselon uses Claude Code — the version it's built and tested on. Don't have either installed yet? The launcher in the next step installs one for you.

## Installation

Proselon works with any AI coding agent that can read and write files on your computer — Claude Code, Codex, Cursor, Windsurf, or others. You just need to get this project folder onto your machine and open your agent inside it.

1. **Get the project folder onto your computer.** If you downloaded Proselon, unzip it and move the folder wherever you want your novel to live — your Documents folder is a good choice. Rename the folder to your book or series title if you like.

   If you're comfortable with Git, you can clone it instead:

   ```
   git clone https://github.com/megan-holstein/proselon.git "My Novel Title"
   ```

2. **Open your AI coding agent inside that folder.** The easiest way is the launcher — double-click it and it walks you through everything, including installing the writing engine if it isn't installed yet:

   - **Mac:** `Start Proselon - Mac.command`
   - **Windows:** `Start Proselon - Windows.bat`

   The launcher uses whichever writing engine you have installed (Claude → Claude Code, ChatGPT → Codex), and only asks which subscription you use if you have both or neither.

   If you're using Cursor, Windsurf, or another editor-based agent, open the folder as a project in that editor instead.

3. **Log in the first time.** When the agent starts, it asks you to sign in:

   - **Claude:** choose **"Claude account"** and log in the way you normally log in to Claude.
   - **ChatGPT:** choose **"Sign in with ChatGPT"** and log in the way you normally log in to ChatGPT.

   That connects Proselon to your own subscription. Then just start talking about your story.

### If your computer blocks the launcher

Downloaded launchers are sometimes blocked the first time. It's harmless, and you only have to clear it once:

- **Mac:** if you see "cannot be opened because it is from an unidentified developer," **right-click the launcher and choose Open**, then click **Open** in the dialog. On newer macOS you may instead need to open **System Settings → Privacy & Security**, scroll down, and click **Open Anyway**.
  - If you instead see a message about **"appropriate access privileges,"** or the launcher opens in a text editor, it lost its run permission when it was downloaded. Open Terminal, type `chmod +x ` (with a trailing space), drag the launcher into the Terminal window, press Return, then double-click it again.
- **Windows:** if you see a blue **"Windows protected your PC"** screen, click **More info**, then **Run anyway**.

## Updating

Proselon improves over time, and pulling the latest framework into an existing project is a one-liner. There are two ways to do it — use whichever you like.

**Just ask your AI agent.** Open your project and say *"update Proselon"* (or *"update yourself"*). It runs the updater for you and confirms when it's done — same on every platform, nothing to type.

**Or run it yourself,** from inside your project folder:

```
curl -fsSL https://raw.githubusercontent.com/megan-holstein/proselon/main/.proselon/scripts/update.sh | sh
```

- **Mac / Linux:** works as-is in the normal Terminal.
- **Windows:** use the PowerShell updater instead — open PowerShell inside the project folder and run:

  ```
  powershell -ExecutionPolicy Bypass -File ".proselon\scripts\update.ps1"
  ```

  (The `curl` one-liner also works unchanged in Git Bash or WSL, if you have those.) Or just ask the agent — see above.

Either way it refreshes Proselon's own files in place — the process docs under `.proselon/`, this README, and the launchers — straight from the public repo. It's independent of your project's own version control, so it works no matter how (or whether) you use Git. **It never touches your writing** (`Plot/`, `Manuscripts/`, `Worldbuilding/`, …) or your Obsidian setup (`.obsidian/`) — only Proselon's files change.

> **For AI agents:** when the author asks to update Proselon (or "update yourself"), run the updater from the project root — `sh .proselon/scripts/update.sh` on Mac/Linux, or `powershell -ExecutionPolicy Bypass -File ".proselon\scripts\update.ps1"` on Windows. Either script handles everything safely on its own: it refreshes only Proselon's framework files and never touches the author's writing. If neither shell is available, read the script and reproduce its steps directly.

## Getting Started

Once your AI agent is open in your project folder, just tell it about your story, in your own words:

> *"I want to write a mystery set in a lighthouse town in the 1950s."*

> *"I have a fantasy series about two sisters on opposite sides of a war. Where do we start?"*

> *"Here's a premise — just run with it and show me what you come up with."*

You don't need to know anything about the files in this project; the AI manages all of that behind the scenes. If you already have a premise, tell it. If you're still figuring it out, say so — it'll help you work through it. You can be as hands-on or hands-off as you like.

## How the Process Works

The AI guides you through your novel in stages, from the big picture down to individual scenes. How collaborative each stage gets is up to you — you can hand it a one-line premise and say "just write it," spend an hour talking through a single character before any planning gets saved, or sign off on every detail. The AI adapts.

By default, it works like a developmental editor:

1. **Interviews you** — asks open-ended questions about your story, characters, world, and intentions. This is a conversation, not a form. Talk naturally.
2. **Organizes your answers** — takes what you said and shapes it into a structured planning document.
3. **Checks in at natural seams** — when a foundation decision is settling (the shape of the series, the themes, the voice) or when something it found needs your call, it'll show you the work and ask if it's right.
4. **Keeps moving** — fills in the routine work without making you sign off on every step.

You can change the mode anytime:

- **"Just run with it"** — the AI takes the wheel, only stopping for hard blockers
- **"Walk me through every step"** — the AI checks in before saving anything
- **"Let's go deep on X"** — the AI sets aside the cascade and works the area you want

The stages, roughly in order:

- **Book specs** — what market category your book fits, what readers of that genre expect, how long the book should be
- **Series plot** — the big-picture shape of your series: premise, arc, major movements, threads that carry across books
- **Themes and conflict** — what your story is *about*: themes, the central outer conflict, and each major character's inner conflict, mapped across the series
- **Style and voice** — how the prose should sound: sentence style, POV, tense, vocabulary, what to avoid
- **Book plot** — the arc of a single book: what happens, how the characters change, where it starts and ends
- **Chapter map** — what belongs in each chapter, how the book's pacing works
- **Chapter plots** — detailed arc for each chapter, a few chapters at a time
- **Scene plots** — specific plans for individual scenes
- **Drafting** — the AI writes prose from approved scene plots, matching your style guide
- **Editing and proofing** — developmental editing, a voice pass, line editing, continuity checks, copy editing, and proofreading
- **Publishing** — title selection, KDP listing (blurb, categories, keywords, author bio), cover design, ebook formatting, and going live on KDP (pricing, royalties, and the upload walkthrough)

You don't have to think about this sequence. The AI tracks where you are and suggests what to do next. If you want to skip ahead or circle back, just say so.

## What You Can Say at Any Time

You're not locked into a rigid process. Some things you can always do:

- **"Let's work on Chapter 3"** — jump to a specific part of the project
- **"I changed my mind about the ending"** — the AI will help you figure out what needs to change downstream
- **"This scene isn't working"** — it'll diagnose the problem and suggest fixes
- **"Make the prose more clipped and tense"** — style feedback gets incorporated
- **"What should we do next?"** — if you're not sure where things stand
- **"I don't like that"** — the AI will ask what's wrong and revise

The AI is your collaborator, not your boss. Push back on anything that doesn't feel right.

## What to Expect from the AI

**It will have opinions.** If it thinks a plot point is weak, a character arc is missing a turn, or a chapter is doing too much, it'll tell you. This is a feature. You’re working with a developmental editor, not a yes-machine.

**It will ask before acting.** It won't rewrite your approved plans or change your story without asking. If something needs to change, it'll explain why and wait for your call.

**It will remember your project.** It reads your planning documents, character profiles, worldbuilding, and style guide before writing or editing. You don't need to repeat yourself across sessions — just open your agent and the AI will pick up where things left off.

**It won't always be perfect.** AI-generated prose needs your eye. The editing passes catch a lot, but your taste and judgment are what make the book yours. Read what it writes. Mark what doesn't work. The AI will fix it.

## Reading Your Book

Your manuscript and plans are plain text (Markdown) files, so you can open and edit them with anything. For a nicer experience, we recommend **[Obsidian](https://obsidian.md)** — a free app that shows your whole project as a sidebar of cleanly formatted pages.

It's entirely optional; your book is the same plain files with or without it. To use it, install Obsidian, then the first time click **"Open folder as vault"** and choose this project folder. From then on, the launcher opens Obsidian straight to your book each time you start Proselon — so you can write in one window and read in the other. If Obsidian isn't installed, the launcher simply skips it.

## Saving Your Work

**Your book is always saved.** The latest version of everything — manuscript, plans, characters — lives right here in this folder on your computer, exactly where you left it: your manuscript in `Manuscripts/`, your plans in `Plot/`, your characters and world in `Worldbuilding/`. Close the window and reopen the launcher anytime; Proselon picks up exactly where it left off, because these files *are* the complete state of your book — nothing is lost between sessions.

**Optional: version history.** If you'd also like to go back in time — to see or restore earlier versions of your project — Proselon can keep that history for you. It needs one free tool (Apple's developer tools on a Mac, or Git on Windows). The launcher offers to set it up, and you can also just tell your editor *"I want version history"* at any point. If you skip it, nothing is ever lost; you simply always have the latest version.

## Tips

- **Be specific about what you don't like.** "This doesn't work" is fine as a starting point, but "the dialogue feels too formal" or "she wouldn't react that way" gives the AI something to act on.
- **Don't worry about being polished.** Ramble, brainstorm, contradict yourself. The AI's job is to sort through that and find the story. You can think out loud.
- **Trust the interview process.** The AI will ask questions that might seem basic or obvious. It's building a shared understanding of your story so it can write prose that matches your vision, not a generic version of your premise.
- **You can always say "I don't know yet."** Not every question needs an answer right now. The AI will mark it as an open question and come back to it when it matters.

## License

Proselon is source-available under the [PolyForm Noncommercial License 1.0.0](LICENSE.md) — free to use, modify, and share for any noncommercial purpose. **Anything you write with Proselon is entirely yours, including books you sell.** Commercial use of the harness itself (selling, hosting, or repackaging it as a paid product or service) requires a separate commercial license from Megan Holstein. "Proselon" is a trademark; please give forks and derivatives a different name. See [LICENSE.md](LICENSE.md) for details.
