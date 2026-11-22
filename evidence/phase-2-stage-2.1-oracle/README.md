# Stage 2.1 oracle evidence — EC-022 balance-assignment elision

**Durable, version-controlled replacement for fixtures and transcripts
that previously lived only in an agent session's scratch directory**
(`/tmp/.../scratchpad/lk-oracle/`) — found as a defect by the
authorising prompt's §5: "Reproducible oracle evidence must survive
the agent session." The files in this directory were **re-run fresh
against the live, pinned oracle in this same session** rather than
blindly copied from scratch — the scratch files still happened to be
present when this evidence was assembled (checked directly), so this
is a *confirmed reproduction*, not a blind recovery, and is recorded
as such rather than silently claiming either "recovered" or
"regenerated from nothing."

This directory is this project's own evidence (`evidence/`, per
`docs/knowledge-placement.md`'s placement table: "Verification
outcomes... cite what was checked and how"). It is **not** part of
Ledgerkit — nothing here was written into `~/projects/ledgerkit`.

## Exact executable/revision identification

- **hledger**: binary at `~/.local/bin/hledger`, version string
  `hledger 1.52.4-g33fa849e7-20260910, linux-aarch64` (re-confirmed by
  running `hledger --version` in this same session, immediately before
  capturing the transcripts below). The git-describe suffix
  (`g33fa849e7`) matches `~/projects/hledger`'s checked-out HEAD commit
  `33fa849e7ae841968bd21c427094c4fb4a4ec38d` exactly (`git -C
  ~/projects/hledger log -1 --format=%H`, re-confirmed this session).
- **Ledgerkit**: HEAD `a7740fd04fe1814d2a557bfcb67a9a775a4a22f9`
  (`git -C ~/projects/ledgerkit log -1 --format=%H`, re-confirmed this
  session), clean working tree, unchanged since Stage 2.1's original
  research pass.

## Fixture files (all nine rows of
`planning/phase-02-stage-2.1-plan.md` §4's matrix)

| File | Row | Case |
|---|---|---|
| `row-01-prefix-period-plain.journal` | 1 | Prefix `$`, period decimal, plain `=` |
| `row-02-suffix-period-plain.journal` | 2 | Suffix `USD`, period decimal, plain `=` |
| `row-03-suffix-comma-plain.journal` | 3 | Suffix `EUR`, comma decimal, plain `=` — the original reproduction |
| `row-04-prefix-period-sole-commodity.journal` | 4 | Prefix, period, `==` (sole-commodity assertion) |
| `row-05-suffix-comma-inclusive.journal` | 5 | Suffix, comma, `=*` (inclusive assertion) |
| `row-06-suffix-comma-multiposting.journal` | 6 | Suffix, comma, 3-posting transaction (sibling-net case) |
| `row-07-negative-unbalanced-assertion.journal` | 7 (negative) | Assertion amount that doesn't balance against the other posting |
| `row-08-negative-malformed-marker.journal` | 8 (negative) | Malformed `===` marker |
| `row-09-boundary-cross-transaction-running-balance.journal` | 9 (boundary, out of EC-022's scope) | Two transactions; account has a nonzero prior balance before the balance-assignment posting |

## Commands used (identical for every row, run in this directory)

```sh
hledger -f <file>.journal print
hledger -f <file>.journal balance
```

Full output, including exit codes, for every row: `oracle-transcripts.txt`
(captured in one batch run, this session, via a loop over all nine
files — not hand-transcribed from memory).

Ledgerkit's own current behaviour on the two rows that demonstrate
EC-022's failure modes (row 1: crash; row 3: silent corruption):
`ledgerkit-current-behaviour.txt`, captured via
`ledgerkit.parser.parse_string()` called directly against each
fixture's text, from `~/projects/ledgerkit`'s own checkout (its
`.venv`), in this same session.

## Expected outputs and exit codes (summary; full text in
`oracle-transcripts.txt`)

