# 0005. Replace the API-backed Codex CI gate with native Codex GitHub PR review for Phase 1

## Status

Accepted — 2026-11-21

## Context

`decisions/0004` (Amendment B) split Stage 1.3 into a deterministic policy
evaluator (`.github/scripts/policy_evaluator.py`, buildable and testable
without external credentials) and a live piece: an `OPENAI_API_KEY`-backed
GitHub Actions workflow (`.github/workflows/codex-review.yml`) calling
`openai/codex-action@v1`, gated by that evaluator, intended to become an
enforceable required-status check. That live piece has remained blocked
throughout Phase 1 on two independent grounds: no `OPENAI_API_KEY` exists
in this environment (a cost/billing decision only a human can make), and
configuring GitHub branch protection/required status checks needs
repository-admin API access this environment does not have (no `gh`
CLI, no token — confirmed again directly in this session: `gh` is not
installed, `apt-cache policy gh` shows "Installed: (none)", and
passwordless `sudo` is unavailable to install it).

A third authorising prompt
(`planning/prompts/003-phase-1-corrective-amendment.md`, Amendment A)
changes the requirement itself rather than asking this session to keep
waiting on that blocker: for Phase 1, independent AI review of a PR is to
be performed through **native Codex GitHub PR review** — the Codex
GitHub App/integration reviewing an actual opened PR, triggered by
`@codex review` or equivalent, using a connected ChatGPT/Codex account —
not a self-hosted, API-key-backed Actions workflow. The prompt is explicit
that an OpenAI API key is "not required or expected for Phase 1," and that
automated required-status-check merge blocking is "not a Phase 1 exit
requirement under the amended methodology."

## Decision

1. **For Phase 1, independent Codex review means native Codex GitHub PR
   review**, performed on the actual opened PR for this branch, not a
   simulated or locally-invoked equivalent. The review workflow is:
   push → open/update PR → request native review (`@codex review` or the
   connected integration's equivalent) → independently assess and
   disposition findings (P0/P1 resolved or explicitly escalated to the
   human; P2/advisory dispositioned but non-blocking) → record the
   reviewed commit and findings → human merge decision. This is recorded
   in `planning/phase-01-foundation.md` §17.
2. **The original automatic, API-backed, required-status-check gate is
   superseded for Phase 1, not secretly satisfied and not deleted.**
   `.github/workflows/codex-review.yml` is moved out of the active
   `.github/workflows/` path (where GitHub Actions would otherwise treat
   its `check-secret`-gated skip as part of normal CI status) to
   `.github/deferred/codex-review.yml`, with its header updated to record
   this supersession. `.github/scripts/policy_evaluator.py` and its test
   suite (`.github/scripts/tests/test_policy_evaluator.py`) are
   **preserved unmodified**; `contracts/codex-gate-policy-evaluator.md`
   required one trivial path-reference update (the comment naming where
   its "caller responsibility" obligation lives, now
   `.github/deferred/codex-review.yml` rather than
   `.github/workflows/codex-review.yml`) — a necessary consequence of the
   file move itself, not a change to any rule's logic (found worth
   stating precisely by independent review, which checked `git diff`
   rather than taking "preserved as-is" at face value). All three remain
   real, independently-reviewed, locally-tested artifacts with no
   live-credential dependency of their own, reusable if an automated
   gate is reconsidered later (see Consequences).
3. **Deterministic CI is unaffected and is strengthened in the same
   change** (Amendment E, tracked separately): the validator's own test
   suite and a check of a small, explicit set of governed documentation
   files now run in `.github/workflows/deterministic-checks.yml`. This
   was already true of the policy-evaluator tests; it did not previously
   extend to the validator itself, which this ADR's companion plan
   amendment corrects.
4. This decision does **not** reverse `decisions/0003`'s independent
   verification principles or `decisions/0004`'s anti-circularity
   mechanics — those govern how *this session's own* work is checked
   (fresh-context dispatch, checksum-protected fixtures, defect ledgers).
   Native Codex review is an *additional*, externally-sourced review
   mechanism layered on top, not a replacement for them.

## Alternatives considered

- **Keep pursuing the API-backed gate and continue reporting it blocked.**
  Rejected: prompt 003 explicitly changes the requirement rather than
  asking this session to keep waiting on an unresolved cost/access
  decision; continuing to report the same blocker without acting on the
  new authorisation would itself become a form of documentation drift.
- **Delete the API-backed workflow and its scripts entirely.** Rejected:
  prompt 003 explicitly says "do not delete working, verified components
  merely because their live integration is deferred," and the policy
  evaluator is real, tested, independently reviewed work
  (`evidence/phase-1-log.md`) with no live-credential dependency — keeping
  it preserves that investment for reconsideration (see Consequences)
  without pretending it is currently part of Phase 1's active gate.
