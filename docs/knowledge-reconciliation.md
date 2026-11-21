---
audience: anyone landing a change that touches behaviour, decisions, interfaces, or documented knowledge
purpose: define the procedure for checking documentation and knowledge records against a real change, and prove it's been run at least once
required_sections: [Procedure, Worked example]
authoritative_sources: [AGENTS.md, docs/knowledge-placement.md]
acceptance_criteria:
  - the procedure is concrete enough to follow without inventing steps
  - a real reconciliation pass against this repository is recorded below, not just described abstractly
---

# Knowledge reconciliation

This is the full procedure behind the "Reconciliation hook" named in
`docs/knowledge-placement.md`.

## Procedure

1. **Diff.** List every file changed in the unit of work being
   reconciled (a commit, a PR, or — for this first run — a whole stage).
2. **Dependents.** For each changed file, list every other file whose
   claims assume the old state: cross-references (`§` citations, relative
   links), status tables (`planning/ROADMAP.md`), and any document whose
   `authoritative_sources` front-matter field names the changed file.
3. **Check.** For each dependent, confirm its claim still holds against
   the new state. Three outcomes per dependent: still true (no action),
   false and fixed now (record what changed), or false and deliberately
   left open (record why, and where the open item is tracked).
4. **Record.** Write a short reconciliation note — what was checked, what
   was found, what was fixed — either inline (as a changelog/log entry) or
   as its own evidence entry if the findings are substantial enough to
   warrant one.
5. **No silent gaps.** If a dependent can't be checked (e.g. the checker
   doesn't have access to something), that's recorded as UNCERTAIN
   (`docs/knowledge-placement.md` classification), not skipped silently.

## Worked example

Run on 2026-11-21, reconciling the Stage 1.0 → Stage 1.1 (partial)
transition — i.e., checking everything Stage 1.0 established against the
changes this amendment and Stage 1.1's first real content just made.

**1. Diff:** `planning/phase-01-foundation.md` (amendment: §0 added, Stage
1.3/1.4 extended, §9/§10 added), `decisions/0004` (new), `planning/prompts/002-...md`
(new), `evidence/phase-1-log.md` (new), `docs/knowledge-placement.md`
(new), `docs/documentation-schema.md` (new), `contracts/documentation-schema-validator.md`
(new), `README.md` (front-matter added, status line updated, repository
map extended), `planning/ROADMAP.md` (Stage 1.1 status, directories-list
updated).

**2. Dependents found:**
- `planning/CONTEXT.md` — claims current phase/status and next action;
  assumes Stage 1.0-only state.
- `AGENTS.md` §7 — the short placement table; now has a full version in
  `docs/knowledge-placement.md` that must not contradict it.
- `decisions/0002` — "Unresolved: exact schema sidecar format" — now
  resolved by `docs/documentation-schema.md`; the ADR itself is
  append-only (can't be edited), so the resolution lives in the newer
  document, which cites `decisions/0002` back.

**3. Check:**
- `planning/CONTEXT.md`: claim "Stage 1.0 — In progress... next action:
  open the PR" no longer reflects that Stage 1.1 work has also started.
  **False, fixed** — see the `planning/CONTEXT.md` update in this same
  change.
- `AGENTS.md` §7 vs. `docs/knowledge-placement.md`: both tables list the
  same seven/nine categories with the same artifact mapping (the full
  version adds two rows — `planning/CONTEXT.md` and
  `planning/retros/`/history — that the short version doesn't need to
  enumerate). **No contradiction found.**
- `decisions/0002` Unresolved item: still correctly says "unresolved" as
  of when it was written (ADRs are historical and not edited) — the
  resolution is a new fact recorded in `docs/documentation-schema.md`,
  which explicitly says it resolves that item. **Consistent by design**,
  not a drift — this is exactly what "historical reasoning is not current
  justification" (`docs/knowledge-placement.md`) is for: the ADR records
  what was true then, the newer doc records what's true now, and each
  says so.

**4. Recorded:** this worked example is the record. The one real fix (
`planning/CONTEXT.md`) is applied in the same change as this document.

**5. No silent gaps:** none identified in this pass — all dependents
found in step 2 were checked. Future reconciliation passes may find more
as the repository grows; this is a demonstrated procedure, not a claim
that documentation will never drift again.

**Limitation, stated honestly:** this first run is a real reconciliation
pass with a real finding and a real fix, but it is a weak test of the
procedure's value — the drift it found (`planning/CONTEXT.md` going
stale) was introduced and discovered within the same session, not drift
that survived a session boundary unnoticed. A stronger test is Stage 1.5's
independent reconstruction, run from a genuinely fresh context after real
time and real changes have passed.
