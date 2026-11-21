---
id: 001
title: Phase 1 Bootstrap, Governance and Implementation Planning
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amendments: []
---

> **Provenance note.** The text below is the complete, verbatim original
> assignment prompt that authorised Axiom Dev's Phase 1 bootstrap. It is
> preserved unmodified as historical source material, per the methodology
> this prompt itself establishes (`planning/prompts/` — original planning
> prompts and amendments must be preserved with provenance, never
> reconstructed from memory or rewritten into a summary). Harness-level
> wrapper content from the originating session (system reminders, command
> metadata, environment banners) has been excluded as it is not part of the
> assignment itself; the assignment text is otherwise reproduced exactly as
> written, including its own internal numbering and formatting.
>
> Relationship to subsequent work: **Original prompt → Plan → Decisions →
> Implementation → Verification → Reconciliation**. This prompt is the root
> of that chain for Phase 1. See `planning/phase-01-foundation.md` for the
> plan it authorised, and `decisions/0001-development-governance.md`,
> `decisions/0002-knowledge-architecture.md`, and
> `decisions/0003-independent-verification.md` for the initial ADRs it
> produced.

---

# AXIOM DEV — PHASE 1 BOOTSTRAP, GOVERNANCE AND IMPLEMENTATION PLANNING

## 1. Your assignment

You are the lead development orchestrator for Axiom Dev, a new open-source project focused on knowledge-driven, AI-assisted software engineering.

Your assignment is to:

1. Inspect the existing Axiom Dev repository and relevant CodeCompass development practices.
2. Establish Axiom Dev's initial engineering governance and development methodology.
3. Create the minimum viable repository directory structure and foundational documentation.
4. Develop a detailed, dependency-aware Phase 1 implementation plan.
5. Preserve this original planning prompt in the repository.
6. Record initial architectural decisions using ADRs.
7. Independently review the planning and repository structure.
8. Commit and push the initial foundation to GitHub.

This assignment authorises planning, documentation and repository scaffolding only. Do not implement the substantive Axiom Dev software components yet.

Do not begin subsequent implementation stages until the initial foundation has been reviewed.

## 2. Project identity and strategic context

Project: Axiom
Primary product: Axiom Dev
Complementary product: Axiom Assure

Repositories:

* `github.com/ctosullivan/axiom-dev`
* `github.com/ctosullivan/axiom-assure`

Expected local development directory:
`~/projects/axiom-dev`

Verify the actual repository location rather than assuming this path exists.

### Axiom Dev mission

Develop the simplest practical methodology for AI-assisted software development that preserves important project knowledge, supports independent verification, maintains accurate documentation and enables complex software to evolve reliably across successive development sessions.

The central principles are:

Agents are transient. Project knowledge compounds.
Reason once, preserve what matters, and reuse verified understanding.
Verification requires evidence, not confidence.
Build the simplest system that demonstrably works.

### Fundamental hypothesis

A lightweight, knowledge-driven development methodology implemented predominantly using conventional engineering tools can improve the correctness, efficiency and maintainability of agentic software development without requiring a specialised AI development platform.

This hypothesis must be tested rather than assumed.

The objective is not to maximise automation, knowledge records or architectural sophistication.

The objective is to establish demonstrable improvement after accounting for the methodology's own overhead.

### Relationship with Axiom Assure

Axiom Assure is a separate experimental and independent assurance laboratory.

The projects should share knowledge principles, contracts, evidence conventions and relevant semantic standards.

They should not initially share runtime infrastructure or require one another to operate.

Axiom Dev is the immediate development priority.

## 3. Historical reference — CodeCompass

Axiom follows an earlier project:
`~/projects/codecompass`

Repository:
`github.com/ctosullivan/codecompass`

CodeCompass explored evidence-backed knowledge management, independent verification, agentic software development, documentation reconstruction, contracts, knowledge reconciliation and development orchestration.

Its development is discontinued in favour of a fundamentally simpler methodology.

Axiom is a new project, not CodeCompass v3.

Do not inherit CodeCompass's implementation, schemas, architectural decisions or infrastructure by default.

However, its established engineering practices and experimental findings should inform Axiom's methodology.

### Required CodeCompass inspection

Inspect the actual repository, including relevant examples of:

