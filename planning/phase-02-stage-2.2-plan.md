# Stage 2.2 implementation-ready plan — minimal Axiom adoption and knowledge retrieval

**Status: Planned. Not authorisation to implement.** Requires
independent review and explicit human approval before BUILD starts,
per `AGENTS.md` §2/§11 — the same pattern Stage 2.1 used
(`planning/archive/phase-02-stage-2.1/README.md`).

## 1. Objective and baseline

Per `planning/ROADMAP.md`'s Stage 2.2 row and `planning/phase-02-template.md`
§2.2: introduce the smallest practical Axiom integration into
Ledgerkit — one Claude Code skill, read-only `get`/`find` against
Ledgerkit's own existing `dev-docs/compat-register/` (not a duplicate
store), a minimal comparative wiki slice, and optional JSONL logging.
**This plan reuses, and does not repeat, the three cross-cutting
designs Stage 2.1 already produced and had independently reviewed**:

- [`planning/phase-02-adoption-design.md`](phase-02-adoption-design.md) —
  the skill's exact content (§6), file layout (§2), install/upgrade/
  removal (§4–5).
- [`planning/phase-02-knowledge-api-design.md`](phase-02-knowledge-api-design.md) —
  the Claim/Source/Evidence model, the native-register adapter (§3a–3f),
  `get`/`find` (§4), contract tests (§6).
- [`planning/phase-02-measurement-design.md`](phase-02-measurement-design.md) —
  the JSONL event format, session-ID handoff, usefulness
  classification.

Stage 2.2 does not redesign any of these; it builds the `get`/`find`
slice of the already-specified API and adopts the already-specified
skill, nothing more.

## 2. Scope — split across two repositories, two separate PRs

Axiom Dev and Ledgerkit keep their existing, separate governance
(established practice: "Axiom Dev: reusable methodology, knowledge
API, skill, CI tooling and template. Ledgerkit: actual accounting
implementation, compatibility evidence, integration and dogfooding").
Stage 2.2 BUILD is therefore **two dependent PRs, not one**:

### 2a. Axiom Dev PR — the reusable `axiom-knowledge` library/CLI

New, self-contained module (e.g. `src/axiom_knowledge/`), implementing
**only** `get(id)` and `find(query)` from
`planning/phase-02-knowledge-api-design.md` §4 — `related`/`impacted`
are explicitly deferred to Stage 2.3, which is what "introduced
incrementally" in that design already specifies; this plan does not
re-decide that. Includes:

- The §3a–§3f native-register adapter (status/relationship mapping,
  scope gate, dependency extraction fields) and the §3 generic
  default-schema path, both already fully specified.
- A thin CLI wrapper (`axiom-knowledge get <id>`, `axiom-knowledge
  find "<query>"`), plus the `task-start`/`task-accepted` helpers
  `planning/phase-02-measurement-design.md` requires.
- Unit tests against **synthetic fixture YAML files** shaped like
  Ledgerkit's real compat-register schema (`dev-docs/compat-register/schema.md`,
  already read in full during Stage 2.1) — this PR needs no live
  Ledgerkit checkout and does not touch `~/projects/ledgerkit`.
- This PR is reviewable, testable and mergeable entirely within
  Axiom Dev's own CI (`ci-required`), independently of Ledgerkit.

### 2b. Ledgerkit PR — adoption (depends on 2a being merged)

A **separate, later, Ledgerkit-targeted PR**, not built or opened by
this plan or this round:

- Copy `.claude/skills/axiom-work/SKILL.md` verbatim from
  `planning/phase-02-adoption-design.md` §6 into Ledgerkit's own
  `.claude/skills/axiom-work/`.
- Add `knowledge/README.md` pointing the CLI's source configuration at
  Ledgerkit's own `dev-docs/compat-register/` (the deferral decision
  `planning/phase-02-stage-2.1-plan.md` §7 already made — **not** a
  new `knowledge/claims/` directory).
- Add `knowledge/wiki/`: an illustrative **10–20 claim** slice (per
  `planning/phase-02-template.md` §2.2's own "not a quota" framing),
  each entry linking to a stable compat-register ID rather than
  restating its content.
- Add `.axiom-local/` to Ledgerkit's `.gitignore` (events + the
  session-ID handoff directory, `planning/phase-02-measurement-design.md`).
- Install `axiom-knowledge`: template-copy the script/library from 2a
  into Ledgerkit for now, per `planning/phase-02-adoption-design.md`
  §5's explicit decision to defer packaging until a second real
  consumer exists — not re-decided here.

**Neither sub-PR modifies anything about Ledgerkit's actual accounting
implementation** — this stage is adoption scaffolding only; EC-022
remains Stage 2.4's work, unchanged by this plan.

## 3. Interfaces

Exactly `get(id) -> Claim | NotFound` and `find(query) -> list[Claim]`
as specified in `planning/phase-02-knowledge-api-design.md` §4 —
including their exact error semantics (`NotFound`, `Malformed`,
`InvalidQuery`) and the §3a–§3f native/derived separation. This plan
does not restate those signatures; implement against the cited
sections directly.

## 4. Independent acceptance criteria

