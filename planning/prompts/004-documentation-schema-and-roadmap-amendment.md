---
id: 004
title: Documentation Schema and Roadmap Amendment
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002, 003]
---

> **Provenance note.** The text below is the complete, verbatim prompt
> that authorised moving documentation schemas out of embedded Markdown
> front-matter into companion `.schema.yaml` files, expanding
> `planning/ROADMAP.md` beyond Phase 1, and establishing a phase-archiving
> procedure. Preserved unmodified as historical source material, per
> `AGENTS.md` §2/§3 and this project's established convention (prompts
> 001–003) of keeping prompts with provenance, never reconstructed from
> memory. Harness-level wrapper content (system reminders, tool-call
> metadata, environment blocks) is excluded as it is not part of the
> assignment; the assignment text is otherwise reproduced exactly as
> written, including its own internal section numbering.
>
> Relationship to prior work: this is **amendment 004** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued by
> `002-phase-1-amend-and-implement.md` and
> `003-phase-1-corrective-amendment.md`. It does not replace any of them;
> all four are preserved. See
> `decisions/0006-companion-schema-files.md` for the resulting ADR and
> `planning/phase-02-documentation-schema-and-roadmap.md` for this
> amendment's own focused implementation plan.

AXIOM DEV — DOCUMENTATION SCHEMA AND ROADMAP AMENDMENT
1. Assignment
You are the Claude Code orchestrator responsible for implementing a focused architectural amendment to Axiom Dev.
Repository: `ctosullivan/axiom-dev`
Expected local location: `~/projects/axiom-dev`
This amendment has two primary objectives:

1. Move documentation schemas out of Markdown front matter into separate YAML files, improving human readability and separating documentation from its verification contract.
2. Expand the project roadmap beyond Phase 1, establishing a clear long-term development direction and a repeatable procedure for archiving completed phases.

The changes must be implemented using Axiom's existing evidence-based development methodology.
Do not restart Phase 1, recreate existing components or introduce unnecessary infrastructure.
Before implementing anything, inspect the repository's current state, active branch, existing contracts, tests, decisions and documentation.
The previously inspected development branch was:
`phase-1/stage-1.0-bootstrap`
Do not assume this remains the current working branch.
2. Governing principles
Preserve Axiom Dev's existing development lifecycle:
UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE
The purpose of Axiom Dev is to establish the simplest practical conventional development methodology that supports:

* Evidence-based software development.
* Reliable knowledge preservation across agent sessions.
* Independent verification of implementation and documentation.
* Behavioural contracts and reproducible tests.
* Knowledge reconciliation following changes.
* Long-term maintainability without excessive procedural overhead.

Prefer Git, Markdown, YAML, Python, conventional CI and native Codex GitHub review.
Do not introduce a database, knowledge graph, documentation compiler, custom orchestration framework or additional runtime services.
3. Current implementation to inspect
Relevant existing files include:

* `AGENTS.md`
* `CLAUDE.md`
* `CONTRIBUTING.md`
* `README.md`
* `planning/ROADMAP.md`
* `planning/CONTEXT.md`
* `planning/phase-01-foundation.md`
* `planning/prompts/`
* `planning/retros/`
* `decisions/`
* `docs/documentation-schema.md`
* `docs/governed-documents.txt`
* `docs/knowledge-placement.md`
* `docs/knowledge-reconciliation.md`
* `docs/development-lifecycle.md`
* `docs/axiom-validator.md`
* `contracts/documentation-schema-validator.md`
* `src/axiom_validator/`
* `tests/`
* `.github/workflows/deterministic-checks.yml`
* `evidence/`

The documentation validator currently uses YAML front matter embedded directly in Markdown.
A previous corrective amendment strengthened its field validation, introduced a governed-document manifest and added the validator tests to CI.
Preserve those improvements.
The existing accepted decisions and historical evidence must remain traceable.
4. Amendment A — Separate documentation from its schema
Architectural decision
Markdown documents should contain human-facing documentation, not embedded validation metadata.
Move the existing YAML front matter into separate companion files.
Use this naming convention:

```
README.md
README.md.schema.yaml

docs/
    axiom-validator.md
    axiom-validator.md.schema.yaml

    knowledge-placement.md
    knowledge-placement.md.schema.yaml

    development-lifecycle.md
    development-lifecycle.md.schema.yaml
```