| Row | hledger exit | hledger result | Ledgerkit current behaviour |
|---|---|---|---|
| 1 | 0 | balances at `$100.00`/`$-100.00` | `ParseError: invalid amount: '= $100.00'` (crash) |
| 2 | 0 | balances at `100.00 USD`/`-100.00 USD` | not independently re-run this round (same code path as row 1/3) |
| 3 | 0 | balances at `100,00 EUR`/`-100,00 EUR` | silently assigns `commodity='='`, drops the `EUR` and the assertion (corruption) |
| 4 | 0 | balances identically to row 1 | not independently re-run this round |
| 5 | 0 | balances identically to row 3 | not independently re-run this round |
| 6 | 0 | balances at `100,00`/`50,00`/`-150,00 EUR` | not independently re-run this round |
| 7 | 1 | `"This transaction is unbalanced... should be 0 but is: 899,00 EUR"` | not independently re-run this round (hledger-side negative case) |
| 8 | 1 | `"unexpected '='... expecting '*' or amount"` | not independently re-run this round (hledger-side negative case) |
| 9 | 0 | `equity:unknown` resolves to `$-150.00` — proving the assigned amount is `$250.00 − $100.00(prior balance)`, not `$250.00` outright | N/A — Ledgerkit cannot even reach this case; it fails on the single-transaction syntax first |

Rows 2, 4, 5, 6, 7, 8 were re-confirmed on the **hledger side** in
this session (full transcripts in `oracle-transcripts.txt`); their
**Ledgerkit-side** behaviour was established in the prior planning
round (`planning/phase-02-planning-review.md` §3, "Independently
re-verified" section, for rows 1, 7, 8 specifically via a second
reviewer's own independently-constructed fixtures) and is not
re-run again here, since this directory's purpose is durability of
the **oracle** (hledger) evidence specifically — row 1/3's Ledgerkit
transcripts are included here because they are the two rows whose
Ledgerkit-side failure mode this plan's root-cause analysis cites
directly (`planning/phase-02-stage-2.1-plan.md` §3).

## Normalisation rules

None required — hledger's and Ledgerkit's output here is
deterministic plain text for a fixed input; no floating-point,
timestamp, or ordering nondeterminism was observed across repeated
runs in this or the prior session.

## Evidence of independent review

- The row-9 cross-transaction finding and rows 1/7/8 were
  independently re-derived by a separately-dispatched reviewer with
  its **own**, differently-valued fixtures (not these files) in
  `planning/phase-02-planning-review.md` §6 ("Independently
  re-verified and found accurate") — that review used USD amounts of
  $200/$350 and different account names, confirming the same
  underlying hledger behaviour from a genuinely independent fixture,
  not a copy of this directory's files.
- This directory's own files were produced and re-run directly by the
  orchestrating session, not independently verified a second time as
  *these exact files* — recorded honestly as that narrower claim, not
  conflated with the broader independent re-derivation above.

## Scope boundary preserved (authorising prompt §5)

Row 9 is a **required disposition, not a required pass** for EC-022's
eventual fix (`planning/phase-02-stage-2.1-plan.md` §4/§5) — it
demonstrates a real, larger boundary (full cross-transaction
running-balance semantics) that Ledgerkit's existing `resolve_elision()`
(`ledgerkit/parser.py:816–869`) cannot provide, and which EC-022's own
documented scope (a single-transaction parsing defect) does not
require fixing. Stage 2.4 must record this boundary as an explicit,
reasoned compat-register disposition (`kind: unsupported` or
`intentional_divergence`) if the fix does not extend to cover it —
not silently diverge from hledger here without anyone having decided
that was acceptable.

## Reproducing this evidence

```sh
cd evidence/phase-2-stage-2.1-oracle
for f in row-*.journal; do
  echo "=== $f ==="
  hledger -f "$f" print; echo "exit: $?"
  hledger -f "$f" balance; echo "exit: $?"
done
```

Requires `hledger` on `PATH` at version `1.52.4` (or a later version
confirmed not to have changed this behaviour — re-check against
`~/projects/hledger`'s current HEAD before trusting an unreviewed
later version silently).