* `CLAUDE.md`
* `CONTRIBUTING.md`
* `CHANGELOG.md`
* Roadmaps and phase plans under `planning/`
* Original planning prompts and amendments
* Numbered architectural decision records under `decisions/`
* Session continuity records
* Phase retrospectives
* Knowledge placement policy
* Documentation schemas
* Documentation reconciliation workflows
* Agent isolation and clean-room documentation procedures
* Independent verification and phase closeout practices

Distinguish historical design intentions from implemented and verified capabilities.

Identify practices that should be retained, simplified or excluded.

Do not conduct an exhaustive CodeCompass archaeology exercise. Focus on the practices relevant to Axiom's initial methodology.

Record the relevant findings and source references in the Phase 1 planning documentation.

## 4. Governing development methodology

Axiom Dev will adopt the lifecycle:
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

This process must govern Axiom Dev's own development from the beginning.

### Mandatory development practices

**A. Plan before implementation**

Every substantive development phase must have a version-controlled implementation plan.

Plans must identify:

* Objective and expected value.
* Authorising prompt and relevant ADRs.
* Current implementation and knowledge baseline.
* Scope and explicit non-goals.
* Dependencies.
* Proposed files and architectural changes.
* Behavioural contracts and acceptance criteria.
* Independent verification methods.
* Documentation and knowledge implications.
* Completion criteria.
* Evidence required before progressing.

Do not start implementation merely because a roadmap item exists.

**B. Preserve original planning prompts**

Create:
`planning/prompts/`

Original user instructions and subsequent amendments must be preserved as historical source material.

Save this complete assignment prompt as the initial bootstrap prompt.

Where earlier original prompts are accessible, preserve them with provenance.

Do not reconstruct missing original prompts from memory and present them as verbatim originals.

Where useful, record the relationship:
Original prompt → Plan → Decisions → Implementation → Verification → Reconciliation

Do not commit secrets, credentials or sensitive personal information from prompts.

**C. Architecture Decision Records**

Create:
`decisions/`

Use sequentially numbered ADRs.

Each ADR should contain:

* Title.
* Status.
* Context.
* Decision.
* Alternatives considered.
* Rationale.
* Consequences.
* Relevant evidence.
* Supersession references where applicable.

Accepted ADRs should be historically preserved. A material reversal should normally create a new ADR superseding the earlier decision.

Avoid recording trivial implementation choices as ADRs.

**D. Roadmap management**

Create:
`planning/ROADMAP.md`

Maintain an accurate distinction between:

* Proposed.
* Planned.
* In progress.
* Completed.
* Deferred.
* Blocked.

A phase must not be marked complete merely because its code or documentation has been written.

Completion requires acceptance evidence.

**E. Session continuity**

Create:
`planning/CONTEXT.md`

Record:

* Current phase and status.
* Latest completed work.
* Relevant decisions.
* Outstanding issues.
* Current branch or PR where applicable.
* Next concrete development action.

Keep this concise and current rather than accumulating a second historical narrative.

**F. Contribution and agent instructions**

Create:

* `AGENTS.md`
* `CLAUDE.md`
* `CONTRIBUTING.md`

Establish clear rules for human contributors and coding agents.

Prefer one canonical source for shared agent instructions, with provider-specific files containing only necessary adaptations.

Avoid duplicating competing instructions across multiple files.

Include:

* Planning requirements.
* ADR discipline.
* Testing requirements.
* Independent verification.
* Documentation synchronisation.
* Knowledge reconciliation.
* Commit conventions.
* Pull request requirements.
* Definition of Done.
* Human approval boundaries.

**G. Retrospectives**

Create:
`planning/retros/`

Each completed development phase should record:

* Intended outcome.
* Actual outcome.
* Verification evidence.
* Unexpected findings.
* Process overhead.
* Lessons learned.
* Recommended methodology improvements.

Retrospectives should be proportionate to the scope of the work.

**H. Documentation synchronisation**

Changes affecting intended behaviour, architectural decisions, implementation interfaces or established knowledge must update affected documentation in the same PR.

Documentation changes must not silently introduce new authoritative requirements.

**I. Independent phase closeout**

Every substantive phase must undergo an independent completion assessment.

