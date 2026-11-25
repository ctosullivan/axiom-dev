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
(**Stage 2.2 PR 2a BUILD underway** — `src/axiom_knowledge/`, against
`planning/phase-02-stage-2.2-plan.md` — PR 2b/Ledgerkit adoption not yet
started, gated on 2a merging); then demonstrate drift, reconciliation and
fresh-session reuse before extracting the template. **No Phase 2 A/B
test of the template.**

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
  closeout, Stage 2.2 planning, Apache 2.0 relicensing) remains **open**,
  CI green, native Codex review clean. **Current branch:**
  `phase-2/stage-2.2-pr2a-knowledge-library`, stacked on top of PR #5's
  own branch (`phase-2/stage-2.1-closeout-and-licensing`) — per PR #5
  not yet being merged, this is a clearly identified stacked PR, not a
  branch from `main`. Inspect actual HEAD and PR state rather than
  trusting this text.
- PR #5's branch: (1) marks **Stage 2.1 Completed** and archives it
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
- This stacked branch (PR 2a, Stage 2.2 BUILD, authorised directly by
  the repository owner): implements `src/axiom_knowledge/` -- the
  `get`/`find` library, the Ledgerkit native-register adapter, the
  scope-manifest gate, repository/register discovery and the CLI, all
  against synthetic fixtures, **no live Ledgerkit checkout touched**.
  75 new deterministic tests, all passing; see `CHANGELOG.md`'s "Stage
  2.2 PR 2a" entry for the full list. PR 2b (Ledgerkit adoption) has
  **not** started -- it depends on this PR merging first, which itself
  depends on PR #5 merging first. **Stage 2.2 is not marked
  Completed.**
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

**Next action:** human review and approval of two open PRs: #5
(closeout/planning/licensing, unmerged) and the new stacked PR 2a
(`phase-2/stage-2.2-pr2a-knowledge-library`, this implementation).
`planning/ROADMAP.md` already states Stage 2.1 Completed and this file
already reflects it — per the prior round's own explicit authorisation,
naming the specific merged PR (#4) and the explicit instruction to mark
the status, which together constitute the recorded evidence of owner
acceptance (`docs/phase-archiving.md`'s phase-completion procedure,
applied at stage granularity for the first time). **PR 2a's own BUILD
was explicitly authorised directly by the repository owner** (a
separate prompt from PR #5's own authorisation) and is implemented on
this stacked branch; PR 2b (Ledgerkit adoption) remains unauthorised and
unstarted, gated on 2a merging, per
`planning/phase-02-stage-2.2-plan.md` §8. Neither open PR is merged; no
PR 2a functionality has been copied into Ledgerkit.
