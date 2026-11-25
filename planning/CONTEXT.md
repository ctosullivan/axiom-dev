# Session continuity

Keep this concise and current; preserve completed-phase history under
`planning/archive/`, `planning/retros/` and `evidence/`.

## Current phase and status

**Phase 1 — Completed** by owner decision on 2026-11-22 following
[PR #1](https://github.com/ctosullivan/axiom-dev/pull/1).
[PR #2](https://github.com/ctosullivan/axiom-dev/pull/2) merged its
archive and original Phase 2 direction. Historical acceptance limitations
remain in [the qualification record](../evidence/phase-1-owner-acceptance.md).

**Phase 2 — Planned, not in implementation. Stage 2.1 Completed**
(owner decision 2026-11-25, following the merge of
[PR #4](https://github.com/ctosullivan/axiom-dev/pull/4) —
[archive](archive/phase-02-stage-2.1/README.md)). The objective is a
reusable, knowledge-based methodology packaged for independent adoption.
The [roadmap](ROADMAP.md) and [Phase 2 proposal](phase-02-template.md)
put a **real Ledgerkit/hledger vertical slice first**: establish
an independent behavioural oracle (done, Stage 2.1); create only the
evidence-backed comparative knowledge, stable IDs, minimal local
knowledge API and deterministic checks required for that slice
(**Stage 2.2 PR 2a merged into `main`** — `src/axiom_knowledge/`, against
`planning/phase-02-stage-2.2-plan.md` — PR 2b/Ledgerkit adoption not yet
started, separately unauthorised; Stage 2.2 itself not yet marked
Completed); then demonstrate drift, reconciliation and
fresh-session reuse before extracting the template. **No Phase 2 A/B
test of the template.** PR 2b has also just been **redefined**: the
repository owner decided to retire CodeCompass (Ledgerkit's prior
dependency/code-comprehension tool) entirely as part of adopting
Axiom, rather than installing Axiom alongside it — see
`planning/phase-02-stage-2.2-plan.md` §9 and
`planning/phase-02-ledgerkit-codecompass-migration-handoff.md`.

**Phase 3 — Proposed:** deliver a thin MCP adapter over Phase 2's API
(required Phase 3 deliverable under ADR 0008, but optional for
consumers) and investigate specific agent/retrieval strategy
hypotheses using Axiom Assure when ready. MCP is not a Phase 2
dependency or the project's purpose.

## Current focus and constraints

- [PR #4](https://github.com/ctosullivan/axiom-dev/pull/4) (Stage 2.1
  planning/evidence, the `ci-required` CI gate, and
  `AGENTS.md` §14's bounded corrective cycle) merged into `main` on
  2026-11-22 by the repository owner.
  [PR #5](https://github.com/ctosullivan/axiom-dev/pull/5) (Stage 2.1
  closeout, Stage 2.2 planning, Apache 2.0 relicensing) merged into
  `main` (merge commit `d144aba`) on 2026-11-25 by the repository
  owner, after a clean final native Codex review and green CI at its
  merged head (`810b87a`).
  [PR #6](https://github.com/ctosullivan/axiom-dev/pull/6) (Stage 2.2
  PR 2a, `src/axiom_knowledge/`), originally a stacked PR on PR #5's own
  branch, was retargeted to `main` once PR #5 merged and itself merged
  into `main` (merge commit `1dbb0ab`) on 2026-11-25 by the repository
  owner, after CI passed at its head (`1cfc3ef`) and an explicitly
  authorised, narrowly scoped 4th corrective round against native Codex
  review returned no further material findings. A small
  [PR #7](https://github.com/ctosullivan/axiom-dev/pull/7) recording
  these two merges in this file and `ROADMAP.md` was opened but is
  **superseded by this round's own CodeCompass-retirement planning
  amendment PR**, whose CONTEXT.md/ROADMAP.md changes carry the same
  content plus the new amendment — close PR #7 without merging once
  this round's PR is confirmed, rather than merging both. Inspect
  actual HEAD and PR state rather than trusting this text.
- PR #5 (merged): (1) marks **Stage 2.1 Completed** and archives it
  (`planning/archive/phase-02-stage-2.1/README.md`) without moving or
  duplicating its canonical plan/evidence — the cross-cutting designs
  (`planning/phase-02-adoption-design.md`,
  `planning/phase-02-knowledge-api-design.md`,
  `planning/phase-02-measurement-design.md`) remain active, unarchived,
  needed by Stage 2.2 onward; (2) adds the **Stage 2.2 plan**
  (`planning/phase-02-stage-2.2-plan.md`), since corrected once more:
  a two-PR split (Axiom Dev's reusable `get`/`find` library,
  Ledgerkit's adoption of the skill/wiki/config), reusing the
  already-reviewed cross-cutting designs rather than duplicating
  them, now with a named `--repo-root`-discovery mechanism, a
  positive `derived.status: VERIFIED` demonstration and a contrasting
  `UNCERTAIN` one using **four real, already-existing**
  `dev-docs/compat-register/` claims (not an illustrative 10–20-claim
  quota), clarified logging/hook scope for Stage 2.2 specifically, and
  explicit Python-version/licence boundaries between Axiom Dev
  (Apache 2.0) and Ledgerkit (`GPL-3.0-or-later`, confirmed
  unaffected); (3) **relicenses to Apache 2.0**
  (`decisions/0009-apache-2.0-licensing.md`, `LICENSE`, `NOTICE`),
  preserving the existing copyright holder and year.
- PR #6 (merged, Stage 2.2 PR 2a BUILD, authorised directly by the
  repository owner, including one exceptional 4th corrective round):
  implements `src/axiom_knowledge/` -- the `get`/`find` library, the
  Ledgerkit native-register adapter, the scope-manifest gate,
  repository/register discovery, the CLI and `knowledge_find`'s
  result-count/returned-claim-ID telemetry, all against synthetic
  fixtures, **no live Ledgerkit checkout touched**. 85 new deterministic
  tests (173 total with `axiom_validator`'s own suite), all passing; see
  `CHANGELOG.md`'s "Stage 2.2 PR 2a" entry for the full list.
- **PR 2b is redefined, this round (`planning/phase-02-stage-2.2-plan.md`
  §9):** the repository owner decided to retire CodeCompass entirely
  from Ledgerkit as part of adopting Axiom, not alongside it. Axiom
  Dev performed an isolated scratch-clone feasibility evaluation
  against Ledgerkit's real `dev-docs/compat-register/` (never the real
  checkout, confirmed unmodified afterward) and produced a precise
  removal/adoption specification and a self-contained handoff for
  Ledgerkit's own orchestrator:
  `planning/phase-02-ledgerkit-codecompass-migration-handoff.md`.
  PR 2b itself has **not** started -- it remains separately
  unauthorised. **Stage 2.2 is not marked Completed.**
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

**Next action:** both PR #5 (closeout/planning/licensing, merge commit
`d144aba`) and PR #6 (Stage 2.2 PR 2a, merge commit `1dbb0ab`) are
merged into `main`, by explicit repository-owner authorisation, after
final verification of latest-head CI and Codex-review disposition on
each. Local `main` is fast-forwarded to `1dbb0ab` and the full
deterministic test suite (173 tests) and governed-document validator
(13/13 PASS) pass against it. `planning/ROADMAP.md` already states
Stage 2.1 Completed and this file already reflects it — per the prior
round's own explicit authorisation, naming the specific merged PR (#4)
and the explicit instruction to mark the status, which together
constitute the recorded evidence of owner acceptance
(`docs/phase-archiving.md`'s phase-completion procedure, applied at
stage granularity for the first time). **Stage 2.2 itself is not
marked Completed**, and **PR 2b (Ledgerkit, now redefined to include
CodeCompass's full retirement, §9) remains unauthorised and
unstarted**, per `planning/phase-02-stage-2.2-plan.md` §8 — both
require separate, explicit owner authorisation. The Ledgerkit
migration handoff
(`planning/phase-02-ledgerkit-codecompass-migration-handoff.md`) is a
specification for Ledgerkit's own orchestrator to pick up under that
separate authorisation, not an authorisation itself. No PR 2a
functionality, and no CodeCompass removal, has been applied to
Ledgerkit's real checkout.
