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

First real software and first real passing tests in this project.
Everything else is still process and documentation.
