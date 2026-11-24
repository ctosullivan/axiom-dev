# Minimal adoption design — Claude skill, file layout, install/update

**Status: Proposed design, not implemented.** Answers this assignment's
§3/§4/§16.C: how an independent repository (Ledgerkit, or any other)
adopts Axiom with minimal configuration, and the one project-local
skill's content. Nothing here is built until Stage 2.2 is reviewed and
approved (`planning/phase-02-stage-2.1-plan.md` §6.3's approval-checkpoint
pattern applies again at the next stage boundary).

## 1. Capability-sourced design constraints

Based on `claude-code-guide` research into the actually-installed
Claude Code version (sources: `code.claude.com/docs/en/skills.md`,
`hooks.md`; full capability notes kept in
`planning/phase-02-planning-review.md`'s provenance section — treat
anything below marked "uncertain" there as needing a build-time check,
not as settled fact):

- **Project-local skills are supported and documented.** A skill can
  live at `<repo>/.claude/skills/<name>/SKILL.md`, loads for anyone
  working in that repo (no plugin marketplace, no hosted account), and
  is invoked either automatically (Claude matches its `description`)
  or explicitly via `/<name>`. `disable-model-invocation: true` can
  force manual-only invocation if that proves useful later — not
  adopted by default, since automatic matching is simpler for a
  five-minute methodology to actually get used.
- SKILL.md **can reference other files by relative path** rather than
  inlining content (a `reference.md` alongside it, or — critically for
  this project — relative links straight into the consuming project's
  own `AGENTS.md`/`CLAUDE.md`). This directly satisfies §4's "reference
  existing project files rather than copying the entire methodology
  into its instructions."
- **Hooks are supported** (`PreToolUse`, `PostToolUse`, `SessionStart`,
  `SessionEnd`, and others) and can run an ordinary shell command,
  including appending to a local file — this is plain shell behaviour,
  not a special Axiom mechanism. Used by the measurement design
  (`planning/phase-02-measurement-design.md`), not by the skill itself
  — including a `SessionStart`/`SessionEnd` hook pair that writes
  and removes a small, per-session-scoped (not shared) local handoff
  file so the CLI subcommands this skill invokes (which receive no
  hook stdin of their own) can stamp their own events with the
  correct session's ID, even when more than one session is active
  against the same checkout.
- Nothing requires a persistent daemon, an MCP server, or a hosted
  account for any of the above.

## 2. Adoption file layout (evaluated against the candidate structure)

