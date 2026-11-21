---
id: 005
title: Phase 1 Final Remediation and Closeout
status: original
date_received: 2026-11-21
source: user prompt, interactive session (Claude Code)
authorising: true
amends: [001, 002, 003, 004]
---

> **Provenance note.** The text below is the complete, verbatim prompt
> that authorised correcting the two native-Codex-review findings on
> PR #1, consolidating documentation schemas into a top-level
> `schemas/` directory, and preparing (not completing unilaterally)
> Phase 1's final closeout. Preserved unmodified as historical source
> material, per `AGENTS.md` §2/§3 and this project's established
> convention (prompts 001–004) of keeping prompts with provenance,
> never reconstructed from memory. Harness-level wrapper content
> (system reminders, tool-call metadata, environment blocks) is
> excluded as it is not part of the assignment; the assignment text is
> otherwise reproduced exactly as written, including its own internal
> section numbering.
>
> Relationship to prior work: this is **amendment 005** to the chain
> **Original prompt → Plan → Decisions → Implementation → Verification →
> Reconciliation** started by `001-phase-1-bootstrap.md` and continued
> by `002`, `003`, and `004`. It does not replace any of them; all five
> are preserved. See `decisions/0007` (if created) for the schemas/
> relocation ADR and `planning/phase-01-foundation.md` §23+ for this
> amendment's own plan detail.

# AXIOM DEV — PHASE 1 FINAL REMEDIATION AND CLOSEOUT

## 1. Assignment

You are the Claude Code orchestrator responsible for completing the final remediation and closeout of Axiom Dev Phase 1.

Repository: `ctosullivan/axiom-dev`

Expected working directory: `~/projects/axiom-dev`

Current development branch, subject to verification:

`phase-1/stage-1.0-bootstrap`

Existing GitHub pull request:

https://github.com/ctosullivan/axiom-dev/pull/1

This assignment has four objectives:

1. Correct the two defects identified by native Codex review of PR #1.
2. Consolidate documentation schemas into a dedicated top-level `schemas/` directory, keeping human-readable documentation separate from validation metadata.
3. Independently verify all corrections, regression coverage, documentation consistency and Phase 1 acceptance requirements.
4. Prepare and execute Phase 1 closeout in accordance with Axiom's existing governance, including human approval and subsequent archiving.

Do not restart Phase 1 or redesign the methodology.

Preserve existing working functionality, accepted contracts, evidence, architectural decisions and historical records.

**The desired outcome is a demonstrably corrected, independently reviewed and formally accepted Phase 1, ready for Phase 2 planning.**

---

## 2. Governing methodology

Follow the canonical Axiom development lifecycle:

**UNDERSTAND → SPECIFY → ASSESS IMPACT → BUILD → VERIFY → RECONCILE**

Read and comply with:

- `AGENTS.md`
- `CLAUDE.md`
- `CONTRIBUTING.md`
- `planning/ROADMAP.md`
- `planning/CONTEXT.md`
- `planning/phase-01-foundation.md`
- `docs/development-lifecycle.md`
- `docs/knowledge-placement.md`
- `docs/knowledge-reconciliation.md`
- `docs/documentation-schema.md`
- `docs/phase-archiving.md`

Review applicable ADRs, especially:

- `decisions/0003` — independent verification.
- `decisions/0004` — verification, measurement and acceptance.
- `decisions/0005` — native Codex review and deferred automated CI gating.
- `decisions/0006` — separate documentation schemas.

Preserve existing human-approval boundaries.

This prompt authorises the remediation work and preparation of Phase 1 closeout. It does not constitute advance approval to mark Phase 1 Completed or merge pull requests before the final evidence has been presented.

---

# PART A — CORRECT CODEX FINDINGS

## 3. Current Codex review

A native Codex GitHub review was successfully completed on PR #1.

Reviewed commit:

`3a8c395c86db9164e0f9c9c6725cdb8204a72a4b`

The review identified two P2 findings.

At the time this assignment was prepared:

- Both findings were unresolved.
- No P0/P1 findings were reported.
- All four deterministic GitHub Actions jobs passed.
- The pull request remained open and unmerged.

