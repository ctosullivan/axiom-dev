# Phase 2 — Evidence-first Ledgerkit development and reusable template

**Status: Proposed implementation plan; Phase 2 is Planned.**
The owner has approved the template-first direction and explicitly excluded
template A/B testing. **This document proposes sequencing and acceptance
criteria; it is not permission to implement** until each focused increment,
its independent acceptance oracle and contracts have been reviewed under
`AGENTS.md` §2.

## Objective and expected value

Demonstrate that a *small, conventional, evidence-based knowledge system*
helps agents develop and maintain a substantive Ledgerkit feature across
disconnected sessions. Prove that source changes identify possibly stale
knowledge and that an independently verifiable claim can be reconciled and
reused. **Only after using the method on real work, extract a reusable,
low-overhead Axiom Dev template for independent projects.**

Project outcomes (not merely deliverables):

1. Important scoped understanding survives agent-session boundaries.
2. Required behaviour is verified against evidence independent of
   the implementation under test.
3. Changed source surfaces impacted claims without pretending to know
   their semantic truth.
4. Useful knowledge reuse and verification justify their creation,
   review and maintenance effort.
5. Another repository can adopt the method without Ledgerkit-specific
   logic, a hosted runtime, MCP or Assure.

The Phase 2 knowledge API, comparative wiki, stable IDs, deterministic
CI gate, dogfooding and reusable template **all remain required**.
The change from the earlier plan is sequencing: **a real use case drives
the minimum infrastructure**, rather than a finished platform
preceding dogfooding.

## Baseline and authority

- Existing lifecycle, documentation validator, governance, evidence
  conventions and CI from Phase 1.
- [ADR 0008](../decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md)
  establishes template-first Phase 2, stable identity, local knowledge
  API, deterministic integrity and drift, and deferred MCP/A/B work.
- [Roadmap refinement](phase-02-roadmap-refinement.md) records this
  owner-requested evidence-first sequencing.
- Ledgerkit/hledger are external projects; inspect their current
  code, versions, licences and actual behaviour *before* fixing a
  particular compatibility scenario. Neither is vendored into Axiom.
- Disclosed Phase 1 validator issues (absolute document links and
  empty-string link/source values) require explicit triage; do not
  describe those known checks as more complete than they are.

## Scope and delivery sequence

### 2.1 — Choose a meaningful Ledgerkit problem and oracle

Inspect a bounded area of Ledgerkit and hledger, e.g. posting/balancing,
query or register semantics, and choose a **real development change**
where misunderstanding behaviour could cause a defect.

Before any implementation or knowledge-tool expansion:

- Record the relevant code/docs at pinned versions or commits,
  assumptions, scope and intended behavioural equivalence.
- Write and independently review the contract, input fixture,
  expected output and negative/boundary examples.
- Establish an **independent oracle**: for example, reproduce the
  pinned hledger reference output with fixed inputs, then independently
  judge whether matching it is the right requirement. Do not derive
  the expected result from Ledgerkit's newly written code or the
  implementing agent's judgement.
- Define questions that will demonstrate or falsify practical value,
  including expected setup, maintenance and review costs. Do not
  select or revise success criteria after seeing results.
- Use the existing methodology to implement the smallest possible
  first record; add generic machinery only when this case exposes
  a concrete requirement.

**Exit evidence:** an accepted, bounded problem statement, fixture,
independent oracle, negative case and value/overhead measures.

### 2.2 — Build only the comparative knowledge the problem requires

Create a readable **Ledgerkit ↔ hledger semantic wiki slice**, first
with perhaps 10–20 materially useful, independently testable claims
as an *illustrative scope*, not a quota. Distinguish mapping results
(equivalent / partially equivalent / divergent / unknown) from claim
evidence status (INTENDED / OBSERVED / VERIFIED / UNCERTAIN / CONTESTED).
Every semantic statement states scope, versions, assumptions,
counterexamples and unresolved boundaries.

Model only three essential concerns:

1. **Claim:** a precise assertion, with scope and status.
2. **Source:** a code/document reference pinned to the evidence
   baseline (repository, path and version/commit where applicable).
3. **Evidence:** a fixture/test result or independently reviewed
   assessment that supports or contradicts the assertion.

Give **every governed knowledge artifact and materially testable
claim a stable unique ID**, independent of its path/title. Keep identity
separate from revision and status. A rename does not change an ID;
references to other IDs are explicit. Do **not** give ordinary
explanatory sentences individual claim records. Link wiki Markdown
to canonical machine-readable records, rather than maintaining two
copies of the same assertion.

