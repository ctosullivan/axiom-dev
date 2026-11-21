# Claude Code instructions

`AGENTS.md` is the canonical development methodology and approval policy.
Read it and `planning/CONTEXT.md` before making changes. Do not duplicate
or override those rules here.

- At session start, inspect the actual branch, diff, current plan and
  implementation; do not trust a prior session's summary as evidence.
- Use Claude Code's planning and agent tools to support the lifecycle in
  `AGENTS.md`, not to bypass its contract-first or approval steps.
- When delegating a review, disclose the achieved isolation level.
  A fresh subagent in one session is **not** independent by default.
- Run deterministic checks and inspect their results. Report any tests or
  reviews not executed; never infer a pass from generated text.
- Preserve provenance for externally sourced claims. Keep changes scoped
  to an authorised focused plan, and reconcile affected documents in
  the same PR.
- For commits, PRs, and model/session attribution, comply with
  `AGENTS.md` and applicable Claude Code session/tooling requirements;
  do not invent extra repository-wide attribution rules.

Current work and next step: `planning/CONTEXT.md`.
Phase sequence: `planning/ROADMAP.md`.