Place each schema alongside the Markdown document it governs.
The relationship must be deterministic:
`<document>.md` → `<document>.md.schema.yaml`
Do not require a separate registry of schema-to-document mappings.
The existing governed-document manifest may continue identifying which Markdown documents require schemas.
Rationale
Documentation and its schema serve different purposes.
The Markdown document explains the system to a human reader.
The YAML schema specifies the requirements against which that explanation can be checked.
Separating them provides:

1. Cleaner Markdown rendering in GitHub and VS Code.
2. A more natural reading experience.
3. Explicit separation between explanation and acceptance contract.
4. Independent evolution and review of documentation requirements.
5. Reuse of ordinary Markdown tooling.
6. Continued compatibility with deterministic validation and agent-based semantic review.

The primary optimisation objective is reducing total development and maintenance complexity, not merely minimising the number of repository files.
Example
Current format:

```
---
audience: developers and agents
purpose: explain the documentation validator
required_sections:
  - Purpose
  - Architecture
  - Usage
  - Limitations
authoritative_sources:
  - src/axiom_validator/__init__.py
acceptance_criteria:
  - architecture matches the actual implementation
---

# Axiom Validator

## Purpose

The validator checks documentation...
```

Required new format:
`docs/axiom-validator.md`

```
# Axiom Validator

## Purpose

The validator checks documentation...

## Architecture

The implementation consists of...

## Usage

Run the validator using...

## Limitations

The validator does not...
```

`docs/axiom-validator.md.schema.yaml`

```
audience: developers and agents
purpose: explain the documentation validator

required_sections:
  - Purpose
  - Architecture
  - Usage
  - Limitations

authoritative_sources:
  - src/axiom_validator/__init__.py

acceptance_criteria:
  - architecture matches the actual implementation
```

The schema retains its existing purpose and substantive requirements.
Only its location and the validator's loading mechanism should change.
5. Amendment B — Migrate existing documentation
Inspect all repository Markdown files for embedded YAML front matter.
For each schema-bearing document:

1. Extract the existing YAML schema.
2. Create the corresponding `.md.schema.yaml` file.
3. Remove the front matter from the Markdown document.
4. Preserve the substantive Markdown content.
5. Preserve the original schema's meaning and acceptance criteria.
6. Verify that source references still resolve.
7. Verify that the resulting document renders cleanly in standard Markdown viewers.

Do not perform unrelated rewriting or stylistic changes during migration.
Do not silently discard metadata.
Historical evidence and retrospectives must remain historically accurate. If their schemas are migrated, preserve their substantive content and record the migration as a format change, not a change to the historical findings.
Accepted ADRs must not be rewritten to make historical decisions appear different.
The previous decision to use front matter must be superseded through a new ADR explaining the architectural change.
Required migration evidence
For each migrated document, verify that:

* The Markdown body is unchanged apart from removing the front matter and any strictly necessary formatting.
* The extracted schema retains its original requirements.
* The schema is discoverable through the naming convention.
* Existing relative links remain valid.
* The new validator accepts the migrated document and its schema.

Produce a concise migration report identifying migrated files and any exceptions.
6. Amendment C — Adapt the documentation validator
Update the existing validator to load schemas from companion YAML files.
Do not replace the validator with a new implementation.
Preserve its modular architecture:

* Parsing.
* Rules.
* Reporting.
* Orchestration.
* CLI.

Required behaviour
For a governed Markdown document:

1. Locate its companion `.md.schema.yaml`.
2. Report a failure if the required schema is missing.
3. Parse and validate the YAML.
4. Validate the required fields and their types.
5. Check that required sections exist in the Markdown body.
6. Check authoritative-source paths.
7. Check relevant relative links.
8. Return useful, actionable validation errors.

For a non-governed document:

* If a companion schema exists, validate it.
* If no companion schema exists, retain the existing `SKIPPED` behaviour unless a reviewed contract change explicitly specifies otherwise.

The validator should detect an orphaned schema where practical, rather than silently accepting a schema with no corresponding document.
Accidental reintroduction of YAML validation front matter should be detected or explicitly reported.
Do not silently support two competing schema conventions indefinitely.
Existing mechanical validation
Preserve the current rules covering:

* Required schema fields.
* Non-empty required content.
* Field types.
* Required headings.
* Authoritative-source paths.
* Repository path containment.
* Relative links.
* ADR references.
* Governed-document requirements.

Preserve the distinction between structural and semantic checks.
The validator must not claim that a document is factually accurate simply because its schema passes.
Compatibility
Preserve the public CLI and programmatic interface where practical:

