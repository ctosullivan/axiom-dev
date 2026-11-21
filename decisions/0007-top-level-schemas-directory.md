# 0007. Consolidate documentation schemas into a top-level `schemas/` directory

## Status

Accepted — 2026-11-21

## Context

`decisions/0006` moved documentation schemas out of embedded Markdown
front-matter into a companion file colocated beside its document:
`<path>.md` → `<path>.md.schema.yaml`, in the same directory. That
solved the readability problem embedded front-matter caused, but
introduced a narrower one: `docs/` (and `contracts/`, `evidence/`,
`planning/retros/`, `planning/archive/`) now mix human-readable
Markdown with machine-oriented `.schema.yaml` files in the same
directory listing — a reader browsing `docs/` for an explanation has to
pick the real documents out from their schemas, which is a smaller
version of the exact problem `decisions/0006` was written to solve one
level down. A fifth authorising prompt
(`planning/prompts/005-phase-1-final-remediation-and-closeout.md`,
Part B) requires consolidating every production schema into one
dedicated top-level `schemas/` directory, mirroring each document's own
path.

## Decision

1. **Every production schema moves to `<repo_root>/schemas/<relative-document-path>.schema.yaml`** —
   deterministic, computed from the document's own repository-relative
   path alone (`src/axiom_validator/parsing.py`'s `schema_path_for`),
   with no registry mapping document to schema. `README.md`'s schema is
   `schemas/README.md.schema.yaml`; `docs/axiom-validator.md`'s is
   `schemas/docs/axiom-validator.md.schema.yaml`; and so on for every
   governed/schema-bearing document.
2. **The governed-document manifest moves with it**, to
   `schemas/governed-documents.txt` — still a flat list of
   repository-relative *document* paths, not schema paths; its own
   logic (which documents must carry a passing schema) is unchanged by
   this ADR, only its file's location.
3. **Test fixtures get their own, separate mirror tree**
   (`tests/fixtures/schemas/`, rooted at `tests/fixtures/` rather than
   the repository root), never nested inside the production `schemas/`
   tree. This is not cosmetic: it is what lets the production
   repository-wide orphan scan (`rules.find_orphaned_schemas`, scoped
   to `<repo_root>/schemas/`) never see a fixture at all, closing the
   exact recurring problem prompt 004's "exclude `tests/` by name"
   workaround was patching around — the two trees now simply don't
   overlap, so there is nothing to exclude.
4. **A missing governed-document manifest *file* now fails closed**,
   distinctly from a present-but-empty one (which legitimately means
   "nothing is governed" and stays a no-op). Found worth deciding
   explicitly, not left as an accidental side effect of the move:
   `rules.load_governed_manifest` raises `GovernedManifestMissing` when
   the file doesn't exist, and `validate_file` turns that into a `FAIL`
   result for whatever document was being checked, rather than silently
   treating every document as ungoverned the moment the manifest file
   is deleted or the move is done incompletely.
5. **Path-safety**: `schema_path_for` raises `PathEscapesMirrorRoot` for
   a document path that doesn't resolve under the mirror root it's
   being mirrored against, rather than computing a nonsensical or
   escaping path.

## Alternatives considered

- **Keep the colocated convention (`decisions/0006`'s), accept the
  clutter.** Rejected: this is the status quo prompt 005 explicitly
  asks to change, for the same class of reason `decisions/0006` itself
  gave for moving away from front-matter — a human reader shouldn't
  have to filter machine-oriented files out of a documentation
  directory listing.
- **A schema registry file** (document path → schema path mapping).
  Rejected per prompt 005's explicit instruction ("do not introduce a
  database, schema registry or manually maintained document-to-schema
  mapping") and for the same reason the governed-documents manifest is
  a flat list, not a mapping: a registry is itself a second place that
  can drift out of sync with the files it describes.
- **Mirror fixture schemas inside the production `schemas/` tree**
  (e.g. `schemas/tests/fixtures/...`). Rejected after noticing it would
  reintroduce prompt 004's exact "deliberately orphaned fixture breaks
  the real orphan scan forever" problem, since a repo-wide orphan scan
  over all of `schemas/` would then have to specially tolerate the one
  fixture that's supposed to look orphaned. A wholly separate fixture
  mirror tree avoids this by construction, not by exclusion.
- **Silently treat a missing manifest file the same as an empty one.**
  Rejected per prompt 005 Sec 7's explicit instruction to assess this
  case and fail closed if it would otherwise silently disable
  enforcement — which it would have.

## Rationale

The readability argument is the same one `decisions/0006` already
made, one directory level up: separate what a human reads from what a
machine checks, and make the separation itself mechanically checkable
(orphan detection, reintroduction detection) rather than relying on
discipline to keep two files in step. The fixture-tree separation and
the fail-closed manifest behaviour are both responses to concrete
failure modes this project has already hit once before (prompt 004's
orphan-scan-breaks-CI-forever bug) or was asked to assess explicitly
(a silently-disabled governed-document check) — not speculative
hardening.

## Consequences

- Every governed/schema-bearing document now has its schema at a
  *different* relative location than `decisions/0006` put it — a real,
  disclosed migration, not a silent one. See
  `evidence/schema-migration.md`'s update for this move's own itemised
  record (appended, not rewritten — `decisions/0006`'s migration record
  for the front-matter-to-sidecar move stays accurate for what it
  described at the time).
- `docs/` now contains only human-readable Markdown — no
  `.schema.yaml` files, no manifest file.
- `validate_file` gains one new optional parameter,
  `schema_mirror_root` (defaults to `repo_root`), so every existing
  call site is unaffected unless it needs to point at a different
  mirror tree (as the test suite now does for fixtures).
- `find_orphaned_schemas` gains one new optional parameter,
  `mirror_root` (defaults to `repo_root`), with the same
  backward-compatible default.
- A missing `schemas/governed-documents.txt` is now a loud, visible
  failure (every document checked without an explicit override fails)
  rather than a silent, total loss of enforcement — a stricter
  guarantee than `decisions/0006` provided, recorded here as a
  deliberate decision, not an incidental side effect.

## Relevant evidence

- `planning/prompts/005-phase-1-final-remediation-and-closeout.md`
  §5–§7 (Amendments B/C's requirements, verbatim).
- `contracts/documentation-schema-validator.md` "Contract revision 2"
  section.
- `evidence/schema-migration.md` (migration record, both moves).
- `tests/test_schema_relocation.py` (the mirroring/fail-closed/no-stray-files
  regression tests).
- `decisions/0006` (the convention this ADR relocates, not reverses —
  companion files remain the convention; only their directory changes).

## Supersession

**Partially supersedes `decisions/0006`**: the *location* convention
(colocated beside the document) is superseded by the mirrored
`schemas/` tree; `decisions/0006`'s decision to use companion files at
all (rather than embedded front-matter) is unaffected and remains in
force. `decisions/0006` is not edited; its own historical record of the
front-matter-to-sidecar move remains accurate for what it described at
the time.
