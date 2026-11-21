# Axiom Dev documentation/knowledge validator

This document was written after the validator existed and was refactored
— found missing during Stage 1.4→1.5 reconciliation (a real knowledge-placement
gap: the validator had a contract and evidence records, but no
human-facing `docs/` explanation, which `AGENTS.md` §7's placement table
calls for). It is deliberately written from the outside, describing what
the component does and how it's built, not restating the contract's rule
text verbatim.

## Purpose

Checks a Markdown document's companion `<document>.md.schema.yaml` file
(the schema convention in `docs/documentation-schema.md`, since
`decisions/0006` — originally embedded front-matter, see that ADR for
why it moved) against the document's own declared requirements: are the
required sections actually present, do the sources it claims to be
consistent with actually exist, do its body links resolve. It's a
mechanical check — it can tell you a required heading is missing; it
can't tell you the document is well-written. See
`docs/knowledge-placement.md` "Enforcement classes" for that distinction.

This is Axiom Dev's first real software component (`planning/prompts/001-...md`
§5 named it as the first substantive piece to build). Its exact required
behaviour is fixed in `contracts/documentation-schema-validator.md`,
written and accepted before any of this code existed, and later amended
twice with its own independently reviewed revisions (prompt 003's field
type/content rules; prompt 004's move to companion schema files).

## Architecture

`src/axiom_validator/` is a small package, split (via a Stage 1.4
behaviour-preserving refactor — `evidence/stage-1.4-refactor.md`) into:

- **`parsing.py`** — turns a document's raw text and its companion
  schema file into usable pieces: computes the deterministic companion
  path (`companion_schema_path`), detects an accidentally reintroduced
  embedded front-matter block (`has_embedded_frontmatter` — repurposed
  from the old front-matter-splitting logic it replaced), parses the
  companion file's YAML (`parse_schema_yaml`), extracts the set of
  headings actually present in the document's full text (excluding
  anything inside a fenced code block), and extracts the Markdown links
  in the body (excluding inline code spans). No rule logic lives here —
  just "what's in this text, and where is its schema."
- **`rules.py`** — the actual checks, each a small function taking
  already-parsed data and returning a list of error strings: required
  fields, field types and non-empty content (`audience`/`purpose` as
  non-empty strings; `required_sections`/`authoritative_sources`/
  `acceptance_criteria` as correctly-typed, and non-empty where the
  contract requires it), required sections, authoritative-source paths
  (including the repository-containment check — a path can't escape the
  repo via `../` even if something happens to exist there), body links
  (same containment rule, plus ADR-specific error messages for
  `decisions/NNNN-*.md` references), the governed-documents manifest
  (`load_governed_manifest`, rule 15 — see Limitations below for exactly
  what this does and does not cover), and orphaned-schema detection
  (`find_orphaned_schemas` — a repository-wide scan for
  `*.md.schema.yaml` files with no corresponding document, excluding
  `tests/` by default since fixtures deliberately include a real orphan
  to test this function; scanning the real repo root without that
  exclusion would flag it on every run). `load_governed_manifest` and
  `find_orphaned_schemas` are the two exceptions to "no file-reading
  lives here": both are inherently about files other than the one
  document being validated, not about already-parsed content.
- **`reporting.py`** — turns a result into the dict shape
  (`file`/`result`/`errors`) everything else expects, and formats a batch
  for the CLI.
- **`__init__.py`** — orchestrates the above for one document
  (`validate_file`): detect embedded front-matter reintroduction first
  (immediate `FAIL`, never falls through to parsing it as a schema);
  otherwise locate the companion schema file (missing → `SKIPPED`,
  or `FAIL` if the document is on the governed manifest); parse it
  (`INVALID_SCHEMA` on failure); check required fields, then field
  types/non-empty content (both short-circuit to `INVALID_SCHEMA`); then
  sections/sources/links; then report. `main()` additionally scans
  `repo_root` for orphaned schemas after validating the given paths —
  this is a repository-wide check, not a per-document one, so it lives
  in the CLI entry point rather than `validate_file`. `validate_file`
  resolves `repo_root` internally so callers don't have to pass an
  already-resolved path themselves.
- **`__main__.py`** — lets `python3 -m axiom_validator <files>` work.

Why split it this way: parsing, rule-checking, and reporting are
genuinely separable concerns — you can change how a link is reported
without touching how it's detected, or add a new rule without touching
how a schema is located and parsed. The pre-refactor version had all
three tangled into one function; the split is verified
behaviour-preserving for the Stage 1.4 refactor itself
(`evidence/stage-1.4-refactor.md`) — the later move from front-matter to
companion files (prompt 004) is explicitly **not** behaviour-preserving
(`contracts/documentation-schema-validator.md` "Contract revision"), and
is not described as such.

