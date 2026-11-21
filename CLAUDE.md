# CLAUDE.md — Claude Code adaptations

`AGENTS.md` is canonical for Axiom Dev's development methodology. This file
holds only the adaptations specific to running Claude Code against this
repository. If anything here appears to conflict with `AGENTS.md`,
`AGENTS.md` wins — treat the conflict as a bug in this file.

## Commit and session attribution

Claude Code sessions working in this repository add attribution lines to
commits and PR descriptions as instructed by the operating environment at
the time (model name/co-author line, session link where applicable). This
is a session/tooling-level convention, not an Axiom Dev project decision —
it can vary by how the session was launched, and `AGENTS.md` §9's
commit/PR conventions apply in addition to, not instead of, it.

This is a deliberate departure from CodeCompass precedent, which fixed "no
AI attribution in commits, ever" as project policy
(`codecompass/decisions/0007-no-claude-attribution-in-commits.md`). Axiom
Dev has not adopted that policy; the divergence is recorded here rather
than silently inherited or silently dropped. If Axiom Dev later wants a
fixed project-level policy on this (rather than deferring to session
convention), that is a real decision and should get its own ADR.

## Planning and ADR discipline

Follow `AGENTS.md` §1–§3 exactly: write a plan before implementing,
restrict ADRs to genuinely non-obvious decisions, and never edit an
accepted ADR in place — supersede it. Claude Code's tendency to move fast
and summarize confidently is exactly the failure mode `AGENTS.md` §6 is
written against: an agent's own summary is not verification evidence.

## Scope discipline

When working a Phase 1 stage, implement only what that stage's focused plan
(`planning/phase-01-foundation.md` plus any stage-specific plan it points
to) authorises. Do not pull forward work from a later stage because it
would be convenient to do now, and do not create directories or files for
future stages before they have real content — see `README.md`'s repository
map for which directories are intentionally absent and why.

## Independent review requests

When asked to dispatch an "independent" review or verification pass within
a single Claude Code session, be explicit in the resulting report about
what independence was actually achieved (fresh context, no shared
investment in the outcome) versus what was not (same operator, same
session, same underlying model). See `AGENTS.md` §6.
