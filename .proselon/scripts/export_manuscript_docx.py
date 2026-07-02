#!/usr/bin/env python3
"""Export manuscript scene files into a Word (.docx) document.

Usage:
    python .proselon/scripts/export_manuscript_docx.py "Book 1" "Favorite Person" ["Author Name"]

Arguments:
    book_folder:  Name of the folder under Manuscripts/ (e.g. "Book 1")
    book_title:   Title used for metadata and output filename (e.g. "Favorite Person")
    author:       Optional author or pen name for the title page and metadata

Dependencies:
    python3 -m pip install --user python-docx
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
    parse_inline,
    read_scene,
)

try:
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print(
        "Error: the python-docx library is not installed.\n"
        "Install it with:  python3 -m pip install --user python-docx\n"
        "If installing is a hassle, ask the agent for an HTML export instead —\n"
        "it opens directly in Word or Pages and saves normally.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FONT_NAME = "Georgia"
BODY_FONT_SIZE = Pt(11)
CHAPTER_HEADING_SIZE = Pt(16)   # level-1 headings (chapter titles)
SUB_HEADING_SIZE = Pt(13)       # level-2 headings inside scenes
HEADING_COLOR = RGBColor(0, 0, 0)  # override Word's default blue heading style


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def style_heading(paragraph, size):
    """Give a heading the manuscript font, size, and plain black color."""
    for run in paragraph.runs:
        run.font.name = FONT_NAME
        run.font.size = size
        run.font.color.rgb = HEADING_COLOR


def add_formatted_text(paragraph, text):
    """Parse markdown inline formatting (**bold**, *italic*) into Word runs.

    Emphasis parsing is shared with the EPUB exporter via
    _manuscript.parse_inline — fix emphasis bugs there, once, for both.
    """
    for run_text, bold, italic in parse_inline(text):
        run = paragraph.add_run(run_text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        run.font.name = FONT_NAME
        run.font.size = BODY_FONT_SIZE


def add_scene_break(doc):
    """Insert a centred bullet scene-break separator."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("•  •  •")
    run.font.name = FONT_NAME
    run.font.size = BODY_FONT_SIZE
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def add_markdown_block(doc, md_text):
    """Add a block of markdown text, handling headings, lists, and paragraphs."""
    for line in md_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("## "):
            p = doc.add_heading(stripped[3:], level=2)
            style_heading(p, SUB_HEADING_SIZE)
        elif stripped.startswith("# "):
            p = doc.add_heading(stripped[2:], level=1)
            style_heading(p, CHAPTER_HEADING_SIZE)
        elif stripped.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_formatted_text(p, stripped[2:])
        elif stripped == "---":
            add_scene_break(doc)
        else:
            p = doc.add_paragraph()
            add_formatted_text(p, stripped)


# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------

def export(book_folder, book_title, author=None):
    manuscripts_dir = find_book_dir(book_folder)
    chapter_dirs = find_chapter_dirs(manuscripts_dir)

    # --- Create document --------------------------------------------------
    doc = Document()

    # Document metadata
    doc.core_properties.title = book_title
    if author:
        doc.core_properties.author = author

    # Default style
    style = doc.styles["Normal"]
    style.font.name = FONT_NAME
    style.font.size = BODY_FONT_SIZE
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.space_before = Pt(0)

    # --- Title page -------------------------------------------------------
    for _ in range(8):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(book_title)
    run.font.name = FONT_NAME
    run.font.size = Pt(28)
    run.bold = True

    if author:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        run = p.add_run("by " + author)
        run.font.name = FONT_NAME
        run.font.size = Pt(14)
        run.italic = True
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_page_break()

    # --- Manuscript chapters ----------------------------------------------
    total_scenes = 0
    total_words = 0

    for chapter_dir in chapter_dirs:
        scene_files = find_scene_files(chapter_dir)

        h = doc.add_heading(chapter_heading(chapter_dir.name), level=1)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_heading(h, CHAPTER_HEADING_SIZE)

        for i, scene_file in enumerate(scene_files):
            content = read_scene(scene_file)
            add_markdown_block(doc, content)
            total_scenes += 1
            total_words += count_words(content)

            if i < len(scene_files) - 1:
                add_scene_break(doc)

        doc.add_page_break()

    # --- Write output -----------------------------------------------------
    output_path = export_output_path(manuscripts_dir, book_folder, book_title, ".docx")
    doc.save(str(output_path))

    print("Exported: " + output_path.name)
    print("Chapters: %d, Scenes: %d" % (len(chapter_dirs), total_scenes))
    print("Words: {:,}".format(total_words))
    size_kb = output_path.stat().st_size / 1024
    print("Size: %.0f KB" % size_kb)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print(__doc__.strip())
        sys.exit(1)
    export(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
