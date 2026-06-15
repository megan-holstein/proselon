#!/usr/bin/env python3
"""Export manuscript scene files into an EPUB for personal Kindle reading.

Usage:
    python .proselon/scripts/export_manuscript_epub.py "Book 1" "Favorite Person" ["Author Name"]

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
    book_title:   Title used for metadata and output filename (e.g. "Favorite Person")
    author:       Optional author or pen name for the book metadata

This produces a reading copy. To read it on a Kindle, attach the .epub to an
email and send it to your Send-to-Kindle address, or upload it at
send-to-kindle.amazon.com.

Dependencies:
    pip3 install EbookLib
"""

import re
import sys
import uuid
from html import escape
from pathlib import Path

try:
    from ebooklib import epub
except ImportError:
    print(
        "Error: the EbookLib library is not installed.\n"
        "Install it with:  pip3 install EbookLib",
        file=sys.stderr,
    )
    sys.exit(1)


LANGUAGE = "en"

STYLESHEET = """
body { font-family: Georgia, serif; line-height: 1.5; margin: 0 1em; }
h1 { text-align: center; margin: 3em 0 1.5em 0; font-weight: bold; }
h2 { text-align: center; margin: 1.5em 0 1em 0; font-weight: normal; font-style: italic; }
p { text-indent: 1.5em; margin: 0; }
p.first, h1 + p, h2 + p, .scene-break + p { text-indent: 0; }
p.scene-break { text-align: center; text-indent: 0; margin: 1.5em 0; color: #666; }
"""


def natural_sort_key(path):
    """Sort by embedded numbers so Chapter 2 comes before Chapter 10."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def render_inline(text):
    """Convert markdown ***bold-italic***, **bold**, *italic* to HTML."""
    text = escape(text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def render_scene_html(text):
    """Convert a scene's markdown body to HTML paragraphs."""
    parts = []
    first_para = True
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line == "---":
            parts.append('<p class="scene-break">• • •</p>')
            first_para = True
            continue
        if line.startswith("## "):
            parts.append(f"<h2>{render_inline(line[3:])}</h2>")
            first_para = True
            continue
        if line.startswith("# "):
            parts.append(f"<h1>{render_inline(line[2:])}</h1>")
            first_para = True
            continue
        cls = ' class="first"' if first_para else ""
        parts.append(f"<p{cls}>{render_inline(line)}</p>")
        first_para = False
    return "\n".join(parts)


def export(book_folder, book_title, author=None):
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

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(book_title)
    book.set_language(LANGUAGE)
    if author:
        book.add_author(author)

    css = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=STYLESHEET,
    )
    book.add_item(css)

    chapters = []
    total_scenes = 0

    for chapter_dir in chapter_dirs:
        chapter_num = re.search(r"\d+", chapter_dir.name)
        chapter_heading = (
            f"Chapter {chapter_num.group()}" if chapter_num else chapter_dir.name
        )

        scene_files = sorted(
            [f for f in chapter_dir.iterdir()
             if f.is_file() and f.suffix == ".md" and f.name.startswith("S")],
            key=natural_sort_key,
        )

        body_parts = [f"<h1>{escape(chapter_heading)}</h1>"]
        for i, scene_file in enumerate(scene_files):
            content = scene_file.read_text(encoding="utf-8").strip()
            body_parts.append(render_scene_html(content))
            total_scenes += 1
            if i < len(scene_files) - 1:
                body_parts.append(
                    '<p class="scene-break">• • •</p>'
                )

        slug = re.sub(r"[^a-z0-9]+", "-", chapter_dir.name.lower()).strip("-")
        chapter = epub.EpubHtml(
            title=chapter_heading,
            file_name=f"{slug}.xhtml",
            lang=LANGUAGE,
        )
        chapter.content = (
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            f"<head><title>{escape(chapter_heading)}</title>"
            '<link rel="stylesheet" type="text/css" href="style/main.css"/>'
            "</head><body>" + "\n".join(body_parts) + "</body></html>"
        )
        chapter.add_item(css)
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + chapters

    output_path = manuscripts_dir.parent / f"{book_folder} - {book_title}.epub"
    epub.write_epub(str(output_path), book)

    print(f"Exported: {output_path.name}")
    print(f"Chapters: {len(chapter_dirs)}, Scenes: {total_scenes}")
    size_kb = output_path.stat().st_size / 1024
    print(f"Size: {size_kb:.0f} KB")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print(__doc__.strip())
        sys.exit(1)
    export(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
