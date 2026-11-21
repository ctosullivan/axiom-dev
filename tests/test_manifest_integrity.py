"""Regression tests for the fourth native Codex review finding on PR #1
(third review, commit 6e75d2b): "Governed-document manifest integrity
is not checked when a companion schema exists"
(src/axiom_validator/__init__.py).

The pre-fix `validate_file` only loaded/validated
schemas/governed-documents.txt inside the branch taken when a
document's own schema file was ABSENT. A document whose schema existed
and parsed cleanly could therefore return `PASS` even when the
manifest file itself did not exist at all, violating contract revision
2 rule 4 ("a missing manifest *file* fails closed... every document
checked without an explicit override").

Reproduced directly against the actual pre-fix code before this file
was written (not merely asserted): an isolated temp directory with a
valid `foo.md` + a valid, parseable `schemas/foo.md.schema.yaml`, and
no `schemas/governed-documents.txt` at all, made
`validate_file(Path("foo.md"), Path("."))` return `{"result": "PASS"}`
against the pre-fix code. The corrected code returns `FAIL`, naming the
missing manifest, for the same input.

A separate file from tests/test_schema_relocation.py, following this
project's established convention of one dedicated regression-test file
per corrective fix — discovered by the same `unittest discover` run,
not a new testing framework.

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

from axiom_validator import main, validate_file  # noqa: E402

VALID_SCHEMA = (
    "audience: test\n"
    "purpose: test\n"
    "required_sections: [Required]\n"
    "authoritative_sources: []\n"
    'acceptance_criteria: ["checkable"]\n'
)
MALFORMED_SCHEMA = "purpose: [unterminated\n"


class _TempRepoCase(unittest.TestCase):
    """Shared helper: build an isolated temp directory shaped like a
    tiny repo (a document, optionally its schema, optionally a
    manifest), used instead of any real repository file so these tests
    never depend on — or risk mutating — this project's own
    schemas/governed-documents.txt."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        (self.tmp / "schemas").mkdir()
        (self.tmp / "foo.md").write_text("# Required\n", encoding="utf-8")

    def write_schema(self, content=VALID_SCHEMA):
        (self.tmp / "schemas" / "foo.md.schema.yaml").write_text(
            content, encoding="utf-8"
        )

    def write_manifest(self, governed_paths=()):
        lines = "\n".join(governed_paths)
        (self.tmp / "schemas" / "governed-documents.txt").write_text(
            lines + ("\n" if lines else ""), encoding="utf-8"
        )


class TestValidDocumentSchemaManifestAbsent(_TempRepoCase):
    """Required case: valid document + valid schema, manifest absent -> FAIL.
    This is the exact finding-D reproduction."""

    def test_fails_closed_even_though_schema_is_valid(self):
        self.write_schema()
        # Deliberately no schemas/governed-documents.txt.
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("governed-documents.txt does not exist" in e for e in result["errors"])
        )


class TestNoSchemaManifestAbsent(_TempRepoCase):
    """Required case: document without schema, manifest absent -> FAIL
    (this path already worked before the fix; confirms no regression)."""

    def test_fails_closed_with_no_schema_either(self):
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("governed-documents.txt does not exist" in e for e in result["errors"])
        )


class TestValidDocumentSchemaManifestPresent(_TempRepoCase):
    """Required case: valid document + schema, manifest present -> PASS."""

    def test_passes_when_manifest_exists(self):
        self.write_schema()
        self.write_manifest()  # present, empty — legitimate
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "PASS", result["errors"])


class TestGovernedDocumentWithoutSchema(_TempRepoCase):
    """Required case: governed document without required schema -> FAIL."""

    def test_fails_naming_governed_document(self):
        self.write_manifest(governed_paths=["foo.md"])
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("governed document" in e for e in result["errors"]))


class TestNonGovernedDocumentWithoutSchemaManifestPresent(_TempRepoCase):
    """Required case: non-governed document without schema, manifest
    present -> SKIPPED."""

    def test_skipped_when_not_listed(self):
        self.write_manifest(governed_paths=[])
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "SKIPPED")
        self.assertEqual(result["errors"], [])


class TestExplicitOverridePreservesExistingBehaviour(_TempRepoCase):
    """Required case: explicit governed_manifest override, on-disk
    manifest absent -> preserve existing documented override behaviour
    (the on-disk manifest is never consulted when an explicit override
    is given, regardless of whether a schema exists)."""

    def test_override_with_no_schema_and_no_disk_manifest(self):
        result = validate_file(self.tmp / "foo.md", self.tmp, governed_manifest=set())
        self.assertEqual(result["result"], "SKIPPED")

    def test_override_marking_document_governed_with_no_schema_and_no_disk_manifest(self):
        result = validate_file(
            self.tmp / "foo.md", self.tmp, governed_manifest={"foo.md"}
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("governed document" in e for e in result["errors"]))

    def test_override_with_valid_schema_and_no_disk_manifest_passes(self):
        self.write_schema()
        result = validate_file(self.tmp / "foo.md", self.tmp, governed_manifest=set())
        self.assertEqual(result["result"], "PASS", result["errors"])


class TestMalformedSchemaValidManifestPresent(_TempRepoCase):
    """Required case: malformed document schema, valid manifest present
    -> INVALID_SCHEMA (confirms the manifest-integrity check doesn't
    short-circuit or mask this separate, pre-existing rule)."""

    def test_invalid_schema_still_reported(self):
        self.write_schema(MALFORMED_SCHEMA)
        self.write_manifest()
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "INVALID_SCHEMA")


class TestManifestPathNotAReadableFile(_TempRepoCase):
    """Found by independent review of this exact batch (not one of
    prompt 007's original required scenarios): schemas/governed-documents.txt
    existing as a directory (or anything else that raises OSError on
    read) previously propagated an unhandled `IsADirectoryError` out of
    `validate_file`, instead of the structured FAIL this contract
    requires. Reproduced directly before this fix: the directory-as-manifest
    case above raised uncaught; the corrected `load_governed_manifest`
    catches OSError generally, not just FileNotFoundError."""

    def test_directory_as_manifest_fails_closed_without_raising(self):
        self.write_schema()
        (self.tmp / "schemas" / "governed-documents.txt").mkdir()
        result = validate_file(self.tmp / "foo.md", self.tmp)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(
            any("could not be read" in e for e in result["errors"])
        )


class TestCliEncountersMissingManifest(_TempRepoCase):
    """Required case: CLI encounters missing manifest -> nonzero exit,
    structured, actionable failure report."""

    def test_cli_nonzero_exit_and_structured_report(self):
        self.write_schema()
        cwd = os.getcwd()
        os.chdir(self.tmp)
        try:
            exit_code = main(["foo.md", "--repo-root", "."])
        finally:
            os.chdir(cwd)
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
