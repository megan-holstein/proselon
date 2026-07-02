---
type: Reference
title: AI Prose Tendencies
description: Canonical catalog of AI-drafted prose tells — patterns, word lists, formulaic constructions, and density thresholds — loaded condensed by the drafter and in full by the Line Assessment.
tags: [reference, style, editing]
related: ["4 - Style and Voice/4.1 - Style Guide.md", "6 - Drafting and Editing/6.1 - First Draft.md", "6 - Drafting and Editing/6.4 - Line Assessment.md"]
---
# AI Prose Tendencies

The single source of truth for known AI prose tendencies. Every pattern, word list, and density threshold lives here and only here: the First Draft (6.1) loads the **Core Tells** section so the Writer avoids these while generating; the Line Assessment (6.4) loads the **full catalog** and checks the scene against every section; the Style Guide template (4.1) seeds its Red Flag List's AI-tendency entries from here.

The remedies below are written as the moves to make. A Writer applies them directly; an Assessor working from this catalog recommends them in a findings report — it never edits the manuscript.

## Core Tells (Drafting Checklist)

What a drafter must avoid while generating. Each item is expanded — with full lists, diagnostics, and remedies — in the catalog below.

### Density Thresholds

These ceilings are **defaults calibrated to contemporary commercial fiction, and the project Style Guide may override any of them** where the voice demands it — a deliberately em-dash-heavy narrator, a simile-rich figurative voice. Record every override in the Style Guide (with its rationale, like any subversion); Writers and Assessors then judge against the overridden value, not the table.

| Signal | Ceiling | Clustering |
|--------|---------|------------|
| Em dashes | 1 per 6–7 paragraphs, or 1 per 500 words — whichever is stricter for the scene | Two in one paragraph, or em dashes in three consecutive paragraphs, is overuse even under the per-scene total |
| Prose colons | 1–2 per chapter, or 1 per ~3,000 words; a scene should rarely contain more than one | — |
| Semicolons | 0–1 per chapter — effectively avoid in narration | — |
| Similes | 2–3 per scene, each earning its place | — |
| "As if" constructions | 1 per scene; must deliver information, not decoration | — |
| Rule-of-three constructions | 1 per scene | — |

### Checklist

- **Punctuation defaults** — default to commas and periods. Reach for an em dash only when no other punctuation does the same work: hard interruption, rhythmic kick, deliberate emphasis. Never swap em dashes for colons or semicolons — that trades one tell for another.
- **Fragment runs** — join parallel fragments with commas by default; periods between them are for deliberate emphasis only.
- **Formulaic constructions** — do not build sentences on the formulas cataloged below (escalating negation, corrective contrast, "The kind of [noun] that…", narrated beats, and kin).
- **Over-frequent words** — watch for clustering of the AI-favored verbs, adjectives, and abstract metaphor nouns listed below; prefer the specific or unexpected word.
- **Red-flag phrases** — never produce any phrase on the Red-Flag Phrases list below.
- **Token defaults** — do not default numbers, weekdays, or food and drink; specifics below.
- **Repetition** — vary paragraph openings, sentence structures, transitions, and physical-emotional beats across the scene.
- **Sense-cycling** — do not cycle through senses in order; pick the one or two that matter and skip the rest.

## Full Catalog

### Repetition

- **Sentence-structure repetition** — multiple paragraphs opening the same way, or overuse of a syntactic pattern (e.g., participial-phrase openers, "Subject, [gerund], [main clause]"). Scan paragraph openings across the whole scene; they should vary.
- **Word repetition** — same adjective, verb, adverb, or noun appearing more often than the prose warrants. If a notable word appears three or more times in the scene, at least two of those should change.
- **Emotional-beat repetition** — same physical-emotional response used multiple times in the scene (jaw tightening, breath catching, chest tightening, stomach dropping). If any of these appears more than once per scene, one instance needs to change.
- **Transition repetition** — same method of moving between beats or paragraphs. If three consecutive transitions are "She turned," "He looked," "She glanced," break the pattern.

### Over-Frequent Words

These appear with detectable frequency in AI-drafted prose. Not banned, but clustering (3+ in a scene) signals the prose needs roughening. Clustering means most instances should be replaced with more specific or unexpected alternatives.

