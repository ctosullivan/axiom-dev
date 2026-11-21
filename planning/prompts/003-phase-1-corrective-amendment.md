---
id: 003
title: Phase 1 Corrective Amendment and Implementation
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002]
---

> **Provenance note.** The text below is the complete, verbatim prompt that
> authorised this corrective amendment to Phase 1 — fixing documentation
> drift, strengthening the documentation/knowledge validator's schema
> validation, adding deterministic CI integration for it, replacing the
> API-backed Codex CI gate with native Codex GitHub PR review for Phase 1,
> and preparing a reviewable GitHub PR. Preserved unmodified as historical
> source material, per `AGENTS.md` §2/§3 and this project's own convention
> (established in `001-phase-1-bootstrap.md` and
> `002-phase-1-amend-and-implement.md`) of keeping prompts with provenance,
> never reconstructed from memory. Harness-level wrapper content (system
> reminders, tool-call metadata, environment blocks) is excluded as it is
> not part of the assignment; the assignment text is otherwise reproduced
> exactly as written, including its own internal section numbering.
>
> Relationship to prior work: this is **amendment 003** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued by
> `002-phase-1-amend-and-implement.md`. It does not replace either; all
> three are preserved. See
> `decisions/0005-native-codex-review-and-deferred-automated-gate.md` for
> the resulting ADR and `planning/phase-01-foundation.md` §17 for the plan
> amendment this prompt required.

AXIOM DEV — PHASE 1 CORRECTIVE AMENDMENT AND IMPLEMENTATION

1. Assignment

You are the lead Claude orchestrator responsible for completing the remaining corrective work for Axiom Dev Phase 1.

The project has already implemented substantial functionality, including its development methodology, documentation schema, knowledge placement policy, behavioural contracts, documentation validator, refactoring demonstration and independent documentation reconstruction.

Your assignment is not to restart Phase 1 or redesign Axiom Dev.

Instead:

1. Inspect the actual repository and its current Phase 1 evidence.
2. Amend the existing plan and architectural decisions to reflect the requirements below.
3. Correct identified documentation drift and schema-validation weaknesses.
4. Improve documentation acceptance and independent semantic review.
5. Complete deterministic CI integration for the existing validator.
6. Replace the Phase 1 API-backed Codex gate requirement with native Codex GitHub PR review.
7. Preserve the existing refactoring evidence and make any necessary corrections to its documentation.
8. Independently verify the corrective changes.
9. Prepare and push a reviewable GitHub PR.
10. Record remaining requirements and obtain human approval before declaring Phase 1 complete.

Do not introduce unnecessary new infrastructure.

2. Repository and historical context

Primary repository:

~/projects/axiom-dev

GitHub:

https://github.com/ctosullivan/axiom-dev

Previously inspected development branch:

phase-1/stage-1.0-bootstrap

Historical reference:

~/projects/codecompass

Related repositories:

* ~/projects/ledgerkit
* ~/projects/axiom-assure

Inspect the actual repository state before making changes.

Do not assume the previously inspected branch, commit or outstanding findings are still current.

Important existing artifacts include:

* AGENTS.md
* CLAUDE.md
* CONTRIBUTING.md
* planning/ROADMAP.md
* planning/CONTEXT.md
* planning/phase-01-foundation.md
* planning/prompts/
* decisions/0001 through 0004
* docs/documentation-schema.md
* docs/knowledge-placement.md
* docs/knowledge-reconciliation.md
* docs/development-lifecycle.md
* docs/agent-isolation.md
* docs/axiom-validator.md
* contracts/documentation-schema-validator.md
* contracts/codex-gate-policy-evaluator.md
* src/axiom_validator/
* tests/test_axiom_validator.py
* .github/scripts/policy_evaluator.py
* .github/workflows/
* evidence/stage-1.4-baseline.md
* evidence/stage-1.4-refactor.md
* evidence/stage-1.5-reconstruction.md
* evidence/phase-1-closeout.md

Inspect the original sources rather than relying on their titles or previous agent summaries.

3. Preserve Axiom's governing principles

Axiom Dev exists to develop the simplest practical evidence-backed methodology for AI-assisted software engineering.

Its development lifecycle remains:

UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

The following principles are unchanged:

