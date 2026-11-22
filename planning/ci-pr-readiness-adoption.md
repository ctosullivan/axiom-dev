# Focused adoption plan — required CI and bounded PR auto-fix

**Status:** Implemented on PR branch, pending GitHub protection setup, latest-head Codex review and human acceptance.
**Authorisation:** Owner request, 2026-11-22, to harden CI and extend AGENTS.md with a bounded Claude ↔ Codex implementation-PR correction cycle on the current PR branch.
**Related policy:** AGENTS.md §§2, 6, 8–13; decisions/0005 (Codex review advisory, not a mechanically enforced gate).

## Baseline and objective

The current `deterministic-checks` workflow runs four independent, credential-free jobs on pushes and PRs. At initial inspection no repository rulesets existed; branch-protection read requires administration permission unavailable to the connected integration. A passing workflow is not proof that GitHub requires those checks for merging. Native Codex reviews are asynchronous comments, not required CI statuses.

Deliver a simple, auditable workflow where Claude can take an *already authorised* implementation task from build to PR readiness without requesting routine fixes from the owner, while GitHub mechanically blocks a merge if deterministic CI is red. Retain human planning, governance, semantic acceptance and merge authority.

## Scope and implementation

1. Introduce one stable summary check `ci-required` in the existing workflow; it fails if any of the four dependent jobs failed, skipped, or was cancelled, and runs despite upstream failures.
2. Add a bounded agent procedure to `AGENTS.md` for local verification, pushing and creating/updating implementation PRs, obtaining a *latest-head* native Codex review, triaging findings, rerunning CI, and stopping at human acceptance. No automatic merging or bypass.
3. Document one-time GitHub branch protection setup and verification in `docs/ci-enforcement-setup.md`. A repository setting, not a workflow file, makes a check required.
4. Update stale CI enforcement descriptions without claiming server-side configuration is complete.

Non-goals: custom review runner, API-backed Codex workflow, autonomous phase approval, auto-merge, new secrets or paid infrastructure, a new test suite, or modifying Ledgerkit.

## Verification and acceptance

- Existing four jobs are unchanged, `ci-required` is an explicit `needs` dependent gate, and is set to `always()`; any non-success dependency yields a failing summary check.
- CI must complete for the latest PR SHA; confirm four underlying checks and `ci-required` succeeded in the GitHub UI.
- A repository admin must configure `main` to require a PR and the exact `ci-required` check, then verify a failing required check would block merging. Until then **mechanical enforcement is not complete**.
- Native Codex must review the latest PR head after these modifications, findings must be reviewed/dispositioned, and governance change needs human review. Only then may the owner approve a merge.
- No phase is declared complete by this workflow change.

## Rollout / risks

The repository owner must apply the branch rule manually or through authenticated `gh api` on their Pi; the connected GitHub integration cannot mutate branch protection. Neither a green CI run nor an old Codex receipt proves the newest commit was reviewed. Bound fix iterations (default three) to prevent loops, and report unresolved findings rather than silently weakening contracts, tests, or checks.

**State:** Checked-in files are only the repository portion of the change; enable and validate the external branch rule separately.