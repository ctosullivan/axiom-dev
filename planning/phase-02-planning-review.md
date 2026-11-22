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

## 5. Corrective-review addendum (planning amendment)

Preserving everything above exactly as written — this section records
a later amendment to the planning package, not a rewrite of what §1–4
found or concluded at the time. Where this addendum says an earlier
finding was "corrected," the original finding entry above is left
intact; only the planning documents themselves changed.

### 5.1 What prompted this amendment

A follow-up authorising prompt reviewed the planning package
independently of this file's own §3 review and identified further
defects not caught there: a Stage 2.1/2.4 sequencing overlap (Stage
2.1's plan included fix-implementation and regression-testing
requirements that belong to Stage 2.4); a knowledge-adapter design
that, even after §3's BLOCKING-2 fix, still risked overstating
Ledgerkit's native verification tiers in two specific ways; an
`impacted()` contract that treated a legitimate source deletion as a
malformed request; a drift demonstration dependent on an unpredictable
future event; a measurement design that didn't clearly separate skill
activation from knowledge use from assessed usefulness, and defaulted
to logging raw error strings rather than a safe classification; and a
planning-document volume this file's own §3 (Material-Nonblocking 4)
had already flagged without resolving.

### 5.2 Corrections made

1. **Stage 2.1/2.4 sequencing** — `planning/phase-02-stage-2.1-plan.md`
   rewritten: Stage 2.1 now ends at the reviewed contract, pinned
   oracle and a **fully captured** fixture matrix (all 9 rows run
   against the live hledger binary in this revision, not deferred to
   BUILD); a new explicit "Handoff to Stage 2.4" section carries every
   fix-implementation, regression-test, independent-verification and
   compat-register acceptance criterion that an earlier draft had
   misplaced in Stage 2.1.
2. **A genuinely new scope finding, surfaced by actually capturing the
   full fixture matrix** (not something either prior research or
   review agent had found): hledger's true balance-assignment
   semantics resolve an elided amount against the account's full
   *running balance* across the journal, not merely the net of
   sibling postings in the same transaction — confirmed directly with
   a two-transaction fixture. Ledgerkit's existing `resolve_elision()`
   (`ledgerkit/parser.py:816–869`, read in full) only ever had access
   to one transaction's own postings, so it structurally cannot
   provide this. This is now fixture row 9 and an explicit, named
   scope boundary — EC-022's fix is scoped to the single-transaction
   case; the cross-transaction case is a required *disposition*, not
   a required pass, so a future fix cannot silently diverge from
   hledger here without anyone having decided that was acceptable.
3. **Knowledge-adapter conservatism** — `planning/phase-02-knowledge-api-design.md`
   §3a–§3e rewritten: `native` and `derived` fields are now kept
   visibly separate (not merged into one record as the prior revision
   did); `proposed` now maps to `UNCERTAIN` rather than `OBSERVED`
   (Ledgerkit's own schema note says no execution has happened yet —
   the prior mapping overstated it); `verified`/`final` now require
   `verified_by`/`verified_date` to actually be present on the native
   record, mapping to `CONTESTED` otherwise, rather than trusting the
   native `status` string alone; reviewer metadata is now mapped from
   its real location (top-level `verified_by`/`verified_date` on the
   register entry) instead of an assumed-but-never-checked
   `evidence[].reviewed_by`; a present reviewer name is now explicitly
   stated to satisfy only the mechanical precondition, not to prove
   actual independence; `superset`/`subset` relationships now carry a
   required `mapping_scope` string rather than collapsing silently
   into an unqualified `equivalent`/`partial`.
4. **`impacted()` redesigned** — now takes Git-derived change records
   (`base`/`head`/`path`/`change_type`/`old_path`) rather than bare
   paths; `deleted` and `renamed` are legitimate, explicitly handled
   change types, not malformed requests; a rename preserves the
   ability to find claims referencing the old path. 9 new contract
   tests added (modification, deletion, rename, evidence-file
   deletion, relevant/irrelevant/unrelated source changes, invalid
   spec, empty list).
