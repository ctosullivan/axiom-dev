# 0002. Canonical knowledge and documentation architecture

## Status

Accepted (partial — see Unresolved) — 2026-11-21

## Context

The bootstrap prompt (`planning/prompts/001-phase-1-bootstrap.md` §5)
requires a canonical knowledge model distinguishing INTENDED, OBSERVED,
VERIFIED, UNCERTAIN and CONTESTED behaviour, a lightweight documentation
schema, a knowledge placement policy, and a note that none of this should
recreate CodeCompass's full record hierarchy without demonstrated need.

CodeCompass's relevant precedent:

- `docs/concepts/knowledge-placement-policy.md` and
  `decisions/0094-knowledge-placement-policy-and-review.md` define
  placement as a small fixed table mapping knowledge categories onto
  already-existing artifacts (code, docstrings, ADRs, contracts, evidence,
  docs), with three enforcement classes — mechanical, behavioural, and
  semantic/editorial — where only the first two ever block a change.
  `decisions/0094` also states a "no synthetic substitute" rule: a
  real-dogfood exit gate cannot be satisfied by a constructed fixture; an
  unmet gate must be reported unmet.
- CodeCompass backs its schema-driven docs with declarative schema sidecar
  files (e.g. `README.md.schema.yaml`,
  `docs/concepts/knowledge-model.md.schema.yaml`) naming audience, purpose,
  required topics, relevant canonical knowledge, and acceptance criteria
  per document.
- `decisions/0094` itself records that two originally-designed mechanical
  checks (a docstring-contradicted-by-oracle-result check and a
  decision-citation-status-mismatch check) were designed in detail and then
  explicitly deferred/never shipped — a concrete, admitted example of
  designed-but-unimplemented capability, cited here because Axiom Dev must
  not repeat the pattern of describing such a check as if it already runs.
- CodeCompass's schema sidecars additionally reference a knowledge-base ID
  apparatus (e.g. claim IDs like `CL-CTXT-005`, claim-status gating) that
  presumes a working knowledge API/store behind it.

## Decision

1. Canonical knowledge is Git-versioned Markdown and YAML — no database,
   no graph store, no custom compiler, for Phase 1.
2. The five-state classification (INTENDED / OBSERVED / VERIFIED /
   UNCERTAIN / CONTESTED) is adopted as Axiom Dev's vocabulary for
   describing the status of any claim about the system, and must not be
   collapsed into a single confidence score anywhere it is used.
3. Knowledge placement for Stage 1.0 is the fixed table already recorded in
   `AGENTS.md` §7 (source code / docstrings / comments / ADRs / contracts /
   evidence / docs), adopting CodeCompass's category-to-artifact mapping
   but not its enforcement machinery yet.
4. The full lightweight documentation schema (schema sidecars, required
   topics, acceptance criteria per document, and a Python validator for
   them) is **deferred to Stage 1.1**, per the bootstrap prompt's explicit
   instruction not to implement a documentation compiler during bootstrap.
   This ADR records the *intent* to build it; it is not itself the schema
   design.
5. Axiom Dev will not adopt a knowledge-base-ID apparatus (claim IDs,
   claim-status gating) until Stage 1.1 or later demonstrates a concrete
   need for one backed by an actual store — CodeCompass's version presumes
   infrastructure Axiom Dev does not have at bootstrap.

## Alternatives considered

- **Build the full schema/validator now, during bootstrap.** Rejected:
  explicitly out of scope per the bootstrap prompt ("do not implement a
  custom documentation compiler during bootstrap"); also nothing exists
  yet for a schema to validate against.
- **Skip the placement table until Stage 1.1.** Rejected: Stage 1.0 already
  produces documents (ADRs, plans, `README.md`, etc.) that need a placement
  rule now, even an informal one, so contributors aren't guessing where new
  facts belong while they write the very first files.
- **Adopt CodeCompass's claim-ID/knowledge-base apparatus wholesale.**
  Rejected per the rationale in point 5 above and per the bootstrap
  prompt's instruction not to recreate CodeCompass's record hierarchy
  without demonstrated requirement.

## Rationale

The placement table and five-state vocabulary are cheap to state and
immediately useful; the schema/validator and any ID-based knowledge-base
apparatus are expensive and premature without a concrete document corpus
or implementation to validate against. Deferring the latter to Stage 1.1,
explicitly, avoids the common failure CodeCompass's own ADR 0094 documents
— designing enforcement machinery in detail and then never shipping it
while continuing to describe it as part of the system.

## Consequences

- Until Stage 1.1, documentation in this repository has no mechanical
  schema enforcement — only the informal placement table and ordinary
  review. This is an accepted, named gap, not a silent one.
- Stage 1.1's plan must explicitly design: the schema sidecar format (or a
  simpler alternative), what "required topics" means for Axiom Dev's own
  document set, and the validator's scope — and must avoid reintroducing
  CodeCompass's ID/claim-status apparatus without justifying it fresh.
- Any future ADR that proposes the claim-ID apparatus must address why the
  simpler placement table in this ADR is no longer sufficient.

## Relevant evidence

- `~/projects/codecompass/docs/concepts/knowledge-placement-policy.md`.
- `~/projects/codecompass/decisions/0094-knowledge-placement-policy-and-review.md`
  (placement table, enforcement classes, "no synthetic substitute" rule,
  and the admitted deferred/unshipped mechanical checks).
- `~/projects/codecompass/README.md.schema.yaml`,
  `~/projects/codecompass/docs/concepts/knowledge-model.md.schema.yaml`
  (schema sidecar format and claim-ID apparatus referenced in Decision
  point 5).
- `planning/prompts/001-phase-1-bootstrap.md` §5 (knowledge architecture
  requirements and the instruction not to build a documentation compiler
  during bootstrap).

## Unresolved

- Exact schema sidecar format (or whether Axiom Dev needs sidecars at all
  versus a simpler convention) — left open for Stage 1.1's plan.
- Validator design and scope — left open for Stage 1.1/1.4 (the validator
  is slated as the first substantive Axiom Dev component).
- Whether/when a knowledge-base-ID apparatus becomes justified — left open,
  no timeline committed.

## Supersession

None. This is the second ADR; it may be partially superseded by a Stage 1.1
ADR once the schema and validator are actually designed.