**These lists decay.** The named words and phrases in this catalog are examples of a phenomenon, not a permanent registry: tics differ between models and change as models change, and prose steered hard off a named list converges on the next-most-probable alternatives — which become the new tics the list doesn't name. The ground truth is measured repetition in *this project's* prose: `prose_stats.py` frequency output and the Style Guide's Red Flag List (the project tic sheet). Trust those over this list when they disagree, and refresh these lists when the drafting models change.

- **Verbs**: measured, pulsed, shifted, flickered, tilted, hummed, dragged, settled, landed, clenched, delve, unlock
- **Adjectives/adverbs**: quietly, carefully, gently, familiar, dangerous, palpable, visceral, almost
- **Abstract nouns used as metaphor vehicles**: architecture, mechanism, cadence, texture, weight (of [abstract noun]), rhythm, landscape, tapestry
- **Catch-all hedges**: something, seemed

### Fragment Runs

A run of short, parallel sentences that share a structure — "Green for all good. Amber for warning. Red for emergency." — is a tell. The remedy is a single compound sentence with commas. Periods between parallel fragments should be the exception, used only for deliberate emphasis or rhythm, not the default. If the fragments are not parallel, or the staccato beat is clearly doing intentional work in the passage, leave them.

When combining fragments produces a perfectly symmetric tricolon ("Green for all good, amber for warning, red for emergency" — which the Rule of Three check flags), vary the final element's length or structure: "Green for all good, amber for warning, red when something is about to fail."

### Simile and Metaphor

For each simile, test:

1. Does it deliver information the literal prose cannot?
2. Is it specific to this moment, character, world?
3. Does it extend understanding, or merely decorate?

Similes that fail all three go. Per-scene caps for similes and "as if" constructions: see the Density Thresholds table.

Watch specifically for:

- **"As if" constructions** that decorate rather than inform ("He looked at her, as if she were the only thing to look at" — cut.)
- **Similes that restate what's literally happening** ("like a man standing by the road" when he is standing by the road)
- **Character-type similes**: "Like a man/woman/creature who..." or "With the [quality/precision/ease] of someone who [verb]"

### Rule of Three

Tripled constructions (three examples, three escalating beats, three restatements). Past the per-scene cap (Density Thresholds table) it's a tic — at least one must break. Perfectly parallel tricolons with identical rhythm and structure are an especially strong signal; break the symmetry.

### Formulaic Constructions

These sentence formulas appear with detectable frequency in AI-drafted prose. Every instance needs a rewrite:

- "Not [X]. Not [Y]. [Z]." — escalating-negation countdown
- "Not [X], just/but [Y]" — corrective-contrast formula
- "[Noun] — not [expected], but [unexpected]." — corrective pivot
- "It wasn't [X]. It was something [worse/deeper/quieter]."
- "Something in [noun] shifted/softened/changed"
- "The kind of [noun] that [poetic observation]"
- "And somehow, that was [enough/worse/exactly right]."
- "[Character] noticed. [Other] noticed [them] noticing." — recursive perception
- "Just… [fragment]." — trailing fragment for understated presence
- "A pause." / "A beat." — narrated stage directions
- Dialogue repetition-as-emphasis: "[Word]. Absolutely [word]."

### Sense-Cycling

Descriptive passages that cycle through senses in order (sight, then sound, then smell, then touch). Real perception is selective and unbalanced. Break the order — pick the one or two senses that matter and skip the rest.

### Token Defaults

Specific tokens appear with detectable frequency in AI-drafted prose. Replace defaults with varied alternatives:

- **Numbers**: 17, 37, 47 over-appear, especially as minutes in timestamps (3:47, 8:47). Use irregular numbers instead (14, 23, 52, 08).
- **Days of the week**: Tuesday and Thursday are defaults. Vary deliberately.
- **Food and drink**: tea, coffee, water default as comfort/domesticity crutches. Verify any food or drink in the scene serves the scene; otherwise replace or remove.

### Em-Dash Density

