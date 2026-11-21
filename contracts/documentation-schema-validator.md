---
audience: whoever implements, refactors, or independently verifies the Stage 1.4 validator
purpose: fix the validator's required behaviour before implementation exists, so later work has something fixed to be checked against
required_sections: [Scope, Contract, Non-goals, Traceability]
authoritative_sources: [docs/documentation-schema.md, planning/phase-01-foundation.md]
acceptance_criteria:
  - every behaviour below is phrased so a test can assert it directly
  - this contract predates the Stage 1.4 implementation it governs (decisions/0004, Amendment B)
---

# Contract: documentation/knowledge validator

Status: **Accepted, pre-implementation.** This is the contract Stage 1.4's
validator must satisfy. Written and committed before any validator code
exists, per `decisions/0004` (Amendment B — "behavioural contracts
established before implementation"). Changing this contract after
implementation starts requires its own reviewed change explaining why,
not a silent edit inside the implementation PR
(`planning/phase-01-foundation.md` §4, Stage 1.4 "Anti-circularity
mechanics").

## Scope

The validator checks one Markdown document with an optional YAML
front-matter block, as defined by `docs/documentation-schema.md`, against
its own declared schema. It does not check any document *without* a
front-matter block — such documents are out of scope, not failures.

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
