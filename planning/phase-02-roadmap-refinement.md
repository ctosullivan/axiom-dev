# Phase 2 roadmap refinement — evidence-first vertical slice

## Objective and authority

Record the repository owner's request on 2026-11-22 to align Axiom Dev's
roadmap with the previously discussed ideal: begin with a substantive,
bounded Ledgerkit/hledger development problem; introduce only the minimum
knowledge needed to solve and verify it; dogfood the full lifecycle; and
extract a reusable template *after* observing what works. The Phase 2
knowledge API remains mandatory, and there is no Phase 2 template A/B test.

This is a **planning/documentation amendment**, not Phase 2 implementation
authorisation. The existing accepted direction in
[ADR 0008](../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md)
continues to govern. Sequencing and proposed mechanisms are refined here,
without reversing that decision or rewriting Phase 1's accepted record.

## Current baseline

- [Roadmap](ROADMAP.md): Phase 1 Completed; Phase 2 Planned; Phases 3–4
  Proposed.
- [Phase 2 proposal](phase-02-template.md): previously organised largely
  by infrastructure deliverable (package, identity/API, wiki, gates, then
  dogfooding); this amendment makes a real vertical slice drive them.
- [Knowledge policy](../docs/knowledge-placement.md): intended/observed/
  verified/uncertain/contested distinctions; existing deterministic
  validator and CI from Phase 1.
- Axiom Dev's Phase 2 knowledge API, wiki integration and CI drift gate
  are **not implemented**. No Ledgerkit/hledger equivalence is presumed.

## Scope and impact

Update `planning/ROADMAP.md`, `planning/phase-02-template.md`,
`planning/CONTEXT.md`, `README.md` and `CHANGELOG.md` in the same PR.
Retain the six-stage Phase 2 plan, but make stages follow one real use case
from contract and independent oracle through minimally structured claims,
a small read-only API, deterministic drift checks, actual changes,
reconciliation, extraction and clean adoption.

Use ordinary Markdown/YAML, Git and CI as the authoritative substrate;
allow a minimal, ephemeral index. Treat explicit sources and independent
test evidence as support for bounded claims, not automatic truth. Require
persistent IDs for **governed knowledge artifacts and materially testable
claims**, not every sentence. Differentiate deterministic referential
integrity from semantic judgement. Document actual costs, false positives,
misses and pruning decisions; avoid unproven comparative claims.

Phase 3 should be hypothesis-led: measure whether knowledge access or
different agent strategies improve results using Assure when ready; MCP
remains an optional adapter, not the purpose of the project.

## Non-goals

No source code, scripts, APIs, wiki records, schema migration or CI
workflows are implemented by this amendment. No new platform, graph store,
embeddings, automated reconciliation, write API or MCP. No modification of
accepted ADRs. No Phase 2 A/B test. No claim that Phase 2 acceptance
criteria have been achieved or that future experiments proved superiority.

## Verification and completion

- Cross-check the roadmap, Phase 2 plan, context, README and the existing
  ADR 0008 for scope and status consistency.
- Confirm links resolve, Phase 1 remains Completed, Phase 2 remains
  Planned pending independent plan/contract approval, and Phase 3 remains
  Proposed.
- Check that the Phase 2 milestone uses an independently specified
  compatibility oracle, explicit scoped evidence, a subsequent source
  change and detectable impact, not an agent's self-authored assertion.
- Check the minimal API remains independent of MCP, Assure, any LLM and a
  persistent server; the gate does not mistake source impact for proof of
  semantic change.
- Ask an independent reviewer to inspect the PR against `AGENTS.md`
  §§2, 5, 6, 9–11. Review GitHub CI; never claim tests have passed if they
  have not been observed. Human approval is required to merge.

## Next action

Independent review and human-approved merge of this documentation-only
PR; only then agree a focused Stage 2.1 contract and inspect the current
Ledgerkit/hledger implementation before beginning Phase 2 coding.