These facts are a starting baseline, not a substitute for checking the current PR state.

Retrieve the actual review comments and source code before implementation.

### Finding 1

File:

`src/axiom_validator/parsing.py`

GitHub review comment:

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629983

Title:

**Exclude all supported fenced code blocks from heading checks**

Codex identified that the existing code-block-removal expression supports only fences containing exactly three backticks.

The implementation can therefore count Markdown headings inside tilde-fenced or longer-backtick-fenced examples as real document sections.

For example:

````markdown
~~~markdown
# Required
~~~
````

A document containing only that example can incorrectly satisfy:

```yaml
required_sections:
  - Required
```

This is a false-positive validation result.

### Required correction

Replace or strengthen the existing code-fence handling so that heading extraction correctly excludes headings inside supported fenced code blocks.

Prefer a simple, understandable implementation over increasingly complex regular expressions.

Consider a line-oriented parser that tracks:

- Opening fence character.
- Opening fence length.
- Valid matching closing fences.
- Longer closing fences.
- Unterminated fences.
- Ordinary headings outside fences.

Support appropriate Markdown fence forms, including three or more backticks and three or more tildes.

Preserve existing heading-extraction behaviour outside fenced blocks.

Do not introduce a new Markdown parsing dependency unless a demonstrated need justifies it.

### Required regression tests

Add tests covering:

1. Three-backtick fenced examples.
2. Four-backtick fenced examples.
3. Longer backtick fences.
4. Tilde-fenced examples.
5. Closing fences longer than their openings.
6. Unclosed fenced blocks.
7. Actual required headings outside fenced examples.
8. Mixed documents containing real headings and fenced examples.
9. A document where the only matching required heading is inside a fenced block, which must fail validation.

Capture evidence that at least one newly added regression test fails against the original implementation and passes after correction.

Do not weaken the existing accepted contract to make the implementation pass.

---

## 4. Finding 2 — Malformed reviewer severity

File:

`.github/scripts/policy_evaluator.py`

GitHub review comment:

https://github.com/ctosullivan/axiom-dev/pull/1#discussion_r4651629985

Title:

**Validate severity types before testing set membership**

The evaluator currently classifies findings using:

```python
if finding["severity"] in BLOCKING_SEVERITIES:
    blocking.append(finding)
else:
    advisory.append(finding)
```

If a finding contains:

```json
{"severity": []}
```

or:

```json
{"severity": {}}
```

the implementation can raise an unhandled `TypeError`.

This violates the accepted policy evaluator contract requiring malformed reviewer output to produce a structured `FAIL_CLOSED` decision.

### Required correction

Validate the severity value before classification.

Malformed severity values must produce a structured `EvaluationResult` with:

`decision = FAIL_CLOSED`

The result must preserve the existing documented response structure:

- `decision`
- `reasons`
- `blocking_findings`
- `advisory_findings`

The CLI must return a nonzero exit code for malformed input without an unhandled traceback.

Preserve the existing P0/P1 blocking behaviour.

Evaluate whether unknown severity strings should be rejected rather than treated as advisory.

However, do not silently broaden or reverse the accepted contract. If stricter severity enumeration is appropriate, amend the contract explicitly and document the rationale.

### Required regression tests

Test malformed severity values including:

- Empty list.
- Empty object.
- Integer.
- Boolean.
- Null.
- Missing severity field.
- Malformed finding object.

Also preserve coverage of:

- P0/P1 blocking.
- Advisory findings.
- Missing reviewer output.
- Invalid JSON.
- Stale review SHA.
- Incomplete review.
- Structured output.

Capture evidence showing the original defect and successful corrected behaviour.

### Important scope restriction

The policy evaluator remains a real, tested component, but its API-backed GitHub Actions integration is deferred under ADR 0005.

Do not reactivate the API-backed workflow.

Do not request an `OPENAI_API_KEY`.

Do not claim that native Codex review is a mechanically enforced merge gate.

---

# PART B — CONSOLIDATE DOCUMENTATION SCHEMAS

## 5. Architectural amendment

The existing documentation-schema migration successfully removed YAML front matter from Markdown.

However, it currently places `.md.schema.yaml` files immediately alongside their Markdown documents.

