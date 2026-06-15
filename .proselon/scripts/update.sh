#!/bin/sh
# Update the Proselon framework in the current project to the latest version.
#
# Run this from inside your Proselon project folder:
#   curl -fsSL https://raw.githubusercontent.com/megan-holstein/proselon/main/.proselon/scripts/update.sh | sh
#
# It pulls the latest framework from the public repo and refreshes the Proselon
# files in place. It is git-agnostic (uses curl + tar, never touches your repo)
# and never modifies your writing (Plot/, Manuscripts/, Worldbuilding/, ...),
# your Obsidian setup (.obsidian/), or your version history (.git/).

set -eu

REPO_OWNER="megan-holstein"
REPO_NAME="proselon"
BRANCH="main"
TARBALL="https://github.com/$REPO_OWNER/$REPO_NAME/archive/refs/heads/$BRANCH.tar.gz"

TARGET="$(pwd)"

# Guard: make sure we're in a Proselon project, not a random directory.
if [ ! -e "$TARGET/AGENTS.md" ] && [ ! -d "$TARGET/.proselon" ] && \
   [ ! -d "$TARGET/.workflow" ] && [ ! -d "$TARGET/Plot" ]; then
    echo "This doesn't look like a Proselon project folder." >&2
    echo "cd into your project (the folder with AGENTS.md) and run this again." >&2
    exit 1
fi

command -v curl >/dev/null 2>&1 || { echo "Error: curl is required." >&2; exit 1; }
command -v tar  >/dev/null 2>&1 || { echo "Error: tar is required." >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT INT TERM

echo "Downloading the latest Proselon framework..."
curl -fsSL "$TARBALL" -o "$TMP/proselon.tar.gz"
tar -xzf "$TMP/proselon.tar.gz" -C "$TMP"
SRC="$TMP/$REPO_NAME-$BRANCH"
if [ ! -d "$SRC" ]; then
    echo "Error: downloaded framework not found where expected." >&2
    exit 1
fi

# One-time migration from the old flat layout (.workflow/.scripts at the project
# root, plus a pre-release .proselon/ that once held launcher state) to the new
# layout where .proselon/ holds the framework. Any old launcher state is dropped;
# the launcher re-detects what's installed on the next run.
if [ -d "$TARGET/.workflow" ] || [ -d "$TARGET/.scripts" ]; then
    echo "Migrating to the new .proselon/ layout..."
    rm -rf "$TARGET/.workflow" "$TARGET/.scripts"
    if [ -d "$TARGET/.proselon" ] && [ ! -d "$TARGET/.proselon/workflow" ]; then
        rm -rf "$TARGET/.proselon"
    fi
fi

# Refresh the framework. .proselon/ is pure framework, so it's safe to replace
# wholesale; nothing else in your project is touched.
rm -rf "$TARGET/.proselon"
cp -R "$SRC/.proselon" "$TARGET/.proselon"

# Root framework files (Proselon-owned, not your writing).
for f in "AGENTS.md" "README.md" "LICENSE.md" \
         "Start Proselon - Mac.command" "Start Proselon - Windows.bat"; do
    if [ -e "$SRC/$f" ]; then
        cp -f "$SRC/$f" "$TARGET/$f"
    fi
done
chmod +x "$TARGET/Start Proselon - Mac.command" 2>/dev/null || true

# CLAUDE.md ships as a symlink in the repo; write a portable regular file here.
printf '@AGENTS.md\n' > "$TARGET/CLAUDE.md"

VERSION="$(cat "$TARGET/.proselon/VERSION" 2>/dev/null || echo "latest")"
echo "Proselon updated to $VERSION."