The knowledge API is part of **Phase 2**: initially a small,
read-only local library/CLI with deterministic, machine-readable
operations:

- `get(id)` — claim/artifact, evidence, scope and status;
- `find(query)` — exact-ID and text/metadata discovery;
- `related(id)` — explicitly declared references;
- `impacted(changes)` — records possibly affected by changed sources.

Use Markdown/YAML and Git as the source of truth. A temporary in-memory
index is permissible; a persistent graph database or server is not
assumed. Git/PR review remains the write path. Define missing/duplicate
ID, invalid source, unsupported status and stale-evidence semantics in
reviewed contracts. Existing Axiom documentation conventions remain
in force; do not create a competing document-management scheme.

**Exit evidence:** a fresh-context consumer queries a scoped wiki
claim by ID, locates its independent evidence and sees its unknowns.
An ID, path or passing schema alone never turns a claim VERIFIED.

### 2.3 — Add deterministic integrity and source-impact gating

Build contract-tested, negative-fixture-backed validation for:

- schema completeness and field validity;
- ID uniqueness, stable references and prohibited silent ID reuse;
- resolvable source/evidence references and captured source revisions;
- consistent explicit relationships and any declared coverage boundary;
- relevant changed-source-to-claim impact;
- missing required review/acknowledgement on affected, stale or
  contested claims, with narrow, recorded waiver handling.

Treat **mechanical integrity** (which can fail closed) separately
from **semantic correctness** (which needs independent assessment).
A file change signals *potential impact*, not evidence of a changed
meaning. Do not auto-mark impacted records false or re-mark them
VERIFIED because tests, validation or an LLM succeeded.

Document which CI checks only **execute and report**, which fail a
pipeline, and which are independently confirmed as **required merge
checks**. These are distinct enforcement levels. Demonstrate CI
on the *consuming Ledgerkit integration*, not only fixtures in Axiom
Dev. Avoid brittle gates that force meaningless edits for unrelated
code changes; record misses and false positives.

**Exit evidence:** intentionally invalid records are rejected;
changed supporting source flags the right records with actionable
review work; unaffected records are not gratuitously invalidated.

### 2.4 — Dogfood a complete lifecycle including real drift

Use the wiki and read-only API *before* writing code to understand a
Ledgerkit behaviour. Execute UNDERSTAND → SPECIFY → ASSESS IMPACT →
BUILD → VERIFY → RECONCILE against an accepted contract and oracle.

Then make a second meaningful change whose inputs or source
dependencies threaten a prior claim. Demonstrate:

1. a stable ID and old evidence can still be retrieved;
2. the change-impact check identifies the relevant claim;
3. deterministic failures and semantic review are distinguished;
4. a reviewer who did not define the implementation independently
   tests the new behaviour against the accepted oracle or authorised
   revision;
5. changed claims and evidence are reconciled without erasing
   original provenance; a fresh agent can subsequently reuse them.

Measure real defects caught/missed, false positives, retrieval usefulness,
review and maintenance effort, friction, and any unnecessary procedure.
Dogfooding **does not** establish that Axiom causes superiority over
simpler approaches.

**Exit evidence:** an independently reproduced end-to-end change,
drift report, disposition and subsequent fresh-agent knowledge reuse.

### 2.5 — Extract and simplify the reusable template

Only now remove Ledgerkit-specific assumptions and package the
minimum adopted conventions, record schemas, CLI/API, gate and
lifecycle guidance for an independent repository. Prefer ordinary
files/Git/CI. Review each additional mechanism against a real failure
it prevents and the cost it adds. Remove or defer mechanisms without
demonstrated value.

**Exit evidence:** an installable/opt-in, documented, reversible
package that still supports the full lifecycle, stable evidence and
drift detection without Ledgerkit, an MCP server, LLM or Assure.

### 2.6 — Independently adopt and assess value

Have a fresh-context agent or developer use the package in a second
small repository (or suitably representative clean-room consumer),
with no private project-specific integration. Independently inspect
actual changes, fixtures, test outcomes, documentation reconciliation
and knowledge retrieval.

Evaluate:

| Criterion | Observation to preserve |
|---|---|
| Knowledge continuity | Could a fresh agent reuse previously verified, scoped knowledge? |
| Independent correctness | Which real defects or bad assumptions were exposed, missed or left unknown? |
| Drift detection | Did changes flag relevant claims; how many false positives/negatives? |
| Maintenance cost | Time and complexity to write, verify, update and prune knowledge |
| Setup/adoption cost | Work required by an independent consumer without special infrastructure |
| Net value | Which mechanisms earn their cost and which should be removed/deferred? |

