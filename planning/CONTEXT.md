# Session continuity

Keep this current, not historical. Historical narrative belongs in
`planning/retros/` and in commit/PR history.

## Current phase and status

**Phase 1: Stages 1.0, 1.1, 1.2, 1.4, 1.5 done with evidence; Stage
1.3's deterministic piece done with evidence, now also wired into CI.
A corrective-amendment pass (`planning/prompts/003-...md`,
`decisions/0005`) fixed documentation drift, strengthened the validator's
schema checks, completed deterministic CI, and changed Phase 1's
independent-Codex-review requirement to native Codex GitHub PR review —
see `planning/phase-01-foundation.md` §17–§20. A further amendment
(`planning/prompts/004-...md`, `decisions/0006`) moved every governed
document's schema out of embedded front-matter into a companion
`<doc>.md.schema.yaml` file, adapted the validator accordingly, expanded
`planning/ROADMAP.md` into a concise multi-phase roadmap (Phases 2–4
proposed, not authorised), and established (but did not use) a
phase-archiving procedure — see §21–§22. Phase 1 stays open, not marked
Completed; nothing in either amendment closes the one real remaining
gap below.** Everything is on `phase-1/stage-1.0-bootstrap`, pushed,
unmerged (no PR opened — no `gh`/token, re-confirmed again in the
prompt 004 batch, not merely carried forward from an earlier check).

## Relevant decisions

`decisions/0001`–`0006`. `decisions/0005` **partially supersedes**
`decisions/0004`'s Stage 1.3 live-integration expectation;
`decisions/0006` supersedes `docs/documentation-schema.md`'s prior
front-matter-vs-sidecar resolution of `decisions/0002`'s Unresolved item
(not `decisions/0002` itself, which made no commitment either way).
`decisions/0004`'s anti-circularity/measurement/demonstration content is
otherwise unaffected and still governs Stages 1.1–1.5's evidence.

## Outstanding issues (the real, named blockers)

1. **No `gh` CLI or GitHub token** — no PR has ever been opened for any
   work on this branch. A human needs to open it from the URL below.
   This is now the blocker for native Codex GitHub PR review too (not
   only for a human to read the diff) — see item 2.
2. **Native Codex GitHub PR review (the current Phase 1 requirement,
   per `decisions/0005`) has not been performed** — it needs an actual
   opened PR to review, which this session cannot create (item 1). This
   is a different, narrower gap than the one this file used to describe:
   `decisions/0005` is explicit that an `OPENAI_API_KEY` and GitHub
   required-status-check configuration are **no longer Phase 1
   requirements at all** — do not treat provisioning either of those as
   a remaining step.
3. Because of (1)/(2), **no real GitHub PR has ever existed, let alone
   been reviewed** — `planning/phase-01-foundation.md` §18's DoD items
   10–12 and the corresponding Amendment D (`decisions/0004`) row stay
   open. This is the one genuine, currently-irresolvable-from-here gap
   in Phase 1.

None of these are shortcuts taken — each is a named, verified-real
external blocker, re-confirmed directly in this corrective pass (not
taken on a prior session's word).

## Recent human action

The repository owner pushed a commit directly to this branch on GitHub
(`ba9c592`, "docs: add evidence-based Codex review rules") adding
`AGENTS.md` §13 — explicit review priorities and finding-report shape
for native Codex PR review (contract integrity, verification
independence, knowledge/documentation integrity, enforcement/failure
behaviour), reiterating `decisions/0005`'s "advisory, not a mechanical
gate" framing. Merged cleanly into this branch (`033dfe6`), no conflicts
— this session's prompt 004 batch did not touch `AGENTS.md`. This is
real engagement from the human on the native-Codex-review setup, but it
does not by itself mean a PR now exists; this session has no way to
query GitHub's API to check (no `gh`/token, confirmed again).

## Current branch / PR

- Branch: `phase-1/stage-1.0-bootstrap`, pushed to `origin`. Check
  `git log --oneline -1` for the exact current HEAD at read time — this
  file is updated same-commit as the work it describes, but always
  verify against `git log` rather than trusting a SHA frozen in prose.
- PR: still not opened. Creation URL:
  `https://github.com/ctosullivan/axiom-dev/pull/new/phase-1/stage-1.0-bootstrap`
- Once opened, request native Codex review with `@codex review` as a PR
  comment (or the connected Codex GitHub integration's equivalent
  trigger) — see `decisions/0005` and
  `planning/phase-01-foundation.md` §17 Amendment A.

## Next concrete action

1. A human needs to: (a) open the PR from the URL above and request
   native Codex review (`@codex review`); (b) disposition any P0/P1
   Codex findings (resolve or explicitly accept/escalate) and record the
   reviewed commit + findings in `planning/phase-01-foundation.md`;
   (c) decide, stage by stage, what to mark Completed in
   `planning/ROADMAP.md` given the evidence — a human-approval action
   (`AGENTS.md` §11), not something this session does unilaterally.
   **Provisioning `OPENAI_API_KEY` or configuring branch protection is
   not part of this list** — `decisions/0005` removed both as Phase 1
   requirements.
2. Only after (a)/(b): Phase 1 can be reassessed for full completion.
   Everything else is already done with evidence.
