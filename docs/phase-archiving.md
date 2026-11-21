# Phase archiving

The procedure for moving a **Completed** phase's detail out of the
active `planning/ROADMAP.md`/`planning/CONTEXT.md` into
`planning/archive/`, while keeping it reachable and verifiable. Purpose:
preserve evidence and historical decisions without letting the active
roadmap and session context grow without bound as phases finish
(`planning/prompts/004-documentation-schema-and-roadmap-amendment.md`
§9).

**This procedure has not yet been run for real.** It is established and
tested against the mechanism available to check it (see Verification
below), but no phase has actually been archived — Phase 1 is explicitly
not eligible yet (see Non-goals). Writing this procedure now, before a
real archiving, follows the same contract-first discipline
`decisions/0004` established for the validator: define the requirement
before the first real use, so the first real use is checked against
something, not invented as it happens.

## Archive structure

```
planning/
    ROADMAP.md
    CONTEXT.md
    phase-01-foundation.md
    archive/
        README.md              <- top-level index, lists every archived phase
        phase-01/
            README.md           <- one phase's archive entry
```

Logical, not physical: archiving does **not** move the original phase
plan (`planning/phase-01-foundation.md` stays at its established
canonical path). `planning/archive/phase-NN/README.md` is a new,
separate index entry that *links to* the existing plan, evidence, ADRs
and contracts — it does not duplicate or relocate them. "Logical
archiving is preferred to unnecessary file relocation"
(`planning/prompts/004-...md` §9) — moving a plan's canonical path is a
separately reviewed decision of its own, not a side effect of archiving.

## Archive entry contents

Each `planning/archive/phase-NN/README.md` states, at minimum: phase
number and title; objective; actual completion status and date; accepted
scope; completion evidence (links, not copies); independent closeout
findings (summary + link); relevant ADRs (links); associated contracts
(links); retrospective (link); the final approved PR or commit that
closed the phase; important limitations or deferred work; links to the
phase's own plan and other historical artifacts.

**An archive entry is an index, not a duplicated knowledge store** — it
never copies the full text of a contract, evidence file, or ADR. If a
link breaks, that is a real defect (see Verification below), not
something the archive entry should work around by inlining a copy.

## Phase completion procedure

1. **Verify.** Run deterministic checks and the independent review the
   phase's own plan requires. Compare results against the accepted
   completion criteria (not criteria invented after the fact). Identify
   outstanding defects, incomplete requirements, and uncertainties —
   explicitly, not silently absorbed into a generic "looks done."
2. **Close out.** Produce an independent closeout assessment: which
   acceptance criteria were met, which were not, and the evidence for
   each conclusion (`AGENTS.md` §6) — exactly the practice
   `evidence/phase-1-closeout.md` already demonstrates for Phase 1,
   which found it *not* ready to close.
3. **Obtain human approval.** A phase is never marked Completed because
   an agent believes its work is finished — human approval is required
   (`AGENTS.md` §11), regardless of how complete the closeout assessment
   looks.
4. **Reconcile.** Update the roadmap, session context, contracts,
   documentation and evidence to reflect the accepted final state.
   Unfinished work is explicitly deferred, rejected, or transferred to a
   later phase in writing — never silently dropped.
5. **Archive.** Create `planning/archive/phase-NN/README.md` with the
   content listed above. Record the accepted completion commit/PR and
   the closeout's scope. The original phase plan stays at its canonical
   path (see Archive structure) unless a *separately reviewed* migration
   specifically justifies moving it.
6. **Update the active roadmap.** Reduce the phase's `planning/ROADMAP.md`
   entry to a short summary plus a link to its archive entry. The phase
   stays visible as **Completed** in the roadmap — archiving removes
   detail, not visibility. Detailed historical narrative moves to the
   archive entry (by link), not to a longer roadmap paragraph.
7. **Prepare the next phase.** Update `planning/CONTEXT.md`: current
   active phase, current implementation baseline, relevant accepted
   decisions, outstanding issues, next concrete action. The next phase
   still needs its own accepted implementation plan before substantive
   work begins (`AGENTS.md` §2) — archiving the previous phase is not,
   by itself, authorisation to start the next one.

## Verification

Proportionate, reusing existing mechanisms rather than building new
ones (`planning/prompts/004-...md` §9: "do not build an archival
database or bespoke project-management system"):

- **Archive entries link to real artifacts, not broken or duplicated
  ones.** `planning/archive/README.md` and every `phase-NN/README.md`
  are schema-bearing documents on `docs/governed-documents.txt`, so the
  existing validator's link-resolution and required-sections checks
  (`contracts/documentation-schema-validator.md` rules 4, 6) already
  cover this — no new checking code needed. A broken link in an archive
  entry fails CI the same way a broken link anywhere else does.
- **No unfinished phase is archived as Completed.** This is a procedural
  check (step 2/3 above, human-approved), not a mechanical one — whether
  a phase's evidence actually supports "Completed" requires judgement an
  automated check cannot make. Named here as semantic/editorial
  (`docs/knowledge-placement.md` "Enforcement classes," level 6), not
  overclaimed as automated.
- **Archived phases are marked Completed in the roadmap.** Checked by
  the same independent review that checks everything else in this
  project (`AGENTS.md` §6) at archiving time — a roadmap entry that says
  "In progress" with an archive link would be caught the same way any
  other documentation-drift finding is.
- **Active documentation does not depend on silently duplicated
  historical records.** Enforced by the archive-entry convention itself
  (link, don't copy) plus ordinary review — not a new mechanical check.

## Non-goals

- Does not archive Phase 1. Phase 1 is explicitly not eligible —
  `planning/prompts/004-...md` §9: "Do not archive Phase 1 yet. Phase 1
  remains open until its outstanding requirements... are satisfied." See
  `planning/ROADMAP.md` for Phase 1's actual open items.
- Does not create `planning/archive/phase-01/` or any other phase
  subdirectory speculatively. `planning/archive/README.md` exists (this
  change) as the empty top-level index; no phase-specific subdirectory
  exists until a real phase is actually archived.
- Does not build a database, dashboard, or any tooling beyond the
  existing validator and ordinary review — archiving is a documented
  human/agent procedure using Markdown, Git, and the mechanisms this
  project already has.