Predeclare evaluation questions and record negative results as well
as positive ones. **No A/B testing of the template in Phase 2**, and
no causal attribution beyond what observational evidence can support.

**Exit evidence:** a reproducible second adoption, frank overhead/
failure review, simplification decisions and independent closeout.

## Architectural boundaries and complexity budget

- **Canonical storage:** human-readable Markdown/YAML and Git, not
  a second mutable database. Maintain one authoritative assertion
  location and reference it from wiki prose.
- **Identity:** stable IDs for governed artifacts and useful testable
  claims, not an ontology for every sentence. Use the simplest ID
  format that guarantees uniqueness and stable references.
- **API:** start read-only, local and deterministic; Git/PR changes
  are the write interface. Four operations only until real use
  demonstrates a fifth is needed.
- **Retrieval:** exact IDs, explicit links, text/metadata search.
  No embeddings or autonomously inferred relationship graph by default.
- **Reconciliation:** CI identifies mechanical defects and affected
  claims; a human/independent verifier evaluates semantic truth and
  authorises a revision. No agent silently overwrites evidence.
- **Increment rule:** before adding infrastructure, record the
  observed Ledgerkit failure it addresses, a smaller alternative,
  expected maintenance cost and a test proving usefulness.
- **No new runtime dependency** on MCP, Axiom Assure, an LLM, a hosted
  service, specialised orchestration or a persistent knowledge server.

## Non-goals

- No Phase 2 template A/B test or claims of comparative superiority.
- No encyclopaedic reverse engineering of Ledgerkit/hledger; initial
  comparison is limited to the selected bounded behaviour.
- No retroactive conversion of every Phase 1 narrative sentence to
  a claim ID.
- No inference that changed code means semantics definitely changed,
  or that a green mechanical gate proves a financial assertion true.
- No Phase 2 MCP implementation or Assure experimental harness.
- No speculative platform architecture ahead of a real use case.

## Proposed files, contracts and first increment

Inspect the actual Ledgerkit and hledger source before selecting file
names, exact record shape, persistent ID syntax or CLI signatures.
The first reviewed implementation plan must specify an independent
oracle, fixture, false-positive/negative tests, knowledge scope,
proposed files, constraints, reference source versions and cost budget.
Subsequent stage plans may refine the proposal but cannot silently
weaken acceptance criteria after outcomes are known.

`AGENTS.md` remains canonical for Axiom Dev. Template-consuming
repositories opt in explicitly; do not assume their governance is
identical to Axiom Dev's.

## Acceptance criteria and evidence

Phase 2 closes only when independently reproducible evidence confirms:

1. The selected Ledgerkit scenario was specified with an
   independently reviewed contract and an oracle not circularly
   derived from its implementation.
2. The scoped wiki distinguishes documented intent, observed
   behaviour, verified mapping, partial equivalence and unknowns.
3. Material claims and governed artifacts retain unique stable IDs
   through rename/revision, with negative tests for duplicates,
   non-reuse and dangling evidence/reference cases.
4. The **Phase 2** local knowledge API retrieves a scoped claim and
   evidence, searches, follows declared links and reports impact
   without MCP or Assure.
5. Deterministic CI rejects seeded mechanical defects and identifies
   affected evidence after relevant source changes, without
   presenting semantic uncertainty as a machine-proven verdict.
6. Real Ledgerkit implementation, independent verification, later
   drift, reconciliation and subsequent fresh-agent reuse are
   demonstrated across the complete lifecycle.
7. A second independent repository can adopt the extracted template
   without specialised infrastructure or Ledgerkit assumptions.
8. Evidence reports real useful outcomes, misses, false positives,
   setup/maintenance costs, simplification decisions and limitations,
   **without a Phase 2 A/B test or causal superiority claims**.
9. A fresh-context independent closeout assesses all criteria, and
   the human owner confirms completion under `AGENTS.md` §11.

## Independent verification and next action

Request independent review of this plan *before* implementation,
especially for excessive schema/API scope, circular oracles, claimed
drift certainty, enforcement gaps and over-ambitious acceptance.
If accepted, begin **Stage 2.1** by inspecting Ledgerkit/hledger and
writing one focused behavioural contract and test case.

Phase 3's Assure-backed agent/retrieval experiments are separate and
remain conditional on a demonstrably adequate independent harness.
