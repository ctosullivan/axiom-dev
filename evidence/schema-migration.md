# Schema migration report (prompt 004 Amendment B)

Written directly in the companion-schema convention (`decisions/0006`)
rather than with embedded front-matter, since that convention no longer
exists for new documents as of this change.

## Scope

Every Markdown file in the repository that carried embedded YAML
front-matter was inspected (`git grep`-equivalent scan: check the first
line of every tracked `.md` file for `---`). **29 files** matched.
**15** use the documentation-schema convention
(`audience`/`purpose`/`required_sections`/`authoritative_sources`/
`acceptance_criteria`) and were migrated. **14** are test fixtures under
`tests/fixtures/` and were migrated separately (same mechanism, listed
below, plus new fixtures added for the new rules). **4 files were found
and deliberately excepted**: `planning/prompts/001-004-*.md` use a
different, unrelated front-matter convention (`id`/`title`/`status`/
`date_received`/`source`/`authorising`/`amends` — preserved-prompt
provenance metadata, not a documentation schema) and are explicitly out
of scope for this migration — see
`contracts/documentation-schema-validator.md`'s "Contract revision"
Non-goal and `docs/axiom-validator.md`'s Limitations for why the
validator's embedded-front-matter detection still (correctly, if
imprecisely-worded) reports `FAIL` for them, and why that is not treated
as a defect.

## Migrated real documents (15)

Each migrated by: extracting the exact YAML text between the `---`
delimiters verbatim (no re-formatting through a YAML dumper, so list
styles, quoting, and comments are preserved byte-for-byte) into
`<path>.schema.yaml`; removing the front-matter block and one leading
blank line from the `.md` file; leaving every other byte of the
document body untouched. Verified per file via `git diff --stat` on the
`.md` file: every file below shows **exactly N front-matter lines
deleted, zero lines added** — confirmed directly, not assumed, for a
representative sample (`evidence/stage-1.4-baseline.md`,
`evidence/stage-1.4-refactor.md`, `evidence/stage-1.5-reconstruction.md`,
`evidence/phase-1-closeout.md`,
`planning/retros/phase-1-stages-1.0-through-1.5.md`,
`docs/agent-isolation.md`, `docs/development-lifecycle.md` — each showed
exactly 10 deletions, 0 additions).

