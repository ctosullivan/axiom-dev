# Phase 1 — Foundation

Authorising prompts:
[`planning/prompts/001-phase-1-bootstrap.md`](prompts/001-phase-1-bootstrap.md)
(original bootstrap),
[`planning/prompts/002-phase-1-amend-and-implement.md`](prompts/002-phase-1-amend-and-implement.md)
(amendment, supersedes the bootstrap-only restriction and authorises full
Stage 1.0–1.5 implementation), and
[`planning/prompts/003-phase-1-corrective-amendment.md`](prompts/003-phase-1-corrective-amendment.md)
(corrective amendment: documentation-drift fixes, validator schema
strengthening, deterministic CI completion, native-Codex-review strategy
change, independent semantic review — see §17 below).
Related ADRs: [`decisions/0001`](../decisions/0001-development-governance.md),
[`decisions/0002`](../decisions/0002-knowledge-architecture.md),
[`decisions/0003`](../decisions/0003-independent-verification.md),
[`decisions/0004`](../decisions/0004-phase-1-amendment-verification-measurement-and-acceptance.md)
(partially superseded — see `decisions/0005`),
[`decisions/0005`](../decisions/0005-native-codex-review-and-deferred-automated-gate.md).

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
| 1 | A fresh agent resumes development using repository knowledge alone | `evidence/phase-1-log.md` 2026-11-21 entry | **Demonstrated** — correctly reconstructed project/methodology/ADRs/status from repo contents alone, and caught a real transient CONTEXT.md/ROADMAP.md staleness mid-session (fixed in the same commit as this row) |
| 2 | One requirement traced: instruction → plan → decision → implementation → verification | The "reject a document missing a required section" requirement: `planning/prompts/001-...md` §5 → `decisions/0002` → this plan's Stage 1.4 → `contracts/documentation-schema-validator.md` rule 4 → `src/axiom_validator/rules.py`'s `check_required_sections` → `tests/test_axiom_validator.py`'s `TestMissingSection` (passing) → `evidence/stage-1.4-baseline.md`/`stage-1.4-refactor.md` | **Demonstrated** — full chain, every link a real file, not asserted |
| 3 | ~~A deliberately defective PR is rejected by the required CI gate~~ — **requirement changed by `decisions/0005`**: Phase 1 no longer requires an enforceable automated gate; it requires a real native Codex GitHub PR review on an actual PR, with findings dispositioned | Stage 1.3 (deterministic piece, done); native-review piece, §17 below | Not yet demonstrated — depends on a human opening the PR this session cannot open (no `gh`/token) and triggering native Codex review on it; see §17 |
| 4 | A meaningful refactor preserves independently established behaviour | Stage 1.4 (`evidence/stage-1.4-refactor.md`) | **Demonstrated** — real structural split, identical before/after test results, independently verified |
| 5 | Knowledge placement and documentation consistency evaluated against real changes | §11 (Stage 1.1 format fix), Stage 1.4 dogfooding (real ADR-citation defect), Stage 1.5 reconstruction (missing-doc gap + 2 Limitations fixes) | **Demonstrated** — four independent, real (non-synthetic) instances across three different stages |
| 6 | Documentation independently reconstructed from permitted evidence | Stage 1.5 (`evidence/stage-1.5-reconstruction.md`) | **Demonstrated** — restricted-evidence reconstruction, compared, 2 real findings fixed, 1 correctly accepted as out-of-scope-for-the-evidence-given |
| 7 | Knowledge from earlier work reused in a later task | Stage 1.4 reused Stage 1.1's documentation-schema convention (every Stage 1.4 evidence/contract document carries the front-matter format Stage 1.1 defined, and is itself validated by the Stage 1.4 tool against that convention) and Stage 1.2's lifecycle/isolation vocabulary (every review record names its isolation level using Stage 1.2's taxonomy) | **Demonstrated** — concrete, citable instances, not just a stated intention |
| 8 | Methodology overhead recorded and assessed | `evidence/phase-1-log.md` (recorded); `evidence/phase-1-closeout.md` + §16 (assessed) | **Demonstrated** |

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

## 13. Independent review record — Stage 1.4 initial implementation

Per `decisions/0004` (Amendment B), the initial validator implementation
was independently reviewed *before* the pre-refactor baseline was locked.
Full findings, fixes, and the locked checksums/test output live in
`evidence/stage-1.4-baseline.md` (verification outcomes belong in
`evidence/`, not duplicated at length here — `AGENTS.md` §7). Summary:
the reviewer re-ran the tests and re-computed checksums rather than
trusting the claims, confirmed the real-document dogfooding finding
against `git diff`, and found two real, demonstrated-with-counter-examples
blocking defects (an unenforced "no paths outside the repository" rule,
and a fenced-code-block false positive in heading detection) — both fixed
with regression fixtures and tests, not just prose. Isolation level:
best-effort, same as §6, §11, §12.

## 14. Independent review record — Stage 1.4 refactor

The behaviour-preserving refactor (splitting `src/axiom_validator.py`
into `parsing.py`/`rules.py`/`reporting.py`/`__init__.py`) was
independently reviewed against the locked baseline. Full findings live
in `evidence/stage-1.4-refactor.md`. Summary: the reviewer re-computed
every protected checksum (exact match), re-ran the 14-test suite itself
(exact match), diffed the old monolith against the new modules line by
line and confirmed a genuine separation of concerns with identical rule
ordering (including both prior bug fixes carrying over unchanged), and
confirmed the one CLI-invocation change (`python3 -m axiom_validator`
instead of direct script execution) is not a contract violation since
the contract specifies no CLI shape. **No blocking findings.** Isolation
level: best-effort, same as §6, §11, §12, §13.

Stage 1.4 is now complete with evidence: initial implementation built,
contracted, independently reviewed, fixed; real documentation defect
found and fixed via dogfooding; baseline locked; refactor performed,
independently reviewed, before/after behaviour verified identical. Per
`AGENTS.md` §11, marking it Completed in `planning/ROADMAP.md` is still a
human approval action — this record documents the evidence for that
approval, it does not self-certify.

## 15. Stage 1.5 — independent documentation reconstruction

Full record: `evidence/stage-1.5-reconstruction.md` (verification
outcomes belong in `evidence/`, not duplicated at length here). Summary:
a fresh agent was given a restricted permitted-evidence set (validator
source, tests, contract, Stage 1.4 evidence files — explicitly excluding
`docs/`, `planning/`, `decisions/`, `AGENTS.md`, git history) and asked
to reconstruct the validator's purpose, architecture, usage, and
limitations blind, then compare against the real `docs/axiom-validator.md`.
The reconstruction was accurate on every verifiable point. The
comparison found three real items: one unverifiable-but-true provenance
claim (correctly classified by the agent as a gap in its restricted
evidence, not an error — no fix needed); two real non-goals missing
from the doc's own Limitations section (fixed); and one true claim
placed in the wrong section — project-roadmap context mixed into a list
that should only describe the validator's own behavioural limitations
(fixed, and the underlying claim was independently verified — `grep`
confirmed no workflow references `axiom_validator` — before being kept,
not merely moved). Isolation level: best-effort, same as all prior
reviews; named explicitly in `evidence/stage-1.5-reconstruction.md`'s
"Isolation honesty note."

This satisfies Amendment D demonstration 6
(`docs/axiom-validator.md`/`planning/phase-01-foundation.md` §10,
updated to Demonstrated) and is also a second real instance of
demonstration 5 (documentation consistency evaluated against real
changes, not synthetic ones).

## 16. Phase 1 closeout assessment

Full record: `evidence/phase-1-closeout.md`; retrospective:
`planning/retros/phase-1-stages-1.0-through-1.5.md`.

**Verdict: partially complete, with two named, real, currently-external
blockers. Phase 1 stays open — not marked Completed.** An independent
assessment (fresh dispatch, no prior involvement, best-effort isolation
per the same standard as every other review in this plan) re-verified
all 17 Definition-of-Done items
(`planning/prompts/002-phase-1-amend-and-implement.md` §11) and all 8
Amendment D rows (§10 above) by re-running tests and re-checking files
itself: 15 of 17 DoD items MET, 1 partially met (validator tests pass
locally but aren't wired into CI yet), 1 not met (the live Codex gate —
no `OPENAI_API_KEY`, no `gh`, no PR ever opened, and the project's own
"no synthetic substitute" rule correctly disqualifies the unit-test-level
evidence from counting). 6 of 8 Amendment D rows fully demonstrated; row
3 correctly left open; row 8 is this assessment.

The assessment also found and this session fixed two staleness issues
no prior review's scope had covered — `CONTRIBUTING.md`'s testing
section still read as a future-tense placeholder after Stage 1.4
shipped, and `planning/CONTEXT.md` carried a self-reference that went
stale the instant its own commit landed. Explicitly **not** found:
anything describing the Codex gate, branch protection, or a required
check as working despite the known blockers; anything marked Completed
in `planning/ROADMAP.md` without human sign-off; any "mechanical"
claim for what is actually procedural.

Per `AGENTS.md` §11, this record documents the evidence for a human to
decide what to mark Completed — it does not self-certify, and
`planning/ROADMAP.md` is not changed to say "Completed" by this session.

## 17. Corrective amendment (prompt 003, 2026-11-21)

Authorising prompt:
[`planning/prompts/003-phase-1-corrective-amendment.md`](prompts/003-phase-1-corrective-amendment.md).
This section amends — does not replace — §0 and §9/§10 above, per
`AGENTS.md` §3's append-and-supersede convention applied to plans as well
as ADRs. Prompt 003 required seven lettered amendments (also labelled
A–G, in a **separate sequence from `decisions/0004`'s Amendments A–D** —
the two are not the same list; this section always writes "prompt 003
Amendment X" or "prompt 002 Amendment X" where the letter alone would be
ambiguous).

**Prompt 003 Amendment A — Codex review strategy.** Resolved by
`decisions/0005`: Phase 1's independent-Codex-review requirement is now
satisfied by a **native Codex GitHub PR review** of an actual opened PR
(no `OpenAI API key, no self-hosted Action), not the API-backed workflow
`decisions/0004` originally specified. That workflow
(`.github/workflows/codex-review.yml`) is moved to
`.github/deferred/codex-review.yml` so GitHub Actions no longer lists its
gated skip as part of normal CI status for new commits; its policy
evaluator and contract (`.github/scripts/policy_evaluator.py`,
`contracts/codex-gate-policy-evaluator.md`, both independently reviewed
and locally tested — `evidence/phase-1-log.md`) are preserved unmodified
as reusable material, not deleted. **This session still cannot open a
GitHub PR** (`gh` confirmed not installed, no passwordless `sudo` to
install it, no token) — re-verified directly in this session, not
assumed from the prior one. The acceptance criterion therefore stays
open: this amendment changes *what* would satisfy it, not whether it is
currently satisfied. See §18 for the exact human hand-off this produces.

**Prompt 003 Amendment B — documentation drift.** Re-inspected directly
(not assumed from the prior closeout) and confirmed still present:

- **B1** — `AGENTS.md` §8 still read "Nothing in this repository yet
  requires this in practice," false since Stage 1.4 shipped. Corrected to
  describe the actual, already-enforced requirement with real file
  references (`AGENTS.md` §8, this change).
- **B2** — `CONTRIBUTING.md`'s "Making a change" §5 still read "for now
  (pre-Stage-1.4, no source code yet)," even though that same document's
  own "Testing requirements" section (further down) had already been
  corrected in the Phase 1 closeout — a real instance of the exact
  partial-reconciliation risk prompt 003 names. Corrected in this change.
- **B3** — `docs/knowledge-placement.md`'s "Enforcement classes" and
  "Reconciliation hook" sections said "once Stage 1.4's validator
  exists" / "checked by hand" as if the validator did not yet exist,
  although it has existed and been dogfooded since Stage 1.4. Rewritten
  to the six-level distinction prompt 003 B3 requires (policy defined /
  mechanism implemented / locally tested / executed by CI / enforced as a
  required merge condition / semantic-editorial manual review), stating
  plainly which level each control in this project is actually at —
  including that **sequential ADR numbering is not mechanically
  enforced** by anything in this repository (a human/reviewer convention
  only), which the prior wording never claimed but also never explicitly
  ruled out.
- **B4** — wider reconciliation pass across README, development-lifecycle,
  agent-isolation, documentation-schema, knowledge-reconciliation,
  axiom-validator docs, ROADMAP, CONTEXT, and both governance files:
  performed by direct read of each file's current text against the
  repository's current state (not a restatement of the prior closeout).
  No further current-state drift found beyond B1–B3 in this pass; this is
  recorded as what was actually inspected, not a blanket "reconciled"
  claim — see the independent review record below for a second,
  independent pass over the same files.

**Prompt 003 Amendment C — strengthen validator schema validation.**
`contracts/documentation-schema-validator.md` gained an explicit,
clearly-marked contract amendment (new rules 10–14, appended — the
original 9 rules are untouched) requiring: `audience`/`purpose` to be
non-empty strings; `required_sections`, `authoritative_sources`,
`acceptance_criteria` to be correctly typed (lists of strings);
`required_sections` and `acceptance_criteria` to be non-empty;
`authoritative_sources` may legitimately be an empty list (no placeholder
entries required or accepted — an empty list already passes every
existing per-entry check vacuously, which is the intended behaviour, not
a gap); and a new, minimal **governed-documents manifest**
(`docs/governed-documents.txt`) under which a listed path with no
front-matter is `FAIL`, not `SKIPPED` — closing the "delete the schema to
silently bypass its checks" gap named in the prompt. Implemented in
`src/axiom_validator/rules.py` (`check_field_types_and_content`,
`load_governed_manifest`) and wired into `validate_file` in
`src/axiom_validator/__init__.py`, with new fixtures under
`tests/fixtures/` and a **new, separate test file**
(`tests/test_axiom_validator_schema_content.py`) rather than editing the
checksum-protected `tests/test_axiom_validator.py` or any of its
protected fixtures — those files and their recorded checksums in
`evidence/stage-1.4-baseline.md` are confirmed unchanged (see §19
"Independent review record — corrective amendment batch").

**Prompt 003 Amendment D — semantic documentation review.** Performed
against `docs/axiom-validator.md`, `docs/knowledge-placement.md`, and
`docs/development-lifecycle.md`, following the exact seven-step
VERIFIED/FAILED/UNCERTAIN procedure prompt 003 specifies, by a fresh,
best-effort-isolated reviewer instructed to inspect the documents'
declared authoritative sources directly rather than paraphrase the
documents themselves. Full record: §19 below.

**Prompt 003 Amendment E — deterministic CI completion.**
`.github/workflows/deterministic-checks.yml` gained two new jobs:
`axiom-validator-tests` (installs `requirements.txt`, runs
`tests/test_axiom_validator.py` and the new
`tests/test_axiom_validator_schema_content.py`) and
`validate-governed-documentation` (runs the validator CLI against every
path in `docs/governed-documents.txt`, failing the job on any
`FAIL`/`INVALID_SCHEMA`). Neither requires a secret. Semantic findings
(prompt 003 Amendment D) are explicitly **not** wired into CI — they are
human/agent-judgement findings recorded in `evidence/`, not a mechanical
check, per `docs/knowledge-placement.md`'s enforcement-class distinction.

**Prompt 003 Amendment F — refactor re-confirmation.**
`evidence/stage-1.4-refactor.md` was not rewritten; a second, independent
re-confirmation pass re-derived its claims directly against git history
and current checksums rather than trusting the prior review, and recorded
the three required distinctions (tests/fixtures demonstrate equivalence
under existing coverage, not universal semantic equivalence; the
programmatic interface is preserved under that coverage; the CLI
invocation shape changed and was never contract-protected) as an explicit
addendum. Full record: §19 below.

**Prompt 003 Amendment G — schema value assessment.** A focused,
three-example assessment (`evidence/schema-value-assessment.md`) compares
each named document's actual schema against its actual content, using
the four-way distinction prompt 003 requires (schema-enforced /
schema-encouraged-not-verified / general-planning-introduced /
independent-review-corrected), and records the open research hypothesis
verbatim as **not** a Phase 1 completion requirement. Written after, and
using the real findings of, the Amendment D semantic review — not before
it, since G explicitly depends on D's actual results, not a prediction of
them.

## 18. Revised Phase 1 Definition of Done (prompt 003 §12)

This is the definition of done prompt 003 requires, tracked here as its
own table rather than silently replacing §7/§8's prior criteria (which
remain historically accurate for what Stage 1.0 alone required). Status
below reflects §19/§20's findings after both independent dispatches
(review + confirmation) completed — filled in once there was real
evidence to assess, not asserted ahead of it. **Final tally: 10 of 16
MET, 1 locally-verified-only, 5 open.**

| # | Criterion | Status |
|---|---|---|
| 1 | Governance, roadmap, ADRs and preserved planning prompts are coherent | **Met** — §19's one real gap (`planning/CONTEXT.md`) fixed and independently re-confirmed |
| 2 | Previously identified documentation drift has been corrected | **Met** — B1–B4 plus the additional items §19 found, all fixed and re-confirmed |
| 3 | Documentation schemas are valid and meaningful for governed documents | **Met** — Amendment C implemented, independently stress-tested with 6 fresh counter-examples, zero survived |
| 4 | Deterministic schema validation and tests operate in GitHub Actions | **Locally verified only** — the exact CI commands run correctly in this session (twice, by two independent dispatches); no actual GitHub Actions run has been triggered, since this session cannot push a commit through a live Actions run beyond what's already on `origin` |
| 5 | Semantic documentation acceptance criteria evaluated against real source evidence | **Met** — all 3 named documents reviewed per the 7-step procedure; real gaps found and fixed, not a clean pass rubber-stamped |
| 6 | Knowledge placement evaluated on actual project changes | **Met** — `docs/knowledge-placement.md` itself was evaluated and corrected against real repository state (B3, and §19's further findings) |
| 7 | Validator refactoring evidence independently confirmed | **Met** — re-derived from git history independently, including a from-scratch re-run of the pre-refactor test suite |
| 8 | Refactoring limitations and unprotected interfaces recorded | **Met** — CLI-invocation qualification and its contract-design implication recorded in §19 and `evidence/stage-1.4-refactor.md` |
| 9 | Independent documentation reconstruction demonstrated, isolation limitations explicit | **Met** — Stage 1.5, unchanged by this amendment |
| 10 | Native Codex GitHub review actually performed on the relevant PR | **Open — blocked.** No PR exists (no `gh`/token, re-confirmed); see `decisions/0005` and §20 |
| 11 | Significant Codex findings resolved or dispositioned by the human | **Open** — depends on #10 |
| 12 | Reviewed commit and review evidence recorded | **Open** — depends on #10 |
| 13 | Automatic API-backed Codex CI gate explicitly deferred in accepted ADRs | **Met** — `decisions/0005` |
| 14 | Process overhead and unresolved research hypotheses documented | **Met** — `evidence/phase-1-log.md`; hypothesis recorded verbatim in `evidence/schema-value-assessment.md` |
| 15 | Independent closeout review supports Phase 1 acceptance | **Open** — the two dispatches in §19 were narrowly scoped (named checks; confirmation of named fixes), not a holistic closeout judging whether this batch deserves acceptance. The confirmation reviewer said so explicitly in its own report: it "does not itself constitute the separate, fully-independent closeout dispatch that §20 says is still outstanding." Not worked around — recorded open. |
| 16 | Human approval obtained before marking Phase 1 complete or merging | **Open, deliberately not sought by this session** as a substitute for human action — remains a human action per `AGENTS.md` §11 |

Items 10–12 cannot be met from inside this session without a human first
opening the PR this session has no credentials to open. This is recorded
as an open item, not worked around.

## 19. Independent review record — corrective amendment batch (prompt 003)

Dispatched: a fresh, non-forked `general-purpose` agent with no prior
conversation context, given the repository directly and the exact
four-check brief below (Amendment B documentation drift, Amendment C
validator strengthening, Amendment D semantic review of three named
docs, Amendment F refactor re-confirmation) — best-effort isolation,
level 2 of `docs/agent-isolation.md`'s taxonomy (fresh context, same
operator/session line), not mechanically enforced, named that way in the
reviewer's own report rather than overclaimed. 60 tool uses, 187,061
tokens, 602.2s — logged in `evidence/phase-1-log.md`.

**This review's first pass caught a real, important process failure
before anyone else did: §17/§18 of this plan and `evidence/schema-value-assessment.md`
had been *written as if §19/§20 and that file already existed*, when
they did not yet.** The reviewer flagged this explicitly as BLOCKING
rather than treating the surrounding prose as adequate — exactly the
"writing done language before doing the thing" failure mode this
project's own Phase 1 retrospective (`planning/retros/phase-1-stages-1.0-through-1.5.md`,
"Unexpected findings" §1) already named as its single most important
finding, recurring a third time. This section and §20, and
`evidence/schema-value-assessment.md`, are the fix — written after the
review, from the review's own findings, not before it.

**Findings and disposition** (condensed; the reviewer's full report is
the primary record — this section states what was found and what this
session did about it, not a restatement of methodology):

- **BLOCKING — `planning/CONTEXT.md` was never touched in this
  corrective pass** and had gone actively stale against `decisions/0005`
  (framing `OPENAI_API_KEY` and branch-protection configuration as live
  blockers, when Amendment A removed both as Phase 1 requirements; citing
  `decisions/0001`–`0004` only, omitting `0005`; telling the reader to
  next run the now-deferred live-gate test matrix). **Fixed**: rewritten
  to reflect `decisions/0005` accurately — see the current file.
- **BLOCKING — this plan cited `§19`/`§20` and `evidence/schema-value-assessment.md`
  before they existed** (16 dangling cross-references, confirmed by the
  reviewer via `grep`). **Fixed**: this section, §20, and that evidence
  file now exist, written from the review's actual findings.
- **ADVISORY — `decisions/0005` claimed `contracts/codex-gate-policy-evaluator.md`
  was "preserved as-is"/"without modification," but it required one
  real (trivial) path-reference edit.** **Fixed**: wording corrected in
  `decisions/0005` to state precisely what changed and why.
- **ADVISORY — contract rule 12 (`required_sections` non-empty) applies
  to every document with front-matter, not only `docs/governed-documents.txt`
  entries, which is broader than prompt 003's literal "governed
  substantive documents" phrasing.** **Disposition: accepted as a
  documented, deliberate generalisation, not a defect** — a scope note
  explaining why (rule 3 already makes the field mandatory for any
  front-matter-bearing document; narrowing rule 12 to the manifest would
  make it weaker than rule 3) was added to
  `contracts/documentation-schema-validator.md` rather than changing the
  behaviour.
- **No BLOCKING findings in Check 2** (validator strengthening): the
  reviewer independently re-ran the full test suite (23/23 pass, matched
  exactly), recomputed all 11 protected-baseline checksums (all matched
  `evidence/stage-1.4-baseline.md` exactly — the historical baseline was
  not altered), and constructed six of its own counter-examples beyond
  this session's fixtures, none of which defeated rules 10–15.
- **FAILED (Check 3, `docs/axiom-validator.md`) — three concrete,
  code-contradicted claims**: (1) "no file-reading... lives here"
  (rules.py) stated in the same bullet naming `load_governed_manifest`,
  which reads a file; (2) the `__init__.py` call-order description
  omitted the `check_field_types_and_content` step; (3) the documented
  `validate_file(Path("README.md"), Path("."))` usage example
  **reproducibly failed** (`FAIL` with 11 spurious "outside the
  repository" errors) because `validate_file` required a pre-resolved
  `repo_root` and the example didn't supply one. **All three fixed**:
  the module-level claim corrected; the call-order description now names
  the step; and — the substantive fix — `validate_file` now resolves
  `repo_root` internally (`src/axiom_validator/__init__.py`), a real
  latent defect present identically in the pre-refactor monolith (not a
  refactor regression, confirmed via Check 4), fixed rather than merely
  documented around. Re-verified: the exact documented example now
  produces the documented output; full suite re-run, still 23/23;
  protected checksums re-confirmed unchanged after the fix.
- **FAILED/UNCERTAIN (Check 3, `docs/knowledge-placement.md`) —
  two acceptance criteria not actually met as literally written**: the
  Placement table's "Historical narrative" row named two destinations,
  not one; enforcement levels 1–3 described what exists without stating
  blocking/advisory; the "checked against `docs/documentation-schema.md`"
  claim had no itemized record, unlike `docs/documentation-schema.md`'s
  own worked example for `README.md`. **All three fixed**: the row now
  names one primary location with an explanatory note; levels 1–3 each
  state "Advisory only" explicitly; a "Manual validation record" section
  was added, itemized per criterion, in the same style as
  `docs/documentation-schema.md`'s.
- **FAILED/partial (Check 3, `docs/development-lifecycle.md`) — the
  phase-acceptance procedure named an actor for only 1 of its 5 steps.**
  **Fixed**: each of the 5 steps now opens with an explicit "Who:"
  statement.
- **No BLOCKING findings in Check 4** (refactor re-confirmation): the
  reviewer independently identified the pre-refactor commit (`07d5548`)
  from `git log`, diffed it line-by-line against the current package,
  confirmed the check ordering is unchanged and the only delta since the
  refactor is the later Amendment C addition in exactly the position the
  contract specifies, and — going beyond re-reading
  `evidence/stage-1.4-refactor.md` — physically extracted the `07d5548`
  monolith via `git show` into an isolated layout and re-ran
  `tests/test_axiom_validator.py` against it directly, reproducing
  14/14 pass independently rather than taking the recorded number on
  trust. The three required distinctions (tests/fixtures demonstrate
  equivalence under existing coverage, not universal semantic
  equivalence; the programmatic interface is preserved under that
  coverage, now with one later-added optional kwarg from Amendment C;
  the CLI invocation shape changed and was never contract-protected,
  with the explicit implication recorded: a contract that means to
  protect a CLI shape must say so, since silence here let a real change
  pass unflagged) are adopted into this record as the reviewer stated
  them, not restated independently.

**What this review did not need to re-litigate**: Amendment A
(`decisions/0005`) and Amendment E (CI completion) were not separately
re-verified by this dispatch beyond what Checks 1–2 already covered
(the CI workflow's actual content, the deferred file's real location);
no finding challenged either.

**Confirmation dispatch (second independent pass, same day):** 71,421
tokens, 17 tool uses, 77.5s. After the fixes above were made, a second
fresh, non-forked agent — same best-effort isolation level as the first,
explicit about not being a fully independent closeout (see §20) — was
given the 8 specific fixes above and told to verify each by direct
re-execution, not by reading the surrounding prose. Result: **all 8
CONFIRMED** — `planning/CONTEXT.md`
read in full and found consistent with `decisions/0005`; §19/§20 found
to exist with coherent section numbering (`grep -n "^## "` through §20);
`evidence/schema-value-assessment.md` confirmed to exist and `PASS` the
validator; `docs/axiom-validator.md`'s three fixes confirmed, including
re-running the exact documented usage example and getting the documented
`PASS` output; `docs/knowledge-placement.md`'s Placement-table/
enforcement-level/validation-record fixes confirmed by direct read;
`docs/development-lifecycle.md`'s five `Who:` statements confirmed via
`grep`; the full test suite re-run a third time (23/23); all 11 protected
baseline checksums re-confirmed exactly matching; the governed-document
CI command re-run directly with all 9 files `PASS`. One nuance recorded
by the reviewer: the `__init__.py` call-order fix describes the
`check_field_types_and_content` step in prose without quoting that exact
identifier — the reviewer separately confirmed the identifier is real
and the description matches it in substance and position, and counted
the fix as real, not cosmetic.

## 20. Corrective-amendment batch status (prompt 003)

**Not yet independently closed out as a whole — this section records
status, not a self-certified completion.** Every BLOCKING and FAILED
finding from §19 has a recorded fix, re-verified by this session (re-run
test suite, re-checked checksums, re-run the specific failing example)
immediately after each fix — but per `AGENTS.md` §6, a phase/batch
closeout needs its *own* independent check that the fixes actually hold,
not just the fixing session's word that they do. That further check has
not yet run as a separate dispatch; §18's DoD item 15 ("an independent
closeout review supports Phase 1 acceptance") stays open for that reason,
not only for the native-Codex-review gap.

Status of this corrective batch's own objectives, honestly, against
prompt 003 §13's reporting list:

- **Plan/ADR amendments** (§17 above, `decisions/0005`): done.
- **Documentation drift corrected** (Amendment B, B1–B4): done, including
  one real instance (`planning/CONTEXT.md`) this session's own first pass
  missed and the independent review caught.
- **Schema-validation strengthening** (Amendment C): done, independently
  verified against the protected baseline and six fresh counter-examples
  with zero surviving defects.
- **Deterministic CI completion** (Amendment E): done locally (new
  workflow jobs run the exact commands they specify, verified by running
  them directly in this session); **not independently verified against
  an actual GitHub Actions run** — this session cannot trigger one. This
  is DoD item 4's explicit limitation, not a claim that it has been.
- **Semantic documentation review** (Amendment D): done against all
  three named documents, and — unusually for this project's prior
  reviews — it actually found and this session fixed real, reproducible
  defects rather than confirming a clean draft; see `evidence/schema-value-assessment.md`
  for what this implies about the schema's own demonstrated value
  (Amendment G).
- **Refactor re-confirmation** (Amendment F): done, independently,
  including a from-scratch re-run of the pre-refactor test suite against
  the actual extracted pre-refactor file.
- **Native Codex GitHub PR review** (Amendment A's new requirement):
  **not performed** — no PR exists; this session still cannot open one.
  Stays open per `decisions/0005` and §18 items 10–12.
- **Phase 1 acceptance**: **not recommended yet by this session** — a
  human still needs to open the PR, trigger native Codex review,
  disposition its findings, and decide what to mark Completed
  (`AGENTS.md` §11). This corrective batch is ready for that human step;
  it does not substitute for it.

## 21. Documentation schema and roadmap amendment (prompt 004)

Authorising prompt:
[`planning/prompts/004-documentation-schema-and-roadmap-amendment.md`](prompts/004-documentation-schema-and-roadmap-amendment.md).
New ADR: [`decisions/0006`](../decisions/0006-companion-schema-files.md).
This section amends — does not replace — the plan above, same
append-and-supersede convention as §17. Prompt 004 required seven
lettered amendments (A–G, a **third, separate sequence** from both
`decisions/0004`'s Amendments A–D and prompt 003's Amendments A–G —
always written "prompt 004 Amendment X" where ambiguous).

**Prompt 004 Amendment A — separate documentation from its schema.**
Resolved by `decisions/0006`: every governed/schema-bearing document's
schema moves from embedded front-matter to a companion
`<document>.md.schema.yaml` file, computed deterministically from the
document's own path (no registry). Implemented in
`src/axiom_validator/{parsing,rules,__init__}.py`; contract-first per
the "Contract revision" section added to
`contracts/documentation-schema-validator.md` before the implementation
changed.

**Prompt 004 Amendment B — migrate existing documentation.** 15 real
documents (`README.md`, 6 under `docs/`, 2 under `contracts/`, 5 under
`evidence/`, 1 retrospective) and 20 test fixtures migrated; 4 files
(`planning/prompts/001`–`004`) correctly excepted as a different,
unrelated front-matter convention (provenance metadata, not a
documentation schema). Full itemised record, including the
`git diff --stat` verification that every real document's Markdown body
is byte-for-byte unchanged apart from front-matter removal:
`evidence/schema-migration.md`.

**Prompt 004 Amendment C — adapt the documentation validator.** New
contract revision rules 16–27 (companion-path lookup, missing-schema
SKIPPED/FAIL split, embedded-front-matter reintroduction detection,
orphaned-schema detection) implemented without replacing the validator's
modular architecture — `parsing.py`/`rules.py`/`__init__.py` each
changed in place, `reporting.py`/`__main__.py` unchanged. The public CLI
and `validate_file`/`main` call shapes are preserved; their *return
values* for previously-front-matter-bearing documents intentionally
change, as an authorised contract evolution, not a silent compatibility
break. One real latent bug was found and fixed during this work, before
any independent review: `find_orphaned_schemas` run against the real
repository root would have flagged the deliberately-orphaned test
fixture on every future CI run, forever — fixed by excluding `tests/`
from the repo-wide scan by default (`rules.find_orphaned_schemas`).

**Prompt 004 Amendment D — tests and CI.** All 12 required test
scenarios covered: valid document (existing), missing schema for a
governed document (existing, retargeted), missing schema for a
non-governed document (existing, retargeted + renamed
`no_frontmatter.md` → `no_schema.md`), malformed YAML (existing,
retargeted), missing required fields / incorrect field types / empty
required values (existing, retargeted — 5 fixtures), missing required
headings / broken authoritative-source references / links escaping the
repository / existing ADR-reference behaviour (existing, retargeted — 4
fixtures), orphaned schemas (new fixture + new test), accidental
embedded front-matter (new fixture + new test). 27/27 tests pass (up
from 23 before this amendment — independently recounted, since the
first draft of this sentence said 26/3 and was internally inconsistent
on its own arithmetic: `git show HEAD:tests/test_axiom_validator.py`
had 14 test methods and
`git show HEAD:tests/test_axiom_validator_schema_content.py` had 9,
baseline 23; the 4 net-new methods are
`TestEmbeddedFrontmatterReintroduced` (1),
`TestOrphanedSchema` (2), and `TestArchiveEntryLinkVerification` (1,
actually introduced by Amendment F below, not D) — caught by
independent review, not self-corrected first).
`.github/workflows/deterministic-checks.yml`'s existing
`axiom-validator-tests` and `validate-governed-documentation` jobs
needed no structural change — the same commands now exercise the new
convention, including the orphan scan, which runs automatically as a
side effect of `main()`'s existing batch pass. No `OPENAI_API_KEY` or
paid invocation required, unchanged.

**Prompt 004 Amendment E — expand the roadmap.** `planning/ROADMAP.md`
rewritten from a detailed Stage 1.0–1.5 record into a concise overview
(status table + Phase 1 summary pointing here for detail + Phases 2–4
as explicitly-labelled proposals, no invented dates/benefits/results).
The detailed Phase 1 history this replaced is not lost — it already
lived in this file (§0–§20), which the new roadmap links to rather than
duplicates.

**Prompt 004 Amendment F — establish phase archiving.** Procedure
documented in `docs/phase-archiving.md` (schema-governed); index created
at `planning/archive/README.md` (schema-governed, currently empty).
**Phase 1 is explicitly not archived** — `docs/phase-archiving.md`
Non-goals states this plainly, matching prompt 004 §9's restriction.
The procedure's "archive entries link to real artifacts" verification
claim was **tested**, not merely asserted: a fixture shaped like a
future archive entry, with one deliberately broken link
(`tests/fixtures/invalid/archive_entry_broken_link.md`), confirms the
existing validator's link-resolution check catches it
(`TestArchiveEntryLinkVerification`) — proving the reused mechanism
works without fabricating a completed phase to archive for real.

**Prompt 004 Amendment G — documentation and governance reconciliation.**
`decisions/0006` documents the original front-matter rationale
(quoted, not restated as though never true), the readability
disadvantage that motivated reversing it, the companion-file
alternative, the explicit file-maintenance cost, why deterministic
validation's role is unchanged in kind, and why semantic review remains
necessary. `docs/documentation-schema.md` (Convention section),
`docs/axiom-validator.md` (Architecture/Usage/Limitations),
`docs/knowledge-placement.md` and `docs/knowledge-reconciliation.md`
(prose references) updated to describe current policy accurately;
`decisions/0002`'s Unresolved item annotated (not edited in substance)
to point to `decisions/0006` for continuity. `planning/prompts/004-...md`
itself preserved verbatim with provenance, alongside 001–003.

**Preserved, per prompt 004 §11:** `decisions/0005`'s native-Codex-review
decision is unaffected by this batch — no `OPENAI_API_KEY` requested,
`.github/deferred/codex-review.yml` still deferred, no claim of
automated AI merge enforcement anywhere in this batch's changes.

## 22. Independent review record — documentation schema and roadmap batch (prompt 004)

Dispatched: a fresh, non-forked `general-purpose` agent with no prior
conversation context, given the repository directly and a four-check
brief (migration correctness, validator behaviour, roadmap/archiving,
documentation/governance reconciliation) — best-effort isolation, level
2 of `docs/agent-isolation.md`'s taxonomy, named that way in the
reviewer's own report. 50 tool uses, 131,094 tokens, 286.3s.

**No BLOCKING findings in any of the four checks.** The reviewer went
beyond re-reading this plan's and `evidence/schema-migration.md`'s own
claims: it independently re-ran `git diff --stat` on all 15 migrated
real documents (not just the 7-file sample this plan cited), confirmed
3+ documents' companion-schema content byte-for-byte against the
deleted front-matter, constructed 4 of its own adversarial test
scenarios beyond this project's existing fixtures (a schema file that's
valid YAML but a list, not a mapping; a document with *both* embedded
front-matter and a companion file present simultaneously, confirming no
silent fallback; `--repo-root` resolution invoked from a subdirectory;
an orphaned schema created in `/tmp` outside the `tests/` exclusion, to
confirm the exclusion is scoped correctly and not simply "always skip
orphans"), cross-checked `decisions/0006`'s quoted "original rationale"
against `git show HEAD:docs/documentation-schema.md`'s actual prior
text to rule out strawmanning, and confirmed `decisions/0002`'s edit is
annotation-only via `git log -p`.

**Two ADVISORY findings, both bookkeeping/narrative inaccuracies in
this plan's own and `evidence/schema-migration.md`'s record-keeping —
neither affecting actual behaviour, test results, or decision
substance:**

1. This plan's §21 Amendment D paragraph originally claimed "27/27
   tests pass (up from 26 before this amendment; the net-new count is 3
   test methods...)" — internally inconsistent on its own arithmetic
   (26 + 3 ≠ 27) and the baseline was wrong. The reviewer recounted
   directly (`git show HEAD:tests/test_axiom_validator*.py` against the
   working tree): actual baseline 23, actual net-new 4 methods
   (`TestEmbeddedFrontmatterReintroduced`,
   `TestOrphanedSchema` × 2, `TestArchiveEntryLinkVerification`).
   **Fixed** — §21 above now states the corrected figures and the
   correction itself, rather than silently replacing the wrong number.
2. `evidence/schema-migration.md` stated "all 9 governed documents
   report `PASS`" in its Verification section, written before Amendment
   F added `docs/phase-archiving.md` and `planning/archive/README.md`
   to the manifest (11 entries as of this plan's current state). **Not
   actually wrong at the time it was written** (a timing snapshot, not
   a fabrication) but stale relative to the finished state. **Fixed** —
   that file now states both counts and why they differ.

**Minor observation, not actioned as a defect:**
`planning/prompts/004-...md` was untracked in git at review time —
expected, since nothing in this batch had been committed yet; resolved
by the commit this record accompanies.

**Verdict (reviewer's own words, condensed):** "Every mechanism-level
claim I could independently execute... reproduced exactly as the
repository's own records describe... nothing BLOCKING was found in this
pass."

## 23. Phase 1 final remediation and closeout (prompt 005)

Authorising prompt:
[`planning/prompts/005-phase-1-final-remediation-and-closeout.md`](prompts/005-phase-1-final-remediation-and-closeout.md).
New ADR: [`decisions/0007`](../decisions/0007-top-level-schemas-directory.md).
This section amends — does not replace — the plan above. Prompt 005 has
four parts: A (correct two native-Codex-review findings on PR #1), B
(consolidate schemas into `schemas/`), C (verify), D (GitHub/Codex
re-review), E (final closeout). This section covers A–C; §24 (below, once
written) will cover the independent review of this batch; D and E are
addressed directly in the final report, since D requires a human action
this session cannot perform and E's outcome depends on D.

**Baseline recorded before any change (prompt 005 §9, "record... before
implementation"):** branch `phase-1/stage-1.0-bootstrap`, HEAD
`3a8c395` (clean working tree, matching PR #1's actual reviewed
commit — confirmed by fetching the live PR page, not assumed), 49
tests passing before this batch (37 validator + ... — actually recorded
as of the prior batch's close: 37 validator tests, 33 policy-evaluator
tests). Codex's two P2 findings, their file/line anchors, and their
required corrections are preserved verbatim in
`planning/prompts/005-...md` §3–§4; both were independently reproduced
against the actual pre-fix code (not merely read as claims) before any
fix was written — see Part A below.

**Part A — Codex findings, corrected.**

1. **Finding 1 (parsing.py, fenced-code-block handling).** Reproduced:
   `PYTHONPATH=src python3 -c "..."` against the pre-fix
   `extract_headings` returned `{'Required', 'Doc'}` for a document
   containing only a `~~~`-fenced "# Required" example — the exact
   false positive Codex described. Corrected by replacing the
   single-regex fence stripper with a line-oriented parser tracking
   fence character, fence length, and valid/invalid closing fences
   (`parsing._strip_fenced_code_blocks`) — the exact approach Codex's
   own comment suggested. All 9 required regression scenarios
   implemented and passing (`tests/test_fenced_code_blocks.py`, 10
   tests — the 9th scenario plus an extra "shorter closing candidate
   does not close" case). Before/after evidence: the fix was verified
   against the actual pre-fix implementation extracted via
   `git show 3a8c395:src/axiom_validator/parsing.py`, not a
   reconstruction from memory.
2. **Finding 2 (policy_evaluator.py, severity type).** Reproduced:
   `evaluate(..., [{"severity": []}])` raised an unhandled `TypeError:
   unhashable type: 'list'` against the pre-fix code. Corrected by
   validating `isinstance(severity, str)` before the `in
   BLOCKING_SEVERITIES` membership test, returning `FAIL_CLOSED` with
   the documented `EvaluationResult` shape instead of raising. All 7
   required malformed-severity scenarios plus preserved coverage of 8
   existing scenarios implemented
   (`.github/scripts/tests/test_policy_evaluator_severity_types.py`,
   17 tests). The explicit "should unknown severity strings be
   rejected" evaluation required by prompt 005 §4 was answered
   **no** — recorded as a reasoned decision in
   `contracts/codex-gate-policy-evaluator.md` rule 8's amendment, not
   left implicit.

Both corrections amend `contracts/codex-gate-policy-evaluator.md` (rule
6, rule 8's note) in place as historically-dated amendments — not
silently, and not by weakening any existing guarantee (both fixes
strictly narrow what is accepted, matching prompt 005 §4's explicit
"do not weaken the existing accepted contract" instruction).

**Part B — Schema consolidation.** Every one of the 18 production
schema files and 18 fixture schema files (36 total — independently
recounted via `find . -name "*.md.schema.yaml"`, not assumed to match
the prior batch's "15 real + 20 fixture" figure, which predates
subsequent fixtures added since) moved: production schemas to a
mirrored path under a new top-level `schemas/` directory
(`schemas/<relative-document-path>.schema.yaml`); fixture schemas to
their own separate mirror tree (`tests/fixtures/schemas/`), never
nested inside the production tree. `docs/governed-documents.txt` moved
to `schemas/governed-documents.txt`. Implemented via two new pure
functions (`parsing.schema_path_for`, `parsing.doc_path_for_schema`)
and one new optional `validate_file`/`find_orphaned_schemas` parameter
each (`schema_mirror_root` / `mirror_root`, both defaulting to
`repo_root` so every untouched call site is unaffected). Full record:
`evidence/schema-migration.md`'s "Second relocation" section. New
ADR: `decisions/0007`. New contract section: "Contract revision 2" in
`contracts/documentation-schema-validator.md` (the original "Contract
revision" section is left as the historical record of the first,
colocated-companion-file move, with a note at its top pointing to the
superseding section rather than being rewritten).

Two things found and fixed during this work, before independent review
dispatch:

- **A genuine design gap, caught by re-deriving the "exclude tests/ by
  name" workaround's own rationale rather than copying it forward
  unexamined:** the previous orphan-scan exclusion (prompt 004) was a
  patch for a problem that this relocation's own architecture (a
  wholly separate fixture mirror tree, never nested in the production
  one) makes structurally impossible — so the exclusion mechanism was
  removed rather than carried forward as now-redundant complexity.
- **Manifest integrity, explicitly required by prompt 005 §7 to be
  assessed rather than left as an accident:** a missing
  `schemas/governed-documents.txt` file previously (and would have
  continued to) silently disable all governed-document enforcement.
  Fixed with a new `GovernedManifestMissing` exception and fail-closed
  handling in `validate_file`, with its own regression tests
  (`tests/test_schema_relocation.py`'s `TestMissingManifestFailsClosed`,
  3 tests covering missing-file, explicit-override, and
  present-but-empty cases separately so the three are never conflated).

**Part C — Verification.** 50/50 validator tests pass: 27 before this
batch (confirmed via `git show 3a8c395:tests/test_axiom_validator.py`
and its sibling file's method counts) + 23 net-new
(`test_fenced_code_blocks.py`, 10; `test_schema_relocation.py`, 13,
including a symlink-escape regression test added after path-safety was
checked by hand against a real symlink before independent review was
dispatched) — arithmetic checked against the actual `python3 -m
unittest discover -s tests -v` "Ran 50 tests" line, not asserted from
hand-added subtotals, precisely because §22 above already found one
such subtotal wrong once in this project. 33/33 policy-evaluator tests
pass (16 before + 17 new, `test_policy_evaluator_severity_types.py`). Both suites and the exact
CI commands (`schemas/governed-documents.txt`-driven validation, the
orphan scan that runs as a `main()` side effect) were run directly
against the real repository, not assumed from file existence.

## 24. Independent review record — final remediation batch (prompt 005)

Dispatched: a fresh, non-forked `general-purpose` agent with no prior
conversation context — best-effort isolation, level 2 of
`docs/agent-isolation.md`'s taxonomy, named that way in the reviewer's
own report. 35 tool uses, 128,983 tokens, 270.7s.

**No BLOCKING code findings.** The reviewer independently reproduced
both pre-fix Codex defects from `git show 3a8c395:...` (not from reading
the diff), confirmed both fixes against the real post-fix code,
re-ran both full test suites directly (50/50, 33/33 — matching this
plan's own figures exactly, itself informative since §22/§23 above
record two prior instances of this project's own test-count arithmetic
being wrong), constructed 11 of its own fence scenarios and 5 of its
own malformed/edge-case severity values beyond every existing fixture,
diffed 5 real schema files against their pre-relocation git history to
confirm only the one disclosed content change actually occurred, built
its own temp-directory reproductions of the missing-manifest and
path-escape (including an actual Unix symlink, not just a `../`
string) cases, and confirmed `decisions/0002` was untouched and
`decisions/0006` only gained its disclosed Status annotation via
direct `git diff` against `3a8c395`.

**One real finding, in the evidence record rather than the code:**
`evidence/schema-migration.md`'s "Second relocation" section stated
"49 tests... 12 new" — stale by exactly one in both figures, because
that section was written before the symlink-escape regression test
(added after this session's own hand-check of path safety, per §23
above) was added to `tests/test_schema_relocation.py`. **Fixed** —
corrected to 50/13, with a note on what caused the discrepancy rather
than a silent number swap.

**Two ADVISORY findings, both pre-existing gaps the fence fix never
claimed to close, found by the reviewer constructing scenarios beyond
every existing fixture, not reproductions of anything already known:**

1. CommonMark's 4-space-indented code-block convention is not
   recognised as code at all by `extract_headings` — a heading-looking
   line inside one still counts as real. Out of scope for Codex's
   finding (which was about fence character/length recognition, not
   indentation) and genuinely new, not previously documented.
2. A closing fence indented with a tab (rather than spaces) fails to
   close. Fails safe (over-hides content, risking a missed real
   heading reported `FAIL`) — never reintroduces the false-PASS
   direction Codex's original finding was about.

Both **disposition: documented, not fixed** — added to
`contracts/documentation-schema-validator.md`'s Non-goals and
`docs/axiom-validator.md`'s Limitations in this same change, per this
project's own standing practice of recording a genuinely out-of-scope
gap rather than expanding a bounded fix's scope to chase it.

**Also assessed, not merely accepted:** the reviewer gave its own
independent judgement that rule 8's "unrecognised severity stays
advisory, not malformed" decision (contract amendment, §23 Part A
above) is "reasonable, and explicitly, non-evasively justified," not
scope-avoidance — with one soft, non-blocking observation (case
sensitivity of the `P0`/`P1` match is a real operational
consideration the contract discusses for *unrecognised* severities but
not explicitly for *case-variant* ones) recorded here for visibility,
not actioned as a defect.

**Verdict (reviewer's own words, condensed):** "The two Codex P2
findings are genuinely corrected... the schema relocation is
structurally complete and byte-level verified where claimed, path-safety
and fail-closed manifest behaviour hold up against my own adversarial
constructions... This batch is not yet ready to be committed and
independently closed out until that evidence-count discrepancy is
corrected — everything else checked here supports proceeding once it
is." That correction is the fix recorded above; no other blocking gap
remains open from this review.

## 25. Final Codex correction — heading whitespace (prompt 006)

Authorising prompt:
[`planning/prompts/006-final-phase-1-correction-and-closeout.md`](prompts/006-final-phase-1-correction-and-closeout.md).
Baseline recorded before implementation: branch
`phase-1/stage-1.0-bootstrap`, HEAD `2ebac4c` (clean working tree,
matching the prompt's "Last confirmed PR head" exactly). A `web-fetch`
attempt against the live PR page for the second Codex review's exact
text returned a truncated page (~40K of 78K characters) and an
unverified model-extracted summary for the rest — **recorded honestly
as partially unconfirmed**, not treated as ground truth. What the
fetch *did* establish with enough confidence to act on, cross-checked
against the prompt's own detailed description (title "Restrict heading
whitespace to the same line," file `src/axiom_validator/parsing.py`,
P2, anchored to commit `2ebac4c`): a third finding exists and matches
what this session then verified directly against the actual code.
Per this project's standing practice, the live PR fetch is corroborating
context, not the basis for the fix — the fix is based on reproducing
the defect against the real code.

**Reproduced before any change:** `git show 2ebac4c:src/axiom_validator/parsing.py`,
loaded in isolation, confirmed `extract_headings("#\nRequired\n")`
returned `{"Required"}` against the actual pre-fix code — the exact
false positive both the prompt and the (partially unconfirmed) Codex
comment describe: `HEADING_RE`'s `\s+` separator matches a newline,
letting a bare `#` marker with no text of its own "absorb" an unrelated
paragraph on the next line as its heading text.

**Corrected** by changing the marker/text separator from `\s+` to
`[ \t]+` (horizontal whitespace only). **A related, narrower artifact
found while independently verifying this fix's own 9 required
scenarios, not a separate Codex finding:** a bare `#` marker followed
only by trailing whitespace and nothing else (`"#  \n"`) still matched
after the first change, capturing a single space character that
`.strip()` then reduced to an empty string — so `extract_headings`
could return `{""}` for a line with no real heading text at all. Not
exploitable as a false `PASS` (contract rule 12 already requires
`required_sections` entries to be non-empty strings, so no real
document could declare an empty-string requirement), but still a line
with no real heading contributing a spurious result. Fixed in the same
change by requiring the captured text's first character to be
non-whitespace (`\S` instead of `.` at the start of the capture group).

All 9 required regression scenarios plus CRLF line-ending coverage and
the related empty-heading case implemented in a new, dedicated file
(`tests/test_heading_whitespace.py`, 12 tests), following this
project's established convention of giving each corrective fix its own
test file rather than editing an earlier one. One new fixture pair
(`tests/fixtures/invalid/heading_whitespace_next_line.md` +
`tests/fixtures/schemas/invalid/heading_whitespace_next_line.md.schema.yaml`)
exercises required scenario 8 end-to-end through `validate_file`, not
just the parsing function directly.

**Verification:** full suite 62/62 (50 before this batch + 12 new),
policy-evaluator suite unaffected at 33/33, all 11 governed documents
still `PASS`, zero orphaned schemas. The two earlier Codex corrections
(fenced-code-block handling; severity-type validation) were re-run
as part of the same full-suite pass, not assumed still passing from an
earlier record — `tests/test_fenced_code_blocks.py` and
`.github/scripts/tests/test_policy_evaluator_severity_types.py` both
still pass unchanged.

**Thread disposition (prompt 006 §10) — prepared, not posted:** this
session has no `gh`/token/API access to reply on or resolve a GitHub
review thread. Suggested reply text for the repository owner, one per
finding, to post directly on PR #1:

- **Finding A (fenced-code-block handling):** "Fixed in commit
  `162e5c6` — `src/axiom_validator/parsing.py`'s fence stripper now
  tracks fence character/length/closing validity line-by-line instead
  of matching only exactly-3-backtick fences. Regression tests:
  `tests/test_fenced_code_blocks.py` (10 tests, all 9 required
  scenarios + 1 extra). Independently re-verified in
  `planning/phase-01-foundation.md` §24 (no blocking findings) and
  re-run again in this batch (§25) — still passing."
- **Finding B (severity validation):** "Fixed in commit `162e5c6` —
  `.github/scripts/policy_evaluator.py`'s `evaluate()` now validates
  `isinstance(severity, str)` before the set-membership test.
  Regression tests:
  `.github/scripts/tests/test_policy_evaluator_severity_types.py` (17
  tests). Independently re-verified in §24 (no blocking findings) and
  re-run again in this batch — still passing."
- **Finding C (heading whitespace):** "Fixed in commit `0645af3` —
  `HEADING_RE`'s marker/text separator changed from `\s+` to `[ \t]+`,
  plus a related tightening (captured text must start with a
  non-whitespace character) found while verifying this fix's own
  required scenarios. Regression tests: `tests/test_heading_whitespace.py`
  (12 tests, all 9 required scenarios + CRLF coverage + the related
  case). Independent verification: see §26 — no blocking findings,
  including 12 of the reviewer's own adversarial scenarios beyond the
  required set."

These are suggested texts for the human to post and then mark each
thread Resolved on GitHub's own terms — this record does not claim any
thread is actually resolved, since this session cannot observe or
change that state (prompt 006 §10: "Never claim a thread has been
resolved unless its actual GitHub state confirms that").

**Suggested PR #1 description update (prompt 006 §9) — prepared, not
posted**, for the repository owner to paste over the current
description:

> **Phase 1 — Foundation.** Establishes and tests a lightweight,
> evidence-based AI-assisted development methodology: governance,
> knowledge placement, documentation schemas, behavioural contracts,
> independent review, deterministic CI, self-development of a real
> component, a genuine refactor, and independent documentation
> reconstruction. Full plan: `planning/phase-01-foundation.md`. Key
> ADRs: `decisions/0001`–`0007`.
>
> **Native Codex review findings and corrections:**
> 1. Fenced-code-block heading false positive
>    (`src/axiom_validator/parsing.py`) — fixed, commit `162e5c6`,
>    `tests/test_fenced_code_blocks.py` (10 tests).
> 2. Policy-evaluator `TypeError` on malformed severity
>    (`.github/scripts/policy_evaluator.py`) — fixed, commit `162e5c6`,
>    `.github/scripts/tests/test_policy_evaluator_severity_types.py`
>    (17 tests).
> 3. Heading-whitespace false positive (`\s+` matching a newline,
>    `src/axiom_validator/parsing.py`) — fixed, commit `0645af3`,
>    `tests/test_heading_whitespace.py` (12 tests).
>
> **Deterministic verification:** 62/62 validator tests, 33/33
> policy-evaluator tests, all 11 governed documents `PASS`, zero
> orphaned schemas — all re-run after each correction, not assumed.
> GitHub Actions' actual run result on the latest commit is not
> independently confirmed from the authoring session (no API access).
>
> **Independent verification:** every correction in this PR was
> reviewed by a fresh-context agent before being treated as final —
> see `planning/phase-01-foundation.md` §19, §22, §24, §26 for each
> review's findings and disposition. All best-effort (not mechanically
> enforced) isolation, named as such throughout.
>
> **Outstanding:** a third native Codex review of the latest commit
> (request with `@codex review`); the three existing review threads'
> resolution on GitHub; human acceptance. See
> `evidence/phase-1-final-closeout.md` and its addendum for the full
> acceptance matrix. **Do not merge without explicit human approval.**

## 26. Independent review record — heading-whitespace correction (prompt 006)

Dispatched: a fresh, non-forked `general-purpose` agent with no prior
conversation context — best-effort isolation, level 2 of
`docs/agent-isolation.md`'s taxonomy, named that way in the reviewer's
own report. 33 tool uses, 111,140 tokens, 187.5s.

**No BLOCKING findings.** The reviewer independently reproduced the
pre-fix defect from `git show 2ebac4c:...` (not from reading the diff),
confirmed the current regex's exact behaviour by reading it directly,
re-ran both full test suites itself (62/62, 33/33 — matching this
plan's own figures), and constructed 12 of its own adversarial
scenarios beyond every required/existing one — including checking
whether Python's `\s` matches Unicode whitespace like U+00A0 (it does,
but only on the unchanged trailing `\s*$` side, which was never the bug
class this fix addresses, not a new defect), vertical tab, form feed,
7+ `#` characters, and tab-only content after `#` (also correctly
caught by the `\S`-first-character fix, not just the space-only case
this plan's own write-up emphasised). It judged treating this as a bug
fix rather than a contract amendment to be the right call, since rule 4
never specified same-line semantics and the fix makes the
implementation match the contract's plain intent more faithfully, not
a changed one.

**Two MATERIAL-NONBLOCKING findings, both documentation
cross-reference hygiene, not correctness:**

1. This plan's own §25 (and `evidence/phase-1-final-closeout.md`'s
   addendum, and `planning/ROADMAP.md`/`planning/CONTEXT.md`) forward-
   referenced "§26" before it existed — the reviewer correctly read
   this as an anticipated reference to its own review being recorded
   here, not a pre-existing dangling link, but flagged it as something
   that must actually resolve once this section landed. **Fixed —
   this section is that §26.**
2. `README.md`'s status banner still pointed to
   "`planning/phase-01-foundation.md` §16–§24" — stale by one batch,
   since §25 (this correction) was the most relevant section for what
   the banner was summarising. **Fixed** — widened to §16–§26.

**One ADVISORY, not actioned:** `contracts/documentation-schema-validator.md`
rule 4 could state explicitly that a required heading's marker and
text must be on the same line, for future precision — its current
silence on this did not cause the bug and isn't required for the rule
to be satisfiable, so this is recorded as a possible future
refinement, not a defect requiring a contract amendment now.

**Verdict (reviewer's own words, condensed):** "The heading-whitespace
correction itself is genuinely fixed, correctly verified against both
the original defect and a dozen adversarial cases of my own
construction, fully covered by passing regression tests, and does not
regress either earlier Codex correction or the broader governed-document
validation... neither [documentation finding] blocks Phase 1 from being
in a 'ready for human acceptance' state once those two small reference
fixes are made." Both are made in this section and the next edit.

## 27. Final Codex correction — manifest integrity (prompt 007)

Authorising prompt:
[`planning/prompts/007-final-corrective-remediation-and-closeout-preparation.md`](prompts/007-final-corrective-remediation-and-closeout-preparation.md).
Baseline recorded before implementation: branch
`phase-1/stage-1.0-bootstrap`, HEAD `6e75d2b` (clean working tree,
matching the prompt's "Last confirmed PR head" exactly). A `web-fetch`
of the actual GitHub Actions run the prompt cited
(`.../actions/runs/44891748857`) confirmed, verbatim from the page
(not the truncated/summarised part): **Status Success**, 4 jobs shown
with durations matching `deterministic-checks.yml`'s 4 jobs exactly
(`policy-evaluator-tests`, `axiom-validator-tests`,
`validate-governed-documentation`, `no-trailing-whitespace`). This is
the first time this project has had direct, verbatim confirmation of a
real GitHub Actions run result — every earlier closeout record
(`evidence/phase-1-final-closeout.md` and its addendum) correctly
recorded this as *unconfirmed*, not assumed passing; it is now
confirmed, for this one specific commit, and recorded as such rather
than silently backfilled into the earlier records. A second fetch of
the live PR page (again partially truncated) found a Codex comment
reviewing `6e75d2b` whose described finding
("Check manifest integrity even when a companion schema exists...
when a valid companion schema exists but `schemas/governed-documents.txt`
is missing, `validate_file()` returns PASS") matches exactly what this
session then independently reproduced against the real code — cross-checked,
not assumed.

**Reproduced before any change**, per the prompt's exact reproduction
recipe: an isolated temp directory with a valid `foo.md` and a valid,
parsing `schemas/foo.md.schema.yaml`, no `schemas/governed-documents.txt`
at all, and `validate_file(path, repo_root)` called with no override —
returned `{"result": "PASS"}` against the actual pre-fix code. Root
cause confirmed by reading `src/axiom_validator/__init__.py` directly:
the manifest-missing fail-closed check (`decisions/0007` contract
revision 2 rule 4) was only ever reached inside the `if not
schema_path.exists():` branch — a document whose own schema existed
never triggered it at all.

**Corrected** by moving the manifest load/check to run unconditionally
(whenever `governed_manifest` is not explicitly overridden), before
branching on whether the document's own schema file exists. No contract
amendment or new ADR — per prompt 007 §2's explicit instruction, this
is an implementation defect against an already-correctly-specified
rule, not a changed decision; a short implementation note was added to
the contract's existing rule 4 recording the bug and fix, not a new
rule. All 8 required test-table scenarios implemented in a new,
dedicated file (`tests/test_manifest_integrity.py`, 10 tests — the
override scenario split into 3 sub-cases for clarity), following this
project's established one-file-per-correction convention.

**Verification:** full suite 72/72 (62 before this batch + 10 new),
policy-evaluator suite unaffected at 33/33, all 11 governed documents
still `PASS`, zero orphaned schemas, no trailing whitespace. The three
earlier Codex corrections (fenced-code-block handling; severity-type
validation; heading-whitespace) were re-run as part of the same
full-suite pass, not assumed still passing — `tests/test_fenced_code_blocks.py`,
`tests/test_heading_whitespace.py`, and
`.github/scripts/tests/test_policy_evaluator_severity_types.py` all
still pass unchanged.

**Four-finding disposition table (prompt 007 §12):**

| Finding | File | Correction commit | Regression tests | Independent verification | GitHub thread |
|---|---|---|---|---|---|
| A — fenced-code heading false positive | `src/axiom_validator/parsing.py` | `162e5c6` | `tests/test_fenced_code_blocks.py` (10) | §24 (no blocking) | Suggested reply in §25; not confirmed resolved on GitHub |
| B — malformed severity `TypeError` | `.github/scripts/policy_evaluator.py` | `162e5c6` | `.github/scripts/tests/test_policy_evaluator_severity_types.py` (17) | §24 (no blocking) | Suggested reply in §25; not confirmed resolved on GitHub |
| C — heading whitespace crosses newline | `src/axiom_validator/parsing.py` | `0645af3` | `tests/test_heading_whitespace.py` (12) | §26 (no blocking) | Suggested reply in §25; not confirmed resolved on GitHub |
| D — manifest integrity not checked when schema exists | `src/axiom_validator/__init__.py` | `e0094f7` (plus a follow-up fix for a gap the review itself found — see §28) | `tests/test_manifest_integrity.py` (11) | §28 (no blocking findings in the fix; 1 real code gap + 1 real documentation overclaim found and fixed) | Suggested reply below; not confirmed resolved on GitHub |

**Suggested reply text for Finding D's GitHub thread (prompt 007 §12),
prepared, not posted** — this session has no `gh`/token/API access to
post or resolve a thread:

> "Fixed in commit `e0094f7` —
> `src/axiom_validator/__init__.py`'s `validate_file` now loads and
> checks `schemas/governed-documents.txt` unconditionally (unless an
> explicit `governed_manifest` override is given), before branching on
> whether the document's own schema file exists — not only inside the
> 'schema absent' branch, which is what let a document with a valid
> schema wrongly `PASS` even with no manifest file at all. Regression
> tests: `tests/test_manifest_integrity.py` (10 tests, all 8 required
> scenarios from the review comment's own reproduction recipe).
> Independent verification: see `planning/phase-01-foundation.md` §28 —
> no blocking findings in the fix itself; the review also found (and
> this session fixed) a real gap where a `schemas/governed-documents.txt`
> that exists but isn't a readable file raised an unhandled exception
> instead of a structured FAIL."

No contract amendment was needed (the contract already specified this
rule correctly; only the implementation didn't match it) — recorded
here so a reviewer doesn't go looking for one.

## 28. Independent review record — manifest-integrity correction (prompt 007)

Dispatched: a fresh, non-forked `general-purpose` agent with no prior
conversation context — best-effort isolation, level 2 of
`docs/agent-isolation.md`'s taxonomy, named that way in the reviewer's
own report. 51 tool uses, 143,423 tokens, 301.9s. The orchestrating
turn hit a usage limit partway through this dispatch; commits `e0094f7`
and `2357d35` were pushed before the review finished, with
`planning/CONTEXT.md` recording that honestly as pending rather than
guessing at a result (see that commit's own message). The review
completed shortly after and is recorded here, in the next turn, exactly
as it found things — not backdated to read as though it had already
been incorporated into `e0094f7`.

**No BLOCKING finding in the correction itself.** The reviewer
independently reproduced the pre-fix defect by extracting
`src/axiom_validator/__init__.py` from commit `6e75d2b` via `git show`
(confirming via `git diff` that `parsing.py`/`rules.py`/`reporting.py`
were unchanged since that commit, so pairing the old orchestrator with
current modules was valid), confirmed the current code's exact fix
ordering via `git diff 6e75d2b HEAD -- src/axiom_validator/__init__.py`,
re-ran both full suites itself (72 and 33, matching this plan's
figures), and constructed 3 of its own adversarial scenarios beyond
the required 8 — including confirming the `governed_manifest` override
takes full precedence over a *contradictory* on-disk manifest in both
directions (override says ungoverned while disk says governed, and
vice versa), which the required test table didn't explicitly cover.

**One BLOCKING finding — not in the fix, in this project's own
record-keeping, found and fixed in the same commit as this section:**
`README.md` and `planning/ROADMAP.md`, both edited in commit `e0094f7`,
asserted Finding D was already "independently reviewed with no
blocking findings" in the same breath as findings A–C — while
`planning/CONTEXT.md`, edited in the very next commit (`2357d35`),
correctly disclosed that this review had not yet run. The reviewer
caught this live, checkable self-contradiction directly (not a
historical artifact): exactly the "an agent's own claim treated as
verification evidence before verification occurred" failure
`AGENTS.md` §6 exists to prevent. **Fixed**: both files' wording
corrected in this same change, once the review's actual (now genuinely
available) result could be cited honestly.

**One MATERIAL-NONBLOCKING finding, a real and previously-latent
defect:** the reviewer constructed `schemas/governed-documents.txt` as
a directory (not a file) and found `validate_file` raised an unhandled
`IsADirectoryError` straight out of the function, instead of the
structured `FAIL` prompt 007 §5 explicitly requires ("do not introduce
an unhandled exception"). Root cause: `load_governed_manifest` checked
`.exists()` (true for a directory) before unconditionally calling
`.read_text()`, and the only exception type caught upstream was
`GovernedManifestMissing`, not a generic I/O failure. This gap
predated this specific correction (it was already latent on the
narrower "schema absent" path) but this correction's fix widened its
reach to every document validated through the default path, making it
worth closing now rather than carrying forward. **Fixed**:
`load_governed_manifest` now reads the file inside a `try`/`except`,
catching `FileNotFoundError` (the original message) and `OSError`
generally (a new message, same `GovernedManifestMissing` exception,
same fail-closed `FAIL` outcome) instead of checking `.exists()` first.
One new regression test
(`tests/test_manifest_integrity.py::TestManifestPathNotAReadableFile`,
reproducing the exact directory-as-manifest scenario) — 11 tests in
that file now, 73/73 in the full suite.

**One ADVISORY, not actioned:** the reviewer judged this plan's
implementation note phrasing ("prompt 006's follow-up, found by a
third native Codex review") as slightly imprecise shorthand (Finding D
was found by the review of the commit that *followed* prompt 006's
work, not literally part of prompt 006 itself) but not worth a
separate fix.

**Verdict (reviewer's own words, condensed):** "The Finding D fix
itself is correct, independently reproduced, correctly verified by
both required test suites, and contract-compliant — but README.md and
planning/ROADMAP.md currently contain a live, checkable false claim...
which must be corrected (and the directory-as-manifest unhandled-exception
gap should at minimum be recorded, if not fixed) before this
correction can be considered fully reconciled." Both are fixed in this
same change; no other blocking gap remains open from this review.
