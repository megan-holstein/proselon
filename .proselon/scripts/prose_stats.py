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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)
    main(sys.argv[1:])
