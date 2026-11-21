---
id: 008
title: Final Phase 1 Correction and Acceptance Preparation
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002, 003, 004, 005, 006, 007]
---

> **Provenance note.** The text below is the complete, verbatim prompt
> that authorised correcting the fifth native-Codex-review finding
> (`check_authoritative_sources` wrongly accepting an absolute path to
> a file inside the repository) on PR #1, and preparing Phase 1 for
> final acceptance. Preserved unmodified as historical source material,
> per `AGENTS.md` §2/§3 and this project's established convention
> (prompts 001–007) of keeping prompts with provenance, never
> reconstructed from memory. Harness-level wrapper content (system
> reminders, tool-call metadata, environment blocks) is excluded as it
> is not part of the assignment; the assignment text is otherwise
> reproduced exactly as written.
>
> Relationship to prior work: this is **amendment 008** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued
> by `002`–`007`. It does not replace any of them; all eight are
> preserved. See `planning/phase-01-foundation.md` §29+ for this
> amendment's own plan detail.

Axiom Dev — Final Phase 1 Correction and Acceptance Preparation

You are the Claude Code orchestrator working on ctosullivan/axiom-dev.

Branch: phase-1/stage-1.0-bootstrap
PR: https://github.com/ctosullivan/axiom-dev/pull/1
Last confirmed HEAD: 10dd266c98

Verify the current state before proceeding.

Objective

Correct the fifth native Codex finding, independently verify the correction, reconcile project knowledge and prepare Phase 1 for human acceptance.

Follow the existing Axiom methodology in AGENTS.md:

UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE

Read the governing contracts, ADRs, Phase 1 plan, existing review findings and closeout evidence.

1. Correct the outstanding Codex finding

Finding E: src/axiom_validator/rules.py

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4652621806

check_authoritative_sources() incorrectly accepts an absolute path to an existing file inside the repository.

This violates contracts/documentation-schema-validator.md, rule 5, requiring repository-relative authoritative-source paths.

Required actions:

1. Reproduce the defect against the existing implementation.
2. Add a failing regression test.
3. Reject absolute paths explicitly before resolving them.
4. Preserve valid repository-relative paths, missing-path detection, ADR-reference handling and repository-containment checks.
5. Test absolute paths inside and outside the repository, valid relative paths and relevant edge cases.
6. Avoid unrelated refactoring or contract changes.

2. Verify independently

Run the full existing test suites:

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=.github/scripts python3 -m unittest discover \
  -s .github/scripts/tests -v

Validate every governed document and check for orphaned schemas.

Dispatch a fresh-context independent reviewer to reproduce the original defect, examine the correction, construct adversarial tests and check for regressions.

Confirm all five Codex findings remain corrected.

Record actual test results and reviewer evidence.

3. Reconcile project knowledge

Update only the necessary current-state records:

* README.md
* planning/ROADMAP.md
* planning/CONTEXT.md
* planning/phase-01-foundation.md
* evidence/phase-1-final-closeout.md

Preserve historical observations. Use concise addenda where appropriate.

Record the fifth Codex finding, correction, regression tests and independent verification.

Keep Phase 1 In progress until human approval.

4. Complete PR preparation

Commit and push the correction to the existing PR branch.

Confirm GitHub Actions passes on the new HEAD.

Add the missing PR description summarising scope, relevant ADRs, verification evidence and known limitations.

For all five Codex findings:

* Record the correction and supporting tests.
* Prepare or post evidence-backed thread replies.
* Resolve threads only after verifying their disposition.

Request native Codex re-review using @codex review on the corrected commit.

Assess any new findings independently. Correct genuine material defects; document proportionate dispositions for nonblocking findings.

Do not initiate an indefinite review cycle or expand Phase 1 for speculative improvements.

5. Prepare final acceptance

Produce a concise acceptance matrix covering:

* Governance and methodology.
* Knowledge placement and documentation reconciliation.
* Behavioural contracts and schemas.
* Validator self-development and refactoring.
* Documentation reconstruction.
* Deterministic CI.
* Independent verification.
* Native Codex review and all finding dispositions.
* Outstanding limitations.
* Human approval requirements.

Use MET / PARTIAL / NOT MET, with evidence references.

Provide the latest commit SHA, CI result, Codex status and any remaining actions.

6. Authority and scope

Do not introduce new architecture, tooling, ADRs or Phase 2 functionality.

Do not reactivate API-backed Codex CI.

Do not merge PR #1, mark Phase 1 Completed or archive it without explicit human approval.

Once the technical requirements are satisfied, stop at:

READY FOR HUMAN ACCEPTANCE

After separate approval, PR #1 can be merged and a small follow-up PR can formally complete and archive Phase 1 under docs/phase-archiving.md.

Execute the corrective work now. Prioritise the smallest reproducible fix, independent evidence and closure over further methodology development.
