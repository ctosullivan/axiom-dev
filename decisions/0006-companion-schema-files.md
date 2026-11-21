# 0006. Move documentation schemas out of embedded front-matter into companion `.schema.yaml` files

## Status

Accepted — 2026-11-21. **Partially superseded by `decisions/0007`**
(the *location* of the companion file — colocated beside its document
here, mirrored under a top-level `schemas/` directory there; this
ADR's decision to use companion files *at all*, rather than embedded
front-matter, is unaffected and remains in force).

## Context

`decisions/0002` left "exact schema sidecar format, or whether Axiom Dev
needs sidecars at all" explicitly **Unresolved**, deferred to Stage 1.1.
Stage 1.1 resolved it in `docs/documentation-schema.md`, choosing
**embedded YAML front-matter** over CodeCompass's separate sidecar-file
convention (`~/projects/codecompass/README.md.schema.yaml`). That
document's own recorded rationale (preserved here verbatim as historical
context, not restated as though it were never true):

> **Why front-matter instead of a sidecar file:** a sidecar is a second
> file that can silently drift out of sync with the document it
> describes — the schema can be edited, or not, independently of the
> content, and nothing forces them to move together. Front-matter lives
> inside the same file, in the same commit, in the same diff hunk
> reviewers already look at. [...] **Trade-off accepted:** front-matter
> requires the document itself to be Markdown-with-YAML-header rather
> than plain Markdown [...]

That trade-off was deliberately accepted at the time and held for three
amendments' worth of real use (Stages 1.1–1.5, the prompt 003 corrective
batch). A fourth authorising prompt
(`planning/prompts/004-documentation-schema-and-roadmap-amendment.md`,
Amendment A) now requires reversing it: every governed document's own
front-matter block, read directly in GitHub or an editor, is validation
metadata a human reader has to scroll past before reaching the actual
explanation — a real, accumulated readability cost the original decision
weighed against drift risk and accepted as the lesser one. Fifteen real
documents now carry this cost in practice (see
`evidence/schema-migration.md` for the exact list), which is a
different, more concrete situation than the zero-documents hypothetical
`docs/documentation-schema.md` was reasoning about when it made the
original trade-off.

## Decision

1. **Documentation schemas move to companion files**, one per governed
   document, at a fully deterministic path: `<document>.md` →
   `<document>.md.schema.yaml`, alongside the document, with no separate
   registry of schema-to-document mappings. `docs/governed-documents.txt`
   continues to name which documents require one.
2. **The drift risk the original decision was built around is accepted
   as real, not dismissed — but addressed differently than "keep them in
   one file."** The companion file sits beside its document in the same
   directory, is committed in the same change by the same
   `AGENTS.md` §5 same-commit-sync rule that already governs every other
   documentation update, and — critically, closing the actual gap a
   sidecar convention opens — the validator now mechanically detects an
   **orphaned schema** (a `.schema.yaml` with no corresponding document)
   and an **accidentally reintroduced embedded front-matter block**
   (silently supporting both conventions indefinitely was explicitly
   ruled out by prompt 004 Amendment C). Drift is not prevented by
   physical proximity anymore; it is caught mechanically instead.
3. **The additional file-maintenance cost is real and is not minimised
   away**: governed documents now have two files instead of one. This is
   the direct, named cost of the readability gain in point 1 — recorded
   here rather than left implicit, per prompt 004 Amendment G's explicit
   request to state "the additional file-maintenance cost," not just the
   benefit.
4. **Deterministic validation's role is unchanged in kind, only in input
   source**: it still only checks structure (fields present, correctly
   typed, non-empty; required headings present; paths/links resolve) —
   never whether the document's prose is factually accurate. Moving the
   schema to its own file does not and cannot close that gap; semantic
   review (`planning/phase-01-foundation.md` §17 Amendment D procedure)
   remains necessary for exactly the same reason it already was —
   structure and truth are independent axes, demonstrated concretely by
   the prompt 003 batch (`evidence/schema-value-assessment.md`) before
   this decision was ever proposed.
