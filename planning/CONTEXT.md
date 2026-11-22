# Session continuity

Keep this concise and current; preserve completed-phase history under
`planning/archive/`, `planning/retros/` and `evidence/`.

## Current phase and status

**Phase 1 — Completed** by owner decision on 2026-11-22 following
[PR #1](https://github.com/ctosullivan/axiom-dev/pull/1).
[PR #2](https://github.com/ctosullivan/axiom-dev/pull/2) merged its
archive and original Phase 2 direction. Historical acceptance limitations
remain in [the qualification record](../evidence/phase-1-owner-acceptance.md).

**Phase 2 — Planned, not in implementation.** The objective is a
reusable, knowledge-based methodology packaged for independent adoption.
The [roadmap](ROADMAP.md) and [Phase 2 proposal](phase-02-template.md)
now put a **real Ledgerkit/hledger vertical slice first**: establish
an independent behavioural oracle; create only the evidence-backed
comparative knowledge, stable IDs, minimal local knowledge API and
deterministic checks required for that slice; then demonstrate drift,
reconciliation and fresh-session reuse before extracting the template.
**No Phase 2 A/B test of the template.**

**Phase 3 — Proposed:** deliver a thin MCP adapter over Phase 2's API
(required Phase 3 deliverable under ADR 0008, but optional for
consumers) and investigate specific agent/retrieval strategy
hypotheses using Axiom Assure when ready. MCP is not a Phase 2
dependency or the project's purpose.

## Current focus and constraints

- Current documentation amendment branch:
  `docs/phase-2-evidence-first-vertical-slice`, based on `main`.
  Inspect actual HEAD and PR state rather than trusting this text.
- Review [this refinement plan](phase-02-roadmap-refinement.md),
  [Phase 2 proposal](phase-02-template.md), and the current roadmap
  for evidence/semantic consistency before owner-approved merge.
- Phase 2's wiki, knowledge API, identity/drift gate and template
  **do not yet exist**; do not imply they have been implemented.
- The core should be Git/files plus a small read-only local API
  (`get`, `find`, `related`, `impacted`) and deterministic CI,
  with independently reviewed semantic verification. Do not build a
  graph database, hosted service, automatic claim generator or
  autonomous reconciliation without observed need.
- A claim may be VERIFIED only for a scoped, independently checked
  contract/oracle. Changed source means possible impact, not proven
  semantic invalidity; green schema/CI alone does not prove truth.
- Preserve Phase 1 open qualifications and triage its documented
  validator path/link edge cases in Phase 2 plans.
- Track meaningful knowledge reuse, real defects caught/missed,
  drift false positives, overhead and adoption cost. A/B work is
  reserved for Phase 3 and cannot be inferred from Phase 2 dogfooding.

## Relevant decisions and next action

`decisions/0001`–`0007` describe the foundation;
[ADR 0008](../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md)
sets the accepted Phase 2/3 direction. This roadmap refinement changes
**sequencing and proposed scope, not the accepted architectural decision**.

**Next action:** independent review and CI inspection of this
documentation PR, followed by explicit human approval to merge.
Then **inspect the actual Ledgerkit/hledger baseline and prepare a
Stage 2.1 contract and independent oracle before any API coding**.