* Agents are transient; project knowledge should compound.
* Contracts describe intended behaviour.
* Tests and observations provide evidence.
* Verification must not be based solely on the implementing agent's assertions.
* Knowledge should have an identifiable authoritative location.
* Historical decisions must not masquerade as current design justification.
* Development should follow version-controlled plans and ADRs.
* Git, Markdown, YAML, Python and conventional CI are preferred over custom infrastructure.
* Axiom should retain CodeCompass's valuable engineering discipline without recreating its complexity.

Apply the existing methodology to this corrective amendment.

4. Amendment A — Change Phase 1 Codex review strategy

This is an explicit change to the previously accepted Phase 1 implementation plan.

New decision

During Phase 1, Codex review will be performed through native Codex GitHub PR review, using an available ChatGPT/Codex account and GitHub integration.

An OpenAI API key is not required or expected for Phase 1.

The previously proposed custom API-backed Codex GitHub Actions review gate is deferred.

Automated Codex-derived required status checks, P0/P1 merge blocking and related live-gate scenarios are not Phase 1 exit requirements under the amended methodology.

Deterministic tests must continue to run in GitHub Actions, but configuring branch protection or required merge-status checks is not a prerequisite for Phase 1 closeout.

Required Phase 1 review workflow

1. Claude Code develops a bounded change according to an accepted plan.
2. Deterministic tests and documentation checks execute.
3. The change is pushed to a GitHub branch.
4. A pull request is opened.
5. Codex reviews the actual PR using the native GitHub integration.
6. Findings are independently assessed and explicitly dispositioned.
7. Significant findings are corrected.
8. Where necessary, a follow-up Codex review is requested.
9. The reviewed commit, findings, corrections and verification evidence are recorded.
10. A human makes the final merge and acceptance decision.

Use @codex review where supported by the connected Codex GitHub integration.

Verify the actual integration is available rather than assuming it works.

Review severity

P0 and P1 findings must be resolved or explicitly escalated to the human decision-maker before acceptance.

P2 and advisory findings require disposition but do not automatically prevent acceptance.

Codex-generated findings must not be treated as inherently correct. Check important claims against code, tests, contracts and other evidence.

Distinguish review from enforcement

A native Codex PR review is an independent AI review mechanism.

It is not automatically an enforceable GitHub CI gate.

Never describe this Phase 1 arrangement as mechanically preventing an unauthorised merge.

Record the human acceptance boundary and its limitations accurately.

Existing Codex Action

Inspect:

* .github/workflows/codex-review.yml
* .github/scripts/policy_evaluator.py
* Its contract and test suite.

Remove or disable the untested API-dependent review workflow from the active Phase 1 path so skipped jobs cannot be confused with successful reviews.

Preserve the deterministic policy evaluator and its tests as reusable experimental material where justified.

Do not delete working, verified components merely because their live integration is deferred.

Record the original automatic-gate requirement as superseded, not secretly satisfied.

Prepare an ADR documenting:

* The original requirement.
* The revised decision.
* Why native Codex review is preferable for this MVP.
* The independence and enforcement trade-offs.
* What remains deferred.
* Conditions under which an automated gate should be reconsidered.

Update the roadmap, Phase 1 plan, contributor instructions, agent instructions and evidence requirements consistently.

This prompt authorises proposing the governance changes and preparing them for review. Do not bypass the repository's human approval requirements or merge without approval.

5. Amendment B — Correct documentation drift

Previous independent inspection identified specific current-state documentation defects.

Verify whether each remains present.

B1. Canonical agent instructions

AGENTS.md previously contained wording indicating that no implemented source code yet required its testing rules.

This became inaccurate after Stage 1.4 implemented the validator.

Correct the relevant section to describe the actual requirements and existing implementation.

Ensure AGENTS.md remains the canonical shared agent guidance.

B2. Contributor instructions

CONTRIBUTING.md previously retained a statement referring to a pre-Stage-1.4 repository with no source code.

Another section had already been updated, demonstrating that partial reconciliation can leave inconsistencies elsewhere.

Review the entire document, not only the previously corrected section.

B3. Knowledge placement and enforcement

docs/knowledge-placement.md described mechanical validation and enforcement using language that was partly prospective.

Distinguish accurately among:

