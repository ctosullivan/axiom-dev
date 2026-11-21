# AGENTS.md — Axiom Dev development methodology

This file is the **canonical** source of development rules for both human
contributors and coding agents working on Axiom Dev. Provider-specific files
(e.g. `CLAUDE.md`) contain only the adaptations a specific tool needs — they
must not restate or contradict the rules here. If you find a conflict,
this file wins; fix the provider file.

## 0. Bootstrap exception

This file, `CLAUDE.md`, `CONTRIBUTING.md`, the initial ADRs, and the Phase 1
plan were written during repository bootstrap (Phase 1, Stage 1.0), before
any of the process described below existed to govern their own creation.
That is an acknowledged, one-time exception. From this point forward,
changes to these governing files follow the rules in this document and in
`CONTRIBUTING.md` like any other change — including the planning and review
requirements below.

## 1. Development lifecycle

Every substantive change to Axiom Dev follows:

```
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE
```

- **UNDERSTAND** — read the current implementation, knowledge and
  documentation baseline before proposing anything. Do not assume a prior
  session's understanding is still accurate.
- **SPECIFY** — write a version-controlled plan (see §2) before writing
  implementation code.
- **ASSESS IMPACT** — identify what existing contracts, documentation,
  decisions and knowledge records the change touches, and what must change
  alongside it.
- **BUILD** — implement to the plan. A plan may be revised, but revisions
  are recorded, not silently absorbed.
- **VERIFY** — produce evidence (tests, independent review, direct
  inspection) that the change does what it claims. A confident summary from
  the implementing agent is not evidence.
- **RECONCILE** — update affected documentation and knowledge records in
  the same change, and close out the plan against the evidence actually
  produced.

## 2. Plan before implementation

No substantive implementation work starts without a version-controlled plan.
A roadmap entry existing is not authorisation to implement it — the entry
only becomes actionable once its own focused plan exists and has been
reviewed.

A plan must identify:

- Objective and expected value.
- Authorising prompt and relevant ADRs.
- Current implementation and knowledge baseline.
- Scope and explicit non-goals.
- Dependencies.
- Proposed files and architectural changes.
- Behavioural contracts and acceptance criteria.
- Independent verification method.
- Documentation and knowledge implications.
- Completion criteria and the evidence required before progressing.

Plans live under `planning/`. Trivial, purely mechanical changes (typo
fixes, formatting) do not need one; anything that changes behaviour,
interfaces, architecture, or established knowledge does.

## 3. Architecture Decision Records (ADRs)

Record a decision in `decisions/` only when it is genuinely non-obvious —
a real tradeoff was weighed, or a future reader would otherwise have to
re-derive the reasoning. Do not record routine implementation choices as
ADRs.

- ADRs are numbered sequentially (`0001-...`, `0002-...`, no reuse, no
  gaps-by-renumbering).
- Status is one of `Accepted`, `Superseded by NNNN`, or `Accepted
  (partial — see Unresolved)` when part of the decision is deliberately
  left open and recorded in an "Unresolved" section rather than settled —
  use the plain form unless something is genuinely still open.
- ADRs are **append-only** once accepted. A reversed or materially changed
  decision gets a **new**, superseding ADR; it does not edit the old one in
  place. The old ADR's status is updated to `Superseded by NNNN` and its
  content is otherwise left intact as a historical record.
- Each ADR contains: Title, Status, Context, Decision, Alternatives
  considered, Rationale, Consequences, Relevant evidence, and any
  supersession reference.
- Unresolved or speculative choices are recorded as unresolved — not written
  up as settled decisions because they appear in a plan or roadmap.

## 4. Roadmap and session continuity

- `planning/ROADMAP.md` tracks every phase/stage as one of: Proposed,
  Planned, In progress, Completed, Deferred, Blocked. A phase moves to
  Completed only after an independent closeout assessment (§6) finds its
  acceptance criteria met with evidence — writing the code or the docs is
  not sufficient on its own.
- `planning/CONTEXT.md` is kept current, not historical: current phase and
  status, latest completed work, relevant decisions, outstanding issues,
  current branch/PR, and the next concrete action. Historical narrative
  belongs in retros and commit/PR history, not here.

## 5. Documentation synchronisation

A change that affects intended behaviour, an architectural decision, an
implementation interface, or an established knowledge record must update
the affected documentation **in the same change** (commit/PR), not as
follow-up work. Documentation changes must not introduce new authoritative
requirements on their own — new requirements go through a plan and, if
non-obvious, an ADR.

