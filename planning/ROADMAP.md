# Roadmap

Axiom Dev tests whether a **small, conventional, knowledge-based development
method** makes AI-assisted maintenance of complex software more trustworthy
and practically useful. The method must preserve verified understanding
across disconnected sessions, support independent verification, expose
potential knowledge drift, and justify its own overhead. A wiki, API,
template, MCP adapter or experiment is a *means*, not the product outcome.

`AGENTS.md` governs plans, verification, evidence, human approval and phase
closure. Detailed plans and historical records remain at their canonical
paths; do not duplicate them here.

## Phase overview

| Phase | Outcome | Status | Detail |
|---|---|---|---|
| 1 — Foundation | Evidence-based development lifecycle, validator and governance | **Completed** (owner decision 2026-11-22, with recorded qualifications) | [Archive](archive/phase-01/README.md) |
| 2 — Practical value and reusable template | Demonstrate a complete, evidence-backed Ledgerkit vertical slice; extract a minimal portable package | **Planned** (direction approved; focused contracts require review) | [Phase 2 plan](phase-02-template.md) |
| 3 — Measured effectiveness and MCP | Deliver a thin, consumer-optional MCP adapter over Phase 2's API and test agent/retrieval strategies with an independent Assure harness | **Proposed** | Below |
| 4 — Product maturity | Independent adoption, simplification, hardening and evidence-backed release | **Proposed** | Below |

**Planning status is not implementation authorisation.** Each substantive
stage requires an independently reviewed focused plan and contracts before
building (`AGENTS.md` §2). Phase 2 deliberately does **not** A/B test the
template.

## Phase 1 — Foundation (Completed)

