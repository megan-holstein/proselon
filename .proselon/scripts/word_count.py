#!/usr/bin/env python3
"""Print word counts for each chapter in a manuscript, plus the total.

Usage:
    python .proselon/scripts/word_count.py "Book 1"

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
"""

import re
import sys
from pathlib import Path


def natural_sort_key(path):
    """Sort by embedded numbers so Chapter 2 comes before Chapter 10."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def strip_front_matter(text):
    """Remove YAML front matter if present."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:].lstrip("\n")
    return text


def count_words(text):
    """Count words in a string."""
    return len(text.split())


def word_count(book_folder):
    project_root = Path(__file__).resolve().parent.parent.parent
    manuscripts_dir = project_root / "Manuscripts" / book_folder

    if not manuscripts_dir.is_dir():
        print(f"Error: {manuscripts_dir} not found.", file=sys.stderr)
        sys.exit(1)

    chapter_dirs = sorted(
        [d for d in manuscripts_dir.iterdir() if d.is_dir() and "Chapter" in d.name],
        key=natural_sort_key,
    )

    if not chapter_dirs:
        print(f"Error: No chapter folders found in {manuscripts_dir}.", file=sys.stderr)
        sys.exit(1)

    total_words = 0
    chapter_counts = []

    for chapter_dir in chapter_dirs:
        chapter_num = re.search(r"\d+", chapter_dir.name)
        chapter_label = f"Chapter {chapter_num.group()}" if chapter_num else chapter_dir.name

        scene_files = sorted(
            [f for f in chapter_dir.iterdir() if f.is_file() and f.suffix == ".md" and f.name.startswith("S")],
            key=natural_sort_key,
        )

        chapter_words = 0
        for scene_file in scene_files:
            content = strip_front_matter(scene_file.read_text(encoding="utf-8")).strip()
            chapter_words += count_words(content)

        chapter_counts.append((chapter_label, chapter_words, len(scene_files)))
        total_words += chapter_words

    # Print results
    label_width = max(len(c[0]) for c in chapter_counts)

    for label, words, scenes in chapter_counts:
        scene_note = f"  ({scenes} scene{'s' if scenes != 1 else ''})"
        print(f"  {label:<{label_width}}   {words:>6,} words{scene_note}")

    print(f"  {'':─<{label_width + 30}}")
    print(f"  {'Total':<{label_width}}   {total_words:>6,} words  ({len(chapter_counts)} chapters)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(1)
    word_count(sys.argv[1])
