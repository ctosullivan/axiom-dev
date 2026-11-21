# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not yet have a release; entries accumulate under
`Unreleased` until Phase 1 produces something releasable.

## [Unreleased]

### Added

- Repository governance foundation (Phase 1, Stage 1.0): `AGENTS.md`,
  `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`.
- Planning infrastructure: `planning/ROADMAP.md`, `planning/CONTEXT.md`,
  `planning/phase-01-foundation.md`, `planning/prompts/`,
  `planning/retros/`.
- Initial Architecture Decision Records: `decisions/0001` (development
  governance and repository methodology), `decisions/0002` (canonical
  knowledge and documentation architecture), `decisions/0003` (independent
  verification and agent responsibilities).
- `.github/pull_request_template.md`.
- Phase 1 amendment (prompt 002): `decisions/0004` (anti-circularity
  verification mechanics, measurement, explicit acceptance
  demonstrations); `planning/prompts/002-phase-1-amend-and-implement.md`;
  `evidence/phase-1-log.md`.
- Stage 1.1 first real content: `docs/documentation-schema.md`,
  `docs/knowledge-placement.md`, `docs/knowledge-reconciliation.md`,
  `contracts/documentation-schema-validator.md`.
- Stage 1.2: `docs/development-lifecycle.md`, `docs/agent-isolation.md`.
- Stage 1.3 (partial — deterministic piece only, live Codex integration
  blocked): `contracts/codex-gate-policy-evaluator.md`,
  `.github/scripts/policy_evaluator.py` and its test suite (16 passing
  tests), `.github/workflows/deterministic-checks.yml`,
  `.github/workflows/codex-review.yml` (written to spec, gated to skip
  without `OPENAI_API_KEY`), `.github/codex/prompts/review.md`.

- Stage 1.4 (initial implementation, pre-refactor): the first real Axiom
  Dev component — `src/axiom_validator.py`, a knowledge/documentation
  schema validator — against `contracts/documentation-schema-validator.md`,
  with 10 fixtures and 14 passing tests
  (`tests/test_axiom_validator.py`), `requirements.txt` (PyYAML), and a
  locked pre-refactor baseline (`evidence/stage-1.4-baseline.md`).
  Independent review before the baseline was locked found and this
  session fixed two real defects (an unenforced
  "no paths outside the repository" rule; a fenced-code-block false
  positive in heading detection). Dogfooding this validator against
  already-committed real documents (not just fixtures) found and fixed
  one real documentation defect: shorthand ADR citations in
  `docs/documentation-schema.md` and `docs/knowledge-placement.md` that
  didn't resolve as real paths.

- Stage 1.4 (refactor): `src/axiom_validator.py` (one monolithic file)
  split into `src/axiom_validator/{parsing,rules,reporting}.py` plus an
  orchestrator (`__init__.py`) and a new `__main__.py` for
  `python3 -m axiom_validator`. Identical before/after test results
  (14/14, same tests), zero blocking findings from independent review —
  see `evidence/stage-1.4-refactor.md`.

- Stage 1.5: `docs/axiom-validator.md` (human-facing validator
  documentation — a real knowledge-placement gap found via a
  pre-Stage-1.5 self-check, since the component had a contract and
  evidence but no human-facing explanation); a restricted-evidence
  independent documentation reconstruction
  (`evidence/stage-1.5-reconstruction.md`) found and fixed two real
  gaps in that doc (two missing non-goals; one true claim misplaced in
  the wrong section).

- Phase 1 closeout: `evidence/phase-1-closeout.md` (independent
  assessment against all 17 Definition-of-Done items and all 8
  Amendment D rows: 15 MET, 1 partially met, 1 not met — the live Codex
  gate, genuinely blocked on missing credentials/access, not glossed
  over); `planning/retros/phase-1-stages-1.0-through-1.5.md` (first
  retrospective in this project); fixes to two staleness issues the
  closeout found (`CONTRIBUTING.md`, `planning/CONTEXT.md`).

First real software, first real passing tests, first real (non-synthetic)
defect found in this project's own documentation by its own tooling,
first genuine behaviour-preserving refactor with a clean independent
review, first independent documentation reconstruction run against a
deliberately restricted evidence set, and first Phase 1 closeout
assessment — which recommends **leaving Phase 1 open**, not marking it
complete, on two named, real, external blockers.

### Changed

- Corrective amendment (`planning/prompts/003-phase-1-corrective-amendment.md`,
  `decisions/0005`): **Phase 1's independent-Codex-review requirement is
  now native Codex GitHub PR review**, not the API-backed
  `openai/codex-action@v1` workflow — `OPENAI_API_KEY` and GitHub
  required-status-check configuration are no longer Phase 1 blockers.
  `.github/workflows/codex-review.yml` moved to
  `.github/deferred/codex-review.yml` (preserved, not deleted);
  `.github/scripts/policy_evaluator.py` and its tests are unaffected and
  now also run in CI alongside the validator's own suite.
