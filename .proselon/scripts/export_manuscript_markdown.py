#!/usr/bin/env python3
"""Export individual scene files into a single manuscript markdown file.

Usage:
    python .proselon/scripts/export_manuscript_markdown.py "Book 1" "Signal Override"

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
    book_title:   Title for the H1 heading and output filename (e.g. "Signal Override")
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


def export(book_folder, book_title):
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

    lines = [f"# {book_title}\n"]
    total_scenes = 0

    for chapter_dir in chapter_dirs:
        chapter_num = re.search(r"\d+", chapter_dir.name)
        chapter_heading = f"Chapter {chapter_num.group()}" if chapter_num else chapter_dir.name
        lines.append(f"\n## {chapter_heading}\n\n")

        scene_files = sorted(
            [f for f in chapter_dir.iterdir() if f.is_file() and f.suffix == ".md" and f.name.startswith("S")],
            key=natural_sort_key,
        )

        for i, scene_file in enumerate(scene_files):
            content = scene_file.read_text(encoding="utf-8").strip()
            lines.append(content)
            lines.append("\n")
            total_scenes += 1

            if i < len(scene_files) - 1:
                lines.append("\n---\n\n")

    output = "".join(lines).rstrip("\n") + "\n"
    output_path = manuscripts_dir.parent / f"{book_folder} - {book_title}.md"
    output_path.write_text(output, encoding="utf-8")

    word_count = len(output.split())
    print(f"Exported: {output_path.name}")
    print(f"Chapters: {len(chapter_dirs)}, Scenes: {total_scenes}")
    print(f"Words: {word_count:,}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)
    export(sys.argv[1], sys.argv[2])
