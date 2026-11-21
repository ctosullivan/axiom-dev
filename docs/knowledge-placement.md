---
audience: contributors and agents making any non-trivial change
purpose: define where a given piece of project knowledge belongs, and what enforces that
required_sections: [Classification, Placement table, Enforcement classes, Reconciliation hook]
authoritative_sources: [AGENTS.md, decisions/0002-knowledge-architecture.md]
acceptance_criteria:
  - every knowledge category in the placement table maps to exactly one authoritative artifact kind
  - every enforcement class states whether it blocks a change or is advisory
  - this document itself has been checked against docs/documentation-schema.md
---

# Knowledge placement policy

This is the full version of the placement table in `AGENTS.md` §7, which
remains the short, canonical summary — if the two ever disagree, fix
`AGENTS.md` first (it is the more-trusted file) and update this document
to match, don't let them drift apart.

## Classification

Every claim this project makes about its own behaviour is one of:

- **INTENDED** — authorised, documented behaviour (e.g. "the validator
  rejects a document missing a required section" as stated in a contract).
- **OBSERVED** — behaviour actually seen by direct inspection or execution,
  which may or may not match what was intended.
- **VERIFIED** — OBSERVED behaviour checked against an accepted contract,
  within a stated scope, by someone/something other than the implementer.
- **UNCERTAIN** — insufficient evidence either way. Honest default when no
  one has checked yet.
- **CONTESTED** — direct, unresolved conflict between two evidence
  sources (e.g. a passing test and a failing independent review).

These five are never collapsed into a single confidence number. A
document or evidence record states which one applies to a given claim,
explicitly, when the distinction matters (it usually matters for anything
under `contracts/` or `evidence/`).

## Placement table

| Knowledge category | Lives in | Who/what can write it |
|---|---|---|
| Implementation behaviour | Source code (`src/`, once it exists) | Implementer |
| Interfaces | Docstrings | Implementer, same change as the code |
| Non-obvious local rationale | Code comments | Implementer, same change as the code |
| Architectural decisions | `decisions/` (ADRs) | Whoever proposes the decision; accepted only with human approval (`AGENTS.md` §11) |
| Required behaviour (contracts) | `contracts/` | Written and independently reviewed *before* the implementation it governs (`decisions/0004`) |
| Verification outcomes | `evidence/` | Whoever ran the verification; must cite what was checked and how |
| Human-facing explanation | `docs/` | Anyone; synchronised in the same change as whatever it explains (`AGENTS.md` §5) |
| Current status / next action | `planning/CONTEXT.md` | Whoever last touched the project state; kept current, not historical |
| Historical narrative | `planning/retros/` (phase retrospectives) | Written once, after the fact; never edited to read as current |

Historical reasoning is not current architectural justification: if an
ADR's stated rationale stops applying, write a superseding ADR
(`AGENTS.md` §3) rather than letting people cite the old rationale as if
it still held.

**Commit and PR history is not a second "lives in" location for
historical narrative** — found worth stating explicitly by independent
review, which read the prior wording ("`planning/retros/`, commit/PR
history") as naming two authoritative locations for one category,
contradicting this document's own acceptance criterion that every
category map to exactly one. Commit/PR history is a supplementary,
naturally-occurring record (every change already has one); `planning/retros/`
is the one place a narrative account is deliberately *written*, and is
what this table's "Lives in" column names.

## Enforcement classes

Adapted from CodeCompass's three-class split (`decisions/0094`), with the
same rule about which classes block. A given control can be at one of six
distinct levels, and this document states the *actual current* level for
each real control in this repository — not the level a future stage
intends to reach. Conflating these (claiming "mechanical" for something
only "locally tested," or "enforced" for something merely "executed by
CI") is itself the documentation-drift failure mode
`planning/prompts/003-phase-1-corrective-amendment.md` Amendment B3
identified and this section was rewritten to stop:

1. **Policy defined** — written down, not yet checked by anything.
   **Advisory only** — nothing can fail here because nothing runs.
2. **Mechanism implemented** — code exists that can check it.
   **Advisory only** — the code existing doesn't mean anyone ran it.
3. **Mechanism locally tested** — a developer can run it and get a real
   answer, but nothing runs it automatically. **Advisory only** — it
   catches a real violation only if someone remembers to run it.
4. **Mechanism executed by CI** — runs automatically on every push/PR.
   **Advisory/blocks-nothing-mechanically** — a failure is visible, but
   nothing currently stops a merge on it.
5. **Mechanism enforced as a required merge condition** — a failure
   mechanically blocks merge (GitHub branch protection / required status
   checks). **Blocks** — by definition, this is the one level that does.
   **Nothing in this repository is currently at this level** — reaching
   it needs repository-admin API access this environment has never had
   (confirmed again, directly, as part of this correction — see
   `decisions/0005`).
6. **Semantic / editorial (manual)** — needs human or independent-agent
   judgement about quality, clarity, or whether a claim is well-supported
   (CONTESTED items in particular). **Advisory only, by design** — never
   mechanically enforced, not because of a missing capability.

Where each real control in this repository actually sits, as of this
correction:

| Control | Level |
|---|---|
| `src/axiom_validator/` — front-matter presence, required sections, path/link resolution, ADR-reference existence, field type/non-emptiness (Amendment C), governed-document scope | 4 — executed by CI (`.github/workflows/deterministic-checks.yml`), **not** a required merge check |
| `.github/scripts/policy_evaluator.py` — Codex-finding policy decisions | 4 — executed by CI, not a required merge check; its live Codex input source is deferred (`decisions/0005`) |
| Sequential ADR numbering | 1 — policy only (`AGENTS.md` §3). **Nothing in this repository mechanically checks that ADR numbers are sequential or gap-free** — the validator's `ADR_PATH_RE` only checks that a *referenced* ADR number resolves to a real file, which is a different, narrower check than "the ADR sequence has no gaps." Do not read the validator's existing-ADR-reference check as sequential-numbering enforcement. |
| Complete documentation correctness (semantic accuracy of claims) | 6 — semantic/editorial only, by design; see `docs/knowledge-reconciliation.md` and the Amendment D semantic-review procedure (`planning/phase-01-foundation.md` §17, §19) |
| Native Codex GitHub PR review | Not yet run for real (no PR opened); once run, it is level 6 (an independent AI review a human acts on), **never** level 5 — `decisions/0005` is explicit that this must never be described as mechanically preventing an unauthorised merge |
| GitHub required status checks / branch protection | Not configured; would be level 5 if it existed, and nothing here claims it does |

## Reconciliation hook

After any change that touches behaviour, an architectural decision, an
interface, or an established knowledge record, run this check:

1. List what changed (diff).
2. For each change, find every doc/decision/evidence record whose claims
   depend on the old state.
3. For each, confirm the claim still holds; if not, fix it in the same
   change (`AGENTS.md` §5) — not as follow-up.
4. Record anything found and fixed as a reconciliation note (see
   `docs/knowledge-reconciliation.md` for the full procedure and a worked
   example run against this repository's own Stage 1.0→1.1 transition).

Step 1 (listing governed-documentation-schema violations) can now be
partly mechanised: `src/axiom_validator/` checks structural/type/content
rules against `docs/governed-documents.txt` and runs in CI (level 4
above) — but steps 2–4 (finding every *dependent* claim and confirming it
still holds) remain semantic/editorial (level 6) and are not something
the validator does or is intended to do.

## Manual validation record

Checked by hand against this document's own front-matter schema
(`docs/documentation-schema.md`'s convention), itemized per acceptance
criterion rather than asserted in the abstract — independent review found
the prior, unitemized version of this claim left two of the three
criteria `UNCERTAIN`:

- `required_sections`: all four present as written (`Classification`,
  `Placement table`, `Enforcement classes`, `Reconciliation hook` —
  checked exact heading text).
- `authoritative_sources`: both resolve (`AGENTS.md`, `decisions/0002-knowledge-architecture.md`).
- Acceptance criterion 1 ("every knowledge category... maps to exactly
  one authoritative artifact kind"): true as of this correction — the
  Placement table's "Historical narrative" row previously named two
  destinations (`planning/retros/` and commit/PR history); fixed above.
- Acceptance criterion 2 ("every enforcement class states whether it
  blocks or is advisory"): true as of this correction — levels 1–3
  previously described only what exists without an explicit
  blocking/advisory statement; each now states one.
- Acceptance criterion 3 ("this document itself has been checked against
  `docs/documentation-schema.md`"): this record is that check — see
  `evidence/phase-1-log.md` for the dated log entry.
