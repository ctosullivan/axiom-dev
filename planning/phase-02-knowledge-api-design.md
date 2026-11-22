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
  scope: null          # see §3d — never fabricated
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

**Corrected in this revision** (an earlier draft mapped `proposed` to
`OBSERVED`, which overstated it — see below):

| Ledgerkit `status` | Axiom `derived.status` | Why |
|---|---|---|
| `proposed` | `UNCERTAIN` | Ledgerkit's own schema note: "hledger-researcher's reading; **not yet run against the real binary**." No execution has happened at all — this is closer to an unconfirmed reading than an OBSERVED fact, so Axiom's honest default (`docs/knowledge-placement.md`: "insufficient evidence either way") applies, not `OBSERVED`. |
| `self-verified` | `OBSERVED`, **never** `VERIFIED` | a real comparison WAS run with real output, but by the same identity that implemented the fix. Mapping this to `VERIFIED` would launder a self-check into independent status — the exact circularity `AGENTS.md` §6/`decisions/0004` Amendment B exists to prevent. |
| `verified` | `VERIFIED`, **conditionally** | only if `verified_by` AND `verified_date` are both present and non-empty on the **native record itself** (see reviewer-identity rule below) — if either is missing despite `status: verified`, `derived.status` is `CONTESTED`, not `VERIFIED` and not silently `UNCERTAIN` either: a native record claiming `verified` with missing required metadata is an unresolved conflict between what it asserts and what it can actually support, which is exactly what `CONTESTED` means. |
| `final` | `VERIFIED`, same condition as `verified` | additionally reconciled/published; the evidence status is unchanged from `verified`'s own conditional rule — `final` does not bypass the metadata check. |

**Reviewer-identity field mapping, corrected.** Ledgerkit's own schema
(`dev-docs/compat-register/schema.md`, read in full) stores reviewer
metadata as **top-level fields on the register entry itself**,
`verified_by`/`verified_date` — **not** nested inside individual
`evidence[]` items, as an earlier draft of this design assumed by
specifying a generic `evidence[].reviewed_by`/`reviewed_date` for
every source without checking the one real source against it. The
adapter maps `native.verified_by` → `derived.reviewer` at the top
level, exactly where Ledgerkit's own schema puts it; it does **not**
invent a per-evidence-item reviewer where the native schema has none.

**What a present `verified_by` name does and does not prove.** A
non-empty `verified_by` field satisfies the *mechanical* precondition
for `derived.status: VERIFIED` above — it does **not**, by itself,
constitute deterministic proof that the named reviewer was actually
independent of the implementer. That is a **process** guarantee
(Ledgerkit's own rule that `status: verified` "must NEVER be written
into a register YAML directly [by the implementer] — only a
dispatched `compat-differential-tester` agent's own output sets it"),
not something the API can verify by inspecting a string. The API's
mechanical check is therefore necessary, not sufficient: it blocks the
*clear* failure case (claimed `verified`/`final` with no reviewer
recorded at all), while independence of the named reviewer itself
remains a human/process judgement, exactly as `docs/agent-isolation.md`
already treats isolation-level claims generally.

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
is therefore always `null`, never fabricated. A human wanting the
scope reads that entry's `area` and `reason` fields directly.

### 3e. Terminology note

A compat-register entry **is a Claim**, in this API's own three-concept
vocabulary — not a `Source`. Its `upstream:` block (project + pinned
version) is that Claim's `Source`; its `evidence:` list is that
Claim's `Evidence` list.

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
exception — this is also exactly what the CI schema check (§5 of
`planning/phase-02-template.md` §2.3) reuses.

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

**Output and semantics**, per change type:

- **`modified`**: every claim whose `source.ref`/`evidence[].ref`
  falls under `path`, or whose `pinned_at` no longer matches `head`'s
  revision of that path, is flagged `possible_impact: true` with the
  specific reference that triggered it.
- **`deleted`**: every claim referencing `path` is flagged
  `possible_impact: true`, reason `"source deleted"` — a deletion is
  **not** treated as proof the claim is now false (the behaviour it
  described may have moved, or the claim may need retiring — a human/
  reviewer decides which), only as a certain reason to look.
- **`renamed`**: every claim referencing `old_path` is flagged
  `possible_impact: true`, reason `"source renamed to <path>"` —
  **preserving the ability to find claims that reference the old
  path** is the specific requirement this case exists for; the API
  does not silently update the claim's `source.ref` itself (that is a
  human/reviewer edit through a normal commit, per §5).
