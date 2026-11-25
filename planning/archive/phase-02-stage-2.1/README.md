# Phase 2, Stage 2.1 — Ledgerkit oracle baseline archive

## Status and accepted scope

**Completed by repository-owner decision**, evidenced by the owner's
own merge of [PR #4](https://github.com/ctosullivan/axiom-dev/pull/4)
on 2026-11-22 (merged by `ctosullivan`, confirmed via
`gh pr view 4 --json mergedAt,mergedBy`) and by this PR's own explicit
instruction to mark the stage Completed. The accepted scope was
Stage 2.1's own, narrower deliverable — a reviewed development
contract and independent oracle for Ledgerkit's EC-022
(balance-assignment elision parsing), **not** EC-022's actual fix,
which this stage deliberately does not attempt (see "Limitations and
deferred work" below).

This archive is a logical index, per `docs/phase-archiving.md`'s
existing convention extended to stage granularity for the first time:
canonical plans and evidence are **not moved or duplicated** here,
only linked. Nothing in this entry overwrites or restates the
historical record at its own canonical path.

## Canonical record

- [Stage 2.1 plan](../../phase-02-stage-2.1-plan.md) — selected
  problem, independently re-derived root cause, the 9-row fixture
  matrix, frozen acceptance criteria, and the explicit "Handoff to
  Stage 2.4" (§6) that remains **active**, not archived — Stage 2.4
  reads this same file for its own implementation contract.
- [Durable oracle evidence](../../../evidence/phase-2-stage-2.1-oracle/README.md) —
  all 9 fixture journals, full hledger transcripts, exact binary/
  commit identification, reproduction recipe.
- [Independent review record](../../phase-02-planning-review.md) —
  all review rounds across this stage's planning and its PR #4
  implementation-readiness work (gate tests, licensing is out of
  scope of this record — see below), each preserved as a dated,
  appended section, nothing rewritten to look flawless in hindsight.

## Decisions and contracts

- [ADR 0008](../../../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md)
  sets the Phase 2 direction this stage executed against.
- The cross-cutting Phase 2 designs this stage produced remain **in
  active use by subsequent stages, not archived**:
  [adoption design](../../phase-02-adoption-design.md),
  [knowledge API design](../../phase-02-knowledge-api-design.md),
  [measurement design](../../phase-02-measurement-design.md), and the
  [master plan](../../phase-02-template.md).

## Achievements

1. Selected and scoped a real, bounded Ledgerkit development problem
   (EC-022) against actually-inspected source, not a hypothetical.
2. Established an independent, exact-commit hledger oracle and
   captured it durably as version-controlled evidence, reproduced
   twice (by this session and by a separately-dispatched reviewer
   with its own, differently-valued fixtures).
3. Found a genuinely new scope boundary (cross-transaction
   running-balance semantics) through direct oracle work, not
   assumed from the original Codex-adjacent write-up.
4. Produced the cross-cutting adoption, knowledge-API and measurement
   designs Stage 2.2 onward will build against, each independently
   reviewed and corrected across multiple rounds (`planning/phase-02-planning-review.md`).
5. Added a deterministic `ci-required` aggregate CI gate and its own
   regression test suite (`.github/scripts/ci_required_gate.py`,
   `.github/scripts/tests/test_ci_required_gate.py`), and confirmed
   GitHub branch-protection enforcement is genuinely active on `main`
   (`gh api repos/ctosullivan/axiom-dev/rulesets` — ruleset
   `enforcement: "active"`, `current_user_can_bypass: "never"`).
6. Five rounds of native Codex review on PR #4 (summarised in
   `planning/phase-02-planning-review.md` §9–§10): every real finding
   fixed, one genuine gap explicitly deferred with a recorded reason
   (see below), nothing silently dismissed.

## Limitations and deferred work

- **EC-022 itself is not fixed.** This stage's entire acceptance
  criteria (`planning/phase-02-stage-2.1-plan.md` §5) explicitly
  exclude implementing the fix, adding a Ledgerkit regression test,
  independently verifying a fix, or writing a compat-register entry —
  all of that is Stage 2.4's own, separately-approved work
  (`planning/phase-02-stage-2.1-plan.md` §6, "Handoff to Stage 2.4").
- **Native-register identity/reference integrity checking is a known,
  confirmed gap, not yet designed.** Found by native Codex review
  (`planning/phase-02-planning-review.md` §10): `impacted()`/`get()`
  as designed cannot detect, for example, two native compat-register
  records sharing an ID, because Ledgerkit's own register has no CI
  validation of its own to rely on. This requires its own focused
  design increment before Stage 2.3's deterministic-CI build, not
  silently assumed solved.
- **Row 9's cross-transaction running-balance case remains an
  explicit, accepted divergence boundary**, not a defect — Stage 2.4
  must record it as a reasoned compat-register disposition
  (`kind: unsupported` or `intentional_divergence`) once the fix
  lands, per `planning/phase-02-stage-2.1-plan.md` §3/§4.
- **EC-021's continued availability as Stage 2.4's drift-demonstration
  "relevant change" condition is not guaranteed** by the time Stage
  2.4 actually runs — Ledgerkit's own state may have moved on; the
  handoff names a fallback (any new, genuinely relevant hledger
  commit found at that time).

Next: [Stage 2.2 plan](../../phase-02-stage-2.2-plan.md);
[active roadmap](../../ROADMAP.md).
