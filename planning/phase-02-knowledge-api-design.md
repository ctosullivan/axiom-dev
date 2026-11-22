# Minimal knowledge API design — claim model, identity, operations, contracts

**Status: Proposed design, not implemented.** Answers this assignment's
§6/§16.D. Builds directly on ADR 0008 (Decisions 3–4) and
`planning/phase-02-template.md` §2.2–2.3; made concrete against the
actual Stage 2.1 consumer (Ledgerkit) rather than written in the
abstract.

## 1. Three concepts, kept exactly three

**Claim**: a precise, scoped assertion with an evidence status
(INTENDED/OBSERVED/VERIFIED/UNCERTAIN/CONTESTED — reusing
`docs/knowledge-placement.md`'s existing taxonomy verbatim, not
inventing a new one) and, where the claim is a Ledgerkit/hledger
comparison specifically, a *separate* mapping-result axis
(equivalent/partial/divergent/unknown — per the authorising prompt's
§7; this is orthogonal to evidence status, not a replacement for it: a
claim can be OBSERVED-and-divergent, or VERIFIED-and-equivalent, and
the two axes must never be collapsed into one field).

**Source**: the code, spec, or reference behaviour supporting a claim,
pinned to a specific revision (commit SHA or exact version string —
never "latest").

**Evidence**: a reproducible observation, test, or independently
reviewed assessment supporting or challenging a claim, itself pinned
to the source revision it was taken against.

No fourth concept is introduced. "Relationship" and "revision history"
(both required by ADR 0008 Decision 4) are fields *on* a Claim, not
separate record types — see §3.

## 2. Identity

**For Ledgerkit specifically: reuse its existing identity scheme,
don't invent a second one.** `dev-docs/compat-register/schema.md`
already defines `LK-<KIND>-<AREA>-<NNN>` (stable, never reused, matches
the filename) with `KIND` ∈ `COMPAT`/`EXT`/`DIV`/`UNSUP`/`MISMATCH`.
This independently-arrived-at scheme already satisfies ADR 0008
Decision 4 in full: globally unique, persistent, independent of
title, separate from revision/status, with an explicit non-destructive
supersession mechanism (`resolved_into`/`resolves`, reciprocal pair).
Axiom's knowledge API's identity contract for a *Ledgerkit* claim is
therefore: **an ID is whatever `dev-docs/compat-register/`'s own
schema says it is; Axiom does not re-mint one.**

**For a consumer with no existing register** (the default
`knowledge/claims/` layout, `planning/phase-02-adoption-design.md` §2),
the generic default format is deliberately modelled on the same shape,
since an independently-built real project converging on it is evidence
the shape is sound, not a coincidence to ignore:

```
<PROJECT>-<KIND>-<AREA>-<NNN>
```

- `PROJECT`: short, fixed per-repo prefix (e.g. a consumer sets this
  once, in `knowledge/README.md`).
- `KIND`: a small closed set, consumer-defined but recommended as
  `COMPAT`/`EXT`/`DIV`/`UNSUP`/`MISMATCH` for a compatibility-mapping
  use case, or a project's own equivalent closed set for a different
  kind of claim.
- `AREA`: short slug.
- `NNN`: zero-padded sequence, never reused even if a claim is deleted
  (deletion is itself discouraged — see §5, supersession instead).

**Only governed knowledge artifacts and materially testable claims get
an ID** — ADR 0008 Decision 4 and the authorising prompt's §2.E, both
followed exactly: an ordinary explanatory sentence in the wiki does not
get a claim ID merely for existing.

## 3. Claim schema (illustrative, generic default)

```yaml
id: <PROJECT>-<KIND>-<AREA>-<NNN>       # stable identity, see §2

area: <dotted path>                      # e.g. "parser.balance_assignment"

kind: <project-defined closed set>       # e.g. compatible | extension
                                          # | intentional_divergence
                                          # | unsupported | unexplained_mismatch

mapping_result: equivalent | partial | divergent | unknown
                                          # ONLY present for a comparative
                                          # claim against an external
                                          # reference; orthogonal to `status`

status: INTENDED | OBSERVED | VERIFIED | UNCERTAIN | CONTESTED
                                          # docs/knowledge-placement.md's
                                          # taxonomy, reused verbatim

scope: >
  Exact boundary of what this claim covers (inputs, versions,
  configuration) — a claim with no stated scope cannot be VERIFIED,
  only UNCERTAIN, regardless of how much evidence exists.

assumptions:
  - <explicit assumption the claim depends on>

source:
  project: <name>                        # "self" for the consumer's own code
  ref: <file:line, function, or doc section>
  pinned_at: <exact commit SHA or version — never "latest">

evidence:
  - kind: manual | source | executable | test
    ref: <URL, file:line, or exact command run>
    pinned_at: <version/commit — required for executable/test evidence>
    reviewed_by: <agent/person, required once status is VERIFIED>
    reviewed_date: <YYYY-MM-DD>

related:
  - <other claim ID>                     # explicit only — never inferred

resolved_into: <new claim ID>            # optional, non-destructive
resolved_date: <YYYY-MM-DD>              # required once resolved_into is set
resolves: <old claim ID>                 # reciprocal, set on the new claim

reason: >
  Why this status/kind was chosen — the single field independent
  review should scrutinise hardest, per Ledgerkit's own schema notes:
  a thin or missing reason means not-yet-ready, regardless of what
  status is claimed.
```

