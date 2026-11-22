"""Tests for ci_required_gate.py — the `ci-required` aggregate CI gate.

Found missing by native Codex review of PR #4 (P1: "Add deterministic
regression tests for the aggregate gate" — a repository-wide search for
`ci-required`/`NEEDS_JSON` found only the workflow and documentation, no
committed test exercised the predicate; AGENTS.md Sec 8 requires a
deterministic test for every behavioural change). Covers success, failure,
skipped and cancelled dependency results, and verifies the four jobs this
gate actually depends on in the real workflow file, not just in this
module's own `REQUIRED_JOBS` constant.

Run with:
    PYTHONPATH=.github/scripts python3 -m unittest discover -s .github/scripts/tests -v
"""
import contextlib
import io
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ci_required_gate import REQUIRED_JOBS, find_nonpassing, main  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "deterministic-checks.yml"


def _needs(**results):
    """Build a NEEDS_JSON-shaped dict: {job: {"result": "<status>"}}."""
    return {job: {"result": status} for job, status in results.items()}


class TestFindNonpassingSuccessCase(unittest.TestCase):
    """All four dependencies succeeded -> no nonpassing jobs."""

    def test_all_success_is_empty(self):
        needs = _needs(
            **{job: "success" for job in sorted(REQUIRED_JOBS)}
        )
        self.assertEqual(find_nonpassing(needs), {})


class TestFindNonpassingFailureCase(unittest.TestCase):
    """A real job failure is reported, naming the job and its result."""

    def test_single_failure_detected(self):
        needs = _needs(
            **{job: "success" for job in sorted(REQUIRED_JOBS)}
        )
        needs["axiom-validator-tests"] = {"result": "failure"}
        self.assertEqual(
            find_nonpassing(needs), {"axiom-validator-tests": "failure"}
        )


class TestFindNonpassingSkippedCase(unittest.TestCase):
    """A skipped dependency fails the gate, not just an outright failure."""

    def test_skipped_detected(self):
        needs = _needs(
            **{job: "success" for job in sorted(REQUIRED_JOBS)}
        )
        needs["no-trailing-whitespace"] = {"result": "skipped"}
        self.assertEqual(
            find_nonpassing(needs), {"no-trailing-whitespace": "skipped"}
        )


class TestFindNonpassingCancelledCase(unittest.TestCase):
    """A cancelled dependency fails the gate."""

    def test_cancelled_detected(self):
        needs = _needs(
            **{job: "success" for job in sorted(REQUIRED_JOBS)}
        )
        needs["policy-evaluator-tests"] = {"result": "cancelled"}
        self.assertEqual(
            find_nonpassing(needs), {"policy-evaluator-tests": "cancelled"}
        )


class TestFindNonpassingMultipleFailures(unittest.TestCase):
    """More than one non-success dependency is reported together, not
    just the first one found."""

    def test_multiple_nonpassing_all_reported(self):
        needs = _needs(
            **{job: "success" for job in sorted(REQUIRED_JOBS)}
        )
        needs["validate-governed-documentation"] = {"result": "failure"}
        needs["no-trailing-whitespace"] = {"result": "cancelled"}
        self.assertEqual(
            find_nonpassing(needs),
            {
                "validate-governed-documentation": "failure",
                "no-trailing-whitespace": "cancelled",
            },
        )


class TestMainExitCode(unittest.TestCase):
    """main() wires find_nonpassing() to a process exit code, via the
    same NEEDS_JSON environment variable the workflow actually sets."""

    def _run_main(self, needs_json: str) -> int:
        with mock.patch.dict(os.environ, {"NEEDS_JSON": needs_json}):
            with contextlib.redirect_stdout(io.StringIO()):
                return main([])

    def test_all_success_exits_zero(self):
        import json

        needs = _needs(**{job: "success" for job in sorted(REQUIRED_JOBS)})
        self.assertEqual(self._run_main(json.dumps(needs)), 0)

    def test_any_nonpassing_exits_nonzero(self):
        import json

        needs = _needs(**{job: "success" for job in sorted(REQUIRED_JOBS)})
        needs["axiom-validator-tests"] = {"result": "failure"}
        self.assertEqual(self._run_main(json.dumps(needs)), 1)


class TestRequiredJobsMatchActualWorkflow(unittest.TestCase):
    """Verify all four required jobs remain dependencies in the real
    workflow file — not just asserted by this module's own constant,
    which could silently drift from the actual YAML."""

    def setUp(self):
        self.workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    def test_ci_required_job_exists(self):
        self.assertIn("ci-required", self.workflow["jobs"])

    def test_ci_required_depends_on_exactly_the_required_jobs(self):
        needs = self.workflow["jobs"]["ci-required"]["needs"]
        self.assertEqual(set(needs), set(REQUIRED_JOBS))

    def test_ci_required_runs_even_if_a_dependency_failed(self):
        # "always()" is what makes the gate itself run (and therefore be
        # able to report) even when an upstream job failed/was skipped —
        # without it, GitHub would skip ci-required entirely on any
        # upstream failure, and a skipped required check does not block
        # merge the way a failed one does.
        condition = self.workflow["jobs"]["ci-required"].get("if", "")
        self.assertIn("always()", condition)

    def test_every_required_job_is_an_actual_job_in_the_workflow(self):
        # Catches the opposite drift: a job renamed/removed from the
        # workflow but left in REQUIRED_JOBS, which would make this
        # module's own tests pass while the real gate silently stopped
        # depending on it.
        for job in REQUIRED_JOBS:
            self.assertIn(job, self.workflow["jobs"])


if __name__ == "__main__":
    unittest.main()
