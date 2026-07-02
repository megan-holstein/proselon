# Content Migrations

A Proselon update replaces framework files (`.proselon/`, `AGENTS.md`, the
launchers) and never touches author content. But an update can change the
project's *shape* — where the workflow expects to find files. When that
happens, an existing project must have its content moved to the new locations,
or state detection will read the project as less complete than it is.

This file is the ledger of those shape changes, newest first. The update
script prints the version the project was on; find every entry newer than
that version and apply the applicable ones in chronological order, oldest
first.

## Rules

These override anything an individual entry says:

1. **Move, never modify.** A migration relocates files; document contents stay
   byte-identical. If an entry seems to require editing a document's contents,
   stop and surface it to the author instead of editing.
2. **Best fit, not force fit.** Move a file only when its new home is clear
   from the entry and the file's role. If placement is ambiguous, leave the
   file where it is and report it to the author as an open question.
3. **Author content never gets deleted.** A migration may leave empty
   directories behind; removing those is fine. Removing files is not.
4. **Use `git mv` when the project is a repository**, and commit the migration
   as one commit (`Proselon <version>: migrate content layout`). This is a
   working commit — don't surface git to the author.
5. **Leave the invisible folders alone:** `.obsidian/`, `Archive/`, `.git/`.
6. **Verify by re-running state detection.** After the moves, the project must
   read at the same (or better) workflow position as before the update — every
   gate file that existed before must still be found. If a gate regressed, a
   move went wrong; fix it before reporting.
7. **Report to the author:** which files moved where, and anything left
   unmoved as ambiguous. Keep it in plain terms — locations, not git.

If the previous version is `unknown` (a pre-release project), don't hunt for
entries: reconcile the whole project against the canonical layout in AGENTS.md
(**File Placement and Naming**) and move any author file at an obsolete
location to its best-fit canonical path, under the same rules.

## Migrations

### 2026.06.14 — baseline (initial public release)

No content moves. The pre-release flat framework layout (`.workflow/`,
`.scripts/` at the project root) is migrated mechanically by the update script
itself; author content locations did not change.

<!-- Adding an entry (do it in the same commit as the layout change):

### <VERSION> — <one-line summary>

- `<old canonical path or glob>` → `<new canonical path>` — <why>

Name concrete old→new path pairs. If the move needs judgment ("scene plots
gain a subfolder per chapter"), describe how to decide placement. Never
require content edits — if a change needs documents rewritten, that's a
framework feature with its own procedure, not a migration entry.
-->
