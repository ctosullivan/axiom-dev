"""Tests for src/axiom_validator against contracts/documentation-schema-validator.md,
including its "Contract revision" section (prompt 004, decisions/0006).

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v

Each fixture under tests/fixtures/ was written to exercise exactly one
contract rule; each test method here names the rule and fixture it
checks, and asserts both the overall result and that the specific
expected error actually appears (not just "FAIL" with no detail —
contract rule 9 requires actionable error text).

Fixtures were migrated from embedded front-matter to companion
`.schema.yaml` files by this same change (an explicit, independently
reviewed contract evolution — not a silent rewrite). `no_frontmatter.md`
was renamed to `no_schema.md` since that is what it now tests; every
other fixture kept its name, with its schema moved to a sibling
`<name>.schema.yaml` file and its Markdown body otherwise unchanged. See
evidence/schema-migration.md for the itemised migration record.
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from axiom_validator import validate_file  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"


class TestValidDocument(unittest.TestCase):
    """Rule 8: a fully conforming document passes with no errors."""

    def test_complete_fixture_passes(self):
        result = validate_file(FIXTURES / "valid" / "complete.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["errors"], [])


class TestNoCompanionSchema(unittest.TestCase):
    """Contract revision rule 2: no companion schema file is SKIPPED for a
    non-governed document, not an error. (Formerly "no front-matter",
    rule 1, under the superseded convention — same behaviour, new
    trigger condition.)"""

    def test_no_schema_is_skipped(self):
        result = validate_file(FIXTURES / "invalid" / "no_schema.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "SKIPPED")
        self.assertEqual(result["errors"], [])


class TestInvalidYaml(unittest.TestCase):
    """Contract revision rule 3: an unparseable companion schema file is
    INVALID_SCHEMA with the parse error. (Formerly rule 2.)"""

    def test_bad_yaml_is_invalid_schema(self):
        result = validate_file(FIXTURES / "invalid" / "bad_yaml.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("YAML" in e for e in result["errors"]))


class TestMissingField(unittest.TestCase):
    """Rule 3: valid YAML missing a required field is INVALID_SCHEMA, naming it."""

    def test_missing_field_is_invalid_schema(self):
        result = validate_file(FIXTURES / "invalid" / "missing_field.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("acceptance_criteria" in e for e in result["errors"]))


class TestMissingSection(unittest.TestCase):
    """Rule 4: a required_sections entry absent from the body is FAIL, named."""

    def test_missing_section_fails_and_names_it(self):
        result = validate_file(FIXTURES / "invalid" / "missing_section.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("NotPresent" in e for e in result["errors"]))


class TestBrokenAuthoritativeSource(unittest.TestCase):
    """Rule 5: an authoritative_sources path that doesn't resolve is FAIL, named."""

    def test_broken_authoritative_source_fails_and_names_it(self):
        result = validate_file(
            FIXTURES / "invalid" / "broken_authoritative_source.md", REPO_ROOT, schema_mirror_root=FIXTURES
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("this-file-does-not-exist.md" in e for e in result["errors"])
        )


class TestBrokenLink(unittest.TestCase):
    """Rule 6: a broken body Markdown link is FAIL, named."""

    def test_broken_link_fails_and_names_it(self):
        result = validate_file(FIXTURES / "invalid" / "broken_link.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("this-does-not-exist.md" in e for e in result["errors"])
        )


class TestBadAdrReference(unittest.TestCase):
    """Rule 7: a decisions/NNNN-*.md reference to a non-existent ADR is FAIL,
    with ADR-specific error detail (not just a generic broken-link message)."""

    def test_bad_adr_reference_fails_with_adr_specific_message(self):
        result = validate_file(FIXTURES / "invalid" / "bad_adr_reference.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("9999" in e for e in result["errors"]))
        self.assertTrue(any("ADR" in e for e in result["errors"]))


class TestPathOutsideRepository(unittest.TestCase):
    """Rule 5/6: a path that resolves outside the repository fails, even
    if something happens to exist there. Added after independent review
    found this was unenforced — see evidence/stage-1.4-baseline.md."""

    def test_authoritative_source_outside_repo_fails(self):
        result = validate_file(FIXTURES / "invalid" / "path_outside_repo.md", REPO_ROOT, schema_mirror_root=FIXTURES)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("outside the repository" in e for e in result["errors"])
        )


