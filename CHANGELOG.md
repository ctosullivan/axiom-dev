# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not yet have a release; entries accumulate under
`Unreleased` until Phase 1 produces something releasable.

## [Unreleased]

### Added

- Repository governance foundation (Phase 1, Stage 1.0): `AGENTS.md`,
  `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`.
- Planning infrastructure: `planning/ROADMAP.md`, `planning/CONTEXT.md`,
  `planning/phase-01-foundation.md`, `planning/prompts/`,
  `planning/retros/`.
- Initial Architecture Decision Records: `decisions/0001` (development
  governance and repository methodology), `decisions/0002` (canonical
  knowledge and documentation architecture), `decisions/0003` (independent
  verification and agent responsibilities).
- `.github/pull_request_template.md`.
- Phase 1 amendment (prompt 002): `decisions/0004` (anti-circularity
  verification mechanics, measurement, explicit acceptance
  demonstrations); `planning/prompts/002-phase-1-amend-and-implement.md`;
  `evidence/phase-1-log.md`.
- Stage 1.1 first real content: `docs/documentation-schema.md`,
  `docs/knowledge-placement.md`, `docs/knowledge-reconciliation.md`,
  `contracts/documentation-schema-validator.md`.
- Stage 1.2: `docs/development-lifecycle.md`, `docs/agent-isolation.md`.
- Stage 1.3 (partial — deterministic piece only, live Codex integration
  blocked): `contracts/codex-gate-policy-evaluator.md`,
  `.github/scripts/policy_evaluator.py` and its test suite (16 passing
  tests), `.github/workflows/deterministic-checks.yml`,
  `.github/workflows/codex-review.yml` (written to spec, gated to skip
  without `OPENAI_API_KEY`), `.github/codex/prompts/review.md`.

- Stage 1.4 (initial implementation, pre-refactor): the first real Axiom
  Dev component — `src/axiom_validator.py`, a knowledge/documentation
  schema validator — against `contracts/documentation-schema-validator.md`,
  with 10 fixtures and 14 passing tests
  (`tests/test_axiom_validator.py`), `requirements.txt` (PyYAML), and a
  locked pre-refactor baseline (`evidence/stage-1.4-baseline.md`).
  Independent review before the baseline was locked found and this
  session fixed two real defects (an unenforced
  "no paths outside the repository" rule; a fenced-code-block false
  positive in heading detection). Dogfooding this validator against
  already-committed real documents (not just fixtures) found and fixed
  one real documentation defect: shorthand ADR citations in
  `docs/documentation-schema.md` and `docs/knowledge-placement.md` that
  didn't resolve as real paths.

- Stage 1.4 (refactor): `src/axiom_validator.py` (one monolithic file)
  split into `src/axiom_validator/{parsing,rules,reporting}.py` plus an
  orchestrator (`__init__.py`) and a new `__main__.py` for
  `python3 -m axiom_validator`. Identical before/after test results
  (14/14, same tests), zero blocking findings from independent review —
  see `evidence/stage-1.4-refactor.md`.

First real software, first real passing tests, first real (non-synthetic)
defect found in this project's own documentation by its own tooling, and
first genuine behaviour-preserving refactor with a clean independent
review.