| Document | Schema requirements preserved | Further content update in this same change |
|---|---|---|
| `README.md` | Yes, unchanged | Repository-map table entries (unrelated to migration, pre-existing maintenance) |
| `contracts/codex-gate-policy-evaluator.md` | Yes, unchanged | One path reference (`.github/deferred/...`) from the prompt 003 batch, unrelated to this migration |
| `contracts/documentation-schema-validator.md` | Yes, unchanged | "Contract revision" section added (this is the contract being amended, not merely migrated) |
| `docs/agent-isolation.md` | Yes, unchanged | None |
| `docs/axiom-validator.md` | Yes, unchanged | Architecture/Usage/Limitations substantially rewritten to describe companion-schema loading (the component's own behaviour changed, so its docs must too, same commit) |
| `docs/development-lifecycle.md` | Yes, unchanged | None |
| `docs/documentation-schema.md` | **Acceptance criteria rewritten** — see note below | Convention section substantially rewritten (this document defines the convention being changed) |
| `docs/knowledge-placement.md` | Yes, unchanged | Two prose references to "front-matter" updated to "companion schema" |
| `docs/knowledge-reconciliation.md` | Yes, unchanged | One prose reference in the (prescriptive, non-historical) Procedure section updated; the historical Worked Example section left as written |
| `evidence/phase-1-closeout.md` | Yes, unchanged | None |
| `evidence/schema-value-assessment.md` | Yes, unchanged | None |
| `evidence/stage-1.4-baseline.md` | Yes, unchanged | None (historical evidence — not reinterpreted) |
| `evidence/stage-1.4-refactor.md` | Yes, unchanged | None (historical evidence — not reinterpreted) |
| `evidence/stage-1.5-reconstruction.md` | Yes, unchanged | None (historical evidence — not reinterpreted) |
| `planning/retros/phase-1-stages-1.0-through-1.5.md` | Yes, unchanged | None (historical retrospective — not reinterpreted) |

**Note on `docs/documentation-schema.md`'s schema:** this is the one
file whose *schema itself* needed a substantive edit, not just a
location change — its original acceptance criterion ("the convention is
simpler than CodeCompass's separate-sidecar-file approach") became
false the moment the convention became a sidecar approach. Rewritten to
assert what's actually true now (the reversal is evidence-justified, and
the reintroduced drift risk is named and mechanically addressed) rather
than left as a criterion the document could never again satisfy. This
is the one exception to "preserve the original schema's meaning"
Amendment B requires — justified because the original meaning was
specifically "sidecars are worse than front-matter," which this exact
change reverses by design; keeping it verbatim would make this document
permanently, knowingly FAIL its own acceptance criterion.

## Migrated and added test fixtures

14 existing fixtures migrated the same way (verbatim YAML extraction);
`tests/fixtures/invalid/no_frontmatter.md` renamed to `no_schema.md`
(same SKIPPED behaviour, new accurate name — the fixture never had
front-matter to begin with, so "no_frontmatter" described the input,
while "no_schema" describes what it now tests under the companion
convention). `tests/fixtures/invalid/bad_yaml.md` is a special case: its
deliberately-malformed YAML moved from embedded front-matter into
`bad_yaml.md.schema.yaml` unchanged in content, with the `.md` file's
body rewritten to describe the new scenario (the old body text
referenced "front-matter" explicitly, which would itself have been
inaccurate to leave in place).

**4 new fixtures added** for contract revision rules not covered by any
pre-existing fixture: `embedded_frontmatter_reintroduced.md` (rule 7),
`orphaned.md.schema.yaml` with no sibling `.md` (rule 8) — both exercised
by new test classes in `tests/test_axiom_validator.py`
(`TestEmbeddedFrontmatterReintroduced`, `TestOrphanedSchema`). The
existing governed-document-scope tests in
`tests/test_axiom_validator_schema_content.py`
(`TestGovernedDocumentScope`) were updated in place to use `no_schema.md`
and the new "no companion schema file" wording — same test intent (rule
15), new trigger condition.

This retires `evidence/stage-1.4-baseline.md`'s checksum-protection as a
live gate for the fixtures it covers — explicitly anticipated by that
file's own governing rule ("if the refactor needs a fixture or test to
change, that's a contract change... needs its own explicit, reviewed
commit" — this is that commit, per `decisions/0006`). The baseline file
itself is not edited; it remains the accurate historical record of what
Stage 1.4 verified at the time.

## Verification performed

(Per Amendment B's "Required migration evidence" list.)

- **Markdown body unchanged apart from front-matter removal:** confirmed
  via `git diff --stat` for every real document (sample shown above, all
  exactly N-deletions/0-additions); the remaining real documents were
  migrated by the identical mechanical script, not hand-edited, so the
  same guarantee applies uniformly.
- **Extracted schema retains original requirements:** confirmed by
  direct read of each `.schema.yaml` file against its source document's
  prior front-matter (byte-for-byte for all but
  `docs/documentation-schema.md`, explained above) and by the full test
  suite passing (next section).
- **Schema discoverable through the naming convention:** confirmed —
  every migrated document's companion file sits at exactly
  `<path>.md.schema.yaml`, computed and verified by
  `parsing.companion_schema_path`, exercised by every passing test below.
- **Existing relative links remain valid:** confirmed — `check_links`
  and `check_authoritative_sources` ran against every migrated document
  as part of the full validator run below; zero broken-link/broken-source
  findings.
- **The new validator accepts the migrated document and its schema:**
  confirmed — all 9 governed documents existing at the time this check
  was written report `PASS` (the manifest grew to 11 later, by Amendment
  F below, adding `docs/phase-archiving.md` and
  `planning/archive/README.md` — both also confirmed `PASS`, see §21);
  all 15 migrated
  real documents (governed or not) report `PASS` when validated directly
  (see commit's test run).

## Test results

`PYTHONPATH=src python3 -m unittest discover -s tests -v`: **26/26
pass** (14 original Stage 1.4 tests + 9 prompt 003 Amendment C tests,
both suites re-targeted at the new fixture layout with identical
rule-level intent, plus 3 new tests for contract revision rules 7/8:
`TestEmbeddedFrontmatterReintroduced`,
`TestOrphanedSchema` × 2 methods).
`PYTHONPATH=.github/scripts python3 -m unittest discover -s .github/scripts/tests -v`:
**16/16 pass**, unaffected by this change.

## Exceptions

`planning/prompts/001-004-*.md` (4 files) — not schema-bearing
documents under this convention; see Scope above. No other exceptions —
every file the initial scan found was either migrated or is one of
these 4, accounted for.

## Second relocation (prompt 005 — top-level `schemas/` directory, decisions/0007)

A second, independent move, recorded separately rather than rewriting
the record above (which remains accurate for the front-matter → companion-file
move it describes): every schema file this document lists above moved
again, from colocated-beside-its-document to a path mirrored under a
top-level `schemas/` directory, via `git mv` (production schemas) or
`mv` + re-staging (the small number untracked at move time). **YAML
content unchanged** for every file except
`schemas/docs/documentation-schema.md.schema.yaml`, whose
`acceptance_criteria` needed updating for the same reason its content
needed updating during the first move (`decisions/0006`'s own schema
asserted something the convention itself was about to make false) —
see that file directly for the exact wording change.

| Original path (decisions/0006) | New path (decisions/0007) | Document | YAML changed? | Validates? |
|---|---|---|---|---|
| `README.md.schema.yaml` | `schemas/README.md.schema.yaml` | `README.md` | No | PASS |
| `docs/*.md.schema.yaml` (7 files) | `schemas/docs/*.md.schema.yaml` | `docs/*.md` | `documentation-schema.md.schema.yaml` only | All PASS |
| `contracts/*.md.schema.yaml` (2 files) | `schemas/contracts/*.md.schema.yaml` | `contracts/*.md` | No | Both PASS |
| `evidence/*.md.schema.yaml` (5 files) | `schemas/evidence/*.md.schema.yaml` | `evidence/*.md` | No | All PASS (not governed; checked directly) |
| `planning/retros/*.md.schema.yaml` (1 file) | `schemas/planning/retros/*.md.schema.yaml` | the Phase 1 retrospective | No | PASS (not governed; checked directly) |
| `planning/archive/README.md.schema.yaml` | `schemas/planning/archive/README.md.schema.yaml` | `planning/archive/README.md` | No | PASS |
| `docs/governed-documents.txt` | `schemas/governed-documents.txt` | — (the manifest itself) | No | N/A |
| 18 fixture `.md.schema.yaml` files, colocated under `tests/fixtures/{invalid,valid}/` | `tests/fixtures/schemas/{invalid,valid}/*.md.schema.yaml` | the corresponding fixture `.md` files | No | All 50 tests pass against the new layout |

**Verification performed for this move:**

- **Authoritative-source references still resolve from the repository
  root:** unaffected by this move — `authoritative_sources` entries are
  paths to *other* repository files (e.g. `AGENTS.md`), never to a
  schema file itself, so moving schema files cannot break them. Checked
  directly: all 11 governed documents and all migrated real documents
  still report `PASS`.
- **The new validator discovers every relocated schema correctly:** the
  full test suite (50 tests, including the 13
  `tests/test_schema_relocation.py` tests exercising the mirroring
  function directly against real repository paths — corrected here
  from an initial 49/12 count that predated this section's own
  symlink-escape regression test being added; caught by independent
  review recounting directly rather than trusting the figure already
  written here) passes; the exact CI command
  (`PYTHONPATH=src python3 -m axiom_validator "$(cat
  schemas/governed-documents.txt | ...)" --repo-root .`) was run
  directly and returns `PASS` for all 11 entries, exit code 0.
- **No obsolete production schemas left alongside Markdown files:**
  checked by a repository-wide scan
  (`tests/test_schema_relocation.py`'s
  `TestNoStraySchemaFilesOutsideSchemasTree`) asserting every
  `*.md.schema.yaml` file in the repository has `schemas` as one of its
  path components (true for both the production `schemas/` tree and the
  separate `tests/fixtures/schemas/` fixture tree) — zero stray files
  found.
- **No competing orphan false-positive:** `rules.find_orphaned_schemas`
  run against the real repository root returns `[]` (confirmed
  directly), because it now scans only `<repo_root>/schemas/`, which
  never contains the fixture tree at all.
