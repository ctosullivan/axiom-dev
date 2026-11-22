# Roadmap

Axiom Dev seeks the simplest useful, evidence-based development lifecycle
that preserves trustworthy knowledge across coding sessions and exposes
drift before unsupported claims become accepted facts. `AGENTS.md`
governs planning, verification and phase acceptance; detailed plans and
historical records live outside this summary.

## Phase overview

| Phase | Goal | Status | Plan / record |
|---|---|---|---|
| 1 | Foundation: lifecycle, validator, governance and verified dogfooding | **Completed** (owner decision, 2026-11-22; qualifications recorded) | [Archive](archive/phase-01/README.md) |
| 2 | Reusable knowledge-based template, comparative wiki, knowledge API and deterministic CI in Ledgerkit | **Planned** (direction approved; implementation plan pending review) | [Phase 2 plan](phase-02-template.md) |
| 3 | Optional MCP adapter and controlled agent-strategy A/B evaluation with a mature Assure harness | **Proposed** | Below |
| 4 | Wider adoption, hardening, evidence-backed release | **Proposed** | Below |

A roadmap entry alone is not authorisation to start implementing it:
follow `AGENTS.md` §2 and the acceptance process in
[phase archiving](../docs/phase-archiving.md).

## Phase 1 — Foundation (Completed)

The repository owner declared Phase 1 complete on 2026-11-22, following
the merge of [PR #1](https://github.com/ctosullivan/axiom-dev/pull/1).
The [archive](archive/phase-01/README.md) links the unchanged
implementation plan, closeout assessments, retrospective, decisions
and verification evidence. Completion is an **explicit owner acceptance
with disclosed residual conditions**, not a claim that the previously
requested fifth Codex review, outstanding review-thread resolutions or
required-merge enforcement were independently demonstrated. See the
[acceptance qualification](../evidence/phase-1-owner-acceptance.md).

## Phase 2 — Reusable template and Ledgerkit dogfooding (Planned)

**Objective:** produce a reusable, lightweight package that applies
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE in
an **independent** codebase, with Ledgerkit as the first consumer.
The [focused proposal](phase-02-template.md) requires review before
implementation.

**Required deliverables:** a comparative **Ledgerkit ↔ hledger
semantic wiki** with reproducible examples and versioned evidence;
stable identifiers for **all governed knowledge artifacts and claims**;
a local **knowledge API** for lookup, relations and impact/drift
queries; deterministic CI integrity gates; and end-to-end dogfooding
through initial change, subsequent drift, review and reconciliation.
A second clean adoption must establish that the template is not
Ledgerkit-specific.

**Drift control:** mechanically detect duplicate/reused IDs, invalid
schemas, dangling references, invalid provenance, uncovered relations,
stale source revisions and unreviewed impacted claims. Distinguish
*CI executed* from *CI required for merge*. Semantic equivalence,
truthfulness and the meaning of an upstream change are reviewable
claims—not automatically proven by a green check.

**Evidence:** reproducible adoption, validator and negative-case CI
runs, wiki examples, actual defects caught/missed, and measured
operational friction. **No Phase 2 A/B testing of the template**;
dogfooding demonstrates applicability and observations, not causal
superiority.

## Phase 3 — MCP and Assure-backed experiments (Proposed)

Add a thin **optional MCP interface over Phase 2's stable knowledge
API**, preserving the local API and identifiers. Define security,
read/write permissions, provenance, deterministic responses and
conformance tests. Once Axiom Assure has a demonstrably adequate
independent experiment harness, pre-register controlled **A/B tests
of knowledge retrieval and agent strategies** (e.g. with/without
structured knowledge access or different context-selection methods):
held-out tasks, common acceptance oracle, equivalent resources,
cost/latency and defect metrics, leakage controls and independent
adjudication. The experiments test stated strategies—not the Phase 2
template retroactively. The core template must work without MCP or
Assure.

**Exit evidence:** interoperable MCP adapter and replicated,
well-controlled findings with limitations and no unearned claims
of improvement. A focused Phase 3 plan is required before work starts.

## Phase 4 — Broader adoption and release (Proposed)

Try the mature template with additional independent repositories,
migration/refactoring scenarios and more developers; simplify
procedures that show little value, harden versioning and compatibility,
document failure cases and issue a supported release. Do not infer
generalisability from Ledgerkit dogfooding alone.

**Exit evidence:** independently reproducible onboarding, cross-project
test results, declared support boundary, versioned release, adoption
costs and documented limitations.

## Archived phases

- [Phase 1 — Foundation](archive/phase-01/README.md) — completed by
  owner decision on 2026-11-22 with documented qualifications.

See [archive index](archive/README.md) for the canonical archive list.
