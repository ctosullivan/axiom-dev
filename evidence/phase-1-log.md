# Phase 1 evidence and measurement log

Started 2026-11-21, per `decisions/0004` (Amendment C). Records real,
observed data only. Entries predating this log (most of Stage 1.0) are
not back-filled with invented numbers — only what was actually captured
in that work is noted below, under "Stage 1.0 (retrospective, partial)."

Format per entry: date, stage, what happened, what was measured, what
could not be measured and why.

## Stage 1.0 (retrospective, partial — this log did not exist yet)

- **Agent usage (the only sub-metric this session can state exactly,
  because dispatch notifications report it directly):**
  - CodeCompass-precedent research fork: 113,229 tokens, 11 tool uses,
    57.6s duration.
  - Independent review of the Stage 1.0 foundation: 96,363 tokens,
    27 tool uses, 151.9s duration.
- **Defects detected by independent review, not by the implementing
  agent's own checks:** 2 blocking (B1: status docs claimed an unperformed
  commit/push; B2: independent-review section was an empty placeholder
  while other files claimed its findings were "resolved"), 1 advisory
  acted on (A1: undefined ADR status string), 4 advisory not requiring
  action (A2–A6: dependency soundness, citation accuracy, scope
  discipline, cross-reference integrity — all confirmed, no fix needed).
- **Rework:** both blocking findings required a real fix (not a
  documentation-only patch) before commit — `planning/phase-01-foundation.md`
  §6 was rewritten with real findings, and the actual git branch/commit/push
  were performed for the first time only after that fix.
- **Not measured:** wall-clock time for the orchestrating session's own
  (non-subagent) work; any real monetary cost; a non-Axiom comparison
  baseline. None of these were observable from inside the session, so
  none are estimated here.

## 2026-11-21 — Phase 1 amendment (prompt 002) + Stage 1.1 first content

- **Development effort:** one orchestrating-session pass covering the
  amendment (`decisions/0004`, `planning/prompts/002-...md`, plan edits)
  and Stage 1.1's first real content (`docs/documentation-schema.md`,
  `docs/knowledge-placement.md`, `docs/knowledge-reconciliation.md`,
  `contracts/documentation-schema-validator.md`), plus one independent
  review pass and its resolution.
- **Knowledge reused:** the amendment builds on, rather than replaces,
  `decisions/0001`–`0003`; `docs/documentation-schema.md` explicitly
  resolves an item `decisions/0002` left open rather than re-deciding it
  from scratch; `contracts/documentation-schema-validator.md` traces
  directly to `planning/prompts/001-...md` §5's original validator
  mention.
