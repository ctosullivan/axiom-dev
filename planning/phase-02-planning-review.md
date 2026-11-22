# Phase 2 planning — independent review and verification report

**Status: planning-only review, no implementation reviewed.** This is
deliverable G of the Phase 2 planning assignment: sources inspected,
decisions considered, review findings, unresolved issues, checks
actually performed, and matters requiring human approval. It also
serves as the provenance record several other Phase 2 planning
documents cite — a gap this file's own absence at first independent
review (see §3) was itself a BLOCKING finding, now closed by this
file existing.

## 1. Sources actually inspected (orchestrating session)

- `AGENTS.md`, `CLAUDE.md`, `planning/ROADMAP.md`, `planning/CONTEXT.md`
  (as they stood on `main` at commit `53d818b`, after fast-forwarding
  the local checkout — confirmed via `git fetch`/`git log` that `main`
  was 32 commits ahead of the prior session's last-known branch state,
  all already merged via PR #1/#2/#3, none unmerged).
- `decisions/0008-template-first-knowledge-identity-and-experiment-sequencing.md`,
  `planning/phase-02-template.md`, `planning/phase-02-roadmap-refinement.md`
  (full text, all three).
- `docs/knowledge-placement.md`, `docs/development-lifecycle.md`,
  `docs/agent-isolation.md`, `evidence/phase-1-owner-acceptance.md`,
  `evidence/schema-value-assessment.md` (full text).
- `schemas/governed-documents.txt` (confirmed none of the new Phase 2
  planning documents are governed/schema'd — they are ordinary
  planning prose under `planning/`, matching `phase-02-template.md`'s
  and `phase-02-roadmap-refinement.md`'s own, already-accepted status).
- PR state: confirmed via live fetch of
  `github.com/ctosullivan/axiom-dev/pulls?q=is%3Apr` that all three
  existing PRs (#1, #2, #3) are merged and none are open.
- `~/projects/ledgerkit` and `~/projects/hledger` — see §2.
- Claude Code's actually-documented capabilities — see §2.

## 2. Research dispatched and its provenance

### 2.1 Claude Code capability research

Dispatched to the `claude-code-guide` agent type (fresh context). 10
tool uses, 84,144 tokens, ~49s. Full findings (organised by the 7
questions asked):

1. **Project-local skills**: supported, documented
   (`code.claude.com/docs/en/skills.md`). Location
   `.claude/skills/<name>/SKILL.md`; personal skills in
   `~/.claude/skills/` win on a name clash. Invocation: both automatic
   (description-matching) and explicit `/<name>`;
   `disable-model-invocation`/`user-invocable` control this.
   Frontmatter fields: `name`, `description`, `when_to_use`,
   `argument-hint`, `arguments`, `disable-model-invocation`,
   `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`,
   `effort`, `context` (`fork`), `agent`, `background`, `hooks`,
   `paths`, `shell`; unknown fields ignored silently. Supporting files
   supported (relative links, `${CLAUDE_SKILL_DIR}`); keep SKILL.md
   under 500 lines. Subdirectory skills load lazily; parent-directory
   skills load at startup.
2. **Hooks**: supported, documented (`.../hooks.md`). 33 named events
   including `SessionStart`, `SessionEnd`, `PreToolUse`, `PostToolUse`,
   `PostToolUseFailure`, `SubagentStart`/`Stop`, `PreCompact`/
   `PostCompact`, and others. Common stdin JSON fields: `session_id`,
   `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`,
   `prompt_id`, `scratchpad_dir`, `effort`; `agent_id`/`agent_type` in
   subagents. `CLAUDE_PROJECT_DIR` env var documented; no session-ID
   env var documented. Deterministic file logging from a hook command
   is ordinary shell behaviour, confirmed possible. Blocking: exit 2
   blocks on events that support it (`PreToolUse`, `UserPromptSubmit`,
   `Stop`, `PreCompact`); `PostToolUse`/`SessionStart` only observe;
   `PreToolUse` can also return a structured `permissionDecision`.
3. **Skill invocation detection**: no dedicated "skill invoked" hook
   event exists. A `PreToolUse` hook matched on `Skill` fires when
   Claude invokes the Skill tool; the exact `tool_input` shape for that
   matcher was **not confirmed** from documentation alone. A user
   typing `/skill-name` bypasses `PreToolUse` and fires
   `UserPromptExpansion` instead. Skills can register their own
   frontmatter `hooks`.
4. **Tool-call information**: `PreToolUse` gives `tool_name`,
   `tool_input`, `tool_use_id`; `PostToolUse` gives `tool_response` and
   optional `duration_ms` (excludes permission-prompt wait time);
   `PostToolUseFailure` gives `error`, `is_interrupt`, `duration_ms`.
5. **Session identification**: `session_id` present in every hook's
   stdin JSON; no documented env var exposing it. `--session-id`,
   `--resume`, `--fork-session`, `/branch` affect it as documented; its
   behaviour across `/clear` and compaction specifically was **not**
   confirmed from documentation and is flagged as needing a build-time
   check, not assumed stable.
6. **Usage/cost telemetry**: `/usage` (interactive only) shows
   per-session tokens/cost. `claude -p --output-format json` (or the
   terminal message of `stream-json`) returns `session_id`,
   `total_cost_usd` and usage fields, programmatically — cost is a
   client-side, list-price estimate. Hooks do **not** receive cost/
   token fields. Transcript JSONL files exist but their format is
   documented as internal/version-unstable — not a supported
   integration point.
7. **OpenTelemetry**: supported
   (`.../monitoring-usage.md`), off by default
   (`CLAUDE_CODE_ENABLE_TELEMETRY=1`). Metrics:
   `claude_code.session.count`, `.cost.usage`, `.token.usage`,
   `.lines_of_code.count`, `.commit.count`, `.pull_request.count`,
   `.code_edit_tool.decision`, `.active_time.total`. Log events:
   `claude_code.tool_result`, `user_prompt`, `api_request`,
   `api_error`, `tool_decision`, others. Traces are beta/opt-in and
   unstable. **Correction recorded during independent review (§3,
   Material-Nonblocking #5):** only the `otlp` metrics exporter
   requires a standing collector endpoint; `console` and `prometheus`
   exporters do not. The decision to keep OTel optional and outside
   the Phase 2 minimum viable template (`planning/phase-02-measurement-design.md`
   §4) is unchanged, but for the corrected reason: a console-only
   export has little value as the *template's own default*
   instrumentation, not that a collector is unconditionally required.

Pages noted as partially truncated during this research: the hooks
reference's `PostToolUse`/`Skill`-matcher sections, the monitoring
page's full event list, and the CLI reference's cost-flag section —
flagged by the research agent itself as needing a re-check before
final reliance, not glossed over.

### 2.2 Ledgerkit/hledger inspection

Dispatched to a `general-purpose` agent (fresh context). 33 tool uses,
87,745 tokens, ~220s. Its claims were **not accepted at face value** —
the orchestrating session independently re-read
`ledgerkit/parser.py` lines 665–753 directly and independently
re-confirmed the regex defect and its consequence before relying on it
in `planning/phase-02-stage-2.1-plan.md`. The full candidate analysis
(three candidates, one recommended, two rejected with reasons) is
summarized in that plan's §1 and §8; the raw dispatch covered:

- Ledgerkit baseline: pure Python, `~/projects/ledgerkit`, HEAD
  `a7740fd04fe1814d2a557bfcb67a9a775a4a22f9`, 935/935 tests passing,
  version `1.0.0.dev1`, an existing `dev-docs/compat-register/` with
  49 entries and a documented YAML schema.
- hledger baseline: `~/projects/hledger` HEAD
  `33fa849e7ae841968bd21c427094c4fb4a4ec38d`; installed binary
  `~/.local/bin/hledger` reports version string
  `1.52.4-g33fa849e7-20260910`, whose git-describe suffix matches the
  checked-out HEAD SHA exactly.
- Candidate 1 (recommended, selected): EC-022, balance-assignment
  elision parsing. Candidate 2 (rejected): EC-021, directive-mid-block
  silent posting loss. Candidate 3 (rejected): an empty-alternation
  regex divergence already fully investigated by Ledgerkit's own prior
  process, offering less fresh evidence-gathering to dogfood.

## 3. Independent architectural review of the full planning package

Dispatched to a `general-purpose` agent (fresh context), after all
five Phase 2 planning documents and the `phase-02-template.md` edit
existed on disk (uncommitted, on branch
`planning/phase-2-stage-2.1-ledgerkit-oracle`). 39 tool uses, 122,145
tokens, ~310s.

**Independence actually achieved, in the reviewer's own words:**
"fresh context... no investment in this package's outcome... re-derived
every technical claim from the actual files/binaries/git histories
rather than trusting the plan's prose." **Independence NOT achieved:**
"same operator, same machine, and almost certainly the same underlying
model family... as whoever produced this planning package" —
best-effort, single-operator isolation (`docs/agent-isolation.md`
level 2), not organisational or model-diverse independence. Stated
honestly here rather than overclaimed, per this project's standing
practice.

### Findings and disposition

**BLOCKING 1 — `planning/phase-02-planning-review.md` cited as
existing in six places before it was ever written.** Confirmed real:
the file did not exist when five other documents already linked to it
in the present tense ("now exists," "is preserved in," "kept in").
**Disposition: fixed.** This file is that document, written
immediately upon the finding, with the actual research content (§2
above) and this review itself (§3) — closing every one of the six
dangling references. The reviewer is correct that nothing mechanical
caught this (the validator correctly `SKIPPED` all six files as
ungoverned planning prose); it was found only by a reviewer actually
attempting to open the link, which is itself a small, useful,
generalisable finding about this project's own review discipline.

**BLOCKING 2 — the generic Claim schema does not line up field-for-field
with the real compat-register it commits to reading, with no adapter
specified.** Confirmed real, checked directly against
`dev-docs/compat-register/schema.md`:

- The compat-register has **no `scope` field**, contradicting the
  generic schema's claim that scope is required for VERIFIED status.
- `ledgerkit.relationship` (`equivalent|superset|subset|incomparable`)
  is not the same vocabulary as the generic `mapping_result`
  (`equivalent|partial|divergent|unknown`), with no stated translation.
- `status` (`proposed|self-verified|verified|final`) is not the same
  vocabulary as Axiom's `INTENDED|OBSERVED|VERIFIED|UNCERTAIN|CONTESTED`,
  again with no stated translation — and critically, a naive
  word-association would wrongly treat `self-verified` as close to
  `VERIFIED`, when Ledgerkit's own rule (same-session evidence, not
  independently confirmed) means it must map to something *weaker*.
- A terminology inconsistency: `phase-02-stage-2.1-plan.md` §5 called
  the compat-register entry both "the authoritative claim" and "one of
  [the API's] `Source` kinds" — these are two different concepts in
  the API design's own three-concept vocabulary, not interchangeable.

**Disposition: fixed.** `planning/phase-02-knowledge-api-design.md`
now has an explicit "Reading an existing non-Axiom register" section
with: (a) a field-by-field mapping table for `relationship` →
`mapping_result` and `status` → Axiom's five-state taxonomy, including
the `self-verified → OBSERVED, not VERIFIED` rule stated explicitly as
a direct application of `AGENTS.md` §6's own circularity principle; (b)
an explicit disclosure that `scope` is **not present** in the source
register and is returned as absent/null rather than fabricated, with a
pointer to where a human would read `area`/`reason` manually instead;
(c) a statement that normalisation is additive — `get()` returns both
the common view and the original native fields losslessly, nothing is
discarded. `phase-02-stage-2.1-plan.md` §5 is corrected: the
compat-register entry is the **Claim**; its `upstream:` block is the
**Source**; its `evidence:` list is the **Evidence** — the erroneous
"Source kinds" phrasing is removed.

**MATERIAL-NONBLOCKING 3 — the Stage 2.4 drift-demonstration's
dependence on a *future* hledger commit landing during Phase 2 was
somewhat oversold; the three cited hledger commits all predate this
planning work, so they demonstrate the area churns, not that a new
relevant commit is guaranteed.** Confirmed real and correctly reasoned
by the reviewer. **Disposition: clarified, not a design change** —
`phase-02-stage-2.1-plan.md` §1 now states explicitly that
`planning/phase-02-template.md` §2.4's actual requirement is "a second
meaningful change," which can equally be a second Ledgerkit-side
change (e.g. EC-021, already identified as a rejected-but-viable
alternative) if no new relevant hledger commit lands in Phase 2's
timeline — the hledger-commit-churn evidence supports plausibility, it
is not treated as a guarantee.

**MATERIAL-NONBLOCKING 4 — planning-document volume (five new
documents, well over 1,000 lines) looks disproportionate to a
few-line eventual code fix.** Correctly observed. **Disposition:
acknowledged, not reduced** — the volume is a one-time cost covering
four cross-cutting designs (adoption, knowledge API, measurement,
architecture) that every subsequent Phase 2 stage reuses, not a
per-task cost that recurs at Stage 2.2's actual scale; this is
recorded as a judgement call this review surfaces rather than hides,
per the reviewer's own request. Future planning batches in Phase 2
should explicitly re-apply the complexity-budget self-check to their
own prose volume, not only to proposed infrastructure.

**MATERIAL-NONBLOCKING 5 — OTel collector-requirement framing
slightly overstated** (only the `otlp` exporter needs a standing
collector; `console`/`prometheus` do not). **Disposition: fixed** —
corrected in §2.1 above and in `planning/phase-02-measurement-design.md`
§4 directly.

**ADVISORY 6 — "reusing Ledgerkit's own existing rule" (for the
missing-`reason` CI check) could be misread as claiming Ledgerkit
already mechanically enforces it; it doesn't** (no CI workflow
validates the compat-register; the rule is a documented human
convention only). **Disposition: fixed** — wording changed to
"convention" in `planning/phase-02-knowledge-api-design.md` §6.

**ADVISORY 7 — the usefulness/repeated-investigation classifications
rest on one reviewer's subjective read with no inter-rater check.**
**Disposition: accepted as stated** — the measurement design already
discloses this is observational, not causal (§8 of
`planning/phase-02-measurement-design.md`); no mechanism change is
warranted in Phase 2, but this review's caution against treating the
resulting numbers as more rigorous than a single-rater judgement is
recorded here for whoever reads them later.

### Independently verified and found accurate (reviewer's own re-derivation, not trust in the plan)

- `ledgerkit/parser.py:673`'s regex and its consequence, exactly as
  described.
- Both failure-mode reproductions, re-run independently with matching
  output, including the exact Ledgerkit error string.
- The hledger binary-version-to-HEAD-SHA match.
- Ledgerkit's 935/935 test pass and `1.0.0.dev1` version.
- `knowledge/EDGE_CASES.md`'s EC-022 (and EC-021) content.
- `dev-docs/compat-register/schema.md`'s ID scheme, status tiers and
  non-destructive supersession mechanism (modulo the field-mismatch
  issue, now fixed above).
- The cited Claude Code hook/OTel facts (modulo the OTel nuance, now
  fixed above).
- A direct complexity comparison against `~/projects/codecompass`
  (~15,400 files, a database, an adapter/protocol layer) confirming
  the new design is genuinely, not just nominally, lighter.
- Every new document's explicit "Proposed design, not implemented"
  status line, and the validator's correct `SKIPPED` result for all
  six (none are governed/schema'd documents).

### What the reviewer did not check (disclosed limitations, carried forward)

- The claimed token/tool-use counts for the Ledgerkit/hledger research
  dispatch (unverifiable without this file, which did not yet exist at
  review time — resolved now that it does, §2.2).
- Fixture-matrix rows 4–8 of `phase-02-stage-2.1-plan.md` §3 (deferred
  to BUILD by that plan itself).
- `/usage`/`claude -p --output-format json`'s exact field names beyond
  what was spot-checked.
- `ROADMAP.md`'s/`knowledge/DECISIONS.md`'s full content beyond the
  cited entries, and Ledgerkit's `dev-docs/compat-register/examples/`.
- Solo-developer realism for the full six-stage Phase 2 roadmap beyond
  Stage 2.1's own proportionality.

### Quotable overall verdict (reviewer's own words, preserved verbatim)

> "The package's checkable factual claims about Ledgerkit and hledger
> — the regex bug, both failure-mode reproductions, the exact-commit
> oracle match, the existing compat-register's shape, and the Claude
> Code hook/OTel capability claims — all independently verified as
> accurate, which is unusually strong diligence for a planning
> document. But the package oversells its own completeness: it lists a
> review/provenance document as 'now existing' that was never created
> and is cited as a source of truth in five separate places, and its
> single most load-bearing design decision (deferring to Ledgerkit's
> compat-register) is specified against a generic claim schema that
> demonstrably does not line up field-for-field with the real register
> it commits to reading, with no adapter given. Fix those two things
> and this is a genuinely well-grounded, appropriately minimal design;
> as submitted, it is not yet the 'concrete enough for another agent to
> execute' artifact it claims to be."

Both BLOCKING findings are fixed in the same batch this file was
written in, per the disposition entries above.

## 4. Matters requiring human approval

Per `AGENTS.md` §11 and this assignment's §17: none of the planning
work in this batch requires human approval *to have been written* —
writing a plan is not itself the gated action. What **does** require
explicit human approval before proceeding, named here so it is not
missed:

1. **Review and acceptance of this whole planning package** —
   Stage 2.1's own plan, the adoption/API/measurement/architecture
   designs, and this review — before Stage 2.1 BUILD work starts
   (`AGENTS.md` §2, §11; `docs/development-lifecycle.md`'s SPECIFY exit
   criterion).
2. **Merging the planning-only PR** this batch is pushed under.
3. **Marking any Phase 2 stage Completed** in `planning/ROADMAP.md` —
   not proposed here; Phase 2 remains Planned.

No code was modified anywhere in this round (`~/projects/axiom-dev`,
`~/projects/ledgerkit`, `~/projects/hledger` are all unchanged except
this repository's own `planning/` documents). No A/B test of any kind
was performed or implied, consistent with ADR 0008.
