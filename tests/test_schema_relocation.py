"""Regression tests for prompt 005's schema-relocation amendment
(decisions/0007): production schemas move from colocated
`<doc>.md.schema.yaml` files to a mirrored tree under a top-level
`schemas/` directory; the governed-document manifest moves to
`schemas/governed-documents.txt`; a missing manifest file fails closed
rather than silently disabling all governed-document enforcement.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from axiom_validator import validate_file  # noqa: E402
from axiom_validator.parsing import (  # noqa: E402
    PathEscapesMirrorRoot,
    doc_path_for_schema,
    schema_path_for,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"


class TestSchemaPathForMirroring(unittest.TestCase):
    """The deterministic <mirror_root>/schemas/<rel>.schema.yaml mapping,
    tested directly against real repository paths."""

    def test_readme_maps_to_top_level_schemas(self):
        self.assertEqual(
            schema_path_for(REPO_ROOT / "README.md", REPO_ROOT),
            REPO_ROOT / "schemas" / "README.md.schema.yaml",
        )

    def test_docs_file_maps_to_mirrored_subdirectory(self):
        self.assertEqual(
            schema_path_for(REPO_ROOT / "docs" / "axiom-validator.md", REPO_ROOT),
            REPO_ROOT / "schemas" / "docs" / "axiom-validator.md.schema.yaml",
        )

    def test_contracts_file_maps_to_mirrored_subdirectory(self):
        self.assertEqual(
            schema_path_for(
                REPO_ROOT / "contracts" / "documentation-schema-validator.md",
                REPO_ROOT,
            ),
            REPO_ROOT
            / "schemas"
            / "contracts"
            / "documentation-schema-validator.md.schema.yaml",
        )

    def test_fixture_maps_under_its_own_mirror_root_not_production_tree(self):
        result = schema_path_for(
            FIXTURES / "invalid" / "bad_adr_reference.md", FIXTURES
        )
        self.assertEqual(
            result, FIXTURES / "schemas" / "invalid" / "bad_adr_reference.md.schema.yaml"
        )
        # And NOT inside the production schemas/ tree:
        self.assertFalse((REPO_ROOT / "schemas" / "tests").exists())

    def test_path_outside_mirror_root_raises(self):
        with self.assertRaises(PathEscapesMirrorRoot):
            schema_path_for(Path("/tmp/not-in-repo.md"), REPO_ROOT)

    def test_symlink_escaping_mirror_root_raises(self):
        """A symlink physically inside the mirror root but pointing to a
        target outside it must not be treated as "inside" — .resolve()
        follows the symlink to its real target before the containment
        check, so this is caught the same way a manipulated relative
        path (../../etc) would be."""
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        repo = tmp / "repo"
        repo.mkdir()
        outside = tmp / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        link = repo / "escape.md"
        os.symlink(outside, link)
        with self.assertRaises(PathEscapesMirrorRoot):
            schema_path_for(link, repo)

    def test_doc_path_for_schema_is_the_exact_inverse(self):
        doc = REPO_ROOT / "docs" / "knowledge-placement.md"
        schema = schema_path_for(doc, REPO_ROOT)
        self.assertEqual(doc_path_for_schema(schema, REPO_ROOT), doc)


class TestMissingManifestFailsClosed(unittest.TestCase):
    """prompt 005 "Manifest integrity": a missing schemas/governed-documents.txt
    file must not silently disable enforcement — every document checked
    without an explicit governed_manifest override must FAIL, not
    SKIPPED, when the manifest file itself does not exist."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_document_with_no_schema_and_no_manifest_file_fails_closed(self):
        doc = self.tmp / "foo.md"
        doc.write_text("# Foo\n", encoding="utf-8")
        # Deliberately no schemas/governed-documents.txt under self.tmp.
        result = validate_file(doc, self.tmp)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("governed-documents.txt does not exist" in e for e in result["errors"])
        )

    def test_explicit_governed_manifest_override_bypasses_the_missing_file_check(self):
        """An explicit override (as every other test in this suite uses)
        is a deliberate bypass of the disk-loading path entirely, not a
        loophole in the fail-closed guarantee — it exists so tests don't
        need a real manifest file to exercise rule 15's logic directly."""
        doc = self.tmp / "foo.md"
        doc.write_text("# Foo\n", encoding="utf-8")
        result = validate_file(doc, self.tmp, governed_manifest=set())
        self.assertEqual(result["result"], "SKIPPED")

    def test_present_but_empty_manifest_is_not_the_missing_case(self):
        """An empty (but present) manifest legitimately means "nothing is
        governed" — this must stay SKIPPED, not FAIL; only an absent
        *file* fails closed."""
        doc = self.tmp / "foo.md"
        doc.write_text("# Foo\n", encoding="utf-8")
        manifest = self.tmp / "schemas" / "governed-documents.txt"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("# nothing governed yet\n", encoding="utf-8")
        result = validate_file(doc, self.tmp)
        self.assertEqual(result["result"], "SKIPPED")


class TestNoStraySchemaFilesOutsideSchemasTree(unittest.TestCase):
    """prompt 005 Sec 6: "Confirm there are no obsolete production
    schemas left alongside Markdown files" after the migration — a
    repo-wide dogfooding check, not a synthetic one."""

    def test_no_schema_file_exists_outside_a_schemas_directory(self):
        stray = []
        for schema_path in REPO_ROOT.rglob("*.md.schema.yaml"):
            if ".git" in schema_path.parts:
                continue
            if "schemas" not in schema_path.parts:
                stray.append(schema_path)
        self.assertEqual(
            stray,
            [],
            f"found .md.schema.yaml file(s) outside any schemas/ directory: {stray}",
        )


class TestGovernedManifestRelocated(unittest.TestCase):
    """The manifest itself must actually be at the new location, and
    nowhere claim to still be at the old one."""

    def test_manifest_exists_at_schemas_path(self):
        self.assertTrue((REPO_ROOT / "schemas" / "governed-documents.txt").exists())

    def test_old_location_no_longer_exists(self):
        self.assertFalse((REPO_ROOT / "docs" / "governed-documents.txt").exists())


if __name__ == "__main__":
    unittest.main()
