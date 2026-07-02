#!/usr/bin/env python3
"""Report prose statistics for one or more manuscript markdown files.

Usage:
    python .proselon/scripts/prose_stats.py <file.md> [<more files...>]

Pass one scene for a scene-level check, or every scene in a book (e.g. with a
shell glob) for a whole-book tic scan — all files are combined and reported as
one body of prose. Front matter is stripped; headings and scene-break lines
don't count as paragraphs.

Reports:
  - word and paragraph counts
  - em-dash count, density (per paragraph / per 1,000 words), and clustering
  - colon and semicolon counts
  - simile proxies ("as if", "like a")
  - most-repeated content words, and bigrams/trigrams appearing 3+ times
  - paragraph-length distribution and one-sentence-paragraph count
  - sentence-length distribution and variance (low variance reads metronomic)
  - repeated paragraph openings and participial (-ing) openers
  - filter and hedge words (felt, noticed, seemed, began to, ...)
  - hits on the mechanically detectable Red-Flag Phrases from the
    AI Prose Tendencies catalog (verify each hit in context)

These back the Line Assessment (6.4) density checks. Stdlib only — no installs.
"""

import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _manuscript import count_words, strip_front_matter

EM_DASH = "—"

# Small stopword list: common function words only, so story words rise to the top.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "nor", "so", "yet",
    "of", "to", "in", "on", "at", "by", "for", "with", "from", "into", "onto",
    "up", "down", "out", "off", "over", "under", "again", "then", "than",
    "as", "if", "when", "while", "because", "though", "through", "about",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did", "done",
    "will", "would", "can", "could", "shall", "should", "may", "might", "must",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs",
    "this", "that", "these", "those", "there", "here",
    "what", "which", "who", "whom", "whose", "how", "why", "where",
    "not", "no", "n't", "s", "t", "d", "ll", "m", "re", "ve",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "too", "very", "just", "now",
}

WORD_RE = re.compile(r"[a-z']+")
SENTENCE_END_RE = re.compile(r"[.!?…]+[\"'”’)\]]*(?=\s|$)")
SCENE_BREAK_RE = re.compile(r"[-*_](?:\s*[-*_]){2,}$")

# Words ending in -ing that aren't participles when opening a paragraph.
ING_FALSE_POSITIVES = {
    "nothing", "something", "anything", "everything",
    "morning", "evening", "during", "spring", "king", "ring", "thing", "wing",
}

# Filter and hedge words: perception verbs that stand between the reader and
# the event, and hedges that soften prose into mush. Counts only — the
# assessor judges which instances are the dramatic action vs. a filter.
FILTER_PATTERNS = [
    ('"felt"', r"\bfelt\b"),
    ('"noticed"', r"\bnoticed\b"),
    ('"realized"', r"\brealized\b"),
    ('"saw"', r"\bsaw\b"),
    ('"heard"', r"\bheard\b"),
    ('"watched"', r"\bwatched\b"),
    ('"knew"', r"\bknew\b"),
    ('"seemed"', r"\bseemed\b"),
    ('"began to" / "started to"', r"\b(?:began|started) to\b"),
    ('"could see/hear/feel"', r"\bcould (?:see|hear|feel)\b"),
]

# The mechanically matchable patterns from the AI Prose Tendencies catalog's
# Red-Flag Phrases list. Every hit is reported; the assessor verifies each in
# context (e.g. "the weight of the crate" is literal, not a flag).
RED_FLAG_PATTERNS = [
    ('"couldn\'t help but"', r"couldn['’]t help but"),
    ('"let out a breath"', r"\blet out a breath\b"),
    ('"a mixture of"', r"\ba mixture of\b"),
    ('adverb after "said"/"says"', r"\bsa(?:id|ys) \w+ly\b"),
    ('"the weight of"', r"\bthe weight of\b"),
    ('"eyes were warm"', r"\beyes were warm\b"),
    ('"looked very much like"', r"\blooked very much like\b"),
    ('"etched across/into/on"', r"\betched (?:across|into|on)\b"),
    ('"flooded/surged/washed through"', r"\b(?:flooded|surged|washed) through\b"),
    ('"something in ... shifted/softened/changed"',
     r"\bsomething in \w+(?: \w+)? (?:shifted|softened|changed)\b"),
    ('"that was worse"', r"\bthat was worse\b"),
    ('"that was enough" and kin',
     r"\bthat was enough\b|\bit was a start\b|\bit would have to do\b"
     r"|\bthat was something, at least\b"),
    ('"one [noun] at a time"', r"\bone \w+ at a time\b"),
    ('"unguarded in a way"', r"\bunguarded in a way\b"),
    ('"heart ached"', r"\bheart ached\b"),
    ('"A pause." / "A beat."', r"(?m)(?:^|[.!?\"”'] )A (?:pause|beat)\."),
]