* Policy defined.
* Mechanism implemented.
* Mechanism locally tested.
* Mechanism executed by CI.
* Mechanism enforced as a required merge condition.
* Semantic or editorial review performed manually.

Do not imply that the existing validator enforces sequential ADR numbering or complete documentation correctness unless it actually does.

B4. Wider current-state reconciliation

Review:

* README.
* Development lifecycle.
* Agent isolation.
* Documentation schema.
* Knowledge reconciliation.
* Validator documentation.
* Roadmap and session context.
* Contributor and agent instructions.

Identify statements that are outdated, contradictory, prematurely marked complete, or expressed as future functionality even though the feature now exists.

Distinguish legitimate historical descriptions from inaccurate current-state descriptions.

Historical evidence files and ADRs should retain historical truth.

Do not rewrite history to make earlier stages appear more successful.

Acceptance

Record each confirmed defect, its authoritative source, the correction and the verification performed.

A broad claim that documentation has been reconciled is insufficient without identifying what was inspected.

6. Amendment C — Strengthen lightweight schema validation

Preserve Axiom's existing YAML-front-matter approach.

Do not implement a documentation compiler, knowledge graph or separate documentation database.

Existing weakness

The validator currently requires the presence of five fields:

* audience
* purpose
* required_sections
* authoritative_sources
* acceptance_criteria

However, its current implementation does not fully validate their types or meaningful content.

For example, a document containing empty strings and empty arrays can satisfy the structural checks.

Required improvement

Review and amend the accepted validator contract before changing its implementation.

Introduce proportionate mechanical validation for:

* Correct field types.
* Non-empty audience and purpose.
* Non-empty required sections for governed substantive documents.
* Non-empty, meaningful acceptance criteria.
* Correctly typed source references.
* Valid path and reference syntax.
* Existing accepted link and ADR-reference behaviours.

Allow explicitly justified empty source lists where a document legitimately has no internal authoritative dependencies.

Define the rule clearly rather than introducing arbitrary placeholder sources.

Governed document scope

The existing validator treats documents without YAML front matter as SKIPPED.

Preserve that behaviour where appropriate.

However, define which important documents must carry schemas, or use a small explicit manifest of governed documents.

Otherwise, deleting a document's schema could silently bypass its checks.

Keep this mechanism minimal.

Tests

Add positive and negative test fixtures covering the new validation rules.

Preserve the historical Stage 1.4 refactoring baseline.

Do not rewrite or silently replace its fixtures, checksums or recorded test results.

New validation behaviour must be introduced through an explicit, independently reviewed contract amendment with its own regression tests.

7. Amendment D — Treat documentation schemas as acceptance contracts

The current validator checks structural properties but cannot verify semantic correctness.

That distinction must remain explicit.

The next improvement is not a more elaborate document-generation system.

Instead, use the schema's acceptance_criteria to guide a bounded independent documentation review.

Required review procedure

For each substantive document selected for semantic review:

1. Read its declared audience, purpose, required sections, authoritative sources and acceptance criteria.
2. Independently inspect the authoritative sources.
3. Determine which criteria can be established from observable evidence.
4. Compare the document's claims against that evidence.
5. Classify each criterion as:
    * VERIFIED: Supported within the stated scope by identified evidence.
    * FAILED: Contradicted by identified evidence.
    * UNCERTAIN: Not established from the available evidence.
6. Cite the relevant files, code, tests or decisions supporting each finding.
7. Record corrective actions and remaining uncertainties.

Do not promote an agent's confident opinion to VERIFIED.

Example

A document may declare:

acceptance_criteria:
  - architecture description matches the current implementation

The reviewer should inspect the actual modules, reconstruct their responsibilities, compare those findings against the document, and record any discrepancies.

The mere existence of an Architecture heading is not sufficient.

Scope

Apply this procedure to a small selection of high-value Phase 1 documents, including:

* docs/axiom-validator.md
* docs/knowledge-placement.md
* docs/development-lifecycle.md

Use the findings to evaluate whether the review adds value.

Do not impose exhaustive semantic review on every Markdown file.

Isolation

Use fresh-context review where practical.

For documentation reconstruction, restrict the initial evidence set so the reviewer does not simply paraphrase the explanatory document being evaluated.

Distinguish prompt-based exclusion from mechanically enforced access restrictions.

Do not claim clean-room independence unless it is technically established.

