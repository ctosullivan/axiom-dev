# 0001. Development governance and repository methodology

## Status

Accepted — 2026-11-21

## Context

Axiom Dev needs a development methodology from its first commit, because
the methodology itself is the thing Axiom Dev is trying to validate
(`planning/prompts/001-phase-1-bootstrap.md` §2, fundamental hypothesis).
The bootstrap prompt authorises adopting the lifecycle
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE and a set
of mandatory practices (planning-before-implementation, ADRs, roadmap
tracking, session continuity, agent instructions, retrospectives,
documentation sync, independent closeout).

Axiom follows an earlier project, CodeCompass
(`~/projects/codecompass`), whose governance apparatus we inspected
directly rather than assumed. Concretely, as of this inspection
(2026-11-21): CodeCompass has 97 ADRs under `decisions/`, roughly 115
per-phase planning files under `planning/phase-*.md`, and on the order of
190 retrospective/audit files under `planning/retros/` (including separate
`*-audit-phase-N`, `*-drift-audit-phase-N`, and `*-domain-skeptic-review`
files per phase). Several ADRs exist purely to amend a very recent prior
ADR in place before it had seen real use (e.g. `decisions/0066` was edited
three times the same day it was created; `decisions/0067` and `0068` are
both "corrective pass" amendments to the same phase; `decisions/0081`
through `0083` are first/second/third/"final" corrective passes on one
decision). `planning/milestone-closeout-checklist.md` had its own phase
numbers wrong in its header and needed correcting twice after phase
renumbering — governance documents drifted too, not just code docs.

At the same time, CodeCompass's `CLAUDE.md` and `CONTRIBUTING.md` contain
specific practices that worked and are worth keeping: a plan-before-code
gate naming scope, non-goals, files touched and verification method per
phase (`CLAUDE.md` §1); same-commit documentation synchronisation across
`docs/`, `decisions/`, `CONTEXT.md` and `ROADMAP.md` (`CLAUDE.md` §2); a
read-only, non-repairing independent closeout role whose pass is voided by
any later commit (`CLAUDE.md` §5); and an append-only ADR convention where
a reversed decision gets a new numbered ADR rather than an edit — the
concrete working example being `decisions/0061`
("decisions-0019-superseded-by-0035").

## Decision

Axiom Dev adopts:

1. The UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE
   lifecycle as binding on its own development (`AGENTS.md` §1).
2. Mandatory planning before implementation, with one focused plan per
   phase/stage rather than an aspirational full-project plan written once
   (`AGENTS.md` §2).
3. Sequentially numbered, append-only ADRs, restricted to genuinely
   non-obvious decisions, with reversals recorded as new superseding ADRs,
   never in-place edits (`AGENTS.md` §3).
4. A single roadmap (`planning/ROADMAP.md`) with six honest states
   (Proposed/Planned/In progress/Completed/Deferred/Blocked), where
   Completed requires independent closeout evidence, not just finished
   work (`AGENTS.md` §4, §6).
5. A current-state-only session continuity file (`planning/CONTEXT.md`)
   kept separate from historical narrative, which belongs in retros and
   VCS history instead.
6. Proportionate retrospectives — one file per completed phase under
   `planning/retros/`, not a parallel taxonomy of separate audit files per
   phase.
7. Same-commit documentation synchronisation for any change affecting
   behaviour, architecture, interfaces, or established knowledge
   (`AGENTS.md` §5).
8. One canonical agent-instructions file (`AGENTS.md`), with
   provider-specific files (`CLAUDE.md`) containing only necessary
   adaptations, never competing or restated instructions.

## Alternatives considered

- **Adopt CodeCompass's governance structure as-is.** Rejected: the scale
  evidence above (97 ADRs, ~115 phase files, ~190 retro/audit files, and
  the same-day multi-amendment ADR pattern) shows this volume became
  process overhead in its own right rather than a cost paid once for
  lasting clarity — exactly the kind of overhead Axiom Dev's own fundamental
  hypothesis requires it to avoid defaulting into.
- **No formal governance; rely on commit messages and memory.** Rejected:
  this is the failure mode Axiom Dev exists to address (agents are
  transient; project knowledge must compound in artifacts, not in any one
  session's memory).
- **A fixed, pre-committed roster of specialist agent roles**, as
  CodeCompass did (`decisions/0049-agent-led-development-model.md`,
  originally fixed at 7 roles, pruned at a named gate). Rejected for now:
  CodeCompass's own Phase 43c added an 8th role anyway, despite the
  fixed-and-pruned design — evidence that a roster fixed before real work
  doesn't survive contact with real work. Axiom Dev's agent responsibilities
  (`decisions/0003`) are described by function, not by a committed list of
  named roles.

## Rationale

The chosen governance is deliberately lighter than CodeCompass's, sized to
what Phase 1 Stage 1.0 actually needs, with explicit room to add weight
later only if a demonstrated requirement justifies it (per the bootstrap
prompt's own instruction not to recreate CodeCompass's record hierarchy
without demonstrated need). The practices retained are the ones CodeCompass
evidence shows actually earned their cost; the practices excluded are the
ones CodeCompass's own later files show became churn (corrective-pass ADR
thrashing) or sprawl (the retros/audit file count) rather than value.

## Consequences

- Phase work will feel slower up front (a plan and, where warranted, an ADR
  before implementation) in exchange for traceability that survives a
  session boundary.
- There is a real risk of regressing toward CodeCompass's volume if ADR and
  retro discipline aren't actively held to "genuinely non-obvious" and
  "proportionate" — this ADR is itself the reference point for judging that
  later.
- Agent responsibilities are deliberately not fixed into a named roster yet
  (see `decisions/0003`); this is revisited if and when a stage
  demonstrates a specific, recurring need for one.

## Relevant evidence

- `~/projects/codecompass/CLAUDE.md` §1, §2, §5 (plan-before-code,
  same-commit doc sync, independent audit role).
- `~/projects/codecompass/decisions/0061-...md` (append-only supersession
  pattern in practice).
- `~/projects/codecompass/decisions/0066...md`, `0067`, `0068`, `0081`,
  `0082`, `0083` (same-day/multi-pass ADR amendment pattern — the
  overhead this ADR decides against).
- `~/projects/codecompass/decisions/0049-agent-led-development-model.md`
  (fixed roster, later broken by Phase 43c adding an 8th role).
- `~/projects/codecompass/planning/milestone-closeout-checklist.md`
  (governance document header drift, corrected twice).
- Directory counts (`ls decisions/`, `ls planning/phase-*.md | wc -l`,
  `planning/retros/`) taken directly from the CodeCompass working tree on
  2026-11-21.
- `planning/prompts/001-phase-1-bootstrap.md` (the authorising prompt).

## Supersession

None. This is the first ADR.
