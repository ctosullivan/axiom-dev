# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not yet have a versioned release; unreleased entries
remain under `Unreleased` until a release is explicitly prepared.

## [Unreleased]

### 2026-11-22 — Phase 2 evidence-first refinement

- Reordered the Phase 2 implementation proposal around an independently
  specified Ledgerkit/hledger vertical slice; knowledge/API and CI now grow
  from demonstrated need rather than preceding dogfooding as a platform.
- Clarified the minimal, read-only Git/file-backed knowledge API, governed
  stable claim IDs, reproducible independent evidence, drift-impact limits
  and explicit CI-versus-required-merge enforcement levels.
- Added a reproducible whole-lifecycle acceptance scenario and value/overhead
  evaluation, including false positives, missed defects and pruning low-value
  features. Template extraction follows actual Ledgerkit use.
- Recast Phase 3 as hypothesis-driven Axiom Assure evaluation of agent and
  retrieval strategies, while preserving ADR 0008's required thin MCP
  adapter deliverable (optional for consumers). **Phase 2 still has no
  A/B test of the template.**
- Reconciled roadmap, Phase 2 proposal, current context and README;
  no runtime/API functionality has been added by this documentation PR.


### 2026-11-22 — Phase transition

- Phase 1 marked Completed by explicit owner decision after PR #1 merged;
  acceptance exceptions retained in a separate evidence record and
  linked logical archive (no historical closeout rewritten).
- Recast roadmap: Phase 2 reusable template with Ledgerkit/hledger
  comparative wiki, local knowledge API, stable claim/artifact IDs,
  deterministic CI drift controls and full-lifecycle dogfooding, with
  **no Phase 2 A/B test of the template**.
- Phase 3 now reserves optional MCP and controlled A/B evaluation of
  agent/knowledge-retrieval strategies when Axiom Assure is ready.
- Simplified `CLAUDE.md` to provider-specific operating instructions;
  updated current context, archive conventions and documentation schemas.


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

### Fixed (fifth native Codex review finding)

- `src/axiom_validator/rules.py`: `check_authoritative_sources` wrongly
  accepted an absolute path to a file inside the repository as if it
  were a valid bare, repository-relative path (contract rule 5).
  `(repo_root / source).resolve()` relies on pathlib's `/` operator,
  which discards `repo_root` when `source` is itself absolute, so an
  absolute path to a real in-repo file passed both the
  repository-containment and existence checks by coincidence. Fixed by
  rejecting `Path(source).is_absolute()` explicitly, before any
  resolution. 9 new regression tests
  (`tests/test_authoritative_source_absolute_path.py`). A structurally
  identical gap in `check_links` (rule 6, body links) was found while
  fixing this and deliberately left open, as out of this specific
  finding's scope — recorded in
  `contracts/documentation-schema-validator.md` and
  `planning/phase-01-foundation.md` §29.

## Phase 2 planning — Stage 2.1 and cross-cutting designs made implementation-ready

Planning only; no code, skill, API, wiki record, CI check or logger
was implemented by this change.

### Added

- `planning/phase-02-stage-2.1-plan.md`: selects Ledgerkit's own
  documented EC-022 (balance-assignment elision parsing,
  `ledgerkit/parser.py`) as the Stage 2.1 dogfooding task, with an
  independently re-derived root cause, both failure modes reproduced
  against the actual pinned hledger binary (commit-matched to
  `~/projects/hledger` HEAD), a required fixture matrix, acceptance
  criteria, and the decision to defer to Ledgerkit's own existing
  `dev-docs/compat-register/` rather than duplicating it.
- `planning/phase-02-adoption-design.md`: the Claude Code skill
  (`.claude/skills/axiom-work/SKILL.md`), consumer file layout,
  install/upgrade/removal mechanism, and non-Claude-agent equivalence.
- `planning/phase-02-knowledge-api-design.md`: the Claim/Source/
  Evidence model, stable identity (reusing Ledgerkit's own
  `LK-<KIND>-<AREA>-<NNN>` scheme where one already exists), the
  four-operation `get`/`find`/`related`/`impacted` API with error
  semantics and contract tests, and an explicit adapter contract for
  normalising an existing non-Axiom register's fields into Axiom's
  common view without altering or duplicating the source record.
