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

**Found missing by this package's own independent review
(`planning/phase-02-planning-review.md` §3, BLOCKING 2) and specified
here rather than left implicit.** When `get`/`find`/`related`/
`impacted` read a claim from an existing, non-Axiom register (the
Stage 2.1 case: Ledgerkit's `dev-docs/compat-register/`, per §2
above), the native record is **not** silently assumed to already match
§3's generic schema field-for-field — it does not. The API returns a
normalised common view **additively**, alongside the untouched native
fields, never discarding or overwriting the source record:

```yaml
id: <native ID, unchanged — e.g. LK-COMPAT-PARSER-BALANCEASSIGN-001>
status: <mapped — see table below>
mapping_result: <mapped — see table below>
scope: null          # see "known gap" below — never fabricated
evidence: <native evidence list, field names unchanged>
related: <native resolved_into/resolves, unchanged>
native:
  <the complete, unmodified original record, exactly as read>
```

**`relationship` → `mapping_result` mapping** (Ledgerkit's
`ledgerkit.relationship` has no field named `mapping_result`, and the
two vocabularies are not synonyms):

| Ledgerkit `relationship` | Axiom `mapping_result` | Why |
|---|---|---|
| `equivalent` | `equivalent` | same behaviour, direct match |
| `superset` | `equivalent` | for the hledger-defined behaviour itself, Ledgerkit matches it; the *additional* extension behaviour is out of scope for a mapping-result comparison and is described by `kind: extension` instead, not by this field |
| `subset` | `partial` | intentionally covers less than hledger — a partial mapping, not a full equivalence or a genuine divergence |
| `incomparable` | `divergent` | genuinely different, not reducible to subset/superset |
| *(no `unexplained_mismatch` relationship value — that's a `kind`, not a `relationship`)* | `unknown` | a `kind: unexplained_mismatch` entry has not yet been classified; `mapping_result: unknown` until it resolves into a new entry |

**`status` → Axiom status mapping** (word-similarity is actively
misleading here — checked explicitly, not assumed):

| Ledgerkit `status` | Axiom `status` | Why |
|---|---|---|
| `proposed` | `OBSERVED` | a reading exists; not yet run against the real binary, so no independent (or even self-run) evidence yet — closer to "observed via inspection" than confirmed |
| `self-verified` | `OBSERVED`, **not** `VERIFIED` | a real comparison WAS run with real output, but by the same identity that implemented the fix — Ledgerkit's own schema explicitly reserves `verified` for a separately-dispatched reviewer, the same circularity rule as `AGENTS.md` §6/`decisions/0004` Amendment B. Mapping this to `VERIFIED` would launder a self-check into independent status; it must not. |
| `verified` | `VERIFIED` | set only by a separately-dispatched `compat-differential-tester`, matching Axiom's own definition of VERIFIED exactly |
| `final` | `VERIFIED` | additionally reconciled/published; evidence status unchanged from `verified` |

**Known gap, disclosed rather than papered over:** the compat-register
schema has **no field carrying scope/input-boundary information** —
confirmed directly against `dev-docs/compat-register/schema.md`, which
has no `scope` key. `get()` on a Ledgerkit-backed claim therefore
returns `scope: null`, not a fabricated value. A human wanting the
scope must read that entry's `area` and `reason` fields directly — the
API does not claim to supply something the source record doesn't have.
This is recorded as a real, acknowledged limitation of deferring to an
existing register that wasn't designed with Axiom's exact field set in
mind, not resolved by inventing data.

**Terminology correction** (the same independent review flagged an
internal inconsistency): a compat-register entry **is a Claim**, in
this API's own three-concept vocabulary — not a `Source`. Its
`upstream:` block (project + pinned version) is that Claim's `Source`;
its `evidence:` list is that Claim's `Evidence` list. The phrase "one
of its `Source` kinds," used in an earlier draft of
`planning/phase-02-stage-2.1-plan.md` §5, was a misuse of this design's
own terms and has been corrected there.

## 4. Operations

Read-only in Phase 2 (ADR 0008 Decision 3: "not postponed until MCP,"
but also not a write API — Git/PR review is the write path,
`AGENTS.md` §9). Implemented as a small Python library with a thin CLI
wrapper (`axiom-knowledge <op> ...`), reading Markdown/YAML directly,
with an optional in-memory index rebuilt per invocation — no persistent
server, per architectural principle C.

### `get(id) -> Claim | NotFound`

Returns the claim/artifact record and its evidence list, scope, status
and relationships. **Minimum data returned:** `id`, `status`, `scope`,
`source`, `evidence` (full list), `related` (IDs only, not expanded —
expansion is `related()`'s job). If `resolved_into` is set, `get`
returns the record **and** a pointer to the superseding ID — it never
silently redirects, since the authorising prompt's §6 requires
identity/revision/status to stay distinct and visible.

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

Input: a list of changed source paths/revisions (e.g. from `git diff
--name-only` against a claim's pinned `source.ref`/`pinned_at`).
Output: every claim whose `source` or `evidence[].ref` falls under a
changed path, or whose `pinned_at` no longer matches the current
revision of that path — each flagged `possible_impact: true` with the
specific changed reference that triggered it. **This never sets or
implies a status change** — per ADR 0008 Decision 4/§5 of the
authorising prompt, change detection establishes *possible* impact,
never proven invalidity; `impacted()`'s output is a worklist for a
human/independent reviewer, not a verdict. An unaffected claim is not
returned at all (not returned-with-`possible_impact: false`) — keeping
the "affected" set small and actionable is more useful than echoing
every claim back with a boolean.

**Errors:** `InvalidChangeSpec` if a given path doesn't exist in the
repository at all (distinct from "exists but affects nothing," which is
simply absent from the result).

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
- **`impacted([])`** (empty change list) → `[]`, not an error — the
  degenerate case must be well-defined, not merely untested.
- **`impacted(["path/that/does/not/exist"])`** → `InvalidChangeSpec`,
  distinguishing "nothing is affected" from "the input itself was
  wrong."

## 7. What this explicitly is not

No graph database (plain files + an ephemeral in-memory index on each
CLI invocation). No persistent service (every operation is a one-shot
process). No embeddings/vector search (§4). No autonomous knowledge
generation (every claim is written and reviewed by a human/agent
through a normal commit, never auto-synthesised by the API). No MCP
transport (Phase 3's adapter wraps this same library; this library
works fully without it, per ADR 0008 Decision 3 and architectural
principle G).
