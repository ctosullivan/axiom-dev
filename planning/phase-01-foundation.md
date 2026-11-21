# Phase 1 — Foundation

Authorising prompts:
[`planning/prompts/001-phase-1-bootstrap.md`](prompts/001-phase-1-bootstrap.md)
(original bootstrap) and
[`planning/prompts/002-phase-1-amend-and-implement.md`](prompts/002-phase-1-amend-and-implement.md)
(amendment, supersedes the bootstrap-only restriction and authorises full
Stage 1.0–1.5 implementation).
Related ADRs: [`decisions/0001`](../decisions/0001-development-governance.md),
[`decisions/0002`](../decisions/0002-knowledge-architecture.md),
[`decisions/0003`](../decisions/0003-independent-verification.md),
[`decisions/0004`](../decisions/0004-phase-1-amendment-verification-measurement-and-acceptance.md).

This is the implementation-ready Phase 1 plan, amended per prompt 002.
**Completing Stage 1.0 does not complete Phase 1.** Phase 1 closes
only when Stage 1.5's dogfooding exercise closes out successfully against
the acceptance requirements in §8, §9 and §10 below. Stages 1.1–1.5 are
specified here to the depth needed to establish dependencies, scope, and
acceptance criteria — each still requires its own focused plan, written
and reviewed, immediately before that stage's implementation starts
(`AGENTS.md` §2).

## 0. Amendment record (prompt 002, 2026-11-21)

Prompt 002 required four amendments to this plan, resolved as follows
(full rationale in `decisions/0004`):

- **Amendment A (minimise bootstrap overhead):** assessed against the
  existing plan and found largely already satisfied (see `decisions/0001`,
  §2 below). One gap closed: §4's stage specs are tightened below so that
  no stage documents a capability's behaviour as OBSERVED/VERIFIED before
  that capability actually exists and has been run for real — "detailed
  technical documentation... alongside the functionality it describes,"
  not ahead of it.
- **Amendment B (strengthen independent verification):** Stage 1.3 and
  1.4's specs below now require protected/baseline fixtures, independently
  reviewed acceptance criteria predating implementation, an explicit
  detected/missed/introduced defect ledger, and hard separation between
  test results, Codex findings and human acceptance as distinct evidence
  artifacts — not a reviewer re-deriving the implementer's own assumptions.
- **Amendment C (measurement from the beginning):** `evidence/phase-1-log.md`
  (new, §9 below) starts recording real effort/cost/defect/rework/reuse
  data from this amendment onward — not retroactively for Stage 1.0, which
  predates the log and is not re-measured after the fact.
- **Amendment D (explicit acceptance demonstrations):** eight concrete
  demonstrations (§10 below), each mapped to the stage that produces it
  and tracked as not-yet-demonstrated until real evidence exists.

## 1. Objective and expected value

Establish a working, self-governing development methodology for Axiom Dev,
and then prove — not assume — that the methodology holds up by using it to
build and refactor a real piece of Axiom Dev itself, with independent
verification at each step. The value being tested is the project's own
fundamental hypothesis (`planning/prompts/001-phase-1-bootstrap.md` §2):
that a lightweight, Markdown/YAML-and-conventional-tools methodology
improves correctness, efficiency and maintainability of agentic
development net of its own overhead. Phase 1 is the first and most direct
test of that hypothesis, not a formality before "real" work starts.

## 2. CodeCompass precedents — Retain / Simplify / Exclude

Produced by direct inspection of `~/projects/codecompass` on 2026-11-21
(97 ADRs under `decisions/`, ~115 files under `planning/phase-*.md`, ~190
files under `planning/retros/`). Full citations are in `decisions/0001`,
`0002`, and `0003`; this section summarizes the resulting posture.

**Retain:**
- Plan-before-code, one plan per phase, naming scope/non-goals/files/
  verification (`CLAUDE.md` §1) → adopted as `AGENTS.md` §2.
- Same-commit documentation sync (`CLAUDE.md` §2) → adopted as
  `AGENTS.md` §5.
- The one file every session trusts unconditionally (their `CLAUDE.md`)
  gets the *highest* change friction, not the lowest → adopted as
  `AGENTS.md` §0, §11, §12 (governance changes need explicit human
  approval).
- Append-only ADRs; reversal = new ADR, not an edit (`decisions/0061`
  pattern) → adopted as `AGENTS.md` §3.
- Independent, read-only, non-repairing closeout role, voided by later
  commits (`CLAUDE.md` §5) → adopted as `AGENTS.md` §6.
- Knowledge placement as a small fixed category→artifact table, with
  enforcement classes that distinguish mechanical/behavioural (blocking)
  from semantic/editorial (non-blocking) (`decisions/0094`) → adopted in
  simplified form as `AGENTS.md` §7, full version deferred to Stage 1.1.
- "No synthetic substitute" for a real dogfooding gate — report unmet
  honestly rather than satisfy it with a constructed fixture
  (`decisions/0094` point 4) → binding on Stage 1.5 (§7 below).

**Simplify:**
- ADR volume and the same-day/multi-"corrective pass" amendment pattern
  (`decisions/0066`, `0067`/`0068`, `0081`–`0083`) → Axiom Dev reserves
  ADRs for genuinely non-obvious tradeoffs and fixes drafts before
  acceptance rather than multiplying numbered amendments after.
