# Minimal architecture diagram — Phase 2

**Status: Proposed, not implemented.** Answers this assignment's
§16.F. Every component shown has a justification in
`planning/phase-02-adoption-design.md`,
`planning/phase-02-knowledge-api-design.md` or
`planning/phase-02-measurement-design.md`; nothing is added here that
those documents don't already account for.

```
                    ┌─────────────────────────────────────────┐
                    │  Independent consuming repository         │
                    │  (e.g. Ledgerkit)                          │
                    │                                            │
                    │  AGENTS.md / CLAUDE.md  (unchanged,        │
                    │  remains the project's own governance)     │
                    │                                            │
                    │  ┌──────────────────────────────────┐     │
                    │  │ .claude/skills/axiom-work/         │     │
                    │  │   SKILL.md                         │     │
                    │  │ (Claude Code-specific adapter;      │     │
                    │  │  guides UNDERSTAND..RECONCILE,      │     │
                    │  │  calls out to the CLI below —       │     │
                    │  │  never implements logic itself)     │     │
                    │  └──────────────┬─────────────────────┘     │
                    │                 │ invokes                   │
                    │                 ▼                            │
                    │  ┌──────────────────────────────────┐     │
                    │  │ axiom-knowledge CLI / library       │     │
                    │  │ get / find / related / impacted     │     │
                    │  │ (plain Python, no daemon)           │     │
                    │  └───┬─────────────────┬──────────────┘     │
                    │      │ reads            │ appends            │
                    │      ▼                  ▼                    │
                    │ ┌──────────────┐  ┌─────────────────────┐  │
                    │ │ knowledge/    │  │ .axiom-local/        │  │
                    │ │  wiki/        │  │  events.jsonl         │  │
                    │ │  claims/      │  │ (gitignored,          │  │
                    │ │  (default —   │  │  per-checkout only)   │  │
                    │ │  OR an        │  └─────────────────────┘  │
                    │ │  existing     │                            │
                    │ │  register,    │                            │
                    │ │  e.g.         │                            │
                    │ │  Ledgerkit's  │                            │
                    │ │  own          │                            │
                    │ │  dev-docs/    │                            │
                    │ │  compat-      │                            │
                    │ │  register/)   │                            │
                    │ └──────┬───────┘                            │
                    │        │ versioned by                        │
                    └────────┼────────────────────────────────────┘
                             ▼
                    ┌─────────────────────────────────────────┐
                    │  Git  (the authoritative store and the    │
                    │  only write path — commits/PRs, not an     │
                    │  API call)                                 │
                    └────────────────┬────────────────────────┘
                                      │ triggers
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │  CI (existing GitHub Actions or           │
                    │  equivalent — not new orchestration)       │
                    │  - schema/identity/reference integrity     │
                    │  - changed-source -> impacted() report     │
                    │  - deterministic test suite                │
                    └────────────────┬────────────────────────┘
                                      │ surfaces findings for
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │  Independent verification                  │
                    │  (fresh-context agent or human reviewer,    │
                    │  isolation level named honestly —           │
                    │  docs/agent-isolation.md-style discipline;  │
                    │  for Ledgerkit, may reuse its own existing  │
                    │  compat-differential-tester convention)     │
                    │  — establishes actual correctness; CI       │
                    │  alone never does                           │
                    └─────────────────────────────────────────┘


              ┌───────────────────────────────────────────────┐
              │  Future, optional, Phase 3 (NOT built in         │
              │  Phase 2, not a Phase 2 dependency):              │
              │                                                   │
              │   MCP adapter ──(wraps, read-only)──> axiom-     │
              │   (thin, consumer-optional)          knowledge   │
              │                                        library    │
              │                                                   │
              │   Axiom Assure ──(controlled A/B of agent/        │
              │   (experimental harness)   retrieval strategies,  │
              │                             using the same stable │
              │                             IDs/claims as data)   │
              └───────────────────────────────────────────────┘
```

## Relationships, stated explicitly (nothing implied by the picture alone)

- The **consuming repository** owns its governance file and its
  knowledge files outright; Axiom adds a skill and a CLI, it does not
  take ownership of either.
- The **skill** is the only Claude-Code-specific component. It calls
  the CLI exactly as a human or non-Claude agent would — there is no
  hidden channel between the skill and the knowledge store that
  bypasses the CLI.
- The **CLI/library** is the only thing that reads/writes structured
  knowledge data, and it never writes without a human/agent committing
  the result through Git — "appends" to the event log is the one
  exception, and that log is explicitly not the knowledge store (it's
  disposable, gitignored, observational).
- **Git is the single authoritative store** for both knowledge/
  wiki/claims and events' *absence of* write access — the CLI reads
  Git-tracked files directly, with no intermediate database.
- **CI** runs the same deterministic checks a developer can run
  locally (per `docs/agent-isolation.md`'s existing enforcement-level
  taxonomy, reused rather than reinvented) and is explicitly not the
  same thing as independent verification — the diagram keeps these as
  two boxes, not one, because conflating "CI passed" with "verified"
  is the exact mistake ADR 0008 Decision 5 and this assignment's §12
  warn against.
- **Independent verification** sits outside CI on purpose: a human or
  a fresh-context agent, not the pipeline, makes the semantic call CI
  cannot make.
- The **Phase 3 box is drawn separately and down-weighted visually**
  (dashed boundary intent, shown here as a separate block) specifically
  to make it obvious that removing it entirely still leaves a complete,
  functioning Phase 2 system above — satisfying architectural principle
  G directly in the diagram, not just in prose.

## Complexity-budget check against this diagram

No component above is a database, a persistent background service, a
write-capable API, an autonomous knowledge generator, an embedding
index, or a dashboard. Every box maps to an existing justification:
skill → `planning/phase-02-adoption-design.md` §6–8; CLI/library →
`planning/phase-02-knowledge-api-design.md` §4; knowledge files → §2–3
of the same; event log → `planning/phase-02-measurement-design.md` §1;
Git/CI/independent verification → existing Axiom Dev conventions,
reused, not rebuilt.
