---
id: 006
title: Final Phase 1 Correction and Closeout
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002, 003, 004, 005]
---

> **Provenance note.** The text below is the complete, verbatim prompt
> that authorised correcting the third native-Codex-review finding on
> PR #1, reconciling remaining documentation/evidence staleness, and
> preparing (not completing unilaterally) Phase 1's final closeout and
> merge/archive sequence. Preserved unmodified as historical source
> material, per `AGENTS.md` §2/§3 and this project's established
> convention (prompts 001–005) of keeping prompts with provenance,
> never reconstructed from memory. Harness-level wrapper content
> (system reminders, tool-call metadata, environment blocks) is
> excluded as it is not part of the assignment; the assignment text is
> otherwise reproduced exactly as written, including its own internal
> section numbering.
>
> Relationship to prior work: this is **amendment 006** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued
> by `002`–`005`. It does not replace any of them; all six are
> preserved. See `planning/phase-01-foundation.md` §25+ for this
> amendment's own plan detail.

AXIOM DEV — FINAL PHASE 1 CORRECTION AND CLOSEOUT

1. Assignment

You are the Claude Code orchestrator responsible for completing the final corrective work and closeout of Axiom Dev Phase 1.

Repository: ctosullivan/axiom-dev
Expected local directory: ~/projects/axiom-dev
Development branch: phase-1/stage-1.0-bootstrap
Existing PR: https://github.com/ctosullivan/axiom-dev/pull/1

Last confirmed PR head: 2ebac4c19beea270f696e349853c7b40c3756f0d

Verify the current repository state before proceeding. Do not assume the above commit remains HEAD.

Your objectives are to:

1. Correct the remaining P2 defect identified by the second native Codex review.
2. Independently demonstrate that the defect is corrected and no relevant behaviour has regressed.
3. Formally disposition the original Codex findings.
4. Correct outstanding documentation and evidence inconsistencies.
5. Run the complete deterministic verification process.
6. Prepare PR #1 for final native Codex review and human approval.
7. Complete the formal Phase 1 closeout and archiving procedure only after explicit human approval and the required merge.

Do not introduce additional features, architectural changes or new phases.

The objective is to close Phase 1 with sufficient evidence, not to continue improving it indefinitely.

⸻

2. Governing methodology

Follow Axiom's established lifecycle:

UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

Before making changes, read:

* AGENTS.md, especially §§5–6 and §§10–13.
* CLAUDE.md.
* planning/ROADMAP.md.
* planning/CONTEXT.md.
* planning/phase-01-foundation.md.
* planning/prompts/005-phase-1-final-remediation-and-closeout.md.
* evidence/phase-1-final-closeout.md.
* docs/phase-archiving.md.
* contracts/documentation-schema-validator.md.
* contracts/codex-gate-policy-evaluator.md.
* decisions/0005 through 0007.

Preserve existing accepted decisions.

ADR 0005 establishes native Codex GitHub review as the Phase 1 independent-review mechanism. API-backed Codex CI gating remains deferred.

Do not require an OpenAI API key, activate the deferred workflow or introduce a new automated merge gate.

Preserve explicit human approval requirements for governance changes, PR merging and phase completion.

⸻

3. Current review baseline

PR #1 has undergone two native Codex reviews.

First review

Reviewed commit: 3a8c395c86

Two P2 findings:

Finding A — Fenced-code heading detection

src/axiom_validator/parsing.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629983

The previous validator could count headings inside tilde-fenced or longer-backtick-fenced examples as actual document headings.

Finding B — Malformed severity handling

.github/scripts/policy_evaluator.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629985

Malformed severity values could produce an unhandled TypeError rather than a structured FAIL_CLOSED result.

Both defects were subsequently corrected, with regression tests and independent verification.

Their GitHub review threads are still unresolved.

Do not reimplement these corrections unless new evidence establishes they remain defective.

Second review

Reviewed commit: 2ebac4c19b

One new P2 finding:

Finding C — Restrict heading whitespace to the same line

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651808543

