# 0004. Phase 1 amendment — anti-circular verification, measurement, and acceptance demonstrations

## Status

Accepted — 2026-11-21

## Context

A second authorising prompt
(`planning/prompts/002-phase-1-amend-and-implement.md`) superseded the
bootstrap-only restriction from `decisions/0001`–`0003` and required the
existing Phase 1 plan to be *amended* (not replaced) along four axes:

- **Amendment A** — confirm bootstrap overhead is actually minimised, not
  merely intended to be.
- **Amendment B** — the self-development exercise in Stage 1.4 as
  originally planned (`planning/phase-01-foundation.md` §4, prior
  revision) required contracts-before-implementation and independent
  review, but did not mechanically prevent an implementer from quietly
  editing its own accepted fixtures, did not separate test results from
  review findings from human acceptance, and did not require a defect
  ledger. Prompt 002 names this risk directly: "a reviewer repeating the
  implementer's assumptions is not sufficient independent assurance."
- **Amendment C** — the prior plan deferred all measurement to a later,
  unspecified point ("later controlled comparisons must establish whether
  it outperforms simpler alternatives" was already present, but nothing
  recorded effort/defects/reuse *during* Phase 1 itself).
- **Amendment D** — the prior plan's exit criteria were stage-shaped
  ("Stage 1.3 exit: real GitHub PR evidence...") but did not state, as a
  single cross-cutting list, the demonstrations prompt 002 now requires
  explicitly (fresh-agent resume, instruction-to-verification traceability,
  a rejected defective PR, preserved refactor behaviour, placement/doc
  consistency against real changes, independent reconstruction, knowledge
  reuse across stages, recorded overhead).

This is itself a direct application of `decisions/0001`'s append-only ADR
rule: none of `decisions/0001`–`0003` are edited in place by this change;
this ADR records what's added/changed and why.

## Decision

1. **Amendment A:** assessed, not re-architected. The existing plan
   (`decisions/0001`) already satisfies essentially all of Amendment A's
   sub-requirements (concise single-purpose files, `AGENTS.md` canonical,
   `CLAUDE.md` thin, ADRs restricted to real decisions, minimal directory
   creation, proportionate retros, no fixed roster). The one addition: a
   named rule that no stage may describe a capability as OBSERVED/VERIFIED
   ahead of it actually running for real (`planning/phase-01-foundation.md`
   §0).
2. **Amendment B:** Stage 1.3 is split into a deterministic policy
   evaluator (locally buildable/testable, no external credentials needed)
   and a live GitHub/Codex integration (which may be blocked by missing
   credentials/access/cost-authorisation, and must be reported as such,
   not simulated around). Stage 1.4 adopts concrete anti-circularity
   mechanics: pre-implementation independent review of contracts/fixtures,
   valid-and-defective fixture pairs, checksum-recorded accepted fixtures
   where an undocumented change is a flagged verification failure
   (a **procedural** control today, not a mechanical one — it becomes
   mechanical only once something actually computes and compares the
   checksum automatically; see
   `planning/phase-01-foundation.md` §4 Stage 1.4 for the honesty
   requirement this is held to, matching `decisions/0003` §3's own
   standard for isolation claims), fresh-context evaluation of the
   initial implementation, a captured pre-refactor baseline, identical
   before/after test runs, an explicit detected/missed/introduced defect
   ledger, and hard separation of test results vs. independent-review
   findings vs. human acceptance as distinct evidence artifacts.
3. **Amendment C:** `evidence/phase-1-log.md` is created now and begins
   recording real data from this amendment forward (not retroactively for
   already-completed Stage 1.0 work). It records only what is actually
   observable in this environment and says so explicitly where a
   requested metric (e.g. real billing figures) isn't available, rather
   than estimating and presenting an invented number as measured.
4. **Amendment D:** eight explicit demonstrations are tracked as a single
   table (`planning/phase-01-foundation.md` §10), each mapped to the stage
   that produces it, defaulting to "Not yet demonstrated" until real
   evidence lands. Phase 1 (§7) cannot close while any row remains
   undemonstrated without an explicitly recorded, genuine blocker.

## Alternatives considered

- **Treat the amendment as a new, separate plan.** Rejected: prompt 002
  explicitly requires amending the existing plan rather than creating a
  competing one, and a second plan would fragment the single authoritative
  source `decisions/0001` already established.
- **Simulate the Stage 1.3 live gate locally to avoid reporting a
  credentials blocker.** Rejected: prompt 002 §9 is explicit — "a local
  simulation cannot substitute for a required real GitHub merge-gate
  demonstration" — and this project's own fundamental hypothesis depends
  on not manufacturing evidence.
- **Defer measurement (Amendment C) until Stage 1.4 produces something
  worth measuring.** Rejected: prompt 002 explicitly requires measurement
  "from the beginning," and the amendment process itself (this ADR, the
  plan edit, the independent review that follows) is itself a measurable
  unit of development effort worth logging as the first entry.

## Rationale

Each amendment closes a specific, named gap rather than adding generic
rigor: Amendment B's checksum-recorded-fixture procedure gives
"cannot silently modify" a concrete, checkable artifact (a recorded
checksum a reviewer actually compares) rather than leaving it as a
restatement of the existing "contracts aren't weakened unilaterally"
rule — it is a real improvement in checkability, honestly scoped as
procedural rather than overclaimed as mechanical. Amendment D's table turns
eight prose requirements into a trackable, falsifiable checklist rather
than leaving "fresh agent can resume" as an assumption nobody has to
actually test.

## Consequences

- Stage 1.3's acceptance criterion is now explicitly two-part, and it is
  acceptable (per prompt 002 §9) for the live-integration part to remain
  open with a recorded blocker — this ADR pre-authorises reporting that
  blocker rather than treating an unmet live-gate criterion as a reason to
  fabricate evidence.
- Stage 1.4's implementation now carries real process overhead (fixture
  checksums, pre-implementation independent review, defect ledger) beyond
  what `decisions/0001` originally scoped — this is deliberate, in
  direct response to Amendment B's named failure mode, and its cost is
  itself logged per Amendment C.
- The Amendment D table is a standing, visible "not yet demonstrated" list
  until Stage 1.5 closes — this is intended to make partial-Phase-1-completion
  reporting the default honest state, not an exceptional admission.

## Relevant evidence

- `planning/prompts/002-phase-1-amend-and-implement.md` §4 (Amendments
  A–D, verbatim).
- `planning/phase-01-foundation.md` §0, §4 (Stage 1.3/1.4), §9, §10 (the
  amended plan sections this ADR authorises).
- `decisions/0001`–`0003` (unedited; this ADR extends, does not revise,
  them).

## Supersession

None. This ADR extends `decisions/0001`–`0003`; it supersedes no prior
ADR. If a future amendment materially reverses any of the above, that
reversal gets its own ADR referencing this one.
