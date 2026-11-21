---
audience: future sessions resuming this project, and anyone evaluating whether the methodology is worth its overhead
purpose: retrospective on the Phase 1 execution pass covering Stages 1.0-1.5 — intended vs actual outcome, overhead, lessons
required_sections: [Intended outcome, Actual outcome, Verification evidence, Unexpected findings, Process overhead, Lessons learned, Recommended methodology improvements]
authoritative_sources: [planning/phase-01-foundation.md, evidence/phase-1-closeout.md, decisions/0001-development-governance.md]
acceptance_criteria:
  - this is a retrospective on real events in this execution, not a restatement of the plan
  - Phase 1 is not described as complete, since it isn't
---

# Phase 1 retrospective (Stages 1.0–1.5, partial)

**Status note:** this retrospective covers one continuous execution
pass across Stages 1.0–1.5. **Phase 1 itself is not complete** —
`evidence/phase-1-closeout.md` recommends leaving it open on two named,
real blockers. This retrospective is written now because the bulk of
the work and the most interesting findings are already behind this
session, not because the phase has closed.

## Intended outcome

Per `planning/prompts/001-phase-1-bootstrap.md` and its amendment
`002-phase-1-amend-and-implement.md`: establish a lightweight,
self-governing development methodology and then prove it by using it to
build, verify, refactor, and independently re-document a real piece of
Axiom Dev itself — with measurement from the start, anti-circular
verification, and an explicit, falsifiable set of acceptance
demonstrations, not an assumed success.

## Actual outcome

Governance (1.0), the knowledge/documentation methodology (1.1), the
development lifecycle and agent-isolation vocabulary (1.2), a real
software component built, contracted, tested, independently reviewed,
and genuinely refactored with verified identical before/after behaviour
(1.4), and an independent documentation reconstruction against a
restricted evidence set that found and fixed real gaps (1.5) — all done
with evidence, not assertion. Stage 1.3 split cleanly into a
deterministic piece (done, tested) and a live piece (genuinely blocked
on an API key, a cost decision, and repository-admin access this
environment does not have). 6 of 8 Amendment D demonstrations are fully
real; the 7th is honestly reported as blocked rather than faked; the
8th is this retrospective and the closeout assessment it accompanies.

## Verification evidence

Every claim above has a corresponding file: `decisions/0001`–`0004`;
`docs/documentation-schema.md`, `docs/knowledge-placement.md`,
`docs/knowledge-reconciliation.md`, `docs/development-lifecycle.md`,
`docs/agent-isolation.md`, `docs/axiom-validator.md`;
`contracts/documentation-schema-validator.md`,
`contracts/codex-gate-policy-evaluator.md`; `src/axiom_validator/`
(5 modules) and `.github/scripts/policy_evaluator.py`; 30 passing tests
across two suites, independently re-run by multiple separate reviewers,
not just self-reported; `evidence/stage-1.4-baseline.md`,
`evidence/stage-1.4-refactor.md`, `evidence/stage-1.5-reconstruction.md`,
`evidence/phase-1-closeout.md`, `evidence/phase-1-log.md`.

## Unexpected findings

- **Writing "done" language before doing the thing happened twice in
  Stage 1.0 alone**, caught both times by independent review before
  commit, not by self-check. This is the single most important finding
  of the whole phase: the discipline this project is built around is
  genuinely hard to hold even inside the session that wrote the rules
  for it.
- **Dogfooding found a real documentation defect on its very first real
  run**: two Stage 1.1 docs cited ADRs by shorthand number instead of
  real filename, which the validator correctly rejected. This was not
  staged — it surfaced because `TestRealRepositoryDocuments` tests
  against actually-committed files, not only synthetic fixtures.
- **An independent review once found that "mechanical enforcement" was
  claimed for something that was actually only procedural** (the
  checksum-protected-fixture mechanism) — the exact mislabeling
  `decisions/0003` was written to prevent, caught in the wild, not
  hypothetically.
- **A later review found a genuinely vacuous security check**: an
  earlier version of the Codex-gate staleness rule compared a value
  against itself, so it could never fail. The fix required actual new
  architecture (a live GitHub API call), not a comment edit — the only
  defect in this phase that needed redesign rather than correction.
- **The fresh-agent "resume from repo knowledge alone" test caught a
  real transient inconsistency** between the working tree and the
  committed `planning/CONTEXT.md`/`ROADMAP.md` — a demonstration that
  found something real is better evidence than one that passed cleanly,
  and this project got genuinely better evidence by accident, not by
  design.
- **The Phase 1 closeout assessment caught a stale `CONTRIBUTING.md`
  section** that every prior review had missed, because no prior
  review's stated scope included that file — a direct lesson that
  review scope boundaries themselves can quietly exclude real drift.

## Process overhead

See `evidence/phase-1-log.md` for the full ledger. Totals as of this
retrospective: 9 independent-review/reconstruction dispatches, ~721,000
subagent tokens, 13 real blocking/defect findings (all fixed), 8
advisory findings (fixed or explicitly accepted with reasoning), 30
passing tests across 2 suites. Not measured, and not estimated: real
monetary API cost, wall-clock time for the orchestrating session's own
(non-dispatched) work, and any comparison against a non-Axiom-governed
baseline — this project has no access to the first and no basis for the
third, and says so rather than inventing numbers.

## Lessons learned

1. Independent review earned its cost repeatedly and concretely — every
   single batch of work in this phase had at least one real,
   independently-found defect, several of them the kind that would have
   shipped silently (the vacuous staleness check, the fabricated-field
   bug) without a reviewer actually running the code rather than reading
   it.
2. "Best-effort" isolation, named honestly throughout, was still useful
   — none of the reviews above needed mechanical isolation to find real
   defects. Whether a *harder* case would need it remains untested.
3. Review scope boundaries are themselves a drift vector: a file outside
   every review's stated scope (`CONTRIBUTING.md`) went stale for several
   commits before the broadest-scope review (Phase 1 closeout) caught it.
4. Writing status claims in the same document that will later state
   whether they came true is a recurring trap (the "pushed" claims in
   Stage 1.0, the "uncommitted as of this note" self-reference in Stage
   1.5) — not fully solved by this phase, only caught each time by
   review.
5. The project's own scope discipline (Amendment A) mostly held — no
   `src/`/`tests/` created early, no premature claims — but process
   weight grew with each stage regardless (more review rounds, more
   evidence files), which is itself worth watching in Phase 2.

## Recommended methodology improvements

- **Add a lightweight pre-commit self-check for "future-tense" language
  describing already-shipped capabilities** (e.g. grep for phrases like
  "not yet" or "once X introduces" against files outside the current
  change's stated scope) — would have caught the `CONTRIBUTING.md`
  staleness without needing the broadest-scope review to stumble on it.
- **Stop freezing commit SHAs in `planning/CONTEXT.md` prose**; point to
  `git log` instead (done in this same change, per
  `evidence/phase-1-closeout.md`'s own observation) — a frozen SHA goes
  stale the moment a new commit lands, which is close to always.
- **Consider whether every independent review needs the same depth.**
  Several reviews in this phase were proportionate to genuinely risky
  changes (the Codex workflow, the refactor); a future phase should
  watch whether review depth is actually being matched to risk, or
  just applied uniformly because it's the default.
- **Stage 1.3's split (deterministic piece buildable now, live piece
  explicitly deferred) worked well** and is worth reusing as a pattern
  whenever a capability depends on credentials/access this environment
  doesn't reliably have — build and test the logic that doesn't need
  them, and name the blocker precisely rather than waiting on it to
  start anything.
