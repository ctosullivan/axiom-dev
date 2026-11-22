# Stage 2.1 implementation-ready plan — Ledgerkit balance-assignment elision

**Status: Planned. Not authorisation to implement.** Per `AGENTS.md` §2
and §11, and `docs/development-lifecycle.md`'s SPECIFY exit criterion,
this plan requires independent review before BUILD starts — done; see
`planning/phase-02-planning-review.md` for the full review and the two
BLOCKING findings it raised against this planning package, both fixed
in the same batch. §11's "beginning a new stage beyond the one
currently authorised" boundary applies to starting BUILD, not to
writing or reviewing this plan; BUILD itself still awaits human
approval.

This is the Stage 2.1 deliverable required by `planning/ROADMAP.md`
and `planning/phase-02-template.md` §2.1: a bounded Ledgerkit problem,
frozen contract, independent oracle, fixtures and a measurement plan,
concrete enough for another agent to execute once approved.

## 0. Baseline inspected (UNDERSTAND)

Recorded here because the Stage 2.1 exit criterion requires citing the
actual files read, not "the codebase":

- **Ledgerkit**: `~/projects/ledgerkit`, pure Python, zero runtime
  dependencies, declared version `1.0.0.dev1`. HEAD at inspection time:
  `a7740fd04fe1814d2a557bfcb67a9a775a4a22f9` on branch `main`, clean
  tree. `.venv/bin/python -m pytest -q` → **935 passed**, no failures.
  Code read directly: `ledgerkit/parser.py` lines 665–753 (posting
  parsing, assertion-marker detection, elision handling).
- **hledger**: `~/projects/hledger`, HEAD `33fa849e7ae841968bd21c427094c4fb4a4ec38d`.
  Installed binary `~/.local/bin/hledger` reports
  `hledger 1.52.4-g33fa849e7-20260910, linux-aarch64` — the
  git-describe suffix (`g33fa849e7`) matches this exact checked-out
  commit, confirmed by direct comparison of the two SHAs. This is
  independent live-oracle access to the literal reference commit
  present in this environment, not merely "some hledger version."