This means the `docs/` directory contains both human-readable documentation and machine-oriented schema files.

**Amend the architecture so all production documentation schemas live under one dedicated top-level `schemas/` directory.**

The purpose is to make documentation navigation simpler for humans while retaining explicit validation contracts.

### Required repository structure

Adopt the following convention:

```text
axiom-dev/
│
├── README.md
│
├── docs/
│   ├── axiom-validator.md
│   ├── documentation-schema.md
│   ├── development-lifecycle.md
│   ├── knowledge-placement.md
│   ├── knowledge-reconciliation.md
│   ├── agent-isolation.md
│   └── phase-archiving.md
│
├── contracts/
│   ├── documentation-schema-validator.md
│   └── codex-gate-policy-evaluator.md
│
├── schemas/
│   ├── README.md.schema.yaml
│   ├── governed-documents.txt
│   │
│   ├── docs/
│   │   ├── axiom-validator.md.schema.yaml
│   │   ├── documentation-schema.md.schema.yaml
│   │   └── ...
│   │
│   ├── contracts/
│   │   ├── documentation-schema-validator.md.schema.yaml
│   │   └── ...
│   │
│   ├── evidence/
│   │   └── ...
│   │
│   └── planning/
│       ├── archive/
│       │   └── README.md.schema.yaml
│       └── ...
│
├── src/
├── tests/
├── evidence/
├── decisions/
└── planning/
```

This illustrates the intended structure. Build the actual inventory from the repository rather than assuming every illustrated file exists.

### Naming and discovery convention

For a document with repository-relative path:

`docs/axiom-validator.md`

Its schema must exist at:

`schemas/docs/axiom-validator.md.schema.yaml`

For:

`README.md`

Use:

`schemas/README.md.schema.yaml`

For:

`contracts/documentation-schema-validator.md`

Use:

`schemas/contracts/documentation-schema-validator.md.schema.yaml`

The mapping is:

**`<repo>/<relative-document-path>` → `<repo>/schemas/<relative-document-path>.schema.yaml`**

This mapping must be deterministic.

Do not introduce a database, schema registry or manually maintained document-to-schema mapping.

Keep the existing governed-document manifest as the list of documents that require schemas, but relocate it to:

`schemas/governed-documents.txt`

The manifest continues to list repository-relative Markdown paths, not schema paths.

### Directory responsibilities

- `docs/`: human-readable Markdown documentation only.
- `schemas/`: production documentation schemas and their minimal governance manifest.
- `contracts/`: behavioural contracts.
- `evidence/`: verification results.
- `decisions/`: ADRs.
- `planning/`: active plans, historical plans, retrospectives and archives.
- `tests/`: tests and test fixtures.

The `docs/` directory should contain no `.schema.yaml` files or machine-oriented manifest files.

Test-only fixtures may remain under `tests/`, but arrange their schemas in a separate fixture schema directory where necessary to exercise the same deterministic lookup convention.

Do not confuse production schemas with deliberately invalid test fixtures.

---

## 6. Schema migration

Inspect the complete repository for `.md.schema.yaml` files.

The previous migration affected fifteen real schema-bearing documents and twenty fixture schemas. Verify the current inventory independently.

For each production schema:

1. Determine its corresponding Markdown document.
2. Move the schema to the appropriate mirrored location under `schemas/`.
3. Preserve its YAML content and acceptance criteria.
4. Preserve the Markdown document's content.
5. Confirm that authoritative-source references still resolve from the repository root.
6. Verify that the new validator discovers the schema correctly.
7. Confirm there are no obsolete production schemas left alongside Markdown files.

Use Git-aware moves where practical.

Produce a migration record showing:

- Original schema path.
- New schema path.
- Corresponding Markdown document.
- Whether YAML contents changed.
- Validation result.

Any substantive schema-content change must be independently justified.

**This amendment is primarily a location change, not an opportunity to rewrite documentation acceptance criteria.**

---

## 7. Adapt the validator

Relevant existing modules:

- `src/axiom_validator/__init__.py`
- `src/axiom_validator/parsing.py`
- `src/axiom_validator/rules.py`
- `src/axiom_validator/reporting.py`
- `src/axiom_validator/__main__.py`