- **`added`**: never produces an impact entry on its own (nothing
  existing could have depended on a path that didn't exist before) —
  included in the input schema only so a caller's Git-diff-derived
  change list doesn't need pre-filtering before calling `impacted()`.

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
- **`status: VERIFIED` with no `evidence[].reviewed_by`** → CI failure
  (this is the mechanical half of preventing the implementer from
  self-certifying `VERIFIED`; the semantic half — confirming the
  reviewer was genuinely independent — remains human/reviewer
  judgement, per `docs/agent-isolation.md`).
- **`resolved_into` set without a reciprocal `resolves`** on the target
  → CI failure (asymmetric supersession is exactly the kind of
  "quietly edit history" this project's conventions exist to prevent).
- **`get(id)` for a nonexistent ID** → `NotFound`, not an exception
  that crashes a caller; **`get(id)` for a superseded ID** → returns
  the historical record plus the `resolved_into` pointer, never a bare
  redirect.

**Native-register translation tests (§3a–§3e), added in this revision:**

- **Missing `scope`** (any native register lacking the field, e.g.
  Ledgerkit's) → `derived.scope: null`, never fabricated; `get()`
  succeeds, it does not error.
- **Missing reviewer metadata**: `native.status: verified` but
  `verified_by`/`verified_date` absent or empty → `derived.status:
  CONTESTED`, not `VERIFIED` and not `UNCERTAIN` — the native record's
  own claim conflicts with what it can support.
- **Conflicting evidence**: an entry's own `evidence[]` contains both
  a passing and a failing `executable` result at the same `pinned_at`
  → `derived.status: CONTESTED`, regardless of the native `status`
  field's value — an unresolved conflict in the evidence itself always
  takes precedence over whatever status was claimed.
- **Unsupported/unrecognised native value**: a `relationship` or
  `status` value outside the known enums (a future Ledgerkit schema
  revision adds one this adapter doesn't know about) → `derived.status:
  UNCERTAIN` with an explicit `translation_gap: true` marker and the
  raw native value preserved — never silently dropped, never crashes.
- **`superset`/`subset` relationship always carries a `mapping_scope`**
  — tested as a positive assertion (the field is present and non-empty)
  whenever `relationship` is one of those two values, and *absent*
  whenever it's `equivalent`/`incomparable`.

**Git-change (`impacted()`) regression fixtures, added in this revision:**

- **Source modification**: a claim's `source.ref` under the changed
  `path`, `change_type: modified` → flagged, reason cites the specific
  reference.
- **Source deletion**: a claim referencing a `path` with
  `change_type: deleted` → flagged, reason `"source deleted"`, no
  status implied.
- **Source rename**: a claim referencing `old_path`, change record has
  `change_type: renamed`, `old_path` set, `path` the new location →
  flagged against the old reference, confirming the rename case is
  findable, not silently missed because the literal path changed.
- **Evidence file deletion**: a claim's `evidence[].ref` (not its
  `source.ref`) under a deleted path → flagged, same treatment as
  source deletion — evidence references are checked exactly like
  source references, not a weaker case.
- **Changed source with a relevant claim** → flagged with
  `possible_impact: true` and the specific reference.
- **Changed source with no relevant claim** → claim absent from the
  result entirely (not returned with `possible_impact: false`).
- **Unrelated source change** (a path no claim references at all) →
  no entries in the result; this is the false-positive check Stage
  2.4's drift demonstration (`planning/phase-02-stage-2.1-plan.md` §6.2)
  exercises for real.
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
