# Documentation schema

Resolves the open item in `decisions/0002` ("exact schema sidecar format,
or whether Axiom Dev needs sidecars at all"): Axiom Dev uses a companion
`.schema.yaml` file per document — a sidecar convention, reversing
Stage 1.1's original choice. **This is the current policy; it is not
the first answer this project gave to that question.** Stage 1.1
originally resolved the same open item against sidecars, in favour of
embedded YAML front-matter; `decisions/0006` reversed that choice once
real use across fifteen documents showed the readability cost was worse
in practice than the drift risk it was meant to avoid. The original
front-matter rationale is preserved there, not here, since this
document describes current policy, not history.

## Convention

Each document that needs a declarative schema has a companion file at a
fully deterministic path: `<document>.md` → `<document>.md.schema.yaml`,
in the same directory, with no separate registry mapping one to the
other.

**Why a companion file instead of embedded front-matter (reversing the
original choice):** fifteen real governed/schema-bearing documents
accumulated embedded YAML blocks a human reader had to scroll past
before reaching the actual explanation — a real, concrete readability
cost, not a hypothetical one, once there was real content to weigh it
against. A companion file keeps the Markdown document as plain,
cleanly-rendering Markdown.

**The drift risk the original choice was built around is real, and is
not dismissed — it's addressed mechanically instead of by physical
proximity.** `src/axiom_validator/` detects two failure modes a sidecar
convention would otherwise risk going unnoticed: an **orphaned schema**
(a `.schema.yaml` file with no corresponding document — contract
revision rule 8) and an **accidentally reintroduced embedded
front-matter block** (contract revision rule 7 — the validator never
silently falls back to parsing it, and never supports both conventions
side by side). Same-commit-sync (`AGENTS.md` §5) still applies to the
companion file exactly as it did to front-matter: both files change
together, in the same change, by the same rule.

**Cost accepted, stated plainly:** a governed document is now two files
instead of one. This is the direct, named cost of the readability gain
above — see `decisions/0006`'s own Decision point 3.

**Not every document needs this.** Only documents whose audience,
required content, or acceptance criteria are non-obvious benefit from
declaring them — a short file like `CHANGELOG.md` does not need a
schema; `docs/knowledge-placement.md` and this file do, because getting
their scope wrong would be easy to miss in review.

## Required fields

A companion schema file is plain YAML — no `---` delimiters, since there
is no host document to delimit the block from:

```yaml
audience: who this document is for
purpose: one sentence — why this document exists
required_sections: [list of heading names that must appear]
authoritative_sources: [files this document must stay consistent with]
acceptance_criteria:
  - a list of checkable statements; at least one should be checkable by a person today and by the validator
```

- `audience` and `purpose`: free text, one line each; must be non-empty
  (`contracts/documentation-schema-validator.md` rule 10).
- `required_sections`: exact heading text (without the `#`) that must
  appear in the document body; must be a non-empty list of strings
  (rules 4, 11, 12) — this is deliberately the simplest possible
  mechanical check (§"Enforcement classes" in
  `docs/knowledge-placement.md`).
- `authoritative_sources`: other files whose claims this document must
  not contradict; a list of strings, may legitimately be empty (rule
  14). Path resolution is mechanically checked (rule 5); whether the
  document's claims are actually *consistent* with those sources is not
  — that remains a semantic/editorial item, surfaced in review, not
  blocked automatically.
- `acceptance_criteria`: what "this document is in good shape" means,
  stated so a reader (human or an independent reviewer) can check it
  without having to infer intent; must be a non-empty list of non-empty
  strings (rule 13).

## Worked example

`README.md` was fitted with this schema as the first real example —
originally as embedded front-matter (Stage 1.1), migrated to a companion
file by this same change (`evidence/schema-migration.md`):

`README.md`:

```markdown
# Axiom Dev

Axiom Dev is the primary product of the Axiom project...
```

`README.md.schema.yaml`:

```yaml
audience: new contributors, agents resuming work, and anyone evaluating the project
purpose: orient a reader to what Axiom Dev is, its current status, and where to find governing detail
required_sections: [Mission, Fundamental hypothesis, Development methodology, Repository map, Licence]
authoritative_sources: [AGENTS.md, planning/ROADMAP.md, planning/CONTEXT.md]
acceptance_criteria:
  - every stage status claim matches planning/ROADMAP.md at time of reading
  - the repository map lists every top-level governance file and planning directory that actually exists
```

## Manual validation record

**Historical record, from Stage 1.1 — performed under the
since-superseded embedded-front-matter convention, preserved as written
rather than restated as though it always described companion files.**
Checked by hand on 2026-11-21 (no validator existed yet — that's Stage
1.4): `README.md` against its own front-matter schema (then embedded,
now migrated to `README.md.schema.yaml` with identical substantive
content).

- `required_sections`: all five present as written (`Mission`,
  `Fundamental hypothesis`, `Development methodology`, `Repository map`,
  `Licence` — checked exact heading text, case included).
- `acceptance_criteria` item 1: the repository-map table's status line
  matched `planning/ROADMAP.md` at the time of this check (both describe
  Stage 1.0 as in progress, Stage 1.1 as in progress since this change).
- `acceptance_criteria` item 2: repository-map table entries were
  cross-checked against `ls` output. The first pass of this check
  (recorded here honestly rather than silently corrected) missed
  `.github/pull_request_template.md`, a real, existing governance file —
  an independent review of this batch caught the gap. Fixed in the same
  change: the row is now in README.md's table, and this record says so
  rather than claiming the original check was already complete.

This is the "manual validation of at least one real document" acceptance
criterion for Stage 1.1 (`planning/phase-01-foundation.md` §4, Stage 1.1).
Logged in `evidence/phase-1-log.md`.