```
PYTHONPATH=src python3 -m axiom_validator README.md --repo-root .
```

If a breaking interface change is genuinely necessary, document and independently review it.
Contract-first requirement
Amend the accepted documentation-validator contract before changing implementation behaviour.
Explicitly document the change from embedded front matter to companion schema files.
This is an authorised contract evolution, not a behaviour-preserving refactor.
Preserve the historical Stage 1.4 baseline and evidence. Existing tests or fixtures may be migrated only through a documented, independently reviewed contract change.
Do not rewrite historical evidence to imply that the original implementation used sidecar schemas.
7. Amendment D — Tests and CI
Update deterministic tests to cover the new schema convention.
Include tests for:

* Valid document with valid companion schema.
* Missing schema for a governed document.
* Missing schema for a non-governed document.
* Malformed YAML.
* Missing required fields.
* Incorrect field types.
* Empty required values.
* Missing required headings.
* Broken authoritative-source references.
* Links escaping the repository.
* Orphaned schemas.
* Accidental embedded front matter.
* Existing ADR-reference behaviour.

Verify that schema migration does not weaken the intended documentation controls.
Update:
`.github/workflows/deterministic-checks.yml`
The workflow must continue running the policy-evaluator tests, validator tests and governed-document checks.
It must validate the new companion-schema format.
No API keys or paid AI invocations should be necessary for deterministic CI.
Use real tests and captured results, not statements that tests are expected to pass.
8. Amendment E — Expand the roadmap beyond Phase 1
The current `planning/ROADMAP.md` is primarily a detailed Phase 1 record.
Replace this structure with a concise, long-term project roadmap.
The roadmap should answer:

1. What is Axiom Dev trying to achieve?
2. What phases are planned?
3. What is the purpose of each phase?
4. What evidence is required to complete each phase?
5. Which phase is currently active?
6. Which phases are completed, proposed, blocked or deferred?
7. Where can previous phases be found?

Keep detailed implementation plans separate from the roadmap.
Proposed long-term structure
Use the following direction as the initial proposal, refining it against existing project plans and decisions.
Phase 1 — Foundation
Establish and test the basic evidence-based development methodology.
Includes:

* Governance.
* Knowledge placement.
* Documentation schemas.
* Behavioural contracts.
* Independent review.
* Deterministic CI.
* Self-development.
* Refactoring.
* Documentation reconstruction.

Exit evidence:
Working methodology, demonstrated internal use, independent verification and accepted Phase 1 closeout.
Current status: In progress until outstanding acceptance requirements are met.
Phase 2 — Real-world validation
Apply the methodology to a substantive development task in an existing project.
Ledgerkit is the preferred candidate.
Potential activities:

* Select a bounded, meaningful Ledgerkit development objective.
* Establish an independently reviewed behavioural contract.
* Measure baseline development performance.
* Execute the work using Axiom Dev.
* Compare against a simpler conventional agent-development approach where a fair comparison is feasible.
* Record defects, rework, effort, verification coverage and knowledge reuse.
* Evaluate whether Axiom's additional procedures deliver value exceeding their overhead.

Exit evidence:
A credible, reproducible real-world evaluation that distinguishes demonstrated improvements from unresolved hypotheses.
Do not claim superiority over alternative development methods before the evidence exists.
Phase 3 — Methodology consolidation and reusable template
Refine the methodology based on Phase 2 findings.
Potential activities:

* Remove unnecessary procedures.
* Simplify governance and documentation.
* Consolidate reusable contracts, checks and workflows.
* Produce an Axiom Dev starter/template repository.
* Demonstrate that a fresh agent can use the template to develop and verify a bounded change.

Exit evidence:
A reusable, documented development template with a successful independent adoption exercise.
Phase 4 — Broader validation and release
Evaluate the methodology across additional projects and development scenarios.
Potential activities:

* Cross-project trials.
* Maintenance and refactoring exercises.
* Documentation reconstruction after substantial change.
* Comparison of verification approaches.
* Usability and overhead assessment.
* Versioned release of the methodology and template.

Exit evidence:
A stable release with documented capabilities, limitations and reproducible supporting evidence.
Roadmap requirements
These later phases are proposals, not authorised implementation commitments.
Keep their descriptions appropriately high-level.
Do not invent completion dates, measured benefits or acceptance results.
A phase becomes actionable only after its focused implementation plan has been written, independently reviewed and approved as required by existing governance.
Retain the existing status vocabulary:

