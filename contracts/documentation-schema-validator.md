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