The authorising prompt's candidate structure is evaluated field-by-field,
not copied uncritically (per its own "assess whether every proposed
file and directory is necessary" instruction):

```
<consumer-repo>/
├── AGENTS.md / CLAUDE.md / equivalent     [existing, untouched]
├── .claude/
│   └── skills/
│       └── axiom-work/
│           └── SKILL.md                   [new, Axiom's own]
├── knowledge/
│   ├── claims/                            [new, DEFAULT ONLY — see below]
│   ├── scope-manifests/                   [new, OPTIONAL — see below]
│   └── wiki/                              [new]
└── .axiom-local/
    └── events.jsonl                       [new, gitignored]
```

- **`knowledge/claims/` is a default for a consumer with no existing
  claim register — not a mandatory directory.** Stage 2.1's own
  concrete case (`planning/phase-02-stage-2.1-plan.md` §7) shows why:
  Ledgerkit already has `dev-docs/compat-register/`, which is a mature,
  governed claim register in its own right. Forcing a *second*,
  Axiom-shaped `knowledge/claims/` directory into Ledgerkit would
  directly violate this assignment's own "do not duplicate the same
  claim across multiple authoritative locations" instruction and its
  adoption requirement #3 ("use existing project governance without
  duplicating or replacing it"). **The adoption procedure's first real
  step is therefore not "create `knowledge/claims/`" but "ask whether
  an equivalent, governed claim location already exists; if so, point
  the knowledge API's source configuration at it instead."** A project
  with nothing equivalent gets the default `knowledge/claims/` layout
  described in `planning/phase-02-knowledge-api-design.md`.
- **`knowledge/wiki/`** is retained — a small set of Markdown pages
  giving human-readable comparison/explanation, each linking out to
  stable claim IDs rather than restating them (§7 of the authorising
  prompt: "separate human-readable wiki explanations from authoritative
  structured assertions"). This has no pre-existing Ledgerkit
  equivalent and is genuinely new.
- **`knowledge/scope-manifests/`** is new in this revision, and
  **optional per claim, not a mandatory directory either** — one small
  file per claim that needs a derived `VERIFIED` status when the
  claim's own native/default record carries no scope field of its own
  (`planning/phase-02-knowledge-api-design.md` §3b.1). It is
  deliberately kept outside Ledgerkit's own `dev-docs/compat-register/`
  — Axiom's own, separately-reviewed artifact, never a modification to
  a schema another project also uses.
- **`.claude/skills/axiom-work/SKILL.md`** — one skill (§3 below), kept.
- **`.axiom-local/events.jsonl`** — kept, Git-ignored by default (see
  `planning/phase-02-measurement-design.md` for format/retention). The
  directory name is deliberately **not** `.axiom/` — a leading-dot
  `-local` suffix signals at a glance that this is per-checkout,
  disposable, and never the authoritative knowledge store, unlike
  `knowledge/`.
- **No `axiom.toml`/config file is added at this stage.** A real need
  (e.g. "where is the claim register, if not the default path") would
  justify one line of config; inventing a configuration format ahead of
  that need would itself be the CodeCompass-style complexity this
  assignment's §14 exists to prevent. If Stage 2.2's actual
  implementation needs to point the API at `dev-docs/compat-register/`
  instead of `knowledge/claims/`, the simplest adequate mechanism (one
  constructor argument, one environment variable, or one line in
  `knowledge/README.md`) is chosen then, against the real requirement
  — not pre-decided here.

## 3. Required adoption capabilities, addressed one by one

| Capability (authorising prompt §3) | How this design provides it |
|---|---|
| 1. Add Axiom via a straightforward procedure | Copy `.claude/skills/axiom-work/`, `knowledge/wiki/` (and `knowledge/claims/` only if no existing register), add one line to the consumer's own `AGENTS.md`/`CLAUDE.md` pointing at the skill. No installer, no package registry dependency at this stage (§5 below assesses whether a thin pip package is warranted later). |
| 2. Activate an Axiom Claude Code skill | The skill loads automatically once present in `.claude/skills/`; no further activation step. |
| 3. Use existing project governance, not duplicate it | §2 above: defer to an existing claim register if one exists; the skill reads the consumer's own `AGENTS.md`/`CLAUDE.md` rather than asserting Axiom's own rules as authoritative over them. |
| 4. Retrieve project-specific evidence-backed knowledge | `get`/`find`/`related`/`impacted` — `planning/phase-02-knowledge-api-design.md`. |
| 5. Run deterministic validation | A small Python CLI (`axiom-validate` or similar; exact command named in the API design doc), runnable locally and from CI, independent of the skill. |
| 6. Record limited agent activity/outcome evidence | `.axiom-local/events.jsonl` via hooks — `planning/phase-02-measurement-design.md`. |
| 7. Reconcile via ordinary Git commits/PRs | No write API (§4 below); every claim/wiki change is an ordinary file edit reviewed like any other change. |
| 8. Upgrade/remove Axiom without losing project-owned knowledge | §4 below. |

## 4. Upgrade and removal

Because `knowledge/claims/` (or the consumer's own existing register),
`knowledge/wiki/` and the skill are all **plain files under the
consumer's own Git control**, upgrading Axiom means replacing the
skill's `SKILL.md`/supporting files and the small Python CLI/library
with a newer version — a normal file update, reviewable as a normal
diff. **Removing Axiom** means deleting `.claude/skills/axiom-work/`
and `.axiom-local/`; `knowledge/claims/` and `knowledge/wiki/` are
project-owned content, not Axiom-owned, and are explicitly *not*
deleted by a removal step — they remain as plain Markdown/YAML the
project can keep, repurpose, or delete itself. This reversibility is
mechanical, not merely a documentation promise: nothing in the design
requires a registered uninstall hook, a database migration, or
contacting a hosted service.

## 5. Distribution mechanism

Evaluated, per the authorising prompt's §3 explicit instruction, against
a project-local skill, shared skill distribution, template copy, and a
lightweight Python package:

- **A plugin marketplace is rejected outright** — explicit non-goal,
  adds an operational dependency this project does not need yet.
- **A persistent daemon or MCP server is rejected** — ADR 0008
  Decision 3 and this assignment's architectural principle G both
  require Phase 2 to work without either.
- **Template copy (clone a starter repo / copy a directory tree)** is
  the simplest mechanism and is **what Stage 2.2 should actually use
  first**: copy `.claude/skills/axiom-work/`, `knowledge/wiki/README.md`
  and a short `AGENTS.md` snippet into the consumer repo. It has no
  packaging, versioning or dependency-resolution machinery at all —
  appropriate for a first real adoption (Stage 2.6) where the goal is
  observing whether the *content* is useful, not polishing a release
  pipeline.
- **A lightweight Python package** (`pip install axiom-dev-kit` or
  similar, providing the knowledge-API CLI/library only — not the
  skill, which stays a template-copied file) is **the second-choice
  mechanism for the knowledge API specifically**, worth adopting once
  more than one consumer needs it, so the CLI/library has one
  canonical version instead of N copy-pasted ones. **Not built in
  Phase 2**: packaging the API now, before a second real consumer
  exists to need it, would be exactly the "build generality before a
  real use case demonstrates the need" mistake this assignment's §2.B
  warns against. Stage 2.5 (template extraction) is the right point to
  revisit this, once Stage 2.4's dogfooding has shown what the API
  actually needs to export.
- **A shared/distributed Claude-Code-specific skill package** is
  rejected for now for the same reason, and because it would make the
  skill itself the distribution unit, coupling Axiom's portability to
  Claude Code's own plugin mechanism — contrary to §4's explicit
  requirement that Claude-specific integration stay "a convenient
  initial adapter, not Axiom's canonical architecture."

**Decision for Phase 2: template copy for the skill and wiki
scaffolding; defer packaging the API until Stage 2.5 or later, against
a demonstrated second-consumer need.**

## 6. The skill itself

```
.claude/skills/axiom-work/SKILL.md
```

Frontmatter (per the researched, currently-supported fields):

```yaml
---
name: axiom-work
description: >
  Guides a bounded development change through Axiom's evidence-based
  lifecycle (UNDERSTAND -> SPECIFY -> ASSESS IMPACT -> BUILD -> VERIFY
  -> RECONCILE): reads project governance and current plan, retrieves
  relevant scoped knowledge with its evidence status, checks for
  source-change impact on existing claims, and reconciles documentation
  and claims after the change. Use when starting, continuing or closing
  out a development task that this project's Axiom knowledge covers.
---
```

Body (kept concise; references, does not duplicate, project files —
this is the actual target shape, not merely a description of one):

```markdown
# Axiom development work

This skill guides one bounded change through this project's
development lifecycle. It does not replace project governance — read
and follow `AGENTS.md` (or this project's equivalent) and the current
plan in `planning/CONTEXT.md` (or equivalent) first; this skill adds
knowledge retrieval and evidence discipline on top of them.

## Before starting (UNDERSTAND / SPECIFY)

1. Read the project's own governance file and current plan/context —
   do not assume a prior session's summary is still accurate.
2. **Choose a short task ID for this unit of work and record it before
   any retrieval**: `axiom-knowledge task-start --task-id <id>`.
   Required, not optional — task identity cannot be inferred
   automatically (`planning/phase-02-measurement-design.md` §1–§2),
   and every subsequent command in this skill carries `--task-id <id>`
   so retrieval, overhead and usefulness can actually be measured per
   task, not just logged with no way to group the events back
   together.
3. If relevant existing knowledge may exist, retrieve it:
   `axiom-knowledge get <id> --task-id <id>` or `axiom-knowledge find
   "<query>" --task-id <id>` (see `knowledge/README.md` for where this
   project's claims live — its own existing register, if one exists,
   takes priority over a generic `knowledge/claims/` default).
4. Distinguish the claim's evidence status
   (INTENDED/OBSERVED/VERIFIED/UNCERTAIN/CONTESTED, or this project's
   own equivalent taxonomy if it has one already) from your own
   confidence. A retrieved claim being VERIFIED for one scope does not
   make it VERIFIED for a different scope or a different source
   version — check what it was actually verified against.

## Before changing code (ASSESS IMPACT)

5. If the change touches a source a recorded claim depends on, run
   `axiom-knowledge impacted <changed-paths> --task-id <id>` and read
   what comes back as *potentially* affected, not proven stale.
   **Availability note, added per native Codex review of PR #5's
   finding on this exact step**: `impacted` is a Stage 2.3 deliverable
   (`planning/phase-02-stage-2.2-plan.md` §2a explicitly builds only
   `get`/`find` in Stage 2.2). If this command does not yet exist in
   the installed `axiom-knowledge`, **skip this step and say so
   explicitly** rather than silently treating "ASSESS IMPACT" as
   satisfied — do not guess at impact by other means and call it
   equivalent.

## While developing (BUILD / VERIFY)

6. Develop against an independently specified contract/oracle, not one
   derived from your own new code.
7. Run this project's deterministic checks directly; report what
   actually ran and its actual result. Request independent review
   named at the isolation level actually used (see this project's own
   isolation-level documentation if present). **Availability note,
   added for the same reason as step 5**: a dedicated test-runner
   wrapper emitting `test_result` events
   (`planning/phase-02-measurement-design.md` §1) is not part of
   Stage 2.2's own delivery scope either — until one exists, run the
   project's actual test command directly and report its real output;
   do not fabricate a `test_result` event for a check that was not
   actually wrapped.

## After the change (RECONCILE)

8. Update affected claims/evidence in the same change, through an
   ordinary commit/PR — never by having this skill or any agent write
   directly to a claim's authoritative file without that normal review
   path.
9. Report unresolved uncertainty and verification limitations
   explicitly; do not let a passing test or a clean schema check stand
   in for semantic correctness. If this task's acceptance criteria are
   confirmed met, record it: `axiom-knowledge task-accepted --task-id
   <id>`.
```

This is short by design (well under the ~500-line guidance) and
**names operations, it does not implement them** — `axiom-knowledge`
is the CLI specified in `planning/phase-02-knowledge-api-design.md`,
built once, invoked the same way by this skill, by a human at a
terminal, or by a non-Claude agent (§7 below).

## 7. Non-Claude-agent equivalence

Nothing above is Claude-specific except the SKILL.md frontmatter/
loading mechanism itself. The actual operations (`get`/`find`/`related`/
`impacted`, the deterministic CLI, the event log) are plain
command-line tools any agent or human can invoke, and the lifecycle
guidance in the skill body is prose any agent (or developer) can read
directly from the project's own `AGENTS.md`-equivalent file — the
skill is a convenience wrapper that surfaces that guidance
automatically inside Claude Code, not a separate source of truth. A
non-Claude agent loses only the automatic surfacing, not any
capability.

## 8. One skill, assessed as sufficient for Phase 2

A single skill is proposed, not several specialised skills (explicit
non-goal, authorising prompt §14). The lifecycle above has five
sub-steps, but they are one coherent flow for one unit of work, not
independent concerns needing separate activation triggers. Splitting
by lifecycle phase (e.g. a separate "axiom-verify" skill) is deferred
until Stage 2.4's dogfooding shows a real reason one phase needs
different tool access or framing than the rest — no such reason is
evident yet.

## 9. Architecture diagram

**Merged into this document in this revision** (previously a separate
file, `planning/phase-02-architecture.md` — removed as pure
duplication of what §1–8 above already specify; a diagram of this
design belongs beside the design, not in a document a reader has to
separately locate and cross-reference).

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
                    │  │   SKILL.md  (§6 above)             │     │
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
                    │ │  wiki/claims/ │  │  events.jsonl         │  │
                    │ │  (default —   │  │ (gitignored,          │  │
                    │ │  OR an        │  │  per-checkout only)   │  │
                    │ │  existing     │  └─────────────────────┘  │
                    │ │  register,    │                            │
                    │ │  e.g.         │                            │
                    │ │  Ledgerkit's  │                            │
                    │ │  compat-      │                            │
                    │ │  register/)   │                            │
                    │ └──────┬───────┘                            │
                    │        │ versioned by                        │
                    └────────┼────────────────────────────────────┘
                             ▼
                    ┌─────────────────────────────────────────┐
                    │  Git  (authoritative store, only write     │
                    │  path — commits/PRs, not an API call)       │
                    └────────────────┬────────────────────────┘
                                      │ triggers
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │  CI — schema/identity/reference integrity, │
                    │  changed-source -> impacted() report,       │
                    │  deterministic test suite (existing CI,     │
                    │  no new orchestration)                      │
                    └────────────────┬────────────────────────┘
                                      │ surfaces findings for
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │  Independent verification (fresh-context    │
                    │  agent or human; isolation level named      │
                    │  honestly) — establishes actual correctness;│
                    │  CI alone never does                        │
                    └─────────────────────────────────────────┘

              ┌───────────────────────────────────────────────┐
              │  Future, optional, Phase 3 (NOT built in         │
              │  Phase 2, not a Phase 2 dependency): a thin MCP   │
              │  adapter wrapping axiom-knowledge read-only, and  │
              │  Axiom Assure's controlled A/B of agent/retrieval │
              │  strategies, using the same stable IDs as data.   │
              └───────────────────────────────────────────────┘
```

**Relationships stated explicitly:** the consuming repository owns
its governance and knowledge files outright, not Axiom. The skill is
the only Claude-Code-specific component and calls the CLI exactly as
a human or non-Claude agent would — no hidden channel bypasses it. The
CLI is the only thing that reads/writes structured knowledge data, and
never writes without a human/agent committing through Git (the event
log's "appends" is the one exception, and that log is explicitly not
the knowledge store). CI and independent verification are kept as two
separate boxes on purpose — conflating "CI passed" with "verified" is
the exact mistake ADR 0008 Decision 5 warns against. The Phase 3 box
is drawn separately to make it visually obvious that removing it
entirely still leaves a complete, functioning Phase 2 system above.

**Complexity-budget check:** no component above is a database, a
persistent background service, a write-capable API, an autonomous
knowledge generator, an embedding index, or a dashboard. Every box
maps to a justification already given in §1–8 above.