* Proposed.
* Planned.
* In progress.
* Completed.
* Deferred.
* Blocked.

The roadmap should contain a compact overview table followed by short phase summaries and links to the detailed plans.
Do not duplicate extensive implementation history in the active roadmap.
9. Amendment F — Establish phase archiving
Introduce a simple, repeatable procedure for archiving a phase after completion.
The purpose of archiving is to preserve evidence and historical decisions while keeping the active roadmap and session context concise.
Archive structure
Use:

```
planning/
    ROADMAP.md
    CONTEXT.md

    phase-01-foundation.md

    phase-02-validation.md
    phase-03-consolidation.md

    archive/
        README.md

        phase-01/
            README.md

        phase-02/
            README.md
```

This is a proposed logical structure, not an instruction to create every future file immediately.
Do not create empty phase directories or speculative implementation plans.
Archive contents
When a phase is completed, its archive entry should identify:

* Phase number and title.
* Objective.
* Actual completion status and date.
* Accepted scope.
* Completion evidence.
* Independent closeout findings.
* Relevant ADRs.
* Associated contracts.
* Retrospective.
* Final approved PR or Git commit.
* Important limitations or deferred work.
* Links to historical phase plans and artifacts.

Use Markdown.
Avoid copying entire contracts, evidence files or ADRs into the archive.
An archive is an index of verified historical artifacts, not a duplicated knowledge store.
Phase completion procedure
Implement and document this procedure:
Step 1 — Verify
Run deterministic checks and required independent review.
Compare the results against the accepted phase completion criteria.
Identify outstanding defects, incomplete requirements and uncertainties.
Step 2 — Close out
Produce an independent closeout assessment.
Record which acceptance criteria were met, which were not, and the evidence supporting each conclusion.
Step 3 — Obtain human approval
A phase must not be marked Completed merely because an agent believes its work is finished.
Human approval is required under `AGENTS.md`.
Step 4 — Reconcile
Ensure the roadmap, session context, contracts, documentation and evidence reflect the accepted final state.
Unfinished work must be explicitly deferred, rejected or transferred to a later phase.
Do not silently lose outstanding requirements.
Step 5 — Archive
Create the phase's archive entry under:
`planning/archive/phase-XX/README.md`
Include the historical summary and links to authoritative artifacts.
Record the accepted completion commit or PR and the scope of the independent closeout.
Preserve the original phase plan at its established canonical path unless a separately reviewed migration demonstrates that moving it will not break existing references.
Logical archiving is preferred to unnecessary file relocation.
Mark the archived phase as historical and avoid modifying its completed plan except through an explicitly documented correction or superseding decision.
Step 6 — Update the active roadmap
Reduce the completed phase's roadmap entry to a concise summary and archive link.
Keep the phase visible in the roadmap as Completed.
Move detailed historical narrative out of the active roadmap.
Step 7 — Prepare the next phase
Update `planning/CONTEXT.md` with:

* Current active phase.
* Current implementation baseline.
* Relevant accepted decisions.
* Outstanding issues.
* Next concrete action.

The next phase must still receive its own accepted implementation plan before substantive work begins.
Archive verification
Add proportionate checks that:

* Archived phases are marked Completed in the roadmap.
* Archive entries link to existing phase plans and evidence.
* Completion evidence and independent closeout references exist.
* No unfinished phase has been archived as completed.
* Active documentation does not depend on silently duplicated historical records.

Prefer existing link-validation mechanisms and independent review.
Do not build an archival database or bespoke project-management system.
Important Phase 1 restriction
Do not archive Phase 1 yet.
Phase 1 remains open until its outstanding requirements, including native Codex GitHub PR review and human acceptance, are satisfied.
This amendment should establish and test the archiving procedure without fabricating a completed phase.
10. Amendment G — Documentation and governance reconciliation
This change affects established architectural decisions and development procedures.
Create an ADR documenting the move from embedded front matter to companion YAML schema files.
Explain:

* The original rationale for front matter.
* Its readability disadvantages.
* The alternative of separate companion files.
* The additional file-maintenance cost.
* Why the new approach is preferable overall.
* How deterministic validation limits schema/document drift.
* Why semantic verification remains necessary.

Update relevant governance documentation to describe:

* Schema file placement.
* Which documents require schemas.
* How schemas are validated.
* How documentation acceptance criteria are independently reviewed.
* How the long-term roadmap works.
* How completed phases are archived.

