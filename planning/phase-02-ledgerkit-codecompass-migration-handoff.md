# Ledgerkit migration handoff — CodeCompass retirement, Axiom adoption

**Status: Planning amendment artifact. Authorises nothing in Ledgerkit.**
Produced by the Axiom Dev orchestrator under the Stage 2.2 PR 2b
planning-amendment prompt (this revision of
`planning/phase-02-stage-2.2-plan.md` §9). This document is the
self-contained, executable brief for **Ledgerkit's own orchestrator**
to pick up under **separate authorisation from Ledgerkit's own
repository owner**. Nothing in this document modifies Ledgerkit;
Axiom Dev's own scratch evaluation (§0) used a disposable clone, never
Ledgerkit's real checkout, which was confirmed unmodified (`git status`
clean, `git diff --stat` empty) after that evaluation.

Architectural decision, made by the repository owner, not re-opened
here: CodeCompass development has been discontinued; its use in
Ledgerkit has not demonstrated sufficient advantage to justify ongoing
maintenance. Axiom replaces it as Ledgerkit's active development
knowledge and evidence framework. No parallel operation, compatibility
layer or permanent CodeCompass fallback. This migration must reduce
operational complexity, not merely swap one tool for another.

---

## 0. Scratch-evaluation evidence (Axiom Dev, this round)

Performed in a disposable `git clone` of
`~/projects/ledgerkit` (not a worktree of the real checkout, to avoid
any shared index/HEAD state), discarded after this evaluation. The
real checkout was confirmed clean before and after
(`git status` → "nothing to commit, working tree clean";
`git diff --stat` → empty).

**Setup performed** (reproducible):
```
git clone ~/projects/ledgerkit /path/to/scratch
cd /path/to/scratch
cp -r <axiom-dev-checkout>/src/axiom_knowledge .     # template-copy, per §2b below
cat > knowledge/README.md <<'EOF'
# Knowledge
Axiom knowledge-API discovery marker for this repository.
register: dev-docs/compat-register
EOF
```
No collision: Ledgerkit's existing `knowledge/` directory already holds
`DECISIONS.md`, `EDGE_CASES.md`, `ANTIPATTERNS.md`, `DOMAIN_RULES.md` —
genuinely Ledgerkit's own, pre-existing, unrelated to CodeCompass or
Axiom. Adding `README.md` beside them, and later a `scope-manifests/`
subdirectory, introduced no naming conflict.

**Results, against real data:**

