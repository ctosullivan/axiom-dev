# 0008. Template-first development, stable knowledge identity, and deferred experimentation

## Status

Accepted — direction authorised by repository owner on 2026-11-22;
implementation and interface contracts remain subject to Phase 2 review.

## Context

Phase 1 established a conventional, evidence-based development lifecycle.
The earlier roadmap placed a comparative real-world trial before a reusable
template. The owner now prefers to prove usefulness through application
to an independent codebase, such as Ledgerkit, **without** A/B testing
the template. Axiom Assure's experimental apparatus is not yet mature
enough to justify coupling it to the first reusable template.

## Decision

1. Phase 2 designs and delivers a reusable, low-dependency package or
   template that supports the full UNDERSTAND → SPECIFY → ASSESS IMPACT →
   BUILD → VERIFY → RECONCILE lifecycle in an independent repository.
   Ledgerkit is the initial dogfood candidate, not a built-in dependency.
2. Phase 2 includes a comparative Ledgerkit/hledger semantic wiki
   backed by traceable claims, explicit equivalence/divergence/unknown
   states, evidence, and reproducible tests or examples.
3. Phase 2 **requires a usable, local, deterministic knowledge API**.
   It is not postponed until MCP. MCP is one possible adapter over
   this API, introduced in Phase 3.
4. Each governed knowledge claim and artifact receives a globally
   unambiguous, persistent identifier independent of title/path.
   Version/revision and lifecycle state are separate from identity.
   References, provenance, dependencies, evidence, and replacement
   relationships are machine-readable. Renames do not mint new IDs.
5. Phase 2 introduces deterministic, independently testable CI checks
   for identity uniqueness, schema validity, link/reference integrity,
   provenance and source-change impact, plus explicit stale/unknown/
   contested states. CI must reject defined mechanical violations and
   flag potential semantic drift for review; it must not claim to
   mechanically prove semantic truth. Required-merge enforcement and
   CI-execution status must be reported separately.
6. Phase 2 demonstrates value through Ledgerkit dogfooding and a
   documented, reproducible case study with defects, friction, cost
   and limitations; **no A/B test of the template is required or
   represented as having been performed**.
7. Phase 3 builds an optional MCP adapter over the stable knowledge API
   and conducts controlled A/B experiments on specified **agent or
   retrieval strategies**, using Axiom Assure when its harness is
   sufficiently mature. The experiment does not retroactively become a
   Phase 2 template A/B test. Phase 3 does not make the Phase 2 package
   depend on MCP, an LLM, or Assure.

## Alternatives considered

- **A/B test the template in Phase 2.** Rejected as an unnecessary
  blocker to producing and dogfooding a useful, conventional package.
  The evidence still must be honest about attribution and limitations.
- **Defer the knowledge API until MCP.** Rejected because identifiers,
  references, impact queries, and CI need a stable machine interface
  before any model-facing protocol is introduced.
- **Make Assure, MCP or a database server part of the core template.**
  Rejected for avoidable installation and operational overhead. An
  optional adapter can follow when the use case is demonstrated.
- **Treat every changed source as proof of semantic drift.** Rejected:
  deterministic detection of affected references is possible, but
  assessing the meaning of a change requires review and new evidence.

## Rationale

Separating a small working knowledge substrate from optional agent
interfaces and experimental comparisons makes adoption and dogfooding
possible sooner. Stable claim identity and transparent drift detection
are the foundation for both reliable documentation and later,
reproducible experiments.

## Consequences

- Phase 2 is now template-first and unambiguously non-A/B.
- Ledgerkit/hledger semantic mapping, stable IDs, knowledge API,
  deterministic CI gating and repeated real-use exercises are Phase 2
  acceptance concerns, not optional embellishments.
- Exact storage, ID syntax, API transport, drift-policy severity and
  experimental design await focused contracts and independent review.
- Any claimed efficiency advantage over other development methods
  remains unproven until separately tested.

## Relevant evidence

- `planning/phase-01-foundation.md` and
  `evidence/phase-1-final-closeout.md` (Phase 1 baseline and limits).
- `planning/phase-02-template.md` (proposed implementation plan).
- Repository owner direction dated 2026-11-22 (this roadmap transition).
