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

## Running totals (updated as entries are added)

| Metric | Value | Basis |
|---|---|---|
| Subagent dispatches so far | 6 | 2 Stage 1.0, 1 amendment/1.1, 1 Stage 1.2/1.3, 2 Stage 1.4 (initial + refactor) |
| Subagent tokens so far | 561,944 | 209,592 + 128,322 + 98,748 + 62,324 + 62,958 |
| Blocking defects found by independent review (not self-caught) | 9 | 2 Stage 1.0, 2 amendment/1.1, 3 Stage 1.2/1.3, 2 Stage 1.4 initial, 0 Stage 1.4 refactor — all fixed |
| Advisory defects found and fixed or accepted | 7 | 1 Stage 1.0, 2 amendment/1.1, 2 Stage 1.2/1.3, 2 Stage 1.4 initial, 0 Stage 1.4 refactor |
| Real passing tests | 30 of 30 | 16 policy-evaluator + 14 axiom_validator, both re-run independently and confirmed (twice, for axiom_validator — before and after the refactor, identical) |
| Real (non-synthetic) defects found in Axiom Dev's own documentation | 1 | shorthand ADR citations in docs/documentation-schema.md, docs/knowledge-placement.md — Amendment D demonstration 5 |
| Stages with a recorded, real (non-synthetic) Amendment-D demonstration | 2 fully (rows 4, 7), 2 partially (rows 2, 5), 1 in progress (row 8) | See `planning/phase-01-foundation.md` §10 |
