"""Event-logging tests: AXIOM_DISABLE_LOGGING opt-out, non-blocking write
failure, task_id propagation, session_id: null -- per
`planning/phase-02-stage-2.2-plan.md` SS2a.3 and SS5's required negative
tests.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, "tests")
import axiom_knowledge_support as sup  # noqa: E402

import axiom_knowledge as ak  # noqa: E402
from axiom_knowledge import events  # noqa: E402


class LoggingOptOutTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)
        sup.write_claim(self.repo, "LK-COMPAT-EVT-001", status="proposed")

    def test_disable_logging_suppresses_knowledge_get_event(self):
        with mock.patch.dict(os.environ, {"AXIOM_DISABLE_LOGGING": "1"}):
            ak.get(str(self.repo), "LK-COMPAT-EVT-001", task_id="t1")
        self.assertFalse((self.repo / ".axiom-local" / "events.jsonl").exists())

    def test_disable_logging_suppresses_knowledge_find_event(self):
        with mock.patch.dict(os.environ, {"AXIOM_DISABLE_LOGGING": "1"}):
            ak.find(str(self.repo), "LK-COMPAT-EVT-001", task_id="t1")
        self.assertFalse((self.repo / ".axiom-local" / "events.jsonl").exists())

    def test_without_opt_out_event_is_written(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AXIOM_DISABLE_LOGGING", None)
            ak.get(str(self.repo), "LK-COMPAT-EVT-001", task_id="t1")
        self.assertTrue((self.repo / ".axiom-local" / "events.jsonl").exists())

    def test_opt_out_does_not_block_the_underlying_read_result(self):
        with mock.patch.dict(os.environ, {"AXIOM_DISABLE_LOGGING": "1"}):
            result = ak.get(str(self.repo), "LK-COMPAT-EVT-001", task_id="t1")
        self.assertEqual(result["id"], "LK-COMPAT-EVT-001")


class LoggingFailureHandlingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)
        sup.write_claim(self.repo, "LK-COMPAT-EVT-002", status="proposed")

    def test_read_only_axiom_local_directory_does_not_block_get(self):
        axiom_local = self.repo / ".axiom-local"
        axiom_local.mkdir()
        axiom_local.chmod(0o500)
        self.addCleanup(axiom_local.chmod, 0o700)
        try:
            result = ak.get(str(self.repo), "LK-COMPAT-EVT-002", task_id="t1")
        finally:
            axiom_local.chmod(0o700)
        self.assertEqual(result["id"], "LK-COMPAT-EVT-002")

    def test_log_event_itself_never_raises_on_write_failure(self):
        axiom_local = self.repo / ".axiom-local"
        axiom_local.mkdir()
        axiom_local.chmod(0o500)
        self.addCleanup(axiom_local.chmod, 0o700)
        try:
            events.log_event(self.repo, "knowledge_get", task_id="t1", result="ok")
        finally:
            axiom_local.chmod(0o700)


class FindEventPayloadTests(unittest.TestCase):
    """Regression for native Codex review of PR #6 (commit 9d23a4f): the
    knowledge_find event must distinguish a zero-match search from a hit,
    and record which claims (if any) were returned, with deterministic
    ordering -- per `planning/phase-02-measurement-design.md` SS0's
    distinction between "API invocation" and "retrieval". A zero-match
    search is a valid, successful result (result: "ok"), not an error:
    retrieval is not evidence of subsequent use."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def _last_event(self):
        lines = (self.repo / ".axiom-local" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        return json.loads(lines[-1])

    def test_zero_results_is_ok_with_empty_claim_list_and_zero_count(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-001", status="proposed", area="parser")
        ak.find(str(self.repo), "area:nonexistent-area", task_id="t1")
        event = self._last_event()
        self.assertEqual(event["result"], "ok")
        self.assertEqual(event["result_count"], 0)
        self.assertEqual(event["returned_claim_ids"], [])

    def test_one_result_records_its_claim_id_and_count_of_one(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-002", status="proposed", area="parser")
        ak.find(str(self.repo), "LK-COMPAT-FIND-002", task_id="t1")
        event = self._last_event()
        self.assertEqual(event["result"], "ok")
        self.assertEqual(event["result_count"], 1)
        self.assertEqual(event["returned_claim_ids"], ["LK-COMPAT-FIND-002"])

    def test_multiple_results_record_all_claim_ids_in_deterministic_order(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-010", status="proposed", area="parser")
        sup.write_claim(self.repo, "LK-COMPAT-FIND-003", status="proposed", area="parser")
        sup.write_claim(self.repo, "LK-COMPAT-FIND-099", status="proposed", area="parser")
        ak.find(str(self.repo), "area:parser", task_id="t1")
        event = self._last_event()
        self.assertEqual(event["result"], "ok")
        self.assertEqual(event["result_count"], 3)
        self.assertEqual(
            event["returned_claim_ids"],
            sorted(["LK-COMPAT-FIND-010", "LK-COMPAT-FIND-003", "LK-COMPAT-FIND-099"]),
        )

    def test_zero_match_search_is_not_logged_as_an_error(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-004", status="proposed", area="parser")
        ak.find(str(self.repo), "area:no-such-area", task_id="t1")
        event = self._last_event()
        self.assertNotEqual(event["result"], "error")
        self.assertNotIn("error_class", event)

    def test_find_event_opt_out_still_covers_the_new_fields(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-005", status="proposed", area="parser")
        with mock.patch.dict(os.environ, {"AXIOM_DISABLE_LOGGING": "1"}):
            ak.find(str(self.repo), "area:parser", task_id="t1")
        self.assertFalse((self.repo / ".axiom-local" / "events.jsonl").exists())

    def test_find_logging_failure_does_not_block_a_zero_match_result(self):
        sup.write_claim(self.repo, "LK-COMPAT-FIND-006", status="proposed", area="parser")
        axiom_local = self.repo / ".axiom-local"
        axiom_local.mkdir()
        axiom_local.chmod(0o500)
        self.addCleanup(axiom_local.chmod, 0o700)
        try:
            results = ak.find(str(self.repo), "area:no-such-area", task_id="t1")
        finally:
            axiom_local.chmod(0o700)
        self.assertEqual(results, [])


class TaskIdAndSessionIdTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_task_id_propagates_through_the_event(self):
        events.log_event(self.repo, "knowledge_get", task_id="abc-123", result="ok")
        lines = (self.repo / ".axiom-local" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(json.loads(lines[0])["task_id"], "abc-123")

    def test_session_id_is_always_null_in_stage_2_2(self):
        events.log_event(self.repo, "task_start", task_id="abc-123", result="ok")
        lines = (self.repo / ".axiom-local" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertIsNone(json.loads(lines[0])["session_id"])

    def test_missing_task_id_is_written_as_null_not_omitted(self):
        events.log_event(self.repo, "knowledge_get", task_id=None, result="ok")
        lines = (self.repo / ".axiom-local" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        event = json.loads(lines[0])
        self.assertIn("task_id", event)
        self.assertIsNone(event["task_id"])


if __name__ == "__main__":
    unittest.main()
