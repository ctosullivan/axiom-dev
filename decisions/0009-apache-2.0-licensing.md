# 0009. Relicense from MIT to Apache License 2.0

## Status

Accepted — direction authorised by repository owner on 2026-11-25.

## Context

Axiom Dev was originally licensed under MIT (`LICENSE`, copyright
2026, Cormac O' Sullivan). The project is now a reusable development
template intended for adoption by independent repositories (Ledgerkit
first, others per Phase 2's own stated goal of independent-project
adoption, `planning/phase-02-template.md`). The owner directed a
licence change to Apache License 2.0 as part of Stage 2.1 closeout and
Stage 2.2 planning.

## Decision

1. Replace `LICENSE`'s MIT text with the complete, unmodified standard
   Apache License 2.0 text (from `https://www.apache.org/licenses/LICENSE-2.0.txt`),
   verbatim — no clauses added, removed or reworded.
2. Add a `NOTICE` file carrying the project's copyright line
   ("Copyright 2026 Cormac O' Sullivan"), preserving the existing
   copyright holder and year exactly as the prior MIT notice stated
   them — the licence change does not reassign or alter authorship.
3. Update `README.md`'s licence section and this ADR are the only
   licence-reference changes; no source file carries its own licence
   header, and none is added by this decision (consistent with
   "minimal documentation" — a per-file SPDX header is not introduced
   without a demonstrated need for one).
4. No third-party code is vendored into this repository (confirmed by
   inspection before this change — the only runtime dependency,
   PyYAML, is an external pip package, not bundled source, and carries
   its own, unaffected licence). This decision relicenses only
   Axiom Dev's own authored content.

## Alternatives considered

- **Keep MIT.** Rejected by explicit owner direction — Apache 2.0's
  express patent grant and contribution-licensing terms (Sections 3,
  5) are judged more appropriate for a template other organisations
  will adopt and potentially contribute to.
- **A different permissive licence (BSD-3-Clause, etc.).** Not
  requested; Apache 2.0 was the owner's specific direction.
- **Add per-file SPDX headers now.** Rejected as unnecessary
  documentation volume for a project with no history of per-file
  licence disputes; revisit only if a real need is demonstrated
  (e.g. a consumer project requires it for its own compliance
  tooling).

## Rationale

A reusable template distributed for adoption by independent projects
benefits from Apache 2.0's explicit patent grant and its clearer
terms for accepting external contributions, over MIT's simpler but
less explicit terms. The change is a direct owner decision, not a
project-internal architectural trade-off discovered through
development — recorded here per `AGENTS.md` §3 because a future
reader would otherwise have to re-derive why the licence changed and
on whose authority, and because `AGENTS.md` §11 lists licence changes
as a standing human-approval boundary.

## Consequences

- All of Axiom Dev's own code and documentation is now licensed under
  Apache 2.0, not MIT, from this commit forward. Prior MIT-licensed
  commits remain MIT for whatever historical distribution already
  occurred under that licence — this ADR does not purport to
  retroactively relicense history, only the current and future state
  of the files in this repository.
- Any future vendored/third-party content must be checked for Apache
  2.0 compatibility before inclusion (Category A/weak-copyleft
  licences such as MIT, BSD are compatible; strong copyleft licences
  such as GPL are not, without separate handling).
- Ledgerkit and hledger remain independent projects under their own,
  unaffected licences; adopting Axiom's template into Ledgerkit does
  not relicense Ledgerkit itself.

## Relevant evidence

- `LICENSE` (full Apache 2.0 text) and `NOTICE` (copyright line),
  this same change.
- `README.md`'s licence section, updated in the same change.
- Repository owner direction dated 2026-11-25 (this decision).
