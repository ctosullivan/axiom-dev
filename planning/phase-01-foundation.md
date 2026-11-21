# Phase 1 — Foundation

Authorising prompt: [`planning/prompts/001-phase-1-bootstrap.md`](prompts/001-phase-1-bootstrap.md).
Related ADRs: [`decisions/0001`](../decisions/0001-development-governance.md),
[`decisions/0002`](../decisions/0002-knowledge-architecture.md),
[`decisions/0003`](../decisions/0003-independent-verification.md).

This is the implementation-ready Phase 1 plan required by the bootstrap
prompt. **Completing Stage 1.0 does not complete Phase 1.** Phase 1 closes
only when Stage 1.5's dogfooding exercise closes out successfully against
the acceptance requirements in §8 below. Stages 1.1–1.5 are specified here
to the depth needed to establish dependencies, scope, and acceptance
criteria — each still requires its own focused plan, written and reviewed,
immediately before that stage's implementation starts (`AGENTS.md` §2).

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
- **Documentation implications:** `docs/` gets the gate's actual behaviour
  documented as OBSERVED/VERIFIED only after the test cases above have
  actually been run — not as INTENDED language describing a design.
- **Completion criteria:** both required-check test cases demonstrated
  with evidence; independent closeout confirms fail-closed behaviour
  specifically, since this is the gate most likely to silently fail open.

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
