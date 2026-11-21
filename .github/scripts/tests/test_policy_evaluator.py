"""Tests for policy_evaluator.py against contracts/codex-gate-policy-evaluator.md.

Run with:
    PYTHONPATH=.github/scripts python3 -m unittest discover -s .github/scripts/tests -v

No pytest dependency — this repository has none installed, and stdlib
unittest is sufficient for a module with no external dependencies
(Amendment A: prefer conventional tools, avoid adding a dependency this
repo would then have to maintain just to run its own tests).

Each test method names the prompt-002 Sec 6 Stage 1.3 scenario and/or
contract rule it demonstrates.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from policy_evaluator import Decision, evaluate  # noqa: E402

HEAD = "abc123def456"


def review(**overrides):
    base = {
        "schema_version": "1",
        "pr_head_sha": HEAD,
        "status": "completed",
        "findings": [],
    }
    base.update(overrides)
    return json.dumps(base)


class TestValidPR(unittest.TestCase):
    """Contract rule 8; prompt 002 Sec 6 Stage 1.3 scenario 'Valid PR'."""

    def test_clean_review_passes(self):
        result = evaluate(review(findings=[]), HEAD)
        self.assertEqual(result.decision, Decision.PASS)
        self.assertEqual(result.blocking_findings, [])
        self.assertEqual(result.advisory_findings, [])


class TestP0P1Defect(unittest.TestCase):
    """Contract rule 7; scenario 'Known P0/P1 defect'."""

    def test_p1_finding_blocks(self):
        result = evaluate(
            review(findings=[{"severity": "P1", "title": "SQL injection"}]), HEAD
        )
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(len(result.blocking_findings), 1)

    def test_p0_and_advisory_mixed_still_blocks_and_lists_both(self):
        result = evaluate(
            review(
                findings=[
                    {"severity": "P0", "title": "RCE"},
                    {"severity": "advisory", "title": "naming nit"},
                ]
            ),
            HEAD,
        )
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(len(result.blocking_findings), 1)
        self.assertEqual(len(result.advisory_findings), 1)


class TestAdvisoryFinding(unittest.TestCase):
    """Contract rule 8; scenario 'Advisory finding' — recorded, not blocking."""

    def test_advisory_only_passes_but_is_recorded(self):
        result = evaluate(
            review(findings=[{"severity": "P2", "title": "could simplify"}]), HEAD
        )
        self.assertEqual(result.decision, Decision.PASS)
        self.assertEqual(len(result.advisory_findings), 1)


class TestMalformedReviewerOutput(unittest.TestCase):
    """Contract rules 2, 3, 6; scenario 'Malformed reviewer output'."""

    def test_invalid_json_fails_closed(self):
        result = evaluate("{not valid json", HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_json_not_an_object_fails_closed(self):
        result = evaluate("[1, 2, 3]", HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_missing_required_field_fails_closed(self):
        data = json.loads(review())
        del data["pr_head_sha"]
        result = evaluate(json.dumps(data), HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_findings_not_a_list_fails_closed(self):
        result = evaluate(review(findings="none"), HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_finding_entry_without_severity_fails_closed(self):
        result = evaluate(review(findings=[{"title": "no severity field"}]), HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)


class TestMissingOrFailedReview(unittest.TestCase):
    """Contract rules 1, 4; scenario 'Missing or failed review'."""

    def test_none_fails_closed(self):
        result = evaluate(None, HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_empty_string_fails_closed(self):
        result = evaluate("", HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_whitespace_only_fails_closed(self):
        result = evaluate("   \n  ", HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_status_errored_fails_closed(self):
        result = evaluate(review(status="error"), HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)


class TestStaleCommitReview(unittest.TestCase):
    """Contract rule 5; scenario 'Review of an outdated commit'."""

    def test_sha_mismatch_fails_closed(self):
        result = evaluate(review(pr_head_sha="old-sha-000"), HEAD)
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)
        self.assertIn("old-sha-000", result.reasons[0])
        self.assertIn(HEAD, result.reasons[0])

    def test_matching_sha_does_not_fail_on_staleness_rule(self):
        # Sanity check: same scenario shape but matching SHA should not
        # trip the staleness rule (it may still PASS or BLOCK depending
        # on findings, but never FAIL_CLOSED for staleness specifically).
        result = evaluate(review(pr_head_sha=HEAD, findings=[]), HEAD)
        self.assertEqual(result.decision, Decision.PASS)


class TestOutputShape(unittest.TestCase):
    """Contract rule 9 — output is always structured, never bare text."""

    def test_to_dict_has_required_keys(self):
        result = evaluate(review(), HEAD)
        d = result.to_dict()
        self.assertEqual(
            set(d.keys()),
            {"decision", "reasons", "blocking_findings", "advisory_findings"},
        )


if __name__ == "__main__":
    unittest.main()
