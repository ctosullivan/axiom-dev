# Session continuity

Keep this current, not historical. Historical narrative belongs in
`planning/retros/` and in commit/PR history.

## Current phase and status

**Phase 1, Stages 1.0–1.3 all touched; none closed out.** Stage 1.0 is
committed/pushed but unmerged (no PR opened yet — no `gh`/token). Stage
1.1 is committed/pushed on the same branch. Stage 1.2 (lifecycle +
agent-isolation docs) and Stage 1.3 (Codex gate, deterministic piece only)
have just been written and are pending independent review before commit.

**Stage 1.3 status, stated precisely:** the deterministic policy
evaluator is implemented, contracted, tested (16/16 passing,
`.github/scripts/tests/`), and wired into a CI workflow that needs no
secrets. The live Codex integration workflow is written to spec but
**blocked** — no `OPENAI_API_KEY` in this environment, and enabling paid
Codex review calls is a cost decision for a human. This is recorded as an
open item, not papered over with a claim the gate is "done."

## Latest completed work

**Stage 1.0 (committed, pushed, unmerged):** commits `0307e83`, `649a025`.

**Amendment (prompt 002) + Stage 1.1 (committed, pushed, unmerged):**
commit `31fb153` on `phase-1/stage-1.0-bootstrap` — `decisions/0004`,
the amended plan, `evidence/phase-1-log.md`, the documentation schema,
full knowledge placement policy, first contract
(`contracts/documentation-schema-validator.md`), and the reconciliation
procedure. Independently reviewed (2 blocking findings, both fixed — see
`planning/phase-01-foundation.md` §11).

**Stage 1.2 (docs only, uncommitted as of this note):**
- `docs/development-lifecycle.md` — the six-step lifecycle with
  entry/exit criteria per step, plus the concrete phase-acceptance
  procedure (how a stage actually gets marked Completed).
- `docs/agent-isolation.md` — responsibilities by function (not roster),
  a three-level isolation taxonomy (prompt-based / fresh-context /
  mechanical), and an explicit statement that every review run in this
  project so far has been level 2 (fresh-context, same operator), never
  level 3.

**Stage 1.3 (real software, uncommitted as of this note):**
- Researched current OpenAI Codex GitHub integration options (two
  searches; chose `openai/codex-action@v1` with structured JSON output
  over the managed Codex Cloud integration, since the latter only
  produces a natural-language PR comment unsuitable for deterministic
  gating).
- `contracts/codex-gate-policy-evaluator.md` — written to match the
  implementation below (recorded honestly as implementation-then-contract,
  unlike Stage 1.4's mandatory contract-first rule).
- `.github/scripts/policy_evaluator.py` + 16 passing unit tests
  (`.github/scripts/tests/`) covering all 6 required test scenarios
  (valid PR, P0/P1 defect, advisory finding, malformed reviewer output,
  missing/failed review, stale-commit review) — real, run, passing.
- `.github/workflows/deterministic-checks.yml` (runs now, no secrets
  needed) and `.github/workflows/codex-review.yml` +
  `.github/codex/prompts/review.md` (written to spec; live path
  untested, gated to skip safely without `OPENAI_API_KEY`).

## Relevant decisions

- `decisions/0001` — development governance and repository methodology.
- `decisions/0002` — canonical knowledge and documentation architecture;
  schema-format question resolved by `docs/documentation-schema.md`.
- `decisions/0003` — independent verification and agent responsibilities;
  the isolation taxonomy is now concretely applied in
  `docs/agent-isolation.md`.
- `decisions/0004` — Phase 1 amendment: anti-circularity verification,
  measurement, acceptance demonstrations; its architectural split for
  Stage 1.3 is what's currently in effect.

## Outstanding issues

- No `gh` CLI or GitHub token — no PR opened yet for any of this work. A
  human needs to open it from the URL below.
- **Stage 1.3 has two distinct, separately-blocking gaps, named
  separately rather than folded into one:**
  1. Live Codex integration needs an `OPENAI_API_KEY` repository secret
     and a human cost/billing decision to enable recurring paid review
     calls (`planning/prompts/002-...md` §9).
  2. Even once (1) is resolved, making `deterministic-checks.yml` and/or
     `codex-review.yml` an actual GitHub "required status check" needs
     repository-admin API access this session doesn't have (no
     `gh`/token) — a human must configure branch protection separately.
     An independent review flagged that this second gap had gone
     unmentioned in earlier status notes; it's recorded explicitly now.
  Until both are resolved, Stage 1.3's "real GitHub PR evidence
  demonstrates both successful and blocked outcomes" exit criterion stays
  unmet — a green `deterministic-checks.yml` run is not, by itself, a
  merge gate.
- The independent review of the Stage 1.2 + Stage 1.3 batch has not run
  yet as of this note.

## Current branch / PR

- Branch: `phase-1/stage-1.0-bootstrap`, pushed to `origin` through commit
  `786e2c9` (verified: `git log`, `git push` output). Includes Stage 1.0
  (`0307e83`, `649a025`), amendment + Stage 1.1 (`31fb153`, `197dfdc`),
  and Stage 1.2 + Stage 1.3 deterministic piece (`786e2c9`).
- PR: still not opened. Creation URL:
  `https://github.com/ctosullivan/axiom-dev/pull/new/phase-1/stage-1.0-bootstrap`

## Next concrete action

1. Begin Stage 1.4 (validator component + behaviour-preserving refactor) —
   this does not require Stage 1.3's live Codex gate to exist first; the
   self-dogfooding rule explicitly permits documented manual independent
   review until the gate is live (`planning/prompts/001-...md` §7).
2. Separately: a human needs to (a) open/review the PR for everything
   pushed on `phase-1/stage-1.0-bootstrap`, and (b) decide whether to
   provision `OPENAI_API_KEY` and accept the cost of enabling Stage 1.3's
   live Codex review, and (c) configure branch protection/required status
   checks (needs repo-admin access this session lacks).
