"""Regression tests for the fifth native Codex review finding on PR #1:
"check_authoritative_sources() incorrectly accepts an absolute path to
an existing file inside the repository" (src/axiom_validator/rules.py).

Root cause: `(repo_root / source).resolve()` relies on pathlib's `/`
operator, which — when `source` is itself an absolute path — silently
discards `repo_root` and resolves `source` alone (this is documented
pathlib behaviour, not a typo). An absolute path that happens to point
at a real file *inside* the repository then passed both the
repository-containment check and the existence check, so it was wrongly
accepted as if it were a valid bare, repository-relative path —
violating contract rule 5 ("authoritative_sources entries must be bare,
repository-relative paths").

Reproduced directly against the actual pre-fix code before this file
was written (not merely asserted): the pre-fix implementation
(`git show 10dd266:src/axiom_validator/rules.py`, loaded alongside the
current, unchanged parsing.py/reporting.py in an isolated scratch
package) returned `[]` (no errors) for
`check_authoritative_sources({"authoritative_sources": [str(repo_root / "AGENTS.md")]}, repo_root)`.
The corrected code returns a clear rejection for the same input.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from axiom_validator.rules import check_authoritative_sources  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def _check(source):
    return check_authoritative_sources({"authoritative_sources": [source]}, REPO_ROOT)


class TestAbsolutePathInsideRepoToExistingFileRejected(unittest.TestCase):
    """The exact finding-E reproduction: an absolute path to a real
    file inside the repository must be rejected, not wrongly accepted."""

    def test_rejects_absolute_path_to_existing_file(self):
        errors = _check(str(REPO_ROOT / "AGENTS.md"))
        self.assertTrue(errors)
        self.assertTrue(any("not absolute" in e for e in errors))


class TestAbsolutePathInsideRepoToMissingFileRejected(unittest.TestCase):
    """An absolute path inside the repo to a file that doesn't exist
    must still be rejected for being absolute — not fall through to a
    (different) "does not resolve" message, confirming the absoluteness
    check runs before any existence check."""

    def test_rejects_absolute_path_regardless_of_existence(self):
        errors = _check(str(REPO_ROOT / "does-not-exist.md"))
        self.assertTrue(errors)
        self.assertTrue(any("not absolute" in e for e in errors))


class TestAbsolutePathOutsideRepoRejected(unittest.TestCase):
    """An absolute path outside the repository entirely must also be
    rejected as not-a-bare-path — not as an "outside the repository"
    containment failure, which is a different rule for a different
    input shape (a relative path that escapes via ../)."""

    def test_rejects_absolute_path_outside_repo(self):
        errors = _check("/etc/hostname")
        self.assertTrue(errors)
        self.assertTrue(any("not absolute" in e for e in errors))


class TestValidRelativePathStillPasses(unittest.TestCase):
    """Preserve existing behaviour: a genuinely bare, repository-relative
    path to a real file still passes with no errors."""

    def test_valid_relative_path_passes(self):
        self.assertEqual(_check("AGENTS.md"), [])


class TestMissingRelativePathStillDetected(unittest.TestCase):
    """Preserve existing behaviour: missing-path detection for a
    relative path is unaffected by the new absolute-path check."""

    def test_missing_relative_path_still_reported(self):
        errors = _check("does-not-exist.md")
        self.assertTrue(any("does not resolve" in e for e in errors))


class TestAdrReferenceHandlingStillWorks(unittest.TestCase):
    """Preserve existing behaviour: ADR-specific error messages for
    decisions/NNNN-*.md references are unaffected."""

    def test_bad_adr_reference_still_detected(self):
        errors = _check("decisions/9999-does-not-exist.md")
        self.assertTrue(any("ADR" in e and "9999" in e for e in errors))

    def test_valid_adr_reference_still_passes(self):
        self.assertEqual(_check("decisions/0001-development-governance.md"), [])


class TestRelativePathEscapeStillDetected(unittest.TestCase):
    """Preserve existing behaviour: a relative path escaping the
    repository via ../ is still caught by the containment check — a
    different code path from the new absolute-path rejection, since
    this input is never absolute to begin with."""

    def test_relative_escape_still_rejected(self):
        errors = _check("../outside-the-repository.md")
        self.assertTrue(any("outside the repository" in e for e in errors))


class TestEmptyAuthoritativeSourcesStillLegitimate(unittest.TestCase):
    """Preserve existing behaviour: an empty authoritative_sources list
    remains legitimate (contract rule 14), unaffected by this fix."""

    def test_empty_list_passes(self):
        self.assertEqual(
            check_authoritative_sources({"authoritative_sources": []}, REPO_ROOT), []
        )


if __name__ == "__main__":
    unittest.main()
