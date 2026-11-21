---
audience: contributors and agents writing or validating Axiom Dev documentation
purpose: define the declarative schema convention every important document uses, and how it's checked
required_sections: [Convention, Required fields, Worked example, Manual validation record]
authoritative_sources: [decisions/0002, decisions/0004]
acceptance_criteria:
  - the convention is simpler than CodeCompass's separate-sidecar-file approach, with the simplification reasoned, not just asserted
  - at least one real Axiom Dev document has been checked against this schema by hand
---

# Documentation schema

Resolves the open item in `decisions/0002` ("exact schema sidecar format,
or whether Axiom Dev needs sidecars at all"): Axiom Dev does not use
separate sidecar files.

## Convention

Each document that needs a declarative schema carries a **YAML front-matter
block** at the top of the file itself — not a separate `<doc>.md.schema.yaml`
file alongside it, which is what CodeCompass did
(`~/projects/codecompass/README.md.schema.yaml`).

**Why front-matter instead of a sidecar file:** a sidecar is a second file
that can silently drift out of sync with the document it describes — the
schema can be edited, or not, independently of the content, and nothing
forces them to move together. Front-matter lives inside the same file, in
the same commit, in the same diff hunk reviewers already look at. This is
a direct application of Amendment A ("each required artifact has one
clear purpose") and Amendment A's broader goal of minimising procedural
overhead: one file to maintain per document, not two.

**Trade-off accepted:** front-matter requires the document itself to be
Markdown-with-YAML-header rather than plain Markdown, and a strict
sidecar-based toolchain (if one existed) couldn't validate a schema
without parsing the host document. Neither cost applies here — Stage 1.4's
validator is being built for this exact format, not adopted from
elsewhere.

**Not every document needs this.** Only documents whose audience,
required content, or acceptance criteria are non-obvious benefit from
declaring them — a short file like `CHANGELOG.md` does not need a schema
header; `docs/knowledge-placement.md` and this file do, because getting
their scope wrong would be easy to miss in review.

## Required fields

```yaml
---
audience: who this document is for
purpose: one sentence — why this document exists
required_sections: [list of heading names that must appear]
authoritative_sources: [files this document must stay consistent with]
acceptance_criteria:
  - a list of checkable statements; at least one should be checkable by a person today and by Stage 1.4's validator later
---
```

- `audience` and `purpose`: free text, one line each.
- `required_sections`: exact heading text (without the `#`) that must
  appear in the document body. This is the first thing Stage 1.4's
  validator checks — it is deliberately the simplest possible mechanical
  check (§"Enforcement classes" in `docs/knowledge-placement.md`).
- `authoritative_sources`: other files whose claims this document must not
  contradict. Not mechanically checked yet (that would require
  understanding meaning, not just structure) — this is a semantic/editorial
  item for now, surfaced in review, not blocked automatically.
- `acceptance_criteria`: what "this document is in good shape" means,
  stated so a reader (human or validator) can check it without having to
  infer intent.

## Worked example

`README.md` was fitted with this schema as the first real example:

```yaml
---
audience: new contributors, agents resuming work, and anyone evaluating the project
purpose: orient a reader to what Axiom Dev is, its current status, and where to find governing detail
required_sections: [Mission, Fundamental hypothesis, Development methodology, Repository map, Licence]
authoritative_sources: [AGENTS.md, planning/ROADMAP.md, planning/CONTEXT.md]
acceptance_criteria:
  - every stage status claim matches planning/ROADMAP.md at time of reading
  - the repository map lists every top-level governance file and planning directory that actually exists
---
```

This front-matter was added to `README.md` itself (see that file) rather
than duplicated only here, per the convention above.

## Manual validation record

Checked by hand on 2026-11-21 (no validator exists yet — that's Stage
1.4): `README.md` against its own front-matter schema above.

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