The owner declared Phase 1 complete on 2026-11-22, following
[PR #1](https://github.com/ctosullivan/axiom-dev/pull/1).
The [archive](archive/phase-01/README.md) links the original plan,
closeout, evidence, decisions and retrospective; the
[acceptance qualification](../evidence/phase-1-owner-acceptance.md)
explicitly discloses the historical outstanding conditions. Phase 1
completion is not evidence that those conditions were subsequently
retested or resolved.

## Phase 2 — Practical value, then template extraction (Planned)

**Objective:** show the full UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD
→ VERIFY → RECONCILE lifecycle works on real Ledgerkit development,
including a subsequent change that threatens previously recorded
knowledge. Develop only the knowledge substrate needed for that
example; then extract a reusable template and test clean adoption
independently.

**Order of work:** the intended product is a reusable package, but
**dogfooding drives design**. Do not finish a generic platform before
learning from the real consumer.

| Stage | Evidence-producing milestone | Exit demonstration |
|---|---|---|
| **2.1** Select a Ledgerkit case | **Planned in full detail, contract-only** — `planning/phase-02-stage-2.1-plan.md` selects Ledgerkit's own EC-022, with an independently re-derived root cause, a 9-row fixture matrix fully captured against the exact-commit hledger oracle (including a newly-found cross-transaction scope boundary), and an explicit handoff carrying all fix/verification work to Stage 2.4. Reviewed twice (`planning/phase-02-planning-review.md`) | Reproducible fixture, scope, failure cases, reviewer and explicit value/overhead questions — plan reviewed; BUILD not yet authorised; EC-022 itself is **not** fixed by this stage |
| **2.2** Minimal comparative knowledge | Create a readable Ledgerkit ↔ hledger wiki slice, stable IDs for governed artifacts/material claims, referenced sources/evidence and a small **local knowledge API** | A fresh session can deterministically retrieve a scoped claim with provenance and limitations |
| **2.3** Deterministic integrity and drift | Add contract-tested CI for IDs, references, source revisions, evidence integrity and change-to-claim impact | Seeded mechanical faults fail; source changes flag relevant claims; no automatic semantic verdict |
| **2.4** Full lifecycle dogfooding | Make a meaningful Ledgerkit change, independently verify it, then change a source on which recorded knowledge depends | Axiom flags potentially stale knowledge and supports evidenced reconciliation that another agent can reuse |
| **2.5** Extract a minimal template | Remove Ledgerkit-specific assumptions, unneeded features and maintenance overhead | The resulting package is conventional, documented, opt-in and independent of a hosted service |
| **2.6** Independent adoption/value review | Reproduce clean adoption in a second repository and independently review outcomes and costs | Review supported value, failure cases, useful reuse, false positives and what to remove or defer |

**Knowledge API boundary:** Phase 2 requires a usable API, preferably a
small read-only Python library/CLI with `get(id)`, `find(query)`,
`related(id)` and `impacted(changes)`. Use Markdown/YAML and Git as
the canonical store, optionally building an ephemeral index. CI
validation is a separate tool/command. Avoid a graph database,
persistent knowledge service, embeddings, agent-written knowledge
reconciliation, a write API or MCP until a *demonstrated* use case
justifies an increment.

**Evidence model:** use first-class stable IDs for governed documents
and *material, independently testable* claims, not every explanatory
sentence. A claim records exact scope/assumptions, source version,
supporting test or review evidence and a meaningful status (INTENDED,
OBSERVED, VERIFIED, UNCERTAIN or CONTESTED). Verification means an
independent check against an accepted contract/oracle for that scope;
a source link, record ID or green schema check alone never proves
semantic truth. Change detection establishes **possible impact**,
not actual invalidity.

**CI:** fail closed for defined mechanical integrity violations;
produce actionable reports for affected claims and require explicit,
reviewed disposition under documented policy. Explain the difference
between a CI job that executes and a check configured as a **required
merge condition**. Never silently reclassify potentially stale claims
as VERIFIED.

**Value evidence:** track supported knowledge reuse, real defects
caught/missed, false positives, reviewer effort, maintenance/setup
time, friction, and independent onboarding. Choose assessment
questions and acceptable overhead *before* observing outcomes.
No Phase 2 A/B test: dogfooding can demonstrate feasibility and
specific instances of usefulness, but **not causal superiority**.
Remove or defer features with no demonstrated net value.

**End-to-end acceptance scenario:** an independently specified
Ledgerkit/hledger semantic claim is retrievable by stable ID with
versioned evidence; a relevant Ledgerkit source changes; CI identifies
affected records; a separate reviewer reproduces the appropriate
behavioural test and dispositions any semantic difference; the wiki
and claim evidence are reconciled without losing provenance; a fresh
agent uses the revised knowledge for a subsequent task. This
demonstrates the *whole lifecycle*, not just independent API features.

See [the Phase 2 plan](phase-02-template.md) for stage contracts,
negative cases, non-goals and independent closeout criteria, and that
plan's own links to the now-concrete Stage 2.1 task plan, adoption
design, knowledge-API design, measurement design, architecture diagram
and independent review. This remains a **planned** phase, not an
implemented package — none of Stage 2.1's BUILD work has started.

## Phase 3 — Experiment-led assurance and MCP adapter (Proposed)

**Question first:** does persistent, scoped, independently verifiable
knowledge improve actual agent development outcomes, and when is
structured retrieval worth its cost? Using Axiom Assure once its
independence and experimental correctness are established, pre-register
controlled A/B evaluations of *agent and retrieval strategies* such as:

- Plain repository search vs verified structured knowledge.
- Complete context vs selective retrieval, with correctness and token costs.
- Fresh-agent reconstruction vs reuse of previously accepted knowledge.
- Conventional Markdown access vs the knowledge API, where comparable.
- Self-review vs genuinely independent verification.

Use held-out tasks, independently established behavioural oracles,
controlled resources and leakage, defect/rework/cost measures,
replications and honest negative findings. A/B here is **not a delayed
A/B test of the Phase 2 template**.

**Phase 3 also delivers a small MCP adapter over the stable Phase 2
knowledge API**, with interoperable read-only operations, conformance
tests, explicit permissions and provenance. The adapter is **required
as a Phase 3 deliverable** under accepted ADR 0008, Decision 7, but
**optional for consumers**: Phase 2's API and template must remain
fully functional without MCP or Assure. Keep the adapter thin; do not
turn it into a new knowledge platform or claim it improves results
without experimental evidence.

**Exit evidence:** a working, independently checked interoperable MCP
adapter **and** an independently reviewed experimental harness with
reproducible, appropriately qualified strategy findings. A focused
Phase 3 plan is required.

## Phase 4 — Product maturity (Proposed)

Test adoption and maintenance in additional independent repositories,
including substantial refactoring and changed legacy behaviour.
Simplify or remove low-value rules, support compatibility/versioning,
document boundaries and issue a versioned package release.

**Exit evidence:** reproducible independent onboarding, across-project
results, operational and maintenance costs, known limitations and a
supported release. Do not generalise from Ledgerkit alone.

## Archived phases

- [Phase 1 — Foundation](archive/phase-01/README.md) — completed by owner
  decision on 2026-11-22 with disclosed qualifications.

See [the archive index](archive/README.md). The sequencing rationale is
recorded in [this refinement plan](phase-02-roadmap-refinement.md) and
[ADR 0008](../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md).
