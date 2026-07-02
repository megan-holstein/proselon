---
type: Procedure
title: Book Specs
description: Pre-plot research into KDP categories, comps, and genre conventions; produces Plot/Specs.md.
tier: craft
tags: [step-1, specs]
related: ["../2 - Series Plot/2.1 - Template.md"]
---
# Book Specs

Research market positioning and genre conventions before story development begins. This procedure produces a default specifications document that feeds the rest of the story development cascade.

## Prerequisites

A high-level premise exists (PITCH.md, a verbal description, or equivalent). This is just the concept — not the plot. No story development work (series plot, book plot, etc.) needs to exist yet.

## Verification and Provenance

Everything this step produces is market data the author cannot easily fact-check, and it feeds every downstream step — so fabricated data is the most damaging failure available here. Every claim in the output is one of two kinds:

- **Retrieved** — confirmed in search results actually fetched during this session (a live category page, a real listing, a review page). Prefer these; cite what was seen.
- **Unverified** — from model knowledge, not confirmed live. Tag it `(unverified)` inline. Never present an unverified title, category path, or "current bestseller" as retrieved.

If web search is unavailable, say so, tag all market claims `(unverified)`, and list them under Open Questions for the author to spot-check. A comp title or browse path that cannot be confirmed to exist does not go in the final three.

## Phase 1 — KDP Category Research

Search the KDP store (via web search) to identify the 3 most appropriate browse categories for the book's premise. For each candidate, confirm the full browse path exists, establish why it fits this premise, learn what readers browsing it expect, and collect representative bestsellers. The Output Template's KDP Category Analysis block is the field inventory — capture what it asks for, per category.

Talk through the candidates with the author and settle on the final 3. This consultation happens in every mode, including autopilot — category selection is a creative decision, never made alone.

## Phase 2 — Comp Title Analysis

Within the selected categories, identify 3–5 comparable titles — books sharing this project's premise, audience, or market positioning. Study each comp's length, structure, prose style, review reception, and cover. The Output Template's Comp Title Analysis block is the field inventory — capture what it asks for, per comp.

## Phase 3 — Genre Convention Research

Using the categories and comps from Phases 1–2, research the conventions for this genre and market position: structure (word count, chapter and scene norms), POV and tense, prose style, pacing, required beats and tropes, reader expectations and dealbreakers, tone, and cover design. The Output Template's convention sections — Structural Conventions through Book Cover Conventions — are the field inventory; research what each asks for.

## Phase 4 — Compile and Save Specifications

Fill the output template (below) with all findings from Phases 1–3. This produces a default specifications document.

Clearly separate "genre norm" from "recommendation for this project" in every section. The author may deliberately deviate from convention — deviations should be informed, not accidental.

Save the result as `Plot/Specs.md` (or update it if it already exists). Mode-driven interaction follows `AGENTS.md` — surface judgment calls and departures from genre norm in collaborative or detailed mode; in autopilot, save and report departures concisely after the fact. Category selection was already settled with the author in Phase 1, so no separate sign-off is required here.

## Completion Gate

`Plot/Specs.md` must exist before the story development cascade can begin. This is checked by the state detection procedure in `AGENTS.md`.

---

## Output Template

Use this template when compiling findings in Phase 4. Fill every section with genre norms and project-specific recommendations.