Mirrors `planning/ROADMAP.md`'s own Stage 2.2 exit demonstration,
made concrete:

1. `get(<a real compat-register ID>)` against Ledgerkit's actual
   register returns the `native`/`derived` pair (§3a), with
   `derived.status` computed by the actual scope-gate/reviewer-identity
   logic (§3b/§3b.1) — not a stub that always returns the native
   status unchanged.
2. `find(<query>)` deterministically returns the same result for the
   same repository state, exact-ID and substring/field-equality
   search only (§4) — no ranking, no embeddings.
3. A **fresh-context** agent, given only the installed skill and
   `knowledge/README.md` (no prior session, no author's own
   explanation), successfully retrieves a scoped claim via the skill's
   own instructions and correctly states which evidence tier it's
   actually at (e.g. distinguishes a `self-verified` native claim,
   correctly derived as `OBSERVED`, from a genuinely `VERIFIED` one) —
   demonstrated and independently observed, not merely asserted.
4. Independent review confirms: no write path exists anywhere in the
   implementation (`AGENTS.md` §6); the native record is never
   altered; `derived.status` never claims `VERIFIED` with a null
   `derived.scope` (the exact defect `planning/phase-02-knowledge-api-design.md`
   §3b.1 was written to prevent — re-checked against the real
   implementation, not just the design).

## 5. Negative tests (required, not exhaustive)

Drawn directly from `planning/phase-02-knowledge-api-design.md` §6 —
this plan selects the subset relevant to `get`/`find` specifically
(the `related`/`impacted` cases in that section apply to Stage 2.3,
not here):

- `get()` for a nonexistent ID → `NotFound`.
- `get()` for a native record claiming `verified` with no scope
  manifest → `derived.status: UNCERTAIN`, `derived.scope: null` (the
  core regression test for the scope-gate fix history in
  `planning/phase-02-planning-review.md` §7–§8).
- `get()` for a native record with `verified_by`/`verified_date`
  missing despite `status: verified` → `UNCERTAIN`, not `CONTESTED`
  (the corrected mapping, §9 of the same review record).
- `get()` for a native record with genuinely conflicting `evidence[]`
  entries → `CONTESTED`.
- `get()` for a malformed/unresolvable native field
  (`implementation[]`/`tests[]` that doesn't parse) → the
  `unresolved_reference` diagnostic (§3f), not a crash.
- `find()` with no matches → `[]`, not an error.
- `find()` with a malformed query (reserved-character misuse) →
  `InvalidQuery`.
- `find()` run twice against the same repository state → identical,
  identically-ordered result (determinism check).

## 6. Measurable overhead

Stage 2.2 measures **construction** cost (building the adoption
itself); Stage 2.4 measures **use** cost (retrieval during a real
development task) — these are deliberately different questions, not
conflated. Per `planning/phase-02-measurement-design.md` (reused, not
redesigned):

- Time and `axiom-knowledge` invocation count to build and pass the
  2a test suite.
- Setup steps required for 2b's adoption (file count, lines changed,
  manual steps) — this is the first real data point toward Stage
  2.6's "adoption effort" question, predeclared now rather than
  invented after the fact.
- `task_start`/`knowledge_get`/`knowledge_find` events recorded during
  this stage's own build-and-test work, joined by the session-ID
  handoff mechanism (`planning/phase-02-measurement-design.md`,
  corrected across its own review history) — exercising that
  mechanism for the first time against real, not hypothetical, CLI
  invocations.

No claim of causal benefit is made from these numbers alone — observed
construction cost, not a controlled comparison (`AGENTS.md` §6;
ADR 0008).

## 7. Dependencies

No new project dependency. `pyyaml` (already in `requirements.txt`)
is sufficient for the native-register adapter's YAML reading. Python
3.13, matching existing CI. No MCP, no Axiom Assure, no persistent
service, no embeddings — unchanged from every prior round's
complexity-budget discipline.

## 8. Approval gates

1. This plan itself, independently reviewed and human-approved,
   before either sub-PR's BUILD starts (`AGENTS.md` §2, §11) — not
   granted by this document's own existence.
2. PR 2a (Axiom Dev): independent review, `ci-required` green,
   fresh-head native Codex review dispositioned, then human merge
   approval — the same bounded cycle `AGENTS.md` §14 already governs.
3. PR 2b (Ledgerkit): **cannot open before 2a is merged** (it depends
   on 2a's CLI/skill artifacts). Reviewed under Ledgerkit's own
   repository governance, which this plan does not assume mirrors
   Axiom Dev's (`planning/phase-02-adoption-design.md` §3, capability
   4: "use existing project governance... without duplicating or
   replacing it"). Separate human merge approval on that repository.
4. Stage 2.2 is marked Completed in `planning/ROADMAP.md` only after
   both sub-PRs are merged and independent acceptance criteria (§4)
   are demonstrated — an agent prepares that status change, a human
   confirms it, per `docs/development-lifecycle.md`'s phase-acceptance
   procedure, same as Stage 2.1's own closeout.

Next: Stage 2.3 (deterministic integrity and drift, including the
native-register identity/reference integrity gap
`planning/archive/phase-02-stage-2.1/README.md` already flagged as
unresolved) remains out of scope for this plan.