- Schema sidecars (`README.md.schema.yaml`,
  `docs/concepts/knowledge-model.md.schema.yaml`) → keep the concept
  (declarative per-doc schema: audience, required topics, acceptance
  criteria), drop the claim-ID/claim-status-gating apparatus until a real
  backing store exists (`decisions/0002`).
- Fixed specialist-agent roster (`decisions/0049`, 7 roles "pruned at
  GATE DA," later broken by Phase 43c's 8th role) → keep the principle
  (producer ≠ verifier) without a pre-committed roster (`decisions/0003`).

**Exclude:**
- `context-graph.db` (SQLite dependency graph) and any custom
  documentation compiler — out of scope for bootstrap per the prompt, and
  not demonstrated as necessary yet.
- The ~190-file `planning/retros/` taxonomy of parallel per-phase audit
  files — Axiom Dev keeps one proportionate retro per completed phase.
- Editing an ADR in place multiple times same-day before first use
  (`decisions/0066`) — get review right before acceptance instead.

**Named divergence from CodeCompass:** CodeCompass fixed "no AI
attribution in commits, ever" as policy (`decisions/0007`). Axiom Dev has
not adopted that as project policy — see `CLAUDE.md` "Commit and session
attribution" for why this is currently a session/tooling convention rather
than a project decision, and what would make it a real ADR instead.

## 3. Current implementation and knowledge baseline

Before this session: the repository contained only `LICENSE` (MIT,
Cormac O'Sullivan, 2026), on a clean `main` branch tracking
`origin/main` = `git@github.com:ctosullivan/axiom-dev.git`. No governance,
planning, decisions, source, or tests existed. `~/projects/axiom-assure`
is similarly a bare `LICENSE`-only repository (not otherwise touched by
this plan). No `gh` CLI or GitHub token is available in this environment.

## 4. Stage specifications

Each stage below lists: objective, scope, explicit non-goals, dependencies,
proposed files, contracts/acceptance criteria, verification method,
documentation implications, and completion criteria. Stages after 1.0
require their own focused plan before implementation — the detail here
fixes *what must be true to call the stage done*, not the implementation
itself.

### Stage 1.0 — Repository bootstrap and governance

- **Objective:** a coherent, internally consistent repository foundation
  that can govern its own subsequent development.
- **Scope:** `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  `CHANGELOG.md`, `planning/ROADMAP.md`, `planning/CONTEXT.md`, this file,
  `planning/prompts/001-phase-1-bootstrap.md`, `planning/retros/` (created,
  empty — no phase has completed yet), `decisions/0001`–`0003`,
  `.github/pull_request_template.md`.
- **Non-goals:** no `docs/`, `contracts/`, `evidence/`, `src/`, `tests/`,
  or `.github/workflows/` — these belong to later stages and would be
  placeholder structure if created now. No Codex integration. No knowledge
  schema/validator.
- **Dependencies:** none (first stage).
- **Contracts / acceptance criteria:** see §8 "Stage 1.0 acceptance" below.
- **Verification method:** independent review (best-effort isolation —
  see §6) plus the deterministic checks in §5; no automated CI exists yet
  to run anything against.
- **Documentation implications:** this stage *is* the documentation; its
  own internal consistency is the test.
- **Completion criteria:** independent review's material findings
  resolved, deterministic checks pass, foundation committed and pushed on
  a reviewable branch. Per `AGENTS.md` §11 and §6, a human still needs to
  merge the PR and mark Stage 1.0 Completed in `planning/ROADMAP.md`;
  this plan does not do that unilaterally.

### Stage 1.1 — Knowledge and documentation methodology

- **Objective:** make the knowledge model in `decisions/0002` concrete and
  demonstrated, not just declared.
- **Scope:** design and document (a) the lightweight documentation schema
  (per-doc schema identifying identity, audience, purpose, required
  topics, relevant canonical knowledge, acceptance criteria — sidecar YAML
  or an equivalent simpler convention, decided fresh rather than copied
  from CodeCompass's claim-ID apparatus); (b) the full knowledge placement
  policy (expanding `AGENTS.md` §7 into `docs/knowledge-placement.md`,
  with mechanical vs. editorial enforcement classes per the retained
  CodeCompass pattern); (c) contract and evidence conventions
  (`contracts/`, `evidence/` directory structure and format — created
  here, for the first time, with real initial content); (d) a knowledge
  reconciliation procedure (how documentation is checked against
  code/decisions and corrected); (e) manual validation of at least one real
  document against its schema, demonstrating the schema is usable before
  any validator is built.
- **Non-goals:** no validator software yet (that is Stage 1.4's first
  component); no claim-ID/knowledge-base apparatus (deferred per
  `decisions/0002`, revisit only if demonstrated necessary).
- **Dependencies:** Stage 1.0 merged (governance files and placement table
  must exist to extend rather than duplicate).
- **Contracts / acceptance criteria:** schema and placement policy exist as
  documents; at least one real Axiom Dev document is checked against the
  schema by hand and passes or is fixed until it does; reconciliation
  procedure is written down and has been run at least once (e.g.
  reconciling this very plan's own stage descriptions against what Stage
  1.0 actually produced).
- **Verification method:** independent review of the schema/policy for
  internal consistency and for not quietly introducing claims about
  capabilities that don't exist yet.
- **Documentation implications:** introduces `docs/`, `contracts/`,
  `evidence/` with real initial content — the first point at which those
  directories in the original scaffold proposal are no longer speculative.
- **Completion criteria:** independent closeout confirms schema +
  placement + reconciliation procedure exist, are internally consistent,
  and have been exercised against real material at least once — not merely
  written.

### Stage 1.2 — Agent development methodology

- **Objective:** make the lifecycle and agent responsibilities in
  `AGENTS.md` and `decisions/0003` operationally concrete for a real
  development task, ahead of Stage 1.4 needing to use them for real.
- **Scope:** document the complete UNDERSTAND→SPECIFY→ASSESS
  IMPACT→BUILD→VERIFY→RECONCILE lifecycle with per-step entry/exit
  criteria; document agent responsibilities by function (not roster, per
  `decisions/0003`) with, for each function, what evidence it may rely on,
  what context it must not have (where isolation matters), and whether
  that isolation is mechanically enforced or best-effort; document phase
  acceptance and reconciliation procedure (how a stage actually gets
  marked Completed in `planning/ROADMAP.md`).
- **Non-goals:** no new orchestration tooling or sandbox; no fixed named
  roster (per `decisions/0003`).
- **Dependencies:** Stage 1.1 (acceptance/reconciliation procedure here
  builds on Stage 1.1's knowledge reconciliation procedure rather than
  duplicating it).
- **Contracts / acceptance criteria:** the lifecycle and responsibility
  documentation must be concrete enough that Stage 1.4 can be executed
  against it without inventing missing procedure mid-stage.
- **Verification method:** independent review checking specifically for
  the failure mode named in `decisions/0003` — isolation claimed without a
  named enforcement mechanism.
- **Documentation implications:** extends `docs/` (e.g.
  `docs/agent-isolation.md`) rather than duplicating `AGENTS.md`.
- **Completion criteria:** independent closeout confirms the documented
  procedure is concrete and self-consistent; real test is whether Stage
  1.4 can proceed without a mid-stage procedural gap.

### Stage 1.3 — Codex CI review gate

- **Objective:** an enforceable, fail-closed independent PR review gate
  using GitHub Actions and supported Codex tooling, per
  `decisions/0003` point 4.
- **Scope:** research current supported Codex integration/authentication
  options (explicitly not assumed by this plan — the bootstrap prompt
  requires this research happen as part of producing the
  implementation-ready stage plan, not before); implement the GitHub
  Actions workflow(s); define structured review-finding format; wire P0/P1
  findings to block merge via GitHub required status checks; define
  fail-closed behaviour for failed/incomplete review runs; define advisory
  (non-blocking) finding disposition and recording.
- **Non-goals:** no custom review-orchestration framework beyond
  conventional GitHub Actions; no MCP.
- **Dependencies:** Stage 1.0 (repo/branch conventions; `.github/` exists);
  does not strictly depend on 1.1/1.2 but is more useful once contracts
  (1.1) exist for the gate to check against.
- **Contracts / acceptance criteria:** demonstrated test cases for *both* a
  permitted merge (clean review) and a blocked merge (P0/P1 finding, or
  failed/incomplete review) — per the bootstrap prompt's explicit
  requirement that tests demonstrate both outcomes, not just the happy
  path.
- **Verification method:** the test cases above, run for real against a
  real PR; independent review of the gate's fail-closed behaviour
  specifically (does an API error or timeout silently pass?).
- **Architectural split (Amendment B):** the gate has two separable
  pieces, and this plan tracks them separately rather than as one
  monolithic "the gate works" claim: (1) a **deterministic policy
  evaluator** — ordinary, locally testable code that takes a structured
  review-finding document as input and decides pass/block/fail-closed; this
  needs no live Codex call to build or unit-test, and its tests are
  deterministic CI from the moment they exist; (2) the **live integration**
  — the actual GitHub Action invoking Codex against a real PR and feeding
  its output to (1). (1) can be built, tested and evidenced without any
  external credentials. (2) requires real GitHub repository configuration
  (secrets, required status checks, possibly admin API access) and, if
  Codex calls are paid, a cost decision — per the authorising prompt, "do
  not bypass protection if configuration fails; report the blocker" rather
  than substituting a local simulation for live GitHub evidence. If (2) is
  blocked by missing credentials/access/cost-authorisation, that is
  recorded as an open item here and in `planning/CONTEXT.md`, not
  papered over by (1)'s test suite passing.
- **Documentation implications:** `docs/` gets the gate's actual behaviour
  documented as OBSERVED/VERIFIED only after the test cases above have
  actually been run — not as INTENDED language describing a design.
- **Completion criteria:** both required-check test cases demonstrated
  with evidence; independent closeout confirms fail-closed behaviour
  specifically, since this is the gate most likely to silently fail open.
  If only the deterministic evaluator (piece 1) is evidenced and the live
  integration (piece 2) is blocked, this stage's exit criterion ("real
  GitHub PR evidence demonstrates both successful and blocked outcomes")
  is **not met** and must be recorded as open, per Amendment D
  demonstration 3 (§10).

### Stage 1.4 — Axiom self-development and refactoring

- **Objective:** build one small, genuine Axiom Dev component — the
  knowledge/documentation validator named in `decisions/0002` — using the
  full methodology established in 1.0–1.3, then perform a real,
  behaviour-preserving refactor of it, demonstrating the methodology holds
  up under actual (not simulated) development pressure.
- **Scope:** implement the validator against the schema from Stage 1.1;
  then refactor it meaningfully (not cosmetically — e.g. a real internal
  restructuring, such as changing its parsing/validation architecture or
  extraction approach, while preserving external behaviour) with: contracts
  established *before* the refactor starts; a baseline verification run
  pre-refactor; a bounded implementation (scoped plan, not open-ended);
  independent review of the refactor; before/after behavioural
  verification showing the contracts still hold; a knowledge-placement
  assessment of the result; documentation reconciliation.
- **Anti-circularity mechanics (Amendment B), binding on this stage:**
  - *Contracts and acceptance criteria* are written and independently
    reviewed (fresh context) **before** implementation starts — the
    reviewer checks the contract/fixtures, not the implementer's code,
    and has not seen the implementation yet.
  - *Fixtures* include both known-valid documents (should pass) and
    deliberately defective ones (should fail, with a specific expected
    error) — not only happy-path examples.
  - *Protected expected outputs*: once a contract/fixture set is accepted,
    its files live under a path recorded with a checksum in
    `evidence/` at acceptance time. A later PR (implementation or
    refactor) that changes a protected file's checksum without a separate,
    explicitly reviewed "contract change" commit explaining why is a
    verification failure. **Named honestly, per the same standard
    `decisions/0003` §3 sets for isolation claims: this is a procedural
    control, not a mechanical one** — nothing in this environment
    currently computes the checksum and blocks the PR automatically; a
    human or independent reviewer has to actually check it. It becomes
    mechanical the moment Stage 1.4's validator (or a CI hook) is taught
    to compare the checksum itself and fail the check on mismatch — until
    then, calling it "mechanical enforcement" would be exactly the
    mislabeling `AGENTS.md` §9's "not weakened unilaterally" rule and
    `decisions/0003` exist to prevent.
  - *Independent evaluation* of the initial implementation happens from a
    fresh context, checking the implementation against the protected
    contract — not against the implementer's own test narrative.
  - *Baseline before refactor*: the full test suite's pass/fail output
    against the protected fixtures is captured to `evidence/` before any
    refactor commit, so "before" is a real recorded artifact, not a
    retrospective claim.
  - *Before/after verification* reruns the identical protected fixture
    suite post-refactor; any difference in result is a regression, full
    stop, regardless of how the refactor is explained.
  - *Defect ledger*: `evidence/` records, per implementation and per
    refactor: defects the test suite detected, defects independent review
    found that tests missed, and (if any) defects the refactor itself
    introduced. An empty ledger is a claim that needs the same evidence
    as a populated one.
  - *Evidence separation*: test-suite results, Codex/independent-review
    findings, and the human merge-acceptance decision are recorded as
    three distinct artifacts/sections — never merged into one "it passed"
    line.
- **Non-goals:** no feature growth beyond what the validator needs to
  validate Stage 1.1's schema; the refactor is not an excuse to add scope.
- **Dependencies:** Stages 1.1 (schema to validate against), 1.2
  (lifecycle/responsibility procedure to execute against), 1.3 (PR gate
  to actually run the implementation and refactor PRs through — if 1.3
  isn't done yet when 1.4 starts, 1.4's plan must say explicitly whether it
  proceeds without the gate or waits).
- **Contracts / acceptance criteria:** validator has deterministic tests
  demonstrating it accepts conforming documents and rejects non-conforming
  ones; refactor's before/after tests are identical (same contract, same
  test suite) and both pass; a cosmetic-only refactor (renames, formatting)
  does not satisfy this stage — the bootstrap prompt is explicit that it is
  insufficient.
- **Verification method:** test suite run before and after refactor;
  independent review of both the original implementation and the refactor
  PR.
- **Documentation implications:** first real content for `src/`, `tests/`;
  first real evidence records under `evidence/`; first real exercise of
  the Stage 1.3 gate if available.
- **Completion criteria:** independent closeout confirms the refactor was
  substantive (not cosmetic), contracts held before and after with
  evidence, and documentation/knowledge records were reconciled in the
  same changes — not as follow-up.

### Stage 1.5 — Independent documentation reconstruction and closeout

- **Objective:** test whether an isolated agent, given only approved
  evidence, reconstructs an account of Axiom Dev's architecture and
  behaviour consistent with the project's existing documentation — and
  use any gap found to actually fix documentation drift, not merely to
  note it.
- **Scope:** define what "approved evidence" means (what the
  reconstructing agent may read: likely source, tests, contracts,
  evidence records — not prior planning narrative or this plan's own
  prose, to avoid it reconstructing the plan instead of the system);
  dispatch the reconstruction with the best isolation actually available
  (per `decisions/0003`, name explicitly whether it is mechanically
  enforced or best-effort); compare reconstruction against existing
  `docs/`; investigate every omission, contradiction, and misplaced-
  knowledge finding; fix deficiencies through the normal development
  workflow (plan → ADR if non-obvious → implement → verify → reconcile),
  not as a one-off patch outside the methodology being tested.
- **Non-goals:** no new sandbox/broker infrastructure to force stricter
  isolation than is already available, unless a Stage 1.5 plan
  specifically justifies building one (see `decisions/0003` Consequences).
- **Dependencies:** Stage 1.4 (there must be a real component with real
  code, tests and docs to reconstruct against — reconstructing governance
  prose alone would not test anything).
- **Contracts / acceptance criteria:** the "no synthetic substitute" rule
  from `decisions/0094` (retained in §2 above) applies directly: this
  gate cannot be satisfied by a constructed, friendly reconstruction
  exercise. If the reconstruction finds nothing wrong, that must be because
  it genuinely found nothing wrong, with the comparison evidence attached
  — not because the exercise was built to pass.
- **Verification method:** direct comparison of reconstruction output
  against `docs/`, with findings classified and each one either fixed
  (with its own change) or explicitly dispositioned as not requiring a fix,
  with reasoning.
- **Documentation implications:** this stage is the first full test of
  whether Stages 1.0–1.4's documentation-sync discipline actually held.
  Expect and record real findings — a clean result on the first attempt is
  a reason for more scrutiny, not less.
- **Completion criteria:** reconstruction run, compared, findings
  resolved through the normal workflow, and outcomes/limitations/overhead
  recorded in a retro under `planning/retros/`. **This is the completion
  criterion for Phase 1 as a whole**, not just Stage 1.5.

## 5. Stage 1.0 deterministic checks (performed in this session)

- Git: `git status` clean before and after staging; diff reviewed file by
  file before commit; no destructive operations used.
- Whitespace: no tool exists yet to check this mechanically beyond normal
  editor behaviour — recorded as a gap, not claimed as checked.
- Internal references: every relative Markdown link added in this stage's
  files was checked by hand against the actual files created in this same
  stage (not against future-stage paths).
- ADR numbering: `0001`, `0002`, `0003` — sequential, no gaps, matches
  `decisions/` directory contents.
- File/directory consistency: `planning/ROADMAP.md` stage table matches
  this file's stage headings; `README.md`'s repository map matches what
  actually exists after this stage.
- Agent instruction consistency: `CLAUDE.md` defers to `AGENTS.md` and
  introduces no contradicting rule; `CONTRIBUTING.md` cites `AGENTS.md`
  section numbers that exist.
- Planning-prompt provenance: `planning/prompts/001-phase-1-bootstrap.md`
  carries a provenance header and is the full original text, not a
  reconstruction or summary.

No CI, validator, or Codex gate exists yet to run — this plan does not
claim otherwise.

## 6. Independent review record

Dispatched: a fresh, non-forked agent with no prior conversation context,
given this repository's files directly and the review questions from the
bootstrap prompt §9 Step 7. **Isolation level: best-effort, not strict** —
same operator/session dispatched it, and it ran on the same underlying
model; no mechanical isolation (capability broker, separate credential,
sandboxed context) was used, per the honesty requirement in
`decisions/0003` §3.

### Findings and dispositions

**B1 (blocking) — status docs claimed the foundation was already committed
and pushed while every file was still untracked.** The reviewer ran
`git status` and `git ls-remote --heads origin` directly and found no
`phase-1/stage-1.0-bootstrap` branch anywhere, local or remote, while
`planning/CONTEXT.md` and this file's §5/§8 both asserted a commit, a push,
and a specific compare URL already existed. Correctly identified as the
exact failure mode this project exists to prevent (`AGENTS.md` §6).
**Disposition: fixed.** This finding is itself evidence that writing
"done" language for a step before performing it is a real, not merely
theoretical, risk even inside the session that wrote the governance rules
against it. The actual commit and push now happen only after this
section was corrected — see the git log and `origin` for the resulting
SHA, which this document does not predict in advance.

**B2 (blocking) — this section (§6) was a placeholder describing that a
review *would* happen, with no actual findings, while other files already
asserted the review's findings were "resolved."** `planning/CONTEXT.md`
claimed findings were resolved; §8 criterion 6 required findings
"recorded in §6"; §6 had none. **Disposition: fixed** — this is the fix:
the findings in this subsection are the actual, verbatim-summarized
findings from the dispatched review, not a forward-looking description.

**A1 (advisory) — "Accepted (partial — see Unresolved)" in `decisions/0002`
and `decisions/0003` is a non-standard status not defined anywhere.**
**Disposition: fixed** — `AGENTS.md` §3 now notes that an ADR may carry a
parenthetical qualifier (e.g. "partial") pointing to its own "Unresolved"
section, alongside the plain `Accepted`/`Superseded by NNNN` statuses.

**A2 (advisory) — the methodology's own discipline is unproven; B1/B2
happening in the only stage executed so far is itself evidence that
holding this discipline is harder in practice than the documents assume.**
**Disposition: accepted as recorded, not actioned further.** This is
exactly the kind of honest, negative finding `AGENTS.md` §6 and the
bootstrap prompt's operating constraints ask to be recorded rather than
smoothed over. It is left here as a standing caution for Stage 1.4's
self-development exercise, not something Stage 1.0 can itself resolve.

**A3 (advisory) — Stage 1.0–1.5 dependency chains in §4 were checked
against what each stage actually consumes and found sound.**
**Disposition: no action needed.**

**A4 (advisory) — CodeCompass citations in `decisions/0001`–`0003` were
spot-checked against the actual CodeCompass repository (ADR count, phase
file count, retro file count, the `0061` supersession pattern, the
`0066`–`0068`/`0081`–`0083` same-day/multi-pass amendment pattern,
`decisions/0049` + its own Phase 43c 8th-role contradiction, `0076`, and
`CLAUDE.md` §5's `release-phase-auditor`) and found accurate; no
fabricated or misdescribed citation found.** **Disposition: no action
needed.**

**A5 (advisory) — scope discipline holds structurally: no `docs/`,
`contracts/`, `evidence/`, `src/`, `tests/`, or `.github/workflows/` exist,
matching what `README.md` and `planning/ROADMAP.md` claim, and no
substantive software is present.** **Disposition: no action needed.**

**A6 (advisory) — every `§`-numbered cross-reference across all files
resolves to a real section; none point to a non-existent one.**
**Disposition: no action needed** (also independently confirmed by the
deterministic check in §5).

### Overall verdict (reviewer's own words, condensed)

"The governance/ADR/planning content itself is well-constructed, genuinely
simpler than CodeCompass, internally cross-referenced correctly, and
honest about isolation limits and unresolved items... However, the
repository is not ready to commit as-is: the planning documents make
specific, checkable factual claims about git state... that are
demonstrably false against the actual repository on disk... Fix B1... and
B2... before this is committed." Both are fixed as recorded above, and the
actual commit/push described in §8 criterion 8 is performed only after
this fix, not before.

## 7. Phase 1 completion requirement (restated)

Per the bootstrap prompt: Phase 1 cannot close until the complete
methodology has been dogfooded successfully on Axiom Dev itself. Concretely,
that means Stage 1.5 must have actually run — a real reconstruction, a
real comparison, real findings resolved through the real workflow — with
the "no synthetic substitute" rule from §2/§4 enforced. No stage before
1.5 marks Phase 1 complete, regardless of how much Stage 1.0–1.4 evidence
accumulates.

## 8. Stage 1.0 acceptance

Stage 1.0 (only) is Completed when, with evidence:

1. `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
   `CHANGELOG.md` exist and are mutually consistent (no contradicting
   rules).
2. `planning/ROADMAP.md` and `planning/CONTEXT.md` exist and accurately
   reflect this stage's actual state.
3. This file exists and covers Stages 1.0–1.5 to the depth in §4.
4. `planning/prompts/001-phase-1-bootstrap.md` exists with provenance and
   is verbatim.
5. `decisions/0001`–`0003` exist, are internally consistent with each
   other and with `AGENTS.md`/`CLAUDE.md`.
6. The independent review (§6) has run and its material findings are
   resolved (recorded in §6, not silently dropped).
7. The checks in §5 have been performed and their results recorded
   honestly, including gaps.
8. The foundation is committed on a dedicated branch and pushed to
   `origin`, with a PR path recorded even if the PR itself could not be
   opened programmatically (see `planning/CONTEXT.md` Outstanding issues).
9. `planning/ROADMAP.md` names Stage 1.1 as the next planned activity,
   not yet authorised to start without its own focused plan and human
   review.

Marking Stage 1.0 Completed in `planning/ROADMAP.md` itself is a human
approval action per `AGENTS.md` §11 — this plan documents that the
criteria above are met; it does not self-certify completion.

## 9. Evidence and measurement (Amendment C)

Living log: [`evidence/phase-1-log.md`](../evidence/phase-1-log.md),
started at the point of this amendment (2026-11-21) — not
back-filled for Stage 1.0, which predates it.

Tracked, where actually measurable:

- Development effort: wall-clock/turn count for substantive work units.
- Agent usage: subagent dispatches, their token counts and durations
  (available directly from this session's own dispatch notifications).
- CI/review overhead: once Stage 1.3 exists, time/cost per PR for
  deterministic checks + Codex review.
- Defects: detected by tests, detected only by independent review, missed
  by both (if later discovered), introduced by a refactor.
- Rework: plan or implementation revisions required after review.
- Documentation maintenance effort: how much a given code change's
  required doc update actually cost.
- Knowledge reuse: concrete instances where a later stage used a decision,
  contract or convention recorded by an earlier one, cited by file.
- Failure cases and unresolved uncertainty: recorded as such, not
  smoothed into a success narrative.

**Not invented:** this project has no access to real token-cost billing
figures, no wall-clock instrumentation beyond what a session can observe
directly, and no baseline from a non-Axiom comparison arm. Where a metric
in the prompt's list (e.g. "agent usage and costs") isn't actually
observable in this environment, the log says so explicitly rather than
estimating a number and presenting it as measured.

## 10. Explicit acceptance demonstrations (Amendment D)

Each demonstration below is required, real-repository evidence — a
synthetic fixture built to pass is not a substitute (prompt 002 §4,
Amendment D, final line; consistent with the retained CodeCompass "no
synthetic substitute" rule in §2 above). Status is tracked here and
updated only when real evidence exists; "Not yet demonstrated" is the
honest default, not a gap to hide.

| # | Demonstration | Produced by | Status |
|---|---|---|---|
| 1 | A fresh agent resumes development using repository knowledge alone | Stage 1.0 exit criterion, re-exercised explicitly | Not yet demonstrated |
| 2 | One requirement traced: instruction → plan → decision → implementation → verification | `contracts/documentation-schema-validator.md`, traced from `planning/prompts/001...md` §5 → `decisions/0002` → this plan's Stage 1.4 → the contract | **Partially demonstrated** — chain exists through the contract (prompt → decision → plan → contract); implementation and verification legs pending Stage 1.4 |
| 3 | A deliberately defective PR is rejected by the required CI gate | Stage 1.3, live integration piece | Not yet demonstrated — depends on Stage 1.3's live-integration blocker status (§4) |
| 4 | A meaningful refactor preserves independently established behaviour | Stage 1.4 | Not yet demonstrated |
| 5 | Knowledge placement and documentation consistency evaluated against real changes | Ongoing from Stage 1.1 onward, against each substantive change | **Partially demonstrated** — this batch's own independent review (§11) found and fixed two real placement/format inconsistencies in live Stage 1.1 content, not a synthetic exercise |
| 6 | Documentation independently reconstructed from permitted evidence | Stage 1.5 | Not yet demonstrated |
| 7 | Knowledge from earlier work reused in a later task | Cross-stage; candidate: Stage 1.4 reusing Stage 1.1's schema/placement conventions and Stage 1.2's verification procedure | Not yet demonstrated |
| 8 | Methodology overhead recorded and assessed | `evidence/phase-1-log.md` (§9), assessed at Stage 1.5 closeout | In progress from this amendment onward |

Phase 1 cannot close (§7) while any row above remains "Not yet
demonstrated" without an explicit, recorded reason the gap is acceptable
to leave open (e.g. a genuine external blocker, not a scheduling
convenience).

## 11. Independent review record — amendment + Stage 1.1 batch

Dispatched: a fresh, non-forked agent with no prior conversation context,
given the repository directly (same best-effort isolation level as §6 —
not strict; see `decisions/0003` §3). Scope: the amendment (§0, §9, §10,
`decisions/0004`, `planning/prompts/002-...md`) and Stage 1.1's first real
content (`docs/documentation-schema.md`, `docs/knowledge-placement.md`,
`docs/knowledge-reconciliation.md`, `contracts/documentation-schema-validator.md`,
and the `README.md`/`planning/CONTEXT.md`/`planning/ROADMAP.md`/`CHANGELOG.md`
updates), all uncommitted at review time.

### Findings and dispositions

**BLOCKING-1 — `authoritative_sources` entries in `docs/knowledge-placement.md`
and `docs/knowledge-reconciliation.md` used a format
(`AGENTS.md §7`, and a reference to CodeCompass's own `decisions/0094`,
which doesn't exist in this repository) that the validator contract
(`contracts/documentation-schema-validator.md`) would fail against its
own Stage 1.1 content.** **Disposition: fixed** — both front-matter
blocks now use bare, repository-relative paths only
(`docs/knowledge-placement.md`, `docs/knowledge-reconciliation.md`); the
contract itself (rules 5 and 7) was also tightened to state explicitly
that entries must be bare paths with no section suffix, that paths
outside this repository belong in prose not in this field, and that rule
7 is a refinement of rules 5/6 (matched paths/links only), not a
full-text scan that would flag a prose mention of another project's ADR
number.

**BLOCKING-2 — Amendment B's checksum-based protected-fixture mechanism
was described as "mechanical enforcement" in `decisions/0004` and this
file, when nothing in this environment actually computes or compares a
checksum automatically; it is a procedure a reviewer has to actually
perform.** The reviewer correctly identified this as the exact mislabeling
`decisions/0003` §3 was written to prevent for isolation claims — the same
standard applies to enforcement claims. **Disposition: fixed** — both
documents now call this a procedural control, name what would make it
mechanical (Stage 1.4's validator or a CI hook actually comparing the
checksum), and state plainly that it isn't that yet.

**ADVISORY — `docs/documentation-schema.md`'s manual validation record
claimed README's repository map was "found complete" against `ls` output,
but it omitted `.github/pull_request_template.md`, a real governance
file.** **Disposition: fixed** — the row was added to README.md's table,
and the validation record now says the first pass missed it and names
that this review caught the gap, rather than silently correcting the
claim to read as if it had been complete from the start.

**ADVISORY — the `docs/knowledge-reconciliation.md` worked example is a
real reconciliation with a real, verified fix, but a weak test of the
procedure's value, since the drift it found was introduced and caught
within the same session rather than surviving a session boundary.**
**Disposition: fixed (caveat added)** — the document now states this
limitation explicitly and points to Stage 1.5's independent reconstruction
as the stronger test.

**ADVISORY — Amendment A's resolution in `decisions/0004` mostly asserts
the existing plan already satisfies it, adding only one small new rule.**
**Disposition: accepted as recorded, no further action** — the reviewer
called this defensible but the thinnest of the four amendments; noted
here rather than padded with additional process to look more substantial
than it is.

**ADVISORY — `evidence/phase-1-log.md`'s subagent token/duration figures
can't be independently re-derived from repository artifacts alone, since
no raw dispatch log is retained.** **Disposition: accepted as recorded,
no further action** — the figures are in-session data available only to
the orchestrating session at the time; this is a real, named limitation
on the evidence log's own evidentiary strength, not a defect to fix.

**ADVISORY — contract rule 4 (heading match) didn't address duplicate
headings or heading level.** **Disposition: fixed** — the contract now
states explicitly that a match at any heading level counts, and duplicate
headings with the same text are not an error.

**No issues found** — all `AGENTS.md §N` and `planning/phase-01-foundation.md §N`
cross-references resolve; `decisions/0002`'s "Unresolved" item is
correctly left unedited (append-only) with its resolution placed in the
newer `docs/documentation-schema.md` instead; scope discipline holds
completely (no `src/`, `tests/`, `.github/workflows/`, or any code exists
anywhere in the tree); ADR numbering (0001–0004) is sequential with no
gaps.

### Overall verdict (reviewer's own words, condensed)

"The governance/planning layer is substantively strong... Amendments A, C,
D are genuinely satisfied with checkable content... But the two BLOCKING
findings are real: the Stage 1.1 documents already violate the format the
Stage 1.4 validator contract will enforce against them, and Amendment B's
flagship anti-circularity mechanism is labeled 'mechanical' when it is
currently only procedural — the exact mislabeling this project's own ADR
0003 was written to prevent. Fix those two before committing; everything
else is advisory polish." Both are fixed as recorded above.

## 12. Independent review record — Stage 1.2 + Stage 1.3 batch

Dispatched: a fresh, non-forked agent, same best-effort isolation level
as §6/§11. Scope: `docs/development-lifecycle.md`,
`docs/agent-isolation.md` (Stage 1.2), and
`contracts/codex-gate-policy-evaluator.md`,
`.github/scripts/policy_evaluator.py`,
`.github/scripts/tests/test_policy_evaluator.py`,
`.github/workflows/deterministic-checks.yml`,
`.github/workflows/codex-review.yml`, `.github/codex/prompts/review.md`
(Stage 1.3, deterministic piece). The reviewer ran the test suite itself
rather than trusting the claim it passed.

### Findings and dispositions

**BLOCKING — the staleness check (contract rule 5) was vacuous in the
only place it was actually wired up live.** `codex-review.yml`'s
SHA-stamping step and the evaluation step both read
`github.event.pull_request.head.sha` — the same triggering-event value —
so the comparison could never fail by construction. The reviewer
identified the real threat this missed: a GitHub Actions "re-run" replays
the *original* triggering event, including its (possibly by-then-stale)
head SHA, so a stale re-run would pass this check every time, which is
exactly the "review of an outdated commit must not authorise a later
unreviewed change" case the rule exists for. The inline comment's stated
rationale (guarding against a cross-run cached artifact) described a
threat this architecture doesn't actually have, while missing the one it
does. **Disposition: fixed** — the evaluation step now queries the PR's
live current head SHA from the GitHub API at evaluation time (a new
"Get the PR's live current head SHA" step, using `gh api .../pulls/<n>`),
independent of the triggering event payload, so a replayed stale event is
now actually caught. `contracts/codex-gate-policy-evaluator.md` rule 5
now documents this as a caller responsibility the pure function cannot
enforce by itself.

**BLOCKING — the same stamping step silently fabricated missing
`status`/`schema_version` fields** (`data.setdefault(...)` for both),
which would have converted a genuinely malformed Codex output (missing
those fields — exactly contract rule 3's `FAIL_CLOSED` case) into
something that looked like a clean completed review the moment the live
path is enabled. Not caught by the unit tests, since they call `evaluate()`
directly and never go through this wiring step. **Disposition: fixed** —
the `setdefault` calls are removed; the step now only records the SHA
actually reviewed, and a comment names the removed code explicitly so it
isn't reintroduced.

**BLOCKING — two compiled `.pyc` files were staged with no `.gitignore`
anywhere in the repository.** **Disposition: fixed** — unstaged and
deleted, `.gitignore` added (`__pycache__/`, `*.pyc`, `.pytest_cache/`).

**ADVISORY — `codex-review.yml`'s workflow-level `permissions:` block
granted `pull-requests: write` to all three jobs**, including the two
that never post a comment. **Disposition: fixed** — moved to
job-level permissions on `codex-review` only; the workflow-level block
is now `contents: read` alone.

**ADVISORY — the second Stage 1.3 blocker (required-status-check
configuration needs repository-admin access this session doesn't have)
had gone unmentioned alongside the `OPENAI_API_KEY` blocker.**
**Disposition: fixed** — both `planning/CONTEXT.md` and this file's
Stage 1.3 record (ROADMAP.md) now name it as a second, distinct gap.

**No issues found** — the 16 unit tests were re-run by the reviewer
directly and genuinely pass; `policy_evaluator.py`'s pure `evaluate()`
function faithfully implements every contract rule; the `pull_request`
(not `pull_request_target`) trigger choice and its fork-secret-withholding
rationale hold up; the `check-secret`/`codex-review` job-gating pattern is
valid; no uncontrolled execution of Codex-generated content; the
isolation-level claim in `docs/agent-isolation.md` ("every review so far
has been level 2, none level 3") was checked against §6 and §11 above and
holds; no `src/` or top-level `tests/` created prematurely; no document
claims the Codex gate "works" or is "enforced" ahead of it actually being
exercised live; `authoritative_sources` front-matter in all three new
schema'd documents uses the bare-path convention fixed in §11.

### Overall verdict (reviewer's own words, condensed)

"The docs (Stage 1.2) and the deterministic evaluator + its tests (Stage
1.3) are solid, honestly scoped, and internally consistent... But
`codex-review.yml` has two real defects (vacuous staleness check,
field-fabrication defeating fail-closed on missing status/schema_version)
that contradict its own contract and inline-comment reasoning, plus
committed `.pyc` files with no `.gitignore`. Fix those three items — all
small, mechanical fixes — before this lands." All fixed as recorded
above.
