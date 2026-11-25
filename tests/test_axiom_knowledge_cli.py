"""CLI argument parsing and machine-readable output tests.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "tests")
import axiom_knowledge_support as sup  # noqa: E402

from axiom_knowledge.cli import main  # noqa: E402


class CLITests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)
        sup.write_claim(self.repo, "LK-COMPAT-CLI-001", status="proposed")

    def _run(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_get_via_repo_root_flag_prints_json_result(self):
        code, out, _ = self._run("--repo-root", str(self.repo), "get", "LK-COMPAT-CLI-001")
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        self.assertEqual(parsed["id"], "LK-COMPAT-CLI-001")
        self.assertEqual(parsed["derived"]["status"], "UNCERTAIN")

    def test_get_nonexistent_id_exits_nonzero_with_named_json_error(self):
        code, _, err = self._run("--repo-root", str(self.repo), "get", "LK-COMPAT-NOPE-999")
        self.assertEqual(code, 1)
        parsed = json.loads(err)
        self.assertEqual(parsed["error"], "NotFoundError")

    def test_repo_root_outside_any_adopted_repository_is_named_error(self):
        outside = self.tmp_path / "outside"
        outside.mkdir()
        code, _, err = self._run("--repo-root", str(outside), "get", "anything")
        self.assertEqual(code, 1)
        parsed = json.loads(err)
        self.assertEqual(parsed["error"], "RepositoryNotFoundError")

    def test_find_prints_json_list(self):
        code, out, _ = self._run("--repo-root", str(self.repo), "find", "LK-COMPAT-CLI-001")
        self.assertEqual(code, 0)
        parsed = json.loads(out)
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["id"], "LK-COMPAT-CLI-001")

    def test_task_start_requires_task_id_argument(self):
        with self.assertRaises(SystemExit):
            self._run("--repo-root", str(self.repo), "task-start")

    def test_task_start_and_task_accepted_ack(self):
        code, out, _ = self._run("--repo-root", str(self.repo), "task-start", "--task-id", "demo-task")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["task_id"], "demo-task")

        code, out, _ = self._run("--repo-root", str(self.repo), "task-accepted", "--task-id", "demo-task")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["task_id"], "demo-task")

    def test_get_with_unquoted_yaml_date_serializes_cleanly(self):
        # Regression for native Codex review of PR #6 (commit 6819c45):
        # yaml.safe_load parses an unquoted date scalar into a
        # datetime.date, which json.dumps cannot serialize by default.
        # schema.md's own illustration shows verified_date unquoted, so
        # a real consumer entry could easily hit this.
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-DATE-001.yaml").write_text(
            "id: LK-COMPAT-DATE-001\n"
            "status: verified\n"
            "verified_by: tester\n"
            "verified_date: 2026-11-25\n",  # deliberately unquoted
            encoding="utf-8",
        )
        code, out, err = self._run("--repo-root", str(self.repo), "get", "LK-COMPAT-DATE-001")
        self.assertEqual(code, 0, msg=err)
        parsed = json.loads(out)
        self.assertEqual(parsed["native"]["verified_date"], "2026-11-25")

    def test_task_id_propagates_into_the_event_log(self):
        self._run("--repo-root", str(self.repo), "get", "LK-COMPAT-CLI-001", "--task-id", "demo-task")
        events_path = self.repo / ".axiom-local" / "events.jsonl"
        lines = events_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(lines), 1)
        event = json.loads(lines[0])
        self.assertEqual(event["task_id"], "demo-task")
        self.assertIsNone(event["session_id"])
        self.assertEqual(event["event_type"], "knowledge_get")


if __name__ == "__main__":
    unittest.main()