5. This ADR **supersedes `docs/documentation-schema.md`'s prior
   front-matter-vs-sidecar resolution**, not `decisions/0002` itself —
   `decisions/0002` only left the question open; it never mandated
   front-matter, so there is nothing in it to reverse. `decisions/0002`'s
   status is annotated to point here for continuity, not edited in
   substance.

## Alternatives considered

- **Keep front-matter, accept the readability cost.** Rejected: this is
  the status quo prompt 004 explicitly asks to change, and the original
  decision's own stated trade-off (readability cost for drift
  resistance) is exactly what no longer looks like the right balance
  once fifteen real documents carry it.
- **Adopt CodeCompass's sidecar convention wholesale, including its
  knowledge-base-ID apparatus.** Rejected per `decisions/0002` point 5,
  unchanged by this ADR — this decision is about schema *location* only,
  not about reopening the claim-ID/knowledge-base question, which stays
  rejected for the same reason it always was (no concrete need, no
  backing store).
- **A schema registry file mapping documents to schema paths.** Rejected:
  prompt 004 explicitly requires the relationship be deterministic from
  the filename alone ("do not require a separate registry") — a registry
  would reintroduce exactly the kind of drift-prone indirection this
  project avoids elsewhere (e.g. the governed-documents manifest is a
  flat list, not a mapping).
- **Support both conventions indefinitely (front-matter OR companion
  file).** Rejected explicitly by prompt 004 Amendment C: "do not
  silently support two competing schema conventions indefinitely." The
  validator detects and fails on a reintroduced front-matter block
  rather than treating it as a quietly-tolerated alternative.

## Rationale

The original front-matter decision was not wrong when made — it was a
reasoned trade-off against a then-hypothetical drift risk, accepted
explicitly and revisited now with real evidence (fifteen real documents,
three completed amendments) rather than overturned on a whim. What
changed is which cost is now better addressed mechanically: drift can be
caught by a validator; embedded metadata cluttering a human-facing
document cannot be un-cluttered by a validator. Separating the two
files lets each constraint be enforced where it's actually checkable.

## Consequences

- Every governed document, and every document that previously carried
  front-matter, gains a sibling `.schema.yaml` file —
  `evidence/schema-migration.md` is the complete, itemised record of
  which files moved and how each was verified.
- `src/axiom_validator/` changes its schema-loading mechanism — this is
  recorded as an authorised contract evolution in
  `contracts/documentation-schema-validator.md`'s new "Contract
  revision" section, not a silent implementation detail.
- The Stage 1.4 checksum-protection convention
  (`evidence/stage-1.4-baseline.md`) is **retired as a live gate** by
  this ADR for the fixtures it covers — those fixtures are migrated to
  the new convention in this same change, which the baseline's own
  governing rule anticipated exactly as its permitted exception: "if the
  refactor needs a fixture or test to change, that's a contract change,
  not an incidental refactor side effect, and needs its own explicit,
  reviewed commit" (`evidence/stage-1.4-baseline.md`). This is that
  commit. `evidence/stage-1.4-baseline.md` itself is not edited — it
  remains the accurate historical record of what Stage 1.4 actually
  verified at the time.
- `docs/documentation-schema.md` is rewritten (not historical narrative;
  a living convention document, like `AGENTS.md`) to describe companion
  files as the current convention — this ADR is where the superseded
  front-matter rationale is preserved, not that document.

## Relevant evidence

- `planning/prompts/004-documentation-schema-and-roadmap-amendment.md`
  §4 (Amendment A, verbatim), §10 (Amendment G, verbatim).
- `docs/documentation-schema.md`'s prior "Convention" section (quoted
  above), superseded by this ADR, rewritten in the same change to
  describe the companion-file convention.
- `evidence/schema-migration.md` (migration report).
- `contracts/documentation-schema-validator.md` (contract revision).
- `decisions/0002` (the originally Unresolved item this closes,
  annotated to point here).

## Supersession

Supersedes `docs/documentation-schema.md`'s prior front-matter
resolution of `decisions/0002`'s Unresolved item (not `decisions/0002`
itself, which made no commitment either way). Does not supersede
`decisions/0001`, `0003`, `0004`, or `0005`.