5. **Drift demonstration no longer depends on an unpredictable future
   event** — `planning/phase-02-stage-2.1-plan.md` §6.2 now specifies
   two controlled conditions for Stage 2.4: a relevant change (EC-021,
   or a genuinely new relevant hledger commit if one has landed by
   then) expected to flag the EC-022 claim, and a deliberately
   unrelated change expected not to — both outcomes recorded,
   including any false positive/negative, rather than one success
   case standing in for the whole mechanism.
6. **Measurement design corrected** — `planning/phase-02-measurement-design.md`
   §0 (new) explicitly distinguishes skill activation, API invocation,
   retrieval, actual use, correct application, independently assessed
   usefulness, and verified outcome, and states which of these each
   metric in §7 actually measures. A `task_start` event is added as
   the explicit, deliberate task-boundary marker the authorising
   prompt asked for. Default error logging changed from the raw
   `error` string to a small closed `error_class` classification,
   opt-in only for the raw string.
7. **Planning volume** — `planning/phase-02-architecture.md` (139
   lines) merged into `planning/phase-02-adoption-design.md` as its
   §9, removing one standalone file that existed only to diagram what
   the adoption design already specified in prose.
   `planning/phase-02-template.md` gained an explicit "Document map
   and navigation path" section stating the actual minimum reading
   order to execute a stage, rather than leaving a reader to infer it
   from six same-weighted links.

### 5.3 What remains open or unresolved

- The planning package is still substantial in total (now six
  documents, not five, after this amendment's own additions — the
  reduction was in redundant cross-referencing and one merged file,
  not raw line count, since most of the growth is genuinely new,
  requested correction content, not padding). Whether this is still
  disproportionate to Stage 2.1's own scope remains a judgement call
  for the human reviewer, not resolved by assertion here.
- `mapping_scope`'s exact wording (§3c of the knowledge-api design) is
  illustrative; the precise phrasing a real implementation uses is
  BUILD-phase work.
- The `Skill`-tool `PreToolUse` matcher's actual payload shape is
  still unconfirmed — unchanged from the original capability research;
  this amendment did not re-attempt that check.
- Whether EC-021 (the Stage 2.4 relevant-change candidate) still
  applies by the time Stage 2.4 actually runs depends on Ledgerkit's
  own state at that time, which this amendment cannot freeze in
  advance — `planning/phase-02-stage-2.1-plan.md` §6.2 names this
  explicitly rather than treating EC-021 as a guaranteed fixture.

### 5.4 Fresh independent review of this amendment

A second, separately-dispatched fresh-context review of the amended
package is recorded in §6 below, checking the actual revised files,
not this addendum's own account of them. **Note on this very
sentence:** an earlier version of this paragraph said that review
"follows below" while §6 did not yet exist — the dispatched reviewer
caught this as its own BLOCKING finding (§6, Blocking 1), the exact
same defect class (a document asserting another document's content
exists before it was written) as this file's original BLOCKING 1 in
§3. Recorded honestly rather than quietly corrected without a trace,
per this project's own standing practice.

## 6. Second independent review (of the corrective amendment itself)

Dispatched to a `general-purpose` agent (fresh context), after all
amendment-round edits existed on disk.

**Isolation achieved, in the reviewer's own words:** "Fresh context:
yes — no prior turns, no memory of earlier rounds, no investment in
this package's outcome... built my own two-transaction and spot-check
fixtures from scratch... different account names/amounts/commodities
than the plan's own examples." **Not achieved:** "same operator/
machine, and almost certainly the same underlying model family as
whoever wrote this package and its own two prior 'independent'
reviews... best-effort, single-operator isolation
(`docs/agent-isolation.md` level 2), not organisational or
model-diverse independence."

### BLOCKING 1 — the addendum cited a review section ("§6... follows
below") that did not exist when it was written

Confirmed real by the reviewer: `wc -l` showed the file ending before
any §6, while §5.4's text asserted the review "follows below." The
reviewer noted this is the exact same defect class as the original
BLOCKING 1 (§3 above) — a document asserting another document's
content exists before it does — now recurring inside the very file
meant to catch that pattern. **Disposition: fixed** — this section
(§6) is that review, and §5.4's text above now records the finding
explicitly rather than silently patching the dangling reference.

