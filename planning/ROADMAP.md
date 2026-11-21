# Roadmap

Status values and what they mean here:

- **Proposed** — described in a plan or prompt, not yet reviewed/accepted.
- **Planned** — accepted in principle; dependencies and acceptance criteria
  recorded; no focused implementation plan written yet.
- **In progress** — a focused plan exists and work is underway.
- **Completed** — acceptance criteria met *with evidence*, confirmed by an
  independent closeout (`AGENTS.md` §6). Writing the code/docs is not
  sufficient on its own.
- **Deferred** — intentionally not pursued now; reason recorded.
- **Blocked** — cannot proceed; blocker recorded.

Full stage detail, dependencies and acceptance criteria:
[`planning/phase-01-foundation.md`](phase-01-foundation.md).

## Phase 1 — Foundation

| Stage | Description | Status |
|---|---|---|
| 1.0 | Repository bootstrap and governance | In progress — see below |
| 1.1 | Knowledge and documentation methodology | In progress |
| 1.2 | Agent development methodology | In progress |
| 1.3 | Codex CI review gate | In progress — deterministic piece built and tested; live integration **blocked** (no `OPENAI_API_KEY`/cost decision) |
| 1.4 | Axiom self-development and refactoring (first real component + behaviour-preserving refactor) | In progress — initial implementation done, reviewed, fixed; refactor not yet started |
| 1.5 | Independent documentation reconstruction and closeout | Planned |

Amended 2026-11-21 per `planning/prompts/002-phase-1-amend-and-implement.md`
and `decisions/0004` — see `planning/phase-01-foundation.md` §0 for what
changed.

**Phase 1 as a whole is not Completed until Stage 1.5's dogfooding exercise
closes out successfully.** Stage 1.0 completing does not imply Phase 1
completing — these are tracked separately below.

### Stage 1.0 — Repository bootstrap and governance

Status: **In progress.** Scaffolding, governance files, initial ADRs, and
the Phase 1 plan have been written in this session and are pending the
independent review and commit/push called for by the bootstrap prompt.
Stage 1.0 moves to Completed only after that review's findings are
resolved and the independent-closeout bar in
`planning/phase-01-foundation.md` is met — not merely because the files
exist.

### Stage 1.3 — Codex CI review gate

Status: **In progress, split per `decisions/0004`'s architectural split.**
`.github/scripts/policy_evaluator.py` (the deterministic policy evaluator)
is implemented against `contracts/codex-gate-policy-evaluator.md` and
covered by 16 passing tests
(`.github/scripts/tests/test_policy_evaluator.py`) exercising all six
required scenarios from `planning/prompts/002-...md` §6. The
`.github/workflows/deterministic-checks.yml` workflow runs this suite on
every push/PR with no secrets required.
`.github/workflows/codex-review.yml` and `.github/codex/prompts/review.md`
implement the live integration to spec (researched against current
OpenAI documentation — citations in the workflow file) but it is
**blocked**: no `OPENAI_API_KEY` exists in this environment, and enabling
it is a cost/billing decision for a human, not this session, to make. The
workflow is written to fail safely (skip, not false-pass) without that
secret. **A second, separately-blocking gap** (flagged by independent
review as previously unmentioned): even with the secret, making either
workflow an actual GitHub "required status check" needs repository-admin
API access this session doesn't have. This stage's exit criterion ("real
GitHub PR evidence demonstrates both successful and blocked outcomes") is
**not met** for the live piece — recorded open on both counts, not
papered over.

An independent review of this stage's code also found and fixed, before
commit: a vacuous staleness check (the comparison was tautological
because both sides read the same triggering-event value — fixed by
sourcing the comparison SHA from a live GitHub API call instead) and a
step that silently fabricated missing `status`/`schema_version` fields,
which would have defeated the malformed-output fail-closed rule the
moment the live path is enabled. See
`planning/phase-01-foundation.md` §12.

### Stage 1.4 — Axiom self-development and refactoring

Status: **In progress — all planned work done with evidence; awaiting
human sign-off to mark Completed (`AGENTS.md` §11).** The initial
implementation of the knowledge/documentation validator was built,
contracted, fixture-tested, and independently reviewed (two real defects
found and fixed: an unenforced "no paths outside the repository" rule; a
fenced-code-block heading false positive). A real, non-synthetic
documentation defect was found and fixed via dogfooding (shorthand ADR
citations in two Stage 1.1 docs). The pre-refactor baseline was locked
(`evidence/stage-1.4-baseline.md`), then a genuine behaviour-preserving
refactor was performed — `src/axiom_validator.py` split into
`src/axiom_validator/{parsing,rules,reporting}.py` plus an orchestrator —
with identical before/after test results (14/14, same tests) and a clean
independent review (zero blocking findings; see
`evidence/stage-1.4-refactor.md`). Amendment D demonstrations 4 and 7
are now fully demonstrated (`planning/phase-01-foundation.md` §10).

### Stage 1.5

Status: **Planned.** Requires its own focused implementation plan,
written and reviewed before work starts (`AGENTS.md` §2) — the detail in
`planning/phase-01-foundation.md` establishes dependencies and acceptance
criteria, not implementation authorisation.

## Directories deliberately not yet created

Nothing remains deliberately uncreated in the originally-proposed
scaffold — `src/` and `tests/` were created as part of Stage 1.4 with
real content (not placeholders): `src/axiom_validator.py`, 10 fixture
files and 14 tests under `tests/`. (`.github/scripts/tests/` is a
separate thing — Stage 1.3's own CI-tooling test suite, distinct from the
top-level `tests/` created for the Axiom component itself.)

`evidence/` was created as part of the Phase 1 amendment (Amendment C,
`decisions/0004`) with real initial content
(`evidence/phase-1-log.md`). `docs/` and `contracts/` were created as
part of Stage 1.1, also with real initial content, not placeholders.
`.github/workflows/` and `.github/scripts/` were created as part of
Stage 1.3, likewise with real, tested content for the deterministic
piece.
