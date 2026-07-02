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
# AGENTS.md alone is not enough — plenty of unrelated repos have one, and this
# script overwrites AGENTS.md/README.md/LICENSE.md. Require a Proselon-specific
# marker before touching anything.
is_proselon_project() {
    [ -e "$TARGET/.proselon/VERSION" ] && return 0
    [ -d "$TARGET/.proselon/workflow" ] && return 0
    [ -d "$TARGET/.workflow" ] && return 0  # pre-release flat layout
    grep -qi "proselon" "$TARGET/AGENTS.md" 2>/dev/null && return 0
    { [ -d "$TARGET/Plot" ] && [ -d "$TARGET/Manuscripts" ]; } && return 0
    return 1
}
if ! is_proselon_project; then
    echo "This doesn't look like a Proselon project folder." >&2
    echo "cd into your project (the folder with AGENTS.md) and run this again." >&2
    exit 1
fi

# Remember the installed version before touching anything, so we can tell
# afterwards whether this update crossed a version boundary (and the content
# migrations in .proselon/MIGRATIONS.md may apply).
OLD_VERSION="$(cat "$TARGET/.proselon/VERSION" 2>/dev/null || echo "unknown")"

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
# wholesale; nothing else in your project is touched. Copy first, then swap, so
# a failed copy (disk full, permissions) can't leave the project without a
# framework.
rm -rf "$TARGET/.proselon.new"
cp -R "$SRC/.proselon" "$TARGET/.proselon.new"
rm -rf "$TARGET/.proselon"
mv "$TARGET/.proselon.new" "$TARGET/.proselon"

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

# The refresh above replaced framework files only -- author content is never
# touched. But an update can change the *shape* the framework expects (where
# the workflow looks for project files). Those moves need judgment, so they
# are done by the agent, not this script: hand it the migration ledger and
# the version boundary it just crossed.
if [ "$OLD_VERSION" != "$VERSION" ] && [ -f "$TARGET/.proselon/MIGRATIONS.md" ]; then
    cat <<EOF

== CONTENT MIGRATION ==
This project was on version: $OLD_VERSION (now: $VERSION).
If you are the AI assistant running this update: read .proselon/MIGRATIONS.md
now and apply every migration entry newer than $OLD_VERSION. Move the author
files those entries name from their old locations to the new canonical ones --
moves only, never edit a document's contents -- then report what moved. If no
entry applies, say so and move on.
If you are a human running this by hand: open your Proselon session and say
"finish the Proselon update" so your assistant completes this step.
EOF
fi