This finding remains outstanding.

At the last inspection, all three review threads were unresolved.

Retrieve the live PR comments before acting.

⸻

PART A — CORRECT THE FINAL CODEX DEFECT

4. Heading parser false-positive

File:

src/axiom_validator/parsing.py

Current implementation:

HEADING_RE = re.compile(
    r"^#{1,6}\s+(.+?)\s*$",
    re.MULTILINE
)

The expression incorrectly uses \s+ to separate the Markdown heading marker from its text.

Python's \s matches newline characters.

Consequently, this document:

#
Required

can incorrectly produce:

{"Required"}

A documentation schema requiring a Required heading could therefore pass even though no such heading exists.

This violates the validator's requirement to check actual Markdown headings.

Required correction

Replace the problematic whitespace handling with a same-line-only rule.

A suitable minimal correction is to use horizontal whitespace ([ \t]) instead of \s where newline consumption is invalid.

Review the complete heading expression, including trailing whitespace handling, rather than blindly replacing a single token.

Preserve existing valid-heading behaviour.

Avoid unrelated Markdown parser improvements.

Required regression coverage

Add tests covering:

1. # followed by a newline and ordinary text.
2. #  followed by a newline and ordinary text.
3. ## followed by a newline and ordinary text.
4. A valid heading using a space.
5. A valid heading using a tab.
6. Multiple valid headings.
7. Headings inside fenced code blocks remaining excluded.
8. Required-section validation failing when the only matching text is on the next line.
9. Ordinary documentation continuing to validate correctly.

Test relevant LF and CRLF line-ending behaviour where practical.

Before-and-after evidence

Before changing the parser:

* Demonstrate the original false positive against the current implementation.
* Record the actual output.
* Add a failing regression test.

After changing the parser:

* Run the new test.
* Run the existing heading and fenced-code tests.
* Confirm the false positive has been eliminated.
* Confirm valid headings remain recognised.

Preserve this evidence in the existing Phase 1 verification records or a concise corrective addendum.

⸻

PART B — RECONCILE DOCUMENTATION

5. Correct current-state documentation

An earlier independent review identified several documents containing statements that are no longer accurate.

Inspect and correct them.

README.md

The README still contains historical claims that:

* No PR has been opened.
* Native Codex review has not occurred.
* The schema convention is at an earlier stage.

Update the current-status description to reflect the actual repository state.

Reference:

* PR #1.
* Native Codex review.
* The existing schemas/ architecture.
* Outstanding acceptance requirements.
* The current roadmap.

Preserve the README's concise, human-facing presentation.

Do not turn it into a historical implementation log.

schemas/governed-documents.txt

The manifest's explanatory comments still describe YAML front matter and the previous documentation-manifest location.

Correct the comments to describe:

* Production schemas under schemas/.
* Deterministic mirrored schema paths.
* The current governed-document requirement.
* The actual validator behaviour when a schema is absent.
* The current manifest location.

Preserve the actual governed-document entries unless an independently justified change is necessary.

planning/ROADMAP.md

Update Phase 1's current status.

Record:

* PR #1 exists.
* The first Codex review identified two P2 defects.
* Both original defects were corrected.
* The second review identified the heading-whitespace defect.
* The latest correction and review status.
* The remaining requirements for acceptance.

Keep Phase 1 marked In progress until human approval has been obtained.

Do not expand the roadmap or create new phases.

planning/CONTEXT.md

Update session continuity to reflect the actual latest development state.

Remove outdated instructions to request a second Codex review if it has already occurred.

Identify the actual next action.

Avoid freezing a stale HEAD SHA as though it will remain current indefinitely.

evidence/phase-1-final-closeout.md

Update the existing closeout assessment through a clearly identified dated addendum, or create a short successor record if that better preserves historical traceability.

Preserve the earlier assessment's original findings.

Incorporate:

* The actual second Codex review.
* The new P2 finding.
* Its correction and verification evidence.
* Confirmed GitHub Actions results.
* Outstanding thread dispositions.
* The status of the final review.
* Human acceptance status.

