---
audience: contributors and agents making any non-trivial change
purpose: define where a given piece of project knowledge belongs, and what enforces that
required_sections: [Classification, Placement table, Enforcement classes, Reconciliation hook]
authoritative_sources: [AGENTS.md, decisions/0002]
acceptance_criteria:
  - every knowledge category in the placement table maps to exactly one authoritative artifact kind
  - every enforcement class states whether it blocks a change or is advisory
  - this document itself has been checked against docs/documentation-schema.md
---

# Knowledge placement policy

This is the full version of the placement table in `AGENTS.md` §7, which
remains the short, canonical summary — if the two ever disagree, fix
`AGENTS.md` first (it is the more-trusted file) and update this document
to match, don't let them drift apart.

## Classification

Every claim this project makes about its own behaviour is one of:

- **INTENDED** — authorised, documented behaviour (e.g. "the validator
  rejects a document missing a required section" as stated in a contract).
- **OBSERVED** — behaviour actually seen by direct inspection or execution,
  which may or may not match what was intended.
- **VERIFIED** — OBSERVED behaviour checked against an accepted contract,
  within a stated scope, by someone/something other than the implementer.
- **UNCERTAIN** — insufficient evidence either way. Honest default when no
  one has checked yet.
- **CONTESTED** — direct, unresolved conflict between two evidence
  sources (e.g. a passing test and a failing independent review).

These five are never collapsed into a single confidence number. A
document or evidence record states which one applies to a given claim,
explicitly, when the distinction matters (it usually matters for anything
under `contracts/` or `evidence/`).

## Placement table

| Knowledge category | Lives in | Who/what can write it |
|---|---|---|
| Implementation behaviour | Source code (`src/`, once it exists) | Implementer |
| Interfaces | Docstrings | Implementer, same change as the code |
| Non-obvious local rationale | Code comments | Implementer, same change as the code |
| Architectural decisions | `decisions/` (ADRs) | Whoever proposes the decision; accepted only with human approval (`AGENTS.md` §11) |
| Required behaviour (contracts) | `contracts/` | Written and independently reviewed *before* the implementation it governs (`decisions/0004`) |
| Verification outcomes | `evidence/` | Whoever ran the verification; must cite what was checked and how |
| Human-facing explanation | `docs/` | Anyone; synchronised in the same change as whatever it explains (`AGENTS.md` §5) |
| Current status / next action | `planning/CONTEXT.md` | Whoever last touched the project state; kept current, not historical |
| Historical narrative | `planning/retros/`, commit/PR history | Written once, after the fact; never edited to read as current |

Historical reasoning is not current architectural justification: if an
ADR's stated rationale stops applying, write a superseding ADR
(`AGENTS.md` §3) rather than letting people cite the old rationale as if
it still held.

## Enforcement classes

Adapted from CodeCompass's three-class split (`decisions/0094`), with the
same rule about which classes block:

- **Mechanical** (blocks) — checkable by a program with no judgement call:
  a link resolves, an ADR number is sequential, a required schema section
  is present. Once Stage 1.4's validator exists, these are its job.
  Until then, checked by hand (as in Stage 1.0's §5 deterministic checks).
- **Behavioural** (blocks) — checkable by running something and comparing
  to a contract: a test passes, a before/after refactor comparison matches.
  No judgement call about *whether* the behaviour is acceptable — the
  contract already settled that; only whether it's upheld.
- **Semantic / editorial** (does not block) — needs human or
  independent-agent judgement about quality, clarity, or whether a claim is
  well-supported given the evidence (CONTESTED items in particular). These
  surface as review findings, not automatic failures.

## Reconciliation hook

After any change that touches behaviour, an architectural decision, an
interface, or an established knowledge record, run this check (manually
until Stage 1.4's tooling exists):

1. List what changed (diff).
2. For each change, find every doc/decision/evidence record whose claims
   depend on the old state.
3. For each, confirm the claim still holds; if not, fix it in the same
   change (`AGENTS.md` §5) — not as follow-up.
4. Record anything found and fixed as a reconciliation note (see
   `docs/knowledge-reconciliation.md` for the full procedure and a worked
   example run against this repository's own Stage 1.0→1.1 transition).

This policy document was itself checked against
`docs/documentation-schema.md` by hand before being committed — see
`evidence/phase-1-log.md` for that check.
