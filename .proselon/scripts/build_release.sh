#!/usr/bin/env bash
# Build a clean customer-facing release zip of the Proselon template.
# Developer tool — not part of the shipped product (excluded via .gitattributes).
#
# Usage:
#   .proselon/scripts/build_release.sh ["Folder Name"]
#
# Packages HEAD with `git archive`, so untracked and gitignored files
# (.claude/settings.local.json, .DS_Store, TODOS.md, .git
# itself) can never leak into the zip. CLAUDE.md is a symlink in the repo and is
# materialized as a regular file in the zip so Windows unzips aren't broken. The
# zip extracts to a single folder (default "My Proselon Project") and preserves
# the Mac launcher's executable bit. Output lands in dist/ (gitignored), named
# after .proselon/VERSION: "dist/Proselon <version>.zip".

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if ! git diff-index --quiet HEAD --; then
    echo "Error: uncommitted changes. git archive packages HEAD — commit first." >&2
    exit 1
fi

# --- Sanity checks for known ship-blockers ---------------------------------

mode="$(git ls-files -s "Start Proselon - Mac.command" | awk '{print $1}')"
if [ "$mode" != "100755" ]; then
    echo "Error: Mac launcher mode is $mode in git, expected 100755." >&2
    echo "Fix: git update-index --chmod=+x 'Start Proselon - Mac.command'" >&2
    exit 1
fi

if git ls-files | grep -qi "superseded\|tombstone"; then
    echo "Error: superseded/tombstone files are still tracked." >&2
    exit 1
fi

# --- Build ------------------------------------------------------------------

NAME="${1:-My Proselon Project}"

# Zip name comes from .proselon/VERSION (e.g. "2026.06.14").
VERSION_FILE="$ROOT/.proselon/VERSION"
TODAY="$(date +%Y.%m.%d)"
if [ -f "$VERSION_FILE" ]; then
    VERSION="$(tr -d '[:space:]' < "$VERSION_FILE")"
else
    echo "Warning: $VERSION_FILE not found — using today's date as the version." >&2
    VERSION="$TODAY"
fi
if [ "$VERSION" != "$TODAY" ]; then
    echo "Warning: .proselon/VERSION is $VERSION but today is $TODAY." >&2
    echo "If this is a new release, bump .proselon/VERSION first (and commit)." >&2
fi

DIST="$ROOT/dist"
mkdir -p "$DIST"
OUT="$DIST/Proselon ${VERSION}.zip"

# Stage HEAD into a temp tree (git archive honors export-ignore), then ship a
# regular CLAUDE.md (it is a symlink in the repo) so Windows unzips work.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
DEST="$TMP/$NAME"
mkdir -p "$DEST"
git archive --format=tar HEAD | tar -x -C "$DEST"

rm -f "$DEST/CLAUDE.md"
printf '@AGENTS.md\n' > "$DEST/CLAUDE.md"

rm -f "$OUT"
( cd "$TMP" && zip -q -r -X "$OUT" "$NAME" )

echo "Built: $OUT"
unzip -l "$OUT" | tail -1