Preserve the existing modular architecture.

Adapt companion schema discovery to use the new repository-level `schemas/` location.

### Required behaviour

For a governed Markdown document:

1. Compute its repository-relative path.
2. Derive the schema path inside `schemas/`.
3. Fail if the schema is missing.
4. Parse the YAML.
5. Validate required schema fields.
6. Validate document headings.
7. Validate authoritative-source references.
8. Validate relative links.
9. Report actionable errors.

For a non-governed Markdown document:

- Validate it if a schema exists.
- Otherwise retain the accepted `SKIPPED` behaviour.

Preserve existing checks for deprecated embedded YAML front matter.

### Orphan detection

Update repository-wide orphan detection to scan production schemas under `schemas/`.

A production schema is orphaned if its mirrored document does not exist.

Do not allow schemas left in obsolete production locations to silently bypass migration checks.

Ensure test fixtures do not trigger false-positive repository-wide orphan errors.

### Path safety

Preserve repository containment checks.

Reject or safely handle paths outside the repository.

Check that schema lookup cannot escape the intended schema root through manipulated relative paths or symlinks.

### Manifest integrity

Move the governed-document manifest to `schemas/governed-documents.txt`.

Ensure that governed documents cannot bypass required validation simply because a schema is missing.

Also assess the current behaviour when the entire governed-document manifest is missing.

If that would silently disable enforcement, implement an appropriately scoped fail-closed behaviour with tests and an explicit contract amendment.

### Public interface

Preserve the existing CLI where practical:

```bash
PYTHONPATH=src python3 -m axiom_validator README.md --repo-root .
```

Preserve the public `validate_file` and `main` interfaces unless a justified change is required.

Internal schema-discovery helpers may be adapted as necessary.

---

## 8. Contract and ADR amendment

This change modifies the schema-location convention established by ADR 0006.

Create a new ADR, using the next available sequential number, documenting:

- Existing companion-schema convention.
- Why physically colocated schemas reduce documentation readability.
- The chosen top-level `schemas/` architecture.
- Deterministic mirrored paths.
- Migration and maintenance costs.
- Orphan and missing-schema detection.
- Alternatives considered.
- Consequences.
- Supersession relationship with ADR 0006.

Do not rewrite the historical reasoning in ADR 0006.

Amend the current documentation-validator contract to specify the new location convention.

Preserve historical contract revisions as historical records.

Distinguish the new location amendment from the earlier front-matter-to-sidecar migration.

---

# PART C — VERIFICATION

## 9. Test strategy

Treat this as a corrective change against an existing, tested baseline.

Before implementation:

1. Record the current branch and commit.
2. Record current Git status.
3. Capture existing test results.
4. Record the two Codex findings.
5. Identify relevant accepted contract requirements.
6. Preserve the existing evidence baseline.

For each defect, implement a regression test demonstrating the violation before correcting the implementation.

Where feasible, run the new test against the previous implementation and capture the failure.

Then implement the correction.

### Required validator checks

Verify:

- Original validator behaviour remains correct except for authorised changes.
- All fenced-code regression cases pass.
- New mirrored schema discovery works.
- Every governed document validates.
- Missing governed schemas fail.
- Optional documents without schemas are skipped appropriately.
- Invalid YAML fails.
- Broken authoritative-source paths fail.
- Repository path escapes fail.
- Orphaned production schemas are detected.
- Missing schema-manifest handling is safe.
- Deprecated embedded front matter is rejected.
- Relative Markdown links continue working.
- No obsolete schema files remain in production documentation directories.

### Required policy evaluator checks

Verify:

- Malformed severity types return structured `FAIL_CLOSED`.
- P0/P1 behaviour remains correct.
- Valid advisory findings remain non-blocking.
- Stale review detection remains correct.
- CLI output remains machine-readable.
- Exit codes remain correct.

### CI

Update:

`.github/workflows/deterministic-checks.yml`

Replace references to the old governed-document manifest location.

Ensure all existing deterministic checks still run.

No AI API key or new external services are required.

### Independent verification

