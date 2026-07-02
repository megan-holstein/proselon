#!/usr/bin/env python3
"""Export individual scene files into a single manuscript markdown file.

Usage:
    python .proselon/scripts/export_manuscript_markdown.py "Book 1" "Signal Override"

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
    book_title:   Title for the H1 heading and output filename (e.g. "Signal Override")
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _manuscript import (
    chapter_heading,
    count_words,
    export_output_path,
    find_book_dir,
    find_chapter_dirs,
    find_scene_files,
    read_scene,
)


def export(book_folder, book_title):
    manuscripts_dir = find_book_dir(book_folder)
    chapter_dirs = find_chapter_dirs(manuscripts_dir)

    lines = [f"# {book_title}\n"]
    total_scenes = 0
    total_words = 0

    for chapter_dir in chapter_dirs:
        lines.append(f"\n## {chapter_heading(chapter_dir.name)}\n\n")

        scene_files = find_scene_files(chapter_dir)

        for i, scene_file in enumerate(scene_files):
            content = read_scene(scene_file)
            lines.append(content)
            lines.append("\n")
            total_scenes += 1
            total_words += count_words(content)

            if i < len(scene_files) - 1:
                lines.append("\n---\n\n")

    output = "".join(lines).rstrip("\n") + "\n"
    output_path = export_output_path(manuscripts_dir, book_folder, book_title, ".md")
    output_path.write_text(output, encoding="utf-8")

    print(f"Exported: {output_path.name}")
    print(f"Chapters: {len(chapter_dirs)}, Scenes: {total_scenes}")
    print(f"Words: {total_words:,}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)
    export(sys.argv[1], sys.argv[2])