Fields excluded on purpose, matching the authorising prompt's §6 and
§14: no confidence score (collapses the five-state taxonomy into one
number, explicitly prohibited), no free-form tag cloud, no
auto-computed "last verified" staleness timer (computed from Git
history on demand by `impacted()`, not stored and allowed to go
stale itself), no embedding vector.

## 3a. Reading an existing non-Axiom register (adapter contract)

**Found missing by independent review (`planning/phase-02-planning-review.md`
§3, BLOCKING 2) and specified here rather than left implicit; corrected
again in this revision (§3 and §3b below) after a second independent
review found the first version's translation itself was too generous
in two places** (`self-verified`/`proposed` status handling — now
fixed; see `planning/phase-02-planning-review.md`'s corrective-review
addendum). When `get`/`find`/`related`/`impacted` read a claim from an
existing, non-Axiom register (the Stage 2.1 case: Ledgerkit's
`dev-docs/compat-register/`), the native record is **never** silently
assumed to already match §3's generic schema field-for-field — it does
not. `get()` returns **native fields and derived fields kept visibly
separate**, never merged into one ambiguous view:

```yaml
id: <native ID, unchanged — e.g. LK-COMPAT-PARSER-BALANCEASSIGN-001>

native:
  status: <verbatim — e.g. "self-verified">
  relationship: <verbatim — e.g. "superset">
  verified_by: <verbatim, or absent>
  verified_date: <verbatim, or absent>
  <every other field exactly as read, unmodified>

derived:
  status: <Axiom's INTENDED|OBSERVED|VERIFIED|UNCERTAIN|CONTESTED — see §3b>
  status_basis: <one line citing which native fields justified it>
  mapping_result: <equivalent|partial|divergent|unknown — see §3c>
  mapping_scope: <required whenever mapping_result is derived from a
                  superset/subset relationship — see §3c; null only
                  when relationship was already `equivalent`/`incomparable`>
  scope: <from a passing scope manifest, or null if none exists — see
          §3b.1/§3d; never fabricated from area/reason>
  reviewer: <native verified_by, surfaced at the top level deliberately
             — see §3b; null if absent>

evidence: <native evidence list, field names unchanged>
related: <native resolved_into/resolves, unchanged>
```

The **native** block is never altered by Axiom's reading of it — it is
exactly what Ledgerkit's own schema and review process produced. The
**derived** block is Axiom's own, conservative, explicitly-justified
reading of what that native record supports under Axiom's own
definitions — and, per the sections below, it is frequently *weaker*
than a naive reading of the native status would suggest, never
stronger.

### 3b. Status and reviewer-identity mapping — conservative by construction

