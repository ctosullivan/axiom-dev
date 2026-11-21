# Stage 1.4 refactor: before/after verification and defect ledger

Per `planning/phase-01-foundation.md` §4 Stage 1.4, a cosmetic refactor
(renames, formatting) does not satisfy this stage. This is a real
structural change: separation of parsing, rule-checking, and reporting
concerns that were previously tangled together in one function.

## What changed

`src/axiom_validator.py` (one file, ~150 lines, front-matter parsing +
all rule checks + result-building interleaved in a single function) was
replaced by the package `src/axiom_validator/`:

- `parsing.py` — front-matter splitting/parsing, heading extraction
  (fenced-code-block-excluding), link extraction (inline-code-excluding).
- `rules.py` — the five rule-check functions (required fields, required
  sections, authoritative sources, links, plus the shared `is_within`
  containment helper), each taking already-parsed data and returning a
  list of error strings — no file I/O, no regex of its own beyond the
  ADR-path pattern.
- `reporting.py` — building the report dict shape and formatting/exit-code
  logic for the CLI.
- `__init__.py` — orchestrates the three above; `validate_file` and
  `main` keep their exact pre-refactor names and signatures.
- `__main__.py` — new, so `python3 -m axiom_validator` works as a package
  (the pre-refactor file supported direct `python3 src/axiom_validator.py`
  execution; this is a CLI-invocation detail, not a contracted or
  tested behaviour, so changing it is an accepted refactor side effect,
  not a regression — see `contracts/documentation-schema-validator.md`,
  which fixes no CLI shape).

`tests/test_axiom_validator.py` and every file under `tests/fixtures/`
are **byte-identical** to the locked baseline — verified by re-computing
their SHA-256 checksums and diffing against
`evidence/stage-1.4-baseline.md`'s recorded values. No "contract change"
commit was needed because no fixture or test needed to change.

## Before/after verification

**Before** (locked in `evidence/stage-1.4-baseline.md`, captured against
the pre-refactor monolithic implementation): 14/14 tests pass, exact
names and order recorded there.

**After** (this refactor, same command, same machine, same fixtures):

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

**Identical set of 14 tests, identical results.** Additionally verified
directly (not only via the test suite): `python3 -m axiom_validator
docs/knowledge-placement.md --repo-root .` produces the same
`{"result": "PASS", "errors": []}` shape as the pre-refactor CLI did for
the same file.

## Defect ledger

- **Detected by tests (before refactor, already fixed then):** 1 real
  documentation defect (shorthand ADR citations) — see
  `evidence/stage-1.4-baseline.md`. Not a refactor-introduced defect;
  listed for continuity.
- **Detected by independent review (before refactor, already fixed
  then):** 2 — unenforced repository-containment check; fenced-code-block
  heading false positive. See `evidence/stage-1.4-baseline.md`. Not
  refactor-introduced; listed for continuity.
- **Defects the refactor itself introduced:** 0, as evidenced by the
  identical before/after test results above. This claim rests on the
  test suite's actual coverage (14 tests across all 9 contract rules
  plus 4 real-document checks) — it is not a claim that the refactor is
  proven bug-free beyond what that suite can observe.
- **Defects the refactor's own review (below) found that the before/after
  test comparison did not:** see Independent review.

## Independent review

A fresh, non-forked agent (best-effort isolation — same standard as
`planning/phase-01-foundation.md` §6, §11, §12, §13) independently
re-derived every claim above rather than trusting it:

- Re-computed SHA-256 of all 10 protected fixture/test files and
  confirmed byte-identical match against the locked baseline.
- Ran the test suite itself: 14/14 pass, same names/order, not
  reproduced from memory.
- Diffed the old monolithic file (`git show 07d5548:src/axiom_validator.py`)
  against the four new modules line-by-line and confirmed a real
  separation of concerns (pure functions, explicit data flow), not
  copy-pasted logic — `parsing.py` owns all regexes and extraction,
  `rules.py` owns the four rule-check functions plus `is_within`,
  `reporting.py` owns report shaping, `__init__.py` orchestrates in the
  same order as the original (required-fields short-circuit, then
  sections, then authoritative-sources, then links) with the
  containment check (`is_within`) still firing before the existence
  check in both `check_authoritative_sources` and `check_links` —
  identical to the pre-refactor ordering, which matters because it
  determines which error message fires first for a path that is both
  outside the repo and nonexistent.
- Read `contracts/documentation-schema-validator.md` directly and
  confirmed it specifies no CLI invocation syntax, so the
  `python3 -m axiom_validator` change is correctly classified as an
  accepted side effect, not a regression; ran the new CLI directly and
  confirmed it works.
- Found no behavioural drift, no feature creep (new module line count is
  docstring/separation overhead, not new functionality;
  `requirements.txt` unchanged), and confirmed the "0 defects introduced"
  ledger entry holds given everything above.

**No blocking findings.** One procedural note: this section itself was a
placeholder until this review completed — now filled in, closing that
gap.

**Verdict (reviewer's own words, condensed):** "This is a genuine,
verified behaviour-preserving refactor. All claims... were independently
re-derived rather than trusted... No blocking findings."
