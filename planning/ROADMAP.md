# Roadmap

Status values and what they mean here:

- **Proposed** — described in a plan or prompt, not yet reviewed/accepted.
- **Planned** — accepted in principle; dependencies and acceptance criteria
  recorded; no focused implementation plan written yet.
- **In progress** — a focused plan exists and work is underway.
- **Completed** — acceptance criteria met *with evidence*, confirmed by an
  independent closeout (`AGENTS.md` §6). Writing the code/docs is not
  sufficient on its own.
- **Deferred** — intentionally not pursued now; reason recorded.
- **Blocked** — cannot proceed; blocker recorded.

Full stage detail, dependencies and acceptance criteria:
[`planning/phase-01-foundation.md`](phase-01-foundation.md).

## Phase 1 — Foundation

| Stage | Description | Status |
|---|---|---|
| 1.0 | Repository bootstrap and governance | In progress — see below |
| 1.1 | Knowledge and documentation methodology | In progress |
| 1.2 | Agent development methodology | Planned |
| 1.3 | Codex CI review gate | Planned |
| 1.4 | Axiom self-development and refactoring (first real component + behaviour-preserving refactor) | Planned |
| 1.5 | Independent documentation reconstruction and closeout | Planned |

Amended 2026-11-21 per `planning/prompts/002-phase-1-amend-and-implement.md`
and `decisions/0004` — see `planning/phase-01-foundation.md` §0 for what
changed.

**Phase 1 as a whole is not Completed until Stage 1.5's dogfooding exercise
closes out successfully.** Stage 1.0 completing does not imply Phase 1
completing — these are tracked separately below.

### Stage 1.0 — Repository bootstrap and governance

Status: **In progress.** Scaffolding, governance files, initial ADRs, and
the Phase 1 plan have been written in this session and are pending the
independent review and commit/push called for by the bootstrap prompt.
Stage 1.0 moves to Completed only after that review's findings are
resolved and the independent-closeout bar in
`planning/phase-01-foundation.md` is met — not merely because the files
exist.

### Stages 1.1–1.5

Status: **Planned.** Each requires its own focused implementation plan,
written and reviewed before work starts (`AGENTS.md` §2) — the detail in
`planning/phase-01-foundation.md` establishes dependencies and acceptance
criteria, not implementation authorisation.

## Directories deliberately not yet created

`src/`, `tests/`, `.github/workflows/` do not exist in this repository
yet. They are scoped to Stage 1.3 (`.github/workflows/`) and Stage 1.4
(`src/`, `tests/`) and are intentionally absent until those stages give
them real content (see `planning/phase-01-foundation.md`), per the
bootstrap prompt's instruction not to create placeholder structure.

`evidence/` was created as part of the Phase 1 amendment (Amendment C,
`decisions/0004`) with real initial content
(`evidence/phase-1-log.md`). `docs/` and `contracts/` are being created
as part of Stage 1.1, also with real initial content, not placeholders.
