#!/usr/bin/env python3
"""Print word counts for each chapter in a manuscript, plus the total.

Usage:
    python .proselon/scripts/word_count.py "Book 1"

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _manuscript import (
    chapter_heading,
    count_words,
    find_book_dir,
    find_chapter_dirs,
    find_scene_files,
    read_scene,
)


def word_count(book_folder):
    manuscripts_dir = find_book_dir(book_folder)
    chapter_dirs = find_chapter_dirs(manuscripts_dir)

    total_words = 0
    chapter_counts = []

    for chapter_dir in chapter_dirs:
        chapter_label = chapter_heading(chapter_dir.name)

        scene_files = find_scene_files(chapter_dir)

        chapter_words = 0
        for scene_file in scene_files:
            chapter_words += count_words(read_scene(scene_file))

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