### Independently re-verified and found accurate

- Ledgerkit HEAD `a7740fd04fe1814d2a557bfcb67a9a775a4a22f9` (clean
  tree) and hledger HEAD `33fa849e7ae841968bd21c427094c4fb4a4ec38d`,
  confirmed matching the installed binary's version string exactly, as
  in every prior round.
- **The row-9 running-balance claim, re-derived with the reviewer's
  own, independently constructed fixture** (different accounts,
  amounts and commodity from this plan's own example — `assets:checking`/
  `equity:opening`/`income:misc`, USD, $200→$350): confirmed `income:misc`
  resolves to `-150.00 USD` (`350 − 200`, not `350`), independently
  proving hledger resolves a balance assignment against the account's
  running balance, not the asserted figure outright. `resolve_elision()`
  (`ledgerkit/parser.py:816–869`) read directly by the reviewer and
  confirmed to take only a single `Transaction`, with no access to
  prior history — the claim that it structurally cannot provide
  cross-transaction resolution is independently confirmed, not merely
  re-asserted.
- Fixture rows 1, 7, 8 spot-checked with the reviewer's own fresh
  journals (different values throughout) — all matched the plan's
  claimed hledger behaviour, including the exact error text for rows
  7/8.
- `dev-docs/compat-register/schema.md` read in full a second time,
  independently: `verified_by`/`verified_date` confirmed top-level
  (schema lines 72–73, not nested in `evidence[]`); no `scope` field
  anywhere in the schema; `relationship` enum confirmed exactly
  `equivalent | superset | subset | incomparable`; `status` enum
  confirmed exactly `proposed | self-verified | verified | final`,
  with the schema's own comment on `proposed` ("not yet run against
  the real binary") directly supporting the corrected `proposed →
  UNCERTAIN` mapping.
- **Stage 2.1/2.4 split confirmed clean**: "`phase-02-stage-2.1-plan.md`
  §5 explicitly states Stage 2.1 does not require EC-022 fixed, any
  regression test, or independent verification of a fix... no
  contradiction between the two documents" (stage plan vs. master
  plan's §2.4).
- Native-status mapping (§3b) independently confirmed conservative,
  with the `verified`/`final → VERIFIED` conditional on
  `verified_by`/`verified_date` both present, `CONTESTED` as the
  fallback, backed by an actual contract test.
- `mapping_scope` confirmed actually required (not aspirational), with
  a real contract test for its presence/absence.
- `impacted()`'s redesign confirmed sound: Git-derived change records,
  `deleted`/`renamed` handled as legitimate, all 9 claimed regression
  fixtures present, no remaining path where a legitimate deletion is
  treated as an error.
- Stage 2.4's two-condition drift design confirmed genuinely
  two-sided, resolving the original Material-Nonblocking 3 finding.
- Measurement design's §0/§5/§7 confirmed mutually consistent — no
  inconsistency found between the common-fields table, the
  event-categories table and the privacy section on default error
  logging.
- `planning/phase-02-architecture.md` confirmed actually gone (not
  merely described as gone), its content confirmed present in
  `phase-02-adoption-design.md` §9, and no remaining document treats
  it as live.
- `decisions/0008` confirmed unmodified (zero diff).
- `planning/phase-02-planning-review.md` §1–§4 (the first review)
  confirmed byte-for-byte preserved (126 insertions, 0 deletions in
  this file's revision) — not retroactively rewritten to look
  flawless.

### ADVISORY

- No `CHANGELOG.md` entry existed yet for this round's corrections at
  review time. **Disposition: fixed** — see `CHANGELOG.md`'s new entry
  for this amendment.
- §5.4's dangling sentence — see BLOCKING 1's disposition above.

### What the reviewer did not check

Fixture rows 2–6 beyond the 1/7/8/9 spot-check; the `Skill`-tool
`PreToolUse` matcher's payload shape (still unconfirmed, build-time
work); `dev-docs/compat-register/examples/`; Ledgerkit's or hledger's
own test suites; solo-developer realism for the full six-stage roadmap
beyond Stage 2.1's own scope. No files anywhere were modified.

### Quotable verdict

> "This amendment's substantive engineering corrections — the Stage
> 2.1/2.4 split, the conservative native-status/relationship mappings
> backed by real contract tests, the Git-change-record redesign of
> `impacted()`, the two-condition drift design, and the measurement
> design's seven-way distinction — all independently re-verified as
> accurate against the real hledger binary, the real Ledgerkit source,
> and the real compat-register schema, including with fixtures I
> constructed myself rather than reusing the plan's own. But the
> package repeats, inside the very file meant to be its own honesty
> mechanism, the precise failure its first review called BLOCKING:
> `planning/phase-02-planning-review.md` §5.4 asserts a second
> independent review 'follows below' at a §6 that was never written.
> Until that sentence is fixed or a real §6 exists, the corrective
> round described as 'just completed, not yet independently reviewed'
> is — accurately, if unintentionally — still unreviewed by the
> document's own account of itself, and this report is the first such
> review to actually exist."

Both the BLOCKING finding and the ADVISORY notes are fixed in the same
batch this section was written in.

## 7. Final-amendment addendum (AMEND phase of the Phase 2 final amendment/implementation assignment)

Preserving everything above exactly as written. A follow-up authorising
prompt ("Phase 2 Final Amendment, Verification and Implementation")
identified further defects not caught by §1–6, specifically in the
knowledge-adapter's scoped-verification invariant, native dependency
extraction for `impacted()`, native-vs-generic validation conflation,
durability of the oracle evidence, and the drift demonstration's
dependency rationale. This section records what was corrected.

### 7.1 Corrections made

1. **Scoped-verification invariant fixed.** The prior revision could
   produce `derived.status: VERIFIED` together with `derived.scope:
   null` — a direct contradiction of `docs/knowledge-placement.md`'s
   own, already-accepted definition of VERIFIED ("within a stated
   scope"). Fixed with a new scope gate (`planning/phase-02-knowledge-api-design.md`
   §3b.1): an optional, small, Axiom-owned "scope manifest" file,
   kept outside Ledgerkit's own schema, with five deterministic
   checks before it can support a `VERIFIED` derivation. Absent a
   passing manifest, `derived.status` is `UNCERTAIN`, never `VERIFIED`
   with a null scope.
2. **"Missing evidence" vs "contradictory evidence" corrected.** The
   prior revision mapped missing reviewer metadata to `CONTESTED`.
   This conflated absence with conflict. Fixed: missing scope and
   missing reviewer metadata now both map to `UNCERTAIN`; `CONTESTED`
   is reserved for an actual conflict (disagreeing evidence items, or
   a scope manifest that names the wrong claim or a stale source
   pin).
3. **Native dependency extraction specified.** `impacted()` previously
   matched only `source.ref`/`evidence[].ref`. Native register fields
   `implementation[]` and `tests[]` are now extracted too (§3f),
   function/class-qualified references resolved to file-level paths
   for Git-diff matching (deliberately conservative, not
   AST-aware — this project's own complexity budget), `upstream`
   revision changes represented as a pseudo-path change record, and
   unparseable/dangling references reported as an explicit
   `unresolved_reference` diagnostic rather than silently dropped.
4. **Native-vs-generic validation distinguished explicitly** (§6.0):
   Axiom's own default schema's `evidence[].reviewed_by` check applies
   only to Axiom's own default `knowledge/claims/` records; it is not
   a requirement imposed on Ledgerkit's native register, which has its
   own, different, equally valid reviewer-identity convention
   (top-level `verified_by`/`verified_date`, §3b).
5. **Oracle evidence made durable.** All nine fixture journals, full
   hledger transcripts, exact binary/commit identification, and a
   reproduction recipe are now version-controlled at
   `evidence/phase-2-stage-2.1-oracle/` — re-run fresh in this session
   against the live pinned oracle (confirmed matching the prior
   round's results), not left in a scratch directory that does not
   survive the session.
6. **Drift demonstration strengthened to three conditions.** EC-021's
   relevance as the "relevant change" condition is now grounded in an
   actual checked dependency (both EC-021 and EC-022 depend on
   `txn.postings` being complete before `resolve_elision()` runs — not
   mere file co-location), and a third, new "same-file,
   semantically-unrelated" condition is added specifically to measure
   file-level impact detection's own known false-positive cost
   directly, rather than leaving it a theoretical limitation.
7. **Stale section cross-references fixed.** Several `§7` references
   to what is actually `§6` ("Handoff to Stage 2.4") in
   `planning/phase-02-stage-2.1-plan.md`, `planning/phase-02-adoption-design.md`
   and `planning/phase-02-template.md` — pre-existing dangling
   references, not introduced by this amendment, found during this
   round's own cross-document consistency check and fixed.

### 7.2 What remains open

- `knowledge/scope-manifests/`'s exact file format is illustrative;
  precise field validation (beyond the five checks named) is BUILD-phase
  work.
- The `Skill`-tool `PreToolUse` matcher's payload shape remains
  unconfirmed (unchanged from all prior rounds).
- Rows 2, 4, 5, 6, 7, 8's Ledgerkit-side (not hledger-side) behaviour
  was not independently re-run again in this round — see
  `evidence/phase-2-stage-2.1-oracle/README.md`'s explicit
  disclosure of exactly what was and wasn't re-confirmed.

### 7.3 Independent review of this amendment

Recorded in §8 below. **Note on this sentence:** when first written,
§8 did not yet exist — a fresh-context reviewer caught this as its own
BLOCKING finding (§8, Blocking 1), the same recurring defect class as
§3's original BLOCKING 1 and §6's BLOCKING 1. This is now the
**third** time this exact pattern has appeared in this file. Recorded
honestly, including the recurrence itself, rather than quietly fixed
without a trace — see §8's own closing note for what changes next
round to actually stop this from recurring a fourth time.

## 8. Third independent review (of the final-amendment round)

Dispatched to a `general-purpose` agent (fresh context), after all of
§7's edits existed on disk.

**Isolation achieved, in the reviewer's own words:** "fresh context
(no prior turns, no memory of any earlier round), no investment in
this package's outcome, re-derived every checkable claim from the
real files/binaries/git history." **Not achieved:** "same operator,
same machine, and... almost certainly the same underlying model
family as whoever produced this package and its three prior
'independent' reviews... best-effort, single-operator isolation."

### BLOCKING 1 — the dangling-forward-reference defect recurred a third time

Confirmed real: §7.3 said "Recorded in §8 below" while §8 did not yet
exist. The reviewer noted this is the exact pattern §3's original
BLOCKING 1 and §6's BLOCKING 1 already named, now appearing a third
time in the one file whose job is catching it. **Disposition: fixed**
— this section is that review. **Process change, not just a content
fix, to actually stop a fourth recurrence**: from this point on, this
file's own addenda are written in two passes within the same editing
session — the corrective-round addendum (§7-shaped) first, with any
promissory forward-reference to a not-yet-run review explicitly
phrased as pending ("a review has been dispatched; not yet returned"),
and the actual review section added as a **separate edit** only after
the dispatch returns, never written as a single pre-committed
"follows below" sentence before the review exists. The recurring
mistake was writing the promise and the promised content as if they
would land together; they haven't, three times running.

### BLOCKING 2 — EC-021's cited fix location was wrong

Confirmed real by the reviewer reading the actual code: `_flush_txn`
(`ledgerkit/parser.py:872–897`) only attaches tags/date-overrides to
an already-complete postings list and never drops one. The actual
EC-021 mechanism is in the directive-handling branches around
`parser.py:1264–1343` (e.g. the `account` directive handler at line
1278), which set `in_subdirective = True` without first checking
whether a transaction is still open, so the adjacent
subdirective-swallowing block (lines 1249–1258) silently consumes the
transaction's next posting line. **Disposition: fixed** —
`planning/phase-02-stage-2.1-plan.md` §6.2 now cites the correct
location, with the correction itself recorded rather than silently
swapped in. The reviewer confirmed the broader dependency argument
(both EC-021 and EC-022 depend on `txn.postings` being complete before
`resolve_elision()` runs) survives the correction — only the specific
function/line citation was wrong, not the underlying relevance
argument.

### MATERIAL-NONBLOCKING 3 — a garbled cross-reference

`planning/phase-02-knowledge-api-design.md`'s `get()` error section
read "the CI schema check (§5 of `planning/phase-02-template.md`
§2.3)" — `§2.3` is an unordered bullet list with no numbered item 5,
so the reference didn't resolve to anything coherent. **Disposition:
fixed.**

### Independently re-verified and found accurate

- The scope gate (§3b/§3b.1) genuinely closes the original
  VERIFIED/null-scope contradiction — the reviewer walked every
  branch and confirmed the combination that caused it is now
  structurally unreachable.
- Missing reviewer metadata maps to `UNCERTAIN`, not `CONTESTED`;
  `CONTESTED` is reserved for genuine conflicts only — confirmed, no
  other path produces it.
- `impacted()`'s native dependency extraction genuinely covers
  `implementation[]`/`tests[]`, with a real file-level resolution rule
  and a defined `unresolved_reference` diagnostic — confirmed present,
  not merely asserted.
- Native-vs-generic validation is actually distinguished; no
  remaining place assumes Ledgerkit's native `evidence[]` carries
  `reviewed_by`.
- `native.status` is never altered anywhere in the document.
- `impacted()` remains read-only, with no graph database or inferred-
  relationship engine.
- **The oracle evidence directory is real, not fabricated** — the
  reviewer independently re-ran rows 3, 7 and 9 against the live
  hledger binary and Ledgerkit's own `parser.parse_string()` against
  rows 1 and 3, in both cases getting results matching the recorded
  transcripts exactly, including the precise `899,00 EUR` and
  `$-150.00` figures.
- hledger/Ledgerkit identification confirmed accurate a third time.
- §7 item 7's claimed `§7`→`§6` fixes are real — every `§N` reference
  checked against each document's actual headings resolved correctly,
  except finding 3 above.
- `knowledge/scope-manifests/` is documented consistently.
- The third drift condition's function citation
  (`_apply_posting_date_override_tags`) is accurate — zero interaction
  with amount/assertion parsing, confirmed by direct reading.
- ADR 0008 unmodified; §1–§6 of this file confirmed byte-for-byte
  preserved (82 insertions, 0 deletions for this round's §7).
- No unnecessary complexity found in this round's fixes.

### What the reviewer did not check

Fixture rows 2, 4, 5, 6, 8's Ledgerkit-side behaviour (disclosed as
not re-run this round); the `Skill`-tool matcher payload shape
(unconfirmed across all rounds); `dev-docs/compat-register/examples/`;
whether a new relevant hledger commit has landed since the plan's
`git log --grep` check (time-sensitive); solo-developer realism
beyond Stage 2.1. No files modified anywhere.

### Quotable verdict

> "This round's substantive engineering content holds up under
> independent re-verification: the scope-gate fix genuinely closes the
> VERIFIED/null-scope contradiction with no path left open to
> fabricate scope from area/reason; missing-evidence and
> contested-evidence are now cleanly separated; impacted()'s native
> dependency extraction, its unresolved_reference diagnostic, and the
> native-vs-generic validation split are all real, specific, and
> correctly described; and the oracle evidence directory is genuine,
> durable, and reproducible — I re-ran three fixtures against the live
> hledger binary and Ledgerkit's own parser myself and got exactly the
> claimed results. But the round has two real defects of its own.
> First, and most serious: the file whose entire job is catching 'a
> document asserting another document's content exists before it was
> written' has now committed that exact error a third time... Second,
> the one specific technical claim this review was asked to check
> hardest — that EC-021's fix and EC-022's fix share a dependency,
> located by reading both functions — turns out to cite the wrong
> function... Fix the dangling §8 reference and correct the EC-021
> fix-location citation, and this round's actual engineering work is
> sound."

Both BLOCKING findings and the MATERIAL-NONBLOCKING finding are fixed
in the same batch this section was written in.

## 9. Native Codex review (PR #4)

The first **native** review of this planning package — distinct from
every round above, which was a fresh-context Claude subagent dispatch
(best-effort, single-operator isolation, per `docs/agent-isolation.md`).
PR #4 (`planning/phase-2-stage-2.1-ledgerkit-oracle` → `main`) was
opened and `@codex review` requested per `decisions/0005`. Reviewed
commit: `e83df4b88fd34e0bba1dfcabe16831326f5dd65f`. Result: **2 P2
findings**, both real, both fixed in the same batch as this entry.

1. **Local dependencies resolved against the wrong revision space**
   (`planning/phase-02-knowledge-api-design.md` §3f): the design
   checked whether `implementation[]`/`tests[]` paths (Ledgerkit
   files) existed "at the claim's own `pinned_at`/`compatibility_target`
   revision" — but `compatibility_target` identifies an **hledger**
   version, not a Ledgerkit repository revision; checking a Ledgerkit
   path's existence against an hledger version string is not a
   well-formed check. **Fixed**: local references now resolve against
   an explicit consumer-repository (Ledgerkit) revision — that
   evidence item's own `pinned_at` if given, else the revision the
   caller is currently evaluating against — never against
   `compatibility_target`, which is reserved exclusively for the
   `upstream:<project>` pseudo-path mechanism.
2. **Logging opt-out didn't cover CLI-owned event writes**
   (`planning/phase-02-measurement-design.md` §5): "removing or not
   installing the hooks is sufficient" to opt out contradicted §1's
   own statement that `axiom-knowledge` appends
   `knowledge_get`/`knowledge_find`/`knowledge_impact` events on its
   own exit, independently of hooks, and that test-runner wrappers/
   manual helpers write directly too. **Fixed**: a single shared
   environment-variable check (`AXIOM_DISABLE_LOGGING=1`) every event
   producer honours — hooks, the CLI's own writes, and manual helpers
   alike — alongside, not instead of, removing the hooks.

Both findings are genuine design defects this project's own fresh-context
review rounds (§1–§8) did not catch — native Codex found something new,
not a repeat of an already-known issue. Full test/governance
verification re-run after the fix: 82/82 + 33/33 tests, all governed
documents `PASS`, no trailing whitespace.

**Re-review requested on the fix** (commit `cdc3fb8`): **1 further P2
finding.** `planning/phase-02-adoption-design.md`'s skill body (§6)
never actually instructed recording `task_start` or passing
`--task-id`, even though `planning/phase-02-measurement-design.md`
§1–§2 requires that marker before retrieval for per-task measurement
to work at all — a real contradiction between what the skill tells an
agent to do and what the measurement design assumes the skill does.
**Fixed**: the skill body now records `task-start` as its first
retrieval-adjacent step, threads `--task-id` through every subsequent
example command (`get`/`find`/`impacted`/the test-runner wrapper), and
closes with `task-accepted` once acceptance criteria are confirmed
met. A pre-existing duplicate step-numbering bug (two steps both
numbered "8") found in the same pass was fixed alongside it.

**Re-review requested on this fix** (commit `441f4c8`): **2 further P2
findings**, both real.

1. **`impacted()`'s upstream-pin detection excluded the exact claim
   §3b.2 promises it catches proactively.** The predicate only flagged
   a claim still pinned at `base` — but a caller following §3f's own
   workflow constructs the upstream change record *after* the
   compat-register entry is already edited to `head`, so the claim
   whose pin just changed (the one with a now-possibly-stale scope
   manifest) was never the one flagged. §3b.2's claim that the two
   mechanisms "agree with each other by construction" was false as
   written. **Fixed**: `impacted()`'s upstream case now checks two
   conditions — not-yet-bumped (as before) and
   just-bumped-with-a-stale-scope-manifest (new) — so the proactive
   and reactive checks genuinely examine the same condition from each
   side.
2. **CLI-owned events (`task_start`, `knowledge_get`/`find`/`impact`)
   had no actual source for `session_id`.** These are plain processes
   with no hook stdin, and the capability research already recorded
   no documented session-ID environment variable — the design wrote
   "independently of hooks" without specifying how a `session_id`
   would reach them at all. **Fixed**: a `SessionStart` hook writes
   the session ID to a small local handoff file
   (`.axiom-local/current_session_id`); CLI-owned producers read it;
   invocation outside any session (human at a terminal, CI) is an
   explicit, named case producing `session_id: null`, not a
   fabricated value.