## Usage

```
PYTHONPATH=src python3 -m axiom_validator <file1.md> [file2.md ...] --repo-root .
```

Exits `0` if every file is `PASS` or `SKIPPED` (no companion schema —
nothing to check) and no orphaned schema was found anywhere under
`--repo-root` (outside `tests/`); `1` if any file is `FAIL` or
`INVALID_SCHEMA`, or an orphan is found. Requires PyYAML
(`requirements.txt`).

**Note:** every CLI run scans the whole `--repo-root` for orphaned
schemas, regardless of which specific files you pass — this is
intentional (orphan detection is inherently a repository-wide question),
not a bug if you see an orphan reported for a file you didn't name.

To validate a document programmatically:

```python
from pathlib import Path
from axiom_validator import validate_file

result = validate_file(Path("README.md"), Path("."))
# {"file": "README.md", "result": "PASS", "errors": []}
```

(`repo_root` does not need to be pre-resolved — `validate_file` resolves
it internally. This example was found to reproducibly FAIL, not PASS, by
independent semantic review in the prompt 003 batch: an unresolved
`Path(".")` previously broke the repository-containment check for every
`authoritative_sources` entry and body link — fixed in that same change,
unaffected by the later move to companion schema files.)
`validate_file` does **not** check for orphaned schemas — see Architecture
above for why that's a `main()`-level concern, not a per-document one.

## Limitations

Limitations of the validator's own behaviour (all from
`contracts/documentation-schema-validator.md`'s Non-goals and its
"Contract revision" section, which this document is required to stay
consistent with as its own cited authoritative source):

- Enforcement of which documents must carry a schema is **narrow, not
  general**: only paths listed in `docs/governed-documents.txt` (rule
  15) are `FAIL` when unschema'd. Deliberately minimal, per
  `planning/phase-01-foundation.md` §17: any document *not* on that
  short list is still `SKIPPED`, not flagged, if it has no companion
  schema file — an explicit scope choice, not an oversight, but it does
  mean deleting a document's schema still goes unnoticed for anything
  the manifest doesn't name.
- Does not check whether `acceptance_criteria` statements are actually
  true, or whether `authoritative_sources` entries are genuinely
  consistent with the document's claims — both are semantic/editorial
  concerns out of scope for a mechanical check
  (`docs/knowledge-placement.md`).
- No network access — it never fetches or checks a remote URL.
- No auto-fixing — it only reports; it never rewrites a document or
  creates a missing companion schema file.
- Rule 5's "bare path" check only recognises a `§` suffix as the
  section-marker example the contract itself gives; other conventions
  (e.g. a line-number suffix) wouldn't be caught. Documented, not fixed —
  found during Stage 1.4's independent review and left as a known,
  proportionate limitation rather than over-engineered.
- A `decisions/NNNN-wrong-slug.md` reference (right ADR number, wrong
  filename) is reported the same way as a wholly non-existent ADR number
  — both are "non-existent" by the file-existence test this validator
  actually runs, even though a human would call the former "close."
- **Embedded-front-matter detection (rule 7) cannot distinguish a
  reintroduced documentation schema from an unrelated `---`-delimited
  block used for something else entirely** — e.g.
  `planning/prompts/`'s preserved-prompt provenance headers
  (`id`/`title`/`status`/etc.), which are not schema-bearing documents
  and are not governed. Those files correctly report `FAIL` under this
  rule; that is expected and harmless, not a defect, since nothing treats
  it as one and no CI step validates them. Distinguishing the two cases
  would require guessing at a block's semantic intent, which this
  mechanical validator deliberately does not do.
- A governed/schema-bearing document is now **two files instead of
  one** (`decisions/0006`'s named, accepted cost) — the validator cannot
  reduce this maintenance cost; it can only catch the two failure modes
  that cost is meant to guard against (orphaned schema, reintroduced
  front-matter).

## Status in the broader methodology

Separate from the validator's own limitations above: this validator's
test suite and a check of every governed document now run automatically
on every push/PR (`.github/workflows/deterministic-checks.yml`, jobs
`axiom-validator-tests` and `validate-governed-documentation` — verified
by grep, not assumed). That is enforcement **level 4** ("executed by
CI") per `docs/knowledge-placement.md`'s "Enforcement classes" table —
a red run here is visible, but nothing currently makes it a GitHub
required status check (level 5), which needs repository-admin access
this environment has never had. Native Codex GitHub PR review (a
separate, independent-AI-review piece of the same methodology —
`decisions/0005`) is unrelated to this validator and does not run it.
