---
id: 007
title: Final Corrective Remediation and Closeout Preparation
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002, 003, 004, 005, 006]
---

> **Provenance note.** The text below is the complete, verbatim prompt
> that authorised correcting the fourth native-Codex-review finding
> (manifest-integrity check not run when a document's own schema
> exists) on PR #1, disposition of all four findings, and preparation
> (not completion) of Phase 1's final acceptance. Preserved unmodified
> as historical source material, per `AGENTS.md` §2/§3 and this
> project's established convention (prompts 001–006) of keeping
> prompts with provenance, never reconstructed from memory.
> Harness-level wrapper content (system reminders, tool-call metadata,
> environment blocks) is excluded as it is not part of the assignment;
> the assignment text is otherwise reproduced exactly as written,
> including its own internal section numbering.
>
> Relationship to prior work: this is **amendment 007** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued
> by `002`–`006`. It does not replace any of them; all seven are
> preserved. See `planning/phase-01-foundation.md` §27+ for this
> amendment's own plan detail.

AXIOM DEV — FINAL CORRECTIVE REMEDIATION AND CLOSEOUT

1. Assignment

You are the Claude Code orchestrator responsible for preparing Axiom Dev Phase 1 for final acceptance.

Repository: ctosullivan/axiom-dev
Local directory: ~/projects/axiom-dev
Development branch: phase-1/stage-1.0-bootstrap
Pull request: https://github.com/ctosullivan/axiom-dev/pull/1

Last confirmed PR head:

6e75d2bac7bfba7f6db7832a39b169a81e78aae2

Verify the live repository and PR state before beginning.

Objectives

1. Correct the outstanding manifest-integrity defect identified by the third native Codex review.
2. Demonstrate the defect and verify its correction with regression tests.
3. Independently verify the change against the existing behavioural contract.
4. Confirm that the previous three Codex corrections remain effective.
5. Reconcile Phase 1 documentation and evidence with actual repository and GitHub state.
6. Prepare responses and dispositions for all four Codex review findings.
7. Update PR #1 and obtain a final native Codex review of its corrected head commit.
8. Produce an evidence-backed final acceptance recommendation.

This assignment prepares Phase 1 for closeout. It does not authorise merging, marking Phase 1 Completed, archiving the phase or beginning Phase 2.

Stop at READY FOR HUMAN ACCEPTANCE unless the user subsequently provides explicit approval for those actions.

⸻

2. Governing methodology

Follow the existing Axiom lifecycle:

UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

Read and comply with:

* AGENTS.md, especially §§5–6 and §§10–13.
* CLAUDE.md.
* CONTRIBUTING.md.
* planning/ROADMAP.md.
* planning/CONTEXT.md.
* planning/phase-01-foundation.md.
* The existing Phase 1 corrective prompts in planning/prompts/.
* evidence/phase-1-final-closeout.md.
* contracts/documentation-schema-validator.md.
* docs/axiom-validator.md.
* docs/documentation-schema.md.
* docs/phase-archiving.md.
* Relevant accepted ADRs, particularly decisions/0005–0007.

Use existing contracts and evidence rather than inventing new acceptance criteria.

Preserve historical records and supersession relationships.

Native Codex GitHub PR review remains advisory under ADR 0005. The API-backed automated review gate remains deferred.

Do not request an OPENAI_API_KEY or activate deferred CI workflows.

Scope discipline

This is a corrective closeout task, not another development phase.

Use the smallest conventional change that satisfies the accepted contract.

Do not introduce new architecture, dependencies, agent infrastructure, documentation conventions or CI systems.

Do not create another ADR unless the correction genuinely changes an accepted architectural decision. Fixing implementation to match an existing contract does not, by itself, require an ADR.

⸻

PART A — CURRENT CODEX FINDING

3. Confirm the review baseline

PR #1 has undergone three native Codex reviews.

Review 1

Commit: 3a8c395c86

Findings:

A. Fenced-code-block heading false positive

src/axiom_validator/parsing.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629983

Corrected in commit 162e5c6.

B. Malformed severity handling

.github/scripts/policy_evaluator.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629985

Corrected in commit 162e5c6.

Review 2

Commit: 2ebac4c19b

Finding:

C. Heading whitespace crosses newline

src/axiom_validator/parsing.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651808543

Corrected in commit 0645af3.

Review 3

Commit: 6e75d2bac7

Finding:

D. Governed-document manifest integrity is not checked when a companion schema exists

src/axiom_validator/__init__.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651913914