Use a fresh-context reviewer that did not implement the corrections.

The reviewer must inspect the actual code, tests, contracts and repository structure rather than relying on the implementing agent's report.

Require an evidence-backed assessment of:

1. Both Codex findings.
2. Correctness and completeness of regression tests.
3. Absence of unintended behavioural changes.
4. Completeness of the schema relocation.
5. Validator compatibility.
6. Documentation and contract reconciliation.
7. Remaining Phase 1 acceptance requirements.

Document the actual isolation mechanism and its limitations.

An agent dispatched from the same orchestration environment is best-effort independent unless technical isolation is enforced.

---

# PART D — GITHUB AND CODEX RE-REVIEW

## 10. Update PR #1

Make the corrections on the existing Phase 1 development branch.

Do not merge into `main` before the final review.

Commit the remediation work with a clear message identifying the purpose.

Push the changes to PR #1.

Record:

- Original reviewed SHA.
- Correction commit SHA.
- Modified files.
- Regression tests.
- Independent verification results.
- Any remaining limitations.

Update the PR description if necessary.

### Native Codex re-review

Request another native Codex review of the updated PR:

`@codex review`

Use the connected integration if available.

If the environment cannot post the request, provide the exact GitHub PR URL and the required action for the repository owner.

**Do not substitute a Claude review for a native Codex review while describing it as Codex.**

The second review must examine the corrected commit, not merely the original reviewed commit.

Do not report that Codex found no issues unless the actual second review establishes that result.

### Finding disposition

For both original review threads:

- Record the defect.
- Explain the correction.
- Reference the regression test.
- Link to the correction commit.
- Record the independent verification result.
- Resolve the thread only after the correction has been verified.

Any new Codex findings must be evaluated against the same evidence-based standard.

Address genuine defects or explicitly document an accepted disposition.

P0/P1 findings must be resolved or escalated for explicit human disposition.

P2 findings require proportionate consideration.

Avoid repeated review cycles solely for cosmetic matters.

---

# PART E — FINAL PHASE 1 CLOSEOUT

## 11. Correct current project-state documentation

The repository's existing `planning/CONTEXT.md` and `planning/ROADMAP.md` still describe the absence of a GitHub PR as a Phase 1 blocker.

That is no longer accurate.

PR #1 exists and native Codex review has successfully run.

Update current-state documentation to reflect:

- Actual PR status.
- Actual reviewed commits.
- First Codex review findings.
- Remediation status.
- Second review findings and disposition, once available.
- Real GitHub Actions results.
- Actual outstanding acceptance requirements.

Distinguish the original blocked state from the current state.

Preserve historical closeout evidence as an accurate record of what was known at the time.

Do not rewrite old evidence to suggest that native Codex review occurred earlier than it did.

---

## 12. Final Phase 1 acceptance assessment

Produce a fresh independent closeout assessment against the current accepted Phase 1 requirements.

Consult:

- Original Phase 1 plan and Definition of Done.
- Subsequent accepted amendments.
- ADR 0005's revision of Codex review requirements.
- Documentation-schema amendments.
- Independent verification records.
- Current GitHub PR and review state.
- Current deterministic CI results.

Distinguish historical superseded requirements from current accepted requirements.

### Required acceptance matrix

For every active Phase 1 acceptance criterion, record:

| Criterion | Status | Evidence | Remaining action |
|---|---|---|---|
| Requirement | MET / PARTIAL / NOT MET | Verifiable source | Action or none |

The assessment must explicitly cover:

1. Repository governance.
2. Knowledge placement.
3. Documentation schemas.
4. Behavioural contracts.
5. Development lifecycle.
6. Deterministic testing.
7. Independent verification.
8. Self-development of the validator.
9. Behaviour-preserving refactoring within the tested scope.
10. Independent documentation reconstruction.
11. Native Codex GitHub PR review.
12. Codex findings and their disposition.
13. Contract and documentation reconciliation.
14. Measurement and evidence records.
15. Roadmap and session-state accuracy.
16. Final human acceptance requirements.

Do not reintroduce the deferred API-backed Codex CI gate as a Phase 1 completion requirement.

### Closeout evidence