```markdown
# Publishing Specs

## Project Identity

- **Title**: [working title]
- **Genre**: [primary genre]
- **Subgenre**: [subgenre(s)]
- **KDP categories**:
  1. [Full browse path] — [why it fits]
  2. [Full browse path] — [why it fits]
  3. [Full browse path] — [why it fits]
- **Comp titles** (3–5):
  1. [Title] by [Author] — [what's comparable]
  2. [Title] by [Author] — [what's comparable]
  3. [Title] by [Author] — [what's comparable]
  4. [optional — include the 4th/5th comp if identified]
- **Target audience**: [description of ideal reader]

## KDP Category Analysis

### Category N: [Category Name]

- **Browse path**: [full path]
- **Reader expectations**: [what readers browsing this category are looking for]
- **Representative bestsellers**: [3–5 titles]
- **Why this book fits**: [rationale]

[Repeat this block for each of the 3 categories.]

## Comp Title Analysis

### [Title] by [Author]

- **Word count**: [approximate]
- **Structure**: [chapter count, chapter length, scene structure]
- **Prose style**: [register, sentence style, POV, tense]
- **Reception**: [common praise and complaints from reviews]
- **Cover style**: [imagery, color palette, typography, layout]
- **What's comparable**: [specific connection to this project]

[Repeat this block for each comp (3–5).]

## Structural Conventions

| Element | Genre Norm | Recommendation |
|---------|-----------|----------------|
| Word count | [range] | [target for this project] |
| Chapter count | [range] | [target] |
| Chapter length | [range] | [target] |
| Scenes per chapter | [range] | [target] |
| Scene length | [range] | [target] |

## POV and Tense Conventions

- **Genre norm**: [what's standard in this genre/category]
- **Recommendation**: [what this project should use and why]

## Pacing Conventions

- **Act structure norms**: [standard act structure for the genre]
- **Hook placement**: [where hooks are expected — chapter openings, endings, act breaks]
- **Pacing by quarter**:
  - First 25%: [expectations]
  - Second 25%: [expectations]
  - Third 25%: [expectations]
  - Final 25%: [expectations]
- **Chapter-end expectations**: [cliffhangers, reveals, quiet beats — what's normal]

## Prose Style Conventions

- **Register**: [formal, conversational, literary, pulpy, etc.]
- **Sentence style**: [short and punchy, complex and layered, varied, etc.]
- **Dialogue norms**: [ratio of dialogue to narration, dialect handling, etc.]
- **Description density**: [sparse, moderate, lush — genre expectations]
- **Genre-specific expectations**: [any stylistic conventions particular to this genre]

## Required Genre Elements

- **Tropes/beats readers expect**: [list]
- **Dealbreakers to avoid**: [things that will alienate genre readers]
- **Optional elements that perform well**: [not required but well-received]

## Reader Promises

[What readers of this genre/category are implicitly promised when they pick up the book. What the cover, blurb, and category placement signal about the reading experience.]

**Series promises** — the specific promises *this* project makes its readers, stated as commitments the story must pay off (the Series Plot assessment tracks each one to a delivery point):

- [Promise]
- [Promise]

## Tone and Atmosphere

- **Genre norms**: [typical tone range for the category]
- **Range of acceptable tones**: [how far you can push before leaving the genre]
- **Recommendation for this project**: [target tone and atmosphere]

## Book Cover Conventions

### Genre Norms

- **Dominant imagery**: [what typically appears — characters, objects, scenes, abstract elements]
- **Color palette**: [colors and color relationships common in the genre]
- **Typography**: [font styles, title weight, author name placement]
- **Layout patterns**: [composition norms — centered, asymmetric, full-bleed, etc.]
- **What signals genre to KDP browsers**: [the visual shorthand that tells a reader "this is [genre]"]

### Comp Cover Analysis

[Brief description of what the comp title covers have in common and where they diverge.]

### Recommendation for This Project

[Specific cover direction based on genre norms, comp analysis, and this project's positioning.]

### Cover Generation Prompt

[A ready-to-use prompt the author can paste into ChatGPT, DALL-E, Midjourney, or similar tools to generate a cover concept consistent with genre conventions and KDP design standards. Include: style direction, imagery, color palette, mood, typography guidance, and KDP thumbnail legibility requirements.]

## Open Questions

[Unresolved decisions, areas where the author should make a deliberate choice, places where convention conflicts with the project's creative goals.]
```

## Completion Criteria

Before marking this procedure complete, verify:

- [ ] Three KDP categories identified with rationale
- [ ] At least 3 comp titles analyzed
- [ ] All structural convention sections populated with genre norms AND project-specific recommendations
- [ ] Genre norms clearly separated from project recommendations
- [ ] Series promises listed as explicit, payable commitments
- [ ] Author deviations from convention explicitly noted with rationale
- [ ] Book cover conventions documented with genre norms and project recommendation
- [ ] Cover generation prompt included
- [ ] `Plot/Specs.md` saved
