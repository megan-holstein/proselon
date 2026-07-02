#!/usr/bin/env python3
"""Shared helpers for Proselon's manuscript scripts.

Imported by export_manuscript_markdown.py, export_manuscript_docx.py,
export_manuscript_epub.py, word_count.py, and prose_stats.py so that chapter
discovery, scene discovery, front-matter handling, word counting, and inline
markdown parsing behave identically everywhere. Not meant to be run directly.

Stdlib only — no pip installs needed.
"""

import re
import sys
from pathlib import Path

# The project root is two levels above .proselon/scripts/.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Sorting and naming
# ---------------------------------------------------------------------------

def natural_sort_key(path):
    """Sort by embedded numbers so Chapter 2 comes before Chapter 10."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def chapter_heading(dir_name):
    """Heading for a chapter folder.

    "Chapter 0 - Prologue" -> "Prologue", "Chapter 13 - Epilogue" -> "Epilogue",
    "Chapter 3" -> "Chapter 3".
    """
    if " - " in dir_name:
        return dir_name.split(" - ", 1)[1].strip()
    num = re.search(r"\d+", dir_name)
    return f"Chapter {num.group()}" if num else dir_name


# Characters the Mac Finder or Windows Explorer can't put in a filename.
_ILLEGAL_FILENAME_CHARS = re.compile(r'[/\\:*?"<>|]')


def sanitize_filename(name):
    """Make a book title safe to use inside an output filename."""
    cleaned = _ILLEGAL_FILENAME_CHARS.sub("-", name).strip()
    return cleaned or "Untitled"


def export_output_path(manuscripts_dir, book_folder, book_title, extension):
    """Where an export lands: next to the book folder, with a safe filename."""
    name = f"{book_folder} - {sanitize_filename(book_title)}{extension}"
    return manuscripts_dir.parent / name


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def find_book_dir(book_folder):
    """Return Manuscripts/<book_folder>, or exit with a friendly message."""
    manuscripts_root = PROJECT_ROOT / "Manuscripts"
    book_dir = manuscripts_root / book_folder
    if book_dir.is_dir():
        return book_dir

    lines = [f'Error: could not find "{book_folder}" under {manuscripts_root}.']
    if manuscripts_root.is_dir():
        books = sorted(d.name for d in manuscripts_root.iterdir() if d.is_dir())
        if books:
            lines.append("Book folders that do exist: " + ", ".join(books))
        else:
            lines.append("The Manuscripts folder is empty — nothing has been drafted yet.")
    else:
        lines.append("There is no Manuscripts folder yet — nothing has been drafted.")
    print("\n".join(lines), file=sys.stderr)
    sys.exit(1)


def find_chapter_dirs(book_dir):
    """Chapter folders of a book in reading order, or exit with a friendly message."""
    chapter_dirs = sorted(
        [d for d in book_dir.iterdir() if d.is_dir() and "Chapter" in d.name],
        key=natural_sort_key,
    )
    if not chapter_dirs:
        print(
            f"Error: no chapter folders found in {book_dir}.\n"
            'Chapter folders are named like "Chapter 1" or "Chapter 0 - Prologue".',
            file=sys.stderr,
        )
        sys.exit(1)
    return chapter_dirs


# Scene files start with a capital S and a number: "S1 - Opening Image.md".
_SCENE_FILE_RE = re.compile(r"S\d+")
# Near-misses we warn about instead of silently skipping: "s1 - foo.md" etc.
_SCENE_LIKE_RE = re.compile(r"[Ss]\d")


def find_scene_files(chapter_dir):
    """Scene .md files of a chapter in reading order.

    Only files named like "S1 - Scene Name.md" (capital S + number) count as
    scenes; other .md files (e.g. a stray Summary.md) are ignored. Files that
    *almost* look like scenes (e.g. a lowercase "s1 - foo.md") are skipped too,
    but with a warning so they aren't silently dropped from an export.
    """
    md_files = [f for f in chapter_dir.iterdir() if f.is_file() and f.suffix == ".md"]
    scene_files = sorted(
        [f for f in md_files if _SCENE_FILE_RE.match(f.name)],
        key=natural_sort_key,
    )
    near_misses = sorted(
        f.name for f in md_files
        if f not in scene_files and _SCENE_LIKE_RE.match(f.name)
    )
    if near_misses:
        print(
            f'Warning: skipped in "{chapter_dir.name}" (scene files must start '
            'with a capital S and a number, like "S1 - Name.md"): '
            + ", ".join(near_misses),
            file=sys.stderr,
        )
    return scene_files


# ---------------------------------------------------------------------------
# Scene text
# ---------------------------------------------------------------------------

# YAML front matter: the file starts with a line that is exactly "---", and the
# block ends at the next line that is exactly "---". Both delimiters are
# line-anchored so a "---" scene break inside prose can never swallow the scene.
_FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\n(.*?\n)?---[ \t]*(\n|\Z)", re.DOTALL)


def strip_front_matter(text):
    """Remove a leading YAML front-matter block, if present."""
    match = _FRONT_MATTER_RE.match(text)
    if match:
        return text[match.end():].lstrip("\n")
    return text


def read_scene(path):
    """Read a scene file: UTF-8, front matter stripped, whitespace trimmed."""
    return strip_front_matter(path.read_text(encoding="utf-8")).strip()


def count_words(text):
    """Count words the same way everywhere, so reported numbers always match."""
    return len(text.split())


# ---------------------------------------------------------------------------
# Inline markdown emphasis
# ---------------------------------------------------------------------------

# ***bold italic***, **bold**, *italic*. Emphasis only opens/closes when the
# asterisks hug the text (no space just inside them), so prose arithmetic like
# "2 * 3 * 4" is left alone. Shared by the docx and epub exporters — fix
# emphasis bugs here, once.
_INLINE_RE = re.compile(
    r"\*\*\*(?!\s)(.+?)(?<!\s)\*\*\*"
    r"|\*\*(?!\s)(.+?)(?<!\s)\*\*"
    r"|\*(?!\s)(.+?)(?<!\s)\*"
)


def parse_inline(text):
    """Split a markdown line into (text, bold, italic) runs.

    Returns a list of tuples; plain text runs have bold=False, italic=False.
    """
    runs = []
    last_end = 0
    for match in _INLINE_RE.finditer(text):
        if match.start() > last_end:
            runs.append((text[last_end:match.start()], False, False))
        if match.group(1) is not None:      # ***bold italic***
            runs.append((match.group(1), True, True))
        elif match.group(2) is not None:    # **bold**
            runs.append((match.group(2), True, False))
        else:                               # *italic*
            runs.append((match.group(3), False, True))
        last_end = match.end()
    if last_end < len(text):
        runs.append((text[last_end:], False, False))
    return runs