**Corrected again in this revision.** `docs/knowledge-placement.md`
itself already defines VERIFIED as "OBSERVED behaviour checked against
an accepted contract, **within a stated scope**, by someone/something
other than the implementer" — Axiom's own, already-accepted Phase 1
vocabulary, not a new requirement invented for Ledgerkit. The prior
revision's mapping could still produce `derived.status: VERIFIED`
together with `derived.scope: null` (§3d's unconditional null),
which directly contradicts that definition — a real defect, not a
style nit, found and fixed here. **Two independent gates now apply,
and both must pass before `derived.status` can be `VERIFIED`**: the
reviewer-identity gate (unchanged from the prior revision) and a new
scope gate (§3b.1).

| Ledgerkit `status` | Axiom `derived.status` | Why |
|---|---|---|
| `proposed` | `UNCERTAIN` | Ledgerkit's own schema note: "hledger-researcher's reading; **not yet run against the real binary**." No execution has happened at all. |
| `self-verified` | `OBSERVED`, **never** `VERIFIED` | a real comparison WAS run with real output, but by the same identity that implemented the fix — mapping this to `VERIFIED` would launder a self-check into independent status. OBSERVED has no scope requirement (`docs/knowledge-placement.md` states none for this tier), so the scope gate does not apply here. |
| `verified` | `VERIFIED` **only if both gates pass**; otherwise `UNCERTAIN` | reviewer-identity gate: `verified_by`/`verified_date` both present and non-empty on the native record. Scope gate: §3b.1. **Missing either is treated as missing evidence, not contradictory evidence** — corrected in this revision; an earlier draft mapped missing reviewer metadata to `CONTESTED`, conflating "nothing was recorded" with "two things disagree." `CONTESTED` is reserved for an actual conflict (§3b.2, §3c). |
| `final` | Same two gates as `verified` | additionally reconciled/published; the evidence status is unchanged from `verified`'s own rule. |

**Reviewer-identity field mapping.** Ledgerkit's own schema
(`dev-docs/compat-register/schema.md`, read in full) stores reviewer
metadata as **top-level fields on the register entry itself**,
`verified_by`/`verified_date` — not nested inside individual
`evidence[]` items. The adapter maps `native.verified_by` →
`derived.reviewer` at the top level, exactly where Ledgerkit's own
schema puts it; it does not invent a per-evidence-item reviewer where
the native schema has none.

**What a present `verified_by` name does and does not prove.** It
satisfies the *mechanical* precondition for the reviewer-identity
gate — it does **not**, by itself, constitute deterministic proof the
named reviewer was actually independent of the implementer. That is a
**process** guarantee (Ledgerkit's own rule that `status: verified`
"must NEVER be written into a register YAML directly [by the
implementer] — only a dispatched `compat-differential-tester` agent's
own output sets it"), not something the API can verify by inspecting
a string. The mechanical check is necessary, not sufficient: it blocks
the clear failure case (claimed `verified`/`final` with no reviewer
recorded at all); independence of the named reviewer remains a
human/process judgement, exactly as `docs/agent-isolation.md` already
treats isolation-level claims generally.

### 3b.1. The scope gate — a small, optional, separately-reviewed evidence manifest

**New in this revision**, closing the gap above. Ledgerkit's
compat-register schema genuinely has no scope field (§3d) — the fix is
**not** to expand that schema (rejected explicitly: Ledgerkit's own
schema is not Axiom's to rewrite, and a second, Axiom-shaped field
bolted onto a schema other projects also use would itself be exactly
the kind of unnecessary coupling this project's complexity budget
warns against) and **not** to fabricate a scope string from `area` or
`reason` prose (explicitly prohibited — those fields describe the
claim, they do not commit to an evidence-reviewed boundary of what was
actually checked).

Instead: an **optional**, small, Axiom-owned YAML file, one per claim
that needs a derived `VERIFIED` status, at
`knowledge/scope-manifests/<claim-id>.yaml` in the consuming
repository (a new, minimal addition to the adoption file layout —
`planning/phase-02-adoption-design.md` §2 — not a change to
Ledgerkit's own schema or directory):

```yaml
claim_id: <must exactly match the native record's own ID>
scope: >
  Explicit boundary of what was actually checked (inputs, versions,
  configuration) — never copied from the native record's `area` or
  `reason`; written and reviewed specifically as a scope statement.
source_pin: <revision this scope statement was written/reviewed
             against — must be consistent with the native record's
             own upstream.compatibility_target, checked below>
reviewed_by: <independent reviewer of this scope statement specifically
              — a separate check from the native record's own
              verified_by; the same person/agent may hold both roles
              only if actually independent of the implementation,
              exactly as for any other reviewer-identity claim>
reviewed_date: <YYYY-MM-DD>
```

**Minimum deterministic requirements for a manifest to support
`derived.status: VERIFIED`** (all five, mechanically checkable,
no judgement call left to the API itself):

1. The file exists, is Git-tracked (an untracked/scratch file does not
   count — it must be reviewable the same way any other change is).
2. `claim_id` matches the native record's `id` exactly.
3. `scope` is present and non-empty.
4. `reviewed_by`/`reviewed_date` are both present and non-empty.
5. `source_pin` matches (or is not contradicted by) the native
   record's own `upstream.compatibility_target`.

**If no manifest file exists for a claim**: `derived.scope: null`,
`derived.status: UNCERTAIN` — missing evidence, not a contradiction,
even if the native record says `verified` with reviewer metadata
present. This is the fix for the exact defect this section opened
with: a claim cannot be `VERIFIED` with no stated scope, full stop.

**If a manifest exists but fails check 2 or 5** (wrong claim, or a
`source_pin` that contradicts the native record's own pin): this *is*
a genuine conflict between two evidence sources — `derived.status:
CONTESTED`, matching `docs/knowledge-placement.md`'s own CONTESTED
definition exactly, not merely treated as if the manifest were absent.

**If a manifest exists and passes all five checks**: `derived.scope`
is set to the manifest's `scope` string, and — combined with the
reviewer-identity gate from §3b — `derived.status` can be `VERIFIED`.

**The native record's own `status: verified` remains visible
regardless of what `derived.status` concludes** — `native.status` is
never altered by any of the above (§3a); a caller reading `native:`
sees Ledgerkit's own claim unchanged, and a caller reading `derived:`
sees Axiom's own, possibly weaker, conclusion. Both are always
present; neither silently overwrites the other.

### 3b.2. Changed-source-revision case

If the native record's `upstream.compatibility_target` changes (the
compatibility target version is bumped) after a scope manifest was
written against the old pin, check 5 above now fails against the
*current* native record — `derived.status` becomes `CONTESTED` on the
next `get()`, not silently still `VERIFIED` against a stale scope.
This is also surfaced proactively by `impacted()` (§4's "just bumped,
scope manifest stale" case), not only reactively on the next `get()`
— **corrected per native Codex review, commit `441f4c8`**: an earlier
draft asserted the two mechanisms "agree with each other by
construction" without `impacted()`'s predicate actually covering the
case where the claim's own pin has *already* been bumped (which is
exactly when a stale scope manifest first becomes detectable) — fixed
by giving `impacted()` the matching second case, so the two checks now
genuinely examine the same condition from each side rather than one of
them silently never firing.

### 3c. Relationship → mapping_result — scoped, never silently collapsed

**Corrected in this revision**: an earlier draft mapped `superset` to
a bare, unqualified `equivalent`, which the authorising prompt's §4.C
specifically warns against ("a superset must not silently become an
unqualified equivalent"). Fixed by requiring an explicit
`mapping_scope` string whenever the native relationship is not already
a 1:1 `equivalent`/`incomparable`:

| Ledgerkit `relationship` | Axiom `mapping_result` | Required `mapping_scope` (always present for these two rows) |
|---|---|---|
| `equivalent` | `equivalent` | not required (already unqualified) |
| `superset` | `equivalent` | **required**: `"equivalent for hledger-defined behaviour only; Ledgerkit's extension behaviour (kind: extension) is additional and out of scope for this comparison"` |
| `subset` | `partial` | **required**: `"partial — Ledgerkit intentionally covers less than hledger for this area; see native.reason for which cases are excluded"` |
| `incomparable` | `divergent` | not required (already unqualified) |
| *(no `relationship` value — entry's `kind` is `unexplained_mismatch`)* | `unknown` | not required — `unknown` is itself the honest statement; there is nothing yet to scope |

A caller reading `derived.mapping_result: equivalent` with no
`mapping_scope` present can rely on it meaning full, unqualified
equivalence. A caller reading it **with** a `mapping_scope` present
must read that string before treating the claim as applying beyond
the stated boundary — the field's mere presence is itself the signal
that a qualification exists, not just its content.

### 3d. Known gap — scope field absent from the native schema

The compat-register schema has **no field carrying scope/input-boundary
information** — confirmed directly against `dev-docs/compat-register/schema.md`,
which has no `scope` key. `derived.scope` on a Ledgerkit-backed claim
is `null` **unless a separately-reviewed scope manifest exists and
passes §3b.1's five checks**, in which case it is that manifest's
`scope` string. A human wanting the scope, absent a manifest, reads
that entry's `area` and `reason` fields directly — those remain
non-authoritative for `derived.scope` itself, by design (§3b.1: never
fabricated from them).

### 3e. Terminology note

A compat-register entry **is a Claim**, in this API's own three-concept
vocabulary — not a `Source`. Its `upstream:` block (project + pinned
version) is that Claim's `Source`; its `evidence:` list is that
Claim's `Evidence` list.

### 3f. Native dependency extraction — what `impacted()` reads from a native record

**New in this revision.** The compat-register schema's own fields
already enumerate exactly what a claim depends on; `impacted()`
extracts from them directly, with the simplest deterministic rule
that works — **path matching, not an AST or a dependency graph**:

**Two separate revision spaces, never conflated.** A native claim's
`upstream.compatibility_target` identifies an **hledger** version
(e.g. `"1.52.4"`) — it has no meaning as a revision of the **Ledgerkit**
repository, where `implementation[]`/`tests[]` paths actually live.
Checking whether `ledgerkit/parser.py` "exists at revision 1.52.4"
is not a well-formed question — an earlier draft of this section did
exactly that, found and confirmed wrong by native Codex review (see
disposition below). The corrected rule: local references
(`implementation[]`, `tests[]`, and any `evidence[].ref` whose `kind`
describes Ledgerkit's own code) are resolved against an explicit
**consumer-repository revision** — the Ledgerkit commit the caller is
currently evaluating against (ordinarily Ledgerkit's own current
HEAD, or the specific commit a historical `impacted()` run is
checking) — never against `upstream.compatibility_target`, which is
reserved exclusively for the `upstream:<project>` pseudo-path case
below.

| Native field | What it identifies | Extraction rule |
|---|---|---|
| `implementation: [<path>:<qualifier>, ...]` | Ledgerkit source location(s) the claim's behaviour depends on | Split each entry on the **last** `:` — everything before it is the file path, resolved against the **consumer-repository revision** (above, never `compatibility_target`) and matched against a Git change the same way. The qualifier (function/class name) is kept for the impact report's human-readable reason; matching itself is file-level, per this project's complexity budget ("deterministic path matching should be sufficient initially") |
| `tests: [<path>::<Class>::<method>, ...]` | regression/verification dependency | Split on the **first** `::` for the file path, same consumer-repository-revision, file-level matching; a test file counts as a dependency exactly like an implementation file — this closes a real gap the prior revision's `evidence[].ref`-only matching left open: a changed *test*, with no corresponding `implementation[]`/`evidence[]` entry touched, previously would not have flagged anything |
| `upstream: {project, compatibility_target}` | the external reference version the claim was evaluated against | Not a local file path, and **not resolved against the consumer-repository revision at all** — represented as a pseudo-path `upstream:<project>` (e.g. `upstream:hledger`) in a change record, with `base`/`head` being the pinned version *before* and *after* a bump. A caller comparing the native record's own `compatibility_target` across two reviewed revisions of the compat-register file builds this change record; `impacted()` does not reach into `~/projects/hledger` itself |
| `evidence: [{kind, ref, pinned_at}, ...]` | supporting observations, each pinned | `ref` matched the same way as `implementation[]` **only when it names a Ledgerkit-local path**, resolved against that evidence item's own `pinned_at` (a Ledgerkit commit) if `pinned_at` is given, falling back to the consumer-repository revision otherwise — never against `compatibility_target`. An evidence item describing hledger's own source/behaviour (not a Ledgerkit path) is not path-checked against the Ledgerkit tree at all; see the gap noted below |

**Resolving a qualified reference to a file** is the one new piece of
logic this revision adds, and it is intentionally the simplest rule
that is still correct for Git's own change granularity: Git reports
changes at the file level (or with line hunks, not named functions),
so a `path:function_name` or `path::Class::method` reference is
resolved to `path` alone for matching purposes — a change *anywhere*
in that file is a potential impact on any claim naming a qualifier in
it, which is deliberately conservative (more false positives than a
function-aware tool would produce) rather than silently under-matching
by trying to be clever about which lines actually moved. Stage 2.4's
drift demonstration (`planning/phase-02-stage-2.1-plan.md` §6.2)
measures how often this conservative choice produces a false positive
in practice, rather than asserting it won't.

**Missing or ambiguous references are reported, not silently
ignored.** A local (`implementation[]`/`tests[]`/Ledgerkit-path
`evidence[].ref`) entry that does not parse into the `path:qualifier`
or `path::Class::method` shape above, or whose extracted path does
not exist in the Ledgerkit repository at the **consumer-repository
revision** being checked (that evidence item's own `pinned_at` if
given, else the revision the caller is currently evaluating against
— **never** `compatibility_target`, which names an hledger version
and is not a Ledgerkit revision at all — corrected per native Codex
review, commit `e83df4b`'s finding on this exact paragraph),
produces an `unresolved_reference` diagnostic on that claim —
distinct from an impact finding (it is a data-quality problem with
the claim's own record, surfaced the same way a dangling reference is
surfaced elsewhere in this design, §6) — rather than being dropped
from consideration with no trace. An `evidence[].ref` describing
hledger's own source (not a Ledgerkit path) is not checked for local
existence at all — it is out of scope for this diagnostic, not
silently treated as resolved.

## 4. Operations

Read-only in Phase 2 (ADR 0008 Decision 3: "not postponed until MCP,"
but also not a write API — Git/PR review is the write path,
`AGENTS.md` §9). Implemented as a small Python library with a thin CLI
wrapper (`axiom-knowledge <op> ...`), reading Markdown/YAML directly,
with an optional in-memory index rebuilt per invocation — no persistent
server, per architectural principle C.

### `get(id) -> Claim | NotFound`

Returns the claim/artifact record and its evidence list, scope, status
and relationships. **Minimum data returned:** `id`, `source`,
`evidence` (full list), `related` (IDs only, not expanded — expansion
is `related()`'s job), and — for a default-schema claim — `status`/
`scope` directly, or — for a claim read from an existing native
register (§3a–§3e) — the `native`/`derived` pair, never collapsed into
one ambiguous view. If `resolved_into` is set, `get` returns the
record **and** a pointer to the superseding ID — it never silently
redirects, since the authorising prompt's §6 requires identity/
revision/status to stay distinct and visible.

**Errors:** `NotFound` (no record at that ID — distinct from
`Superseded`, which still returns the historical record plus the
pointer, not an error). A malformed record (fails schema validation)
returns a `Malformed` result naming the specific field, not a generic
exception — this is the same check `planning/phase-02-template.md`
§2.3's CI schema validation reuses (found as a garbled cross-reference
by independent review, `planning/phase-02-planning-review.md` §8,
Material-Nonblocking 3, and corrected here).

### `find(query) -> list[Claim]` (deterministic)

Exact-ID lookup, plus deterministic text/metadata search (substring or
field-equality match over `area`, `kind`, `status`) — **no fuzzy
ranking, no embeddings**, so the same query always returns the same
ordered result for the same repository state (ADR 0008 Decision 3;
authorising prompt's explicit "No embeddings or vector retrieval
without a demonstrated requirement"). Empty result is a valid, non-error
return (`[]`), distinct from a malformed-query error.

**Errors:** `InvalidQuery` for a syntactically malformed query
(reserved-character misuse, empty string where a field name is
required) — never a silent empty result standing in for "the query
itself was wrong."

### `related(id) -> list[Claim]`

Follows **only explicit** `related`/`resolved_into`/`resolves` links
declared on the record itself — no inferred graph, no transitive
closure by default (a consumer wanting transitive traversal calls
`related` repeatedly and composes it themselves; the API does not grow
a graph-traversal feature until a real case needs one).

**Errors:** `NotFound` if `id` itself doesn't exist. A dangling related
ID (points at something that no longer exists and has no
`resolved_into` chain) is returned as part of the result with an
explicit `dangling: true` marker on that entry, not silently dropped —
dangling references are exactly what the CI integrity check (§2.3) is
also responsible for catching mechanically; the API surfaces the same
condition at read time rather than disagreeing with CI about it.

### `impacted(changes) -> list[ImpactReport]`

**Input redesigned in this revision.** The original design treated a
nonexistent path as a malformed request — found wrong by the
authorising prompt's §5: a deleted source file is a legitimate,
common kind of change, not an error. `impacted()` now takes
**Git-derived change records**, not bare paths:

```yaml
changes:
  - base: <revision>              # required
    head: <revision>              # required
    path: <repository-relative path>
    change_type: added | modified | deleted | renamed
    old_path: <required when change_type == renamed, else absent>
```

This is the simplest input shape that distinguishes every case the
authorising prompt's §5 requires, and is exactly what `git diff
--name-status <base> <head>` already reports — `impacted()`'s caller
is expected to build this list from that output (or equivalent),
not invent change detection itself.

**Output and semantics**, per change type — matching extracted against
**every** native dependency field from §3f (`implementation[]`,
`tests[]`, `evidence[].ref`, and the `source.ref`/default-schema
equivalent), not evidence alone:

- **`modified`**: every claim with an extracted file-level reference
  (§3f) under `path`, or whose pinned revision no longer matches
  `head`'s revision of that path, is flagged `possible_impact: true`
  with the specific reference and native field (`implementation`,
  `tests`, `evidence`, or `upstream`) that triggered it.
- **`deleted`**: every claim referencing `path` (any of §3f's fields)
  is flagged `possible_impact: true`, reason `"source deleted"` — a
  deletion is **not** treated as proof the claim is now false (the
  behaviour it described may have moved, or the claim may need
  retiring — a human/reviewer decides which), only as a certain reason
  to look.
- **`renamed`**: every claim referencing `old_path` (any §3f field) is
  flagged `possible_impact: true`, reason `"source renamed to
  <path>"` — **preserving the ability to find claims that reference
  the old path** is the specific requirement this case exists for; the
  API does not silently update the claim's own reference (that is a
  human/reviewer edit through a normal commit, per §5).
- **`added`**: never produces an impact entry on its own (nothing
  existing could have depended on a path that didn't exist before) —
  included in the input schema only so a caller's Git-diff-derived
  change list doesn't need pre-filtering before calling `impacted()`.
- **`upstream:<project>` pseudo-path, `modified`** (§3f): **two cases,
  not one — corrected per native Codex review, commit `441f4c8`'s
  finding on this exact rule.** The original rule only flagged a
  claim still pinned at `base` — but a caller following §3f's own
  stated workflow constructs this change record *after* the
  compat-register entry has already been edited to bump
  `compatibility_target` to `head`, so that claim's own field already
  equals `head` by the time `impacted()` runs, and the original rule
  excluded exactly the claim whose pin just changed — the one case
  §3b.2 ("changed-source-revision") promises `impacted()` would catch
  proactively. Both cases are now checked:
  - **Not yet bumped**: `upstream.compatibility_target` still equals
    `base` → flagged, reason `"upstream revision changed from <base>
    to <head>, claim not yet re-pinned"`.
  - **Just bumped, scope manifest stale**: `upstream.compatibility_target`
    now equals `head`, **and** the claim has an associated scope
    manifest (§3b.1) whose `source_pin` does not also equal `head` →
    flagged, reason `"claim re-pinned to <head>, scope manifest still
    references <manifest's source_pin>"` — this is the proactive
    counterpart of §3b.2's reactive `get()`-time `CONTESTED` check;
    the two are required to agree (a claim `impacted()` doesn't catch
    here must not then surface as `CONTESTED` on `get()` with no
    corresponding impact history, and vice versa).
  A claim with no scope manifest, or whose manifest's `source_pin`
  already equals `head`, is not flagged in either case — nothing left
  for either check to catch.

**This never sets or implies a status change** — per ADR 0008
Decision 4/§5 of the authorising prompt, change detection establishes
*possible* impact, never proven invalidity, and never proven
*un*-impact either: `impacted()`'s output is a worklist for a human/
independent reviewer, not a verdict in either direction. An unaffected
claim is not returned at all (not returned-with-`possible_impact:
false`) — keeping the "affected" set small and actionable is more
useful than echoing every claim back with a boolean.

**Errors:** `InvalidChangeSpec` for a change record missing `base`/
`head`, or a `renamed` record missing `old_path` — these are
structural defects in the request itself, distinct from every case
above, all of which describe a *legitimate* source change. A `path`/
`old_path` that doesn't exist at the stated revision is **not** an
error by itself — Git's own diff output is the source of truth for
whether a change is legitimate; `impacted()` trusts the caller's
change records rather than re-deriving them from a live checkout.

### Introduced incrementally, full four-operation target retained

Per ADR 0008 Decision 3 and the authorising prompt's §6: Stage 2.2
needs `get` and `find` to demonstrate retrieval; `related` and
`impacted` are not built until Stage 2.3/2.4 actually exercises them
(deterministic integrity gating and drift detection, respectively).
The four-operation **interface is specified now**, in full, so Stage
2.2's implementation doesn't have to guess at a shape Stage 2.3 will
need; only the *build order* is incremental.

## 5. Write path — explicitly none

No `set`/`update`/`delete` operation exists. A claim changes by an
ordinary Git commit editing its YAML file, reviewed like any other
change (`AGENTS.md` §9). Deletion is discouraged in favour of
supersession (`resolved_into`) so historical evidence is never erased —
matching ADR 0008 Decision 4 and Ledgerkit's own existing convention
exactly (§2 above). `impacted()` never writes a status; a human/
reviewer edits the file after assessing the flagged claim.

## 6. Contract tests (negative cases required before Stage 2.3 build)

**6.0 Validation applies differently to native and generic-default
records — stated explicitly, per this revision's own correction.**
The tests immediately below (duplicate ID through superseded-ID
redirect) apply to records in Axiom's **own default schema** (§3,
`knowledge/claims/`, used only when no existing native register
exists — `planning/phase-02-adoption-design.md` §2). For a claim read
from an **existing native register** (Ledgerkit's compat-register),
these same tests do **not** run against the native file at all —
Ledgerkit's own schema and its own validation (whatever Ledgerkit's
own CI or convention already checks, unchanged by Axiom) governs the
native record's own well-formedness; Axiom never requires a native
record to grow a field it doesn't have (`evidence[].reviewed_by`
included) merely so Axiom's own validator has less to special-case.
What Axiom *does* validate for a native-backed claim is §3b–§3d's
**derived** view — whether the normalised result the adapter produces
is internally consistent and conservative — tested separately in
"Native-register translation tests" below, which replaced an earlier
draft's wrong assumption that Ledgerkit's `evidence[]` items carry a
`reviewed_by` field (they don't; see §3b).

**Default-schema tests:**

- **Duplicate ID**: two records claiming the same `id` → CI failure
  naming both file paths (mechanical integrity, §2.3 of
  `planning/phase-02-template.md`).
- **ID reuse after deletion**: a new record reusing a previously-used
  ID without a `resolves` chain → CI failure.
- **Dangling source/evidence reference**: `source.ref` or an
  `evidence[].ref` naming a file/line that doesn't exist at
  `pinned_at` → CI failure, and `get()`/`related()` surface it as
  described in §4, not merely CI.
- **Missing `reason` on a non-`unsupported` kind** → CI failure
  (mechanising Ledgerkit's own existing *documented convention* —
  confirmed, via independent review, that this is a human convention
  in `schema.md`'s field notes, not something Ledgerkit's own CI
  already enforces; Axiom would be the first mechanical enforcement of
  it, not a reuse of an existing gate — corrected wording per
  `planning/phase-02-planning-review.md` §3, Advisory 6).
- **`status: VERIFIED` with no `evidence[].reviewed_by`** — **this
  test is specific to Axiom's own default schema (§3), which chose to
  put reviewer identity on each evidence item; it is not a general
  rule and must not be applied to a native register with a different,
  equally valid convention** (§3b's top-level `verified_by` for
  Ledgerkit is the native-register analogue, tested separately below)
  → CI failure for the default schema case (this is the mechanical
  half of preventing the implementer from self-certifying `VERIFIED`;
  the semantic half — confirming the reviewer was genuinely
  independent — remains human/reviewer judgement, per
  `docs/agent-isolation.md`).
- **`resolved_into` set without a reciprocal `resolves`** on the target
  → CI failure (asymmetric supersession is exactly the kind of
  "quietly edit history" this project's conventions exist to prevent).
- **`get(id)` for a nonexistent ID** → `NotFound`, not an exception
  that crashes a caller; **`get(id)` for a superseded ID** → returns
  the historical record plus the `resolved_into` pointer, never a bare
  redirect.

**Native-register translation tests (§3a–§3e), the required set
from the authorising prompt's §2, by name:**

1. **Native verified + missing scope**: `native.status: verified`,
   `verified_by`/`verified_date` both present, **no scope manifest
   file exists** → `derived.status: UNCERTAIN` (not `VERIFIED`),
   `derived.scope: null` — missing evidence, not a contradiction;
   `native.status: "verified"` remains visible unchanged in the
   `native:` block regardless. This is the exact defect this revision
   exists to close — see §3b.1.
2. **Native verified + explicit, independently supported scope**: as
   above, but a Git-tracked scope manifest exists, `claim_id` matches,
   `scope`/`reviewed_by`/`reviewed_date` all present, `source_pin`
   consistent with the native `upstream.compatibility_target` →
   `derived.status: VERIFIED`, `derived.scope` set to the manifest's
   `scope` string.
3. **Missing reviewer metadata**: `native.status: verified` but
   `verified_by`/`verified_date` absent or empty → `derived.status:
   UNCERTAIN` — **corrected in this revision**: an earlier draft
   mapped this to `CONTESTED`, conflating "nothing was recorded" with
   "two things disagree." Nothing here disagrees; something required
   is simply missing.
4. **Self-verified evidence**: `native.status: self-verified` → always
   `derived.status: OBSERVED`, regardless of scope-manifest presence —
   the scope gate only applies to the `VERIFIED` tier.
5. **Conflicting evidence**: an entry's own `evidence[]` contains both
   a passing and a failing `executable` result at the same `pinned_at`
   → `derived.status: CONTESTED`, regardless of the native `status`
   field's value — an unresolved conflict in the evidence itself always
   takes precedence over whatever status was claimed. **This is the
   genuine-contradiction case test 3 above is deliberately not.**
6. **Changed source revision**: a previously-valid scope manifest's
   `source_pin` no longer matches the native record's current
   `upstream.compatibility_target` (the target version was bumped) →
   `derived.status: CONTESTED` on the next `get()`, not silently still
   `VERIFIED` against a stale scope (§3b.2); the same condition is
   also what `impacted()`'s `modified`/`upstream`-tracking case (§4)
   surfaces proactively.
7. **Unrecognised native status**: a `relationship` or `status` value
   outside the known enums (a future Ledgerkit schema revision adds
   one this adapter doesn't know about) → `derived.status: UNCERTAIN`
   with an explicit `translation_gap: true` marker and the raw native
   value preserved — never silently dropped, never crashes.

Additional translation tests carried over from the prior revision:

- **`superset`/`subset` relationship always carries a `mapping_scope`**
  — tested as a positive assertion (the field is present and non-empty)
  whenever `relationship` is one of those two values, and *absent*
  whenever it's `equivalent`/`incomparable`.
- **A scope manifest with a mismatched `claim_id`** (points at the
  wrong claim, e.g. a copy-paste error) → `derived.status: CONTESTED`
  on the claim it incorrectly names, same treatment as check 5 of
  §3b.1 generally — a manifest that fails checks 2 or 5 is a conflict,
  not an absence.

**Git-change (`impacted()`) regression fixtures** — the authorising
prompt's §3 required set, by name:

- **Modification of a referenced implementation file**: a claim's
  `implementation[]` entry resolves (§3f) to the changed `path`,
  `change_type: modified` → flagged, reason cites the specific
  `implementation[]` entry and its qualifier.
- **Modification or deletion of referenced tests**: a claim's
  `tests[]` entry resolves to the changed/deleted `path` → flagged,
  reason cites the `tests[]` entry — **this is a genuinely new case
  this revision adds**; the prior revision's extraction did not
  consider `tests[]` at all, so a changed test with no corresponding
  `implementation[]`/`evidence[]` entry touched would previously have
  produced no impact finding.
- **Changes to referenced evidence**: a claim's `evidence[].ref`
  under a deleted or modified path → flagged, same treatment as
  implementation/test references, not a weaker case.
- **Source rename**: a claim referencing `old_path` in any of
  `implementation[]`/`tests[]`/`evidence[].ref`, change record has
  `change_type: renamed`, `old_path` set, `path` the new location →
  flagged against the old reference, confirming the rename case is
  findable, not silently missed because the literal path changed.
- **Source deletion**: a claim referencing a deleted `path` in any
  §3f field → flagged, reason `"source deleted"`, no status implied.
- **Relevant upstream revision change where captured dependencies
  permit detection**: a claim with `upstream: {project: hledger,
  compatibility_target: "1.52.3"}`, change record
  `path: "upstream:hledger"`, `base: "1.52.3"`, `head: "1.52.4"` →
  flagged, reason `"upstream revision changed from 1.52.3 to 1.52.4"`.
  **Corrected per native Codex review, commit `c4c41a9`'s finding on
  this exact bullet**: a claim already pinned at `"1.52.4"` is **not**
  automatically "nothing left to flag" — §4's two-case upstream rule
  (added in an earlier round) still flags it if its scope manifest's
  `source_pin` doesn't also equal `"1.52.4"` (the
  "just-bumped-with-stale-scope-manifest" case). This retained-but-
  now-stale bullet asserted the single-case version of the rule after
  the two-case version had already replaced it in §4 — an internal
  contradiction, not a restatement. Only a claim with **no** scope
  manifest, or one whose manifest is already current, is genuinely
  not flagged once pinned at `head`.
- **An unrelated change with no dependency** (a path no claim's §3f
  fields reference at all) → no entries in the result; this is the
  false-positive check Stage 2.4's drift demonstration
  (`planning/phase-02-stage-2.1-plan.md` §6.2) exercises for real.
- **An invalid or unresolved source reference**: a claim's own
  `implementation[]`/`tests[]`/`evidence[].ref` entry that does not
  parse into the expected shape, or whose extracted path does not
  exist in the repository → an `unresolved_reference` diagnostic on
  that claim (§3f), not a crash and not silent dropping; distinct from
  `InvalidChangeSpec` below, which is about the **caller's input**,
  not the claim's own data quality.
- **Changed source with a relevant claim** → flagged with
  `possible_impact: true` and the specific reference (general case,
  subsuming the specific field cases above).
- **Changed source with no relevant claim** → claim absent from the
  result entirely (not returned with `possible_impact: false`).
- **Invalid revision or change specification**: a change record
  missing `base`/`head`, or `change_type: renamed` missing `old_path`
  → `InvalidChangeSpec`, distinguishing a malformed request from every
  legitimate-change case above, all of which succeed.
- **`impacted([])`** (empty change list) → `[]`, not an error.

## 7. What this explicitly is not

No graph database (plain files + an ephemeral in-memory index on each
CLI invocation). No persistent service (every operation is a one-shot
process). No embeddings/vector search (§4). No autonomous knowledge
generation (every claim is written and reviewed by a human/agent
through a normal commit, never auto-synthesised by the API). No MCP
transport (Phase 3's adapter wraps this same library; this library
works fully without it, per ADR 0008 Decision 3 and architectural
principle G).
