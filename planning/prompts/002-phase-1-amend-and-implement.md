---
id: 002
title: Amend and Implement Phase 1
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001]
---

> **Provenance note.** The text below is the complete, verbatim prompt that
> authorised amending and implementing Phase 1, superseding the
> bootstrap-only restriction in `001-phase-1-bootstrap.md`. Preserved
> unmodified as historical source material, per `AGENTS.md` §2/§3 and the
> original prompt's own instruction that prompts and amendments be kept
> with provenance, never reconstructed from memory. Harness-level wrapper
> content (system reminders, command metadata) is excluded as it is not
> part of the assignment; the assignment text is otherwise reproduced
> exactly as written.
>
> Relationship to prior work: this is **amendment 002** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md`. It does not
> replace `001`; both are preserved. See
> `decisions/0004-phase-1-amendment-verification-measurement-and-acceptance.md`
> for the ADR this prompt's Amendments A–D produced, and
> `planning/phase-01-foundation.md` for the amended plan.

---

# AXIOM DEV — AMEND AND IMPLEMENT PHASE 1

## 1. Assignment

You are the lead Claude development orchestrator for Axiom Dev, a lightweight methodology for knowledge-driven, AI-assisted software engineering.

Your assignment is to:

1. Inspect the existing Axiom Dev repository and its Phase 1 implementation plan.
2. Review the relevant development practices and findings from CodeCompass.
3. Amend the Phase 1 plan to address the requirements below.
4. Independently review and correct the amended plan.
5. Implement Phase 1 incrementally, using the Axiom methodology itself.
6. Establish an enforceable Codex pull-request review gate.
7. Develop and meaningfully refactor an Axiom component.
8. Independently verify the implementation and documentation.
9. Reconcile knowledge, capture lessons and assess Phase 1 completion.
10. Commit and push completed work to GitHub.

This instruction supersedes the previous bootstrap-only restriction. You are authorised to implement all Phase 1 substages, subject to their acceptance gates and the constraints below.

Do not skip verification, manufacture evidence or declare a phase successful simply because its planned files exist.

## 2. Repository context

Primary repository:

~/projects/axiom-dev

GitHub:

https://github.com/ctosullivan/axiom-dev

Reference repository:

~/projects/codecompass

GitHub:

https://github.com/ctosullivan/codecompass

Related projects:

* ~/projects/ledgerkit
* ~/projects/axiom-assure

Verify actual paths, branches, remotes and working-tree status before proceeding.

Preserve existing work. Do not overwrite uncommitted changes, rewrite published history or force-push.

Read the current Axiom files and plans rather than assuming the repository matches any earlier discussion.

## 3. Project purpose

Axiom Dev is intended to establish the simplest practical development methodology that allows AI agents to understand, specify, implement, verify and maintain software while preserving durable project knowledge.

The governing principles are:

Agents are transient. Project knowledge compounds.

Verification requires independently established evidence, not agent confidence.

Conventional engineering tools are preferred over custom infrastructure.

The methodology must demonstrate benefits sufficient to justify its overhead.

The development lifecycle is:

UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

Axiom Dev must use this lifecycle to develop itself.

Axiom Assure is a complementary experimental assurance project. It is not a Phase 1 dependency.

## 4. First task — inspect and amend the existing plan

Before implementing further functionality:

1. Inspect the existing repository, governance documents, roadmap, ADRs, phase plans, saved prompts and CI configuration.
2. Inspect CodeCompass's actual development practices and relevant findings.
3. Identify what has already been implemented and verified.
4. Amend the existing Phase 1 implementation plan rather than creating a competing plan.
5. Record material architectural changes through ADRs.
6. Independently review the amended plan.
7. Resolve material findings before implementation proceeds.

If Phase 1 planning has not yet been committed, establish the minimum necessary governance and planning foundation first.

### Amendment A — minimise bootstrap overhead

The initial plan risks recreating CodeCompass's procedural complexity.

Amend it so that:

* Governance files are concise and operational.
* Each required artifact has one clear purpose.
* AGENTS.md is the canonical shared agent guidance.
* CLAUDE.md contains only necessary Claude-specific guidance and links to AGENTS.md.
* CONTRIBUTING.md explains the process for human contributors without introducing competing rules.
* ADRs record actual consequential decisions, not speculative future options.
* Only immediately necessary directories are created.
* Detailed technical documentation is produced alongside the functionality it describes.
* Retrospectives and phase audits are proportional to the work.
* No permanent agent roster is created without demonstrated need.

Retain CodeCompass's development discipline while reducing unnecessary administrative work.

### Amendment B — strengthen independent verification

The Phase 1 self-development experiment must avoid circular verification.

Require:

* Behavioural contracts established before implementation.
* Independently reviewed acceptance criteria.
* Known-valid and deliberately defective test fixtures.
* Protected expected outputs that the implementation agent cannot silently modify.
* Independent evaluation of the initial implementation.
* Baseline behaviour recorded before refactoring.
* Before/after behavioural verification using the same accepted contracts.
* An explicit record of defects detected, missed and introduced.
* Clear separation between test results, Codex review findings and human acceptance.

A reviewer repeating the implementer's assumptions is not sufficient independent assurance.

### Amendment C — capture measurement from the beginning

Do not defer all evaluation until later Axiom phases.

From Phase 1 onward, record proportionate evidence of:

* Development effort.
* Agent usage and costs where available.
* CI and review overhead.
* Defects discovered.
* Rework required.
* Documentation maintenance effort.
* Knowledge reused from earlier development tasks.
* Failure cases and unresolved uncertainty.

Do not invent unavailable metrics.

### Amendment D — explicit acceptance demonstrations

The amended Phase 1 plan must require evidence that:

1. A fresh agent can resume development using repository knowledge alone.
2. A selected requirement can be traced from its original instruction through planning, decisions, implementation and verification.
3. A deliberately defective PR is rejected by the required CI gate.
4. A meaningful refactor preserves independently established behaviour.
5. Knowledge placement and documentation consistency are evaluated against real changes.
6. Documentation can be independently reconstructed from permitted evidence.
7. Knowledge accumulated during earlier development work is reused in a later task.
8. The methodology's overhead has been recorded and assessed.

A synthetic fixture is useful for testing a validator, but it cannot substitute for a required demonstration against the real Axiom repository.

## 5. Preserve the CodeCompass development methodology

Inspect and selectively incorporate CodeCompass practices from:

* CLAUDE.md
* CONTRIBUTING.md
* planning/
* decisions/
* planning/retros/
* Its original planning prompts and amendments.
* Its knowledge placement policy.
* Its documentation schema work.
* Its clean-room reconstruction and isolation findings.
* Its verification and phase closeout procedures.

Retain these practices from the beginning:

Plan before implementation. Each substage has an implementation-ready plan with scope, non-goals, dependencies, files, tests and acceptance criteria.

Preserve original prompts. Save initiating instructions and amendments under planning/prompts/, recording provenance. Preserve source wording rather than inventing reconstructed originals. Exclude credentials and sensitive material.

Use ADRs. Maintain numbered architectural decisions with context, alternatives, rationale, consequences and supersession references.

Maintain a roadmap. planning/ROADMAP.md distinguishes planned, active, completed, deferred and blocked work.

Maintain session continuity. planning/CONTEXT.md records current project state and the next concrete action.

Keep documentation synchronised. Update affected current-state documentation alongside implementation changes.

Record retrospectives. Capture discoveries, failures, process changes and overhead.

Independently assess completion. Require verification against actual artifacts before marking a substage complete.

Do not import CodeCompass implementation code or reproduce its complex record hierarchy unless a specific need is established.

## 6. Phase 1 implementation sequence

Execute the substages in dependency order.

### 1.0 — Repository governance and planning

Deliver the minimum viable repository foundation:

* README.md
* AGENTS.md
* CLAUDE.md
* CONTRIBUTING.md
* CHANGELOG.md
* planning/ROADMAP.md
* planning/CONTEXT.md
* Phase implementation plans.
* planning/prompts/ for original instructions.
* planning/retros/ for retrospectives.
* decisions/ for ADRs.
* Necessary documentation and pull-request templates.

Preserve the existing license.

Record the unavoidable bootstrap exception: the first governance commit precedes full implementation of the development controls.

Exit: A fresh agent can identify the project, its governing methodology, current status, important decisions and next authorised task using repository contents alone.

### 1.1 — Knowledge and documentation methodology

Establish a lightweight approach to:

* Concepts and durable domain knowledge.
* Behavioural contracts and invariants.
* Architectural decisions.
* Evidence and verification records.
* Unresolved questions.
* Knowledge relationships.
* Documentation schemas.
* Knowledge placement.
* Reconciliation after changes.

Distinguish INTENDED, OBSERVED, VERIFIED, UNCERTAIN and CONTESTED knowledge without treating them as interchangeable.

Use Git, Markdown and YAML wherever sufficient.

Create a small declarative documentation schema identifying audience, purpose, required sections, authoritative sources and acceptance criteria.

Do not build a documentation compiler or graph database.

Exit: Axiom's own documents use the conventions, and those conventions can be independently assessed.

### 1.2 — Development workflow and agent isolation

Establish the full development lifecycle and define logical responsibilities for:

* Planning and specification.
* Implementation.
* Independent verification.
* PR review.
* Documentation assessment.
* Knowledge reconciliation.
* Human decision-making.

Prefer ad-hoc, bounded agent dispatches rather than an extensive permanent agent roster.

Specify which artifacts an agent may read and modify.

For independent verification, distinguish:

* Separate reasoning contexts.
* Restricted source access.
* Protected acceptance criteria.
* Mechanically enforced isolation.

Do not claim strict isolation when access restrictions are only prompt-based.

Use existing operating-system and development tools for isolation when needed; do not create a general sandbox framework.

Exit: Another agent can execute a complete development cycle from the repository instructions, with explicit authority and verification boundaries.

### 1.3 — Codex pull-request CI gate

Implement an enforceable GitHub PR review workflow.

Research current supported Codex integration methods using authoritative documentation before selecting the implementation.

The required pipeline is:

1. Claude Code or another implementation agent develops a change.
2. The change is submitted as a GitHub PR.
3. Deterministic tests and validators execute.
4. Codex independently reviews the PR.
5. Codex findings are converted into a validated, enforceable check.
6. P0/P1 findings block merging.
7. Invalid, incomplete or failed reviews fail closed.
8. Lower-severity findings are recorded and dispositioned.
9. Accepted requirements and contracts remain protected.
10. Knowledge and documentation changes are reconciled before completion.

Avoid making Codex's natural-language review comment itself the only gate.

Use a machine-checkable review result and deterministic policy evaluation.

Ensure review results correspond to the actual PR revision being merged. A passing review of an obsolete commit must not authorise a later unreviewed change.

Follow secure GitHub Actions practices:

* Minimum permissions.
* No exposure of API credentials to untrusted PR code.
* Appropriate separation of privileged review and untrusted execution.
* Explicit handling of forked contributions.
* Secure secret storage.
* No uncontrolled execution of generated commands.

Assess API usage and costs before enabling recurring paid review calls.

Configure required GitHub status checks when repository permissions permit.

Do not bypass protection if configuration fails. Report the blocker.

Test:

* Valid PR.
* Known P0/P1 defect.
* Advisory finding.
* Malformed reviewer output.
* Missing or failed review.
* Review of an outdated commit.

Exit: Real GitHub PR evidence demonstrates both successful and blocked outcomes.

### 1.4 — Self-development and behaviour-preserving refactoring

Build a small, genuine Axiom component using the complete methodology.

Preferred candidate:

Axiom knowledge/documentation validator.

Initial functionality should be narrowly scoped to independently testable operations such as:

* Reading documentation schemas.
* Checking required sections.
* Validating local references.
* Checking ADR identifiers.
* Reporting useful validation errors.

Before implementation:

1. Establish accepted behavioural contracts.
2. Prepare independently reviewed expected outputs.
3. Create valid and invalid fixtures.
4. Record protected acceptance criteria.
5. Define measurable success and failure conditions.

Implement the component through the established PR process.

Then conduct a substantive refactoring exercise, such as separating schema parsing, validation rules and reporting without changing accepted external behaviour.

The refactoring must use the full process:

Understand → Specify → Assess Impact → Build → Verify → Reconcile.

The verification agent must compare the implementation against independently established contracts rather than relying exclusively on the implementing agent's tests.

Run the Codex gate on both initial implementation and refactoring PRs.

Review affected documentation, architectural decisions and knowledge placement.

Record actual defects and process overhead.

Exit: Axiom has developed and refactored its own component, with preserved behaviour and independent evidence.

### 1.5 — Independent reconstruction and Phase 1 assessment

Conduct a fresh-context documentation reconstruction.

Provide the reviewer with an explicitly permitted set of source files, accepted decisions, contracts and evidence.

Exclude existing explanatory documentation where necessary to prevent copying or anchoring.

Verify the access boundary where strict isolation is claimed.

Reconstruct the component's intended behaviour and architecture.

Compare that reconstruction with the current documentation.

Identify:

* Missing or inaccurate explanations.
* Contradictions.
* Stale documentation.
* Historical rationale presented as current.
* Knowledge placed in the wrong authoritative location.
* Weaknesses in traceability.
* Unverified claims.

Resolve material findings through the normal development workflow.

Conduct an independent Phase 1 closeout audit.

Exit: Every mandatory acceptance criterion has evidence, open limitations are recorded, and the repository accurately reflects the completed implementation.

## 7. Self-dogfooding rule

Every Phase 1 substage must use the strongest currently operational version of the Axiom methodology.

This necessarily involves progressive bootstrapping:

* Before the CI gate exists, use documented manual independent review.
* Once deterministic CI exists, use it for subsequent changes.
* Once the Codex gate exists, all subsequent relevant PRs must pass it.
* Once documentation schemas and validators exist, use them on Axiom's own documentation.
* Once reconciliation rules exist, apply them to all subsequent substantive changes.

Do not retroactively claim that earlier work passed controls that did not yet exist.

The purpose is to progressively establish a self-governing development environment.

## 8. Execution and orchestration rules

Act as the lead orchestrator.

Delegate bounded research, implementation, verification and documentation work where doing so improves independence or efficiency.

Maintain explicit task ownership and file-write boundaries.

Do not allow separate agents to make concurrent conflicting edits to authoritative project files.

Use fresh contexts for genuinely independent review.

Require agents to cite relevant source files, tests, commits and evidence rather than asserting completion.

For each substage:

1. Inspect current repository state.
2. Confirm the approved scope and relevant decisions.
3. Prepare or update the implementation plan.
4. Independently review the plan where warranted.
5. Implement the bounded change.
6. Run tests and independent verification.
7. Reconcile documentation and knowledge.
8. Record retrospective findings and overhead.
9. Independently assess completion.
10. Update roadmap and context only when justified.
11. Commit and push the completed change.

Do not mark work complete before its evidence is established.

Where a material architectural decision is genuinely unresolved, record it and use the established human approval boundary.

Do not stop for routine implementation choices that are already authorised by this instruction and the accepted plan.

## 9. Git and GitHub rules

Use ordinary Git branches and PRs.

Prefer small, logically coherent commits and independently reviewable changes.

Push completed work to the configured GitHub remote.

Use GitHub status checks and branch protection where supported.

Do not:

* Force-push or rewrite shared history.
* Bypass required checks.
* Commit credentials.
* Merge changes that have failed mandatory verification.
* Change approved behavioural contracts merely to satisfy an implementation.
* Falsely mark an incomplete phase as completed.

If GitHub settings, credentials, API access or costs prevent the required CI gate from operating, document the blocker and keep the relevant acceptance criterion open.

A local simulation cannot substitute for a required real GitHub merge-gate demonstration.

## 10. Evaluation requirements

Maintain a concise evidence log throughout Phase 1.

Record enough information to answer:

* What did the methodology require?
* What actually happened?
* Which defects were detected?
* Which defects escaped detection?
* What knowledge was preserved?
* Was that knowledge reused later?
* Did documentation remain accurate?
* How much overhead did the process introduce?
* Which practices proved unnecessarily expensive or complex?

Distinguish demonstrated findings from hypotheses.

Do not claim that Axiom improves development productivity merely because its own workflow operates.

Phase 1 establishes feasibility and produces initial evidence. Later controlled comparisons must establish whether it outperforms simpler alternatives.

## 11. Phase 1 Definition of Done

Phase 1 is complete only when all of the following are demonstrated:

* [ ] Repository governance is established and coherent.
* [ ] Original planning instructions and amendments are preserved.
* [ ] The roadmap, ADRs, contributor guidance and session continuity records are maintained.
* [ ] The lightweight knowledge and documentation methodology is implemented.
* [ ] Knowledge placement rules are defined and applied.
* [ ] Agent responsibilities and isolation limitations are explicit.
* [ ] Deterministic testing and documentation validation are operational.
* [ ] Codex PR review is an enforceable, tested CI gate.
* [ ] Deliberately defective changes have been blocked.
* [ ] An Axiom component has been genuinely developed.
* [ ] That component has undergone a meaningful refactor.
* [ ] Accepted external behaviour has been independently verified before and after refactoring.
* [ ] Documentation has undergone independent reconstruction and assessment.
* [ ] Relevant knowledge has been reconciled and demonstrably reused.
* [ ] Traceability exists from instruction to implementation and verification.
* [ ] Process costs, limitations and failures have been recorded.
* [ ] An independent closeout assessment supports completion.

If a requirement remains unmet, identify the blocker and leave Phase 1 open.

Do not substitute generated reports, synthetic fixtures or agent assertions for required real-world evidence.

## 12. Required deliverables

The completed Phase 1 repository should contain, as appropriate:

### Governance

* README and contributor guidance.
* Canonical agent instructions.
* Roadmap and session context.
* Original planning prompts.
* Architectural decisions.
* Phase plans and retrospectives.
* Changelog.

### Methodology

* Development lifecycle specification.
* Knowledge and documentation standards.
* Knowledge placement policy.
* Agent independence policy.
* Verification and reconciliation procedures.
* Lightweight schemas and examples.

### Implementation

* Documentation/knowledge validator.
* Deterministic tests and protected acceptance fixtures.
* CI workflows.
* Codex PR review gate.
* Evidence-backed refactoring demonstration.

### Evidence

* Test results.
* Independent verification findings.
* PR review results.
* Documentation reconstruction report.
* Knowledge reconciliation examples.
* Phase closeout assessment.
* Recorded implementation and process overhead.

Avoid speculative artifacts and redundant documents.

## 13. Final report

At the end of execution, provide:

1. Summary: What was amended, implemented and verified.
2. Plan amendments: Changes made in response to the review.
3. CodeCompass lessons: What was retained, simplified and excluded.
4. Phase status: Completion status for Stages 1.0–1.5.
5. Architecture: Implemented components and their responsibilities.
6. Verification: Real tests, PR checks, defects and results.
7. Dogfooding: Evidence of self-development, refactoring and knowledge reuse.
8. Costs and limitations: Actual measured overhead and unresolved issues.
9. GitHub: Branches, commits, PR links and merge status.
10. Next step: Readiness for the Ledgerkit Phase 2 demonstration.

Report partial completion accurately if any acceptance gate remains unmet.

## 14. Final instruction

First inspect and amend the existing Phase 1 plan. Then implement the amended plan sequentially, subject to its verification and acceptance requirements.

Do not stop after writing the amended plan unless a genuine blocker prevents authorised implementation.

Do not replace the original engineering objective with an elaborate governance or orchestration system.

The intended result is:

Axiom Dev v0.1 — a lightweight, documented, independently verified development methodology that has successfully developed, tested, documented and refactored its own implementation.

Proceed.
