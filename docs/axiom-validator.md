---
audience: anyone running the validator, extending it, or trying to understand what it does and why
purpose: human-facing explanation of the knowledge/documentation validator — what it does, how it's built, how to run it
required_sections: [Purpose, Architecture, Usage, Limitations]
authoritative_sources: [contracts/documentation-schema-validator.md, src/axiom_validator/__init__.py]
acceptance_criteria:
  - describes current, actually-built behaviour, not aspirational behaviour
  - architecture section matches the real module split in src/axiom_validator/
---

# Axiom Dev documentation/knowledge validator

This document was written after the validator existed and was refactored
— found missing during Stage 1.4→1.5 reconciliation (a real knowledge-placement
gap: the validator had a contract and evidence records, but no
human-facing `docs/` explanation, which `AGENTS.md` §7's placement table
calls for). It is deliberately written from the outside, describing what
the component does and how it's built, not restating the contract's rule
text verbatim.

## Purpose

Checks a Markdown document's YAML front-matter (the schema convention in
`docs/documentation-schema.md`) against its own declared requirements:
are the required sections actually present, do the sources it claims to
be consistent with actually exist, do its body links resolve. It's a
mechanical check — it can tell you a required heading is missing; it
can't tell you the document is well-written. See
`docs/knowledge-placement.md` "Enforcement classes" for that distinction.

This is Axiom Dev's first real software component (`planning/prompts/001-...md`
§5 named it as the first substantive piece to build). Its exact required
behaviour is fixed in `contracts/documentation-schema-validator.md`,
written and accepted before any of this code existed.

## Architecture

`src/axiom_validator/` is a small package, split (via a Stage 1.4
behaviour-preserving refactor — `evidence/stage-1.4-refactor.md`) into:

- **`parsing.py`** — turns a document's raw text into usable pieces:
  splits off the YAML front-matter block, parses it, extracts the set of
  headings actually present (excluding anything inside a fenced code
  block), and extracts the Markdown links in the body (excluding inline
  code spans). No rule logic lives here — just "what's in this text."
- **`rules.py`** — the actual checks, each a small function taking
  already-parsed data and returning a list of error strings: required
  fields, required sections, authoritative-source paths (including the
  repository-containment check — a path can't escape the repo via `../`
  even if something happens to exist there), and body links (same
  containment rule, plus ADR-specific error messages for
  `decisions/NNNN-*.md` references). No file-reading or Markdown parsing
  lives here — just "is this correct, given these parsed facts."
- **`reporting.py`** — turns a result into the dict shape
  (`file`/`result`/`errors`) everything else expects, and formats a batch
  for the CLI.
- **`__init__.py`** — the one place that calls the other three in order:
  parse, then check required fields (short-circuits on failure), then
  sections/sources/links, then report. This is also where `validate_file`
  and `main` live — the two names tests and the CLI actually import.
- **`__main__.py`** — lets `python3 -m axiom_validator <files>` work.

Why split it this way: parsing, rule-checking, and reporting are
genuinely separable concerns — you can change how a link is reported
without touching how it's detected, or add a new rule without touching
how front-matter is parsed. The pre-refactor version had all three
tangled into one function; the split is verified behaviour-preserving
(`evidence/stage-1.4-refactor.md`), not just reorganised for its own
sake.

## Usage

```
PYTHONPATH=src python3 -m axiom_validator <file1.md> [file2.md ...] --repo-root .
```

Exits `0` if every file is `PASS` or `SKIPPED` (no front-matter — nothing
to check), `1` if any is `FAIL` or `INVALID_SCHEMA`. Requires PyYAML
(`requirements.txt`).

To validate a document programmatically:

```python
from pathlib import Path
from axiom_validator import validate_file

result = validate_file(Path("README.md"), Path("."))
# {"file": "README.md", "result": "PASS", "errors": []}
```

## Limitations

- No enforcement of which documents must carry a schema — an unschema'd
  document is `SKIPPED`, not flagged.
- Does not check whether `acceptance_criteria` statements are actually
  true, or whether `authoritative_sources` entries are genuinely
  consistent with the document's claims — both are semantic/editorial
  concerns out of scope for a mechanical check
  (`docs/knowledge-placement.md`).
- Rule 5's "bare path" check only recognises a `§` suffix as the
  section-marker example the contract itself gives; other conventions
  (e.g. a line-number suffix) wouldn't be caught. Documented, not fixed —
  found during Stage 1.4's independent review and left as a known,
  proportionate limitation rather than over-engineered.
- A `decisions/NNNN-wrong-slug.md` reference (right ADR number, wrong
  filename) is reported the same way as a wholly non-existent ADR number
  — both are "non-existent" by the file-existence test this validator
  actually runs, even though a human would call the former "close."
- No CI integration of its own yet — Stage 1.3's Codex gate and this
  validator are separate pieces of the methodology; nothing currently
  wires this validator into `.github/workflows/` to run automatically on
  every PR. That would be a reasonable future Stage 1.x addition, not
  something this document should claim already exists.