- `planning/phase-02-measurement-design.md`: the `.axiom-local/events.jsonl`
  format, existing Claude Code telemetry reuse (hooks, `/usage`,
  OpenTelemetry), privacy/retention/opt-out rules, knowledge-usefulness
  classification and the per-task scorecard.
- `planning/phase-02-architecture.md`: the minimal component diagram.
- `planning/phase-02-planning-review.md`: full independent review of
  this planning package — 2 BLOCKING findings (a cited-but-nonexistent
  provenance file; a generic claim schema that didn't line up
  field-for-field with the real register it commits to reading), both
  fixed in this same batch, plus 3 MATERIAL-NONBLOCKING and 2 ADVISORY
  findings, dispositioned.

### Changed

- `planning/phase-02-template.md`: points to the five documents above;
  §2.1 marked done-as-a-plan.
- `planning/ROADMAP.md`, `planning/CONTEXT.md`: reconciled to reflect
  the now-concrete Stage 2.1 plan and cross-cutting designs. Phase 2
  remains **Planned**; no stage is marked In progress or Completed.

## Phase 2 planning amendment — sequencing, adapter conservatism and simplification

Corrective planning only; no code, skill, API, wiki record, CI check
or logger was implemented or modified by this change, and
`~/projects/ledgerkit`/`~/projects/hledger` remain untouched.

### Fixed (planning defects found by a follow-up corrective review)

- **Stage 2.1/2.4 sequencing overlap**: `planning/phase-02-stage-2.1-plan.md`
  previously included fix-implementation, regression-testing and
  independent-verification requirements that belong to Stage 2.4.
  Rewritten so Stage 2.1 ends at the reviewed contract and a fully
  captured (not merely specified) 9-row fixture matrix; a new explicit
  "Handoff to Stage 2.4" section carries everything implementation-shaped.
- **A genuinely new scope boundary, found while actually capturing the
  full fixture matrix against the live hledger oracle**: hledger's
  balance-assignment semantics resolve an elided amount against the
  account's full running balance across the journal, not merely the
  current transaction's sibling-posting net — confirmed with a
  two-transaction fixture and independently re-confirmed by a second
  reviewer with a different fixture. Ledgerkit's existing
  `resolve_elision()` (`ledgerkit/parser.py:816-869`) only ever sees
  one transaction and cannot provide this. Added as fixture row 9 and
  an explicit scope boundary for EC-022's eventual fix, not silently
  left for a fix to diverge from hledger without disposition.
- **Knowledge-adapter over-generosity**: `planning/phase-02-knowledge-api-design.md`
  previously merged native and derived fields into one view and mapped
  Ledgerkit's `proposed` status to `OBSERVED` (overstating it — no
  execution has actually happened for a `proposed` entry) and assumed
  reviewer metadata lived inside `evidence[]` items rather than at the
  register entry's own top level. Fixed: native/derived fields kept
  visibly separate; `proposed -> UNCERTAIN`; `verified`/`final ->
  VERIFIED` only when `verified_by`/`verified_date` are actually
  present on the native record, `CONTESTED` otherwise;
  `superset`/`subset` relationships now require an explicit
  `mapping_scope` string rather than collapsing into an unqualified
  `equivalent`/`partial`.
- **`impacted()`'s input contract treated a legitimate source deletion
  as malformed.** Redesigned to take Git-derived change records
  (`base`/`head`/`path`/`change_type`/`old_path`); `deleted` and
  `renamed` are now explicitly legitimate inputs, with a rename
  preserving the ability to find claims referencing the old path. 9
  new contract tests.
- **Drift demonstration depended on an unpredictable future hledger
  commit.** `planning/phase-02-stage-2.1-plan.md` §6.2 now specifies
  two controlled conditions for Stage 2.4 (a relevant change — EC-021
  as the primary choice — and a deliberately unrelated change), both
  outcomes recorded including any false positive/negative.
- **Measurement design conflated distinct things** (skill activation,
  API invocation, retrieval, actual use, correct application,
  assessed usefulness, verified outcome) and defaulted to logging raw
  error strings. Fixed with an explicit distinguishing section, a new
  `task_start` event, and a default `error_class` classification
  (raw string opt-in only).
- **Planning volume**: `planning/phase-02-architecture.md` merged into
  `planning/phase-02-adoption-design.md` §9; `planning/phase-02-template.md`
  gained an explicit "Document map and navigation path" section.
