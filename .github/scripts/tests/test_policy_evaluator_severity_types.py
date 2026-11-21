"""Regression tests for prompt 005's correction to severity-type
validation in .github/scripts/policy_evaluator.py.

Native Codex review of PR #1 found that a finding with a non-string
`severity` (e.g. `{"severity": []}`) raised an unhandled `TypeError`
from `finding["severity"] in BLOCKING_SEVERITIES` (membership test
against a set requires a hashable value; a list or dict is not),
instead of the structured `FAIL_CLOSED` the contract requires for
malformed reviewer output. Reproduced directly before this fix (not
merely asserted): `evaluate(json.dumps({...,"findings":[{"severity":
[]}]}), "abc")` raised `TypeError: unhashable type: 'list'` against the
pre-fix code.

A separate file from test_policy_evaluator.py, for the same reason
test_axiom_validator_schema_content.py is separate from
test_axiom_validator.py — new coverage for a corrective change gets its
own file rather than edits scattered through the original suite.

Run with:
    PYTHONPATH=.github/scripts python3 -m unittest discover -s .github/scripts/tests -v
"""
import os
import sys
import unittest
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from policy_evaluator import Decision, evaluate  # noqa: E402


def _review(findings):
    return json.dumps(
        {
            "schema_version": 1,
            "pr_head_sha": "abc123",
            "status": "completed",
            "findings": findings,
        }
    )


class TestMalformedSeverityTypes(unittest.TestCase):
    """Required malformed-severity scenarios: empty list, empty object,
    integer, boolean, null — none may raise; all must FAIL_CLOSED."""

    def test_empty_list_severity(self):
        result = evaluate(_review([{"severity": []}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)
        self.assertTrue(any("severity must be a string" in r for r in result.reasons))

    def test_empty_object_severity(self):
        result = evaluate(_review([{"severity": {}}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_integer_severity(self):
        result = evaluate(_review([{"severity": 1}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_boolean_severity(self):
        result = evaluate(_review([{"severity": True}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_null_severity(self):
        result = evaluate(_review([{"severity": None}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_missing_severity_field(self):
        result = evaluate(_review([{}]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_malformed_finding_object_not_a_dict(self):
        result = evaluate(_review(["not-a-dict"]), "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_result_shape_preserved_on_malformed_severity(self):
        """The FAIL_CLOSED result for a malformed severity must still
        have the documented EvaluationResult shape (contract rule 9) —
        a raised exception would have none of these attributes at all."""
        result = evaluate(_review([{"severity": []}]), "abc123")
        as_dict = result.to_dict()
        self.assertEqual(
            set(as_dict.keys()),
            {"decision", "reasons", "blocking_findings", "advisory_findings"},
        )


class TestCliExitCodeOnMalformedSeverity(unittest.TestCase):
    """The CLI must exit nonzero without an unhandled traceback — the
    pre-fix defect would have crashed main() with a raised TypeError
    instead of printing structured JSON and exiting 1."""

    def test_main_does_not_raise_and_exits_nonzero(self):
        import tempfile

        from policy_evaluator import main

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as fh:
            fh.write(_review([{"severity": []}]))
            review_path = fh.name
        try:
            exit_code = main(["--review-file", review_path, "--actual-head-sha", "abc123"])
        finally:
            os.unlink(review_path)
        self.assertEqual(exit_code, 1)


class TestPreservedCoverage(unittest.TestCase):
    """Preserve existing behaviour alongside the new checks, per prompt
    005 Sec 4's "also preserve coverage of" list."""

    def test_p0_still_blocks(self):
        result = evaluate(_review([{"severity": "P0"}]), "abc123")
        self.assertEqual(result.decision, Decision.BLOCK)

    def test_p1_still_blocks(self):
        result = evaluate(_review([{"severity": "P1"}]), "abc123")
        self.assertEqual(result.decision, Decision.BLOCK)

    def test_advisory_finding_still_non_blocking(self):
        result = evaluate(_review([{"severity": "P3"}]), "abc123")
        self.assertEqual(result.decision, Decision.PASS)
        self.assertEqual(result.advisory_findings, [{"severity": "P3"}])

    def test_missing_reviewer_output_still_fails_closed(self):
        result = evaluate(None, "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_invalid_json_still_fails_closed(self):
        result = evaluate("not json", "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_stale_sha_still_fails_closed(self):
        stale = json.dumps(
            {
                "schema_version": 1,
                "pr_head_sha": "old-sha",
                "status": "completed",
                "findings": [],
            }
        )
        result = evaluate(stale, "new-sha")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_incomplete_review_still_fails_closed(self):
        incomplete = json.dumps(
            {
                "schema_version": 1,
                "pr_head_sha": "abc123",
                "status": "in_progress",
                "findings": [],
            }
        )
        result = evaluate(incomplete, "abc123")
        self.assertEqual(result.decision, Decision.FAIL_CLOSED)

    def test_structured_output_still_machine_readable(self):
        result = evaluate(_review([{"severity": "P3"}]), "abc123")
        as_dict = result.to_dict()
        self.assertIsInstance(as_dict["decision"], str)
        self.assertIsInstance(as_dict["reasons"], list)
        self.assertIsInstance(as_dict["blocking_findings"], list)
        self.assertIsInstance(as_dict["advisory_findings"], list)


if __name__ == "__main__":
    unittest.main()