def paragraphs_of(text):
    """Prose paragraphs: one per non-blank line, minus headings and breaks."""
    paras = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):            # markdown heading, not prose
            continue
        if SCENE_BREAK_RE.fullmatch(line):  # ---, ***, scene-break lines
            continue
        paras.append(line)
    return paras


def tokens_of(text):
    """Lowercased word tokens, apostrophes kept inside words."""
    lowered = text.lower().replace("’", "'")
    return [w.strip("'") for w in WORD_RE.findall(lowered) if w.strip("'")]


def sentence_count(paragraph):
    """Approximate sentence count from terminal punctuation."""
    return max(1, len(SENTENCE_END_RE.findall(paragraph)))


def sentences_of(paragraph):
    """Split a paragraph into sentences on terminal punctuation."""
    sentences = []
    start = 0
    for m in SENTENCE_END_RE.finditer(paragraph):
        chunk = paragraph[start:m.end()].strip()
        if chunk:
            sentences.append(chunk)
        start = m.end()
    tail = paragraph[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences


def ngram_counts(paragraphs, n):
    counts = Counter()
    for para in paragraphs:
        toks = tokens_of(para)
        for i in range(len(toks) - n + 1):
            gram = toks[i:i + n]
            if all(w in STOPWORDS for w in gram):
                continue  # "of the", "and then a" — noise, not a tic
            counts[" ".join(gram)] += 1
    return counts


def stat_line(label, value, note=""):
    if isinstance(value, float):
        value = f"{value:,.2f}"
    elif isinstance(value, int):
        value = f"{value:,}"
    suffix = f"  {note}" if note else ""
    return f"  {label:<34}{value:>10}{suffix}"


def main(paths):
    bodies = []
    for p in paths:
        path = Path(p)
        if not path.is_file():
            print(f"Error: {path} not found (or is not a file).", file=sys.stderr)
            sys.exit(1)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Error: {path} is not a UTF-8 text file.", file=sys.stderr)
            sys.exit(1)
        bodies.append(strip_front_matter(text).strip())

    combined = "\n\n".join(bodies)
    paragraphs = paragraphs_of(combined)
    if not paragraphs:
        print("No prose found in the given file(s) — nothing to measure.", file=sys.stderr)
        sys.exit(1)

    prose = "\n".join(paragraphs)
    total_words = count_words(prose)
    n_paras = len(paragraphs)

    # --- punctuation ------------------------------------------------------
    em_total = prose.count(EM_DASH)
    em_cluster_paras = sum(1 for p in paragraphs if p.count(EM_DASH) >= 2)
    colons = prose.count(":")
    semicolons = prose.count(";")

    # --- simile proxies -----------------------------------------------------
    as_if = len(re.findall(r"\bas if\b", prose, re.IGNORECASE))
    like_a = len(re.findall(r"\blike an?\b", prose, re.IGNORECASE))

    # --- repeated words and phrases ----------------------------------------
    words = tokens_of(prose)
    content_counts = Counter(w for w in words if w not in STOPWORDS and len(w) > 1)
    top_words = [(w, c) for w, c in content_counts.most_common(15) if c >= 2]

    bigrams = [(g, c) for g, c in ngram_counts(paragraphs, 2).most_common() if c >= 3]
    trigrams = [(g, c) for g, c in ngram_counts(paragraphs, 3).most_common() if c >= 3]

    # --- paragraph lengths --------------------------------------------------
    para_lengths = [count_words(p) for p in paragraphs]
    one_sentence = sum(1 for p in paragraphs if sentence_count(p) == 1)

    # --- sentence lengths ---------------------------------------------------
    sentence_lengths = [count_words(s) for p in paragraphs for s in sentences_of(p)]

    # --- paragraph openings -------------------------------------------------
    opening_counts = Counter()
    ing_openers = 0
    for p in paragraphs:
        toks = tokens_of(p)
        if not toks:
            continue
        opening_counts[" ".join(toks[:2])] += 1
        if toks[0].endswith("ing") and toks[0] not in ING_FALSE_POSITIVES:
            ing_openers += 1
    repeated_openings = [(o, c) for o, c in opening_counts.most_common(10) if c >= 3]

    # --- filter words and red-flag phrases -----------------------------------
    filter_hits = [(label, len(re.findall(pat, prose, re.IGNORECASE)))
                   for label, pat in FILTER_PATTERNS]
    filter_hits = [(label, n) for label, n in filter_hits if n]
    red_flag_hits = [(label, len(re.findall(pat, prose, re.IGNORECASE)))
                     for label, pat in RED_FLAG_PATTERNS]
    red_flag_hits = [(label, n) for label, n in red_flag_hits if n]

    # --- report -------------------------------------------------------------
    file_note = f"{len(paths)} file{'s' if len(paths) != 1 else ''}"
    print(f"Prose statistics ({file_note})")
    print()
    print("Size")
    print(stat_line("Words", total_words))
    print(stat_line("Paragraphs", n_paras))
    print()
    print("Em dashes (—)")
    print(stat_line("Count", em_total))
    print(stat_line("Per paragraph", em_total / n_paras))
    print(stat_line("Per 1,000 words", em_total * 1000 / total_words if total_words else 0.0))
    print(stat_line("Paragraphs with 2+ (clusters)", em_cluster_paras))
    print()
    print("Other punctuation")
    print(stat_line("Colons", colons))
    print(stat_line("Semicolons", semicolons))
    print()
    print("Simile proxies")
    print(stat_line('"as if"', as_if))
    print(stat_line('"like a" / "like an"', like_a))
    print()
    print("Most-repeated content words")
    if top_words:
        for w, c in top_words:
            print(stat_line(w, c))
    else:
        print("  (none repeated)")
    print()
    print("Repeated phrases (3+ uses)")
    shown = False
    for label, grams in (("bigrams", bigrams), ("trigrams", trigrams)):
        for g, c in grams[:20]:
            print(stat_line(f'"{g}"', c))
            shown = True
        if len(grams) > 20:
            print(f"  ... and {len(grams) - 20} more {label}")
    if not shown:
        print("  (none)")
    print()
    print("Paragraph lengths (words)")
    print(stat_line("Shortest", min(para_lengths)))
    print(stat_line("Median", float(statistics.median(para_lengths))))
    print(stat_line("Longest", max(para_lengths)))
    print(stat_line("One-sentence paragraphs", one_sentence,
                    f"({one_sentence * 100 // n_paras}% of paragraphs)"))
    print()
    print("Sentence lengths (words)")
    print(stat_line("Sentences", len(sentence_lengths)))
    print(stat_line("Shortest", min(sentence_lengths)))
    print(stat_line("Median", float(statistics.median(sentence_lengths))))
    print(stat_line("Longest", max(sentence_lengths)))
    mean_len = statistics.fmean(sentence_lengths)
    print(stat_line("Mean", mean_len))
    if len(sentence_lengths) >= 2:
        stdev = statistics.stdev(sentence_lengths)
        cv = stdev / mean_len if mean_len else 0.0
        print(stat_line("Stdev", stdev,
                        f"(stdev/mean {cv:.2f} — low variance reads metronomic)"))
    print()
    print("Paragraph openings")
    print(stat_line("Participial (-ing) openers", ing_openers))
    if repeated_openings:
        for o, c in repeated_openings:
            print(stat_line(f'"{o} ..."', c))
    else:
        print("  (no opening pair used 3+ times)")
    print()
    print("Filter and hedge words (judge each in context)")
    if filter_hits:
        for label, n in filter_hits:
            print(stat_line(label, n))
    else:
        print("  (none)")
    print()
    print("Red-flag phrase hits (every hit needs a look; see the catalog)")
    if red_flag_hits:
        for label, n in red_flag_hits:
            print(stat_line(label, n))
    else:
        print("  (none)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)
    main(sys.argv[1:])
