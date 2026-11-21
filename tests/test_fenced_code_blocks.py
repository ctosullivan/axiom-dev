"""Regression tests for prompt 005's correction to fenced-code-block
handling in heading extraction (src/axiom_validator/parsing.py).

Native Codex review of PR #1 found that the original implementation's
code-fence stripping only recognised exactly-three-backtick fences, so
a required heading hidden inside a tilde-fenced or 4-plus-backtick-fenced
example could wrongly count as present. Reproduced directly against the
pre-fix implementation before writing this file (not merely asserted):
`git show 3a8c395:src/axiom_validator/parsing.py`'s `extract_headings`
returns `{'Required', ...}` for a document containing only a
`~~~`-fenced "# Required" example; the corrected implementation in this
commit returns a set that excludes it.

A separate file from tests/test_axiom_validator.py — not for checksum
protection (that convention no longer applies, decisions/0006/0007) but
because these are pure-function tests of `parsing.extract_headings`
directly, not of `validate_file`'s full pipeline, except for the one
fixture-based end-to-end test at the end (required scenario 9).

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from axiom_validator import validate_file  # noqa: E402
from axiom_validator.parsing import extract_headings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"


class TestThreeBacktickFence(unittest.TestCase):
    """Required scenario 1."""

    def test_heading_inside_three_backtick_fence_excluded(self):
        text = "# Doc\n```\n# Hidden\n```\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestFourBacktickFence(unittest.TestCase):
    """Required scenario 2."""

    def test_heading_inside_four_backtick_fence_excluded(self):
        text = "# Doc\n````\n# Hidden\n````\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestLongerBacktickFence(unittest.TestCase):
    """Required scenario 3."""

    def test_heading_inside_five_backtick_fence_excluded(self):
        text = "# Doc\n`````\n# Hidden\n`````\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestTildeFence(unittest.TestCase):
    """Required scenario 4 — the exact shape Codex's own example used."""

    def test_heading_inside_tilde_fence_excluded(self):
        text = "# Doc\n~~~markdown\n# Hidden\n~~~\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestClosingFenceLongerThanOpening(unittest.TestCase):
    """Required scenario 5: a closing fence at least as long as the
    opening still closes it."""

    def test_longer_closing_fence_still_closes(self):
        text = "# Doc\n```\n# Hidden\n````\n# Real\n"
        self.assertEqual(extract_headings(text), {"Doc", "Real"})

    def test_shorter_closing_candidate_does_not_close(self):
        # A 3-backtick line cannot close a 4-backtick-opened fence —
        # everything after it, including the next heading-looking line,
        # stays inside the (still open) fence.
        text = "# Doc\n````\n# Hidden\n```\n# AlsoHidden\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestUnclosedFence(unittest.TestCase):
    """Required scenario 6: an unterminated fence consumes the rest of
    the document, same as CommonMark."""

    def test_unclosed_fence_hides_everything_after(self):
        text = "# Doc\n```\n# Hidden\n# StillHidden\n"
        self.assertEqual(extract_headings(text), {"Doc"})


class TestRealHeadingOutsideFence(unittest.TestCase):
    """Required scenario 7."""

    def test_plain_heading_with_no_fence_at_all(self):
        text = "# Real\n\nSome text.\n"
        self.assertEqual(extract_headings(text), {"Real"})


class TestMixedRealAndFencedHeadings(unittest.TestCase):
    """Required scenario 8."""

    def test_mixed_document(self):
        text = "# Real\n```\n# Fake\n```\n## AlsoReal\n~~~\n### AlsoFake\n~~~\n"
        self.assertEqual(extract_headings(text), {"Real", "AlsoReal"})


class TestOnlyMatchingHeadingInsideFenceFailsValidation(unittest.TestCase):
    """Required scenario 9: end-to-end through validate_file, not just
    the parsing function — the document's only "Required" heading is
    inside a tilde fence, so the document must FAIL, naming it missing."""

    def test_fixture_fails_required_section_check(self):
        result = validate_file(
            FIXTURES / "invalid" / "heading_only_in_tilde_fence.md",
            REPO_ROOT,
            schema_mirror_root=FIXTURES,
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("Required" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
