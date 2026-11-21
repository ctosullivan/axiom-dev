"""Tests for src/axiom_validator.py against contracts/documentation-schema-validator.md.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v

Each fixture under tests/fixtures/ was written to exercise exactly one
contract rule; each test method here names the rule and fixture it
checks, and asserts both the overall result and that the specific
expected error actually appears (not just "FAIL" with no detail —
contract rule 9 requires actionable error text).
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
        result = validate_file(FIXTURES / "valid" / "complete.md", REPO_ROOT)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["errors"], [])


class TestNoFrontmatter(unittest.TestCase):
    """Rule 1: no front-matter is SKIPPED, not an error."""

    def test_no_frontmatter_is_skipped(self):
        result = validate_file(FIXTURES / "invalid" / "no_frontmatter.md", REPO_ROOT)
        self.assertEqual(result["result"], "SKIPPED")
        self.assertEqual(result["errors"], [])


class TestInvalidYaml(unittest.TestCase):
    """Rule 2: unparseable front-matter is INVALID_SCHEMA with the parse error."""

    def test_bad_yaml_is_invalid_schema(self):
        result = validate_file(FIXTURES / "invalid" / "bad_yaml.md", REPO_ROOT)
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("YAML" in e for e in result["errors"]))


class TestMissingField(unittest.TestCase):
    """Rule 3: valid YAML missing a required field is INVALID_SCHEMA, naming it."""

    def test_missing_field_is_invalid_schema(self):
        result = validate_file(FIXTURES / "invalid" / "missing_field.md", REPO_ROOT)
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("acceptance_criteria" in e for e in result["errors"]))


class TestMissingSection(unittest.TestCase):
    """Rule 4: a required_sections entry absent from the body is FAIL, named."""

    def test_missing_section_fails_and_names_it(self):
        result = validate_file(FIXTURES / "invalid" / "missing_section.md", REPO_ROOT)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("NotPresent" in e for e in result["errors"]))


class TestBrokenAuthoritativeSource(unittest.TestCase):
    """Rule 5: an authoritative_sources path that doesn't resolve is FAIL, named."""

    def test_broken_authoritative_source_fails_and_names_it(self):
        result = validate_file(
            FIXTURES / "invalid" / "broken_authoritative_source.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("this-file-does-not-exist.md" in e for e in result["errors"])
        )


class TestBrokenLink(unittest.TestCase):
    """Rule 6: a broken body Markdown link is FAIL, named."""

    def test_broken_link_fails_and_names_it(self):
        result = validate_file(FIXTURES / "invalid" / "broken_link.md", REPO_ROOT)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("this-does-not-exist.md" in e for e in result["errors"])
        )


class TestBadAdrReference(unittest.TestCase):
    """Rule 7: a decisions/NNNN-*.md reference to a non-existent ADR is FAIL,
    with ADR-specific error detail (not just a generic broken-link message)."""

    def test_bad_adr_reference_fails_with_adr_specific_message(self):
        result = validate_file(FIXTURES / "invalid" / "bad_adr_reference.md", REPO_ROOT)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("9999" in e for e in result["errors"]))
        self.assertTrue(any("ADR" in e for e in result["errors"]))


class TestPathOutsideRepository(unittest.TestCase):
    """Rule 5/6: a path that resolves outside the repository fails, even
    if something happens to exist there. Added after independent review
    found this was unenforced — see evidence/stage-1.4-baseline.md."""

    def test_authoritative_source_outside_repo_fails(self):
        result = validate_file(FIXTURES / "invalid" / "path_outside_repo.md", REPO_ROOT)
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
            FIXTURES / "invalid" / "heading_in_code_block.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("HiddenHeading" in e for e in result["errors"]))


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