- Documentation drift corrected: `AGENTS.md` §8, `CONTRIBUTING.md`
  ("Making a change" §5), `docs/knowledge-placement.md` (Enforcement
  classes rewritten to a six-level distinction; Placement table's
  "Historical narrative" row corrected to name one destination),
  `docs/axiom-validator.md` (three claims corrected after independent
  semantic review found them contradicted by the actual code — including
  one real code defect, not just a documentation error: see below),
  `docs/development-lifecycle.md` (actor-naming added to all 5
  phase-acceptance steps, not just one), `planning/CONTEXT.md` (was
  missed in this pass's first draft, caught by independent review,
  fixed).
- `src/axiom_validator/validate_file` now resolves `repo_root`
  internally — fixes a real latent defect (present identically in the
  pre-refactor monolith) that made the component's own documented usage
  example reproducibly fail.

### Added

- `contracts/documentation-schema-validator.md` rules 10–15 (field
  type/non-emptiness checks; a minimal governed-documents manifest,
  `docs/governed-documents.txt`), implemented in
  `src/axiom_validator/rules.py` and `__init__.py`, with 6 new fixtures
  and a new, separate test file (`tests/test_axiom_validator_schema_content.py`,
  9 tests) that does not touch the checksum-protected Stage 1.4 baseline
  — re-confirmed byte-identical after this change.
- `decisions/0005` (native Codex review decision; partially supersedes
  `decisions/0004`'s live-integration expectation).
- `.github/workflows/deterministic-checks.yml` gained
  `axiom-validator-tests` and `validate-governed-documentation` jobs —
  the validator's own test suite and every governed document now run on
  every push/PR, with no secret required.
- `evidence/schema-value-assessment.md` (prompt 003 Amendment G): three
  paired schema-vs-document examples, finding that the schema's
  mechanical layer caught none of the eleven real defects this pass's
  semantic review found — all eleven were semantic/editorial-class
  issues, which the schema's own design says it cannot mechanically
  catch.
- `planning/phase-01-foundation.md` §17–§20 (corrective-amendment plan
  amendment, revised Definition of Done, independent review record, and
  batch status).

### Changed (documentation schema and roadmap amendment)

- `decisions/0006`: documentation schemas move from embedded Markdown
  front-matter to companion `<document>.md.schema.yaml` files. 15 real
  documents and 20 test fixtures migrated with Markdown bodies
  byte-for-byte unchanged apart from front-matter removal
  (`evidence/schema-migration.md`); `planning/prompts/001`–`004` (a
  different, unrelated front-matter convention) correctly excepted.
- `contracts/documentation-schema-validator.md` "Contract revision"
  (12 new rules): companion-schema lookup, missing-schema SKIPPED/FAIL
  split, embedded-front-matter-reintroduction detection, orphaned-schema
  detection. Implemented in `src/axiom_validator/`, preserving its
  modular architecture and public CLI/programmatic interface.
- `planning/ROADMAP.md` rewritten from a detailed Stage 1.0–1.5 record
  into a concise, long-term overview covering Phases 1 (in progress) and
  2–4 (proposed direction, not authorised commitments).
- `docs/phase-archiving.md` and `planning/archive/README.md`: a
  documented, tested (not fabricated) phase-archiving procedure.
  **Phase 1 is explicitly not archived.** The procedure's link-
  verification claim was tested against a synthetic fixture, not merely
  asserted.
- `docs/documentation-schema.md`, `docs/axiom-validator.md`,
  `docs/knowledge-placement.md`, `docs/knowledge-reconciliation.md`
  updated to describe the companion-schema convention as current
  policy; the superseded front-matter rationale preserved in
  `decisions/0006`, not deleted.
- Two real defects found and fixed by this session's own testing before
  independent review: a repo-wide orphan scan that would have flagged
  the deliberately-orphaned test fixture forever; an imprecise error
  message for the (expected, harmless) case of an unrelated
  `---`-delimited block in `planning/prompts/`.

### Fixed (Phase 1 final remediation — native Codex review findings)

- `src/axiom_validator/parsing.py`: fenced-code-block stripping only
  recognised exactly-three-backtick fences, so a required heading
  hidden inside a tilde-fenced or 4-plus-backtick-fenced example could
  wrongly count as present. Found by native Codex GitHub review of
  PR #1 — the first defect in this project found by an external
  reviewer rather than a dispatched Claude agent. Reproduced against
  the actual pre-fix code, then fixed with a line-oriented fence-state
  parser; 10 new regression tests
  (`tests/test_fenced_code_blocks.py`).
- `.github/scripts/policy_evaluator.py`: a non-string `severity` value
  (e.g. `{"severity": []}`) raised an unhandled `TypeError` instead of
  the contract's required structured `FAIL_CLOSED`. Also found by
  native Codex review of PR #1. Fixed by validating the type before
  the set-membership test; 17 new regression tests
  (`.github/scripts/tests/test_policy_evaluator_severity_types.py`).
  `contracts/codex-gate-policy-evaluator.md` amended (rule 6) with the
  fix and (after rule 8) with the explicit, reasoned decision not to
  reject unrecognised-but-well-formed severity strings.

### Changed (schema consolidation into `schemas/`)

- `decisions/0007`: every production and fixture documentation schema
  moves a second time, from colocated beside its document
  (`decisions/0006`) to a mirrored path under a top-level `schemas/`
  directory; fixture schemas get their own, separate
  `tests/fixtures/schemas/` tree. `docs/governed-documents.txt` moves
  to `schemas/governed-documents.txt`.
- `contracts/documentation-schema-validator.md` "Contract revision 2."
  `src/axiom_validator/parsing.py` gains `schema_path_for`/
  `doc_path_for_schema`; `validate_file`/`find_orphaned_schemas` each
  gain one new optional, backward-compatible parameter
  (`schema_mirror_root`/`mirror_root`).
- **A missing `schemas/governed-documents.txt` file now fails closed**
  (every document checked without an explicit override fails, naming
  the missing manifest) rather than silently disabling all
  governed-document enforcement — assessed and fixed per an explicit
  requirement to check this case, not found by accident.
  `tests/test_schema_relocation.py` (13 tests, including a symlink
  path-escape regression test checked by hand before independent
  review).
- `docs/` now contains only human-readable Markdown — no `.schema.yaml`
  or manifest files remain in it; checked directly, not assumed
  (`tests/test_schema_relocation.py`'s
  `TestNoStraySchemaFilesOutsideSchemasTree`).

### Fixed (third native Codex review finding)

- `src/axiom_validator/parsing.py`: `HEADING_RE`'s marker/text
  separator used `\s+`, which matches newlines — a bare `#` marker
  with no text of its own, followed by an unrelated paragraph, could
  satisfy a required heading named after that paragraph's first word.
  Found by a second native Codex GitHub review of PR #1. Fixed by
  requiring horizontal whitespace only (`[ \t]+`); a related artifact
  found while verifying the fix's own scenarios (a `#` marker followed
  only by whitespace producing a spurious empty-string heading) fixed
  in the same change. 12 new regression tests
  (`tests/test_heading_whitespace.py`), covering all 9 required
  scenarios plus CRLF line endings.