Do not rewrite historical observations to imply work happened earlier than it did.

⸻

6. Verify documentation structure

The previous amendment introduced:

docs/
    *.md
schemas/
    docs/
        *.md.schema.yaml
    contracts/
    evidence/
    planning/
    governed-documents.txt

Preserve this architecture.

Confirm:

* docs/ contains human-readable Markdown only.
* Production schemas remain under schemas/.
* Schema lookup follows the existing mirrored convention.
* The governed-document manifest remains functional.
* No obsolete colocated schema files have been reintroduced.
* Documentation links and authoritative-source references resolve.

Do not redesign the schema system.

⸻

PART C — COMPLETE VERIFICATION

7. Deterministic testing

The last confirmed GitHub Actions run passed:

* Validator tests: 50/50.
* Policy evaluator tests: 33/33.
* Governed-document validation.
* Markdown whitespace validation.

These are historical baseline results, not results for the forthcoming correction.

After implementation, run:

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=.github/scripts python3 -m unittest discover \
  -s .github/scripts/tests -v

Validate all documents listed in:

schemas/governed-documents.txt

Use the existing validator CLI and CI commands.

Confirm:

* No test failures.
* No missing governed schemas.
* No invalid schema contents.
* No orphaned production schemas.
* No broken repository-relative links.
* No unintended behaviour changes.

Capture actual test counts and results.

Do not reuse the previously recorded 50/50 and 33/33 counts unless they remain accurate after the new tests are added.

⸻

8. Independent verification

Dispatch a fresh reviewer that did not implement the correction.

Use the strongest practical isolation available within the existing orchestration environment.

Document the isolation level honestly.

The independent reviewer must:

1. Inspect the accepted behavioural contract.
2. Reproduce the original heading-whitespace defect.
3. Verify the corrected implementation.
4. Inspect the new regression tests.
5. Construct at least one additional adversarial test.
6. Confirm the original two Codex corrections remain effective.
7. Review the documentation reconciliation.
8. Verify the reported test results independently.
9. Assess whether any material outstanding defect prevents Phase 1 acceptance.

The reviewer must not merely summarise the implementing agent's assertions.

Classify findings as:

* Blocking correctness or contract violations.
* Material but nonblocking issues.
* Advisory improvements.
* Explicitly deferred work.

Resolve genuine defects within the accepted scope.

Do not continually expand Phase 1 for unrelated improvements.

⸻

PART D — FINISH THE CODEX REVIEW PROCESS

9. Update PR #1

Commit and push the corrective changes to the existing development branch.

Do not create a replacement PR.

Update the PR description to include:

* Purpose of Phase 1.
* Scope implemented.
* Relevant plans and ADRs.
* Summary of the three Codex findings.
* Corrections and regression evidence.
* Deterministic verification results.
* Independent verification evidence.
* Outstanding limitations.
* Human acceptance requirements.

Record the new commit SHA.

Confirm GitHub Actions passes on that exact commit.

⸻

10. Resolve existing review findings

There are three recorded Codex findings.

Finding A — Fenced-code handling

Already corrected.

Verify the correction still works.

Reply to the original review thread explaining:

* What was changed.
* Relevant regression tests.
* Independent verification evidence.
* Correction commit.

Resolve the thread after verifying the evidence.

Finding B — Severity validation

Already corrected.

Verify malformed severity values still produce structured FAIL_CLOSED results.

Reply with the relevant correction and test evidence.

Resolve the thread after verification.

Finding C — Heading whitespace

Correct under Part A of this assignment.

Reply with:

* Original reproduced behaviour.
* Corrected behaviour.
* Regression tests.
* Verification results.
* Correction commit.

Resolve after verification.

If GitHub write access is unavailable, produce concise suggested replies and direct links for the repository owner.

Never claim a thread has been resolved unless its actual GitHub state confirms that.

⸻

11. Request final Codex review

After the correction is pushed and deterministic CI passes, request native Codex review on the current PR head:

@codex review

Use the existing GitHub integration if available.

If the orchestrator lacks GitHub comment permissions, provide the repository owner with the PR URL and exact comment to post.

Do not use a Claude review as a substitute for native Codex review.

Verify that the resulting Codex review references the current head commit.

If Codex identifies another defect

Assess the finding independently.

A genuine correctness or contract violation must be corrected or receive an explicit evidence-based disposition consistent with AGENTS.md.

Record:

* Finding.
* Severity.
* Reproduction.
* Correction or justified disposition.
* Verification evidence.

Repeat review only where required to verify a material correction.

If no material findings remain

Record the final reviewed commit and result.

Do not claim that Codex formally approved the PR merely because it completed a review without findings.

Native Codex review remains advisory under ADR 0005.

⸻

PART E — FINAL PHASE 1 ACCEPTANCE

12. Final acceptance assessment

Produce a fresh independent Phase 1 completion assessment.

Review all active acceptance requirements established by:

* Original Phase 1 plan.
* Accepted amendments.
* Relevant behavioural contracts.
* ADR 0005's revised Codex review requirement.
* ADRs 0006 and 0007.
* The final remediation prompt.
* Existing verification evidence.

Do not reintroduce the deferred API-backed Codex CI gate as an acceptance requirement.

Required assessment

Evaluate:

Criterion	Status	Evidence	Outstanding action
Repository governance	MET / PARTIAL / NOT MET	Reference	Action
Knowledge placement	…	…	…
Development lifecycle	…	…	…
Behavioural contracts	…	…	…
Documentation schemas	…	…	…
Self-development	…	…	…
Behaviour-preserving refactoring	…	…	…
Documentation reconstruction	…	…	…
Deterministic CI	…	…	…
Independent verification	…	…	…
Codex review	…	…	…
Findings disposition	…	…	…
Documentation reconciliation	…	…	…
Evidence and measurement	…	…	…
Human acceptance	…	…	…

For every MET criterion, provide verifiable evidence.

For every unmet criterion, specify the real remaining action.

Separate:

* Implemented.
* Tested locally.
* Independently verified.
* Executed successfully in CI.
* Reviewed by native Codex.
* Approved by a human.

Do not conflate these states.

⸻

13. Human approval boundary

After completing the correction, verification, reconciliation and final Codex review, present the acceptance assessment to the repository owner.

Request explicit approval to:

1. Accept the Phase 1 technical completion evidence.
2. Merge PR #1.
3. Formally mark Phase 1 Completed.
4. Archive Phase 1.

Do not treat this prompt as advance approval for those actions.

If approval is unavailable, stop at:

READY FOR HUMAN ACCEPTANCE

Provide the final evidence and exact remaining actions.

Do not claim the PR has been merged or the phase closed.

⸻

PART F — MERGE AND ARCHIVE

14. Merge sequence

Following explicit human approval and successful review:

Step A — Merge PR #1

Merge the reviewed implementation into main.

Use the repository's accepted merge procedure.

Record:

* PR URL.
* Final reviewed commit SHA.
* Actual merge commit SHA.
* Merge date.
* Final CI results.

Do not invent these values.

Step B — Formal Phase 1 closeout

Create a small follow-up branch and PR containing only the necessary closeout changes.

Follow:

docs/phase-archiving.md

Create:

planning/archive/phase-01/README.md

Update:

* planning/archive/README.md.
* planning/ROADMAP.md.
* planning/CONTEXT.md.
* Relevant schema files.
* Final closeout evidence.

The archive entry should link to:

* Original Phase 1 plan.
* Accepted decisions.
* Behavioural contracts.
* Implementation evidence.
* Independent verification.
* Codex reviews and finding dispositions.
* Final PR and merge commit.
* Retrospective.
* Accepted limitations.
* Deferred work.

Preserve historical plans and records at their canonical locations.

The archive is an index of historical evidence, not a duplication of the evidence itself.

Mark Phase 1 Completed only with the required approval and evidence.

