# Phase 2 — reusable knowledge-based development template

**Status: Proposed implementation plan / owner-approved direction.**
Do not begin substantive implementation until the plan, contracts and
acceptance criteria have been independently reviewed under `AGENTS.md`
§2. Phase 2's objective and exclusion of template A/B testing have
been authorised; the implementation details have not.

## Objective and expected value

Create an independently usable, low-overhead **Axiom Dev template
package** that applies the complete knowledge-based development
lifecycle to a real third-party codebase. Use Ledgerkit as the
primary dogfood environment, with a Ledgerkit ↔ hledger comparative
semantic wiki as the demanding worked example. A fresh contributor
or agent should be able to find and use verified project knowledge
without depending on a prior agent session.

## Baseline and dependencies

- Phase 1's canonical lifecycle, governance, knowledge placement,
  documentation validator, contracts, evidence and deterministic CI.
- [ADR 0008](../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md).
- Ledgerkit and hledger are **external subjects**, not code vendored
  into Axiom Dev. Capture source commit/version and licence whenever
  asserting their behaviour.
- Phase 1 residual validator edge cases are known carry-over work;
  triage them in the first implementation increment.

## Scope and delivery sequence

### 2.1 — Define adoption contract and minimum package

Specify a clean install/use path for an independent repository:
project opt-in, lifecycle prompts and checklists, ownership of records,
upgrade and removal path, and a bounded first change. Keep the core
usable with conventional local tooling, without a model, MCP, Assure
or a hosted service. Define a realistic overhead budget and
developer workflow before designing extra infrastructure.

### 2.2 — Stable knowledge identity and minimal API

Define machine-readable, version-controlled **claims and knowledge
artifacts** (including wiki pages, semantic mappings, contracts,
decisions and evidence records) with:

- persistent, unique, typed identifiers independent of path and title;
  distinct immutable identity vs editable revision, lifecycle status
  and canonical location;
- type, scope, classification (INTENDED / OBSERVED / VERIFIED /
  UNCERTAIN / CONTESTED), source pointers, provenance, timestamps or
  source revisions, evidence references, relationships and ownership;
- explicit links such as `supports`, `contradicts`, `depends_on`,
  `maps_to`, `supersedes`, `verified_by`; no untracked silent ID
  renumbering, reuse or deletion;
- a **Phase 2 knowledge API**, preferably a small local library/CLI
  with machine-readable outputs, supporting lookup by ID, search/list,
  relation traversal, source-impact queries and stale/contested
  reports. Specify format and error semantics with contract tests.
  Protocol-neutral now; Phase 3 may expose it through MCP.

A claim must never be considered verified solely because it has an
ID, a source link, or a syntactically valid record.

### 2.3 — Comparative semantic wiki

Create a readable wiki for Ledgerkit versus hledger. Start with one
well-bounded accounting domain (for example posting/balancing and
query semantics), then extend only on demonstrated need.

For each comparison record: stable mapping/claim IDs; side-by-side
intent and observed behaviour; version/commit; examples or fixtures;
result classification **equivalent / partially equivalent / divergent /
unknown**; assumptions and boundary cases; evidence and gaps.
Distinguish statements about documented intent from independently
tested observed behaviour. Include a case where new source evidence
invalidates an earlier mapping.

### 2.4 — Deterministic CI integrity and drift gate

Contract-first, fail-closed checks, with positive and negative
fixtures, for: required fields; uniqueness and non-reuse of IDs;
resolvable references; provenance and source revisions; relationships;
mapping coverage for the declared scope; changed-source dependency
impact; unreviewed stale/contested records; invalid waivers; and
reproducible wiki examples/tests where practical.

Document **which failures block CI**, which only generate actionable
review reports, and which are beyond mechanical checking. CI execution
must be demonstrated on the consuming Ledgerkit integration and
required-merge enforcement verified separately before being claimed.
Provide a reviewed process to acknowledge/rebaseline an affected
claim; never automatically re-label a semantically changed claim
VERIFIED because checks are green.

### 2.5 — Dogfood the entire lifecycle

Apply UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY →
RECONCILE to at least one meaningful Ledgerkit change and one
subsequent change that makes previously captured knowledge stale.
Demonstrate the wiki/API being used *before* implementation,
independent verification, CI-driven drift discovery and
reconciliation *after* code changes.

Record concrete outcomes: reproducible steps, detected defects,
missed defects, false positives, time/maintenance overhead, useful
knowledge reuse, reviewer effort and adoption friction. Explicitly
distinguish benefits observed in dogfooding from causal claims that
would require a control group.

### 2.6 — Extract and independently adopt

Separate reusable template infrastructure from Ledgerkit-specific
knowledge. Have a fresh user/agent adopt the packaged template in a
second small repository or clean-room fixture and verify the core
commands and lifecycle without bespoke project assumptions.

## Non-goals

- **No A/B testing of the template in Phase 2.** Do not present
  dogfooding as controlled comparative evidence of superiority.
- No MCP transport, agent orchestrator, specialised vector store,
  LLM-dependent CI, or Axiom Assure runtime requirement.
- No claim of semantic correctness purely from valid schemas or
  graph links; no attempt to encode all hledger behaviour at once.
- No retroactive conversion of every historical Phase 1 document
  into the new stable-ID scheme unless separately justified.

## Proposed files and interfaces

Implementers should propose minimal package layout and contracts
for the API, identity model, wiki format, CI gate and consumer
integration *after inspecting the current Ledgerkit/hledger baselines*.
Axiom Dev's `AGENTS.md` stays canonical for this repository;
template-consuming repositories opt in explicitly. This plan does
not prescribe Python module names, persistence backends, or an MCP
schema before requirements have been verified.

## Acceptance criteria and evidence

Phase 2 closes only when independent reviewers can reproduce:

1. Successful clean adoption in Ledgerkit and in a separate fresh
   consumer, with no Axiom-hosted runtime dependency.
2. A documented end-to-end change and a second change demonstrating
   knowledge impact, verification and reconciliation.
3. Wiki comparison entries tied to real Ledgerkit/hledger versioned
   evidence; explicit divergences/unknowns rather than false
   equivalence claims.
4. Stable identity across rename/move and controlled revision, with
   negative tests for duplicates, missing references and ID reuse.
5. A useful local knowledge API (lookup, relationships, impact/drift)
   exercised in both workflows; no MCP dependency.
6. Deterministic CI failures on seeded mechanical faults and
   actionable drift reports on changed sources, with independently
   reviewed semantics and honest enforcement-level reporting.
7. Evidence of usability, maintenance cost, limitations and useful
   real-world outcomes, **without requiring or claiming an A/B test**.
8. A fresh-context independent closeout, reconciled documentation
   and human completion approval.

## Independent verification and next step

Before implementation, have a reviewer challenge this plan for
unnecessary scope, circular acceptance criteria, identity migration,
CI bypasses and the difference between source drift and semantic
drift. Then accept bounded contracts and a first implementation
increment. Do not start Phase 3's experiments until the Assure
harness's readiness has been demonstrated and independently reviewed.