- `README.md`, `schemas/governed-documents.txt`, `planning/ROADMAP.md`,
  `planning/CONTEXT.md` corrected: all had fallen behind the actual PR
  #1 / native-Codex-review state (one or more claimed "no PR has ever
  been opened" after PR #1 had existed, been reviewed twice, and had
  two of three findings already corrected).
- `evidence/phase-1-final-closeout.md` gained a dated addendum
  recording the second review's actual finding and this correction,
  without rewriting the original assessment's own findings.

### Fixed (fourth native Codex review finding)

- `src/axiom_validator/__init__.py`: `validate_file` only loaded and
  checked `schemas/governed-documents.txt` inside the branch taken
  when a document's own schema file was *absent* — a document whose
  schema existed and parsed cleanly could return `PASS` even when the
  manifest file itself didn't exist at all. Found by a third native
  Codex GitHub review of PR #1. Fixed by loading/checking the manifest
  unconditionally (unless explicitly overridden) before branching on
  schema existence. 10 new regression tests
  (`tests/test_manifest_integrity.py`), covering all 8 required
  scenarios. No new ADR or contract amendment — the contract already
  specified this correctly; only the implementation didn't match it.
- GitHub Actions' actual run result is now confirmed for the first
  time in this project (`Status: Success` on commit `6e75d2b`, fetched
  directly from the live Actions run page), resolving a previously
  open evidence limitation.
- `README.md`, `planning/ROADMAP.md`, `planning/CONTEXT.md`,
  `evidence/phase-1-final-closeout.md` (second addendum) updated to
  reflect PR #1's third review and this correction.

### Fixed (independent review of the fourth-finding correction)

- `src/axiom_validator/rules.py`: `load_governed_manifest` checked
  `.exists()` (true for a directory) before unconditionally calling
  `.read_text()` — a `schemas/governed-documents.txt` that exists but
  isn't a readable regular file (e.g. a directory) raised an unhandled
  `IsADirectoryError` straight out of `validate_file`, instead of the
  structured `FAIL` the contract requires. Found by this session's own
  dispatched independent review (not native Codex this time), via a
  self-constructed adversarial scenario beyond every required test
  case. Fixed by reading inside `try`/`except`, catching `OSError`
  generally rather than checking existence first. 1 new regression
  test.
- `README.md` and `planning/ROADMAP.md` briefly asserted Finding D was
  "independently reviewed with no blocking findings" in the same
  commit that pushed the fix, before that review had actually
  completed — caught live by the review itself (a direct,
  self-contradicting claim against `planning/CONTEXT.md`'s own honest
  "pending" disclosure in the very next commit) and corrected once the
  review's real result was available to cite.
