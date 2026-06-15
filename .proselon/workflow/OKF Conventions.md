---
type: Reference
title: OKF Conventions
description: How Proselon's knowledge docs carry OKF metadata — frontmatter fields, type vocabulary, cross-link rules, and what we deliberately skip.
tags: [reference, okf]
---

# OKF Conventions

Proselon's knowledge docs follow the **Open Knowledge Format** (OKF): a body of knowledge is a directory of markdown files where each file is one *concept*, carrying a little YAML frontmatter and cross-linking to the concepts it relates to. Proselon was already 90% there (one markdown file per concept, `H1` matches filename); these conventions close the gap so the docs form a navigable, visualizable graph.

Two bodies of knowledge use this format:

- **The story bible** the author builds — `Worldbuilding/`, `Plot/`, `Research/`, `Style/`.
- **The framework itself** — the docs under `.proselon/workflow/`.

`Manuscripts/` and `Fragments/` are **excluded**: manuscript files are export-safe prose only, and fragments are raw scraps. Never add frontmatter to either.

## Frontmatter

Every concept doc opens with a frontmatter block. Only `type` is required.

```yaml
---
type: Character          # required — see vocabulary below
title: Alice Chen        # human-readable name; matches the H1
description: Reluctant heir who carries the freedom-vs-duty theme.   # one line
tags: [book-1, pov]      # optional, free-form
---
```

Framework docs add two fields:

```yaml
---
type: Pass
title: Line Assessment
description: Independent sentence-level prose-quality assessment; returns findings, does not edit.
tier: craft              # craft | mechanical — the model tier for this task
tags: [step-6, editing]
related: ["6.5 - Continuity Check.md"]   # see Cross-links
---
```

### `type` vocabulary

**Story bible:** `Book Specs`, `Series Plot`, `Themes & Conflict`, `Style Guide`, `Voice Reference`, `Book Plot`, `Story State`, `Chapter Map`, `Chapter Plot`, `Scene Plot`, `KDP Listing`, `Character`, `Location`, `Faction`, `Worldbuilding` (catch-all topic — magic system, history, technology, culture…), `Research`.

**Framework:** `Template`, `Rubric`, `Pass`, `Procedure`, `Reference`.

Use the closest fit; the value is a human-readable label, not an enum the system enforces.

## Cross-links

Cross-links are the graph's edges. Two mechanisms, by body of knowledge:

- **Story-bible docs link inline, in the body**, using standard markdown links wherever the content naturally names another concept — `POV: [Alice Chen](<../../Worldbuilding/Characters/Alice Chen.md>)`, `Member of [House Vard](<../Factions/House Vard.md>)`. This is OKF-canonical and, because they're real markdown links, **Obsidian's graph view renders them for free** (with "Use [[Wikilinks]]" turned off in Obsidian settings).
- **Framework docs declare edges in a `related:` frontmatter list** of paths relative to the file. Their bodies are fixed instructional text we don't want to clutter; the structural edges (a template ↔ its rubric, a pass → the next pass) live in frontmatter instead.

Because Proselon filenames contain spaces, **wrap body-link paths in angle brackets** — `[Karsk](<../Locations/Karsk.md>)` — so they render on GitHub and in strict CommonMark. (`related:` frontmatter paths are plain quoted strings and need no brackets.)

The visualizer reads **both** — body markdown links and frontmatter `related:` — as edges.

## index.md

`.proselon/workflow/index.md` is the framework bundle's table of contents: the seven steps in order, linked, with tier badges. It complements — does not replace — the Per-Step File Index in `AGENTS.md`.

Story-bible `index.md` files are optional. Don't hand-maintain one just for completeness; the visualizer and Obsidian both walk the tree without it.

## What Proselon deliberately skips

OKF is minimally opinionated, so we adopt only what earns its place:

- **No `log.md`.** Git already is the change history (and underpins the planned authorship-attribution metric). A parallel hand-written log would only drift.
- **No `timestamp` field.** Git tracks modification time; a frontmatter timestamp would churn on every edit.

## Hard rules

- **Frontmatter is additive metadata — never the state authority.** Workflow position is still determined by which **gate files exist** plus the Story State Production table, exactly as before. Do not infer step completion, or anything else stateful, from frontmatter.
- **Never add frontmatter to `Manuscripts/` or `Fragments/`.** Manuscript scenes stay export-safe prose; fragments stay raw.
- **`title` matches the `H1`**, and the `H1` still matches the filename (the existing rule is unchanged).

## Visualizing the graph

`.proselon/scripts/visualize_story_graph.py` walks a bundle, reads frontmatter + links, and writes a single self-contained `Story Graph.html` (nodes colored by `type`, click to open the file). `--bundle story` (default) graphs the author's story bible; `--bundle framework` graphs `.proselon/workflow/`. Obsidian users already have a live graph view from the same cross-links.
