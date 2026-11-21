# Development lifecycle

Expands `AGENTS.md` §1's six-word summary into entry/exit criteria per
step, so a stage can actually be executed against this document without
a session having to invent the missing procedure mid-stage — the gap
Stage 1.2 exists to close (`planning/phase-01-foundation.md` §4, Stage
1.2).

## Lifecycle

### UNDERSTAND

- **Entry:** a stage or change is proposed (roadmap entry, prompt, or
  review finding).
- **Do:** read the current implementation, knowledge, and documentation
  baseline directly — not from memory of a prior session.
- **Exit:** a concrete statement of current state exists, citing the
  files actually read (not "the codebase," but which files).

### SPECIFY

- **Entry:** UNDERSTAND's exit artifact exists.
- **Do:** write a version-controlled plan (`AGENTS.md` §2) naming
  objective, scope, non-goals, dependencies, files, contracts/acceptance
  criteria, verification method, documentation implications, completion
  criteria.
- **Exit:** the plan exists in `planning/` and, for Stage 1.4-type work,
  its contracts/fixtures have been independently reviewed *before* BUILD
  starts (`decisions/0004`, Amendment B).

### ASSESS IMPACT

- **Entry:** a plan exists.
- **Do:** identify every existing contract, documentation file, decision,
  and knowledge record the change touches (the same "dependents" step as
  `docs/knowledge-reconciliation.md`'s procedure, run prospectively here
  instead of retrospectively).
- **Exit:** the plan's "documentation and knowledge implications" section
  names the actual files that will need to change, not a generic
  statement that docs will be "updated as needed."

### BUILD

- **Entry:** plan exists, impact assessed.
- **Do:** implement to the plan. Revisions to the plan are recorded, not
  silently absorbed (`AGENTS.md` §1).
- **Exit:** the bounded change is complete and matches the plan's stated
  scope — scope creep during BUILD is a SPECIFY revision, not a BUILD
  decision made unilaterally.

### VERIFY

- **Entry:** BUILD's output exists.
- **Do:** produce evidence — tests where code exists, independent review
  always, direct inspection of the actual artifact. The implementer's own
  summary is never sufficient evidence on its own (`AGENTS.md` §6).
- **Exit:** evidence exists in `evidence/` or the relevant plan/ADR,
  stating what was checked, how, and by what isolation level
  (`docs/agent-isolation.md`).

### RECONCILE

- **Entry:** VERIFY's evidence exists.
- **Do:** update affected documentation and knowledge records in the same
  change (`AGENTS.md` §5); run the reconciliation procedure
  (`docs/knowledge-reconciliation.md`) against what actually changed.
- **Exit:** `planning/ROADMAP.md` and `planning/CONTEXT.md` reflect the
  real state; no claim anywhere describes something as done that this
  cycle didn't actually establish.

A cycle's exit criteria are the next cycle's entry criteria — there is no
step that can be skipped by asserting its predecessor's work was "good
enough."

## Phase acceptance and reconciliation

This is the concrete answer to "how does a stage actually get marked
Completed in `planning/ROADMAP.md`" (`planning/phase-01-foundation.md`
§4, Stage 1.2 scope):

1. **Who: whoever authors the stage's plan** (the implementing agent or
   session, same actor §2 "Plan before implementation" names) — the
   stage's own plan (in `planning/phase-01-foundation.md` or a dedicated
   stage plan) states its completion criteria in advance, not invented
   retroactively to match whatever got built.
2. **Who: an independent reviewer** — a fresh-context agent (or a human,
   if one is reviewing directly) — runs against the actual artifacts
   (not the implementer's summary), at the isolation level actually
   available, named explicitly (`docs/agent-isolation.md`). Never the
   same actor as step 1 for the same stage, even under best-effort
   isolation.
3. **Who: the implementing agent/session** — resolves material findings:
   fixed, or explicitly accepted with reasoning recorded (as in
   `planning/phase-01-foundation.md` §6, §11), before anyone acts on
   step 4.
4. **Who: an agent prepares; a human confirms.** Only after 1–3:
   `planning/ROADMAP.md`'s status for that stage changes to Completed,
   and `planning/CONTEXT.md`'s "next concrete action" moves to the next
   stage. This edit is itself a human-approval-boundary action
   (`AGENTS.md` §11) — an agent can prepare the edit and point to the
   evidence; a human confirms it.
5. **Who: whoever is updating the roadmap** (same actor as step 4) — if
   a stage's acceptance criteria are not fully met, states so honestly
   (Blocked, or still In progress with the open item named) — never
   Completed with a caveat buried in prose.
