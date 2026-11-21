"""Regression tests for the third native Codex review finding on PR #1
("Restrict heading whitespace to the same line", found on the review
of commit 2ebac4c): src/axiom_validator/parsing.py's HEADING_RE used
`\\s+` to separate the `#` marker from its text. `\\s` matches newlines,
so a bare `#` marker (no text of its own) immediately followed by an
unrelated paragraph — "#\\nRequired\\n" — satisfied a required heading
named "Required", even though the document has no such heading.

Reproduced directly against the actual pre-fix code before this file
was written (not merely asserted): `git show 2ebac4c:src/axiom_validator/parsing.py`,
loaded in isolation, returned `{"Required"}` for
`extract_headings("#\\nRequired\\n")`. The current code returns `set()`
for the same input.

A related, narrower artifact found while verifying this fix's own
required scenarios (not a separate Codex finding): a `#` marker
followed only by trailing whitespace and nothing else ("#  \\n")
previously still matched, capturing a single space character that
`.strip()` then reduced to an empty string — fixed in the same change
by requiring the captured text to start with a non-whitespace
character.

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


class TestBareHashFollowedByTextOnNextLine(unittest.TestCase):
    """Required scenario 1."""

    def test_hash_newline_text_produces_no_heading(self):
        self.assertEqual(extract_headings("#\nRequired\n"), set())


class TestHashWithTrailingSpaceFollowedByTextOnNextLine(unittest.TestCase):
    """Required scenario 2."""

    def test_hash_space_newline_text_produces_no_heading(self):
        self.assertEqual(extract_headings("#  \nRequired\n"), set())


class TestDoubleHashFollowedByTextOnNextLine(unittest.TestCase):
    """Required scenario 3."""

    def test_double_hash_newline_text_produces_no_heading(self):
        self.assertEqual(extract_headings("##\nRequired\n"), set())


class TestValidHeadingUsingASpace(unittest.TestCase):
    """Required scenario 4."""

    def test_space_separated_heading_is_recognised(self):
        self.assertEqual(extract_headings("# Required\n"), {"Required"})


class TestValidHeadingUsingATab(unittest.TestCase):
    """Required scenario 5."""

    def test_tab_separated_heading_is_recognised(self):
        self.assertEqual(extract_headings("#\tRequired\n"), {"Required"})


class TestMultipleValidHeadings(unittest.TestCase):
    """Required scenario 6."""

    def test_multiple_headings_all_recognised(self):
        self.assertEqual(
            extract_headings("# One\n\nSome text.\n\n## Two\n"), {"One", "Two"}
        )


class TestHeadingsInsideFencedCodeBlocksStillExcluded(unittest.TestCase):
    """Required scenario 7 — confirms this fix did not regress the
    separate fenced-code-block exclusion (a different Codex finding,
    fixed earlier in this same file's history)."""

    def test_fenced_heading_still_excluded(self):
        self.assertEqual(
            extract_headings("# Doc\n```\n# Hidden\n```\n"), {"Doc"}
        )


class TestRequiredSectionFailsWhenOnlyMatchOnNextLine(unittest.TestCase):
    """Required scenario 8 — end-to-end through validate_file, not just
    the parsing function, using the exact fixture shape Codex's own
    example used (a bare "#" marker followed by an unrelated
    "Required" paragraph)."""

    def test_fixture_fails_required_section_check(self):
        result = validate_file(
            FIXTURES / "invalid" / "heading_whitespace_next_line.md",
            REPO_ROOT,
            schema_mirror_root=FIXTURES,
        )
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("Required" in e for e in result["errors"]))


class TestOrdinaryDocumentationStillValidatesCorrectly(unittest.TestCase):
    """Required scenario 9 — a real, unschanged document must still
    PASS after this fix; confirms no unintended regression."""

    def test_readme_still_passes(self):
        result = validate_file(REPO_ROOT / "README.md", REPO_ROOT)
        self.assertEqual(result["result"], "PASS", result["errors"])


class TestLineEndingHandling(unittest.TestCase):
    """CRLF coverage, as requested: the trailing `\\s*$` side of the
    pattern was not changed by this fix, but must still behave
    correctly with CRLF line endings."""

    def test_crlf_valid_heading_recognised_without_trailing_cr(self):
        self.assertEqual(extract_headings("# Required\r\n"), {"Required"})

    def test_crlf_bare_hash_then_text_on_next_line_produces_no_heading(self):
        self.assertEqual(extract_headings("#\r\nRequired\r\n"), set())


class TestHashFollowedOnlyByWhitespaceProducesNoHeading(unittest.TestCase):
    """The related, narrower artifact found while verifying scenario 2
    above: a '#' marker followed only by whitespace must contribute no
    heading at all, not an empty string."""

    def test_no_bogus_empty_string_heading(self):
        self.assertEqual(extract_headings("#   \n"), set())


if __name__ == "__main__":
    unittest.main()
