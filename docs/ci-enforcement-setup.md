# Enable required CI on Axiom Dev main

The workflow `.github/workflows/deterministic-checks.yml` has four
deterministic jobs and one **aggregate status check** named `ci-required`.
The aggregate job uses `always()`, depends on all four jobs and fails if
any dependent job is not successful. Adding a fifth required underlying
job means adding it to the aggregate job's `needs` list.

**This file does not itself enforce branch protection.** A repository
administrator must configure the GitHub-side rule, then test it. Current
connected GitHub integration does not have branch-protection write or read
permissions. CI evidence alone is not a substitute.

## One-time setup (recommended: GitHub website)

1. Open the Axiom Dev repository on GitHub, then **Settings →
   Branches → Add branch protection rule** (or use a ruleset under
   **Settings → Rules → Rulesets**, if available).
2. Target exactly the `main` branch; require a pull request before
   merging and require status checks to pass.
3. Once `ci-required` has appeared on at least one current PR run,
   select the **exact** status-check name `ci-required` from GitHub's
   checks list. If an Actions app source is offered, select GitHub Actions.
4. Enable protection against direct pushes/bypass by administrators if
   desired and supported. For a solo-maintainer repository, do **not**
   require one *human approval review*: GitHub will not let you approve
   your own PR. Keep manual merge acceptance in `AGENTS.md` instead.
5. Save, then inspect the actual settings and PR merge box to verify that
   the check is **required**, not merely displayed.

If the status check is unavailable in the UI, run the PR's workflow once,
verify the exact job name shown, then revisit the rule. Do not invent a
status-check name or mark this setup complete before inspection.

## Verification from the Raspberry Pi

```bash
cd ~/projects/axiom-dev
gh auth status
gh pr checks 4
gh api repos/ctosullivan/axiom-dev/branches/main/protection
gh api repos/ctosullivan/axiom-dev/rulesets
```

The protection API may return 404 when no branch rule is configured or
403 when the authentication lacks administrative permissions. In that
case use GitHub's Settings UI; don't claim the rule exists. Record the
actual required check, source, date and verification evidence in the PR.

To prove that protection **blocks** failures, create a disposable PR
branch with a deliberately failing check (for example a temporary tracked
Markdown file with trailing whitespace), observe `ci-required` fail and
GitHub block merge, then remove the negative fixture on that branch.
Never introduce the failing fixture on `main`. A green PR alone does not
prove enforcement.

## What is and is not gated

- **Mechanically gated after setup:** policy-evaluator tests,
  axiom-validator tests, governed-document validation and trailing
  whitespace (collectively via `ci-required`).
- **Advisory:** native Codex GitHub review, human approval, factual
  correctness of semantic claims and documented review iterations.
- **Never infer:** that a Codex review of an old commit covers a new head,
  that a completed workflow means required checks are configured, or that
  GitHub's own green check replaces independent judgement.

The workflow can be executed and reviewed before repository protection
is enabled; until the rule is independently confirmed, its enforcement
class remains **4 (CI runs but does not mechanically block merge)**.
See `docs/knowledge-placement.md` and `AGENTS.md` §§11, 13–14.