| Check | Command | Result |
|---|---|---|
| `get`, no scope manifest | `axiom_knowledge --repo-root . get LK-COMPAT-PARSER-TAG-COMMODITY-001` | `derived.status: UNCERTAIN`, `derived.scope: null` — native `status: verified`, real `verified_by`/`verified_date` present, correctly held at UNCERTAIN for missing scope evidence |
| `get`, no scope manifest | `axiom_knowledge --repo-root . get LK-COMPAT-QUERY-TAG-001` | Same outcome, same reason — the negative-contrast claim |
| **Scoped `VERIFIED` demonstration** | wrote one scope manifest for `LK-COMPAT-PARSER-TAG-COMMODITY-001` (`reviewed_by` naming a dispatch separate from the claim's own `verified_by`, Git-committed in the scratch clone only), re-ran `get` | `derived.status: VERIFIED`, non-null `derived.scope` — the only input that changed between the UNCERTAIN and VERIFIED runs for this claim was the scope manifest's presence |
| `find`, determinism | `find "area:query.tag"` run twice | Identical `["LK-COMPAT-QUERY-TAG-001"]` both times |
| `find`, exact ID | `find "LK-COMPAT-QUERY-TAG-001"` | `["LK-COMPAT-QUERY-TAG-001"]` |
| Discovery walk-up | `get` invoked from `ledgerkit/` (one level down) | Resolved identically, no `--repo-root` needed |
| `NotFound` | `get LK-COMPAT-NONEXISTENT-999` | Named `NotFoundError`, exit 1, no crash |
| `RepositoryNotFound` | invoked from `/tmp` with no `--repo-root` | Named `RepositoryNotFoundError`, exit 1, no crash |
| No CodeCompass needed | confirmed `vendor.toml`/`context-graph.db` absent from the clone (gitignored, never cloned) | `get`/`find` worked with neither present — Axiom's knowledge path has zero dependency on CodeCompass's generated state |
| `task-start`/`task-accepted` events | ran both | `.axiom-local/events.jsonl` recorded `task_start`, `task_accepted`, plus the `knowledge_get`/`knowledge_find` events from the checks above, in order |
| Ledgerkit's own test suite | `~/projects/ledgerkit/.venv/bin/python3 -m pytest -q` (run against the scratch clone, using the real repo's own venv) | **935 passed**, 1 pre-existing warning — unaffected by anything added for Axiom |
| Python/dependency boundary | `python3 --version` → 3.13.5 (system and Ledgerkit's own venv agree); `pyyaml` already present system-wide | Ledgerkit's `pyproject.toml` (`requires-python = ">=3.8"`, `dependencies = []`) untouched; axiom_knowledge never imported by the `ledgerkit` package. **Caveat, added this round** (native Codex review, PR #8 round 1): this scratch host happened to already have PyYAML available system-wide — that is not itself a demonstration of §C.2's clean-clone criterion, which requires a *genuinely* clean clone with no such pre-existing dependency; §B.3's dedicated venv addresses this for the real migration, not demonstrated again here |

**Friction and limitations found** (real, not hypothetical):

1. **`--repo-root` is a global option and must precede the subcommand**
   (`axiom-knowledge --repo-root . get ID`, not
   `axiom-knowledge get ID --repo-root .`). A first attempt in the
   wrong order fails with a generic argparse "unrecognized arguments"
   error, not a pointed message. Not blocking — document the correct
   form in the installed skill (§B below already does) — but worth a
   small CLI usability note for a future round, not this migration.
2. **No launcher exists yet.** PR 2a ships a library/CLI invoked as
   `python3 -m axiom_knowledge`, requiring the caller to set
   `PYTHONPATH` to wherever it was template-copied. §B below specifies
   a minimal launcher script as part of this migration's own required
   scope, not deferred — a fresh agent should not have to know or
   guess the right `PYTHONPATH`.
3. **One of the two real claims' `implementation[]` entries doesn't
   parse under the `path:symbol` convention.**
   `LK-COMPAT-PARSER-TAG-COMMODITY-001`'s first `implementation[]` entry
   (`"ledgerkit/parser.py (commodity directive handling;
   commodity_comment_target)"`) is parenthetical-descriptive, not
   `path:symbol`. Axiom's `unresolved_reference` diagnostic correctly
   flags it (not a crash, not silently dropped) — confirms this
   diagnostic fires routinely on Ledgerkit's real register, not only
   on contrived test fixtures. No action required for this migration;
   worth knowing before treating `diagnostics.unresolved_references`
   as rare.
4. **`.axiom-local/` is not yet in Ledgerkit's real `.gitignore`.**
   Confirmed by direct inspection (`grep -n axiom .gitignore` found
   nothing). Required addition, §B/§E below.
5. **Fresh-agent-session claim, precisely scoped.** This evaluation
   confirms `axiom_knowledge` needs no CodeCompass installation,
   configuration or generated state to retrieve and correctly classify
   real claims — it did not (and could not, within this bounded
   exercise) spawn a literal second Claude Code session; that stronger
   form of the fresh-agent acceptance test is §C.3/§D.5 below, owned by
   the Ledgerkit orchestrator's own implementation PR, not claimed as
   already demonstrated here.

**Retrieval vs. usefulness, stated explicitly**: the above demonstrates
that `get`/`find` correctly retrieve and classify real Ledgerkit
claims. It does not, and does not claim to, show that this retrieval
is more *useful* than CodeCompass was, or than no tool at all — no
controlled comparison was run, and §C.3 below requires the same
discipline from the Ledgerkit orchestrator's own acceptance test.

---

## A. CodeCompass retirement inventory

Produced by direct inspection of `~/projects/ledgerkit`'s actual
working tree and `git log` (read-only; nothing below was changed by
Axiom Dev). Every path is real, not illustrative. Three categories,
per the authorising prompt's own classification:

### A.1 — Remove (active CodeCompass tooling, generated state, config, obsolete skills, pin guards, integration scripts, agent instructions, superseded validation apparatus)

| Path | What it is |
|---|---|
| `vendor.toml`, `vendor/` | CodeCompass-generated dependency digests. Already gitignored; delete the files (zero git-history impact — never tracked) |
| `context-graph.db` | CodeCompass-generated SQLite context graph. Already gitignored; delete |
| `.claude/skills/codecompass/SKILL.md` | The CodeCompass skill itself |
| `.claude/commands/discovery.md` | `/discovery`, the CodeCompass-only read-only exploration slash command (`SKILL.md` §"Commands": "covering the same ground as `query`") |
| `.claude/agents/context-curator.md` | Entirely CodeCompass-dedicated role (its own front-matter: "Ledgerkit's CodeCompass-facing role... Never edits CodeCompass itself"); its sole output path, `validation/codecompass/findings/`, is removed alongside it |
| `validation/codecompass/` (whole directory: `README.md`, `context-packets/`, `findings/CC-LK-001.{md,yaml}`, `findings/CC-LK-001-baseline-evidence.md`, `findings/CC-LK-002.{md,yaml}`, `findings/CC-LK-003.{md,yaml}`, `findings/TEMPLATE.{md,yaml}`) | `context-curator`'s own findings store; moot once CodeCompass and that role are gone |
| `dev-docs/clean-room/check_codecompass_pin.sh` | Mechanically checks CodeCompass's pinned revision SHA — zero function without CodeCompass |
| `dev-docs/clean-room/PINNED-REVISIONS.md` | Records CodeCompass's/`codecompass-template`'s pinned SHAs specifically — remove once there is no CodeCompass pin to record (distinct from the *new* Axiom-pin record, §B.2, which replaces it in spirit, not in file) |
| `CLAUDE.md` lines ~390–417 (the `## CodeCompass` section, including the `<!-- codecompass:start -->...<!-- codecompass:end -->` generated marker block) | The project's own CodeCompass integration doc. Replace with an equivalent short `## Axiom` section (§B.4) |
| `CLAUDE.md`'s folder-structure diagram (§"Folder Structure", lines ~288–386) — the `vendor.toml`, `context-graph.db`, `validation/codecompass/`, `.claude/skills/codecompass/` entries specifically | Update the diagram to match the post-migration tree (remove the above four lines; add `knowledge/README.md`/`knowledge/scope-manifests/` and wherever the Axiom launcher/library land, §B.2) |
| `ROADMAP.md`'s "Tooling & Process Initiatives" → CodeCompass-upgrade row's own **non-blocking follow-up** text about re-pinning CodeCompass past its Phase-1 pin | This specific follow-up item is moot once CodeCompass is retired — remove just that clause, not the row itself (§A.3) |

### A.2 — Preserve or adapt (independently useful methods, deterministic scripts, authoritative knowledge, general-purpose practice — not CodeCompass-dependent)

| Path | Disposition |
|---|---|
| `knowledge/DECISIONS.md`, `knowledge/EDGE_CASES.md`, `knowledge/ANTIPATTERNS.md`, `knowledge/DOMAIN_RULES.md` | Ledgerkit's own pre-existing, authoritative project knowledge — entirely independent of CodeCompass. **Untouched** by removal; **one new entry added** to `knowledge/DECISIONS.md` recording the CodeCompass-retirement decision itself and its rationale, per Ledgerkit's own `CLAUDE.md` rule ("Add an entry... whenever a non-obvious decision is made... in the same response as the change") |
| `dev-docs/compat-register/` (53 entries) | Ledgerkit's authoritative compatibility evidence. **Untouched** — this is exactly what Axiom's native adapter reads, never writes |
| `dev-docs/clean-room/check_snapshot.py`, `dev-docs/clean-room/conceptual-documentation-guide.md`, `dev-docs/clean-room/mechanical-isolation.md`, `dev-docs/clean-room/isolation-preflight.md`, `dev-docs/clean-room/worked-example.md`, `dev-docs/clean-room/WORKFLOW-README.md`, and the `snapshots/`, `assertions/`, `implementation-reconstruction/`, `implementation-comparison/`, `legacy-reconciliation/`, `drafts/`, `coding-context-selection/`, `documentation-verification/`, `propagation/` subdirectories | The **clean-room methodology itself** is general-purpose (model-blind reconstruction, independent comparison, legacy reconciliation) and was, by design, never dependent on CodeCompass output — it explicitly cross-validated *against* independent reconstruction, not *using* CodeCompass. **This migration does not require removing it.** Whether Ledgerkit keeps it as a standing documentation-QA capability, or archives it alongside Plan 29's own closeout, is a separate call for Ledgerkit's own orchestrator/owner — flagged, not decided, here (§E) |
| `.claude/agents/domain-skeptic.md`, `.claude/agents/implementation-reconstructor.md` | General-purpose roles (adversarial assertion review; model-blind reconstruction), added for Plan 29 and *reconciled from* CodeCompass's own agent-brief conventions as a starting template — not dependent on CodeCompass's continued existence. **Preserve**; only their front-matter citations to now-possibly-removed Plan 29 planning docs need reconciling (§A.3) if those docs move |
| `.claude/agents/docs-maintainer.md`, `.claude/agents/docs-reconstructor.md` | General documentation-maintenance roles. **Preserve**; remove the specific guidance about not hand-editing the CodeCompass-generated `CLAUDE.md` marker block (moot — there will be no such block) and reconcile the "Legacy reconciliation mode" section's framing as historical (Plan 29 Phase 5 is complete) rather than a live procedure |
| `.claude/agents/release-phase-auditor.md`, `.claude/agents/roadmap-context-curator.md`, `.claude/agents/compat-differential-tester.md`, `.claude/agents/hledger-researcher.md` | Not CodeCompass-dependent (the first has one historical citation to Plan 29's Phase 6; the latter three never reference CodeCompass at all). **No change required** |
| Ledgerkit's own test suite (935 tests, `unittest`-only), `dev-docs/compat-register/schema.md`'s evidence model, `compat-differential-tester`'s differential-testing practice against the pinned real `hledger` binary | Independent verification practice, entirely untouched by this migration — confirmed still passing in full against the scratch clone (§0) |

### A.3 — Historical only (provenance recoverable via Git history; remove from the active tree where it creates clutter or operational ambiguity, keep where it stands as permanent decision record)

| Path | Disposition |
|---|---|
| `dev-docs/planning/core-redefinition/04-codecompass-integration.md`, `18-stage-c-phase-2-codecompass-adoption-plan.md`, `22-stage-c-phase-5a-codecompass-workflow-adoption-plan.md`, `29-codecompass-upgrade-and-clean-room-docs.md` | The actual design/approval records for CodeCompass's adoption and later upgrade. Purely about a tool that no longer exists in the project — **recommend removing from the active tree**, recoverable via Git history exactly as this category permits. **Do not remove unilaterally**: other preserved files (several `.claude/agents/*.md`, `docs-maintainer.md`'s "Legacy reconciliation mode") cite these by path; removing them creates dangling citations that must be reconciled in the same change (§D step 4), not left broken |
| `dev-docs/retros/CODECOMPASS-UPGRADE-PHASE-1.md` through `-5.md`, `dev-docs/retros/_audit-codecompass-upgrade-cleanroom-docs.md`, `dev-docs/retros/CODECOMPASS-UPGRADE-CLEANROOM-DOCS-PLAN.md`, `dev-docs/retros/CODECOMPASS-UPGRADE-CLEANROOM-DOCS-CLOSEOUT.md`, `dev-docs/retros/STAGE-C-PHASE-2.md`, `STAGE-C-PHASE-2-PLAN.md`, `STAGE-C-PHASE-2-PLAN-AMENDMENT.md`, `STAGE-C-PHASE-5A.md`, `STAGE-C-PHASE-5A-PLAN.md` | Same disposition and same caveat as above — historical retros specifically about CodeCompass's adoption/upgrade, not about Ledgerkit's accounting implementation. Recommend removing from the active tree; recoverable via Git history |
| `ROADMAP.md`'s "CodeCompass upgrade + clean-room documentation reconstruction" row (`## Tooling & Process Initiatives`) | **Not a removal candidate — a pending decision.** Currently "Phases 1-6 complete... Awaiting explicit user confirmation before this row flips to `[DONE]`" (per Ledgerkit's own standing "never infer completion" rule). This migration does not resolve that confirmation; it only removes the now-moot re-pin follow-up clause (§A.1). Flagged for the Ledgerkit owner's own explicit decision in §E |
| `ROADMAP.md`'s "Plan 29 bug-fix backlog" and "Compat-register corrections (Plan 29 follow-up)" rows | **Not CodeCompass artifacts — real, open backlog items** (7 production defects found incidentally during clean-room reconstruction; 2 compat-register citation defects). Fully valid regardless of CodeCompass's fate. **No change** |

**Explicit non-goal, stated for the avoidance of doubt**: this inventory
was built by reading each matching file's actual content and role, not
by a blanket `grep -l codecompass`. Several files that mention
"CodeCompass" in passing (A.2's agent roles, the historical retros in
A.3) are not being deleted wholesale; only the files whose entire
purpose was CodeCompass itself move to A.1, and only the planning/retro
records whose entire subject was CodeCompass's adoption move to A.3.

---

## B. Minimal Axiom adoption — exact scope, nothing broader

Per `planning/phase-02-adoption-design.md`, `planning/phase-02-knowledge-api-design.md`
and `planning/phase-02-stage-2.2-plan.md` §2b (unchanged by this
amendment except as noted). This is PR 2b's entire scope:

**B.1 — The skill.** Copy `.claude/skills/axiom-work/SKILL.md` verbatim
from `planning/phase-02-adoption-design.md` §6 into Ledgerkit's
`.claude/skills/axiom-work/`.

**B.2 — The library/CLI, pinned.** Template-copy `src/axiom_knowledge/`
from Axiom Dev's `main` at the exact merged commit
`1dbb0ab` (PR #6's merge commit — the current head at the time of this
handoff; re-confirm it is still `main`'s head before copying, since
`main` may have advanced) into a new, dedicated location **not inside
`ledgerkit/`** — recommended: `dev-docs/tools/axiom_knowledge/`,
consistent with `dev-docs/` already being Ledgerkit's existing home for
AI-workflow tooling and scripts (`dev-docs/clean-room/check_snapshot.py`
is the direct precedent). The Ledgerkit orchestrator may choose a
different path against that repository's own conventions at BUILD
time — if so, record the final choice in `knowledge/DECISIONS.md`, the
same discipline Axiom Dev itself used for its own BUILD-time register-
directive choice (`planning/phase-02-stage-2.2-plan.md` §2a.2). Record
the exact pinned Axiom Dev commit SHA in a short note alongside the
copied library (e.g. `dev-docs/tools/axiom_knowledge/PINNED-REVISION.md`,
one line: commit SHA + date) — the same spirit as CodeCompass's own now-
removed `PINNED-REVISIONS.md`, reused as a pattern, not as a file.
**Attribution, corrected this round** (native Codex review, PR #8
round 1 — genuine finding): Axiom Dev's `src/axiom_knowledge/` source
files carry no per-file copyright headers of their own; their
attribution is the repository-root `NOTICE` and `LICENSE` files
(confirmed by direct inspection — `NOTICE` names the copyright holder
and year and points to `LICENSE` for the Apache License 2.0 full
text). "Keep the existing files' contents unmodified" does not, on its
own, preserve that attribution, since there is no per-file notice to
keep. **Copy Axiom Dev's root `NOTICE` and `LICENSE` alongside the
library** (e.g. `dev-docs/tools/axiom_knowledge/NOTICE`,
`dev-docs/tools/axiom_knowledge/LICENSE`, copied verbatim from Axiom
Dev's repository root at the pinned commit) — this is what Apache
License 2.0 §4 actually requires when redistributing the source, not
an edit to the copied `.py` files themselves. Do not relicense
anything, and do not edit Ledgerkit's own `LICENSE`
(`GPL-3.0-or-later`, confirmed compatible for one-directional inclusion
by `planning/phase-02-stage-2.2-plan.md` §7; unaffected either way).

**B.3 — A minimal launcher** (new in this amendment — §0 found none
exists). **Dependency/environment setup, corrected this round** (native
Codex review, PR #8 round 1 — genuine finding): Axiom Dev's own
supported environment is Python 3.13 with `pyyaml>=6.0,<7.0` pinned in
its `requirements.txt` (confirmed by direct inspection); `axiom_knowledge`
imports `yaml` and fails immediately without it. §0's own scratch
evaluation happened to work because this machine had PyYAML available
system-wide — that is **not** a demonstration of §C.2's clean-clone
criterion, and a literal reading of this section without a dependency
step would leave a genuinely clean clone failing on import. The
launcher must therefore ensure a **separate, dedicated Python
environment** for Axiom's own tooling — e.g. a small venv at
`dev-docs/tools/axiom_knowledge/.venv/` (bootstrapped once via
`python3.13 -m venv .venv && .venv/bin/pip install 'pyyaml>=6.0,<7.0'`,
**gitignored**, never committed) — and the launcher script (e.g.
`dev-docs/tools/axiom-knowledge`, a short shell script) execs that
environment's own interpreter, not an unqualified `python3` that may
or may not have PyYAML: `exec
"$(dirname "$0")/.venv/bin/python3" -m axiom_knowledge "$@"` with
`PYTHONPATH` set to the copied library's own parent directory. This
environment is Axiom's own development tooling, entirely separate from
Ledgerkit's own runtime/install environment — it changes none of
Ledgerkit's own dependencies (§7). A fresh agent or contributor then
invokes `dev-docs/tools/axiom-knowledge get <id>` directly, with the
venv bootstrap documented as a one-time setup step in the installed
skill (§B.1) and/or a short README note beside the launcher. This
launcher is **not** added to Ledgerkit's `pyproject.toml`
`[project.scripts]` (that table is `ledgerkit`'s own installed console
entry point; adding `axiom-knowledge` there would make Axiom's dev
tooling part of the installed package, which
`planning/phase-02-stage-2.2-plan.md` §7 explicitly rules out).

**B.4 — `knowledge/README.md`.** Add the discovery marker (confirmed
collision-free with Ledgerkit's existing `knowledge/` files, §0) with
the `register: dev-docs/compat-register` directive line, per
`planning/phase-02-stage-2.2-plan.md` §2a.2/§2b.

**B.5 — Exactly one independently reviewed scope manifest.** For
`LK-COMPAT-PARSER-TAG-COMMODITY-001` only, at
`knowledge/scope-manifests/LK-COMPAT-PARSER-TAG-COMMODITY-001.yaml` —
**a genuine review, not the disposable placeholder Axiom Dev wrote for
its own scratch evaluation (§0), which must not be copied into the
real Ledgerkit checkout as-is.** Its `reviewed_by` must name a
dispatch genuinely separate from whoever authored the manifest's
`scope` text, per `planning/phase-02-knowledge-api-design.md` §3b.1.
`LK-COMPAT-QUERY-TAG-001` deliberately gets **no** manifest — the
negative-contrast demonstration (§C.4).

**B.6 — The minimal wiki.** Four real claim IDs, per
`planning/phase-02-stage-2.2-plan.md` §2b.1: `LK-COMPAT-CHECKASSERTIONS-001`,
`LK-COMPAT-DECIMALMARK-001`, `LK-COMPAT-PARSER-TAG-COMMODITY-001`,
`LK-COMPAT-QUERY-TAG-001`. No new claims authored; every entry links to
its real register ID.

**B.7 — `.gitignore`.** Add `.axiom-local/` (confirmed missing, §0).

**B.8 — `CLAUDE.md`.** Replace the removed `## CodeCompass` section
(§A.1) with a short `## Axiom` section of equivalent weight: what it
is, the skill name, the `get`/`find` commands, the pinned revision
note's location (§B.2), and the same "Ledgerkit's own tests,
compat-register and `knowledge/DECISIONS.md` remain authoritative
regardless of what Axiom surfaces" framing the CodeCompass section
used — the same epistemic caution, carried over, not dropped. Update
the folder-structure diagram per §A.1's own table.

**Explicitly not introduced**: new accounting-runtime dependencies,
duplicate knowledge stores, MCP, orchestration infrastructure, a
config framework, `related`/`impacted` (Stage 2.3's own deferred
scope, unchanged by this amendment).

---

## C. Explicit acceptance criteria

The Ledgerkit migration PR must demonstrate, with real evidence, not
asserted claims:

1. **No active CodeCompass dependency remains** in any Ledgerkit
   development command, agent brief, hook, workflow or CI process —
   verified by `grep -ri codecompass` across the post-migration tree
   returning only A.3's historical-record hits (if retained) or
   nothing (if removed), never a live command/config/hook reference.
2. **A clean clone operates with Axiom installed and without
   CodeCompass installed** — a fresh `git clone` of the migrated
   Ledgerkit, on a machine with **no pre-existing PyYAML or other
   Axiom-tooling dependency already present** (the genuinely clean
   case; §0's own scratch evaluation did not establish this — its host
   happened to already have PyYAML system-wide), with no `codecompass`
   binary on `PATH` and no prior `vendor.toml`/`context-graph.db`,
   successfully bootstraps §B.3's dedicated venv and runs `get`/`find`
   against the real register via the new launcher.
3. **A fresh agent** (a genuinely new Claude Code session, not the
   implementing session re-describing its own work) **successfully
   retrieves actual Ledgerkit claims and correctly explains native
   status, derived status, supporting evidence and unresolved
   limitations** for the four claims in §B.6 — mirroring
   `planning/phase-02-stage-2.2-plan.md` §4.4's own fresh-context
   acceptance test, verified by an independent reviewer against the
   original compat-register records (and, where relevant, the Stage
   2.1 oracle evidence), not against the fresh agent's own
   restatement.
4. **Scoped `VERIFIED` and unscoped `UNCERTAIN` are independently
   demonstrated** on the real register — `get(LK-COMPAT-PARSER-TAG-COMMODITY-001)`
   with its one genuine scope manifest (§B.5) → `VERIFIED`, non-null
   scope; `get(LK-COMPAT-QUERY-TAG-001)`, same reviewer-identity gate
   satisfied, no manifest → `UNCERTAIN`, null scope — the only
   difference being the manifest, demonstrated side by side (§0
   already did this once, disposably; the real migration PR must
   redo it with its own genuine manifest, not reuse §0's placeholder).
5. **Ledgerkit's existing accounting tests pass** (currently 935,
   `unittest`-only) **and its Python 3.8+ runtime / zero-mandatory-
   dependency contract is unchanged** — `pyproject.toml`'s
   `requires-python`/`dependencies` diff against pre-migration must be
   empty.
6. **Authoritative records preserved, no unreviewed modifications** —
   `dev-docs/compat-register/`, `knowledge/DECISIONS.md` (etc.), and
   Git history itself are never rewritten; the one new
   `knowledge/DECISIONS.md` entry (§A.2) is an addition, not an edit
   to existing entries.
7. **A reviewable evidence record, human merge approval required** —
   the migration PR documents exactly what moved per §A's inventory,
   the acceptance evidence above, and is not merged without the
   Ledgerkit repository owner's explicit approval (§D step 7).

**Retrieval vs. usefulness, restated for this section specifically**:
criteria 2–4 show the mechanism retrieves and classifies correctly.
None of them, singly or together, is a claim that this retrieval is
more useful than CodeCompass was — no controlled comparison exists or
is required by this migration.

---

## D. Executable implementation prompt for the Ledgerkit orchestrator

Copy the block below as the actual authorising prompt once Ledgerkit's
own repository owner separately authorises this work. It is written to
be self-contained — it does not assume the Ledgerkit orchestrator has
read this whole handoff first, though it should.

> You are the Ledgerkit orchestrator. Execute the CodeCompass-to-Axiom
> migration specified in Axiom Dev's handoff,
> `planning/phase-02-ledgerkit-codecompass-migration-handoff.md`
> (commit-pin it when you read it, since Axiom Dev's own `main` may
> have advanced since). This prompt authorises implementing that
> migration in Ledgerkit, under Ledgerkit's own governance
> (`CLAUDE.md`).
>
> 1. **Baseline and isolate.** Inspect Ledgerkit's actual current
>    branch, diff and CodeCompass footprint directly — do not trust
>    the handoff's inventory (§A) as current without re-verifying it
>    against the real tree, since time may have passed. Do the removal
>    and installation work on a dedicated feature branch, never
>    directly on `main`, and never by force-pushing or discarding any
>    uncommitted work you find.
> 2. **Flag the folder-structure change before touching it.**
>    Ledgerkit's own `CLAUDE.md` "Unauthorised Change Rule" requires
>    explicit user approval before changing the documented folder
>    structure, `pyproject.toml`, or `dev-docs/api-spec.md`. This
>    migration changes the folder structure (§A.1/§B). State exactly
>    what will change (the §A.1 removal list, the §B addition list) and
>    get the user's explicit confirmation **before** making any of
>    these changes, even though the overall migration direction is
>    already authorised at the planning level.
> 3. **Remove, per §A.1.** Delete the CodeCompass tooling/generated-
>    state/skill/command/agent/validation-findings paths named there.
>    Confirm each is genuinely CodeCompass-exclusive by reading it
>    first, not by pattern-matching the word "codecompass" alone — §A's
>    own explicit non-goal applies to you too.
> 4. **Reconcile dangling references.** Several preserved files
>    (`.claude/agents/domain-skeptic.md`, `implementation-reconstructor.md`,
>    `docs-maintainer.md`, `docs-reconstructor.md`, `release-phase-auditor.md`)
>    cite the historical planning/retro docs named in §A.3. If you
>    remove those docs from the active tree, fix or annotate every
>    citation in the same change — a dangling path reference is a
>    documentation defect, not an acceptable side effect.
> 5. **Install, per §B.** The skill, the pinned library/launcher, the
>    `knowledge/README.md` register directive, the one genuine scope
>    manifest (not Axiom Dev's own disposable scratch-eval placeholder
>    — write a real one), the four-claim wiki, the `.gitignore`
>    addition, and the `CLAUDE.md` replacement section.
> 6. **Reconcile documentation and knowledge.** Add the CodeCompass-
>    retirement decision and its rationale to `knowledge/DECISIONS.md`
>    in the same change (Ledgerkit's own standing rule). Resolve or
>    explicitly flag for the user the pending `ROADMAP.md` confirmation
>    on the CodeCompass-upgrade initiative row (§A.3) — do not silently
>    mark it `[DONE]` yourself; that decision belongs to Ledgerkit's
>    owner. Update `CONTEXT.md` to reflect the migration's actual
>    state.
> 7. **Run the acceptance criteria in §C**, in order, with real
>    commands and real output — including criterion 3's genuinely
>    fresh agent session and criterion 5's full existing test suite.
>    Record what you ran and its actual result; never infer a pass
>    from generated text.
> 8. **Publish a PR, request native Codex review, disposition findings**
>    under Ledgerkit's own bounded-correction discipline (mirror
>    Axiom Dev's own `AGENTS.md` §14 if Ledgerkit has no equivalent of
>    its own: a bounded number of corrective rounds, stop and escalate
>    rather than retry indefinitely).
> 9. **Do not merge.** Report the PR URL, the exact removal/addition
>    diff, the acceptance-criteria evidence, and any unresolved risk to
>    Ledgerkit's repository owner, and wait for their explicit merge
>    approval — the same human-approval boundary Axiom Dev's own PRs
>    (#5, #6) were held to.

---

## E. Open questions for the human owner (not resolved by this handoff)

1. **The CodeCompass-upgrade `ROADMAP.md` row** ("Phases 1-6 complete...
   awaiting explicit user confirmation") — confirm it `[DONE]` (the
   clean-room documentation refresh it produced is real and complete,
   independent of CodeCompass's own fate), confirm it `[DONE]` with a
   superseded/retired annotation, or decide otherwise. Not inferred
   here, per Ledgerkit's own standing rule.
2. **The clean-room methodology apparatus** (`dev-docs/clean-room/`'s
   scripts, templates, snapshots, assertions, comparison reports,
   drafts — A.2) — keep as a standing, general-purpose documentation-
   QA capability independent of this migration, or archive it
   alongside Plan 29's closeout. Either is consistent with this
   migration; neither is required by it.
3. **Exact removal of the historical planning/retro docs (§A.3)** —
   recommended, not mandatory; Ledgerkit's own owner may prefer to
   retain them in place as permanent decision history (the same
   argument Axiom Dev itself applies to its own `decisions/*.md`
   ADRs), accepting the "clutter" the authorising prompt warns against
   as a lesser cost than losing in-tree context.