Create a new final closeout record, preserving the earlier assessment separately.

Suggested path:

`evidence/phase-1-final-closeout.md`

Include:

- Scope and review methodology.
- Original Codex review findings.
- Corrections and regression evidence.
- Latest independently verified commit.
- Deterministic CI results.
- Native Codex re-review result.
- Remaining limitations.
- Acceptance matrix.
- Independent reviewer verdict.
- Recommendation to the human owner.

Where evidence is unavailable, record the requirement as pending rather than satisfied.

---

## 13. Human acceptance and merge

Phase completion requires explicit human approval under `AGENTS.md`.

The orchestrator must present the final closeout assessment and request the repository owner's approval before:

- Marking Phase 1 Completed.
- Merging PR #1.
- Archiving Phase 1.
- Starting Phase 2 implementation.

If human approval or required external review cannot be obtained, stop at a clearly identified **Ready for human acceptance** state.

Do not fabricate approval or silently relax acceptance criteria.

### Recommended merge and closeout sequence

Use a two-step process to avoid invalidating the final reviewed code commit with additional post-review bookkeeping.

**Step A — Remediation PR**

Complete corrections, deterministic tests, documentation reconciliation and independent verification on PR #1.

Obtain native Codex re-review on the updated commit.

Resolve findings.

Present the final acceptance recommendation.

After explicit human approval, merge PR #1.

**Step B — Phase 1 formal closeout**

Once PR #1 is merged, record its final merged state and complete the formal closeout and archiving changes in a small follow-up PR.

This avoids claiming that a pending PR has already been merged and avoids constructing self-referential commit records.

The follow-up PR should contain only the necessary closeout, roadmap, context and archive changes, plus any corrections identified during their independent review.

Do not invent merge SHAs or completion dates.

Obtain human approval before marking completion and merging the closeout PR.

---

## 14. Archive Phase 1 after acceptance

Follow the existing procedure in:

`docs/phase-archiving.md`

After successful acceptance and merger of the remediation work, create:

`planning/archive/phase-01/README.md`

Use the actual accepted evidence.

The archive entry must include:

- Phase title and objective.
- Accepted completion date.
- Final scope.
- Relevant ADRs.
- Behavioural contracts.
- Implementation evidence.
- Independent verification results.
- Original and final Codex review.
- Original defects and their corrections.
- Final approved PR.
- Accepted limitations.
- Deferred work.
- Retrospective.
- Links to the original Phase 1 plan.

Preserve the existing canonical Phase 1 plan.

Do not move or duplicate historical contracts and evidence.

Update the archive index and its schema.

Update `planning/ROADMAP.md` to show Phase 1 as Completed only after the required human approval.

Update `planning/CONTEXT.md` to identify Phase 2 planning as the next action.

Phase 2 remains proposed until its own plan is reviewed and authorised.

---

# PART F — DEVELOPMENT HYGIENE

## 15. Scope control

The purpose of this assignment is to close Phase 1, not extend it indefinitely.

Do not introduce:

- A new orchestration framework.
- A knowledge database.
- A knowledge graph.
- New specialist-agent infrastructure.
- Automated Codex API integration.
- Additional CI gating systems.
- Unnecessary schema metadata.
- A new documentation engine.
- Phase 2 implementation.
- Unrelated architectural refactoring.

Prefer the smallest conventional correction that demonstrably satisfies the requirements.

Avoid generating additional ADRs for routine implementation choices.

Use a new ADR only for the substantive schema-location decision or another genuinely necessary architectural change.

Preserve historical evidence and accepted architectural decisions.

---

## 16. Required execution sequence

Execute the work in this order.

### UNDERSTAND

Inspect the repository, current PR, Codex comments, contracts, tests and documentation.

Establish the actual current baseline.

### SPECIFY

Preserve this prompt under the next available `planning/prompts/` identifier.

Create a focused remediation and closeout plan.

Amend behavioural contracts where necessary.

Document the new schema-location decision.

Independently review the planned acceptance criteria.

### ASSESS IMPACT

Identify all affected code, tests, schemas, documentation, CI, contracts and knowledge records.

### BUILD

Correct both Codex findings.

