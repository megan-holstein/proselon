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
    python3 -m pip install --user EbookLib
"""

import re
import sys
import uuid
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _manuscript import (
    chapter_heading,
    count_words,
    export_output_path,
    find_book_dir,
    find_chapter_dirs,
    find_scene_files,
    parse_inline,
    read_scene,
)

try:
    from ebooklib import epub
except ImportError:
    print(
        "Error: the EbookLib library is not installed.\n"
        "Install it with:  python3 -m pip install --user EbookLib\n"
        "If installing is a hassle, ask the agent for an HTML export instead —\n"
        "it opens in any browser and can be sent to a Kindle as-is.",
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


def render_inline(text):
    """Convert markdown ***bold-italic***, **bold**, *italic* to HTML.

    Emphasis parsing is shared with the docx exporter via
    _manuscript.parse_inline — fix emphasis bugs there, once, for both.
    """
    parts = []
    for run_text, bold, italic in parse_inline(text):
        chunk = escape(run_text)
        if italic:
            chunk = f"<em>{chunk}</em>"
        if bold:
            chunk = f"<strong>{chunk}</strong>"
        parts.append(chunk)
    return "".join(parts)


def render_scene_html(text):
    """Convert a scene's markdown body to HTML paragraphs."""
    parts = []
    first_para = True
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line == "---":
            parts.append('<p class="scene-break">• • •</p>')
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


def chapter_slug(dir_name, index, used_slugs):
    """A unique, filesystem-safe slug for a chapter's .xhtml file.

    Falls back to "chapter-<index>" when the name has no ASCII alphanumerics,
    and de-duplicates so two chapters can never collide on the same file.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", dir_name.lower()).strip("-")
    if not slug:
        slug = f"chapter-{index}"
    base, n = slug, 2
    while slug in used_slugs:
        slug = f"{base}-{n}"
        n += 1
    used_slugs.add(slug)
    return slug


def export(book_folder, book_title, author=None):
    manuscripts_dir = find_book_dir(book_folder)
    chapter_dirs = find_chapter_dirs(manuscripts_dir)

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
    total_words = 0
    used_slugs = set()

    for index, chapter_dir in enumerate(chapter_dirs, start=1):
        heading = chapter_heading(chapter_dir.name)

        scene_files = find_scene_files(chapter_dir)

        body_parts = [f"<h1>{escape(heading)}</h1>"]
        for i, scene_file in enumerate(scene_files):
            content = read_scene(scene_file)
            body_parts.append(render_scene_html(content))
            total_scenes += 1
            total_words += count_words(content)
            if i < len(scene_files) - 1:
                body_parts.append(
                    '<p class="scene-break">• • •</p>'
                )

        slug = chapter_slug(chapter_dir.name, index, used_slugs)
        chapter = epub.EpubHtml(
            title=heading,
            file_name=f"{slug}.xhtml",
            lang=LANGUAGE,
        )
        chapter.content = (
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            f"<head><title>{escape(heading)}</title>"
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

    output_path = export_output_path(manuscripts_dir, book_folder, book_title, ".epub")
    epub.write_epub(str(output_path), book)

    print(f"Exported: {output_path.name}")
    print(f"Chapters: {len(chapter_dirs)}, Scenes: {total_scenes}")
    print(f"Words: {total_words:,}")
    size_kb = output_path.stat().st_size / 1024
    print(f"Size: {size_kb:.0f} KB")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print(__doc__.strip())
        sys.exit(1)
    export(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
