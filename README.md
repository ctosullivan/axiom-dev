# Axiom Dev

Axiom Dev is the primary product of the Axiom project: an attempt to find the
simplest practical methodology for AI-assisted software development that
preserves important project knowledge, supports independent verification,
maintains accurate documentation, and lets complex software evolve reliably
across successive, disconnected development sessions.

> **Status: Phase 1 completed by owner decision on 2026-11-22.**
> Its [archive](planning/archive/phase-01/README.md) preserves the
> [independent closeout](evidence/phase-1-final-closeout.md) and
> [outstanding qualifications](evidence/phase-1-owner-acceptance.md).
> **Phase 2 is planned, not implemented**: select one meaningful
> Ledgerkit/hledger compatibility task, specify an independent behavioural
> oracle, and dogfood the full development lifecycle. Build only the
> necessary comparative wiki, stable claim IDs, small Git/file-backed
> read-only knowledge API and deterministic CI impact checks; then
> extract a reusable template and test clean adoption.
> **Phase 2 does not A/B test the template.**
> Phase 3 is hypothesis-driven Assure evaluation of agent/retrieval
> strategies, with an optional MCP adapter where useful. See
> [roadmap](planning/ROADMAP.md) and [current context](planning/CONTEXT.md).

## Mission

Develop the simplest practical methodology for AI-assisted software
development that:

- preserves important project knowledge across sessions,
- supports independent verification of agent work,
- maintains documentation that stays accurate as the system changes, and
- lets complex software evolve reliably when no single agent session has
  continuous memory of the project.

Central principles:

- Agents are transient. Project knowledge compounds.
- Reason once, preserve what matters, and reuse verified understanding.
- Verification requires evidence, not confidence.
- Build the simplest system that demonstrably works.

## Fundamental hypothesis

A lightweight, knowledge-driven development methodology, implemented
predominantly using conventional engineering tools, can improve the
correctness, efficiency and maintainability of agentic software development
without requiring a specialised AI development platform.

This is a hypothesis to be tested, not a conclusion to be assumed. The goal
is not to maximise automation, knowledge records, or architectural
sophistication — it is to demonstrate improvement net of the methodology's
own overhead. Phase 1 included a self-development exercise (Stages 1.1–1.5)
in which Axiom Dev was built, refactored and independently re-documented
using its own methodology. Phase 2 will extend dogfooding to Ledgerkit with an independent oracle,
a small evidence-backed knowledge API and drift checks, then extract a
reusable template. This is not a controlled A/B test.

## Relationship to Axiom Assure

Axiom Assure (`github.com/ctosullivan/axiom-assure`) is a separate,
independent, experimental assurance laboratory. The two projects share
knowledge principles, contracts, evidence conventions and relevant semantic
standards, but do not share runtime infrastructure and do not require one
another to operate. Axiom Dev is the immediate development priority.

## Relationship to CodeCompass

Axiom follows an earlier project, CodeCompass (`~/projects/codecompass`,
`github.com/ctosullivan/codecompass`), now discontinued in favour of a
fundamentally simpler methodology. **Axiom is a new project, not CodeCompass
v3** — it does not inherit CodeCompass's implementation, schemas,
architectural decisions or infrastructure by default. It does carry forward
specific engineering lessons from CodeCompass's experience; these are
recorded with source citations in
[`planning/phase-01-foundation.md`](planning/phase-01-foundation.md) and in
the initial [ADRs](decisions/).

## Development methodology

Axiom Dev's own development is governed by the lifecycle it is designed to
support:

```
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE
```

See [`AGENTS.md`](AGENTS.md) for the canonical rules this implies for both
human contributors and coding agents, and [`CONTRIBUTING.md`](CONTRIBUTING.md)
for how to propose and land a change.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Canonical development methodology and agent rules. |
| `CLAUDE.md` | Claude Code–specific adaptations of `AGENTS.md`. |
| `CONTRIBUTING.md` | How to propose, implement and land a change. |
| `CHANGELOG.md` | Human-readable record of notable changes. |
| `planning/ROADMAP.md` | Concise phase status: Phase 1 completed; Phase 2 template work planned; Phases 3–4 proposed. |
| `planning/CONTEXT.md` | Current phase, latest work, and the next concrete action. |
| `planning/phase-01-foundation.md` | Canonical historical Phase 1 plan, stages and amendments (unchanged by archiving). |
| `planning/phase-02-template.md` | Proposed evidence-first Phase 2 vertical-slice plan, knowledge API, deterministic CI, dogfooding and extraction. |
| `planning/prompts/` | Original planning prompts, preserved verbatim with provenance. |
| `planning/retros/` | Phase retrospectives, created as phases complete. |
| `planning/archive/` | Completed Phase 1 archive index; see `docs/phase-archiving.md`. |
| `decisions/` | Sequentially numbered Architecture Decision Records. |
| `docs/` | Human-facing methodology documentation (knowledge placement, documentation schema, phase archiving) — Markdown only, no schema files, since `decisions/0007`. |
| `schemas/` | Every production document's declarative schema, mirrored by path (`docs/axiom-validator.md` → `schemas/docs/axiom-validator.md.schema.yaml`), plus `schemas/governed-documents.txt`, the minimal manifest of documents that must carry a passing schema (contract rule 15). |
| `contracts/` | Required behaviour, written and reviewed before the implementation it governs. |
| `evidence/` | Verification outcomes, the Phase 1 measurement log and explicit owner acceptance qualifications. |
| `.github/pull_request_template.md` | Checklist a PR description must address. |
| `.github/workflows/` | Deterministic CI: policy-evaluator tests, validator tests, governed-documentation check, doc hygiene — all tested and running, none a required merge check. |
| `.github/deferred/` | The API-backed Codex review workflow, deferred (not deleted) in favour of native Codex GitHub PR review for Phase 1 — see `decisions/0005`. |
| `.github/scripts/` | The Stage 1.3 policy evaluator and its own test suite — preserved, reusable if the deferred automated gate is reconsidered. |
| `.github/codex/prompts/review.md` | The review instructions written for the deferred API-backed workflow. |
| `src/axiom_validator/` | The first Axiom Dev component: a knowledge/documentation schema validator (parsing/rules/reporting modules; reads each document's schema from the mirrored `schemas/` tree, since `decisions/0007`). |
| `tests/` | Fixtures (valid + deliberately invalid, one per contract rule, as `.md` files under `tests/fixtures/{valid,invalid}/`) and tests for the validator, across several test files. Fixture schemas live in their own mirrored tree, `tests/fixtures/schemas/`, never inside the production `schemas/` tree. |
| `requirements.txt` | The one runtime dependency (PyYAML) the validator needs. |

Every directory in the originally-proposed Stage 1.0 scaffold now has
real content — none remain deliberately empty.

## Licence

MIT — see [`LICENSE`](LICENSE).