- **Ledgerkit's own pre-existing knowledge artifacts**, read directly:
  `knowledge/EDGE_CASES.md` (EC-022, lines 193–218), `ROADMAP.md`
  ("Plan 29 bug-fix backlog" row), `knowledge/DECISIONS.md` (the
  2026-05-03 entry and its 2026-11-14 addendum), and
  `dev-docs/compat-register/schema.md` (full YAML schema for
  Ledgerkit's existing compatibility register) and one live entry,
  `dev-docs/compat-register/LK-COMPAT-QUERY-REGEX-EMPTYALT-001.yaml`,
  as a worked example of that register's conventions in actual use.

## 1. Selected task

**Fix Ledgerkit's balance-assignment elision parsing** (`account =
AMOUNT`, no separately-written posting amount — hledger's assertion-as-amount
syntax) for all commodity-placement and decimal-mark combinations.
This is Ledgerkit's own documented, unfixed **EC-022**.

### Why this task, not an alternative

Three candidates were inspected (full detail: the dispatched research
agent's report, preserved below in §8). Rejected alternatives:

- **EC-021** (a bare directive mid-transaction-block silently drops the
  rest of the transaction): real, cleanly reproducible, but narrower —
  one structural case, not a semantically rich area with related
  claims to reuse.
- **`LK-MISMATCH-QUERY-REGEX-EMPTYALT-001`** (empty-alternation regex
  validation gap): already fully investigated to a high standard by
  Ledgerkit's own process (full accept/reject matrix, both sides
  independently verified, root-caused). Picking it up now would mostly
  be "write the fix," with little fresh evidence-gathering — a weaker
  demonstration of Axiom's evidence-first methodology than a case where
  the oracle transcripts still needed to be produced.

EC-022 was selected because it independently satisfies every criterion
in `planning/phase-02-template.md` §2.1 and the authorising prompt's
§5:

- **Real usefulness:** tracked in Ledgerkit's own `ROADMAP.md` backlog
  and cross-referenced from a `DECISIONS.md` entry that Ledgerkit's own
  2026-11-14 addendum admits was wrong — this is a known, named,
  currently-unscheduled gap in a real project, not a manufactured one.
- **Genuine semantic ambiguity:** the specific regex defect is
  unambiguous, but correctly resolving an elided amount against sibling
  postings' net, across commodities, decimal-mark modes and assertion
  strictness markers (`=`, `==`, `=*`, `==*`), is a real design surface
  (`resolve_elision()`, used from `reports.py:418,478,648`).
- **Independent, runnable oracle:** hledger at the exact pinned commit,
  demonstrated live below, not merely documentation.
- **Reproducible positive and negative fixtures:** demonstrated below;
  two *distinct* Ledgerkit failure modes (hard crash vs silent data
  corruption), not one.
- **Knowledge-reuse surface:** the same parser neighbourhood
  (`_ASSERTION_MARKER_RE`, `_parse_posting`, `_parse_amount`) is
  adjacent to two other open items in the same register/EDGE_CASES
  family (EC-018 malformed `commodity` directive, EC-020 alias
  backreference crash), so a correct claim about assertion-marker
  parsing is reusable, not a one-off fact.
- **Drift-demonstration surface:** `hledger`'s own git history has
  *active, recent* commits in exactly this semantic area (balance
  assignments feeding lot-matching), confirmed by
  `git -C ~/projects/hledger log --oneline --grep="balance assignment\|balance assert\|elide"`,
  which surfaced (among others) `de9a91e2a`, `34ba02b5e`, `7685d9a38`.
  **Correction, found by independent review
  (`planning/phase-02-planning-review.md` §3, Material-Nonblocking 3):**
  these three commits all *predate* this planning work, so they are
  evidence this area churns, not a guarantee a new relevant hledger
  commit lands during Phase 2's own timeline. `planning/phase-02-template.md`
  §2.4's actual requirement is "a second meaningful change" — this can
  equally be a second **Ledgerkit-side** change (e.g. EC-021, the
  rejected-but-viable alternative in §1 above) if no new relevant
  hledger commit appears in time. The hledger-churn evidence supports
  plausibility of the richer demonstration; it is not relied on as the
  only path to satisfying Stage 2.4.
- **Solo-developer scope:** one function's control flow
  (`_parse_posting`), a bounded fixture matrix (commodity placement ×
  decimal-mark mode), no new architecture.

## 2. Root cause (independently re-derived, not merely relayed)

`ledgerkit/parser.py:673`:

```python
_ASSERTION_MARKER_RE = re.compile(r"\s+(==\*|==|=\*|=)\s+")
```

This regex requires **whitespace before** the marker. After the
account/amount split on `\s{2,}` (line 697) and `.strip()` (line 713),
a balance-assignment posting with *no separately-written amount* (e.g.
`assets:bank  = 100,00 EUR`) leaves `amount_raw` beginning with the
marker itself (`"= 100,00 EUR"`) — there is no leading whitespace for
`\s+` to match, so `_ASSERTION_MARKER_RE` never fires for this case.
The code comment at lines 668–672 *correctly states* that this is why
the regex won't match a leading bare marker, but no other code path
exists to handle that case as "elided amount, assertion-only" — it
falls through to `_parse_amount(amount_raw, ...)` (line 744), which
parses the whole string, marker included, as a plain amount.

**Independently reproduced, both forms, both wrong — differently than
EC-022's own writeup implies:**

Prefix-commodity form (journal, exact bytes):
```
2024-01-01 Opening balance
    assets:bank  = $100.00
    equity:opening  $-100.00
```
- `hledger -f <file> balance` → exit 0:
  ```
            $100.00  assets:bank
           $-100.00  equity:opening
  --------------------
                   0
  ```
- Ledgerkit `parse_string(...)` → raises
  `ledgerkit.parser.ParseError: invalid amount: '= $100.00' (line 2)`.
  EC-022's own writeup calls this form "already correct" because it
  fails loudly rather than corrupting data — true, but it means this
  form isn't *handled*, it's *rejected outright*; balance-assignment
  elision is unimplemented for both commodity placements, not working
  for one of them.

Suffix-commodity, comma-decimal form:
```
decimal-mark ,
2024-01-01 Opening balance
    assets:bank  = 100,00 EUR
    equity:opening  -100,00 EUR
```
- `hledger -f <file> balance` → exit 0:
  ```
          100,00 EUR  assets:bank
         -100,00 EUR  equity:opening
  --------------------
                   0
  ```
- Ledgerkit `parse_string(...)` → succeeds with **no error** and
  **wrong data**: `Posting(account='assets:bank',
  amount=Amount(quantity=Decimal('100.00'), commodity='='),
  balance_assertion=None)` — the `=` is absorbed as the commodity
  symbol; the intended `EUR` commodity and the assertion are both
  silently gone.
- The full CLI (`ledgerkit -f <file> balance|print|check`) then exits 1
  on all three with a confusing downstream error blaming a bogus `=`
  commodity (`not balanced — net +100.00 = / net -100.00 EUR`), for a
  file hledger accepts and balances cleanly.

**The fix shape** (BUILD-phase work, not specified further here, per
this assignment's "do not implement" boundary): `_parse_posting` needs
a second, anchored check — when `amount_raw` *starts with* one of
`==*`, `==`, `=*`, `=` with nothing before it, the remainder is the
assertion amount and the posting amount is `None`, mirroring the
existing `_ASSERTION_MARKER_RE` branch (lines 722–732) rather than
falling through to `_parse_amount` on the whole token. This must hold
for both commodity placements and both decimal-mark modes.

## 3. Independent oracle (frozen, not re-derived from Ledgerkit's fix)

The oracle is **hledger 1.52.4, commit `33fa849e7` (confirmed
installed and runnable, see §0)**, run against hand-written fixture
journals, with its output captured *before* any Ledgerkit code change.
Per the authorising prompt's explicit instruction, the expected result
is hledger's actual observed behaviour, independently assessed as the
intended requirement — not inferred from reading Ledgerkit's
newly-written fix.

**Independent assessment of whether matching hledger is the right
requirement:** yes, for this specific case — Ledgerkit's own stated
goal (`README.md`: "a documented hledger-compatible foundation") and
its own `DECISIONS.md`/`EDGE_CASES.md` already treat hledger's
assertion-as-amount behaviour as the target; this plan is not
introducing a new compatibility target, only supplying the oracle
evidence that target was missing.

### Required fixture matrix

| # | Commodity placement | Decimal mark | Assertion strictness | hledger behaviour (to capture) |
|---|---|---|---|---|
| 1 | Prefix (`$100.00`) | period | plain `=` | accepts, balances |
| 2 | Suffix (`100.00 USD`) | period | plain `=` | accepts, balances |
| 3 | Suffix (`100,00 EUR`) | comma | plain `=` | accepts, balances |
| 4 | Prefix | period | `==` (sole-commodity) | accepts, balances |
| 5 | Suffix | comma | `=*`/`==*` (inclusive) | accepts, balances |
| 6 | Suffix | comma | plain `=`, multi-posting net | assertion resolves against net of *other* postings, not just one sibling |
| 7 (negative) | Suffix | comma | assertion amount that is wrong (doesn't balance) | hledger rejects — must confirm Ledgerkit's fix also rejects, not silently accepts |
| 8 (negative) | — | — | malformed marker (e.g. `===`) | hledger rejects — confirms the fix doesn't over-match |

Row 3/comma case is the exact transcript already captured in §2 above
and is the primary, already-reproduced example; rows 1–2, 4–8 are
required before the fix can be called complete, but their fixtures are
BUILD-phase work (writing the `.journal` files and capturing hledger's
output for each), not pre-supplied here, since generating them is part
of demonstrating the oracle-capture step of the lifecycle, not a
planning deliverable. This plan specifies the matrix; a future BUILD
step executes it.

### Negative/boundary cases required

- Row 7/8 above (wrong-assertion and malformed-marker rejection).
- A posting with **both** the old crash (prefix form, unbalanced
  assertion) and the old corruption (suffix form) must each become a
  **named, reproducible regression test**, not just "fixed and no
  longer visible" — the fix must demonstrably turn a crash/corruption
  into either correct acceptance or a clean, documented rejection
  matching hledger's own behaviour for that exact input.

## 4. Acceptance criteria

1. For every row in the fixture matrix (§3), Ledgerkit's parser output
   matches hledger's observed behaviour on the same input (same
   resolved amount/commodity, same accept/reject verdict) — or, if a
   deliberate, documented divergence is chosen instead, it is recorded
   as `kind: intentional_divergence` in the compat-register (§5) with
   an explicit `reason`, not silently accepted as "close enough."
2. Both previously-reproduced failure modes (crash on prefix form;
   silent corruption on suffix form) no longer occur for valid input,
   and are preserved as regression tests.
3. No regression in Ledgerkit's existing 935-test suite.
4. The fix is independently verified by a dispatch that did not write
   it, per `AGENTS.md` §6 and Ledgerkit's own existing
   `compat-differential-tester` convention (§5) — not self-reported by
   the implementing session.
5. A `dev-docs/compat-register/` entry exists for this behaviour,
   written in Ledgerkit's own existing schema, reaching at least
   `status: self-verified` before BUILD is considered complete and
   `status: verified` only via a separately-dispatched reviewer, per
   that schema's own rule (never set by the implementer).

## 5. Knowledge recording decision — defer to Ledgerkit's existing register, don't duplicate it

**This is the single most important design decision this plan makes,**
directly answering `planning/phase-02-template.md`'s "do not duplicate
the same claim across multiple authoritative locations" and this
assignment's Principle A ("adopt existing tools rather than replace
them"):

Ledgerkit **already has** a mature, independently-governed
compatibility-claim register at `dev-docs/compat-register/`
(schema at `dev-docs/compat-register/schema.md`, read in full — see
§0), with: stable IDs (`LK-<KIND>-<AREA>-<NNN>`, never reused), a
`kind` taxonomy (`compatible`/`extension`/`intentional_divergence`/
`unsupported`/`unexplained_mismatch`) analogous to the "equivalent /
partial / divergent / unknown" states this assignment's §7 asks for, a
pinned-upstream-version field, an `evidence` list with
`kind`/`ref`/`pinned_at`, a verification-tier `status` field
(`proposed`/`self-verified`/`verified`/`final`) that is structurally
analogous to (though not identical to) Axiom's own
INTENDED/OBSERVED/VERIFIED/UNCERTAIN/CONTESTED taxonomy
(`docs/knowledge-placement.md`), and a non-destructive supersession
mechanism (`resolved_into`/`resolves`) matching ADR 0008 Decision 4's
"renames do not mint new IDs" requirement almost exactly. It even has
its own independent-review discipline: `status: verified` "must NEVER
be written into a register YAML directly [by the implementer] — only a
dispatched `compat-differential-tester` agent's own output sets it" —
the same circularity-prevention rule as `AGENTS.md` §6 and
`decisions/0004` Amendment B, arrived at independently.

**Decision:** Axiom's Phase 2 knowledge vertical slice for this task
does **not** create a parallel `knowledge/claims/` record inside
Ledgerkit duplicating what the compat-register already does. Instead:

- The authoritative claim for "does Ledgerkit's balance-assignment
  elision match hledger" **is** the compat-register entry this fix
  produces (new ID, `kind: compatible` once fixed and matching, written
  in Ledgerkit's own schema, in Ledgerkit's own directory, under
  Ledgerkit's own review process).
- Axiom's comparative wiki slice (Stage 2.2) **links to that entry by
  its stable `LK-...` ID** rather than re-stating its content.
- Axiom's local knowledge API (`planning/phase-02-knowledge-api-design.md`)
  reads the compat-register's YAML files directly — **the
  compat-register entry is the Claim**, in the API's own vocabulary;
  its `upstream:` block is that Claim's Source, and its `evidence:`
  list is that Claim's Evidence. (An earlier draft of this section
  called the register entry a `Source`, which was a misuse of the
  API design's own terms, found by independent review
  (`planning/phase-02-planning-review.md` §3, BLOCKING 2) and corrected
  here.) Axiom does not require Ledgerkit to adopt an Axiom-specific
  record format — the knowledge API's §3a adapter contract
  (`planning/phase-02-knowledge-api-design.md`) maps the native fields
  into a common view additively, without altering or duplicating the
  original record. This is the clean demonstration this assignment's
  §3 and §C ask for of "use existing project governance without
  duplicating or replacing it."
- Axiom's own wiki prose (narrower, hledger-comparison-specific
  commentary — see §2.2 of `planning/phase-02-template.md`) is the one
  place that is Axiom's own to maintain, and it is explicitly scoped to
  commentary/navigation, not a second copy of the compatibility
  verdict.

This decision is plan-level, not ADR-level: ADR 0008 already decided
Phase 2 needs stable IDs, a claim/source/evidence model and a local
API; discovering that one real consumer already has a compatible,
independently-arrived-at implementation of that same shape is evidence
*for* ADR 0008's design, not a reversal of it.

## 6. Smallest skill/logging integration needed to observe this work

Per this assignment's §1 instruction to "define the smallest
skill/logging integration needed to observe subsequent work" at Stage
2.1: **none is built in this stage.** Stage 2.2 introduces the actual
skill and logger (see `planning/phase-02-adoption-design.md` and
`planning/phase-02-measurement-design.md`); Stage 2.1 is scoping and
oracle-capture work that does not yet need either. Building logging
before there is anything to log would violate this project's own
complexity budget (§14 of the authorising prompt).

## 7. Approval checkpoints

1. **This plan** (problem, root cause, oracle, fixture matrix,
   acceptance criteria, knowledge-recording decision) is independently
   reviewed (`planning/phase-02-planning-review.md`) and human-approved
   before BUILD starts — `AGENTS.md` §2, §11.
2. Before the fix lands: the full fixture matrix (§3) exists as actual
   `.journal` files with captured hledger output, reviewed for fidelity
   to the matrix (not reduced without recording why).
3. After the fix: independent verification per §4 item 4, using
   Ledgerkit's own `compat-differential-tester` dispatch convention
   where practical, or Axiom's own fresh-context dispatch
   (`docs/agent-isolation.md` level 2) named honestly if that
   convention isn't reused.
4. Before Stage 2.1 is marked complete in `planning/ROADMAP.md`: a
   human confirms, per `docs/development-lifecycle.md`'s phase
   acceptance procedure — an agent prepares the status change, a human
   confirms it (`AGENTS.md` §11).

## 8. Research provenance

This plan's task selection is based on a dispatched, fresh-context
research agent's inspection of `~/projects/ledgerkit` and
`~/projects/hledger` (33 tool uses, 87,745 tokens), whose key claims
(parser line numbers, the prefix-form crash, the suffix-form
corruption, hledger's HEAD-matching binary) were **independently
re-verified by the orchestrating session directly** before being relied
upon here (§0, §2) — not merely relayed. The research agent's full
report, including the two rejected alternatives' evidence, is preserved
in `planning/phase-02-planning-review.md`'s provenance section.
