# Session continuity

Keep this current, not historical. Historical narrative belongs in
`planning/retros/` and in commit/PR history.

## Current phase and status

**Phase 1: Stages 1.0, 1.1, 1.2, 1.4, 1.5 done with evidence; Stage
1.3's deterministic piece done with evidence and wired into CI. Six
amendments since the original closeout assessment**
(`planning/prompts/003`–`008`, `decisions/0005`–`0007`) **fixed
documentation drift, moved documentation schemas twice, expanded
`planning/ROADMAP.md`, established a phase-archiving procedure, and
corrected five real defects found across four native Codex GitHub
reviews of PR #1** — see `planning/phase-01-foundation.md` §17–§29.
**Phase 1 stays open, not marked Completed.** Everything is on
`phase-1/stage-1.0-bootstrap`, pushed. **PR #1 is open:**
<https://github.com/ctosullivan/axiom-dev/pull/1>, and has had
**four** native Codex reviews so far, all with findings this session
corrected (see Current branch / PR below). A **fifth** review, on the
latest corrected commit, has **not** run yet — this session cannot
trigger it (no `gh`/token) or merge anything; see Outstanding issues.

## Relevant decisions

`decisions/0001`–`0007`. `decisions/0005` partially supersedes
`decisions/0004`'s Stage 1.3 live-integration expectation.
`decisions/0006` moved schemas out of embedded front-matter into a
companion file; `decisions/0007` partially supersedes `0006`, moving
that companion file's *location* again into a mirrored `schemas/`
tree (`0006`'s decision to use a separate schema file *at all* is
unaffected). `decisions/0004`'s anti-circularity/measurement content
is otherwise unaffected and still governs Stages 1.1–1.5's evidence.
No new ADR was needed for any of the fourth or fifth Codex findings
(manifest integrity; absolute authoritative-source paths) — both were
implementation defects against already-correctly-specified contract
rules, not changed decisions.

## Outstanding issues (the real, named blockers)

1. **No `gh` CLI, GitHub token, or passwordless `sudo` to install
   either** — re-confirmed directly in this batch, not assumed. This
   session can commit and push to the existing branch, but cannot post
   a PR comment, trigger a Codex review, resolve a GitHub review
   thread, or merge.
2. **A fifth native Codex review of the latest corrected commit has
   not been requested or run.** `decisions/0005`'s requirement is for
   Codex to review the actual current commit, not one that already
   found findings since corrected. **Required human action:** comment
   `@codex review` on
   <https://github.com/ctosullivan/axiom-dev/pull/1> on the latest
   pushed commit, then report back what it finds.
3. **All five existing review threads' GitHub-side "Resolved" state
   cannot be confirmed or changed from this session** — no API/write
   access. Exact suggested reply text for each is in
   `planning/phase-01-foundation.md` §25 (findings A–C), §27 (finding
   D), and §29's follow-up (finding E) for the repository owner to
   post directly.
4. **Human acceptance of Phase 1 has not been sought or given.**
   `evidence/phase-1-final-closeout.md` (plus its addenda) records the
   current acceptance matrix and stops at "Ready for human
   acceptance." Marking Phase 1 Completed, merging PR #1, and
   archiving Phase 1 all require explicit human approval
   (`AGENTS.md` §11) after items 2–3 above are resolved.

None of these are shortcuts taken — each is a named, verified-real
external blocker or a human-approval boundary this project's own
governance reserves for a human.

## Recent human action

The repository owner pushed a commit directly to this branch on GitHub
(`ba9c592`, "docs: add evidence-based Codex review rules") adding
`AGENTS.md` §13. The owner (or the connected integration) also
triggered all four native Codex reviews on PR #1 directly on GitHub —
this is why findings existed for this session to fix each time;
confirmed by fetching the live PR page each time, not assumed (the
fetches have repeatedly returned truncated pages — see
`planning/phase-01-foundation.md` §25, §27, §29 for exactly what could
and could not be confirmed from each, and what this session verified
independently instead by reproducing each defect directly against the
actual code).

## Current branch / PR

- Branch: `phase-1/stage-1.0-bootstrap`, pushed to `origin`. Check
  `git log --oneline -1` for the exact current HEAD at read time —
  this file is updated same-commit as the work it describes, but
  always verify against `git log` rather than trusting a SHA frozen in
  prose (a lesson this project has now applied to itself more than
  once).
- PR: **open**, <https://github.com/ctosullivan/axiom-dev/pull/1>.
  - First native Codex review (commit `3a8c395`): 2 P2 findings
    (fenced-code-block heading false positive; policy-evaluator
    `TypeError` on malformed severity) — corrected at `162e5c6`,
    independently reviewed in §24.
  - Second native Codex review (commit `2ebac4c`): 1 further P2
    finding (heading-whitespace false positive) — corrected at
    `0645af3`, independently reviewed in §26.
  - Third native Codex review (commit `6e75d2b`): 1 further P2 finding
    (governed-document manifest not checked when a document's own
    schema exists) — corrected at `e0094f7`, independently reviewed in
    §28 (which also found and this session fixed a directory-as-manifest
    unhandled exception, and a brief documentation overclaim).
  - Fourth native Codex review (commit `10dd266`): 1 further P2
    finding (`check_authoritative_sources` wrongly accepting an
    absolute path to a file inside the repository) — corrected in this
    batch (§29); independent review dispatched.
  - Fifth review: not yet requested.
  - **GitHub Actions confirmed passing** across all 25 runs listed for
    this branch to date (fetched directly from the Actions run
    listing, not one spot-checked run) — zero failed or in-progress.

## Next concrete action

1. A human needs to: (a) comment `@codex review` on PR #1 to request a
   fifth native Codex review of the latest pushed commit; (b)
   disposition any findings it returns, and separately post the five
   prepared replies and close the five existing review threads on
   GitHub's own terms (this session can prepare reply text but cannot
   post it or see the actual "Resolved" state); (c) read
   `evidence/phase-1-final-closeout.md` and its addenda, and decide
   whether Phase 1 is ready to mark Completed; (d) if so, approve
   merging PR #1 — a human-approval action (`AGENTS.md` §11), never
   done unilaterally by this session.
2. Only after (a)–(d): a small follow-up PR completes the formal
   closeout (`planning/archive/phase-01/README.md`,
   `planning/ROADMAP.md` updated to Completed, this file updated to
   point at Phase 2 planning) — per `docs/phase-archiving.md`'s
   procedure and the two-step merge sequence this project has used
   since prompt 005 (remediation PR merged first, closeout PR second).