Em-dash overuse is one of the strongest tells of AI-drafted prose. Each em dash loses impact when surrounded by others; a manuscript dotted with them flattens its own rhythm and starts to read as machine cadence.

**Threshold and clustering** — see the Density Thresholds table.

**Diagnostic** — count em dashes in the scene, count paragraphs (or words), and check the ratio and the clustering against the table.

**Remedy** — for em dashes over quota, identify the ones doing the least work and convert them. Standard replacements, in order of preference:

- Comma — for parenthetical aside or soft pause
- Period — for hard break between thoughts
- Rewrite — restructure the sentence so the em dash isn't needed (often the cleanest fix; a sentence that needed an em dash often needed a different structure)
- Parentheses — for a true aside the reader could skip (use sparingly; parentheses have their own intrusion quality)

Do NOT default to colons or semicolons as cheap em-dash substitutes. Colons have their own density cap and read as formal/expository when used in narrative fiction. Semicolons are essentially absent from contemporary fiction and should never appear as em-dash substitutes. Mechanically converting em dashes to colons just trades one AI tell for another.

Preserve em dashes that do work no other punctuation could: hard interruption (a mid-sentence cutoff), rhythmic kick (the unexpected hit that breaks expectation), deliberate emphasis (setting off a punchline or a turn). If no one can articulate what specific work an em dash is doing in its sentence, it goes.

After rewrites are applied, the count runs again; the scene clears only when under threshold. In an assessment, report the count and which instances to change — the Writer iterates until under threshold.

### Colon and Semicolon Density

Colons and semicolons are sparingly used in contemporary fiction. When overused — especially as substitutes for em dashes or commas — they push the prose toward an expository, formal, or academic register that breaks most fiction voices. Heavy colon use is its own AI tell, often arising when an editing pass converts em dashes mechanically.

**Thresholds** — see the Density Thresholds table. Colons inside timestamps (3:47), ratios, dialogue list intros, or other non-narrative contexts don't count toward the prose budget, but should still be examined for whether they're earning their place.

**Diagnostic** — count colons and semicolons per scene and per chapter. Any scene or chapter over its colon budget, and every semicolon, is a flag.

**Remedy** — for over-quota colons and semicolons:

- Period — default replacement (hard break between thoughts)
- Comma — soft connector if the two halves are tightly linked
- Rewrite — when neither feels right, restructure the sentence so the colon or semicolon isn't needed

Preserve colons only for genuine setup-payoff constructions where no other punctuation does the work, and only within the per-chapter budget. Preserve semicolons only in dialogue from a character whose voice would deliberately reach for one (an academic, a pedant, a formal writer); in narration, replace.

### Red-Flag Phrases

Every occurrence of these patterns is an automatic flag for rewrite — no judgment call needed. `.proselon/scripts/prose_stats.py` detects the mechanically matchable patterns on this list and reports each hit; verify its hits in context, then scan for the rest yourself — the paraphrasable patterns no regex can catch:

- "her eyes were warm"
- "he felt [emotion]" — red flag as primary rendering. Permitted only in **negation** ("Not relief — the situation was too sharp for relief") or **retrospective labeling** ("Later she'd call it grief. At the time it was just the pressure behind her eyes"). The physical rendering must come first or replace the label entirely.
- "he realized" — red flag when it filters another event ("he realized the door was locked" → "the door was locked"). Permitted when the realization IS the action ("She realized she wasn't going to leave").
- "he noticed" — red flag when it filters another event. Permitted when the act of noticing IS what matters ("She noticed it only because she was looking for it — the faintest hum beneath the reactor noise").
- "something that looked very much like [emotion]"
- "[emotion] etched across/into [body part]"
- "[emotion] flooded/surged/washed through [pronoun]"
- "unguarded in a way she rarely..."
- "the weight of [abstract noun]"
- "a mixture of [emotion] and [emotion]"
- "he couldn't help but [verb]" / "she couldn't help but [verb]"
- "his heart ached"
- "he let out a breath he didn't know he'd been holding"
- "that was worse"
- "that was enough" / "it was a start, anyway" / "it would have to do" / "that was something, at least" / "one [noun] at a time"
- "that's very [character name]" — character-as-adjective
- any adverb after "said" or "says"
