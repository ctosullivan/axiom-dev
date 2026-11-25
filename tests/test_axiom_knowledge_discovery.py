"""Repository and register discovery tests -- the six required cases from
the authorising prompt's part 3C, plus the discovery module's own unit
coverage of `planning/phase-02-stage-2.2-plan.md` SS2a.2's five cases.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "tests")
import axiom_knowledge_support as sup  # noqa: E402

from axiom_knowledge.discovery import discover_register_root, discover_repo_root  # noqa: E402
from axiom_knowledge.errors import RegisterNotFoundError, RepositoryNotFoundError  # noqa: E402


class RepoRootDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_case_1_invocation_from_repository_root(self):
        repo = sup.make_repo(self.tmp_path)
        found = discover_repo_root(repo_root=None, start=str(repo))
        self.assertEqual(found, repo.resolve())

    def test_case_2_invocation_from_nested_subdirectory(self):
        repo = sup.make_repo(self.tmp_path)
        nested = repo / "a" / "b" / "c"
        nested.mkdir(parents=True)
        found = discover_repo_root(repo_root=None, start=str(nested))
        self.assertEqual(found, repo.resolve())

    def test_case_3_invocation_outside_any_recognised_repository(self):
        outside = self.tmp_path / "not_adopted"
        outside.mkdir()
        with self.assertRaises(RepositoryNotFoundError):
            discover_repo_root(repo_root=None, start=str(outside))

    def test_case_4_explicit_valid_repo_root(self):
        repo = sup.make_repo(self.tmp_path)
        elsewhere = self.tmp_path / "elsewhere"
        elsewhere.mkdir()
        found = discover_repo_root(repo_root=str(repo), start=str(elsewhere))
        self.assertEqual(found, repo.resolve())

    def test_case_5_explicit_invalid_repo_root(self):
        not_adopted = self.tmp_path / "not_adopted"
        not_adopted.mkdir()
        with self.assertRaises(RepositoryNotFoundError):
            discover_repo_root(repo_root=str(not_adopted))

    def test_explicit_repo_root_overrides_discovery_even_when_cwd_would_resolve(self):
        repo_a = sup.make_repo(self.tmp_path / "a")
        repo_b = sup.make_repo(self.tmp_path / "b")
        found = discover_repo_root(repo_root=str(repo_b), start=str(repo_a))
        self.assertEqual(found, repo_b.resolve())


class RegisterRootDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_register_directive_resolved_relative_to_repo_root(self):
        repo = sup.make_repo(self.tmp_path, register_relative="dev-docs/compat-register")
        register_root = discover_register_root(repo)
        self.assertEqual(register_root, (repo / "dev-docs/compat-register").resolve())

    def test_default_register_location_used_when_no_directive(self):
        repo = sup.make_repo(self.tmp_path, register_relative="knowledge/claims")
        # Rewrite the marker with no register: directive at all.
        (repo / "knowledge" / "README.md").write_text("# Knowledge marker\n", encoding="utf-8")
        register_root = discover_register_root(repo)
        self.assertEqual(register_root, (repo / "knowledge/claims").resolve())

    def test_case_6_recognised_repository_missing_register_directory(self):
        repo = sup.make_repo(self.tmp_path, register_relative="dev-docs/compat-register")
        # Remove the directory the directive names, leaving the marker file.
        (repo / "dev-docs" / "compat-register").rmdir()
        with self.assertRaises(RegisterNotFoundError):
            discover_register_root(repo)

    def test_register_not_found_error_names_the_expected_path(self):
        repo = sup.make_repo(self.tmp_path, register_relative="dev-docs/compat-register")
        (repo / "dev-docs" / "compat-register").rmdir()
        with self.assertRaises(RegisterNotFoundError) as ctx:
            discover_register_root(repo)
        self.assertIn("dev-docs/compat-register", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
