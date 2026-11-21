# Contributing to Axiom Dev

This document is the practical "how to land a change" guide for human
contributors. The methodology it implements is defined canonically in
[`AGENTS.md`](AGENTS.md) — read that first if you haven't; this file does
not repeat its reasoning, only the mechanics.

## Before you start

1. Read `planning/CONTEXT.md` for the current phase/stage and what's
   actually in flight.
2. Check `planning/ROADMAP.md` — a roadmap entry existing is not
   authorisation to build it. Each stage needs its own focused,
   version-controlled plan before implementation starts (`AGENTS.md` §2).
3. If your change isn't covered by an existing plan, write one under
   `planning/` before writing code or substantive docs.

## Making a change

1. Branch from `main`. Don't commit directly to `main` for anything
   non-trivial.
2. Implement to the plan. If reality diverges from the plan, update the
   plan — don't silently drift.
3. Update affected documentation, ADRs, `planning/ROADMAP.md`, and
   `planning/CONTEXT.md` in the **same** change (`AGENTS.md` §5). A PR that
   changes behaviour without touching the docs that describe that behaviour
   will be asked to add that before review.
4. Record a new ADR under `decisions/` only if the change involves a
   genuinely non-obvious decision (`AGENTS.md` §3). Never edit an accepted
   ADR's decision in place — add a superseding ADR instead.
5. Attach verification evidence appropriate to the change. For a change to
   `src/axiom_validator/` or `.github/scripts/policy_evaluator.py`, that
   means deterministic tests (`AGENTS.md` §8) — see "Testing requirements"
   below for the real, already-running suites. For a documentation-only or
   governance change, that means internal consistency checks,
   cross-reference checks (ideally run through the validator itself if the
   document carries a schema — `docs/documentation-schema.md`), and an
   independent review pass.

## Commit conventions

- Imperative summary line, `type(scope): subject` where it clarifies intent
  (e.g. `docs(phase-1): establish governance and implementation plan`).
- Explain *why* in the body when the summary line doesn't make it obvious.
- Never commit secrets, credentials, tokens, or personal information —
  including anything pasted into a preserved prompt under
  `planning/prompts/`.

## Pull requests

- Every substantive change goes through a PR, even for a single
  contributor — this is what makes independent review (`AGENTS.md` §6)
  possible before merge.
- The PR description states: what changed, why, which plan and/or ADR
  authorises it, and what verification evidence is attached.
- Do not merge your own PR without the review called for by the plan.
  Human approval is required before merge regardless of agent confidence
  (`AGENTS.md` §11).

## Testing requirements

Stage 1.4 introduced the first real component
(`src/axiom_validator/`), so this is no longer forward-looking — it's
the standard that component was actually built and refactored against,
and it applies to anything added after it:

- New behaviour needs a deterministic test. (`tests/test_axiom_validator.py`
  and `.github/scripts/tests/test_policy_evaluator.py` are the first two
  real examples — run with `PYTHONPATH=src python3 -m unittest discover
  -s tests -v` and `PYTHONPATH=.github/scripts python3 -m unittest
  discover -s .github/scripts/tests -v` respectively.)
- Contract-governed behaviour needs a test that demonstrates the contract
  holds, and ideally one that demonstrates it would fail if violated —
  `contracts/documentation-schema-validator.md` and its fixtures are the
  working example (valid + deliberately invalid documents, one per
  contract rule).
- "Tests pass" is not sufficient evidence on its own for phase closeout —
  see `AGENTS.md` §6 and §8. In practice this meant independent review
  found two real defects in the validator that passing tests alone had
  not caught (`evidence/stage-1.4-baseline.md`).

## Definition of Done

See `AGENTS.md` §10. In short: planned, documented in the same change,
evidenced, ADR'd if non-obvious, and reflected accurately in the roadmap —
not merely written.

## Changing governing files

`AGENTS.md`, `CLAUDE.md`, and this file are governance itself. Changes to
them require explicit human approval and, if they materially change prior
methodology, a superseding ADR (`AGENTS.md` §12). The initial versions of
these three files were necessarily written during bootstrap, before this
process existed to govern their own creation — that bootstrap exception is
recorded in `AGENTS.md` §0 and does not apply to anything after it.

## Human approval boundaries

See `AGENTS.md` §11 for the list of actions that always need explicit human
sign-off (governance changes, marking phases complete, merging PRs,
destructive git operations, starting a new Phase 1 stage, licence changes).
