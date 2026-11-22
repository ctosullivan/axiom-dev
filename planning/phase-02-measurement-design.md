# Lightweight measurement design — logging, telemetry, usefulness classification

**Status: Proposed design, not implemented.** Answers this assignment's
§8/§9/§10/§16.E. Grounded in the `claude-code-guide` capability research
(full notes in `planning/phase-02-planning-review.md`'s provenance
section); every field below is either confirmed-available or explicitly
marked uncertain/to-verify-at-build-time, per that research's own
caveats.

## 1. JSONL event log

`.axiom-local/events.jsonl`, append-only, Git-ignored by default (added
to the consuming repository's `.gitignore` as part of adoption —
`planning/phase-02-adoption-design.md` §2).

### Common event fields (minimum event model, authorising prompt §8)

| Field | Source | Availability |
|---|---|---|
| `timestamp` | logger, at write time | always |
| `event_type` | logger | always |
| `session_id` | hook stdin JSON (`session_id`) | **confirmed available** on every hook event; behaviour across `/clear`/compaction not confirmed — do not assume stability across those without a build-time check |
| `task_id` | caller-supplied (e.g. a Stage-2.x identifier or claim ID being worked on) | **not natively provided by Claude Code** — this project must mint and pass it; see §2 |
| `git_revision` | `git rev-parse HEAD` at write time | always (shell, not a Claude Code feature) |
| `knowledge_id` | event-specific | present only on knowledge-operation events |
| `operation` | event-specific | present only on knowledge-operation/check events |
| `duration_ms` | hook stdin JSON (`PostToolUse`/`PostToolUseFailure`) | **confirmed available**, excludes permission-prompt wait time |
| `result` | event-specific | always, closed small vocabulary (`ok`/`error`/`fail`/`unknown`) |
| `error_class` | event-specific, derived from tool/CLI exit behaviour | present only on failure |
| `evidence_class` | logger, fixed per event type | always — see §3 |

**No invented fields.** Token counts, cost and model name are
deliberately **not** in this common event model — the capability
research confirms hooks do not receive cost/token fields; those come
from a separate source (§4), joined by `session_id`/`git_revision`
after the fact, not fabricated into the hook-based log.

### Event categories (evaluated against the authorising prompt's §8 table)

| Event | Built how | Confirmed source |
|---|---|---|
| `session_start` / `session_end` | `SessionStart`/`SessionEnd` hooks | confirmed hook events exist |
| `knowledge_get` / `knowledge_find` / `knowledge_impact` | the `axiom-knowledge` CLI itself appends its own event on exit — **not** inferred from a generic tool-use hook, since the CLI knows its own operation/result precisely and a hook would only see "a shell command ran" | CLI is Axiom's own code; most reliable source for these three |
| `test_result` | CI/local test-runner wrapper appends on exit (exit code + duration), or parsed from the test runner's own machine-readable output if one exists | shell/CI, not a Claude Code feature |
| `tool_failure` | `PostToolUseFailure` hook | confirmed hook event, confirmed fields (`error`, `is_interrupt`, `duration_ms`) |
| `claim_reconciled` | appended by whoever edits a claim file, via a small `axiom-knowledge reconcile-note` helper invoked as part of the commit, **not** inferred automatically from a Git diff (a file changing is not proof a claim was *reconciled* with evidence — that distinction matters per ADR 0008 Decision 5) | manual, deliberate append — matches "no autonomous semantic reconciliation" |
| `review_finding` | appended by the independent-review dispatch itself, or transcribed by the orchestrating session from the review's own report, naming the isolation level achieved | manual append, mirrors this project's existing practice (`docs/agent-isolation.md`) |
| `task_accepted` | appended once acceptance criteria are confirmed met, by whoever confirms it | manual append, matches `docs/development-lifecycle.md`'s phase-acceptance "who" column |

A skill-invocation event is **not** added as its own category: the
capability research found no dedicated "skill invoked" hook event, only
a `PreToolUse` hook matchable on the `Skill` tool, with the exact input
shape for that matcher unconfirmed. **Decision: do not build against
this until confirmed at implementation time** (authorising prompt's
explicit "do not invent unavailable telemetry fields"); Stage 2.2's
BUILD step confirms the matcher's actual payload shape before relying
on it, and if it turns out not to give a reliable signal, skill
activation is tracked only indirectly (a `knowledge_get`/`knowledge_find`
event firing is itself evidence the skill's guidance was followed,
whether or not the skill-invocation event itself is captured).

## 2. Task/session correlation

