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
