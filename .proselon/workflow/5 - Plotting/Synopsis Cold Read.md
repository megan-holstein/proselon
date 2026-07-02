---
type: Pass
title: Synopsis Cold Read
description: Reader-experience assessment of a plan — the plot rendered as a plain synopsis and read cold, plus a prediction test that measures predictability instead of asserting it.
tier: craft
tags: [step-5, plotting]
related: ["Plot Stress Test.md", "../6 - Drafting and Editing/Cold Read.md", "5.2 - Book Plot Assessment.md"]
---
# Synopsis Cold Read

Tier: craft — reader judgment; run with the strongest available model.

Every plot assessor loads the full canon before judging — it knows every intention, so it cannot simulate not knowing the ending. The freshness criteria ask a judge who has read the answer to guess whether a reader would predict it; that is a weak instrument. This pass applies the Cold Read's insight one level up: let a fresh context meet the *plan* the way a reader will eventually meet the book, and let a second context try to *predict* the plan from its opening — converting freshness from an opinion into a measurement.

## When It Runs

- After the book plot clears its assessment panel (5.2), on a synopsis of the book plot.
- After the chapter map clears its panel (5.6), on a per-chapter synopsis of the map.
- During the Series Refresh (2.3), on a series-level synopsis of the refreshed series shape.

Alongside the Plot Stress Test; both are findings-only.

## The Report File

The book-plot run saves its merged report (cold read testimony, prediction scores, routing outcomes) to **`Plot/Book N/Synopsis Cold Read.md`**; the chapter-map rerun appends a **Chapter Map Rerun** section to the same file. The file's existence is how state detection knows the pass ran: **5.4 does not begin until the report exists with its findings resolved, and chapter plots (5.5) do not begin until the rerun section does.** The series-level run is recorded inside the Series Refresh report instead (see 2.3). Like the reading journal, the report is testimony, never canon — no drafting or plotting pass loads it as story truth.

**Bounded:** one full run, findings routed. When findings changed the plot, re-render the changed stretch and re-read once to confirm; append the result. A plan that takes the regeneration exit re-enters 5.2 as a new artifact and, on approval, gets a fresh run and a fresh report section. Each section opens by naming the plan version it read (date, and the commit in a git project) — a report whose newest section predates the current plot file is stale, and state detection treats the plan as unread. Not an open loop.

## Step 1 — Render the Synopsis

The orchestrating agent (or a fresh context) renders the plan as a **plain, reader-facing synopsis**: the story told in reading order as narrative summary — no planning vocabulary (no "act," "beat," "arc," "theme"), no intentions ("this establishes…"), no structure labels. Roughly 800–1,500 words for a book plot; one to two sentences per chapter for a chapter map; for the series level, one paragraph per shipped book (what a reader who finished it is carrying) plus a fuller 300–500-word treatment of the next book's shape. It should read like a detailed back-of-book-plus-spoilers summary a friend would tell you.

## Step 2 — The Cold Read

A fresh context loads **only the synopsis** — no canon, no specs, no plan documents — reads it start to finish, and reports:

- **Attention** — where did the summary itself get exciting? Where did your interest sag? A stretch of synopsis you had to push through usually maps to a stretch of book that will read the same.
- **Prediction** — at each major turn, had you already guessed it? Say which turns you called and how far back.
- **Confusion** — anything that didn't follow: motivation you didn't buy, causality you couldn't trace, a reveal that seemed to come from nowhere.
- **Appetite** — would you buy this book from this story? What's the moment in the synopsis that would sell it? Is there one?

Attest every check, one line each, even when clean. Verdict: **Approved** or **Needs revision**, naming the finding that most damages the read.

## Step 3 — The Prediction Test

Two more fresh contexts, run in sequence:

1. Give the first **only the opening ~25% of the synopsis** (for a chapter map: the first act's chapter lines; for the series level: the shipped books' paragraphs only). Ask it to predict, concretely: the midpoint turn, the crisis, the climax, and the ending (for the series level: the next book's central conflict, its major turn, and where the series threads land).
2. Give the second the opening **~50%**. Same predictions. (At series level there is one prediction context, not two — the shipped books are the only honest given.)

Score the predictions against the actual plan — a beat counts as *predicted* when the guess matches in substance, not wording. Report the hit rate and which beats were called.

**Reading the score:** major beats fully predicted from the 25% mark mean the plot is walking the genre's default path — measured, not asserted. Some hits are fine and some are necessary (genre promises *should* be guessable; the crisis existing is not a spoiler — its shape is). The finding is the pattern: a plan whose midpoint, crisis, *and* climax were all called early confirms expectations at every point where it could have turned them.

## Routing Findings

Findings route to the plot's freshness and momentum criteria: sagging synopsis stretches and early-called beats are Weaknesses with evidence attached; a heavily predicted plan is a Freshness failure and takes the regeneration exit (fresh structural alternatives), not an in-place patch. A confusion finding may indict the plan's causality — route it to the Plot Stress Test's hunter findings if one is running. Structural changes surface to the author.

One caution: the synopsis is a lossy rendering. Before acting on a finding, confirm it's a fact about the *plan* and not an artifact of the summary — a scene's texture, voice, and interiority don't survive summarization, so "the synopsis feels dry" is not a finding; "I called the climax from the first act" is.
