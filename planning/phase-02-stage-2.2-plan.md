# Stage 2.2 implementation-ready plan — minimal Axiom adoption and knowledge retrieval

**Status: Planned. Not authorisation to implement.** Requires
independent review and explicit human approval before BUILD starts,
per `AGENTS.md` §2/§11 — the same pattern Stage 2.1 used
(`planning/archive/phase-02-stage-2.1/README.md`).

**Corrective amendment, this revision.** Five targeted corrections
were made after review found the previous draft underspecified or
inconsistent in real, checkable ways: a missing positive demonstration
that `derived.status: VERIFIED` is actually reachable (§4); an
unspecified repository-discovery mechanism (§2a.2); an
over-broad logging/hook footprint inconsistent with Stage 2.2's actual
scope (§2a.3); unaddressed Python-version and licence boundaries
between Axiom Dev and Ledgerkit (§7); and an illustrative 10–20-claim
wiki target with no concrete claims named (§2b.2). Each correction is
marked inline; nothing here restarts the plan's own already-accepted
architecture (two-PR split, `get`/`find` only, native-register
adapter) — see `AGENTS.md` §3 on why this is a plan correction, not a
new ADR.

**CodeCompass-retirement amendment, this revision (§9).** Since the
above, **PR 2a has merged into `main`**
([PR #6](https://github.com/ctosullivan/axiom-dev/pull/6), merge
commit `1dbb0ab`) — `src/axiom_knowledge/` exists and is reviewable
directly, not merely designed. Separately, the repository owner has
decided CodeCompass (Ledgerkit's prior dependency/code-comprehension
tool) is discontinued and is to be retired from Ledgerkit entirely as
part of PR 2b's own adoption work, rather than installing Axiom
alongside it. §9 is a planning amendment only — it authorises an
isolated scratch feasibility evaluation and produces a precise
removal/adoption specification and Ledgerkit-orchestrator handoff; it
does **not** authorise modifying Ledgerkit, opening Ledgerkit's PR 2b,
or marking Stage 2.2 Completed.

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
skill, nothing more. Apache 2.0 licensing (`decisions/0009`) and
Stage 2.1's closeout (`planning/archive/phase-02-stage-2.1/README.md`)
are unaffected by anything in this plan.

## 2. Scope — split across two repositories, two separate PRs

Axiom Dev and Ledgerkit keep their existing, separate governance
(established practice: "Axiom Dev: reusable methodology, knowledge
API, skill, CI tooling and template. Ledgerkit: actual accounting
implementation, compatibility evidence, integration and dogfooding").
Stage 2.2 BUILD is therefore **two dependent PRs, not one** — this
sequencing is unchanged by this amendment.

### 2a. Axiom Dev PR — the reusable `axiom-knowledge` library/CLI

New, self-contained module (e.g. `src/axiom_knowledge/`), implementing
**only** `get(id)` and `find(query)` from
`planning/phase-02-knowledge-api-design.md` §4 — `related`/`impacted`
are explicitly deferred to Stage 2.3, which is what "introduced
incrementally" in that design already specifies; this plan does not
re-decide that.

#### 2a.1 — Native adapter prioritised; generic adapter deferred (correction E, second half)

Ledgerkit's real `dev-docs/compat-register/` adapter (§3a–§3f) is
**built first and is this PR's actual deliverable**. The generic
default-schema adapter (§3, `knowledge/claims/`) is specified in full
already and its **interface is preserved** (`get`/`find` return the
same shape either way), but its **implementation is deferred** until
an independent consumer with no existing register actually needs it
— Stage 2.2 has exactly one real consumer, with an existing register,
so building the fallback path now would be speculative generality
ahead of a demonstrated need (`AGENTS.md` §2.B; ADR 0008). A future
PR implementing the generic path does so against the interface
already specified, not a new design.

#### 2a.2 — Repository, register and scope-manifest discovery (correction B)

**New in this revision — the previous draft left this unspecified.**
The simplest deterministic mechanism, no configuration framework:

- `axiom-knowledge <op> ... [--repo-root PATH]`. If `--repo-root` is
  given, it is used exactly as given — no further discovery, no
  validation beyond "does `knowledge/README.md` exist under it"
  (fail with a named error if not, rather than silently proceeding
  against the wrong directory).
- **Default (no `--repo-root`)**: starting at the current working
  directory, walk up parent directories looking for `knowledge/README.md`
  — **correction, found by independent review**: an earlier draft of
  this bullet overstated this as something
  `planning/phase-02-adoption-design.md` §2 "already specifies PR 2b
  must create." That section actually names `knowledge/README.md` as
  one of three *illustrative* options for pointing the API at the
  real register location, explicitly left to be "chosen then, against
  the real requirement — not pre-decided here." This plan now makes
  that choice explicitly, as its own decision, rather than claiming a
  firmer prior commitment than that section actually gives — the file
  itself (confirmed present as a convention elsewhere in that same
  design, §6's skill body) is still a real, not invented, artifact;
  only the "already specifies...must create" phrasing was overstated.
  Its mere presence **is** the discovery marker once this plan adopts
  it; this invents no second config format alongside it.
- The register path and the optional `knowledge/scope-manifests/`
  directory are both read **relative to the discovered repo-root**,
  never relative to the CLI's own installation location or the
  caller's CWD directly.
- **Required test cases** (all five — a prior draft's own prose
  committed to a failure behaviour for case 5 below without actually
  requiring a test for it; found by independent review and added):
  1. Invoked from the repository root → `knowledge/README.md` found
     immediately; `--repo-root` unnecessary.
  2. Invoked from a subdirectory (e.g. a test file several levels
     deep) → the walk-up finds the same file at the real root;
     resolves identically to case 1.
  3. Invoked from outside any recognised repository (e.g. `/tmp`, or
     a clone with no Axiom adoption at all) → no `knowledge/README.md`
     found by the filesystem root → a named `RepositoryNotFound`
     error, not a crash, not a silent empty result.
  4. `--repo-root` explicitly given, pointing somewhere **other**
     than CWD or any ancestor of it, and genuinely containing
     `knowledge/README.md` → used as given, overriding discovery
     entirely (confirms the explicit argument always wins).
  5. `--repo-root` explicitly given, pointing at a directory that does
     **not** contain `knowledge/README.md` → the same
     `RepositoryNotFound` error as case 3, not a silent pass against
     the wrong directory — this is the specific case the bullet above
     already commits to in prose; it now has its own required test.

**Register-location directive, resolved at BUILD time (recorded here per
`AGENTS.md` §5, since this is the exact mechanism
`planning/phase-02-adoption-design.md` §2 explicitly deferred — "chosen
then, against the real requirement — not pre-decided here" — and PR 2a's
BUILD is where that happens).** One optional line inside the same
`knowledge/README.md` marker file: `register: <path-relative-to-repo-root>`
(e.g. `register: dev-docs/compat-register`). If the line is absent, the
generic default `knowledge/claims/` path is assumed (its *implementation*
remains deferred per §2a.1 — this only resolves the path). The resolved
register directory not existing on disk is `RegisterNotFound`, distinct
from `RepositoryNotFound` (the marker file was found; the register path it
names, or the default, was not) — this is required test case 6 of the
authorising prompt's part 3C. PR 2b's own `knowledge/README.md` for
Ledgerkit must include `register: dev-docs/compat-register`.

#### 2a.3 — Logging and hook footprint, clarified (correction C)

**Stage 2.2 delivers exactly these event producers, nothing broader**:
the CLI's own `task-start`, `task-accepted`, `knowledge_get`,
`knowledge_find` commands/events, each honouring
`AXIOM_DISABLE_LOGGING=1` (`planning/phase-02-measurement-design.md`
§5) and each tolerating a write failure without blocking the
operation itself (same section).

**Deferred, not built in Stage 2.2** — found necessary to state
explicitly, since the cross-cutting design's full mechanism includes
pieces this stage does not need yet:

- The `SessionStart`/`SessionEnd` Claude Code hook pair
  (`planning/phase-02-measurement-design.md`'s session-ID handoff) is
  **not installed** by either sub-PR. Every CLI-owned event in Stage
  2.2 therefore has `session_id: null` — this is the design's own
  already-specified, legitimate fallback for "invocation outside any
  session," and Stage 2.2 is simply inside that case for its whole
  duration, not a new gap. Installing the hook pair is deferred until
  a later stage's actual need for session-level joins justifies it
  (`AGENTS.md` §2.B).
- A dedicated test-runner wrapper (`test_result` events) is **not
  built**. Stage 2.2's own test suite (2a) and acceptance
  demonstration (§4) are run and reported directly; nothing fabricates
  a `test_result` event for a check that wasn't actually wrapped.
- `knowledge_impact` (the `impacted` event) does not exist in Stage
  2.2 at all, since `impacted()` itself is Stage 2.3's deliverable.

**Construction-overhead measurement, before the CLI exists**: Stage
2.2's own build-time overhead for 2a (time, steps, decisions) is
recorded **manually** — a plain dated note, not a CLI-logged event,
since the CLI that would log it does not exist until 2a is done. Once
2a's CLI exists, the required validation (§6) switches to real,
CLI-recorded events for 2b's own setup and the acceptance
demonstration (§4).

Includes, otherwise unchanged from the previous draft:

- The §3a–§3f native-register adapter (status/relationship mapping,
  scope gate, dependency extraction fields).
- A thin CLI wrapper (`axiom-knowledge get <id>`, `axiom-knowledge
  find "<query>"`), plus `task-start`/`task-accepted`.
- Unit tests against **synthetic fixture YAML files** shaped like
  Ledgerkit's real compat-register schema — this PR needs no live
  Ledgerkit checkout and does not touch `~/projects/ledgerkit`.
- Reviewable, testable and mergeable entirely within Axiom Dev's own
  CI (`ci-required`), independently of Ledgerkit.

### 2b. Ledgerkit PR — adoption and CodeCompass retirement (depends on 2a being merged; this revision)

**Redefined, this revision (§9).** PR 2b is no longer purely additive.
The repository owner has decided CodeCompass is discontinued and is to
be removed entirely from Ledgerkit's active working tree in the same
PR that installs Axiom — one coherent migration, not parallel
operation, not a transitional compatibility layer. §9 below carries
the full revised architectural decision, the scratch-evaluation
evidence supporting feasibility, and the complete removal/adoption
contract; this section's own bullets (unchanged from the prior
revision) remain PR 2b's *adoption* half only.

A **separate, later, Ledgerkit-targeted PR**, not built or opened by
this plan or this round:

- Copy `.claude/skills/axiom-work/SKILL.md` verbatim from
  `planning/phase-02-adoption-design.md` §6 into Ledgerkit's own
  `.claude/skills/axiom-work/` (that skill's steps already disclose
  which commands Stage 2.2 does not deliver, per the prior round's
  own correction).
- Add `knowledge/README.md` pointing the CLI's source configuration at
  Ledgerkit's own `dev-docs/compat-register/` (the deferral decision
  `planning/phase-02-stage-2.1-plan.md` §7 already made — **not** a
  new `knowledge/claims/` directory) — both the discovery marker §2a.2
  specifies, and, on the exact same file, a `register:
  dev-docs/compat-register` directive line (§2a.2's own BUILD-time
  resolution of this path, implemented by PR 2a).

#### 2b.1 — Minimal initial knowledge corpus: ~3–4 real claims, not an illustrative 10–20 (correction E, first half)

**Replaces the previous "10–20 claim" illustrative target.** Four
**real, already-existing** `dev-docs/compat-register/` entries,
confirmed by direct inspection of the actual register (49 entries
total) — no new claims are authored, no authoritative knowledge is
duplicated, every wiki entry links to its real stable ID:

1. **`LK-COMPAT-CHECKASSERTIONS-001`** (`checks.assertions`) —
   EC-022-related: its own `reason` field already states "Balance
   assignments (implied-amount inference from a bare assertion)
   remain deferred — not claimed compatible by this entry," a direct,
   existing textual boundary between what this claim covers and
   EC-022's own bug. The wiki entry's job is to make that boundary
   legible to a fresh agent, not to restate the claim.
2. **`LK-COMPAT-DECIMALMARK-001`** (`parser.directives.decimal_mark`) —
   EC-022-related: decimal-mark handling is exactly the
   comma/period distinction EC-022's own fixture matrix depends on
   (`planning/phase-02-stage-2.1-plan.md` §4, rows 2–3/5–9).
3. **`LK-COMPAT-PARSER-TAG-COMMODITY-001`** (`parser.tags.commodity`,
   native `status: verified`, `verified_by` naming a separately-
   dispatched `compat-differential-tester`, `verified_date` present)
   — **the positive `derived.status: VERIFIED` demonstration claim**,
   see §4.
4. **`LK-COMPAT-QUERY-TAG-001`** (`query.tag`, also native `status:
   verified` with a real `verified_by`/`verified_date`) —
   **deliberately given no scope manifest**, demonstrating the
   contrasting case: a native `verified` claim with no independently
   reviewed scope evidence stays `derived.status: UNCERTAIN`, not
   `VERIFIED` (§4).

Four claims, not a quota — this plan does not require exactly four if
dogfooding finds a fifth genuinely useful during BUILD, but it does
not start from "10–20" as a target to fill.

- Add `.axiom-local/` to Ledgerkit's `.gitignore` (events only — no
  session-ID handoff directory yet, §2a.3).
- Install `axiom-knowledge`: template-copy the script/library from 2a
  into Ledgerkit for now, per `planning/phase-02-adoption-design.md`
  §5's explicit decision to defer packaging until a second real
  consumer exists — not re-decided here.
- **Write exactly one independently reviewed scope manifest** — for
  `LK-COMPAT-PARSER-TAG-COMMODITY-001` only (§4) — not one per claim
  and not for the register at large. Its `reviewed_by` must name a
  genuinely separate dispatch from whoever wrote the manifest's
  `scope` text, per `planning/phase-02-knowledge-api-design.md`
  §3b.1's own checks; this plan does not fabricate that review, it
  requires BUILD to actually perform and record it.

**Neither sub-PR modifies anything about Ledgerkit's actual accounting
implementation** — this stage is adoption scaffolding only; EC-022
remains Stage 2.4's work, unchanged by this plan.

## 3. Interfaces

Exactly `get(id) -> Claim | NotFound` and `find(query) -> list[Claim]`
as specified in `planning/phase-02-knowledge-api-design.md` §4, now
with the `--repo-root`/discovery behaviour of §2a.2 as part of their
actual CLI entry points — including their exact error semantics
(`NotFound`, `Malformed`, `InvalidQuery`, `RepositoryNotFound`) and
the §3a–§3f native/derived separation. This plan does not restate
those signatures; implement against the cited sections directly.

## 4. Independent acceptance criteria (strengthened)

Mirrors `planning/ROADMAP.md`'s own Stage 2.2 exit demonstration,
made concrete, with the positive/negative `VERIFIED` fixtures named
rather than merely required in the abstract (correction A):

1. **Positive demonstration — `derived.status: VERIFIED` is actually
   reachable, not merely designed.** `get(LK-COMPAT-PARSER-TAG-COMMODITY-001)`,
   with its one real, independently reviewed scope manifest (§2b.1)
   in place, returns `derived.status: VERIFIED` and a non-null
   `derived.scope` — both gates (reviewer-identity, scope) genuinely
   satisfied by real data, not a stubbed or synthetic fixture.
2. **Negative contrast, same mechanism.** `get(LK-COMPAT-QUERY-TAG-001)`
   — native `status: verified`, same reviewer-identity gate satisfied,
   but **no** scope manifest written for it — returns
   `derived.status: UNCERTAIN`, `derived.scope: null`. The only
   difference between the two claims' derived outcome is the
   presence of a reviewed scope manifest, demonstrated side by side,
   not asserted separately.
3. `find(<query>)` deterministically returns the same result for the
   same repository state, exact-ID and substring/field-equality
   search only (§4 of the knowledge-API design) — no ranking, no
   embeddings.
4. **Fresh-context acceptance test, strengthened.** A fresh-context
   agent, using **only** the installed skill and Ledgerkit's own
   repository documentation (no author's own explanation, no prior
   session), must:
   - retrieve the four real claims named in §2b.1 (not a synthetic
     example);
   - correctly state each claim's native status *and* derived status,
     distinguishing `self-verified`→`OBSERVED` from genuinely
     `verified`-with-scope→`VERIFIED` from `verified`-without-scope→
     `UNCERTAIN`;
   - explain **one verified scope** (claim 3's) and **one unresolved
     limitation** (e.g. claim 1's explicit EC-022 boundary, or claim
     4's missing scope manifest) in its own words;
   - cite the specific evidence supporting each statement (the
     native record's own fields, the scope manifest's content, or
     the oracle evidence at `evidence/phase-2-stage-2.1-oracle/` where
     relevant).
   **An independent reviewer — not the agent performing the
   retrieval, not whoever wrote the scope manifest — then verifies
   the agent's conclusions against the original compat-register
   records and, where claim 1/2 touch EC-022's own area, the Stage
   2.1 oracle evidence directly**, not against the agent's own
   restatement of them. A conclusion the reviewer cannot independently
   confirm against the actual records is a finding, not a pass.
5. Independent review confirms: no write path exists anywhere in the
   implementation (`AGENTS.md` §6); the native record is never
   altered; `derived.status` never claims `VERIFIED` with a null
   `derived.scope` (re-checked against the real implementation and
   the real claims above, not just the design).
6. Setup overhead (§6) and retrieval usefulness are measured for this
   demonstration specifically — **no claim of causal superiority** is
   made from it (`AGENTS.md` §6; ADR 0008); it demonstrates the
   mechanism works on real data, not that it outperforms an
   alternative.

## 5. Negative tests (required, not exhaustive)

Drawn directly from `planning/phase-02-knowledge-api-design.md` §6 and
§2a.2 above — this plan selects the subset relevant to `get`/`find`
and discovery specifically (`related`/`impacted` cases apply to Stage
2.3, not here):

- `get()` for a nonexistent ID → `NotFound`.
- `get(LK-COMPAT-QUERY-TAG-001)` (real native `verified`, no scope
  manifest) → `derived.status: UNCERTAIN`, `derived.scope: null` —
  now a **real-data** regression test, not only a synthetic one (the
  core test for the scope-gate fix history in
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
- **Repository discovery (§2a.2), all five cases**: repo root,
  subdirectory, outside any recognised repository
  (`RepositoryNotFound`), a valid explicit `--repo-root` override, and
  an explicit `--repo-root` that itself lacks `knowledge/README.md`
  (also `RepositoryNotFound` — added as its own required case per
  independent review, not left as prose-only behaviour with no test).
- **Logging opt-out and failure handling (§2a.3)**: `AXIOM_DISABLE_LOGGING=1`
  actually suppresses every CLI-owned event; a simulated event-log
  write failure (e.g. a read-only `.axiom-local/`) does not block the
  underlying `get`/`find` operation's own result.

## 6. Measurable overhead (clarified, correction C)

Stage 2.2 measures **construction** cost (building the adoption
itself); Stage 2.4 measures **use** cost (retrieval during a real
development task) — these remain deliberately different questions.
Per `planning/phase-02-measurement-design.md` (reused, not
redesigned), with this revision's own sequencing made explicit:

1. **Before the CLI exists**: 2a's own build time and major decisions,
   recorded manually (a plain dated note — no event to log yet).
2. **Once the CLI exists**: real `task-start`/`knowledge_get`/
   `knowledge_find`/`task-accepted` events, validated for — not
   merely assumed to have — correct `--task-id` threading, correct
   `AXIOM_DISABLE_LOGGING` opt-out, and non-blocking failure handling
   (§5's negative tests), joined by `git_revision` and `task_id`
   (`session_id` is `null` throughout Stage 2.2, §2a.3 — not treated
   as a defect).
3. Setup steps required for 2b's adoption (file count, lines changed,
   manual steps, including the one scope manifest's own review
   effort) — the first real data point toward Stage 2.6's "adoption
   effort" question, predeclared now rather than invented after the
   fact.
4. The §4.4 fresh-context acceptance test's own time/step cost,
   recorded alongside the independent reviewer's time to verify its
   conclusions — both halves of "retrieval usefulness," not just the
   retrieving agent's own.

No claim of causal benefit is made from these numbers alone — observed
construction cost, not a controlled comparison (`AGENTS.md` §6;
ADR 0008).

## 7. Dependencies, Python and licensing boundaries (correction D)

**Axiom's CLI is optional development tooling, not a Ledgerkit runtime
dependency.** Ledgerkit's own `pyproject.toml` declares
`requires-python = ">=3.8"` and `dependencies = []` (confirmed by
direct inspection, this revision) — Stage 2.2 does not change either.
`axiom-knowledge` runs under **its own** supported Python environment
(matching Axiom Dev's existing CI target, currently 3.13) and its own
one dependency, `pyyaml` (already in Axiom Dev's `requirements.txt`) —
it is invoked as a separate tool, never imported by or bundled into
the `ledgerkit` package itself, so Ledgerkit's own installed-package
floor and zero-runtime-dependency guarantee are untouched by adopting
it. No new project dependency for Axiom Dev's own PR 2a either.

**Licensing**: Axiom Dev is Apache License 2.0 (`decisions/0009`);
Ledgerkit is `GPL-3.0-or-later` (confirmed by direct inspection of
Ledgerkit's `pyproject.toml`, this revision) — the two are compatible
for inclusion (Apache 2.0 code may be incorporated into a GPLv3-or-
later work; the reverse is not generally true, which is irrelevant
here since nothing moves the other direction). PR 2b copies
Axiom-authored files (the skill, the template-copied CLI/library)
into Ledgerkit **without changing Ledgerkit's own licence**: per
Apache License 2.0 §4, the copied files retain Axiom's own copyright/
licence notice (a short header or an accompanying `NOTICE` excerpt,
decided at BUILD time against the actual file set, not pre-specified
here in unnecessary detail); Ledgerkit's own `LICENSE`
(`GPL-3.0-or-later`) is not edited, and this plan does not relicense
any of Ledgerkit's own accounting code. No MCP, no Axiom Assure, no
persistent service, no embeddings — unchanged from every prior round's
complexity-budget discipline.

## 8. Approval gates

1. This plan itself, independently reviewed and human-approved,
   before either sub-PR's BUILD starts (`AGENTS.md` §2, §11) — not
   granted by this document's own existence.
2. PR 2a (Axiom Dev): independent review, `ci-required` green,
   fresh-head native Codex review dispositioned, then human merge
   approval — the same bounded cycle `AGENTS.md` §14 already governs.
   **Done**: merged into `main`, merge commit `1dbb0ab`.
3. PR 2b (Ledgerkit, now including §9's CodeCompass-retirement
   migration): **cannot open before 2a is merged** (done) **and
   requires its own separate authorisation**, not granted by this
   amendment (§9's handoff document is a specification, not that
   authorisation). Reviewed under Ledgerkit's own repository
   governance, which this plan does not assume mirrors Axiom Dev's
   (`planning/phase-02-adoption-design.md` §3, capability 4: "use
   existing project governance... without duplicating or replacing
   it") — including Ledgerkit's own `CLAUDE.md` "Unauthorised Change
   Rule" for the folder-structure change §9's removal/adoption
   contract entails. Separate human merge approval on that
   repository.
4. Stage 2.2 is marked Completed in `planning/ROADMAP.md` only after
   both sub-PRs are merged and independent acceptance criteria (§4)
   are demonstrated — an agent prepares that status change, a human
   confirms it, per `docs/development-lifecycle.md`'s phase-acceptance
   procedure, same as Stage 2.1's own closeout. **Amended, §9: this now
   additionally requires PR 2b's CodeCompass-retirement migration to
   be independently verified, not merely Axiom's own installation.**

## 9. CodeCompass retirement and PR 2b migration (this revision)

**Architectural decision (owner, not re-opened here).** CodeCompass
development is discontinued; its use in Ledgerkit has not demonstrated
sufficient advantage to justify ongoing maintenance. Axiom replaces it
as Ledgerkit's active development knowledge and evidence framework.
CodeCompass-specific tooling, generated state, skills, hooks,
configuration, agent dependencies and obsolete documentation are
removed entirely from Ledgerkit's active working tree in the same PR
that installs Axiom — no parallel operation, no compatibility layer,
no permanent fallback. The migration must leave Ledgerkit simpler to
operate, not merely exchange one tool for another. Ledgerkit's
existing authoritative knowledge, compatibility register, independent
verification practices and Git history are preserved; impact analysis
(`related`/`impacted`) remains out of scope, deferred to Stage 2.3
unchanged.

**What this amendment authorises.** An isolated scratch feasibility
evaluation of the merged PR 2a implementation against Ledgerkit's real
register (performed, evidence below); production of a precise
CodeCompass removal/Axiom adoption specification; production of a
self-contained handoff for Ledgerkit's own orchestrator. **It does not
authorise** modifying Ledgerkit's real checkout, opening Ledgerkit's PR
2b, or marking Stage 2.2 Completed — those remain separate, later,
human-authorised actions (§8.3/§8.4, amended).

**Scratch-evaluation evidence (summary; full detail and reproducible
commands in the handoff document).** A disposable `git clone` of
Ledgerkit (never the real checkout, confirmed unmodified afterward)
confirmed, against real data: `get(LK-COMPAT-PARSER-TAG-COMMODITY-001)`
and `get(LK-COMPAT-QUERY-TAG-001)` both correctly return
`derived.status: UNCERTAIN` with no scope manifest present; writing
one genuinely scoped manifest for the former flips it to
`derived.status: VERIFIED` with the manifest as the only changed
input; `find()` is deterministic across repeated runs; discovery
resolves correctly from a nested subdirectory; `NotFoundError`/
`RepositoryNotFoundError` are both named, non-crashing; no CodeCompass
binary, configuration or generated state (`vendor.toml`,
`context-graph.db`) is needed anywhere in this path; Ledgerkit's own
935-test suite passes unchanged against the scratch clone; Ledgerkit's
`pyproject.toml` (`requires-python = ">=3.8"`, `dependencies = []`) is
untouched. Friction found and recorded, not glossed over: `--repo-root`
must precede the subcommand; no launcher exists yet for
`python3 -m axiom_knowledge` (addressed by the handoff's own minimal
addition, not deferred); one real claim's `implementation[]` entry
does not parse under the `path:symbol` convention and is correctly
flagged as `unresolved_reference`, not silently dropped or crashed on;
`.axiom-local/` is not yet in Ledgerkit's `.gitignore`.

**CodeCompass retirement inventory and minimal Axiom adoption
contract.** Produced by direct inspection of Ledgerkit's actual
working tree and `git log` — real paths, not illustrative ones,
classified as remove / preserve-or-adapt / historical-only, per the
authorising prompt's own distinction (not a blanket "delete anything
mentioning CodeCompass"). The full inventory, the minimal adoption
specification (skill, pinned library, launcher, register directive,
one genuine scope manifest, four-claim wiki, `.gitignore`,
`CLAUDE.md` reconciliation), the explicit acceptance criteria, and the
executable implementation prompt for Ledgerkit's own orchestrator are
in
[`planning/phase-02-ledgerkit-codecompass-migration-handoff.md`](phase-02-ledgerkit-codecompass-migration-handoff.md) —
self-contained there rather than duplicated here, to keep this plan
readable. That document also names three open questions this
amendment does not resolve (the pending `ROADMAP.md`
CodeCompass-upgrade-initiative confirmation; whether to retain the
general-purpose clean-room methodology apparatus independent of this
migration; whether to remove or retain CodeCompass-specific historical
planning/retro records in Ledgerkit's active tree) — each belongs to
Ledgerkit's own repository owner, not pre-decided here.

**Division of responsibility, explicit.** Axiom Dev orchestrator:
performs the scratch evaluation, amends this plan, produces the
removal inventory and the Ledgerkit handoff, independently reviews
these planning changes, opens this Axiom Dev planning PR — and does
not modify Ledgerkit's real checkout or open its implementation PR.
Ledgerkit orchestrator (separately authorised later): performs the
actual CodeCompass removal and Axiom installation as one coherent
migration, retains independently valuable Ledgerkit knowledge and
verification practice without retaining CodeCompass infrastructure,
runs deterministic and fresh-agent acceptance tests, reconciles
Ledgerkit's own documentation/agent-instructions/roadmap, obtains
independent review and bounded corrections, opens Ledgerkit's own
implementation PR, and does not merge it without Ledgerkit's own
repository owner's explicit approval.

Next: Stage 2.3 (deterministic integrity and drift, including the
native-register identity/reference integrity gap
`planning/archive/phase-02-stage-2.1/README.md` already flagged as
unresolved) remains out of scope for this plan. PR 2b (Ledgerkit,
including this amendment's CodeCompass-retirement migration) remains
unauthorised and unstarted.