Move production schemas into the new `schemas/` directory.

Update validator discovery and orphan detection.

Update the governed-document manifest.

Update tests and CI.

Reconcile documentation.

### VERIFY

Run deterministic tests.

Demonstrate regression failures against the original defects.

Demonstrate passing corrected behaviour.

Run independent review.

Verify the entire production schema inventory.

### RECONCILE

Record evidence, update contracts and current-state documentation, and commit changes to the existing PR branch.

Request native Codex re-review.

Disposition all findings.

### CLOSE OUT

Prepare an independently evidenced final Phase 1 acceptance assessment.

Obtain human approval.

Merge the remediation PR only after approval.

Complete the formal phase archive and status updates through the documented closeout procedure.

Do not begin Phase 2 implementation.

---

## 17. Definition of Done

The technical remediation is complete when:

- [ ] Both original Codex findings have been independently reproduced or otherwise substantiated with concrete evidence.
- [ ] Both defects are corrected.
- [ ] Regression tests demonstrate the corrections.
- [ ] Existing relevant behaviour remains correct.
- [ ] All production schemas reside under `schemas/`.
- [ ] `docs/` contains only human-readable Markdown documentation.
- [ ] Schema lookup uses deterministic mirrored paths.
- [ ] The governed-document manifest resides under `schemas/`.
- [ ] Missing and orphaned schemas are detected appropriately.
- [ ] Schema location changes are recorded in a new ADR and accepted contract amendment.
- [ ] The complete validator test suite passes.
- [ ] The complete policy evaluator test suite passes.
- [ ] Deterministic GitHub Actions passes on the corrected commit.
- [ ] An independent reviewer verifies the corrections.
- [ ] Historical evidence is preserved.
- [ ] Documentation and current-state records are reconciled.
- [ ] The corrected PR is submitted for native Codex re-review.
- [ ] Codex findings are dispositioned with evidence.

Phase 1 formal closeout is complete only when:

- [ ] Final native Codex review requirements are satisfied.
- [ ] All active Phase 1 acceptance criteria are independently assessed.
- [ ] The final closeout evidence is recorded.
- [ ] Human approval is obtained.
- [ ] PR #1 is merged.
- [ ] Phase 1 is formally marked Completed with approval.
- [ ] The Phase 1 archive entry exists and references actual evidence.
- [ ] The archive index is updated.
- [ ] The roadmap reflects the accepted state.
- [ ] Session context identifies Phase 2 planning as the next action.
- [ ] The formal closeout change has been independently reviewed and merged with human approval.

Do not conflate completion of the technical remediation with completion of the formal acceptance process.

---

## 18. Final report

Produce a concise, evidence-backed report covering:

### A. Codex findings

For each finding:

- Original defect.
- Corrective change.
- Regression test.
- Independent verification result.
- Final disposition.

### B. Schema consolidation

Include the final directory structure, migrated schema inventory, validator changes and contract amendments.

Demonstrate that Markdown documentation is separated from its schema metadata.

### C. Verification

Report actual test counts, failures, GitHub Actions results and independent review findings.

### D. Phase 1 acceptance

Provide the acceptance matrix, final verdict, remaining limitations and human-approval status.

### E. GitHub

Identify the current branch, relevant commits, PR URL, latest Codex review status and any remaining human actions.

### F. Phase archive

Once formally authorised and completed, link the Phase 1 archive record and identify the next planned phase.

---

## 19. Final instruction

**Complete the Phase 1 remediation using Axiom's existing methodology, with the minimum necessary implementation complexity.**

Prioritise:

1. Correctness.
2. Independent verification.
3. Clear documentation.
4. Reproducible evidence.
5. Preservation of accepted behaviour.
6. Minimal architectural overhead.

The expected final result is a corrected and independently reviewed Phase 1 implementation, a clean documentation hierarchy, and an evidence-backed closeout ready for formal human acceptance.

Do not stop after planning or summarising the intended changes. Implement and verify everything that can be completed within the available environment.

Where GitHub access, external Codex review or human approval is required, identify the exact outstanding action rather than claiming completion.

**Phase 1 should close because the evidence supports completion—not because the implementation agent considers the work finished.**
