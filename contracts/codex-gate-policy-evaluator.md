# Contract: Codex-gate policy evaluator

Status: **Accepted.** Governs
`.github/scripts/policy_evaluator.py`.

## Scope

A pure function (`evaluate`) that takes the text of a structured review
document plus the PR's actual current head SHA (obtained independently,
not trusted from the document itself), and returns one of three
decisions: `PASS`, `BLOCK`, `FAIL_CLOSED`. No network access, no
dependency on whether Codex itself is actually configured or reachable —
this is deliberately the part of the Stage 1.3 gate that is fully
buildable and testable without live credentials
(`planning/phase-01-foundation.md` §4, Stage 1.3, "Architectural split").

## Contract

1. **Review text is `None` or empty/whitespace-only** → `FAIL_CLOSED`
   ("missing or failed review run"). *(Covers prompt 002's "missing or
   failed review" test case.)*
2. **Review text is not valid JSON** → `FAIL_CLOSED`, citing the parse
   error. *(Covers "malformed reviewer output.")*
3. **Parsed JSON is not an object**, or is an object missing any of
   `schema_version`, `pr_head_sha`, `status`, `findings` → `FAIL_CLOSED`,
   naming what's wrong. *(Covers "malformed reviewer output.")*
4. **`status` is not the literal string `"completed"`** → `FAIL_CLOSED`.
   *(Covers "missing or failed review" when the review process ran but
   errored rather than producing no file at all.)*
5. **`pr_head_sha` does not equal the actual current head SHA** passed
   in independently → `FAIL_CLOSED`, naming both SHAs. *(Covers "review
   of an outdated commit" — a passing review of an obsolete commit must
   not authorise a later unreviewed change, per prompt 002 §6 Stage 1.3.)*
   **Caller responsibility, found necessary by independent review:** this
   rule is only as meaningful as where `--actual-head-sha` comes from. A
   caller that sources it from the same event/trigger context used to
   produce the review document makes the comparison tautological — it
   must instead be obtained independently at evaluation time (e.g. a live
   GitHub API query for the PR's current head), so a replayed/re-run of a
   stale trigger is actually caught. `evaluate()` itself cannot enforce
   this — it only compares the two strings it's given — so this is a
   documented obligation on the integration
   (`.github/deferred/codex-review.yml` — deferred per `decisions/0005`
   and preserved as reusable material; this rule's logic is unaffected
   by where that workflow file lives),
   not something a unit test of the pure function alone can verify.
6. **`findings` is not a list, or any entry is not an object with a
   `severity` field** → `FAIL_CLOSED`, naming the bad entry. *(Covers
   "malformed reviewer output.")*
7. **Any finding's `severity` is `P0` or `P1`** → `BLOCK`, listing every
   blocking finding (not just the first) and every advisory finding
   found alongside them. *(Covers "known P0/P1 defect.")*
8. **No `P0`/`P1` findings, everything else above passed** → `PASS`,
   listing any advisory findings as recorded, non-blocking.
   *(Covers "valid PR" and "advisory finding" test cases.)*
9. **Output** is always a JSON object with `decision`, `reasons`,
   `blocking_findings`, `advisory_findings` — never bare text, so a
   workflow step can parse it mechanically rather than pattern-matching
   natural language.
10. **Exit code**: `0` for `PASS`, non-zero for `BLOCK` or `FAIL_CLOSED` —
    so a GitHub Actions step can gate on it directly.

## Non-goals

- Does not call any API, fetch any URL, or know how Codex was actually
  invoked — that is the live-integration piece, not this contract.
- Does not decide *how* findings are produced, only how a
  well/malformed/stale finding document is scored.
- Does not auto-dispose advisory findings beyond recording them —
  disposition (acknowledge, fix later, won't-fix) is a human/review
  action outside this module's scope.

## Ordering note

Unlike Stage 1.4, where `decisions/0004` (Amendment B) binds contracts to
be written and independently reviewed *before* implementation, Stage 1.3
carries no such explicit requirement in the amended plan — Amendment B's
anti-circularity mechanics are scoped to "this stage" meaning Stage 1.4's
self-development exercise specifically
(`planning/phase-01-foundation.md` §4, Stage 1.4). This contract was
written to match an already-written implementation
(`.github/scripts/policy_evaluator.py`), not before it. That ordering is
recorded here plainly rather than left implicit, so no later reader
mistakes this for a second instance of Stage 1.4's mandatory
contract-first discipline — and so this gap doesn't quietly become the
norm for every future component. The tests under
`.github/scripts/tests/` are checked against this contract's numbered
rules regardless of the order they were written in.
