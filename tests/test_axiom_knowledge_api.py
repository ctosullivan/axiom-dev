"""get()/find() contract and negative tests, per
`planning/phase-02-knowledge-api-design.md` SS4/SS6 and
`planning/phase-02-stage-2.2-plan.md` SS5.

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
from axiom_knowledge.errors import InvalidQueryError, NotFoundError  # noqa: E402


class GetContractTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_get_nonexistent_id_is_notfound(self):
        with self.assertRaises(NotFoundError):
            ak.get(str(self.repo), "LK-COMPAT-NOPE-001")

    def test_get_native_and_derived_are_kept_visibly_separate(self):
        sup.write_claim(self.repo, "LK-COMPAT-SEP-001", status="proposed")
        result = ak.get(str(self.repo), "LK-COMPAT-SEP-001")
        self.assertIn("native", result)
        self.assertIn("derived", result)
        self.assertEqual(result["native"]["status"], "proposed")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")

    def test_get_accepts_optional_task_id_and_it_is_not_required(self):
        sup.write_claim(self.repo, "LK-COMPAT-TASK-001", status="proposed")
        result = ak.get(str(self.repo), "LK-COMPAT-TASK-001")  # no task_id given
        self.assertEqual(result["id"], "LK-COMPAT-TASK-001")


class FindContractTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)
        sup.write_claim(self.repo, "LK-COMPAT-FIND-001", area="parser.tags.alpha", kind="compatible", status="proposed")
        sup.write_claim(self.repo, "LK-COMPAT-FIND-002", area="parser.tags.beta", kind="extension", status="verified", verified_by="x", verified_date="2026-01-01")
        sup.write_claim(self.repo, "LK-EXT-FIND-003", area="query.tag", kind="extension", status="proposed")

    def test_find_no_matches_returns_empty_list_not_error(self):
        self.assertEqual(ak.find(str(self.repo), "area:nonexistent.area"), [])

    def test_find_exact_id_lookup(self):
        results = ak.find(str(self.repo), "LK-COMPAT-FIND-001")
        self.assertEqual([r["id"] for r in results], ["LK-COMPAT-FIND-001"])

    def test_find_substring_over_area(self):
        results = ak.find(str(self.repo), "tags")
        self.assertEqual(
            sorted(r["id"] for r in results),
            ["LK-COMPAT-FIND-001", "LK-COMPAT-FIND-002"],
        )

    def test_find_field_equality_over_kind(self):
        results = ak.find(str(self.repo), "kind:extension")
        self.assertEqual(
            sorted(r["id"] for r in results),
            ["LK-COMPAT-FIND-002", "LK-EXT-FIND-003"],
        )

    def test_find_field_equality_over_status(self):
        results = ak.find(str(self.repo), "status:verified")
        self.assertEqual([r["id"] for r in results], ["LK-COMPAT-FIND-002"])

    def test_find_malformed_query_empty_string_is_invalid(self):
        with self.assertRaises(InvalidQueryError):
            ak.find(str(self.repo), "")

    def test_find_malformed_query_empty_field_name_is_invalid(self):
        with self.assertRaises(InvalidQueryError):
            ak.find(str(self.repo), ":value")

    def test_find_malformed_query_empty_value_is_invalid(self):
        with self.assertRaises(InvalidQueryError):
            ak.find(str(self.repo), "kind:")

    def test_find_malformed_query_unrecognised_field_is_invalid(self):
        with self.assertRaises(InvalidQueryError):
            ak.find(str(self.repo), "notafield:value")

    def test_find_is_deterministic_across_repeated_calls(self):
        first = ak.find(str(self.repo), "tags")
        second = ak.find(str(self.repo), "tags")
        self.assertEqual(first, second)
        self.assertEqual([r["id"] for r in first], sorted(r["id"] for r in first))


class RealShapeAcceptanceDemonstrationTests(unittest.TestCase):
    """Correction A's positive/negative VERIFIED demonstration, reproduced
    against synthetic fixtures with the exact same field shape as the two
    real claims this stage names (LK-COMPAT-PARSER-TAG-COMMODITY-001,
    LK-COMPAT-QUERY-TAG-001) -- PR 2a itself uses no live Ledgerkit
    checkout (SS2a), so this is the closest this PR gets to that
    demonstration; PR 2b performs it for real, per
    `planning/phase-02-stage-2.2-plan.md` SS4.1/SS4.2.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_positive_verified_demonstration(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-PARSER-TAG-COMMODITY-001",
            area="parser.tags.commodity", kind="compatible", status="verified",
            verified_by="compat-differential-tester (independent dispatch)",
            verified_date="2026-09-25", compatibility_target="1.52.4",
        )
        sup.write_scope_manifest(
            self.repo, "LK-COMPAT-PARSER-TAG-COMMODITY-001", source_pin="1.52.4"
        )
        result = ak.get(str(self.repo), "LK-COMPAT-PARSER-TAG-COMMODITY-001")
        self.assertEqual(result["derived"]["status"], "VERIFIED")
        self.assertIsNotNone(result["derived"]["scope"])

    def test_negative_contrast_same_mechanism(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-QUERY-TAG-001",
            area="query.tag", kind="compatible", status="verified",
            verified_by="compat-differential-tester (independent dispatch)",
            verified_date="2026-09-25", compatibility_target="1.52.4",
        )
        # Deliberately no scope manifest written for this one.
        result = ak.get(str(self.repo), "LK-COMPAT-QUERY-TAG-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertIsNone(result["derived"]["scope"])


if __name__ == "__main__":
    unittest.main()