Preserve the distinction between:
Current implementation
Accepted policy
Proposed future functionality
Historical evidence
Do not describe proposed phases as implemented capabilities.
Do not rewrite previous ADR reasoning as though the new approach had always been accepted.
11. Preserve the existing Codex review decision
The earlier corrective amendment replaced the Phase 1 API-backed Codex CI gate requirement with native Codex GitHub PR review.
That decision remains in force.
For this amendment:

* Use native Codex GitHub PR review.
* Do not request or require an `OPENAI_API_KEY`.
* Keep the custom API-backed Codex workflow deferred.
* Continue running deterministic checks in GitHub Actions.
* Do not claim automated AI merge enforcement exists.
* Record and disposition significant Codex review findings.
* Preserve human approval requirements for merging and phase acceptance.

Do not reopen the Codex integration architecture unless a concrete new requirement justifies doing so.
12. Required implementation sequence
UNDERSTAND
Inspect the repository, current schema convention, validator, tests, CI, roadmap and governance rules.
Identify every document affected by schema migration.
SPECIFY
Preserve this amendment under `planning/prompts/` with provenance.
Create a focused implementation plan.
Record the new architectural decision.
Define and independently review the updated validator contract and migration acceptance criteria before implementation.
ASSESS IMPACT
Identify all affected source files, documentation, tests, fixtures, CI workflows, contracts and knowledge records.
BUILD
Implement:

1. Companion schema convention.
2. Migration of existing schemas.
3. Validator changes.
4. Regression tests.
5. CI changes.
6. Expanded roadmap.
7. Phase-archiving procedure.
8. Documentation and governance updates.

Keep the changes focused.
VERIFY
Run the complete deterministic test suite.
Independently check the migration, including the preservation of Markdown content and schema requirements.
Inspect the resulting documentation in its ordinary rendered form.
Independently review the expanded roadmap and phase-archiving procedure.
Confirm that the archive process can be followed without inventing missing steps.
RECONCILE
Update documentation, current state, planning records and evidence.
Record all material findings, corrections and unresolved issues.
Prepare the changes for native Codex GitHub PR review.
Do not merge or mark a phase Completed without the required human approval.
13. Definition of Done
This amendment is complete when:

* Every existing schema-bearing Markdown document has been assessed and migrated or explicitly excepted.
* Governing Markdown documents render without embedded YAML validation metadata.
* Companion schemas use one consistent naming convention.
* The validator discovers and validates companion schemas.
* Governed documents cannot silently bypass validation by deleting their schema.
* Missing, malformed and orphaned schemas are covered by tests.
* Existing mechanical validation requirements remain effective.
* The validator contract is amended with independently reviewed acceptance criteria.
* Historical refactoring evidence is preserved accurately.
* Relevant deterministic tests pass.
* GitHub Actions validates the new schema convention.
* `planning/ROADMAP.md` covers Phases 1–4 with appropriate status and acceptance expectations.
* Future phases remain proposals until separately authorised.
* A clear, lightweight phase-archiving procedure exists.
* Archive entries have a defined location and minimum required content.
* Historical phase plans and evidence remain accessible.
* Phase 1 is not prematurely archived or marked Completed.
* Documentation and governance are reconciled.
* Independent review findings are recorded and dispositioned.
* Native Codex GitHub review is requested on the resulting PR, with completion status reported accurately.
* Human approval is obtained before merging or changing completion status.

14. Final report
Provide a concise implementation report containing:

1. Updated repository structure.
2. List of migrated documentation schemas.
3. Summary of validator changes.
4. Updated test results.
5. CI status.
6. Expanded roadmap overview.
7. Phase-archiving procedure and example archive entry.
8. New ADR and superseded decision references.
9. Independent verification findings.
10. PR URL and native Codex review status.
11. Remaining issues and next actions.

Include before-and-after excerpts demonstrating the readability improvement.
Do not claim the work is verified without evidence.
15. Final instruction
Implement this amendment using the existing Axiom development methodology.
Optimise for a simple, understandable repository that a human can browse and an independent agent can reliably assess.
The intended result is:

* Clean Markdown documentation.
* Separate, checkable documentation schemas.
* Minimal deterministic validation.
* Independent semantic review where justified.
* A roadmap covering the full development direction.
* Completed phases preserved through an orderly, evidence-backed archive.
* No unnecessary infrastructure.

Preserve the existing Phase 1 achievements and outstanding review requirements.
Proceed with planning, implementation, independent verification and preparation for GitHub review.