## 6. Independent verification and phase closeout

Verification must come from inspecting actual artifacts, tests and
behaviour — not from accepting the implementing agent's own summary.

- Every substantive phase undergoes an independent completion assessment
  before the roadmap marks it Completed.
- "Independent" here means: performed from a fresh context with no prior
  investment in the work being judged correct, inspecting the artifacts
  directly. Where the assessment is dispatched by the same operator or
  session that did the work, that is a real limitation on independence —
  describe it honestly as **best-effort isolation**, not strict isolation,
  unless a technical mechanism actually prevents context leakage. Do not
  claim strict agent isolation without naming the enforcement mechanism.
- A phase closeout records what was checked, what evidence was found, and
  any findings — including findings that something claimed as done is not
  actually done.

## 7. Knowledge placement

Knowledge belongs in one authoritative place per category; duplication
across places is acceptable only when the copies stay consistent with that
one source:

| Knowledge | Lives in |
|---|---|
| Implementation behaviour | Source code |
| Interfaces | Docstrings |
| Non-obvious local rationale | Code comments |
| Architectural decisions | `decisions/` (ADRs) |
| Required behaviour | `contracts/` (from Stage 1.1 onward) |
| Verification outcomes | `evidence/` (from Stage 1.1 onward) |
| Human-facing explanation | `docs/` (from Stage 1.1 onward) |

Historical reasoning is not current architectural justification — if an
ADR's reasoning no longer applies, supersede it (§3); don't let old
rationale drift into being cited as live policy.

The full knowledge model (INTENDED / OBSERVED / VERIFIED / UNCERTAIN /
CONTESTED classification, schemas, contracts, evidence conventions) is
Stage 1.1 work — see `planning/phase-01-foundation.md`. This table is the
Stage 1.0 placement policy only.

## 8. Testing and verification requirements

Once Axiom Dev has source code (Stage 1.4 onward), every behavioural change
needs:

- A deterministic test demonstrating the intended behaviour.
- For contract-governed behaviour, a test demonstrating the contract still
  holds.
- Evidence attached to the plan's completion record, not just a claim that
  "tests pass."

Nothing in this repository yet requires this in practice — it is recorded
here now so the first substantive component (Stage 1.4) is built against a
known bar, not a bar invented after the fact.

## 9. Commit and pull request conventions

- Commit messages: short imperative summary line, `type(scope): subject`
  where helpful (e.g. `docs(phase-1): ...`), body explaining *why* when not
  obvious.
- Do not commit secrets, credentials, or personal information — including
  from preserved prompts (see `planning/prompts/`).
- Substantive changes land via a branch and pull request, not a direct push
  to `main`, so independent review (§6) has something concrete to review
  before merge.
- A PR description states: what changed, why, which plan/ADR authorises it,
  and what verification evidence is attached.
- Accepted behavioural contracts are not weakened by the implementing agent
  unilaterally — a contract change needs its own plan entry and, if it
  reverses an accepted decision, a superseding ADR.

## 10. Definition of Done

A change is done when:

1. It is covered by a plan (§2) or is genuinely trivial.
2. Affected documentation and knowledge records are updated in the same
   change (§5).
3. Required evidence (§6, §8) exists and is attached, not merely asserted.
4. Any new non-obvious decision has an ADR (§3).
5. `planning/ROADMAP.md` and `planning/CONTEXT.md` reflect the actual
   state — no phase is marked Completed without independent closeout.
6. Human approval has been obtained where §11 requires it.

## 11. Human approval boundaries

The following require explicit human approval before proceeding, regardless
of how confident the agent is:

- Changing `AGENTS.md`, `CLAUDE.md`, or `CONTRIBUTING.md` (governance
  itself).
- Marking a phase or stage Completed in `planning/ROADMAP.md`.
- Merging a pull request.
- Any destructive or hard-to-reverse git operation (force-push, history
  rewrite, branch deletion, `reset --hard` on shared work).
- Beginning a new Phase 1 stage beyond the one currently authorised.
- Changing the project's licence.

## 12. Changing this file

Changes to `AGENTS.md` are themselves governed by this process: propose via
a plan, get human review, and if the change reverses or materially alters a
prior methodology decision, record it as a new ADR superseding the old one
rather than quietly editing history.
