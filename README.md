---
audience: new contributors, agents resuming work, and anyone evaluating the project
purpose: orient a reader to what Axiom Dev is, its current status, and where to find governing detail
required_sections: [Mission, Fundamental hypothesis, Development methodology, Repository map, Licence]
authoritative_sources: [AGENTS.md, planning/ROADMAP.md, planning/CONTEXT.md]
acceptance_criteria:
  - every stage status claim matches planning/ROADMAP.md at time of reading
  - the repository map lists every top-level governance file and planning directory that actually exists
---

# Axiom Dev

Axiom Dev is the primary product of the Axiom project: an attempt to find the
simplest practical methodology for AI-assisted software development that
preserves important project knowledge, supports independent verification,
maintains accurate documentation, and lets complex software evolve reliably
across successive, disconnected development sessions.

> **Status: Phase 1, Stages 1.0–1.1 in progress.** Governance (1.0) and the
> knowledge/documentation methodology (1.1) are being established. No
> substantive Axiom Dev software has been implemented yet. See
> [`planning/CONTEXT.md`](planning/CONTEXT.md) for the current state and
> [`planning/ROADMAP.md`](planning/ROADMAP.md) for what is planned, in
> progress, or done.

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
| `planning/ROADMAP.md` | Phase/stage status: proposed, planned, in progress, completed, deferred, blocked. |
| `planning/CONTEXT.md` | Current phase, latest work, and the next concrete action. |
| `planning/phase-01-foundation.md` | The implementation-ready Phase 1 plan (Stages 1.0–1.5). |
| `planning/prompts/` | Original planning prompts, preserved verbatim with provenance. |
| `planning/retros/` | Phase retrospectives, created as phases complete. |
| `decisions/` | Sequentially numbered Architecture Decision Records. |
| `docs/` | Human-facing methodology documentation (knowledge placement, documentation schema). |
| `contracts/` | Required behaviour, written and reviewed before the implementation it governs. |
| `evidence/` | Verification outcomes and the Phase 1 measurement log. |
| `.github/pull_request_template.md` | Checklist a PR description must address. |

Directories named in the Phase 1 plan but not yet present (`src/`,
`tests/`, `.github/workflows/`) are intentionally deferred to Stage 1.3/1.4,
which give them real content — see `planning/phase-01-foundation.md` for
why each is scoped where it is.

## Licence

MIT — see [`LICENSE`](LICENSE).
