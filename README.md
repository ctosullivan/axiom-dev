# Axiom Dev

Axiom Dev is the primary product of the Axiom project: an attempt to find the
simplest practical methodology for AI-assisted software development that
preserves important project knowledge, supports independent verification,
maintains accurate documentation, and lets complex software evolve reliably
across successive, disconnected development sessions.

> **Status: Phase 1 is substantially done but deliberately left open.**
> Documentation schemas now live under a dedicated
> [`schemas/`](schemas/) directory, mirrored by document path
> (`decisions/0006`, `decisions/0007`). Phase 1's independent-review
> requirement is **native Codex GitHub PR review**
> (`decisions/0005`) — [PR #1](https://github.com/ctosullivan/axiom-dev/pull/1)
> is open and has had four native Codex reviews so far; every finding
> stands corrected with regression evidence and independent
> verification. `planning/ROADMAP.md` covers the long-term direction
> beyond Phase 1 (Phases 2–4 proposed, not yet authorised). See
> [`planning/CONTEXT.md`](planning/CONTEXT.md) for the current state,
> [`evidence/phase-1-final-closeout.md`](evidence/phase-1-final-closeout.md)
> for the latest acceptance assessment, and
> [`planning/phase-01-foundation.md`](planning/phase-01-foundation.md)
> §16–§29 for Phase 1's full evidence and status.

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
own overhead. Phase 1 includes a mandatory self-development exercise
(Stages 1.1–1.5) in which Axiom Dev is built, refactored and independently
re-documented using its own methodology, specifically to test this
hypothesis against real work rather than assert it.

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
| `planning/ROADMAP.md` | Concise, long-term roadmap: Phase 1 (in progress) plus Phases 2–4 (proposed direction, not yet authorised). |
| `planning/CONTEXT.md` | Current phase, latest work, and the next concrete action. |
| `planning/phase-01-foundation.md` | The implementation-ready Phase 1 plan (Stages 1.0–1.5) and its two amendments' full detail. |
| `planning/prompts/` | Original planning prompts, preserved verbatim with provenance. |
| `planning/retros/` | Phase retrospectives, created as phases complete. |
| `planning/archive/` | Index of archived (Completed) phases — currently empty; see `docs/phase-archiving.md`. |
| `decisions/` | Sequentially numbered Architecture Decision Records. |
| `docs/` | Human-facing methodology documentation (knowledge placement, documentation schema, phase archiving) — Markdown only, no schema files, since `decisions/0007`. |
| `schemas/` | Every production document's declarative schema, mirrored by path (`docs/axiom-validator.md` → `schemas/docs/axiom-validator.md.schema.yaml`), plus `schemas/governed-documents.txt`, the minimal manifest of documents that must carry a passing schema (contract rule 15). |
| `contracts/` | Required behaviour, written and reviewed before the implementation it governs. |
| `evidence/` | Verification outcomes and the Phase 1 measurement log. |
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