The assessment must examine actual artifacts, tests and evidence rather than accepting the implementing agent's summary.

The roadmap is updated to completed only after successful assessment.

## 5. Knowledge and documentation architecture

Adopt a lightweight version of the strongest CodeCompass knowledge-management concepts.

### Canonical knowledge

Use Git-versioned Markdown and YAML.

The initial knowledge model should accommodate:

* Concepts and domain knowledge.
* Behavioural contracts and invariants.
* Architectural decisions.
* Verification evidence.
* Unresolved questions and uncertainty.
* Relationships between relevant knowledge objects.

Do not recreate CodeCompass's comprehensive record hierarchy unless a demonstrated requirement justifies it.

Distinguish:

* INTENDED: Authorised project behaviour.
* OBSERVED: Behaviour supported by direct inspection or execution.
* VERIFIED: Behaviour established within a specified verification scope.
* UNCERTAIN: Insufficient evidence.
* CONTESTED: Conflicting evidence.

These classifications must not collapse into one confidence score.

### Lightweight documentation schema

Incorporate CodeCompass's schema-driven documentation findings.

Important documents should have a small declarative schema identifying:

* Document identity.
* Intended audience.
* Purpose.
* Required topics or sections.
* Relevant canonical knowledge.
* Acceptance criteria.

Use ordinary Markdown for documents and YAML where structured metadata is useful.

Initially, schemas may be manually validated.

Plan a lightweight Python validator as the first substantive Axiom Dev component.

Do not implement a custom documentation compiler during bootstrap.

### Knowledge placement policy

Define where knowledge belongs.

Use source code for implementation behaviour, docstrings for interfaces, comments for non-obvious local rationale, ADRs for architectural decisions, contracts for required behaviour, evidence records for verification, and documentation for human explanations.

Historical reasoning must not be presented as current architectural justification.

Legitimate duplication is acceptable when representations remain consistent.

Distinguish mechanically enforceable placement rules from subjective editorial judgments.

### Agent isolation

Plan independent responsibilities for:

* Specification and research.
* Implementation.
* Independent verification.
* PR review.
* Documentation reconstruction.
* Knowledge reconciliation.

Do not assume separate agents are genuinely independent merely because they have different prompts.

Where strict isolation is required, identify the permitted evidence, prohibited context and technical enforcement mechanism.

Where isolation is not technically enforced, describe it as best-effort.

Do not implement a custom sandbox or orchestration framework during bootstrap.

## 6. Independent verification and Codex PR gate

The Axiom Dev MVP must incorporate an enforceable Codex pull-request review CI gate.

Plan this as a mandatory Phase 1 capability.

The intended workflow is:

```
Approved specification
        ↓
Claude Code implementation
        ↓
GitHub pull request
        ↓
Deterministic tests
        +
Contract verification
        +
Codex independent PR review
        ↓
Required CI checks
        ↓
Knowledge reconciliation
        ↓
Human acceptance where required
        ↓
Merge
```

Requirements:

* Codex produces structured review findings.
* P0/P1 findings block merging.
* Failed or incomplete reviews fail closed.
* Advisory findings are recorded and dispositioned.
* Accepted contracts cannot be silently weakened by the implementing agent.
* GitHub required checks enforce the relevant gates.
* Tests demonstrate both permitted and blocked merges.

Distinguish review findings from independently demonstrated defects.

Research the current supported Codex integration and authentication options when producing the implementation-ready plan.

Do not implement the Codex integration in this bootstrap task.

## 7. Phase 1 roadmap to be developed

Prepare an implementation-ready plan for Phase 1, divided into the following stages.

### Stage 1.0 — Repository bootstrap and governance

Establish repository structure, project documentation, roadmap, ADR conventions, agent instructions, contribution guidelines, planning prompt preservation and development process.

This is the stage authorised for execution by the present assignment.

### Stage 1.1 — Knowledge and documentation methodology

Define and demonstrate:

* Canonical knowledge representation.
* Lightweight documentation schemas.
* Knowledge placement rules.
* Contract and evidence conventions.
* Knowledge reconciliation.
* Documentation maintenance.

### Stage 1.2 — Agent development methodology

Establish:

* Complete development lifecycle.
* Agent responsibilities.
* Planning and implementation boundaries.
* Agent isolation requirements.
* Independent verification.
* Phase acceptance and reconciliation.

