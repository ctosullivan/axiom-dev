"""Regression tests for the prompt 003 Amendment C contract amendment
(contracts/documentation-schema-validator.md rules 10-15: field
type/non-emptiness checks and the governed-documents manifest).

Deliberately a **separate file** from tests/test_axiom_validator.py,
which is checksum-protected as part of the Stage 1.4 refactor baseline
(evidence/stage-1.4-baseline.md) and must not be edited to add this
amendment's coverage — see planning/phase-01-foundation.md Sec 17,
prompt 003 Amendment C ("new validation behaviour must be introduced
through an explicit, independently reviewed contract amendment with its
own regression tests").

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
(discovered alongside test_axiom_validator.py; no separate invocation
needed.)
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from axiom_validator import validate_file  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"


class TestEmptyAudience(unittest.TestCase):
    """Rule 10: audience must be a non-empty string."""

    def test_whitespace_only_audience_is_invalid_schema(self):
        result = validate_file(FIXTURES / "invalid" / "empty_audience.md", REPO_ROOT)
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("audience" in e for e in result["errors"]))


class TestNonStringRequiredSections(unittest.TestCase):
    """Rule 11: required_sections must be a list of strings, not a bare string."""

    def test_bare_string_required_sections_is_invalid_schema(self):
        result = validate_file(
            FIXTURES / "invalid" / "non_string_required_sections.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("required_sections" in e for e in result["errors"]))


class TestEmptyRequiredSections(unittest.TestCase):
    """Rule 12: required_sections must not be an empty list."""

    def test_empty_required_sections_is_invalid_schema(self):
        result = validate_file(
            FIXTURES / "invalid" / "empty_required_sections.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("required_sections" in e for e in result["errors"]))


class TestEmptyAcceptanceCriteria(unittest.TestCase):
    """Rule 13: acceptance_criteria must not be an empty list."""

    def test_empty_acceptance_criteria_is_invalid_schema(self):
        result = validate_file(
            FIXTURES / "invalid" / "empty_acceptance_criteria.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("acceptance_criteria" in e for e in result["errors"]))


class TestPlaceholderAcceptanceCriteria(unittest.TestCase):
    """Rule 13: acceptance_criteria entries must be non-empty strings, not
    whitespace-only placeholders."""

    def test_whitespace_only_entry_is_invalid_schema(self):
        result = validate_file(
            FIXTURES / "invalid" / "placeholder_acceptance_criteria.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "INVALID_SCHEMA")
        self.assertTrue(any("acceptance_criteria" in e for e in result["errors"]))


class TestEmptyAuthoritativeSourcesIsValid(unittest.TestCase):
    """Rule 14: an empty authoritative_sources list is explicitly legitimate,
    not a violation — this fixture must PASS, not fail."""

    def test_empty_authoritative_sources_passes(self):
        result = validate_file(
            FIXTURES / "valid" / "empty_authoritative_sources.md", REPO_ROOT
        )
        self.assertEqual(result["result"], "PASS", result["errors"])
        self.assertEqual(result["errors"], [])


class TestGovernedDocumentScope(unittest.TestCase):
    """Rule 15: a path listed in the governed manifest with no front-matter
    is FAIL, not SKIPPED. Uses an explicit governed_manifest override so
    this test does not depend on the real docs/governed-documents.txt
    contents, which may change independently of this rule's logic."""

    def test_governed_path_with_no_frontmatter_fails(self):
        fixture = FIXTURES / "invalid" / "no_frontmatter.md"
        rel = str(fixture.resolve().relative_to(REPO_ROOT.resolve()))
        result = validate_file(fixture, REPO_ROOT, governed_manifest={rel})
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("governed document" in e for e in result["errors"]))

    def test_ungoverned_path_with_no_frontmatter_is_still_skipped(self):
        fixture = FIXTURES / "invalid" / "no_frontmatter.md"
        result = validate_file(fixture, REPO_ROOT, governed_manifest=set())
        self.assertEqual(result["result"], "SKIPPED")
        self.assertEqual(result["errors"], [])

    def test_real_governed_manifest_documents_all_pass(self):
        """Dogfooding, per Amendment D's "no synthetic substitute" rule:
        every real document docs/governed-documents.txt actually lists
        must itself pass, using the real (not overridden) manifest."""
        manifest_path = REPO_ROOT / "docs" / "governed-documents.txt"
        paths = [
            line.strip()
            for line in manifest_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        self.assertTrue(paths, "manifest should not be empty")
        for rel_path in paths:
            result = validate_file(REPO_ROOT / rel_path, REPO_ROOT)
            self.assertEqual(
                result["result"], "PASS", f"{rel_path}: {result['errors']}"
            )


if __name__ == "__main__":
    unittest.main()
