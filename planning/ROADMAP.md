# Roadmap

What Axiom Dev is trying to achieve, long-term: find the simplest
practical methodology for AI-assisted software development that
preserves project knowledge, supports independent verification, keeps
documentation accurate as the system changes, and lets complex software
evolve reliably across disconnected agent sessions — see `README.md`
"Fundamental hypothesis." Phases below are the plan for testing that
hypothesis progressively, each building on verified evidence from the
one before, not on assumption.

Status values and what they mean here:

- **Proposed** — described in a plan or prompt, not yet reviewed/accepted.
- **Planned** — accepted in principle; dependencies and acceptance criteria
  recorded; no focused implementation plan written yet.
- **In progress** — a focused plan exists and work is underway.
- **Completed** — acceptance criteria met *with evidence*, confirmed by an
  independent closeout (`AGENTS.md` §6) and approved by a human
  (`AGENTS.md` §11). Writing the code/docs is not sufficient on its own.
- **Deferred** — intentionally not pursued now; reason recorded.
- **Blocked** — cannot proceed; blocker recorded.

This file is deliberately concise — it answers "what's the plan and
what's the current state," not "how did Phase 1 actually go." Detailed
implementation plans, stage-by-stage specs, independent review records
and evidence stay in their own files (linked below and from
`planning/CONTEXT.md`), not duplicated here. Once a phase is archived
(`docs/phase-archiving.md`), its roadmap entry shrinks to a short
summary and an archive link — this entry has not happened for any phase
yet (see "Archived phases" below).

## Overview

| Phase | Title | Status | Plan |
|---|---|---|---|
| 1 | Foundation | In progress | [`planning/phase-01-foundation.md`](phase-01-foundation.md) |
| 2 | Real-world validation | Proposed | *(not yet written — becomes actionable once authorised and planned, `AGENTS.md` §2)* |
| 3 | Methodology consolidation and reusable template | Proposed | *(not yet written)* |
| 4 | Broader validation and release | Proposed | *(not yet written)* |

Phases 2–4 are the long-term direction this project intends to pursue,
proposed by
`planning/prompts/004-documentation-schema-and-roadmap-amendment.md` §8
— **not authorised implementation commitments.** Each becomes actionable
only once its own focused plan is written, independently reviewed, and
approved (`AGENTS.md` §2), exactly like every phase before it. No dates,
measured benefits, or acceptance results are invented for any of them
below — only what each phase is *for* and what evidence would close it.

## Phase 1 — Foundation

**Status: In progress — not Completed.** Establishes and tests the
basic evidence-based development methodology: governance, knowledge
placement, documentation schemas, behavioural contracts, independent
review, deterministic CI, self-development, refactoring, and
documentation reconstruction. Full stage-by-stage detail, dependencies,
and acceptance criteria: [`planning/phase-01-foundation.md`](phase-01-foundation.md).

**Exit evidence required:** a working methodology, demonstrated through
real internal use (not synthetic fixtures alone), independent
verification of that use, and an accepted closeout. An independent
closeout assessment has run
(`evidence/phase-1-closeout.md`, `planning/phase-01-foundation.md` §16)
and found 15 of 17 original Definition-of-Done items met with evidence,
1 partially met, 1 genuinely blocked. A corrective amendment then fixed
documentation drift, strengthened the validator, completed deterministic
CI, and changed the independent-Codex-review requirement to native Codex
GitHub PR review (`decisions/0005`; `planning/phase-01-foundation.md`
§17–§20) — that batch's own revised 16-item Definition of Done
(§18) stands at 10 MET, 1 locally-verified-only, 5 open. A further
amendment moved documentation schemas to companion files and expanded
this roadmap itself (`decisions/0006`; §21–§22) — its own 21-item
Definition of Done (`planning/prompts/004-...md` §13) stands at 19 MET,
1 locally-verified-only, 2 open. **PR #1 exists and is open**
(<https://github.com/ctosullivan/axiom-dev/pull/1>) and has now had
**two native Codex reviews**: the first (on commit `3a8c395`) found 2
P2 findings — a fenced-code-block heading false positive and an
unhandled `TypeError` on malformed severity values — both corrected
with regression tests and independent verification (`decisions/0007`;
§23–§24). The second (on commit `2ebac4c`) found 1 further P2 finding
— a heading-whitespace false positive (`\s+` matching a newline between
a bare `#` marker and unrelated text on the next line) — also
corrected, with its own regression tests and independent verification
(§25–§26). **The remaining open items**: a *third* native Codex review
of the latest corrected commit has not been requested (no `gh`/token to
post the request from this session — confirmed repeatedly across three
amendments, not assumed), and human acceptance has not been sought.
See `evidence/phase-1-final-closeout.md` for the current full
acceptance matrix. Phase 1 cannot be marked Completed, merged, or
archived until a human requests that review, dispositions whatever it
finds, and reviews the result (`AGENTS.md` §11).

## Phase 2 — Real-world validation (proposed)

Apply the methodology to a substantive development task in an existing
project — Ledgerkit is the preferred candidate
(`planning/prompts/004-...md` §8). Potential activities: select a
bounded, meaningful Ledgerkit objective; establish an independently
reviewed behavioural contract; measure baseline development performance;
execute the work using Axiom Dev; compare against a simpler conventional
approach where a fair comparison is feasible; record defects, rework,
effort, verification coverage and knowledge reuse; evaluate whether
Axiom's procedures deliver value exceeding their overhead.

**Exit evidence required:** a credible, reproducible real-world
evaluation that distinguishes demonstrated improvements from unresolved
hypotheses — not a claim of superiority over alternative methods made
before that evidence exists.

## Phase 3 — Methodology consolidation and reusable template (proposed)

Refine the methodology based on Phase 2's actual findings. Potential
activities: remove procedures Phase 2 showed to be unnecessary; simplify
governance and documentation; consolidate reusable contracts, checks and
workflows; produce an Axiom Dev starter/template repository; demonstrate
that a fresh agent can use the template to develop and verify a bounded
change.

**Exit evidence required:** a reusable, documented development template
with a successful independent adoption exercise.

## Phase 4 — Broader validation and release (proposed)

Evaluate the methodology across additional projects and development
scenarios. Potential activities: cross-project trials; maintenance and
refactoring exercises; documentation reconstruction after substantial
change; comparison of verification approaches; usability/overhead
assessment; a versioned release of the methodology and template.

**Exit evidence required:** a stable release with documented
capabilities, limitations, and reproducible supporting evidence.

## Archived phases

None yet. **Phase 1 is not archived** — per
`planning/prompts/004-...md` §9's explicit restriction, it stays open
and un-archived until its outstanding requirements (native Codex GitHub
PR review, human acceptance) are met. See
[`docs/phase-archiving.md`](../docs/phase-archiving.md) for the
procedure that will apply once a phase is actually Completed, and
[`planning/archive/README.md`](archive/README.md) for the (currently
empty) archive index.