class TestHeadingInsideFencedCodeBlock(unittest.TestCase):
    """Rule 4: a heading-looking line inside a fenced code example must
    not count as a real section. Added after independent review found
    this was a false positive — see evidence/stage-1.4-baseline.md."""

    def test_heading_only_in_code_block_still_fails_as_missing(self):
        result = validate_file(
            FIXTURES / "invalid" / "heading_in_code_block.md", REPO_ROOT, schema_mirror_root=FIXTURES
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("HiddenHeading" in e for e in result["errors"]))


class TestEmbeddedFrontmatterReintroduced(unittest.TestCase):
    """Contract revision rule 7: a document that still starts with the
    old embedded front-matter block is FAIL, naming the reintroduction —
    never silently parsed as if it were the current schema."""

    def test_embedded_frontmatter_fails_and_names_it(self):
        result = validate_file(
            FIXTURES / "invalid" / "embedded_frontmatter_reintroduced.md", REPO_ROOT, schema_mirror_root=FIXTURES
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("embedded-front-matter" in e for e in result["errors"])
        )


class TestOrphanedSchema(unittest.TestCase):
    """Contract revision rule 8: a companion schema file with no
    corresponding document is an orphan. Repository-wide by nature, so
    tested via rules.find_orphaned_schemas directly rather than
    validate_file (see contracts/documentation-schema-validator.md,
    "Contract revision" rule 8's scope note)."""

    def test_orphaned_schema_fixture_is_detected(self):
        from axiom_validator import rules

        orphans = rules.find_orphaned_schemas(FIXTURES)
        orphan_names = {p.name for p in orphans}
        self.assertIn("orphaned.md.schema.yaml", orphan_names)

    def test_non_orphaned_schemas_are_not_flagged(self):
        from axiom_validator import rules

        orphans = rules.find_orphaned_schemas(FIXTURES)
        orphan_names = {p.name for p in orphans}
        self.assertNotIn("complete.md.schema.yaml", orphan_names)
        self.assertNotIn("bad_yaml.md.schema.yaml", orphan_names)


class TestArchiveEntryLinkVerification(unittest.TestCase):
    """Tests docs/phase-archiving.md's claim that archive-entry link
    resolution reuses the existing validator rather than needing new
    tooling (prompt 004 Amendment F, "Archive verification"). This
    fixture is deliberately NOT a real archived phase — it only proves
    the reused mechanism actually catches a broken link in a
    similarly-shaped document, without fabricating a completed phase."""

    def test_archive_entry_shaped_fixture_with_broken_link_fails(self):
        result = validate_file(
            FIXTURES / "invalid" / "archive_entry_broken_link.md", REPO_ROOT, schema_mirror_root=FIXTURES
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("this-evidence-file-does-not-exist.md" in e for e in result["errors"])
        )


class TestRealRepositoryDocuments(unittest.TestCase):
    """Sanity check against real, already-committed Axiom Dev documents —
    not just synthetic fixtures. These are expected to PASS; if one of
    them FAILs, that's either a real documentation defect or a validator
    bug, and this test will say which file to look at."""

    def test_docs_knowledge_placement_passes(self):
        result = validate_file(REPO_ROOT / "docs" / "knowledge-placement.md", REPO_ROOT)
        self.assertEqual(result["result"], "PASS", result["errors"])

    def test_docs_knowledge_reconciliation_passes(self):
        result = validate_file(
            REPO_ROOT / "docs" / "knowledge-reconciliation.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "PASS", result["errors"])

    def test_docs_documentation_schema_passes(self):
        result = validate_file(
            REPO_ROOT / "docs" / "documentation-schema.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "PASS", result["errors"])

    def test_readme_passes(self):
        result = validate_file(REPO_ROOT / "README.md", REPO_ROOT)
        self.assertEqual(result["result"], "PASS", result["errors"])


if __name__ == "__main__":
    unittest.main()