Independently verify the closeout PR and obtain human approval before merging it.

After that merge, update session continuity to identify Phase 2 planning as the next development action.

Do not begin Phase 2 implementation under this assignment.

⸻

15. Scope restrictions

This is a final corrective assignment.

Do not introduce:

* Additional architectural frameworks.
* New agent infrastructure.
* New knowledge databases.
* New documentation schema conventions.
* New CI systems.
* Automated Codex API review.
* Ledgerkit integration.
* Cross-semantic wiki development.
* Axiom Assure integration.
* Phase 2 features.
* Unrelated refactoring.

Preserve existing documented limitations unless they constitute a material violation of an active acceptance criterion.

Treat proposed enhancements as Phase 2-or-later candidates rather than automatic blockers.

Avoid adding unnecessary procedures, documents or retrospective detail.

Apply the principle of minimum sufficient correction.

⸻

16. Definition of Done

Technical correction

* [ ]	The new Codex P2 defect is reproduced.
* [ ]	The heading parser is corrected.
* [ ]	Regression tests demonstrate the correction.
* [ ]	Existing valid-heading behaviour is preserved.
* [ ]	Original Codex findings remain corrected.
* [ ]	Full validator tests pass.
* [ ]	Full policy evaluator tests pass.
* [ ]	Governed-document validation passes.
* [ ]	GitHub Actions passes on the corrected commit.
* [ ]	Independent verification is completed.

Knowledge reconciliation

* [ ]	README status is accurate.
* [ ]	Governed-document manifest comments are accurate.
* [ ]	Roadmap reflects the actual review state.
* [ ]	Session context is current.
* [ ]	Final closeout evidence is updated.
* [ ]	Documentation links and schemas validate.
* [ ]	Historical evidence remains accurate.
* [ ]	PR description contains appropriate references.

Codex review

* [ ]	Original findings are documented and dispositioned.
* [ ]	Review threads are resolved, or any remaining unresolved state is explicitly explained.
* [ ]	Final Codex review examines the corrected commit.
* [ ]	Material findings are resolved or explicitly dispositioned.
* [ ]	Final reviewed SHA and result are recorded.

Formal closeout

* [ ]	Final acceptance matrix completed independently.
* [ ]	Human approval obtained.
* [ ]	PR #1 merged.
* [ ]	Actual merge evidence recorded.
* [ ]	Phase 1 archive created.
* [ ]	Roadmap updated to Completed.
* [ ]	Closeout PR independently reviewed and merged with approval.
* [ ]	Phase 2 identified as the next proposed phase.

Do not mark an item complete without corresponding evidence.

⸻

17. Final reporting requirements

Provide a concise final report containing:

1. Corrective change: what was wrong, what changed and why it is correct.
2. Verification: actual test counts, independent findings and CI results.
3. Codex: original findings, dispositions and final review status.
4. Documentation: reconciled files and remaining limitations.
5. Acceptance: final Phase 1 matrix and recommendation.
6. GitHub: branch, commits, PR and merge status.
7. Human actions: exact approvals or GitHub interactions still required.
8. Archive: status and links, once formally completed.

Finish with one of these factual outcomes:

PHASE 1 — READY FOR HUMAN ACCEPTANCE

or

PHASE 1 — FORMALLY COMPLETED AND ARCHIVED

Use the second outcome only when every required action, including approvals and merges, has actually occurred.

⸻

18. Final instruction

Execute this assignment using Axiom's established methodology.

Do not stop at planning. Perform the correction, add regression evidence, run deterministic verification, obtain independent assessment, reconcile documentation and prepare the existing PR for final review.

Where external Codex interaction or human approval is unavailable, identify the exact action required.

Prioritise correctness, evidence and closure over further expansion of the methodology.

Phase 1 is successful when it demonstrates a complete, credible cycle of:

Implement → Test → Independently Review → Discover Defects → Correct → Reverify → Reconcile → Accept

Complete that cycle, preserve the evidence and close the phase in accordance with existing governance.
