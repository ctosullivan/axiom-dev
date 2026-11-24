# Stage 2.1 implementation-ready plan — Ledgerkit balance-assignment elision

**Status: Stage 2.1 Completed** (owner decision 2026-11-25, following
the merge of [PR #4](https://github.com/ctosullivan/axiom-dev/pull/4) —
see [the archive entry](archive/phase-02-stage-2.1/README.md) for the
closeout record). **§6 below ("Handoff to Stage 2.4") remains active
and unarchived** — Stage 2.4 reads this same file for its own
implementation contract; nothing below this point is rewritten to
read as historical only. The rest of this document is preserved
exactly as reviewed and accepted, below.

**Status at original authorship: Planned. Not authorisation to
implement.** This plan
establishes the development **contract** for fixing Ledgerkit's
EC-022 — it does not fix it. Per `AGENTS.md` §2/§11 and
`docs/development-lifecycle.md`'s SPECIFY exit criterion, this plan
requires independent review before BUILD starts; see
`planning/phase-02-planning-review.md` for the review record. BUILD
(Stage 2.4, §6 below) awaits separate human approval.

**Corrected sequencing.** An earlier draft of this plan included
fix-implementation and regression-testing requirements that belonged
to Stage 2.4, creating an overlap between the two stages. This plan
ends Stage 2.1 at the reviewed contract and oracle; §6 below is the
explicit handoff carrying everything implementation-shaped into Stage
2.4. (Found and fixed as a dangling-section-reference defect in this
revision: this note previously cited "§7," which is actually the
knowledge-recording decision, not the handoff.)

## 1. Baseline inspected (UNDERSTAND)

- **Ledgerkit**: `~/projects/ledgerkit`, pure Python, zero runtime
  dependencies, `1.0.0.dev1`. HEAD at inspection:
  `a7740fd04fe1814d2a557bfcb67a9a775a4a22f9`, clean tree, 935/935
  tests passing. Read directly: `ledgerkit/parser.py` lines 665–753
  (posting parsing) and 816–869 (`resolve_elision`).
- **hledger**: `~/projects/hledger`, HEAD
  `33fa849e7ae841968bd21c427094c4fb4a4ec38d`. Installed binary
  `~/.local/bin/hledger` reports `1.52.4-g33fa849e7-20260910` — the
  git-describe suffix matches this exact checked-out commit.
- **Ledgerkit's own knowledge artifacts**, read directly:
  `knowledge/EDGE_CASES.md` (EC-022, lines 193–218), `ROADMAP.md`
  ("Plan 29" backlog), `knowledge/DECISIONS.md` (2026-05-03 entry and
  2026-11-14 addendum), `dev-docs/compat-register/schema.md` (full),
  and one live entry as a worked example.

## 2. Selected development problem

**Ledgerkit's balance-assignment elision parsing** (`account =
AMOUNT`, no separately-written posting amount) — Ledgerkit's own
documented, unfixed **EC-022**. This plan establishes the contract a
later BUILD stage implements against; it does not implement it.

### Why this problem, not an alternative

Three candidates were inspected (research-agent dispatch, 33 tool
uses, 87,745 tokens — full notes in `planning/phase-02-planning-review.md`
§2.2). Rejected:

- **EC-021** (a bare directive mid-transaction-block silently drops
  the rest of the transaction): real, cleanly reproducible, but
  narrower — one structural case, no related-claim reuse surface.
- **`LK-MISMATCH-QUERY-REGEX-EMPTYALT-001`**: already fully
  investigated to a high standard by Ledgerkit's own process — picking
  it up now would be mostly "write the fix," less evidence-gathering
  to dogfood.

EC-022 satisfies every selection criterion: real, named, currently
unscheduled usefulness (Ledgerkit's own `ROADMAP.md`/`DECISIONS.md`);
genuine semantic depth (see §3 — deeper than either EC-022's own
writeup or the first draft of this plan assumed); an independent,
runnable oracle (hledger at the exact pinned commit); two distinct,
reproducible negative fixtures (crash vs silent corruption); a
knowledge-reuse surface (the same parser neighbourhood touches EC-018/
EC-020); solo-developer scope (one function's control flow, a bounded
fixture matrix, no new architecture).

## 3. Root cause and oracle scope (independently re-derived and extended, not merely relayed)

`ledgerkit/parser.py:673`:

```python
_ASSERTION_MARKER_RE = re.compile(r"\s+(==\*|==|=\*|=)\s+")
```

Requires **whitespace before** the marker. A balance-assignment
posting with no separately-written amount (e.g. `assets:bank  =
100,00 EUR`) leaves `amount_raw` beginning with the marker itself, so
the regex never fires; code falls through to `_parse_amount` on the
whole token instead of recognising "elided amount, assertion-only."

**Both failure modes reproduced** (full transcripts preserved in
`planning/phase-02-planning-review.md` §2.2, re-confirmed directly by
this session): prefix-commodity form (`= $100.00`) raises `ParseError`
in Ledgerkit where hledger balances cleanly; suffix-commodity/
comma-decimal form (`= 100,00 EUR`) silently corrupts data in
Ledgerkit (the `=` absorbed as the commodity symbol) where hledger
again balances cleanly.

### A genuinely new scope finding from direct oracle capture

Ledgerkit's existing `resolve_elision()` (`ledgerkit/parser.py:816–869`,
read in full) resolves an elided posting amount **only from the net of
its sibling postings within the same transaction** — it takes a single
`Transaction` and has no access to the account's prior history. hledger's
actual balance-assignment semantics are **not** the same algorithm.
Captured directly, not assumed:

```
2024-01-01 Opening balance
    assets:bank  $100.00
    equity:opening  $-100.00

2024-02-01 Deposit, balance assigned
    assets:bank  = $250.00
    equity:unknown
```
`hledger -f <file> balance` →
```
             $250.00  assets:bank
            $-100.00  equity:opening
            $-150.00  equity:unknown
--------------------
                   0
```
`equity:unknown` resolves to `$-150.00`, proving hledger computed
`assets:bank`'s assigned posting as `$250.00 − $100.00(prior balance)
= $150.00`, **not** `$250.00` outright. Every other fixture captured
below happens to have a zero prior balance, where "net of this
transaction's siblings" and "change needed against running account
balance" coincide — which is exactly why this distinction was not
visible in EC-022's own writeup or the first draft of this plan, and
was only found by actually running the oracle against a two-transaction
input. This is a real, larger boundary than EC-022 itself: true
balance-assignment requires the account's full running balance across
the journal, which `resolve_elision()` structurally cannot provide.

**Scope decision (Stage 2.1's own call, not deferred):** EC-022's fix
is scoped to the **single-transaction case** — recognising the leading
bare marker and resolving it via the existing `resolve_elision()`
sibling-net algorithm, matching Ledgerkit's own already-implemented
approach for ordinary elided amounts. The **cross-transaction running-
balance case is explicitly out of scope for this fix** and is recorded
as a distinct, named limitation (§6, fixture row 9) — not silently
left for a fix to appear to handle and then diverge from hledger
without anyone having decided that was acceptable.

## 4. Independent oracle — frozen and now fully captured

Oracle: **hledger 1.52.4, commit `33fa849e7`**, run against
hand-written fixture journals (no Ledgerkit or hledger files
modified), output captured *before* any Ledgerkit code change, now
preserved durably at `evidence/phase-2-stage-2.1-oracle/` (fixture
files, full transcripts, exact version/commit identification,
commands, and a reproduction recipe — see that directory's
`README.md`). Matching hledger is independently assessed as the right
requirement here: Ledgerkit's own stated goal and its own
`DECISIONS.md`/`EDGE_CASES.md` already treat hledger's assertion-as-
amount behaviour as the target.

### Fixture matrix — all rows captured against the real oracle

| # | Case | hledger result (captured) | In scope for EC-022's fix? |
|---|---|---|---|
| 1 | Prefix `$100.00`, period, plain `=` | exit 0, balances at `$100.00`/`$-100.00` | Yes |
| 2 | Suffix `100.00 USD`, period, plain `=` | exit 0, balances at `100.00 USD`/`-100.00 USD` | Yes |
| 3 | Suffix `100,00 EUR`, comma, plain `=` | exit 0, balances (original reproduction, §3) | Yes |
| 4 | Prefix, period, `==` (sole-commodity) | exit 0, balances identically to row 1 | Yes |
| 5 | Suffix, comma, `=*` (inclusive) | exit 0, balances identically to row 3 | Yes |
| 6 | Suffix, comma, plain `=`, 3-posting transaction (two explicit postings + one elided) | exit 0; elided posting resolves to `100,00 EUR`, matching sibling-net exactly | Yes — this is the case `resolve_elision()` already handles for non-assignment elisions |
| 7 (negative) | Suffix, comma, assertion amount that doesn't balance (`999,00 EUR` against a lone `-100,00 EUR` offset) | **exit 1**: `"This transaction is unbalanced... should be 0 but is: 899,00 EUR"` | Yes — the fix must also reject this, not silently accept |
| 8 (negative) | Malformed marker `===` | **exit 1**: parse error, `"unexpected '='... expecting '*' or amount"` | Yes — the fix must not over-match a triple marker |
| 9 (boundary, **out of EC-022's scope**) | Suffix/prefix, **two transactions**, account has a nonzero prior balance before the balance-assignment posting | exit 0; assigned amount is `(asserted − prior running balance)`, **not** the asserted figure itself — see §3 | **No** — requires running-balance tracking `resolve_elision()` does not have; tracked as a named, accepted limitation, not silently diverged from |

All nine rows were run against the live oracle, twice now in two
separate sessions, with matching results. **Fixture files and full
transcripts are version-controlled** at
`evidence/phase-2-stage-2.1-oracle/` (not left in an agent session's
scratch directory, which does not survive the session — corrected in
this revision per the authorising prompt's explicit "reproducible
oracle evidence must survive the agent session"), reproducible from
the exact journal contents there and in this table — not re-derived
from Ledgerkit's own, not-yet-written fix.
Rows 1–8 are the **required pass set** for EC-022's fix; row 9 is a
**required disposition**, not a required pass — Stage 2.4 must either
extend the fix to cover it (expanding scope, requiring its own review)
or record it with an explicit, reasoned `kind: unsupported` or
`intentional_divergence` compat-register entry. Leaving it
undocumented is not an acceptable outcome under either choice.

## 5. Stage 2.1's own acceptance criteria (this plan's deliverable, not the fix's)

Stage 2.1 is accepted as complete when:

1. The development problem (§2), root cause (§3) and oracle scope
   finding (§3, row 9) are independently reviewed and no BLOCKING
   finding remains open (`planning/phase-02-planning-review.md`).
2. The fixture matrix (§4) is fully specified **and captured** against
   the real pinned oracle — done, this revision; no row is deferred to
   BUILD for its oracle-side transcript.
3. Acceptance criteria for the eventual fix (§6 below) are frozen
   before BUILD starts, so the implementing session cannot redefine
   what "correct" means after seeing its own code's behaviour.
4. The knowledge-recording decision (§7) and the Stage 2.4 handoff
   (§6) are explicit enough that a different agent could execute
   Stage 2.4 from this document alone, without re-deriving the above.

Stage 2.1 does **not** require: EC-022 actually fixed; any Ledgerkit
regression test added or run against a changed implementation;
independent verification of a fix (there is no fix yet); a
compat-register entry written (nothing to record a verdict about
yet). These are Stage 2.4's acceptance criteria, listed in §6.

## 6. Handoff to Stage 2.4 — implementation, verification, reconciliation

Stage 2.4 owns everything below; none of it is done by this plan.

### 6.1 Build acceptance criteria (frozen now, not revisable after the fact)

1. Ledgerkit's parser output matches the fixture matrix (§4) for every
   one of rows 1–8 exactly (same resolved amount/commodity, same
   accept/reject verdict) — or a deliberate divergence is recorded as
   `kind: intentional_divergence` with an explicit `reason`, never
   silently accepted as "close enough."
2. Row 9 (§4) is explicitly dispositioned, one of the two ways named
   there — not silently left matching or diverging without a record.
3. Both original failure modes (crash on prefix form; silent
   corruption on suffix form) no longer occur for valid input and are
   captured as named regression tests.
4. No regression in Ledgerkit's existing 935-test suite.
5. The fix is independently verified by a dispatch that did not write
   it (`AGENTS.md` §6), using Ledgerkit's own `compat-differential-
   tester` convention where practical, or Axiom's fresh-context
   dispatch (`docs/agent-isolation.md` level 2) named honestly
   otherwise.
6. A `dev-docs/compat-register/` entry exists, in Ledgerkit's own
   schema, reaching `status: self-verified` at minimum before BUILD is
   considered complete, and `status: verified` only via the
   separately-dispatched reviewer in item 5 — never set by the
   implementer, per that schema's own rule.

### 6.2 Full-lifecycle demonstration — three controlled conditions, not one

Stage 2.4 must demonstrate drift detection with **three** conditions,
not two — a relevant change, an unrelated change in a different
module, and a same-file-but-semantically-unrelated change — because
two conditions alone cannot separate "the mechanism correctly found a
real dependency" from "the mechanism's own file-level granularity
(`planning/phase-02-knowledge-api-design.md` §3f) just happened to
match." The original plan's reliance on an unpredictable future
hledger commit is replaced with conditions this project controls
directly.

- **Relevant-change condition — EC-021, with its actual dependency
  checked, not assumed from file co-location.** EC-021 (a bare
  directive mid-transaction-block silently drops the rest of the
  transaction). **Corrected fix-location citation** (an earlier draft
  of this section misattributed the bug to `_flush_txn`, which an
  independent reviewer found, by reading it directly, only ever
  attaches tags/date-overrides to an *already-complete* postings list
  and never drops one — `planning/phase-02-planning-review.md` §8,
  BLOCKING 2): the actual mechanism is in the directive-handling
  branches around `ledgerkit/parser.py:1264–1343` (e.g. the `account`
  directive handler at line 1278), each of which sets
  `in_subdirective = True` and `continue`s **without first checking
  whether a transaction block is still open** — the subdirective-
  swallowing block immediately above them (lines 1249–1258) then
  silently consumes the still-open transaction's next posting line as
  if it were an indented subdirective, which is exactly how the rest
  of the transaction gets dropped. **The genuine dependency, now
  correctly located, is still not "same file"** — it is that both
  EC-021 and EC-022 depend on the same underlying assumption: that
  `txn.postings` is complete and correct by the time balance-assignment
  resolution (`resolve_elision()`) runs on it. EC-021's bug (silently
  dropping postings before the transaction is ever flushed) and
  EC-022's fix (resolving an elided posting's amount from its
  siblings) would interact badly in a transaction that triggers both
  — a dropped sibling posting would corrupt EC-022's own sibling-net
  resolution,
  not merely coexist in the same file. This is recorded as the actual
  reason EC-021 is relevant, replacing an earlier draft's weaker "close
  enough that a careful implementer should ask" framing. If a new,
  genuinely relevant hledger commit has landed in the meantime
  (checked via the same `git log --grep` search as §2's candidate
  research, not assumed), that is an equally valid, richer
  relevant-change condition — a bonus if available, not a dependency.
  **Required demonstration:** `impacted()` flags the EC-022 claim via
  its `implementation[]` reference; a reviewer who did not implement
  either change independently reassesses it against the frozen oracle;
  the claim is reconciled (not silently re-marked) with the new
  evidence.
- **Unrelated-change condition (different module):** a change to a
  genuinely unrelated Ledgerkit module such as `commodity_style.py`'s
  display formatting — not referenced by the EC-022 claim's
  `implementation[]`/`tests[]`/`evidence[].ref` at all.
  **Required demonstration:** `impacted()` does **not** flag the
  EC-022 claim.
- **Same-file, semantically unrelated condition (new in this
  revision) — tests the known limitation of file-level matching
  directly, rather than leaving it theoretical:** a change to
  `_apply_posting_date_override_tags` (`ledgerkit/parser.py:900+`,
  read directly: handles `date`/`date2` tag overrides, with zero
  interaction with `Posting.amount`/`balance_assertion` or
  `resolve_elision()`). This is in the **same file** as EC-022's own
  `implementation[]` reference, so `impacted()`'s deliberately
  conservative file-level matching (§3f) **will** flag the EC-022
  claim — a **known, predicted false positive**, not a surprise, and
  not a reason to abandon file-level matching, but direct, measured
  evidence of its actual cost in this one real case rather than an
  assertion that it "probably" produces false positives sometimes.
  **Required demonstration:** `impacted()` flags the claim; the
  reviewer confirms (by reading the actual diff) that the change has
  no real bearing on EC-022's behaviour, and records this as a
  **confirmed false positive**, not a missed impact and not silently
  dropped from the report.
- **All three conditions' actual outcomes are recorded** using these
  exact categories, not a single pass/fail per condition: true
  positives (correctly flagged, genuinely relevant), false positives
  (flagged, confirmed not relevant on review — e.g. the third
  condition above), missed impacts (relevant but not flagged, if any
  occur), actual semantic changes found (does the change really alter
  behaviour, independently assessed against the frozen oracle), source
  changes with no semantic effect (changed code, unchanged behaviour),
  and review effort (time/steps needed for the reviewer to reach each
  determination) — per `planning/phase-02-measurement-design.md` §7.D's predeclared
  drift-effectiveness measure.

### 6.3 Approval checkpoints

1. This plan, independently reviewed and human-approved, before any
   of the above starts (`AGENTS.md` §2, §11).
2. Before the fix lands: nothing further to capture on the oracle side
   (done, §4) — BUILD begins directly against the frozen fixture
   matrix.
3. After the fix: independent verification per §6.1 item 5.
4. Before Stage 2.4 is marked complete in `planning/ROADMAP.md`: human
   confirmation per `docs/development-lifecycle.md`'s phase-acceptance
   procedure.

## 7. Knowledge recording decision — defer to Ledgerkit's existing register, don't duplicate it

Ledgerkit **already has** a mature, independently-governed
compatibility-claim register at `dev-docs/compat-register/` (schema
read in full, §1), with stable IDs (`LK-<KIND>-<AREA>-<NNN>`, never
reused), a `kind` taxonomy, a pinned-upstream-version field, an
`evidence` list, a verification-tier `status` field, and a
non-destructive supersession mechanism (`resolved_into`/`resolves`)
matching ADR 0008 Decision 4 almost exactly — independently arrived
at, not designed to match Axiom.

**Decision:** Axiom's knowledge vertical slice for this task does
**not** create a parallel `knowledge/claims/` record inside Ledgerkit.
The compat-register entry this fix eventually produces **is the
Claim**, in `planning/phase-02-knowledge-api-design.md`'s own
vocabulary — its `upstream:` block is that Claim's Source, its
`evidence:` list is that Claim's Evidence. Axiom's local knowledge API
reads it directly via the adapter contract specified in that document
(§3a), which maps native fields into a common view **additively**,
never altering or duplicating the original record. Axiom's comparative
wiki (Stage 2.2) links to it by stable ID rather than restating it.
This is plan-level, not ADR-level: ADR 0008 already decided Phase 2
needs stable IDs, a claim/source/evidence model and a local API;
finding a real consumer with an independently convergent
implementation of that shape is evidence for that decision, not a
reversal of it.

## 8. Smallest skill/logging integration needed to observe this work

None is built in Stage 2.1. Stage 2.2 introduces the skill and logger
(`planning/phase-02-adoption-design.md`,
`planning/phase-02-measurement-design.md`); building logging before
there is anything to log would itself violate this project's
complexity budget.

## 9. Research and review provenance

Task selection is based on a dispatched research agent's inspection of
`~/projects/ledgerkit` and `~/projects/hledger`, whose key claims were
independently re-verified directly by this session before being relied
upon (§1, §3) — not merely relayed. The oracle-capture work in §3/§4
(including the row-9 running-balance finding) was performed directly
by this session, against the real installed hledger binary, in this
revision. Full research notes, the first independent review (2
BLOCKING findings on the earlier draft, both fixed), and this
revision's own independent review are in
`planning/phase-02-planning-review.md`.