### Stage 1.3 — Codex CI review gate

Implement and test the independent PR review process using conventional GitHub Actions and supported Codex tooling.

### Stage 1.4 — Axiom self-development and refactoring

Build a small genuine Axiom component, preferably the knowledge/documentation validator.

Develop it using the accepted methodology.

Then perform a meaningful behaviour-preserving refactor.

The refactoring exercise must demonstrate:

* Contracts established before modification.
* Baseline verification.
* Bounded implementation.
* Independent review.
* Before/after behavioural verification.
* Knowledge placement assessment.
* Documentation reconciliation.

A cosmetic refactor is insufficient.

### Stage 1.5 — Independent documentation reconstruction and closeout

Use an appropriately isolated agent to reconstruct Axiom's architecture and behaviour from approved evidence.

Compare the reconstruction against the project's existing documentation.

Investigate omissions, contradictions, misplaced knowledge and documentation drift.

Correct deficiencies through the established development workflow.

Record the outcomes, limitations and overhead.

Phase 1 cannot close until the complete methodology has been dogfooded successfully on Axiom Dev itself.

For every stage, specify dependencies, scope, non-goals, deliverables, tests and evidence-based exit criteria.

## 8. Initial repository scaffold

Inspect the existing repository first.

Establish approximately the following structure, adjusting where genuine requirements justify a simpler design:

```
axiom-dev/
│
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
│
├── planning/
│   ├── ROADMAP.md
│   ├── CONTEXT.md
│   ├── phase-01-foundation.md
│   ├── prompts/
│   │   └── 001-phase-1-bootstrap.md
│   └── retros/
│
├── decisions/
│   ├── 0001-development-governance.md
│   ├── 0002-knowledge-architecture.md
│   └── 0003-independent-verification.md
│
├── docs/
│   ├── methodology.md
│   ├── architecture.md
│   ├── knowledge-placement.md
│   ├── agent-isolation.md
│   └── schemas/
│
├── contracts/
├── evidence/
│
├── src/
├── tests/
│
└── .github/
    ├── workflows/
    └── pull_request_template.md
```

This is a proposed structure, not an obligation to create every directory immediately.

Only create directories and files needed for the authorised bootstrap.

Do not populate future implementation directories with speculative abstractions.

Do not create placeholder software merely to make the repository structure appear complete.

Preserve the existing licence unless a separately authorised decision changes it.

## 9. Bootstrap implementation instructions

Execute the following sequence.

### Step 1 — Inspect the environment

Verify:

* Actual working directory.
* Git repository status.
* Current branch.
* Configured remotes.
* Existing tracked files.
* Existing uncommitted changes.
* Available CodeCompass reference repository.
* Existing Axiom Dev documentation, if any.

Do not overwrite existing work.

If the repository has changed since this prompt was written, reconcile the plan with its actual state.

### Step 2 — Inspect CodeCompass precedents

Review the relevant engineering practices identified earlier.

Produce a concise internal comparison:
Retain / Simplify / Exclude

Record material decisions with references to the relevant CodeCompass files.

Do not copy its large governance documents verbatim.

### Step 3 — Establish governance

Create the foundational project files.

Ensure the contributor guidance and agent instructions communicate one consistent methodology.

Establish rules for changing governing instructions.

Record the bootstrap exception explicitly: the initial governance files necessarily precede the fully operational development workflow.

Subsequent development should follow the newly established process.

### Step 4 — Prepare the Phase 1 plan

Create:
`planning/phase-01-foundation.md`

This must be a substantive, implementation-ready roadmap for Stages 1.0–1.5, not merely a list of objectives.

Include the acceptance requirements for the complete dogfooding exercise.

Make clear that successful execution of Stage 1.0 does not constitute completion of Phase 1.

For subsequent stages, provide enough planning detail to establish dependencies and acceptance criteria, but require a focused implementation plan immediately before executing each stage.

### Step 5 — Establish architectural decisions

Create initial ADRs covering:

1. Development governance and repository methodology.
2. Canonical knowledge and documentation architecture.
3. Independent verification and agent responsibilities.

Record unresolved decisions honestly.

Do not mark speculative technical choices as established merely because they appear in the roadmap.