`task_id` has no native Claude Code source, so it must be **deliberately
assigned**: at the start of a bounded Axiom-guided unit of work, the
skill instructs recording a short, human-chosen task identifier (e.g.
`stage-2.1-ec022` or a claim ID being worked on) and every subsequent
`axiom-knowledge` CLI invocation and test-runner wrapper call takes it
as an explicit argument (`--task-id`), not inferred from context. This
is a deliberate, small piece of friction, accepted because inferring a
task boundary automatically (e.g. from a time gap or a branch name) would
be guessing, not measurement — and this assignment explicitly asks for
reproducible, non-invented correlation. `git_revision` plus `task_id`
plus `session_id` together let a report join "what happened, in which
session, for which task, against which code state" without needing any
of the three alone to be perfect.

## 3. Evidence class on every event

Per the authorising prompt's "Events should distinguish direct
measurements, externally reported results and independently reviewed
assessments": every event carries one of:

- `direct` — the logger observed this itself (a hook fired, the CLI's
  own exit code).
- `reported` — relayed from another tool's own output (a test runner's
  summary line, a CI job's conclusion) without independent
  re-execution by the logger.
- `reviewed` — a human/independent-agent assessment (`review_finding`,
  `claim_reconciled`'s underlying judgement, `task_accepted`).

This mirrors `docs/knowledge-placement.md`'s INTENDED/OBSERVED/VERIFIED
distinction at the *event* level rather than duplicating that
vocabulary, since an event is a record of something happening, not a
claim about project behaviour — using the same five-way taxonomy for
both would conflate two different kinds of statement.

## 4. Existing telemetry reuse (confirmed capabilities only)

- **Interactive usage:** `/usage` shows per-session token counts and
  cost — confirmed, but interactive-only; not usable from a hook or
  script.
- **Programmatic cost/usage:** `claude -p --output-format json` (or
  `stream-json`'s terminal `result` message) returns `session_id`,
  `total_cost_usd` and usage fields — confirmed, and this **is** usable
  from CI or a wrapper script, joined to the event log by `session_id`.
  This is the source for cost/token figures in any Phase 2 report, not
  the hook-based event log, which does not carry them.
- **OpenTelemetry:** confirmed supported, off by default
  (`CLAUDE_CODE_ENABLE_TELEMETRY=1`), exporting
  `claude_code.session.count`, `.cost.usage`, `.token.usage`,
  `.lines_of_code.count`, `.commit.count`, `.pull_request.count`,
  `.code_edit_tool.decision`, `.active_time.total` as metrics, plus
  `claude_code.tool_result`/`user_prompt`/`api_request`/`api_error`/
  `tool_decision` as log events. **Correction, found by independent
  review (`planning/phase-02-planning-review.md` §3,
  Material-Nonblocking 5):** only the `otlp` metrics/logs exporter
  requires a standing collector endpoint — the `console` and
  `prometheus` exporters do not. The decision below is unchanged, for
  the corrected reason: a `console`-only export has little value as
  the template's own *default* instrumentation (it's a local printout,
  not a report), and requiring a consumer to stand up `otlp`/a
  collector merely to get Phase 2's minimum data would be exactly the
  "custom distributed tracing infrastructure" this assignment's §14
  challenges. **Decision: OTel is documented as an optional enhancement
  for a consumer who already runs a collector (or wants `console`
  output for their own ad hoc use) — not part of the Phase 2 minimum
  viable template.** Traces are beta/opt-in and are not relied on at
  all.
- **Not reliably inferable from any available trace**: exact per-tool
  latency broken down by *which* knowledge operation triggered it
  (available only if the CLI logs its own duration, which it does, per
  §1); any causal attribution of "this tool call happened because of
  that skill activation" beyond the unconfirmed `Skill` matcher.

## 5. Privacy, retention, opt-out, failure behaviour

- **Redaction:** no full prompts, conversation text, tool arguments,
  file contents, or credentials are logged by default — only the
  structured fields in §1. A `tool_failure` event's `error` field is
  the tool's own error string, which could in principle contain a
  file path or similar; this is accepted as a known, bounded exposure
  (consistent with what `PostToolUseFailure` already surfaces to the
  session itself) rather than attempting content-scanning redaction,
  which would be exactly the kind of "large observability platform"
  this assignment's §8 explicitly rejects. A consumer with stricter
  needs can wrap the hook command with their own filter — not Axiom's
  concern to solve generically before any real need is shown.
- **Retention:** `.axiom-local/` is Git-ignored, so it never enters
  history; retention is whatever the local filesystem does, with no
  default rotation. A future `axiom-knowledge log-rotate` helper is
  deferred until a real file-size problem is observed (§14 complexity
  budget).
- **Opt-out:** removing or not installing the hooks is sufficient — no
  separate "logging enabled" flag is needed when the mechanism is
  "a hook command either exists in `.claude/settings.json` or it
  doesn't."
- **Logging-failure behaviour:** every logging hook command is
  non-blocking (no `exit 2`, no `onFailure: block`) — a failure to
  write the JSONL file (disk full, permissions) must never stop
  ordinary development, per the authorising prompt's explicit
  instruction. A hook write failure is swallowed by the hook command
  itself (`... >> events.jsonl 2>/dev/null || true`), not surfaced as a
  blocking error.

## 6. Knowledge usefulness classification (authorising prompt §10)

At the end of each substantive task, an **independent reviewer** (not
the implementing agent/session) classifies each piece of knowledge
actually encountered during that task as:

| Classification | Required evidence reference |
|---|---|
| Useful | the specific decision/verification step it materially supported, cited by claim ID and what it changed about the outcome |
| Redundant | what readily-accessible source/doc would have given the same information at similar cost |
| Misleading | the specific way it was wrong/stale/misapplied, and what the correct state turned out to be |
| Missing | the gap — what question came up with no discoverable existing claim |

This is **recorded as a `review_finding`-category event** (§1) plus a
short free-text justification, not a separate database — a small
Python script reading the JSONL log and the claim files produces a
CSV/Markdown table per task. **No dashboard is built** — the
authorising prompt explicitly defers one until real use demonstrates
it's warranted, and nothing here needs live/interactive presentation to
be useful as a reviewed table.

## 7. Scorecard (authorising prompt §9)

Per Ledgerkit development task, the report (same small script, §6)
computes:

- **A. Knowledge reuse**: count of `knowledge_get`/`knowledge_find`
  events for that `task_id` whose result was *cited in the task's own
  BUILD or VERIFY output* (a manual, reviewed judgement — retrieval
  alone, per the authorising prompt, does not establish usefulness;
  the report distinguishes "retrieved" from "retrieved and used," the
  second requiring the reviewer's note from §6).
- **B. Repeated investigation**: a reviewer-classified count of
  instances where the task's own session log shows re-deriving
  something a `VERIFIED` claim already stated — **a reproducible
  classification method, not "every repeated search counts"**: a
  repeated search only counts if (a) a relevant `VERIFIED` claim
  existed and was retrievable via `find()` at the time, and (b) the
  session's own transcript or event log shows exploration that
  re-derives the same fact rather than applying it. Both conditions are
  checked by the reviewer against the actual event log and transcript,
  not inferred from search-count alone.
- **C. Verified task correctness**: result of the independent
  behavioural contract/oracle check (Stage 2.1's acceptance criteria,
  generalised) — defects found, rework required, unresolved
  uncertainty, each cited to a `review_finding` event.
- **D. Drift detection effectiveness**: for a task that followed a
  relevant source change, count of claims `impacted()` correctly
  flagged versus claims a reviewer independently judges *should* have
  been flagged but weren't (false negative) versus flagged-but-judged-
  irrelevant (false positive) — all three counted explicitly, not
  collapsed into one "accuracy" number.
- **E. Operational overhead**: wall-clock time, `axiom-knowledge`
  invocation count, and (from §4's programmatic cost source, joined by
  `session_id`) token/cost figures where available, for creating,
  retrieving, verifying and reconciling knowledge on that task.
- **F. Adoption effort**: for Stage 2.6 specifically — setup steps
  required, modifications needed beyond template copy, and whether a
  fresh agent/developer succeeded without project-specific tutoring.

Every one of these is **predeclared before Stage 2.4's dogfooding
produces outcomes** (per the authorising prompt's explicit "predeclare
evaluation questions... do not select or revise success criteria after
seeing results"), not retrofitted to whatever numbers happen to look
good.

## 8. Limitations of this observational evidence (authorising prompt §11)

This logging and scorecard design supports **observation**, not
controlled experimentation: it can show that a specific retrieval was
used, that a specific drift was caught or missed, and what a specific
task cost — but it cannot and does not claim that Axiom caused a better
outcome than an ungoverned alternative would have on the same task,
since no comparable ungoverned run of the same task is performed in
Phase 2. Phase 3's Assure-backed experiments are the only place such a
comparison is planned, with held-out tasks and controlled conditions
this logging design does not attempt to provide. Task/session/claim
identifiers are kept stable and joinable (`task_id`, `session_id`,
`git_revision`, claim IDs) specifically so a future Phase 3 experiment
*can* relate back to Phase 2 records without requiring a new
telemetry platform to be retrofitted first — this is the one place
Phase 2's design deliberately looks ahead, without building anything
Phase 3-specific now.
