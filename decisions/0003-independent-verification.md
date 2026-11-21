# 0003. Independent verification and agent responsibilities

## Status

Accepted (partial — see Unresolved) — 2026-11-21

## Context

The bootstrap prompt (`planning/prompts/001-phase-1-bootstrap.md` §5, §6,
§9 Step 7) requires: independent responsibilities for specification,
implementation, verification, PR review, documentation reconstruction and
knowledge reconciliation; an honest account of whether isolation between
these is technically enforced or merely best-effort; a mandatory Codex
PR-review CI gate planned (not built) for Phase 1; and an independent
review of the bootstrap foundation itself before it is committed.

CodeCompass precedent:

- `CLAUDE.md` §5 defines a `release-phase-auditor` role that is read-only,
  never repairs what it audits, and whose pass is voided by any commit made
  after it ran — a producer-is-never-the-verifier design that held up in
  practice.
- `decisions/0049-agent-led-development-model.md` originally fixed a
  roster of specialist agent roles (7, "pruned at GATE DA"); CodeCompass's
  own Phase 43c later added an 8th role anyway. The fixed-roster design did
  not survive contact with real work.
- `decisions/0066-clean-room-reconstruction-needs-mechanical-isolation-and-independent-implementation-comparison.md`
  and `decisions/0076-cleanroom-broker-gives-a-capability-not-a-credential.md`
  describe what *technically enforced* isolation actually requires for
  clean-room documentation reconstruction: a broker that grants a scoped
  capability rather than a shared credential, and mechanical (not merely
  prompt-based) separation between the reconstructing agent and the
  original implementation context.

For this bootstrap itself: the independent review in step 7 is dispatched
by the same session, same operator, and same underlying model that
produced the material under review. That is not strict isolation by
`decisions/0066`'s own standard — no mechanical barrier prevents context
leakage, only the practical fact that a fresh agent instance starts with no
prior conversation history. This limitation is recorded in
`planning/phase-01-foundation.md`'s review record rather than left
implicit.

## Decision

1. Agent responsibilities for Axiom Dev are described by **function**, not
   by a pre-committed named roster: specification/research,
   implementation, independent verification, PR review, documentation
   reconstruction, and knowledge reconciliation are distinct
   responsibilities that must not be collapsed onto the same actor for the
   same piece of work — but no fixed list of named agent roles is adopted
   at bootstrap. A roster may emerge later if a stage demonstrates a
   specific, recurring need (see `decisions/0001`, Alternatives).
2. Independent verification means inspecting actual artifacts, tests and
   behaviour directly — never accepting the implementing agent's own
   summary as evidence (`AGENTS.md` §6).
3. Isolation between responsibilities is **best-effort** unless a named
   technical mechanism enforces it. Any report claiming "independent
   review" must state plainly whether that independence was mechanically
   enforced or merely a fresh context dispatched by the same operator —
   this bootstrap's own step 7 review is the latter, and is reported as
   such.
4. A Codex-based PR review CI gate (structured findings; P0/P1 blocks
   merge; fail-closed on incomplete review; advisory findings recorded and
   dispositioned, not silently dropped; required GitHub checks enforcing
   the gate) is accepted as a **mandatory Phase 1 capability**, scheduled
   as Stage 1.3. It is explicitly **not implemented** during this
   bootstrap. Supported Codex integration and authentication options are
   to be researched as part of Stage 1.3's own focused plan, not assumed
   now.
5. True mechanical isolation (the broker/capability pattern CodeCompass
   used for clean-room reconstruction) is **not built during bootstrap**.
   If Stage 1.5's independent documentation reconstruction later needs
   stronger-than-best-effort isolation, that is a decision for a Stage 1.5
   plan and, if it introduces new infrastructure, its own ADR — not an
   assumption carried from this one.

## Alternatives considered

- **Fix a named agent roster now** (as CodeCompass did). Rejected — see
  `decisions/0001`'s rationale: CodeCompass's own experience shows a
  roster fixed before real work gets broken by real work.
- **Claim strict isolation for the bootstrap's step 7 review**, since it
  runs in a separate agent dispatch. Rejected: dispatch alone does not meet
  the bar `decisions/0066`/`0076` set for *technically enforced* isolation
  (scoped capability, mechanical separation); claiming otherwise would
  violate the bootstrap prompt's own instruction not to assume independence
  merely because the prompts differ.
- **Build the Codex gate now**, since it is called "mandatory."
  Rejected: explicitly out of scope for bootstrap per the prompt; doing so
  would also mean committing to an integration approach before researching
  current supported options, which the prompt requires happen as part of
  Stage 1.3 specifically.

## Rationale

Function-based responsibilities give the separation-of-concerns benefit
(no actor verifies its own work) without pre-committing to organisational
detail that CodeCompass's own history shows doesn't hold. Naming the
isolation gap honestly — rather than letting "independent review" quietly
come to mean "a different prompt in the same session" — is itself a
direct application of Axiom Dev's "verification requires evidence, not
confidence" principle to the verification process itself.

## Consequences

- Every report of an "independent" assessment in this project must state
  its actual isolation level. A future reviewer (or this project's own
  later retrospective) can check that claim against this ADR.
- The Codex gate remains unimplemented risk until Stage 1.3; Phase 1 cannot
  close with the gate only planned — `planning/phase-01-foundation.md`
  records this as a hard Phase 1 exit dependency, not an optional nicety.
- If Stage 1.5 needs real mechanical isolation, that work has a direct
  CodeCompass precedent to evaluate (`decisions/0066`, `0076`) rather than
  starting from nothing — but adopting it is not pre-authorised here.

## Relevant evidence

- `~/projects/codecompass/CLAUDE.md` §5 (`release-phase-auditor`:
  read-only, non-repairing, voided by later commits).
- `~/projects/codecompass/decisions/0049-agent-led-development-model.md`
  (fixed roster, later contradicted by its own Phase 43c).
- `~/projects/codecompass/decisions/0066-clean-room-reconstruction-needs-mechanical-isolation-and-independent-implementation-comparison.md`.
- `~/projects/codecompass/decisions/0076-cleanroom-broker-gives-a-capability-not-a-credential.md`.
- `planning/prompts/001-phase-1-bootstrap.md` §5, §6, §9 Step 7.
- This bootstrap's own independent review record, in
  `planning/phase-01-foundation.md`, which names its isolation level
  explicitly per Decision point 3.

## Unresolved

- Codex integration/authentication approach — deferred to Stage 1.3's own
  plan, which must research current supported options before committing.
- Whether Axiom Dev will ever need a fixed agent roster or a
  mechanically-enforced isolation mechanism — left open, no timeline
  committed.

## Supersession

None. This is the third ADR.