8. Amendment E — Complete deterministic CI integration

The existing deterministic GitHub workflow runs the policy-evaluator tests but does not execute the validator's own test suite.

Correct this omission.

The deterministic workflow should:

1. Install the project's declared dependencies.
2. Execute the policy-evaluator test suite.
3. Execute the validator test suite.
4. Validate the selected governed documentation files.
5. Fail on applicable mechanical validation errors.
6. Preserve useful failure output.
7. Require no OpenAI API key or paid model invocation.

Do not make advisory semantic findings automatically block CI.

The workflow should accurately distinguish:

* Passing tests.
* Passing document structure checks.
* Unperformed semantic checks.
* Native Codex review status.
* Deferred merge-gate enforcement.

Verify the workflow on an actual GitHub commit or PR.

9. Amendment F — Preserve and assess the refactoring demonstration

The Stage 1.4 validator refactor is already a substantive achievement.

Git history previously showed:

* An initial monolithic src/axiom_validator.py.
* A subsequent modular src/axiom_validator/ package.
* Separation of parsing, rule evaluation, reporting, orchestration and CLI responsibilities.
* An accepted pre-refactor contract.
* Protected tests and fixtures.
* Reported identical before/after results for 14 tests.
* Independent review evidence.

Do not repeat the refactor merely to create another demonstration.

Instead, verify its actual evidence and classify its claims precisely.

Required distinctions

Demonstrated: The existing tests and fixtures produced equivalent results before and after the refactor.

Not necessarily demonstrated: Complete semantic equivalence for every possible input.

Demonstrated: The refactor preserved the documented programmatic interface under the existing test coverage.

Qualification: The direct CLI invocation changed from a single Python file to package execution. The original contract did not explicitly protect the CLI invocation format.

Record the implications for future contract design.

Independent evidence

Review the original and refactored code rather than relying solely on evidence/stage-1.4-refactor.md.

Confirm test preservation through Git history and existing checksums.

Preserve the recorded findings, limitations and original evidence.

Do not make unsupported claims that the refactored implementation is universally bug-free.

10. Amendment G — Document the schema's demonstrated value and limitations

Update the Phase 1 evaluation with a focused assessment of documentation quality.

Use paired examples of the actual YAML schema and corresponding document.

Include at least three examples:

Example 1 — Validator documentation

Compare the schema's requirements for Purpose, Architecture, Usage and Limitations against the actual document.

Evaluate:

* Practical usefulness.
* Accuracy against source.
* Completeness.
* Previously missed limitations.
* What independent review contributed beyond mechanical validation.

Example 2 — Knowledge placement

Compare the schema's knowledge-category and enforcement requirements with the actual policy.

Evaluate:

* Whether authoritative locations are clear.
* Whether enforcement classifications are accurate.
* Whether the document distinguishes implemented controls from proposed controls.
* Whether current-state drift remains.

Example 3 — Development lifecycle

Compare the requirement for entry and exit criteria against the actual six-stage lifecycle documentation.

Evaluate:

* Operational completeness.
* Clarity.
* Traceability.
* Whether examples are sufficient to guide a fresh development agent.

Evaluation rule

Distinguish carefully between:

1. Qualities directly enforced by the schema.
2. Qualities encouraged by the schema but not mechanically verified.
3. Qualities introduced by general planning instructions.
4. Qualities identified or corrected through independent review.

Do not automatically attribute documentation quality to the schema simply because the final document is good.

Do not claim causal effectiveness without a controlled comparison.

Record the following as an open research hypothesis for later evaluation:

Does a lightweight documentation schema with explicit acceptance criteria produce more accurate, complete and maintainable documentation than an ordinary documentation prompt, and does independent semantic review provide an additional measurable benefit?

A later experiment may compare ordinary prompting, schema-guided documentation, and schema-guided documentation with independent verification.

This comparative experiment is not a Phase 1 completion requirement.

11. Implementation workflow

Execute the amendment through the accepted Axiom lifecycle.

Step 1 — Inspect

Check the repository state, relevant commits, existing contracts and historical evidence.

Confirm which previously reported findings remain unresolved.

Step 2 — Plan

Preserve this amendment prompt under planning/prompts/, with provenance.

Amend the existing Phase 1 plan.

Record the Codex review decision in an ADR.

