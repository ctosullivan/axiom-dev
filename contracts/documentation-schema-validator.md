# Contract: documentation/knowledge validator

Status: **Accepted, pre-implementation.** This is the contract Stage 1.4's
validator must satisfy. Written and committed before any validator code
exists, per `decisions/0004` (Amendment B — "behavioural contracts
established before implementation"). Changing this contract after
implementation starts requires its own reviewed change explaining why,
not a silent edit inside the implementation PR
(`planning/phase-01-foundation.md` §4, Stage 1.4 "Anti-circularity
mechanics").

**Note on rules 1–15 below, added by the "Contract revision" section
further down (prompt 004, `decisions/0006`):** rules 1–15 describe the
validator's original embedded-front-matter mechanics (rules 1–9) and
their Amendment C field-validation extension (rules 10–15). They are
preserved **verbatim, as historical record** of what Stage 1.4 and the
prompt 003 batch actually specified and built at the time — not edited
to read as though companion schema files had always been the
convention. The "Contract revision" section states what the validator
actually checks **now**; where the two disagree, the revision governs
current behaviour.

## Scope

The validator checks one Markdown document with an optional YAML
front-matter block, as defined by `docs/documentation-schema.md`, against
its own declared schema. It does not check any document *without* a
front-matter block — such documents are out of scope, not failures.
**(Historical — see "Contract revision" below: the validator now reads
the schema from a companion `.schema.yaml` file, not embedded
front-matter.)**

## Contract

Given a Markdown file:

1. **No front-matter present** → the validator reports `SKIPPED` for that
   file, not an error. (A document with no schema has nothing to check.)
2. **Front-matter present but not valid YAML** → the validator reports
   `INVALID_SCHEMA` with the YAML parser's error location. It does not
   attempt to validate sections if the schema itself can't be parsed.
3. **Front-matter present, valid YAML, missing a required schema field**
   (`audience`, `purpose`, `required_sections`, `authoritative_sources`,
   or `acceptance_criteria`) → the validator reports `INVALID_SCHEMA`
   naming the missing field(s).
4. **Front-matter valid, `required_sections` is a list of heading
   strings** → the validator checks the document body for a heading at
   any level (`#` through `######`) matching each string exactly
   (case-sensitive, ignoring leading/trailing whitespace). One matching
   heading anywhere counts as present — duplicate headings with the same
   text are not an error, and the level a required heading appears at is
   not itself checked. Every required string matched → `PASS` for section
   checks. Any miss → `FAIL` naming every missing heading, not just the
   first.
5. **`authoritative_sources` entries must be bare, repository-relative
   paths** — no appended section markers (e.g. `AGENTS.md §7` is invalid;
   write `AGENTS.md`, and put the section detail in prose if needed) and
   no paths outside this repository (a citation to another project, e.g.
   CodeCompass's own ADRs, belongs in body prose, not in this field). The
   validator checks each entry resolves relative to the repository root.
   A path that doesn't resolve, or that isn't a bare path, → `FAIL`
   naming the offending entry. (This checks the path exists; it does not
   check the document's claims are actually consistent with that source —
   that remains a semantic/editorial check, per
   `docs/knowledge-placement.md` "Enforcement classes.")
6. **Any Markdown relative link in the document body (`[text](path)`,
   excluding `http(s)://` and in-page `#anchor` links)** → checked the same
   way as rule 5: must resolve relative to the document's own location.
   Unresolvable → `FAIL` naming the broken link.
7. **Scope note for rule 5/6 results that point into `decisions/`:** if an
   `authoritative_sources` entry or a body Markdown link (not a bare
   inline-code mention in running prose — those aren't checked, since they
   aren't paths) resolves to this repository's own `decisions/NNNN-*.md`,
   `NNNN` must be a real, existing ADR number in *this* repository. This is
   a refinement of rules 5/6, not a separate full-text scan — a prose
   sentence that merely discusses another project's ADR number (e.g. "per
   CodeCompass's `decisions/0094`") is not a path reference and is out of
   scope for this rule.
8. **Overall result** for a file is `PASS` only if every applicable rule
   above (2–7) that applies to that file returns `PASS`/is satisfied; one
   `FAIL` anywhere makes the file's overall result `FAIL`. `SKIPPED` files
   do not count toward pass or fail totals.
9. **Error reporting**: every `FAIL` or `INVALID_SCHEMA` result names the
   file, the specific rule violated, and enough detail (missing heading
   text, broken path, bad ADR number) that a human doesn't have to re-run
   the check by hand to find the problem.

## Non-goals

- No check of whether `acceptance_criteria` statements are actually true
  — that requires understanding meaning, which is out of scope for a
  mechanical validator (per `docs/knowledge-placement.md`, this stays a
  semantic/editorial, non-blocking concern).
- No enforcement of *which* documents must carry a schema — rule 1 makes
  an unschema'd document a no-op, not a violation.
- No network access, no fetching remote URLs to check they resolve.
- No auto-fixing — the validator reports; it does not rewrite documents.
- **No CommonMark indented-code-block recognition.** The fence-aware
  heading extraction (rule 4; `_strip_fenced_code_blocks`) handles
  fenced blocks (``` ``` ``` or `~~~`, 3+ characters) only — a
  4-space-indented block (CommonMark's other code-block convention) is
  not recognised as code at all, so a heading-looking line inside one
  would still count as a real heading. Found by independent review of
  prompt 005's fence-handling fix, out of scope for that fix (Codex's
  finding was specifically about fence-character/length recognition,
  not indentation conventions) and left as a documented, proportionate
  gap rather than expanded scope.
- **A closing fence indented with a literal tab does not close.** Only
  0–3 leading *spaces* are recognised before a closing fence's
  characters (matching the opening-fence rule, and CommonMark's own
  convention). A tab-indented closing line is treated as still-fenced
  content, which fails in the safe direction (more gets hidden, so a
  real heading could be missed and reported FAIL — never the Codex
  defect's direction of wrongly reporting PASS). Found by the same
  independent review pass; left undocumented no longer, not fixed,
  since over-hiding is not the false-positive failure mode this
  contract's rule 4 exists to prevent.

## Contract amendment (prompt 003 Amendment C, 2026-11-21)

Status: **Accepted, post-implementation amendment.** Unlike the original
contract above (written before any validator code existed), this
amendment follows the existing implementation it extends — the original
9 rules and their numbering are unchanged and not renumbered; this is an
addition, not a revision, per `AGENTS.md` §9 ("a contract change needs
its own plan entry... not weakened unilaterally" — here, strengthened,
with its own reviewed entry: `planning/phase-01-foundation.md` §17).
Motivation: the original contract fixed *presence* of the five required
front-matter fields (rule 3) but not their *type* or *meaningful content*
— a document with `audience: ""` and `acceptance_criteria: []` passed
rule 3 unchanged, which `planning/prompts/003-phase-1-corrective-amendment.md`
Amendment C identifies as a real weakness.

10. **`audience` and `purpose` must be non-empty strings** (after
    stripping leading/trailing whitespace). A missing-content value
    (e.g. `audience: ""` or `audience: "   "`) → `INVALID_SCHEMA`, naming
    the field. (A present-but-wrong-type value, e.g. a number or list,
    is also `INVALID_SCHEMA` under this rule — "non-empty string" implies
    "string.")
11. **`required_sections`, `authoritative_sources`, and
    `acceptance_criteria` must each be a list of strings** (not a bare
    string, mapping, number, or a list containing a non-string entry).
    A violation → `INVALID_SCHEMA`, naming the field and why (wrong type
    entirely, or a specific non-string entry).
12. **`required_sections` must be a non-empty list.** A document that
    declares zero required sections has not meaningfully used the field
    → `INVALID_SCHEMA`. **Scope note, found worth stating explicitly by
    independent review:** prompt 003 Amendment C's prose frames this as
    applying to "governed substantive documents," but this rule applies
    to **every** document that carries front-matter at all, governed or
    not — a deliberate generalisation, not a literal narrowing to the
    governed-manifest set. Rationale: rule 3 already makes
    `required_sections` mandatory for any document with front-matter;
    an empty list under a mandatory field is equally meaningless whether
    or not that document happens to be on `docs/governed-documents.txt`,
    so scoping this rule to the manifest would have made it weaker than
    rule 3 itself, not more proportionate. Rule 15 (governed scope)
    stays narrow by design — it governs which documents *must have* a
    schema at all, which is the part of Amendment C's request this rule
    does not extend.
13. **`acceptance_criteria` must be a non-empty list of non-empty
    strings.** Each entry must have actual content after stripping
    whitespace — this does not check that the content is *true* (that
    remains a semantic/editorial concern per `docs/knowledge-placement.md`
    "Enforcement classes"), only that it is not empty or placeholder
    whitespace. Violation → `INVALID_SCHEMA`.
14. **`authoritative_sources` may legitimately be an empty list (`[]`).**
    This is not itself a violation — it represents a document with no
    internal authoritative dependencies, not an omission. Rule 11's type
    check still applies (it must actually be a list of strings, just
    possibly zero of them); existing rules 5/7 still apply to whatever
    entries are present. **No placeholder entry (e.g. `"N/A"`, `"none"`)
    is required or accepted as a substitute for an empty list** — such an
    entry is a string that must resolve as a real repository path under
    rule 5, so a placeholder string fails rule 5 on its own merits
    (it does not resolve to a real file), rather than needing a special
    "detect placeholder text" rule.
15. **Governed document scope.** A new file, `docs/governed-documents.txt`
    (one repository-relative path per line; blank lines and `#`-prefixed
    comment lines ignored), lists documents that must carry a complete,
    passing schema. For a path listed in that manifest: rule 1's `SKIPPED`
    result for "no front-matter present" is replaced by `FAIL`, naming
    the file as a governed document with no schema. For a path **not**
    listed in the manifest, rule 1's original `SKIPPED` behaviour is
    unchanged — this amendment narrows rule 1's scope for a small,
    explicit set of documents; it does not change it for anything else.
    This directly closes the gap prompt 003 names: "deleting a document's
    schema could silently bypass its checks" — only for documents the
    manifest actually lists, by design (prompt 003: "keep this mechanism
    minimal").

Rules 10–13 are checked immediately after rule 3 (required-field
presence) and before rules 4–7 (which assume well-typed data) — a
violation here short-circuits to `INVALID_SCHEMA` the same way rule 3
itself does, for the same reason: rules 4–7 cannot be meaningfully
evaluated against malformed field content.

Regression fixtures and their own dedicated test file (not the
checksum-protected `tests/test_axiom_validator.py`) are required for
each new rule — see `tests/test_axiom_validator_schema_content.py` and
`tests/fixtures/invalid/{empty_audience,non_string_required_sections,
empty_required_sections,empty_acceptance_criteria,
placeholder_acceptance_criteria}.md`,
`tests/fixtures/valid/empty_authoritative_sources.md`.

## Contract revision (prompt 004 Amendments A/C — companion schema files, 2026-11-21)

**Note, added by "Contract revision 2" further down (prompt 005,
decisions/0007): rules 1–2 and 15's "in the same directory" / "no
companion schema file... colocated" framing below describes the
colocated-companion-file location this revision introduced at the
time — that location is itself superseded by "Contract revision 2."
The field-validation substance (rules 3–9 below) is unaffected and
still describes current behaviour; only where the schema file lives
has moved again.**

Status: **Accepted, authorised contract evolution — not a
behaviour-preserving refactor.** Per
`planning/prompts/004-documentation-schema-and-roadmap-amendment.md`
§6: "Amend the accepted documentation-validator contract before
changing implementation behaviour... This is an authorised contract
evolution, not a behaviour-preserving refactor." Written and committed
before the corresponding implementation change, per the same
contract-first discipline `decisions/0004` established for the original
contract. See `decisions/0006` for the architectural decision this
implements and `evidence/schema-migration.md` for the document
migration this revision requires.

**What changes:** where the schema for a document lives, and how the
validator finds it. **What does not change:** the substantive
field-validation requirements themselves (rules 10–15 above) — a
document's `audience`/`purpose`/`required_sections`/
`authoritative_sources`/`acceptance_criteria` must satisfy exactly the
same constraints as before; only their storage location moves.

1. **Companion schema path.** For a document at `<path>.md`, its schema
   (if any) lives at `<path>.md.schema.yaml`, in the same directory,
   with no separate registry — the relationship is computed from the
   document's own path alone. **Supersedes rule 1's "front-matter
   block" framing.**
2. **No companion schema file exists for a given document** → `SKIPPED`,
   *unless* the document's path is listed in `docs/governed-documents.txt`
   (rule 15, unchanged in substance — only its trigger condition moves
   from "no front-matter" to "no companion schema file"), in which case
   it is `FAIL`, naming the document as governed with no schema.
   **Supersedes rule 1 and rule 15's trigger condition.**
3. **A companion schema file exists but is not valid YAML, or is valid
   YAML but not a mapping** → `INVALID_SCHEMA`, naming the parse error.
   **Supersedes rule 2.**
4. **A companion schema file exists and parses, but is missing a
   required field, has a field of the wrong type, or has empty required
   content** → `INVALID_SCHEMA`, exactly as rules 3 and 10–14 already
   specify — unchanged logic, now operating on the companion file's
   parsed content instead of front-matter's.
5. **Required sections, authoritative sources, and body links** are
   checked against the *document's full text* (there is no front-matter
   to split off any more — the whole file is body) — unchanged logic
   (rules 4–7), applied to the whole file instead of a post-front-matter
   substring. For a migrated document this produces identical results to
   before migration, since the only text removed was the front-matter
   block itself.
6. **Overall PASS/FAIL combination and error reporting** — unchanged
   (rules 8–9).
7. **NEW — Embedded front-matter reintroduction.** A document whose text
   begins with a `---\n...\n---\n` block (the old convention) is `FAIL`,
   naming it as a deprecated-convention reintroduction — **never**
   parsed as if it were the current schema, even if a companion
   `.schema.yaml` file also happens to exist alongside it. Directly
   implements prompt 004 Amendment C: "do not silently support two
   competing schema conventions indefinitely."
8. **NEW — Orphaned schema detection.** A `<path>.md.schema.yaml` file
   with no corresponding `<path>.md` document is `FAIL`, naming the
   orphan. **Scope note:** this check is inherently repository-wide (it
   requires knowing that *no* document exists at a given path, not
   checking one named document), so it runs as part of the CLI's batch
   `main()` entry point scanning `repo_root`, not inside `validate_file`,
   which checks exactly one named document and has no way to assert a
   negative about the rest of the repository from a single call.
9. **Non-governed document with a companion schema present must still be
   validated.** A document's governed-manifest status only changes what
   happens when its schema is *absent* (rule 2 above); if a companion
   schema file exists, it is always checked, governed or not — this was
   already true of embedded front-matter (any document with front-matter
   got checked) and remains true of companion files.

**Non-goal, added to this revision:** rule 7's embedded-front-matter
detection fires on *any* `---`-delimited block at the start of a file —
it cannot and does not try to distinguish "this was the documentation
schema convention" from "this file legitimately uses a `---`-delimited
block for something else" (e.g. `planning/prompts/`'s preserved-prompt
provenance headers — `id`/`title`/`status`/`date_received`/etc., a
different, intentional convention that was never part of the
documentation-schema system and is not governed). Such files report
`FAIL` under rule 7, which is a correct, harmless, if slightly
imprecisely-worded result for them — they are not validated by any CI
step (not in `docs/governed-documents.txt`), and nothing in this project
treats that `FAIL` as a defect requiring migration. Distinguishing the
two cases would require guessing at a block's semantic intent, which
this mechanical validator deliberately does not do.

## Contract revision 2 (prompt 005 — top-level `schemas/` directory, 2026-11-21)

Status: **Accepted, authorised contract evolution — not a
behaviour-preserving refactor.** Per
`planning/prompts/005-phase-1-final-remediation-and-closeout.md` §8:
"Amend the current documentation-validator contract to specify the new
location convention." See `decisions/0007` for the architectural
decision this implements and `evidence/schema-migration.md` for the
document migration this revision requires.

**What changes:** where a document's schema file lives, moving a
second time — from colocated beside its document (Contract revision
above, decisions/0006) to a mirrored path under a top-level `schemas/`
directory (decisions/0007). **What does not change:** everything else
— the field-validation substance (rules 3–9 of the revision above),
and the embedded-front-matter/orphan-detection rules' *existence*
(only rule 2's trigger path and rule 8's scan root move).

1. **Mirrored schema path.** For a document at repository-relative path
   `<rel>`, its schema (if any) lives at `schemas/<rel>.schema.yaml`,
   computed from the document's path and a *mirror root* — normally
   the repository root, so production schemas resolve under
   `<repo_root>/schemas/`. **Supersedes rule 1 of the revision above**
   ("in the same directory" is no longer where the schema lives).
2. **Test fixtures use a separate mirror root** (their own
   `tests/fixtures/` directory, not the repository root), so fixture
   schemas live at `tests/fixtures/schemas/<rel>.schema.yaml` — a tree
   wholly separate from the production `schemas/` tree, never nested
   inside it. This is the mechanism, not a convention taken on faith:
   `schema_path_for(doc_path, mirror_root)` takes the mirror root as an
   explicit parameter, and `validate_file`'s new optional
   `schema_mirror_root` parameter (default: `repo_root`) is how a
   caller supplies a different one.
3. **The governed-document manifest moves to `schemas/governed-documents.txt`**
   (still a flat list of document paths, same logic as rule 15 of the
   original contract — only its own file's location changes).
   **Supersedes rule 2 of the revision above's manifest path.**
4. **NEW — A missing manifest *file* fails closed.** If
   `schemas/governed-documents.txt` does not exist at all, every
   document checked via the default (non-overridden) governed-manifest
   path is `FAIL`, naming the missing manifest — not silently treated
   as "nothing is governed." A manifest file that exists but lists zero
   documents is unaffected by this rule and legitimately produces
   `SKIPPED` for an unschema'd, non-listed document, exactly as before.
   **Implementation note (prompt 006's follow-up, found by a third
   native Codex review of PR #1):** this rule's text was correct from
   the moment it was written, but `validate_file` did not actually
   satisfy it for every document — the manifest was only loaded inside
   the branch taken when a document's *own* schema file was absent, so
   a document whose schema existed and parsed cleanly could still
   return `PASS` even with no manifest file at all. This was an
   implementation defect against an already-correctly-specified rule,
   not a contract change — fixed by loading/checking the manifest
   unconditionally whenever `governed_manifest` is not explicitly
   overridden, before branching on whether the document's own schema
   exists.
5. **NEW — Path safety.** Computing a schema path for a document that
   does not resolve under its mirror root is itself a reported failure
   (`PathEscapesMirrorRoot`), not a silently wrong or escaping path.
6. **Orphan detection's scan root moves** to `<mirror_root>/schemas/`
   (from scanning the whole repository tree minus an excluded `tests/`
   prefix, rule 8 of the revision above). Because the fixture mirror
   tree (rule 2 above) is never nested inside the production one, this
   scan now needs no exclusion list at all to avoid flagging the
   deliberately orphaned test fixture — the two trees simply don't
   overlap, which is a stronger guarantee than excluding a path prefix
   by name.
7. **No obsolete schema files remain outside a `schemas/` directory.**
   Checked directly against the real repository
   (`tests/test_schema_relocation.py`'s
   `TestNoStraySchemaFilesOutsideSchemasTree`), not merely asserted in
   this contract.

## Traceability

This contract traces: `planning/prompts/001-phase-1-bootstrap.md` §5
("plan a lightweight Python validator as the first substantive Axiom Dev
component") → `decisions/0002` (knowledge architecture, validator
deferred to Stage 1.4) → `planning/phase-01-foundation.md` Stage 1.4 →
this contract → (pending) Stage 1.4 implementation and its tests. This is
the concrete instance used for Amendment D demonstration #2
(`planning/phase-01-foundation.md` §10).

Fixture files that exercise rules 1–9 above are expected under
`tests/fixtures/` once Stage 1.4 begins implementation, with checksums
recorded in `evidence/` at the point they're accepted — see
`planning/phase-01-foundation.md` §4 Stage 1.4.