- **Agent usage:** one independent-review dispatch — 128,322 tokens,
  30 tool uses, 233.9s duration (per that dispatch's own notification).
- **Defects detected by independent review, not by self-check:**
  2 blocking (authoritative_sources format inconsistency that would fail
  the validator contract against live Stage 1.1 content; "mechanical
  enforcement" claimed for what is actually a procedural control — the
  same mislabeling risk `decisions/0003` names for isolation claims),
  4 advisory, all acted on or explicitly accepted as recorded (see
  `planning/phase-01-foundation.md` §11 for full disposition).
- **Rework:** both blocking findings required real content fixes (contract
  rules 5/7 reworded, two documents' front-matter corrected, two
  "mechanical" claims reworded to "procedural" with what would make them
  mechanical stated) — not documentation-only acknowledgement.
- **Not measured:** real API/token cost in currency terms (not available
  in this environment); comparison against a non-Axiom-governed baseline
  (no such baseline exists to compare against).

## 2026-11-21 — Stage 1.2 (lifecycle/isolation docs) + Stage 1.3 (Codex gate, partial)

- **Development effort:** one orchestrating-session pass. Stage 1.2:
  two docs (`docs/development-lifecycle.md`, `docs/agent-isolation.md`).
  Stage 1.3: researched current Codex integration options (two web
  searches, four authoritative sources cited), implemented
  `.github/scripts/policy_evaluator.py` against a contract written to
  match it (`contracts/codex-gate-policy-evaluator.md` — written after
  the code, unlike Stage 1.4's mandatory contract-first rule; recorded
  as such in that contract's own "Ordering note" rather than left
  implicit), wrote 16 unit tests, ran them (16/16 pass, 0.003s), ran 3
  real end-to-end CLI invocations, wrote two GitHub Actions workflows and
  one Codex prompt file.
- **Defects / self-caught (not yet independently reviewed as of this
  entry):** none found needing fixes in this pass's own re-reading;
  pending independent review.
- **Real test evidence (first in this project with actual passing
  tests):** 16/16 unit tests pass, exercising all 6 required scenarios
  from `planning/prompts/002-...md` §6 Stage 1.3 (valid PR, P0/P1 defect,
  advisory finding, malformed reviewer output, missing/failed review,
  stale-commit review) plus edge cases (non-object JSON, missing fields,
  non-list findings). 3 real CLI end-to-end runs (BLOCK, FAIL_CLOSED,
  PASS) confirmed matching exit codes.
- **Blocker, named honestly:** the live Codex integration
  (`.github/workflows/codex-review.yml`) is written to spec but cannot
  be exercised — no `OPENAI_API_KEY` exists in this environment, and
  provisioning one plus enabling recurring paid review calls is a
  cost/credentials decision for a human, not this session
  (`planning/prompts/002-...md` §9's own instruction: "assess API usage
  and costs before enabling recurring paid review calls"). Stage 1.3's
  full exit criterion is therefore **not met**; this is recorded as an
  open item, not resolved by the deterministic piece alone.
- **Not measured:** real API/token cost for the Codex calls this stage
  would make if enabled (no key, so no calls were made, so there is
  nothing to measure yet — not estimated).
- **Agent usage:** one independent-review dispatch, which actually ran
  the test suite itself rather than trusting the claim — 98,748 tokens,
  37 tool uses, 290.6s duration.
- **Defects detected by independent review, not by self-check:** 3
  blocking (a vacuous staleness check caused by comparing a value against
  itself; silent fabrication of missing required fields that would have
  defeated a fail-closed rule; committed `.pyc` files with no
  `.gitignore`), 2 advisory (over-broad workflow permissions; a second
  blocker — required-status-check configuration — left unmentioned
  alongside the credentials one). All fixed; see
  `planning/phase-01-foundation.md` §12.
- **Rework:** the staleness-check fix required a real architectural
  change (an added live GitHub API call), not a comment edit — this is
  the first defect in this project caught by independent review that
  required redesigning a mechanism, not just rewording a claim about it.

## 2026-11-21 — Stage 1.4 initial implementation (pre-refactor)

- **Development effort:** one orchestrating-session pass. Built
  `src/axiom_validator.py` (initial, deliberately monolithic) against
  the already-accepted contract, 8 fixtures (1 valid + 7 invalid, one
  per contract rule), 12 initial tests, ran them (real, 12/12 pass
  before the real-document check revealed a real defect — see below).
- **Real dogfooding finding (not synthetic):** `TestRealRepositoryDocuments`
  — testing the validator against already-committed real documents, not
  only fixtures — genuinely failed on first run: `docs/documentation-schema.md`
  and `docs/knowledge-placement.md` used shorthand ADR citations
  (`decisions/0002`, `decisions/0004`) that don't resolve as real paths.
  Fixed in the same pass. This is the first real (non-synthetic) defect
  this project's own tooling has found in its own documentation —
  Amendment D demonstration 5 now has real teeth, not just a
  reviewer-found formatting inconsistency.
- **Agent usage:** one independent-review dispatch of the initial
  implementation (before any refactor), which re-ran the tests,
  re-verified checksums, and verified the dogfooding finding against
  `git diff` itself — 62,324 tokens, 25 tool uses, 104.1s duration.
- **Defects detected by independent review, not by self-check:** 2
  blocking (contract rule 5/6's "no paths outside repository" was
  unenforced — demonstrated with a working counter-example; rule 4's
  heading match had no fenced-code-block exclusion — also demonstrated),
  2 advisory (narrow `§`-only bare-path check; rule 7 doesn't distinguish
  wrong-ADR-number from right-number-wrong-slug). Both blocking findings
  fixed with real regression fixtures and tests, not just prose
  acknowledgement; both advisory findings left as documented limitations
  — see `evidence/stage-1.4-baseline.md`.
- **Rework:** two real code fixes (`_is_within()` containment check;
  `FENCED_CODE_BLOCK_RE` exclusion), 2 new fixtures, 2 new tests. Suite
  grew from 12 to 14 tests, all passing on re-run.
- **Baseline locked:** `evidence/stage-1.4-baseline.md` records the
  final (post-fix) checksums and test output as the pre-refactor
  comparison point for the refactor about to follow.

## 2026-11-21 — Stage 1.4 refactor

- **Development effort:** one orchestrating-session pass. Split
  `src/axiom_validator.py` into `parsing.py`/`rules.py`/`reporting.py`/
  `__init__.py`/`__main__.py`; deleted the original file; re-ran the
  exact test suite (14/14 pass, identical to baseline); verified
  protected checksums unchanged; verified the new `python3 -m
  axiom_validator` CLI entry point directly.
- **Agent usage:** one independent-review dispatch of the refactor —
  62,958 tokens, 16 tool uses, 69.2s duration. Notably the fastest/
  cheapest review so far, consistent with there being nothing wrong to
  investigate at length.
- **Defects detected by independent review, not by self-check:** 0
  blocking, 0 advisory requiring action — the review's role here was
  entirely re-derivation/confirmation (re-computed checksums, re-ran
  tests, diffed old-vs-new logic line by line), not defect-finding. One
  procedural note (fill in the refactor doc's own placeholder section)
  was actioned.
- **Rework:** none needed — first clean independent review in this
  project's history.
- **Amendment D demonstration 4** ("a meaningful refactor preserves
  independently established behaviour") is now fully demonstrated, not
  partial — see `planning/phase-01-foundation.md` §10 row 4.
- **Amendment D demonstration 7** ("knowledge reused in a later task")
  also now fully demonstrated: Stage 1.4's documents reuse Stage 1.1's
  schema convention and Stage 1.2's isolation vocabulary, concretely.

## 2026-11-21 — Pre-Stage-1.5 reconciliation gap found and fixed

- **Self-caught, not by independent review:** before starting Stage
  1.5's reconstruction, a check against `AGENTS.md` §7's placement table
  found that the validator had a contract (`contracts/`) and evidence
  (`evidence/`) but no human-facing `docs/` explanation — a real
  knowledge-placement gap, not a hypothetical one, per the exact category
  that table calls for. Fixed: `docs/axiom-validator.md` written,
  describing the actual (not aspirational) architecture and usage,
  including a limitations section carrying forward the documented gaps
  from Stage 1.4's reviews rather than re-litigating or hiding them.
- **Why this matters for Amendment D demonstration 5:** this is a second
  real instance of "documentation consistency evaluated against real
  changes" — this time caught by checking the project's own placement
  rules against itself, not by an independent reviewer or a failing test.

## 2026-11-21 — Stage 1.5 independent documentation reconstruction

- **Development effort:** one orchestrating-session pass. Defined the
  permitted-evidence boundary explicitly, dispatched a two-phase
  reconstruction (blind reconstruction, then compare against the real
  doc), reviewed its findings, fixed `docs/axiom-validator.md` (two
  missing non-goals, one misplaced-but-true claim moved and
  independently re-verified before being kept), wrote
  `evidence/stage-1.5-reconstruction.md`.
- **Agent usage:** one reconstruction dispatch — 79,349 tokens, 22 tool
  uses, 179.7s duration.
- **Defects/gaps found by the reconstruction, not by self-check:** 2
  real (missing non-goals; misplaced claim), both fixed; 1 correctly
  classified by the agent itself as unverifiable-from-its-restricted-evidence
  rather than wrong (accepted, no fix needed — the claim was true and
  appropriately scoped outside the component's own contract/evidence).
- **No staleness or historical-rationale-as-current-justification
  found** — checked specifically, per the task's own instructions.
- **Isolation note:** this is the first exercise in this project built
  around a restricted evidence set (not full repository access) rather
  than just a fresh context — a stronger approximation of real
  documentation reconstruction, still named as best-effort, not
  mechanical (`evidence/stage-1.5-reconstruction.md` "Isolation honesty
  note").

## 2026-11-21 — Amendment D demonstration 1 (fresh agent resumes from repository knowledge alone)

- **What was run:** a fresh agent, given no context beyond "start working
  on this repository," was asked to identify the project, its
  methodology, current status, key decisions, and next action, using
  only repository contents.
- **Result: a real finding, not a clean pass — which is more valuable
  evidence, not less** (per the project's own repeated principle that a
  clean result on the first attempt deserves more scrutiny). The agent
  correctly reconstructed the project, mission, methodology, all four
  ADRs, and the Stage 1.0–1.4 status accurately from `README.md`,
  `AGENTS.md`, `decisions/`, and `planning/ROADMAP.md`. It also caught a
  **genuine, real, transient inconsistency**: this test was run while
  Stage 1.5's reconstruction work existed in the working tree but had
  not yet been committed, so the committed `planning/CONTEXT.md` and
  `planning/ROADMAP.md` still described Stage 1.5 as "Planned"/not
  started, while uncommitted files already showed it done. The agent
  correctly flagged this as "the one place where reading the docs alone
  would mislead," named it as a real instance of the exact failure mode
  `AGENTS.md` §4/§5 (current CONTEXT.md, same-commit doc sync) exist to
  prevent, and correctly judged it as mid-session work-in-progress
  rather than a methodology failure.
- **Disposition: fixed by committing this same batch** (the one
  containing this log entry) — the inconsistency the test found no
  longer exists once this commit lands. The finding itself, and the
  fact that it was found by a genuinely fresh agent during a real
  working session rather than a staged clean-room exercise, is recorded
  here rather than smoothed over.
- **Agent usage:** 79,707 tokens, 16 tool uses, 72.9s duration.

## 2026-11-21 — Phase 1 closeout assessment

- **What was run:** a fresh, uninvolved agent independently re-verified
  all 17 Definition-of-Done items and all 8 Amendment D rows by
  re-running both test suites itself, re-computing checksums itself, and
  confirming the missing `OPENAI_API_KEY`/`gh` directly rather than
  trusting prior claims.
- **Result:** 15 of 17 DoD items MET, 1 partially met, 1 not met (the
  live Codex gate — genuinely blocked); 6 of 8 Amendment D rows fully
  demonstrated, 1 correctly left open, 1 is this assessment itself. No
  overclaiming found anywhere in the repository. Two real staleness
  issues found (outside every prior review's stated scope) and fixed in
  this same change: `CONTRIBUTING.md`'s testing section, and
  `planning/CONTEXT.md`'s self-referential commit-SHA pattern.
- **Verdict recorded:** Phase 1 stays open — partially complete, two
  named external blockers, not a shortcut taken. Full record:
  `evidence/phase-1-closeout.md`.
- **Agent usage:** 145,847 tokens, 32 tool uses, 181.3s duration — the
  largest single review dispatch in this phase, proportionate to
  assessing the entire repository against two full checklists.
- **Phase 1 retrospective written:** `planning/retros/phase-1-stages-1.0-through-1.5.md`,
  the first entry in `planning/retros/`.
- **One more real, non-synthetic catch, this time pre-commit rather than
  by independent review:** running the validator against the
  retrospective itself (before this commit) found the exact same
  shorthand-ADR-citation defect Stage 1.4's dogfooding found in
  Stage 1.1's docs — `decisions/0001` instead of the real filename —
  this time in the retrospective's own front-matter, introduced while
  writing this very log entry. Fixed before commit. Third real instance
  of this specific defect pattern across the phase.

## 2026-11-21 — Corrective amendment batch (prompt 003)

- **Development effort:** one orchestrating-session pass covering plan
  amendment (`planning/phase-01-foundation.md` §17/§18), a new ADR
  (`decisions/0005`), four documentation-drift fixes (B1–B4, including
  one — `docs/axiom-validator.md`'s own staleness against this pass's
  changes — found by this session's own re-reading, not by the
  independent reviewer), validator schema strengthening (Amendment C: 2
  new rules.py functions, 1 new `__init__.py` wiring point, 6 new
  fixtures, 1 new test file with 9 tests, 1 new governed-documents
  manifest), deterministic CI completion (Amendment E: 2 new workflow
  jobs), and deferring the API-backed Codex workflow (Amendment A:
  `.github/workflows/codex-review.yml` → `.github/deferred/codex-review.yml`).
- **Agent usage:** 2 independent-review dispatches — the first, 187,061
  tokens / 60 tool uses / 602.2s, covering drift (Amendment B), validator
  strengthening (Amendment C), semantic review of 3 named docs (Amendment
  D), and refactor re-confirmation (Amendment F); the second, 71,421
  tokens / 17 tool uses / 77.5s, a focused confirmation pass that
  independently re-ran all 8 of the first review's named fixes (not
  re-reading the surrounding prose) and confirmed every one holds.
- **Defects detected by independent review, not by self-check:** 3
  BLOCKING (`planning/CONTEXT.md` never updated against `decisions/0005`;
  `planning/phase-01-foundation.md` §17/§18 cited a `§19`/`§20` and an
  `evidence/schema-value-assessment.md` that did not yet exist — this
  review's own findings became that missing record), plus — within the
  semantic review itself — 3 concrete FAILED claims in
  `docs/axiom-validator.md` (one tracing to a real latent code defect,
  not just a documentation error: `validate_file` failed to resolve an
  unresolved `repo_root`, reproducibly breaking its own documented usage
  example), 2 unmet acceptance criteria in `docs/knowledge-placement.md`,
  and a partial gap (1 of 5 steps) in `docs/development-lifecycle.md`.
  2 ADVISORY (`decisions/0005`'s "preserved as-is" overstated a trivial
  real edit; contract rule 12 generalised beyond the prompt's literal
  wording — accepted with a recorded rationale, not changed). All
  BLOCKING and FAILED findings fixed in this session, re-verified
  directly (re-ran the fixed usage example, re-ran the full test suite,
  re-checked the protected baseline checksums) before being recorded as
  fixed in `planning/phase-01-foundation.md` §19.
- **Anti-circularity check held under a second round of changes:** the
  Stage 1.4 protected baseline (10 fixtures + `tests/test_axiom_validator.py`)
  was re-checksummed twice in this batch — once after the initial
  Amendment C implementation, once again after the `validate_file`
  `repo_root` fix — and matched `evidence/stage-1.4-baseline.md` exactly
  both times.
- **Real (non-synthetic) defect found in Axiom Dev's own code, not just
  its documentation — a first for this project:** `validate_file`'s
  failure to resolve `repo_root` was a real, reproducible bug (not a
  documentation inaccuracy) present identically in the pre-refactor
  monolith, surfaced only because independent review actually ran
  `docs/axiom-validator.md`'s own documented usage example instead of
  reading it as prose.
- **Not measured:** real API/token cost for native Codex review (none
  has run yet — no PR exists); wall-clock time for this session's own
  non-dispatched work.
- **Blocker, named honestly, unchanged in kind from before this batch but
  narrower in scope:** no `gh` CLI, no GitHub token, no passwordless
  `sudo` to install `gh` — re-confirmed directly in this session, not
  assumed. No PR has ever been opened; native Codex GitHub PR review
  (`decisions/0005`) cannot be performed until one is. `OPENAI_API_KEY`
  provisioning and GitHub required-status-check configuration are
  **no longer** blockers — `decisions/0005` removed both as Phase 1
  requirements.

## 2026-11-21 — Documentation schema and roadmap amendment (prompt 004)

- **Development effort:** one orchestrating-session pass covering a new
  ADR (`decisions/0006`), a contract revision
  (`contracts/documentation-schema-validator.md`, 12 new rules),
  validator code changes (`src/axiom_validator/{parsing,rules,__init__}.py`),
  migration of 15 real documents and 20 test fixtures from embedded
  front-matter to companion `.schema.yaml` files
  (`evidence/schema-migration.md`), 4 new test fixtures/3 new test
  methods, a rewritten `planning/ROADMAP.md`, a new phase-archiving
  procedure (`docs/phase-archiving.md`, `planning/archive/README.md`),
  and documentation/governance reconciliation across 4 `docs/` files.
- **Real latent bug found and fixed by this session's own testing,
  before independent review:** `rules.find_orphaned_schemas`, run
  unmodified against the real repository root, would have flagged the
  deliberately-orphaned test fixture
  (`tests/fixtures/invalid/orphaned.md.schema.yaml`) as a real orphan on
  every future CI run, forever — caught by actually running `main()`
  against the real repo root before committing, not left as a
  hypothetical. Fixed by excluding `tests/` from the repo-wide scan by
  default.
- **Real design gap found and fixed by this session's own testing:**
  embedded-front-matter detection (contract revision rule 7) fires on
  any `---`-delimited block, including `planning/prompts/`'s unrelated
  provenance-metadata convention — not a code defect (those files were
  never validated or claimed to pass), but the original error message
  wording presumed every such block was a reintroduced documentation
  schema. Fixed by rewording the message and adding an explicit
  Non-goal to the contract revision, rather than attempting to guess a
  block's semantic intent.
- **Agent usage:** 1 independent-review dispatch covering migration
  correctness, validator behaviour (including reviewer-constructed
  counter-examples), the roadmap/archiving rewrite, and documentation
  reconciliation — 131,094 tokens, 50 tool uses, 286.3s. No BLOCKING
  findings; 2 ADVISORY bookkeeping/narrative inaccuracies found and
  fixed (a wrong test-count sentence in this plan's §21; a stale
  governed-document count in `evidence/schema-migration.md`) — both
  caught by the reviewer re-deriving numbers directly (`git show`,
  recounting test methods) rather than trusting this session's own
  arithmetic.
- **Not measured:** real API/token cost for native Codex review (still
  no PR exists); wall-clock time for this session's own non-dispatched
  work.
- **Blocker, unchanged in kind:** no `gh` CLI, no GitHub token, no PR
  ever opened. This amendment does not touch that blocker — it was out
  of scope for prompt 004, which explicitly preserves `decisions/0005`'s
  native-Codex-review decision unmodified (§11).

## Running totals (updated as entries are added)

| Metric | Value | Basis |
|---|---|---|
| Subagent dispatches so far | 12 | 2 Stage 1.0, 1 amendment/1.1, 1 Stage 1.2/1.3, 2 Stage 1.4 (initial + refactor), 1 Stage 1.5 reconstruction, 1 Amendment-D demo 1, 1 Phase 1 closeout, 2 prompt-003 corrective batch (review + confirmation), 1 prompt-004 documentation-schema/roadmap batch |
| Subagent tokens so far | 1,256,423 | 209,592 + 128,322 + 98,748 + 62,324 + 62,958 + 79,349 + 79,707 + 145,847 + 187,061 + 71,421 + 131,094 |
| Blocking/real defects found by independent review (not self-caught) | 17 | 2 Stage 1.0, 2 amendment/1.1, 3 Stage 1.2/1.3, 2 Stage 1.4 initial, 0 Stage 1.4 refactor, 2 Stage 1.5, 2 Phase-1-closeout, 4 prompt-003 corrective batch, 0 prompt-004 batch (clean — see `planning/phase-01-foundation.md` §22) — all fixed and independently re-confirmed |
| Advisory defects found and fixed or accepted | 12 | 1 Stage 1.0, 2 amendment/1.1, 2 Stage 1.2/1.3, 2 Stage 1.4 initial, 0 Stage 1.4 refactor, 1 Stage 1.5 (accepted), 2 prompt-003 corrective batch, 2 prompt-004 batch (bookkeeping/narrative inaccuracies, fixed — see §22) |
| Real passing tests | 43 of 43 | 16 policy-evaluator + 27 axiom_validator (23 before prompt 004 + 4 net-new for embedded-front-matter/orphaned-schema/archive-link-verification coverage), all re-run independently and confirmed |
| Real (non-synthetic) defects found in Axiom Dev's own documentation or code | 5 | shorthand ADR citations (Stage 1.4 dogfooding); CONTRIBUTING.md future-tense staleness (Phase 1 closeout); `planning/CONTEXT.md` staleness against `decisions/0005` (prompt-003 batch); `validate_file`'s unresolved-`repo_root` defect (prompt-003 batch); `find_orphaned_schemas`'s would-fail-CI-forever defect against the real repo root (prompt-004 batch, found by this session's own testing before independent review) |
| Amendment-D demonstrations fully demonstrated with real evidence | 7 of 8 (rows 1, 2, 4, 5, 6, 7, 8) | See `planning/phase-01-foundation.md` §10; row 3 is the one genuine, externally-blocked gap, now reframed by `decisions/0005` as "native Codex review on a real PR," not "automated gate rejection" |
| Phase 1 Definition of Done (17 items, `planning/prompts/002-...md` §11) | 15 MET, 1 partially met, 1 not met | See `evidence/phase-1-closeout.md` (predates the prompt-003 corrective batch) |
| Prompt 003's revised Definition of Done (16 items, `planning/phase-01-foundation.md` §18) | 10 MET, 1 locally-verified-only (CI not triggered on a real GitHub Actions run), 5 open (items 10–12: native Codex review, blocked on no `gh`/token; item 15: no holistic closeout dispatch has run yet, only narrowly-scoped checks and a confirmation pass; item 16: human approval, deliberately not sought by this session) | See `planning/phase-01-foundation.md` §18, §20 |
| Prompt 004's Definition of Done (21 bullet items, `planning/prompts/004-...md` §13) | 19 MET, 1 locally-verified-only (GitHub Actions not triggered on a real run), 2 open (native Codex review and human approval — the same cross-cutting PR/`gh`-token blocker as prompt 003, not new work this amendment could resolve on its own) | See `planning/phase-01-foundation.md` §21, §22 |