Write a focused corrective implementation plan with dependencies, non-goals, files to change, acceptance criteria and verification methods.

Avoid creating a competing Phase 1 roadmap.

Step 3 — Assess impact

Identify affected:

* Governance documents.
* ADRs.
* Contracts.
* Implementation files.
* Tests.
* CI workflows.
* Documentation.
* Evidence.
* Roadmap and session context.

Step 4 — Implement

Make bounded changes, preserving unrelated work.

Do not introduce custom orchestration, a graph database, a documentation compiler or an API-backed Codex service.

Step 5 — Verify

Run deterministic tests and documentation checks.

Use independent fresh-context review for substantive changes.

Require the reviewer to inspect the actual implementation and documentation.

Record findings, fixes and accepted limitations.

Step 6 — Reconcile

Update documentation, evidence, roadmap and session context so they match the implementation actually delivered.

Do not mark any unperformed activity as successful.

Step 7 — GitHub review

Commit and push the corrected implementation to an appropriate feature branch.

Open or update the existing Phase 1 PR.

Request native Codex GitHub review using the connected integration.

Where the orchestrator cannot initiate the native review, provide the exact PR URL and the necessary @codex review instruction for the human to submit.

Do not fabricate a Codex review or substitute a Claude review while describing it as Codex.

If native Codex review is not yet completed, leave its acceptance criterion open.

Do not merge without explicit human approval.

12. Revised Phase 1 Definition of Done

The revised Phase 1 closeout must demonstrate:

* [ ] Governance, roadmap, ADRs and preserved planning prompts are coherent.
* [ ] Previously identified documentation drift has been corrected.
* [ ] Documentation schemas are valid and meaningful for governed documents.
* [ ] Deterministic schema validation and tests operate in GitHub Actions.
* [ ] Semantic documentation acceptance criteria have been evaluated against real source evidence.
* [ ] Knowledge placement has been evaluated on actual project changes.
* [ ] The existing validator refactoring evidence has been independently confirmed.
* [ ] Refactoring limitations and unprotected interfaces are recorded.
* [ ] Independent documentation reconstruction has been demonstrated, with isolation limitations explicit.
* [ ] Native Codex GitHub review has actually been performed on the relevant Phase 1 PR.
* [ ] Significant Codex findings have been resolved or explicitly dispositioned by the human decision-maker.
* [ ] The reviewed commit and review evidence are recorded.
* [ ] The automatic API-backed Codex CI gate is explicitly deferred in the accepted architectural decisions.
* [ ] Process overhead and unresolved research hypotheses are documented.
* [ ] An independent closeout review supports Phase 1 acceptance.
* [ ] Human approval has been obtained before marking Phase 1 complete or merging.

A native Codex review satisfies the amended Phase 1 independent-Codex-review requirement. It does not satisfy the original automatic merge-gate requirement, which must remain recorded as superseded and deferred.

13. Final reporting

At completion, report:

1. Changes made to the Phase 1 plan and ADRs.
2. Documentation drift identified and corrected.
3. Schema-validation improvements.
4. Examples of schema versus actual document quality.
5. Results of semantic documentation review.
6. Confirmation of the existing refactor and its limitations.
7. Test counts and CI results.
8. Native Codex review status, PR URL and findings.
9. Remaining limitations and deferred capabilities.
10. Phase 1 acceptance recommendation.

Distinguish completed, partially completed, deferred and blocked work.

Do not claim automated Codex merge enforcement is operational.

Do not declare Phase 1 complete if mandatory review or acceptance evidence is missing.

14. Final instruction

Amend the existing Phase 1 plan first, then implement the corrective changes.

The objective is to finish the current work with stronger documentation quality and simpler independent review, not to expand Axiom's architecture.

Use:

* Deterministic Python tests for mechanical correctness.
* Source-grounded semantic review for documentation accuracy.
* Native Codex GitHub review for independent AI assessment.
* Human approval for acceptance and merging.

Defer API-backed Codex review infrastructure and automated AI CI gating.

Preserve the original Stage 1.4 and 1.5 achievements and their historical evidence.

The intended outcome is Axiom Dev Phase 1 ready for acceptance: a lightweight, self-tested development methodology with accurate, evidence-backed documentation, meaningful refactoring assurance, and a completed native Codex review.

Proceed.