This finding remains outstanding at the last confirmed inspection.

All four review threads were then unresolved.

These are historical reference points. Obtain the current GitHub state before making changes.

Do not reimplement A–C unless fresh evidence identifies a remaining defect.

⸻

4. Reproduce finding D

Current implementation:

src/axiom_validator/__init__.py

Function:

validate_file(...)

The function currently loads the default governed-document manifest only inside the branch executed when the document's companion schema does not exist.

Consequently, this situation can return PASS:

* A Markdown document exists.
* Its mirrored schema exists and is valid.
* schemas/governed-documents.txt does not exist.
* governed_manifest was not explicitly supplied.

This violates:

contracts/documentation-schema-validator.md

Contract revision 2, rule 4 — Missing manifest fails closed.

That rule requires every document checked through the default manifest-loading path to report FAIL if the manifest file itself is missing.

Required reproduction

Create an isolated temporary test repository with:

temporary-repository/
├── foo.md
└── schemas/
    └── foo.md.schema.yaml

The schema must be genuinely valid, with all required fields and a heading matching the Markdown document.

Deliberately omit:

schemas/governed-documents.txt

Call:

validate_file(
    Path("temporary-repository/foo.md"),
    Path("temporary-repository")
)

Demonstrate that the existing implementation incorrectly returns PASS.

Record the actual result before modifying the code.

Use a regression test that fails against the original implementation and passes after the correction.

Do not merely assume Codex's reproduction is correct.

⸻

5. Correct the defect

Modify validate_file so the required default manifest integrity check occurs before branching on whether a companion schema exists.

Required behaviour

When governed_manifest is None:

* Load and validate the existence of schemas/governed-documents.txt.
* If the manifest is absent, return a structured FAIL result.
* Do not return PASS or SKIPPED simply because the document's schema exists or does not exist.

When an explicit governed_manifest argument is supplied:

* Preserve the existing documented override behaviour.
* Do not require the on-disk production manifest solely for that overridden operation.

Keep the existing response format:

{
    "file": "...",
    "result": "FAIL",
    "errors": ["..."]
}

Do not introduce an unhandled exception or change unrelated public interfaces.

Maintain safe repository-root resolution and mirrored schema discovery.

Preserve the existing PASS, FAIL, SKIPPED and INVALID_SCHEMA behaviours for other cases.

The correction should be a small, understandable change to the existing code.

⸻

6. Required regression tests

Extend the existing schema-relocation or manifest-integrity test suite rather than adding a new framework.

Cover:

Case	Expected
Valid document and valid schema, manifest absent	FAIL
Document without schema, manifest absent	FAIL
Valid document and schema, manifest present	PASS
Governed document without required schema	FAIL
Non-governed document without schema, manifest present	SKIPPED
Explicit manifest override, on-disk manifest absent	Preserve existing documented override behaviour
Malformed document schema, valid manifest present	INVALID_SCHEMA
CLI encounters missing manifest	Nonzero exit and structured, actionable failure report

Verify both the overall result and relevant error content.

Do not count any arbitrary failure as proof of the correct rule being enforced.

Preserve other error-handling behaviour unless changing it is necessary to satisfy an accepted contract.

⸻

PART B — VERIFY THE CORRECTION

7. Deterministic verification

Before implementation, record the current baseline.

The previous confirmed GitHub Actions results on commit 6e75d2b were:

* Validator tests: 62 passed.
* Policy evaluator tests: 33 passed.
* Governed-document validation: 11 passed.
* Trailing-whitespace check: passed.

GitHub Actions run:

https://github.com/ctosullivan/axiom-dev/actions/runs/44891748857

These numbers are baseline evidence, not results for the new correction.

After implementation, run:

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=.github/scripts python3 -m unittest discover \
  -s .github/scripts/tests -v

Run the existing governed-document validation procedure against all entries in:

schemas/governed-documents.txt

Confirm:

1. The new regression test passes.
2. The original missing-manifest test continues passing.
3. The previous fenced-code correction remains effective.
4. The previous heading-whitespace correction remains effective.
5. The malformed-severity correction remains effective.
6. Existing schema-discovery and path-safety tests pass.
7. All governed documents validate.
8. Orphaned schemas are not present.
9. No unrelated behaviour changes are introduced.

Record actual test counts.

⸻

8. Independent review

Dispatch a fresh reviewer who has not implemented the correction.

Use the strongest existing practical separation; identify its actual isolation level.

The reviewer must:

* Read the accepted validator contract.
* Independently reproduce finding D against the pre-fix implementation.
* Inspect the corrected code.
* Inspect and execute the regression tests.
* Construct an additional adversarial test involving manifest absence or an override.
* Confirm that the implementation matches contract revision 2, rule 4.
* Confirm A–C remain corrected.
* Review documentation changes.
* Verify actual test results.
* Identify any material remaining correctness or contract violations.

Do not rely solely on the implementing agent's own account.

Report:

* Confirmed defects.
* Material but nonblocking findings.
* Advisory observations.
* Accepted limitations.

Resolve genuine defects within scope.

Avoid expanding this assignment for unrelated improvements.

⸻

PART C — FINAL DOCUMENTATION RECONCILIATION

9. Current-state documentation

Review and update only documents whose current-state claims require correction.

At minimum, inspect:

* README.md.
* planning/ROADMAP.md.
* planning/CONTEXT.md.
* evidence/phase-1-final-closeout.md.
* planning/phase-01-foundation.md.
* schemas/governed-documents.txt.
* Relevant validator documentation.

Required corrections

Record accurately that:

* PR #1 exists and remains open until merged.
* Three native Codex reviews have occurred.
* Four material P2 findings have been identified across those reviews.
* A–C were previously corrected.
* D has now been corrected, if verification establishes that.
* The latest GitHub Actions result must be checked against the current head commit.
* Final native Codex review and human acceptance are outstanding until actually completed.

Preserve the old closeout assessment as historical evidence.

Add a concise, dated addendum rather than rewriting its original observations.

Do not claim that earlier assessments anticipated later findings.

Keep planning/ROADMAP.md concise. Historical technical details belong in the Phase 1 plan and evidence records.

Keep planning/CONTEXT.md focused on the current state and next action.

Documentation validation

Validate affected Markdown and schemas.

Ensure production schemas remain under the mirrored top-level schemas/ directory.

Do not reintroduce front matter or colocated schema files.

Do not create new documentation files unnecessarily.

⸻

PART D — PREPARE PR #1 FOR ACCEPTANCE

10. Commit and push

Commit the targeted correction and documentation reconciliation to the existing development branch.

Use an appropriate commit message, such as:

fix(phase-1): enforce manifest integrity for schema-bearing documents

Push to:

phase-1/stage-1.0-bootstrap

Do not merge into main.

Record the actual commit SHA.

Wait for the GitHub Actions result to be available through the normal development workflow, and verify that all four deterministic jobs pass on the pushed commit.

If GitHub Actions cannot be inspected, report that as an evidence limitation.

Do not infer success from local tests alone.

⸻

11. Update the PR description

PR #1 currently lacks a substantive description.

Update it to include:

* Phase 1 objective.
* Implemented methodology.
* Authorising plans and ADRs.
* Four Codex findings and correction commits.
* Regression-test evidence.
* Independent verification evidence.
* Current GitHub Actions results.
* Outstanding limitations.
* Final acceptance requirements.

Link to the existing Phase 1 plan and final closeout assessment.

Keep the description concise.

If GitHub write access is unavailable, provide the complete ready-to-paste PR description in the final report.

⸻

12. Disposition all Codex findings

All four findings require a recorded disposition.

For each:

1. Identify the original finding.
2. Reference the relevant correction commit.
3. Identify the relevant regression tests.
4. Reference independent verification.
5. Reply to the existing GitHub review thread.
6. Mark the thread resolved after verifying the correction.

The original three findings should not be reimplemented or reopened without evidence.

For finding D, record the new correction and regression tests.

If the orchestrator cannot post GitHub replies or resolve threads, provide ready-to-paste responses and direct GitHub links.

Do not claim GitHub threads are resolved unless their actual state confirms it.

⸻

13. Final native Codex review

After the corrected commit is pushed and the relevant deterministic checks pass, request:

@codex review

on:

https://github.com/ctosullivan/axiom-dev/pull/1

The review must cover the current PR head, not an obsolete commit.

If the final review reports no material findings

Record:

* Reviewed commit SHA.
* Review date.
* Actual outcome.
* Review-thread disposition.
* Remaining human-approval requirements.

Proceed to the final acceptance assessment.

If the final review reports another finding

Evaluate it independently.

Do not automatically accept or reject Codex's judgement.

For a real material correctness or contract violation:

* Reproduce it.
* Correct it.
* Add a targeted regression test.
* Reverify.
* Reconcile the evidence.

For an advisory observation or accepted limitation:

* Document the reasoned disposition.
* Seek human acceptance where appropriate.
* Do not expand Phase 1 merely to eliminate every conceivable enhancement.

Avoid an indefinite review loop.

The completion criterion is proportionate, evidence-backed acceptance of the existing Phase 1 scope, not perfect support for every possible edge case.

If a correction changes the PR head materially, obtain an appropriately current review before recommending merge.

⸻

PART E — FINAL ACCEPTANCE ASSESSMENT

14. Produce the final closeout recommendation

Prepare an independent assessment against the accepted Phase 1 Definition of Done.

Evaluate:

Area	Required evidence
Governance	Accepted methodology and approval boundaries
Knowledge management	Placement, preservation and reconciliation
Behavioural contracts	Accepted contracts with implementation traceability
Documentation schemas	Correct location, discovery and validation
Deterministic testing	Actual passing results
Independent verification	Review evidence and stated isolation limitations
Self-development	Evidence from the validator
Behaviour-preserving refactoring	Original tested-scope evidence
Documentation reconstruction	Stage 1.5 evidence
Native Codex review	Actual PR reviews and current reviewed SHA
Codex finding remediation	All four findings dispositioned
CI	Actual successful GitHub Actions run
Documentation reconciliation	Current status agrees with observed state
Human approval	Explicit approval, not inferred

Classify every requirement as:

* MET
* PARTIAL
* NOT MET

Provide the actual supporting file, commit, test or GitHub record.

Do not mark criteria MET based solely on the implementing agent's assertions.

Preserve accepted limitations and accurately state what Phase 1 has not demonstrated.

For example, Phase 1 has demonstrated that independent review can detect defects missed by existing tests. It has not yet demonstrated that Axiom is superior to simpler development approaches. That is a Phase 2 experimental question.

⸻

15. Closeout boundary

The final recommendation should conclude with one of:

READY FOR HUMAN ACCEPTANCE

or

NOT READY — MATERIAL REQUIREMENTS OUTSTANDING

Use READY FOR HUMAN ACCEPTANCE only when:

* Finding D is corrected and independently verified.
* Previous corrections remain effective.
* Deterministic CI passes on the latest code.
* Current documentation has been reconciled.
* All four findings have a documented disposition.
* The final Codex review has been completed or an explicitly authorised alternative disposition is recorded.
* No unresolved material defect prevents acceptance.

Do not mark Phase 1 Completed.

Do not merge PR #1.

Do not create the Phase 1 archive yet.

These actions require explicit human approval.

⸻

16. Post-approval procedure

After the repository owner separately approves Phase 1 completion:

Step 1 — Merge the implementation PR

Merge PR #1.

Record its actual merge SHA and date.

Step 2 — Formal closeout PR

Create a small follow-up PR that:

* Updates planning/ROADMAP.md to mark Phase 1 Completed.
* Updates planning/CONTEXT.md.
* Creates planning/archive/phase-01/README.md.
* Updates planning/archive/README.md.
* Updates the relevant schemas.
* Records final acceptance and merge evidence.

Follow docs/phase-archiving.md.

Preserve the canonical original Phase 1 plan and historical evidence.

Independently verify the closeout PR and obtain the required human approval before merging it.

Phase 2 remains Proposed until separately planned and authorised.

⸻

17. Final deliverables

Provide a concise final report containing:

A. Correction

Original defect, reproduced failure, code change and passing regression tests.

B. Verification

Actual test counts, independent review findings and GitHub Actions results.

C. Codex

A four-finding disposition table, reviewed SHAs and final review status.

D. Documentation

Files reconciled and remaining limitations.

E. Acceptance

Complete Phase 1 acceptance matrix with evidence references.

F. GitHub

Actual branch, latest commit, PR state, CI state and review-thread status.

G. Human action

Exact steps required to approve, merge and archive Phase 1.

Include ready-to-paste GitHub text wherever access restrictions prevent the orchestrator from carrying out an action.

⸻

18. Final instruction

This is the final planned corrective iteration of Axiom Dev Phase 1.

Execute the smallest sufficient implementation change, independently verify it, reconcile existing evidence and prepare the existing PR for acceptance.

Do not create another extensive corrective amendment merely to document this one.

Avoid unnecessary ADRs, additional methodology, new architecture, unrelated refactoring and speculative improvements.

Finish all work possible in the current environment.

Where human approval or external GitHub interaction is required, preserve the boundary and report the exact action needed.

The goal is to establish that Phase 1 is sufficiently correct, independently verified and documented to justify acceptance—not to make Phase 1 indefinitely self-extending.
