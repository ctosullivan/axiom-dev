---
audience: whoever performs or reviews the Stage 1.4 refactor
purpose: record the protected pre-refactor baseline — fixture checksums and real test output — that the refactor must not silently change
required_sections: [Protected fixture checksums, Pre-refactor test run, Real-document dogfooding finding, Pre-implementation-review findings fixed before baseline lock]
authoritative_sources: [contracts/documentation-schema-validator.md, planning/phase-01-foundation.md]
acceptance_criteria:
  - the checksums below are the ones a post-refactor run must match, or the refactor has changed behaviour
  - the test output below was actually captured from a real run, not written from memory
---

# Stage 1.4 baseline (pre-refactor)

Captured 2026-11-21, after the initial (monolithic) implementation of
`src/axiom_validator.py`, an independent review of that implementation,
and the fixes that review's findings required — this is the **final**
pre-refactor state, locked after fixes, not the first draft. Per
`planning/phase-01-foundation.md` §4 Stage 1.4 "Anti-circularity
mechanics": a later PR (the refactor) that changes any of these files'
checksums without a separate, explicitly reviewed "contract change"
commit explaining why is a verification failure. This is a
**procedural** control (named honestly, per `decisions/0003` §3's
standard — nothing here mechanically blocks a mismatched checksum yet),
not a mechanical one.

## Protected fixture checksums

SHA-256, computed with `sha256sum`:

```
0a473ebe3cb5ab483b7eb123cd725f9fd3a95cfb3cab6c08cb3596cbdf105678  src/axiom_validator.py
65e319a4a92e9b9278dcbc08b8116250e2d5c3b307e81f4eec8494809ccea55e  tests/fixtures/invalid/bad_adr_reference.md
2bcfcb74c36bcf12ef4e5d6e9663dd0f604ab99c37da5f0d6581f5d57e996818  tests/fixtures/invalid/bad_yaml.md
259652c63f5a2c3263ec9929583f0c01112feaf39e1239389a9ab9aa6ba665ae  tests/fixtures/invalid/broken_authoritative_source.md
4cd4ca306a2bc3bd31debe5dddc8da5d10215f06ecf1f0ac3852f2500b4c88f6  tests/fixtures/invalid/broken_link.md
f8d4fcc213278acb44142285668deac2f0a425c68b18943990a3330e99b4cbef  tests/fixtures/invalid/heading_in_code_block.md
ac10526e890882453e882c9653b22c3fe7227abf4eb3d2058e2272e0d5818413  tests/fixtures/invalid/missing_field.md
0ab851b17b53752dcc8034214e56b3195950e6157f5819b121393d6827d15fa7  tests/fixtures/invalid/missing_section.md
a550e9b2f9ffb8fdb62bb877155e364fd959b5e1f593ed3187c639ee5194a657  tests/fixtures/invalid/no_frontmatter.md
72f3c11cadf526793802cd32a185a5aefe0086da4f9f7faee6229ea977482881  tests/fixtures/invalid/path_outside_repo.md
bd38df88a70de8e634615b26a6900105be632cb1d9a1e29abd6f5b168a7f5dea  tests/fixtures/valid/complete.md
88a0303b689d25f53e7089bbeec90cc043eb4b26e390753ca649bab9b89063cd  tests/test_axiom_validator.py
```

**The fixtures and the test file's checksums (not `src/axiom_validator.py`'s)
are what "protected" means for the refactor**: the refactor is expected
and required to change `src/axiom_validator.py`'s checksum (it's the
thing being refactored), but the fixtures and the test assertions must
produce byte-identical files — if the refactor needs a fixture or test
to change, that's a contract change, not an incidental refactor side
effect, and needs its own explicit, reviewed commit.

## Pre-refactor test run

Actual captured output of
`PYTHONPATH=src python3 -m unittest discover -s tests -v`, run
2026-11-21 against the monolithic implementation above:

```
test_bad_adr_reference_fails_with_adr_specific_message ... ok
test_broken_authoritative_source_fails_and_names_it ... ok
test_broken_link_fails_and_names_it ... ok
test_heading_only_in_code_block_still_fails_as_missing ... ok
test_bad_yaml_is_invalid_schema ... ok
test_missing_field_is_invalid_schema ... ok
test_missing_section_fails_and_names_it ... ok
test_no_frontmatter_is_skipped ... ok
test_authoritative_source_outside_repo_fails ... ok
test_docs_documentation_schema_passes ... ok
test_docs_knowledge_placement_passes ... ok
test_docs_knowledge_reconciliation_passes ... ok
test_readme_passes ... ok
test_complete_fixture_passes ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.041s

OK
```

14/14 pass. This exact suite, against the post-refactor implementation,
is the before/after comparison Stage 1.4 requires.

## Real-document dogfooding finding

The first run of `TestRealRepositoryDocuments` (testing the validator
against already-committed, real Axiom Dev documents, not only synthetic
fixtures — per Amendment D's "no synthetic substitute" requirement)
**failed**, for real, before any fix: `docs/documentation-schema.md` and
`docs/knowledge-placement.md` used shorthand ADR references
(`decisions/0002`, `decisions/0004`) in their `authoritative_sources`
front-matter instead of the real, exact filenames
(`decisions/0002-knowledge-architecture.md`,
`decisions/0004-phase-1-amendment-verification-measurement-and-acceptance.md`).
This is a genuine documentation defect the contract's rule 5 is designed
to catch, not a validator bug — fixed in the same change that discovered
it, and recorded here as the first real (non-synthetic) defect this
project's own tooling has found in its own documentation. See the
corresponding commit for the fix.

## Pre-implementation-review findings fixed before baseline lock

Per Amendment B (`decisions/0004`), the initial implementation was
independently reviewed *before* this baseline was locked. The reviewer
ran the tests themselves, re-computed all checksums, and verified the
dogfooding finding above against `git diff` rather than trusting the
narrative — all confirmed accurate. The review also found two real,
reproducible defects in the implementation, verified with concrete
counter-examples:

1. **BLOCKING — contract rule 5/6's "no paths outside the repository"
   was unenforced.** An `authoritative_sources` entry with enough `../`
   segments to resolve outside the repository was reported PASS as long
   as something happened to exist at the resolved location. Fixed by
   adding `_is_within()` in `src/axiom_validator.py` and applying it to
   both rule 5 (authoritative_sources) and rule 6 (body links) before
   the existence check. Regression fixture:
   `tests/fixtures/invalid/path_outside_repo.md`; regression test:
   `TestPathOutsideRepository`.
2. **BLOCKING — rule 4's heading match had no fenced-code-block
   exclusion.** A `#`-prefixed line inside a ` ``` ` fenced example was
   counted as a real heading — a false positive none of the original 7
   fixtures or 4 real-document checks happened to trigger, so it was
   latent, not caught by the test suite until the reviewer constructed a
   direct counter-example. Fixed by stripping fenced code blocks
   (`FENCED_CODE_BLOCK_RE`) before heading detection. Regression fixture:
   `tests/fixtures/invalid/heading_in_code_block.md`; regression test:
   `TestHeadingInsideFencedCodeBlock`.

Both fixes are reflected in the checksums and test run above — this
baseline is the state *after* those fixes, not before. Two advisory
findings were also recorded and left as documented, undemonstrated
limitations rather than fixed (proportionate scope, not every edge case):
rule 5's "bare path" check only recognises `§` as a section-marker
example, matching the contract's own prose; and rule 7's ADR-specific
error message doesn't distinguish "wrong ADR number" from "right number,
wrong filename slug" — both report as "non-existent," which is correct
per the contract's existence-based test but could be clearer. Neither is
exercised by any fixture; both are candidates for the refactor or a
future contract revision, not blocking issues in the current scope.
