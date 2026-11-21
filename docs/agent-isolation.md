---
audience: anyone dispatching or acting as an agent in a Phase 1 (or later) development cycle
purpose: define responsibilities by function, what each may read, and name the real isolation level honestly
required_sections: [Responsibilities by function, Isolation levels, What this session has actually used]
authoritative_sources: [AGENTS.md, decisions/0003]
acceptance_criteria:
  - no function is both the sole implementer and the sole verifier of the same change
  - every isolation claim names mechanical or best-effort explicitly, never leaves it implied
---

# Agent isolation and responsibilities

Per `decisions/0003`: responsibilities are described by **function**, not
by a fixed named roster. This document makes each function concrete
enough to dispatch against, and is explicit about isolation level because
`decisions/0003` §3 requires exactly that — no function here is described
as more independent than it actually is.

## Responsibilities by function

| Function | May read | Must not rely on | Typical dispatch |
|---|---|---|---|
| **Specification / research** | Existing docs, decisions, external authoritative sources (e.g. vendor docs for Stage 1.3's Codex research) | Assuming the current implementation matches an earlier session's description of it | Orchestrating session itself, or a fresh research-only dispatch for a bounded question |
| **Implementation** | The accepted plan/contract for the change | Permission to change the contract/fixtures it's being checked against without a separate reviewed change (`AGENTS.md` §9) | Orchestrating session, or a dispatched implementation agent working to a plan |
| **Independent verification** | The accepted contract/fixtures and the actual implementation artifact | The implementer's own test narrative or summary as its sole evidence (`AGENTS.md` §6) | A fresh-context dispatch with no prior investment in the work being judged — see Isolation levels below |
| **PR review** | The diff, the plan/contract it claims to satisfy, CI/test output | Trusting a natural-language review comment as the only gate (`planning/phase-01-foundation.md` §4, Stage 1.3) | Deterministic policy evaluator + (once live) Codex, both machine-checkable |
| **Documentation assessment** | The current docs and the change that just landed | Assuming docs are accurate because they were accurate once | The reconciliation procedure (`docs/knowledge-reconciliation.md`), run by whoever lands the change, checked independently at stage closeout |
| **Knowledge reconciliation** | Everything the change touches, per `docs/knowledge-placement.md`'s "dependents" step | Treating "no one complained" as evidence nothing drifted | Same as documentation assessment; escalates to a fresh-context pass for Stage 1.5 |
| **Human decision-making** | Everything; the final word on `AGENTS.md` §11's listed actions | Nothing — this function is never automated | The person operating the session |

No function above is ever collapsed into "the implementer also verifies
and also reconciles" for the same unit of work — that is circular
verification, the exact failure `decisions/0004` (Amendment B) exists to
prevent.

## Isolation levels

Three levels actually distinguishable in this environment, from weakest
to strongest:

1. **Prompt-based separation, same session.** A different instruction to
   the same context. **Not isolation at all** — explicitly named here so
   it's never mistaken for independent review.
2. **Fresh-context dispatch, same operator/session.** A new agent
   instance with no prior conversation history, dispatched by the same
   session/operator that produced the work. This is **best-effort
   isolation**: it removes the implementer's own framing and
   rationalisations (the agent genuinely hasn't seen them), but the same
   operator chose what to show the reviewer and could, in principle, have
   shaped that. Every independent review so far in this project
   (`planning/phase-01-foundation.md` §6, §11) is at this level.
3. **Mechanically enforced isolation.** A technical barrier — a separate
   credential, a capability broker instead of a shared one, a sandboxed
   context the dispatching session cannot see into — such that the
   reviewer's access is actually restricted, not just conventionally
   restricted. CodeCompass's clean-room broker
   (`~/projects/codecompass/decisions/0076`) is the cited precedent for
   what this would take. **Not built in Phase 1** unless a stage
   specifically justifies it (`decisions/0003` Consequences) — Stage 1.5's
   reconstruction uses level 2, named as such, not claimed as level 3.

Claiming level 3 without naming the actual mechanism is the specific
failure `decisions/0003` §3 was written to prevent, and this document
exists so no later stage has to re-derive that rule from scratch.

## What this session has actually used

For the record, not as a boast: every independent review dispatched in
Phase 1 so far (Stage 1.0's foundation review, the amendment/Stage-1.1
batch review) was level 2 — fresh-context, same operator. None has been
level 3. This is stated here because `docs/knowledge-placement.md`'s
reconciliation hook requires exactly this kind of claim to stay checkable
against what actually happened, not against what would look best.