- **A dangling forward-reference recurred inside the review record
  itself**: `planning/phase-02-planning-review.md`'s own corrective-review
  addendum asserted a second independent review "follows below" before
  that section existed — the same defect class as the package's
  original BLOCKING finding, caught by the second independent review
  and fixed in the same batch by writing that section.

## Phase 2 final amendment — scoped verification, native dependency extraction, durable oracle evidence

Corrective planning amendment, continuing into Stage 2.1 oracle-evidence
completion only; no skill, API, CI check or logger was implemented,
and `~/projects/ledgerkit`/`~/projects/hledger` remain untouched.

### Fixed

- **Scoped-verification contradiction**: the knowledge-adapter design
  could previously produce `derived.status: VERIFIED` together with
  `derived.scope: null` — contradicting `docs/knowledge-placement.md`'s
  own definition of VERIFIED ("within a stated scope"). Fixed with a
  new scope gate (`planning/phase-02-knowledge-api-design.md` §3b.1):
  an optional, small, Axiom-owned "scope manifest" file, kept outside
  Ledgerkit's own schema, with five deterministic checks. Absent a
  passing manifest, derived status is `UNCERTAIN`, never `VERIFIED`
  with a null scope.
- **Missing evidence vs. contradictory evidence**: missing reviewer
  metadata previously mapped to `CONTESTED`; now maps to `UNCERTAIN`.
  `CONTESTED` is reserved for an actual conflict.
- **Native dependency extraction**: `impacted()` now extracts from a
  native register's `implementation[]` and `tests[]` fields, not only
  `evidence[].ref`; qualified references are resolved to file-level
  paths for Git-diff matching; unparseable/dangling references produce
  an explicit `unresolved_reference` diagnostic.
- **Native-vs-generic validation conflation**: explicitly distinguished
  — Axiom's own default-schema checks (e.g. `evidence[].reviewed_by`)
  no longer apply to a native register with its own, different,
  equally valid convention.
- **Oracle evidence durability**: all nine EC-022 fixture journals,
  full hledger transcripts, exact binary/commit identification and a
  reproduction recipe are now version-controlled at
  `evidence/phase-2-stage-2.1-oracle/`, re-run fresh and reconfirmed
  rather than left in a scratch directory that does not survive the
  session.
- **Drift-demonstration rationale strengthened**: EC-021's relevance
  as the "relevant change" condition is now grounded in an actual
  checked code dependency rather than file co-location; a third,
  same-file-but-semantically-unrelated condition is added to measure
  file-level impact detection's own known false-positive cost directly.
- **Stale section cross-references** (`§7` where the actual section is
  `§6`) fixed across three documents, found during this round's own
  consistency check.

## PR #4 — native Codex review findings fixed

First native Codex review of the planning package (`decisions/0005`),
commit `e83df4b`. 2 P2 findings, both real, both fixed:

- **Local dependencies resolved against the wrong revision space**:
  `implementation[]`/`tests[]` (Ledgerkit file paths) were checked for
  existence against `compatibility_target` (an hledger version
  string) — not a Ledgerkit revision at all. Fixed: local references
  now resolve against an explicit consumer-repository revision,
  `compatibility_target` reserved exclusively for the
  `upstream:<project>` pseudo-path mechanism.
- **Logging opt-out didn't cover CLI-owned event writes**: removing
  hooks did not stop `axiom-knowledge`'s own direct event-writing on
  exit. Fixed with a single shared `AXIOM_DISABLE_LOGGING=1` check
  every event producer honours.

Re-review on the fix (commit `cdc3fb8`) found 1 further P2: the
proposed skill never actually instructed recording `task_start` or
passing `--task-id`, contradicting the measurement design's own
requirement for per-task correlation. Fixed: the skill now records
`task-start` before retrieval and threads `--task-id` through every
subsequent example command, closing with `task-accepted`. A duplicate
step-numbering bug found in the same pass was fixed alongside it.

Re-review on that fix (commit `441f4c8`) found 2 further P2s:
`impacted()`'s upstream-pin detection excluded the exact claim §3b.2
promised it would catch proactively (fixed: now checks both
not-yet-bumped and just-bumped-with-stale-scope-manifest); CLI-owned
events had no actual source for `session_id` (fixed: a `SessionStart`
hook writes a small local handoff file CLI producers read, with an
explicit `null` fallback for invocation outside any session).