### Step 6 — Preserve planning instructions

Commit the complete current assignment prompt under `planning/prompts/`.

Include a short provenance header identifying it as the original bootstrap instruction.

Preserve its substantive content without rewriting it into a summary.

### Step 7 — Independent review

Dispatch an independent review of the proposed foundation.

The reviewer should evaluate:

* Internal consistency.
* Scope discipline.
* Architectural simplicity.
* Missing dependencies.
* Completeness of Phase 1 acceptance criteria.
* Whether CodeCompass lessons were correctly incorporated.
* Whether any documentation claims unimplemented capabilities already exist.
* Whether the proposed workflow can govern its own subsequent development.
* Whether the bootstrap leaves a clear next authorised action.

Resolve material findings before committing.

Review independence and any limitations should be recorded accurately.

### Step 8 — Validate the scaffold

Perform available deterministic checks, including:

* Git whitespace and diff checks.
* Broken internal references.
* File and directory consistency.
* Roadmap and plan alignment.
* ADR numbering.
* Consistency of agent instructions and contributor guidance.
* Presence and provenance of the original planning prompt.

Do not claim that future CI, validation software or Codex review gates have passed when they have not been implemented.

### Step 9 — Commit and push

Create a logical commit containing the initial project foundation.

Use a descriptive commit message, such as:
`docs(phase-1): establish Axiom Dev governance and implementation plan`

Push the changes to GitHub.

Prefer a dedicated bootstrap branch and pull request so the initial foundation can be reviewed before merging.

Do not force-push, rewrite history, bypass branch protection or overwrite unrelated changes.

This instruction explicitly authorises creating and pushing the bootstrap commit and opening the corresponding PR.

It does not authorise merging an unreviewed PR or beginning subsequent implementation stages.

## 10. Definition of Done

This bootstrap assignment is complete when:

1. Axiom Dev has a coherent repository foundation.
2. Development governance is documented and internally consistent.
3. Original planning instructions have been preserved.
4. Initial ADRs exist.
5. The roadmap and session continuity record are established.
6. The complete Phase 1 implementation plan exists.
7. CodeCompass's relevant engineering findings are incorporated.
8. Agent responsibilities and verification expectations are documented.
9. The mandatory self-development and refactoring demonstrations are defined as Phase 1 acceptance requirements.
10. An independent review has been completed and material findings resolved.
11. The initial foundation has been committed and pushed.
12. The repository clearly identifies Stage 1.1 as the next planned development activity, subject to review and authorisation.

Do not mark Phase 1 completed.

Do not mark Stage 1.0 completed before its own acceptance requirements have been independently checked.

Do not represent planned capabilities as implemented functionality.

## 11. Required final report

Once the assignment is complete, report:

Repository: Actual local path and GitHub destination.
Created artifacts: Files and directories established.
Architectural decisions: Initial ADRs and unresolved choices.
CodeCompass lessons: Important practices retained, simplified and excluded.
Implementation roadmap: Summary of Stages 1.0–1.5.
Verification: Checks performed and their results.
Independent review: Findings and dispositions.
Git status: Branch, commit SHA, push result and PR link if available.
Next action: The first concrete task required to begin Stage 1.1.

Keep the report concise but evidence-based.

## 12. Final operating constraints

* Use conventional development tools before building custom infrastructure.
* Preserve a single authoritative source for each category of project knowledge.
* Separate intended behaviour, observed implementation and verified outcomes.
* Maintain traceability between prompts, decisions, requirements, changes and verification.
* Protect accepted behavioural contracts from unilateral implementation changes.
* Treat agent independence as a technical property to be demonstrated, not assumed.
* Record failed experiments and negative results.
* Prefer simple procedures over elaborate automation.
* Do not replicate CodeCompass's architectural complexity.
* Do not introduce MCP, a graph database, a custom orchestrator or a documentation compiler during bootstrap.
* Do not begin substantive implementation beyond Stage 1.0.
* Do not claim work has been completed without inspecting the actual evidence.

The immediate objective is to establish a professional, self-governing engineering repository that can develop Axiom Dev using Axiom Dev's own methodology from its first substantive implementation task.

Proceed with repository inspection, planning, scaffolding, independent review, commit and push.
