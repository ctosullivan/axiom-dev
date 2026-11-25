"""The controlled scope-manifest experiment -- authorising prompt part 3B.

Uses the SAME native claim in two isolated scenarios, holding every other
input constant, to demonstrate that the scope manifest itself -- not an
unrelated difference between two claims -- is what causes the change in
derived status. Also covers invalid claim ID, stale source pin, missing
reviewer information and untracked manifests, as required.

Run with:
    PYTHONPATH=src python3 -m unittest discover -s tests -v
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "tests")
import axiom_knowledge_support as sup  # noqa: E402

import axiom_knowledge as ak  # noqa: E402

CLAIM_ID = "LK-COMPAT-SCOPEEXP-001"


def _base_claim(repo):
    return sup.write_claim(
        repo, CLAIM_ID, status="verified",
        verified_by="compat-differential-tester", verified_date="2026-01-01",
        compatibility_target="1.52.4",
    )


class ControlledScopeManifestExperimentTests(unittest.TestCase):
    """Part 3B.1/3B.2: the same native claim, scope manifest present vs
    absent, every other input held constant."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_scenario_1_no_scope_manifest_is_uncertain_with_null_scope(self):
        repo = sup.make_repo(self.tmp_path / "scenario-1")
        _base_claim(repo)
        result = ak.get(str(repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertIsNone(result["derived"]["scope"])

    def test_scenario_2_valid_tracked_reviewed_manifest_is_verified_with_scope(self):
        repo = sup.make_repo(self.tmp_path / "scenario-2")
        _base_claim(repo)
        sup.write_scope_manifest(repo, CLAIM_ID, source_pin="1.52.4", tracked=True)
        result = ak.get(str(repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "VERIFIED")
        self.assertIsNotNone(result["derived"]["scope"])

    def test_the_manifest_is_the_only_variable_between_the_two_scenarios(self):
        repo_absent = sup.make_repo(self.tmp_path / "scenario-absent")
        _base_claim(repo_absent)
        result_absent = ak.get(str(repo_absent), CLAIM_ID)

        repo_present = sup.make_repo(self.tmp_path / "scenario-present")
        _base_claim(repo_present)
        sup.write_scope_manifest(repo_present, CLAIM_ID, source_pin="1.52.4", tracked=True)
        result_present = ak.get(str(repo_present), CLAIM_ID)

        # Everything about the native record itself is identical.
        self.assertEqual(result_absent["native"], result_present["native"])
        # Only the derived status/scope differ, and only because of the manifest.
        self.assertNotEqual(result_absent["derived"]["status"], result_present["derived"]["status"])
        self.assertIsNone(result_absent["derived"]["scope"])
        self.assertIsNotNone(result_present["derived"]["scope"])


class ScopeManifestEdgeCaseTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)
        _base_claim(self.repo)

    def test_invalid_claim_id_in_manifest_is_contested(self):
        sup.write_scope_manifest(
            self.repo, CLAIM_ID, manifest_claim_id="LK-COMPAT-WRONGID-999", source_pin="1.52.4"
        )
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "CONTESTED")

    def test_stale_source_pin_is_contested(self):
        sup.write_scope_manifest(self.repo, CLAIM_ID, source_pin="1.52.3")
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "CONTESTED")

    def test_missing_reviewer_information_is_uncertain_not_contested(self):
        sup.write_scope_manifest(self.repo, CLAIM_ID, reviewed_by=None, reviewed_date=None)
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")

    def test_untracked_manifest_is_uncertain_not_verified(self):
        sup.write_scope_manifest(self.repo, CLAIM_ID, tracked=False)
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")

    def test_manifest_with_no_source_pin_is_not_contested_vacuously(self):
        sup.write_scope_manifest(self.repo, CLAIM_ID, source_pin=None)
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "VERIFIED")

    def test_empty_scope_text_is_uncertain_not_verified(self):
        sup.write_scope_manifest(self.repo, CLAIM_ID, scope="   ")
        result = ak.get(str(self.repo), CLAIM_ID)
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")


if __name__ == "__main__":
    unittest.main()