Re-review on that fix (commit `1b9904b`) found 1 further P2: the
session-ID handoff file was a single, shared, checkout-wide file —
broken under concurrent sessions (second session's `SessionStart`
overwrites it) and never expired after a session ended. Fixed: the
handoff is now keyed per-session by the `claude` process's own PID,
with `SessionEnd` removing its own file.

Re-review on that fix (commit `449ddea`): **0 findings — clean.**
Five rounds total; every finding fixed in the commit immediately
following its round; three of five rounds were follow-on gaps in the
previous round's own fix (session-ID correlation, in progressively
deeper layers) before converging.

## P1 finding on PR #4's `ci-required` gate (CI enforcement added separately)

The repository owner's own `ci-required` aggregate-gate addition (not
this session's work) was reviewed and found 1 P1: no deterministic
test existed for the gate's merge-decision logic, violating
`AGENTS.md` §8.

- **Fixed**: extracted the gate's inline-YAML logic into
  `.github/scripts/ci_required_gate.py` (byte-identical behaviour) and
  added 11 regression tests covering success/failure/skipped/
  cancelled dependencies and the real workflow's `needs:` list.
- **CI caught a real defect in that fix**: the new test's `pyyaml`
  import wasn't installed in the `policy-evaluator-tests` job. Fixed
  with the same `pip install -r requirements.txt` step the other jobs
  already use.
- Re-review found 2 further P2s on earlier Phase 2 planning content:
  a stale contract-test bullet contradicting an already-corrected
  upstream-detection rule (fixed); and a real, confirmed gap in
  native-register identity/reference integrity checking for Stage 2.3
  (deferred — out of scope for this round, recorded in
  `planning/phase-02-planning-review.md` §10, not silently dropped).

## Stage 2.1 closeout, Stage 2.2 planning, Apache 2.0 relicensing

### Added

- `planning/archive/phase-02-stage-2.1/README.md`: Stage 2.1 closeout
  record (achievements, limitations, deferred EC-022 implementation),
  the first stage-level archive entry — logical archiving, same
  convention as Phase 1's, extended to stage granularity. Registered
  under `schemas/governed-documents.txt` with a mirrored schema.
- `planning/phase-02-stage-2.2-plan.md`: implementation-ready Stage
  2.2 plan — a two-PR split (Axiom Dev's reusable `get`/`find`
  library and tests; Ledgerkit's adoption of the skill/wiki/config),
  reusing the existing adoption/knowledge-API/measurement designs
  rather than duplicating them. Independent acceptance criteria,
  negative tests and measurable-overhead questions predeclared before
  any implementation.
- `decisions/0009-apache-2.0-licensing.md`: ADR recording the MIT →
  Apache 2.0 relicensing decision, its rationale and consequences.
- `NOTICE`: carries the project's copyright line, preserved unchanged
  from the prior MIT notice (2026, Cormac O' Sullivan).

### Changed

- **`LICENSE`**: replaced MIT with the complete, unmodified standard
  Apache License 2.0 text. No vendored third-party code was found
  during inspection; nothing else is relicensed by this change.
- `README.md`'s licence section, `planning/ROADMAP.md` (Stage 2.1 →
  Completed, archived; Stage 2.2 → Planned), `planning/archive/README.md`
  (new "Archived stages" section), `planning/CONTEXT.md` and
  `planning/phase-02-template.md` (document map, §2.1/§2.2 pointers)
  reconciled to the above. No Stage 2.2 functionality implemented; no
  changes to Ledgerkit; no accepted ADR altered in place; PR not
  merged by this change.

### Fixed (native Codex review, PR #5)

- The skill template (`planning/phase-02-adoption-design.md` §6)
  instructed running `axiom-knowledge impacted` and a dedicated
  test-runner wrapper — neither of which Stage 2.2 actually delivers
  (`get`/`find` only; `impacted` is Stage 2.3's work). An agent
  following the skill verbatim after Stage 2.2's own adoption PR
  would have been told to run commands that don't exist yet. Fixed by
  annotating both steps with their actual availability and an
  explicit "skip and say so" instruction, rather than leaving the
  skill to silently fail or an agent to guess at a substitute.