- **Simulate a native Codex review locally to avoid depending on human
  action to open a PR.** Rejected for the same reason `decisions/0004`
  rejected simulating the live API gate: a local simulation cannot
  substitute for real evidence that an actual external reviewer reviewed
  an actual PR. If this session cannot open a PR (see Consequences), the
  acceptance criterion stays open and is reported as such, not faked.
- **Treat a Claude-performed review as if it were the Codex review.**
  Rejected outright per prompt 003 §11 Step 7 ("do not fabricate a Codex
  review or substitute a Claude review while describing it as Codex").
  Claude-performed independent review continues under `decisions/0003`
  for this session's own internal verification; it is never relabelled as
  Codex's review.

## Rationale

Native Codex GitHub PR review is preferable for Phase 1's MVP scope
because it needs no API key, no billing decision, and no repository-admin
configuration to produce real independent review evidence on a real PR —
exactly the resources this environment has repeatedly lacked for the
API-backed alternative. Its cost is a corresponding reduction in
enforcement: a native PR review is an independent AI assessment a human
reads and acts on, not a mechanism that can mechanically block a merge.
`decisions/0003` already requires naming isolation/enforcement claims
honestly rather than overclaiming them; this ADR applies the same
discipline to the word "gate" — a native review is a *review*, and this
project must never describe it as a CI gate that mechanically prevents an
unauthorised merge.

## Consequences

- Phase 1's independent-Codex-review acceptance criterion can now be met
  without `OPENAI_API_KEY` or repository-admin access — but only once a
  real PR exists and a human (or an available integration) actually
  triggers the native review; this session still cannot open a PR itself
  (no `gh`, no token — confirmed again in this session, not merely carried
  forward from an earlier assumption). Until that happens, the criterion
  stays open, not satisfied by this ADR alone.
- The original automated-gate requirement is recorded as **superseded by
  this ADR**, not quietly dropped: `planning/ROADMAP.md` and
  `planning/phase-01-foundation.md` must describe it as deferred, and name
  the conditions under which it should be reconsidered (below), rather
  than letting it silently disappear from the project's history.
- `.github/scripts/policy_evaluator.py`, its tests, and
  `contracts/codex-gate-policy-evaluator.md` remain in the repository
  (the contract carries the one trivial path update noted above),
  reusable with no change to any rule's logic if the conditions below
  are met.
- `.github/workflows/codex-review.yml` moving out of `.github/workflows/`
  means its `check-secret`/skip-not-fail logic no longer appears in GitHub
  Actions' run list at all for new commits — this is intentional: prompt
  003 Amendment A requires that "skipped jobs cannot be confused with
  successful reviews," and a job that no longer runs cannot be misread as
  a passing (or even a skipped-but-present) check.

**Conditions under which the automated API-backed gate should be
reconsidered**, recorded for a future phase rather than left implicit:

1. A human has made an explicit cost/billing decision to provision
   `OPENAI_API_KEY` for this repository, **and**
2. Repository-admin API access (a `gh`-authenticated token with admin
   rights, or equivalent) is available to configure required status
   checks, **and**
3. A real, concrete need for mechanical (not human-mediated) merge
   blocking has been identified — e.g. multiple contributors landing
   concurrent PRs where human review capacity alone is not keeping pace,
   rather than reconsidering it merely because the credentials became
   available.

## Relevant evidence

- `planning/prompts/003-phase-1-corrective-amendment.md` §4 (Amendment A,
  verbatim).
- `planning/phase-01-foundation.md` §17 (the corrective plan amendment
  this ADR authorises).
- `.github/deferred/codex-review.yml`, `.github/scripts/policy_evaluator.py`,
  `.github/scripts/tests/test_policy_evaluator.py`,
  `contracts/codex-gate-policy-evaluator.md` (preserved, not deleted).
- `decisions/0004` (the superseded automatic-gate expectation this ADR
  revises); `decisions/0003` (isolation/enforcement honesty standard this
  ADR applies to the word "gate").
- Direct confirmation in this session that `gh` remains unavailable: not
  installed, no passwordless `sudo` to install it, no `GITHUB_TOKEN` /
  `OPENAI_API_KEY` in the environment.

## Supersession

This ADR **supersedes the automated-gate portion of `decisions/0004`**
(Amendment B's live-integration expectation for Stage 1.3) — `decisions/0004`
itself is not edited; its status line is updated to note the partial
supersession, and its anti-circularity/measurement/demonstration content
(unrelated to the Codex-gate mechanism) remains in force, unrevised.
