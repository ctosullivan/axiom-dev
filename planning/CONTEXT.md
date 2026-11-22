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

- `docs/phase-2-evidence-first-vertical-slice` (PR #3) merged on
  2026-11-22. **Current branch:**
  `planning/phase-2-stage-2.1-ledgerkit-oracle`, based on `main` at
  `53d818b`. Inspect actual HEAD and PR state rather than trusting
  this text.
- This branch makes Stage 2.1 and Phase 2's cross-cutting designs
  implementation-ready: `planning/phase-02-stage-2.1-plan.md` (task,
  oracle, fixtures), `planning/phase-02-adoption-design.md` (skill,
  file layout), `planning/phase-02-knowledge-api-design.md` (claim
  model, API, and — found missing by independent review and now fixed
  — the adapter contract for reading Ledgerkit's own existing
  compat-register rather than duplicating it),
  `planning/phase-02-measurement-design.md` (logging/telemetry),
  `planning/phase-02-architecture.md` (diagram), and
  `planning/phase-02-planning-review.md` (full independent review: 2
  BLOCKING findings, both fixed in this same batch). **This is still
  a plan, not an implementation** — no skill, API, wiki entry, CI
  check or logger has been built.
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

**Next action:** human review and approval of this planning-only PR
(Stage 2.1 plan, four cross-cutting designs, independent review). Only
after approval does Stage 2.1 BUILD work start — reproducing Ledgerkit's
EC-022 fixture matrix and implementing the fix in `_parse_posting`
(`planning/phase-02-stage-2.1-plan.md` §3, §7). No implementation
begins before that approval, per `AGENTS.md` §11.
