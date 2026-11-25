"""Native-register translation tests -- the required set from
`planning/phase-02-knowledge-api-design.md` SS6 and the authorising
prompt's part 3A/4, exercised against synthetic fixtures shaped like
Ledgerkit's real compat-register schema (never a live checkout).

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
from axiom_knowledge.errors import MalformedError, NotFoundError  # noqa: E402
from axiom_knowledge.native_adapter import extract_unresolved_references  # noqa: E402


class StatusMappingTests(unittest.TestCase):
    """3A: proposed -> UNCERTAIN; self-verified -> OBSERVED, never VERIFIED;
    verified without sufficient scoped evidence -> UNCERTAIN; verified with
    valid independently reviewed scope evidence -> VERIFIED; genuinely
    contradictory evidence -> CONTESTED. Missing evidence must not be
    treated as contradictory. Native status is always preserved unchanged.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_proposed_maps_to_uncertain(self):
        sup.write_claim(self.repo, "LK-COMPAT-A-001", status="proposed")
        result = ak.get(str(self.repo), "LK-COMPAT-A-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertEqual(result["native"]["status"], "proposed")

    def test_self_verified_maps_to_observed_never_verified(self):
        sup.write_claim(
            self.repo,
            "LK-COMPAT-B-001",
            status="self-verified",
            verified_by=None,
            verified_date=None,
        )
        result = ak.get(str(self.repo), "LK-COMPAT-B-001")
        self.assertEqual(result["derived"]["status"], "OBSERVED")
        self.assertEqual(result["native"]["status"], "self-verified")

    def test_self_verified_with_scope_manifest_still_observed_not_verified(self):
        # Scope gate must not promote self-verified past OBSERVED even if a
        # scope manifest happens to exist for the same id.
        sup.write_claim(self.repo, "LK-COMPAT-B-002", status="self-verified")
        sup.write_scope_manifest(self.repo, "LK-COMPAT-B-002")
        result = ak.get(str(self.repo), "LK-COMPAT-B-002")
        self.assertEqual(result["derived"]["status"], "OBSERVED")

    def test_verified_without_scope_manifest_is_uncertain_not_verified(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-C-001", status="verified",
            verified_by="compat-differential-tester", verified_date="2026-01-01",
        )
        result = ak.get(str(self.repo), "LK-COMPAT-C-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertIsNone(result["derived"]["scope"])
        self.assertEqual(result["native"]["status"], "verified")

    def test_verified_with_valid_scope_manifest_is_verified(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-D-001", status="verified",
            verified_by="compat-differential-tester", verified_date="2026-01-01",
        )
        sup.write_scope_manifest(self.repo, "LK-COMPAT-D-001")
        result = ak.get(str(self.repo), "LK-COMPAT-D-001")
        self.assertEqual(result["derived"]["status"], "VERIFIED")
        self.assertIsNotNone(result["derived"]["scope"])

    def test_missing_reviewer_metadata_is_uncertain_not_contested(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-E-001", status="verified",
            verified_by=None, verified_date=None,
        )
        result = ak.get(str(self.repo), "LK-COMPAT-E-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")

    def test_conflicting_evidence_is_contested_regardless_of_status(self):
        evidence = [
            {"kind": "executable", "ref": "run A", "pinned_at": "1.52.4", "result": "pass"},
            {"kind": "executable", "ref": "run B", "pinned_at": "1.52.4", "result": "fail"},
        ]
        sup.write_claim(
            self.repo, "LK-COMPAT-F-001", status="verified",
            verified_by="compat-differential-tester", verified_date="2026-01-01",
            evidence=evidence,
        )
        sup.write_scope_manifest(self.repo, "LK-COMPAT-F-001")
        result = ak.get(str(self.repo), "LK-COMPAT-F-001")
        self.assertEqual(result["derived"]["status"], "CONTESTED")

    def test_non_conflicting_evidence_without_result_field_is_unaffected(self):
        # Real Ledgerkit evidence items never carry a result field; this
        # must never be misread as a conflict.
        evidence = [
            {"kind": "manual", "ref": "doc", "pinned_at": "1.52.4"},
            {"kind": "source", "ref": "code", "pinned_at": "1.52.4"},
        ]
        sup.write_claim(
            self.repo, "LK-COMPAT-G-001", status="verified",
            verified_by="compat-differential-tester", verified_date="2026-01-01",
            evidence=evidence,
        )
        sup.write_scope_manifest(self.repo, "LK-COMPAT-G-001")
        result = ak.get(str(self.repo), "LK-COMPAT-G-001")
        self.assertEqual(result["derived"]["status"], "VERIFIED")

    def test_final_status_uses_same_two_gates_as_verified(self):
        sup.write_claim(
            self.repo, "LK-COMPAT-H-001", status="final",
            verified_by="compat-differential-tester", verified_date="2026-01-01",
        )
        result = ak.get(str(self.repo), "LK-COMPAT-H-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        sup.write_scope_manifest(self.repo, "LK-COMPAT-H-001")
        result = ak.get(str(self.repo), "LK-COMPAT-H-001")
        self.assertEqual(result["derived"]["status"], "VERIFIED")

    def test_unrecognised_native_status_is_uncertain_with_translation_gap(self):
        sup.write_claim(self.repo, "LK-COMPAT-I-001", status="exploratory")
        result = ak.get(str(self.repo), "LK-COMPAT-I-001")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertTrue(result["derived"]["translation_gap"])
        self.assertEqual(result["native"]["status"], "exploratory")


class RelationshipMappingTests(unittest.TestCase):
    """3C: superset/subset always carry a mapping_scope; equivalent/
    incomparable never do."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_equivalent_relationship_no_mapping_scope(self):
        sup.write_claim(self.repo, "LK-COMPAT-R-001", relationship="equivalent")
        result = ak.get(str(self.repo), "LK-COMPAT-R-001")
        self.assertEqual(result["derived"]["mapping_result"], "equivalent")
        self.assertIsNone(result["derived"]["mapping_scope"])

    def test_superset_relationship_requires_mapping_scope(self):
        sup.write_claim(self.repo, "LK-COMPAT-R-002", relationship="superset")
        result = ak.get(str(self.repo), "LK-COMPAT-R-002")
        self.assertEqual(result["derived"]["mapping_result"], "equivalent")
        self.assertIsNotNone(result["derived"]["mapping_scope"])

    def test_subset_relationship_requires_mapping_scope(self):
        sup.write_claim(self.repo, "LK-COMPAT-R-003", relationship="subset")
        result = ak.get(str(self.repo), "LK-COMPAT-R-003")
        self.assertEqual(result["derived"]["mapping_result"], "partial")
        self.assertIsNotNone(result["derived"]["mapping_scope"])

    def test_incomparable_relationship_no_mapping_scope(self):
        sup.write_claim(self.repo, "LK-COMPAT-R-004", relationship="incomparable")
        result = ak.get(str(self.repo), "LK-COMPAT-R-004")
        self.assertEqual(result["derived"]["mapping_result"], "divergent")
        self.assertIsNone(result["derived"]["mapping_scope"])

    def test_no_relationship_value_maps_to_unknown(self):
        sup.write_claim(self.repo, "LK-MISMATCH-R-005", relationship=None, kind="unexplained_mismatch")
        result = ak.get(str(self.repo), "LK-MISMATCH-R-005")
        self.assertEqual(result["derived"]["mapping_result"], "unknown")
        self.assertIsNone(result["derived"]["mapping_scope"])

    def test_unrecognised_relationship_value_is_unknown_with_translation_gap(self):
        sup.write_claim(self.repo, "LK-COMPAT-R-006", relationship="novel-future-value")
        result = ak.get(str(self.repo), "LK-COMPAT-R-006")
        self.assertEqual(result["derived"]["mapping_result"], "unknown")
        self.assertTrue(result["derived"]["translation_gap"])

    def test_unrecognised_relationship_forces_overall_status_to_uncertain(self):
        # Regression for native Codex review of PR #6 (commit 6819c45): a
        # verified claim with reviewer metadata AND a passing scope
        # manifest must still be downgraded to UNCERTAIN overall when its
        # relationship value is unrecognised -- knowledge-api-design.md
        # SS6 test 7 names this as one combined rule, not a sub-field-only
        # annotation that leaves derived.status untouched.
        sup.write_claim(
            self.repo, "LK-COMPAT-R-007", relationship="novel-future-value",
            status="verified", verified_by="compat-differential-tester",
            verified_date="2026-01-01",
        )
        sup.write_scope_manifest(self.repo, "LK-COMPAT-R-007")
        result = ak.get(str(self.repo), "LK-COMPAT-R-007")
        self.assertEqual(result["derived"]["status"], "UNCERTAIN")
        self.assertTrue(result["derived"]["translation_gap"])
        self.assertIsNone(result["derived"]["scope"])

    def test_conflicting_evidence_still_takes_precedence_over_relationship_gap(self):
        evidence = [
            {"kind": "executable", "ref": "run A", "pinned_at": "1.52.4", "result": "pass"},
            {"kind": "executable", "ref": "run B", "pinned_at": "1.52.4", "result": "fail"},
        ]
        sup.write_claim(
            self.repo, "LK-COMPAT-R-008", relationship="novel-future-value",
            status="verified", verified_by="compat-differential-tester",
            verified_date="2026-01-01", evidence=evidence,
        )
        result = ak.get(str(self.repo), "LK-COMPAT-R-008")
        self.assertEqual(result["derived"]["status"], "CONTESTED")


class MalformedAndDuplicateTests(unittest.TestCase):
    """Malformed native YAML and duplicate identifiers must be reported as
    a named, non-crashing result, never a silent wrong answer."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = sup.make_repo(self.tmp_path)

    def test_malformed_yaml_raises_malformed_error_not_a_crash(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        bad_path = register_dir / "LK-COMPAT-BAD-001.yaml"
        bad_path.write_text("id: [unterminated\nstatus: proposed\n:::", encoding="utf-8")
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-BAD-001")

    def test_non_mapping_yaml_raises_malformed_error(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-LIST-001.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-LIST-001")

    def test_missing_id_field_raises_malformed_error(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-NOID-001.yaml").write_text("status: proposed\n", encoding="utf-8")
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-NOID-001")

    def test_duplicate_id_raises_malformed_error_naming_both_paths(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        for filename in ("LK-COMPAT-DUP-001.yaml", "LK-COMPAT-DUP-001-copy.yaml"):
            (register_dir / filename).write_text(
                "id: LK-COMPAT-DUP-001\nstatus: proposed\n", encoding="utf-8"
            )
        with self.assertRaises(MalformedError) as ctx:
            ak.get(str(self.repo), "LK-COMPAT-DUP-001")
        self.assertIn("LK-COMPAT-DUP-001-copy.yaml", str(ctx.exception))

    def test_nonexistent_claim_is_notfound_not_malformed(self):
        with self.assertRaises(NotFoundError):
            ak.get(str(self.repo), "LK-COMPAT-NOPE-999")

    def test_non_mapping_upstream_field_raises_malformed_not_a_crash(self):
        # Regression for native Codex review of PR #6 (commit f231b19):
        # `upstream: hledger` (a string, not a mapping) is valid YAML but
        # crashes api._record_to_result's upstream.get(...) with
        # AttributeError instead of failing cleanly as Malformed. Must
        # not break retrieval of a sibling claim in the same register.
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-BADUPSTREAM-001.yaml").write_text(
            "id: LK-COMPAT-BADUPSTREAM-001\nstatus: proposed\nupstream: hledger\n",
            encoding="utf-8",
        )
        sup.write_claim(self.repo, "LK-COMPAT-GOOD-002", status="proposed")
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-BADUPSTREAM-001")
        result = ak.get(str(self.repo), "LK-COMPAT-GOOD-002")
        self.assertEqual(result["id"], "LK-COMPAT-GOOD-002")

    def test_non_mapping_ledgerkit_field_raises_malformed_not_a_crash(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-BADLEDGERKIT-001.yaml").write_text(
            "id: LK-COMPAT-BADLEDGERKIT-001\nstatus: proposed\nledgerkit: equivalent\n",
            encoding="utf-8",
        )
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-BADLEDGERKIT-001")

    def test_find_excludes_a_structurally_malformed_record_without_crashing(self):
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-BADUPSTREAM-002.yaml").write_text(
            "id: LK-COMPAT-BADUPSTREAM-002\narea: parser.example\nstatus: proposed\nupstream: hledger\n",
            encoding="utf-8",
        )
        sup.write_claim(self.repo, "LK-COMPAT-GOOD-003", area="parser.example", status="proposed")
        results = ak.find(str(self.repo), "area:parser.example")
        self.assertEqual([r["id"] for r in results], ["LK-COMPAT-GOOD-003"])

    def test_non_string_id_field_raises_malformed_not_a_crash(self):
        # Regression for native Codex review of PR #6 (commit 6819c45):
        # `id: [bad, id]` is valid YAML but a list is unhashable, so an
        # unguarded dict-membership check on it crashes with TypeError
        # instead of failing cleanly as Malformed. Must not prevent
        # retrieval of other, valid claims in the same register either.
        register_dir = self.repo / "dev-docs" / "compat-register"
        (register_dir / "LK-COMPAT-BADIDTYPE-001.yaml").write_text(
            "id: [bad, id]\nstatus: proposed\n", encoding="utf-8"
        )
        sup.write_claim(self.repo, "LK-COMPAT-GOOD-001", status="proposed")
        with self.assertRaises(MalformedError):
            ak.get(str(self.repo), "LK-COMPAT-BADIDTYPE-001")
        # The malformed record must not break retrieval of a sibling claim.
        result = ak.get(str(self.repo), "LK-COMPAT-GOOD-001")
        self.assertEqual(result["id"], "LK-COMPAT-GOOD-001")


class UnresolvedReferenceTests(unittest.TestCase):
    """SS3f shape-only check: an implementation[]/tests[] entry that does not
    parse into the expected shape produces a diagnostic, not a crash."""

    def test_implementation_entry_without_separator_is_flagged(self):
        native = {"implementation": ["no_separator_here"], "tests": []}
        diagnostics = extract_unresolved_references(native)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["field"], "implementation")

    def test_tests_entry_without_double_colon_is_flagged(self):
        native = {"implementation": [], "tests": ["tests/test_mod.py:single_colon"]}
        diagnostics = extract_unresolved_references(native)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["field"], "tests")

    def test_wellformed_entries_produce_no_diagnostics(self):
        native = {
            "implementation": ["pkg/mod.py:function"],
            "tests": ["tests/test_mod.py::TestClass::test_case"],
        }
        self.assertEqual(extract_unresolved_references(native), [])

    def test_get_surfaces_unresolved_reference_diagnostic_not_a_crash(self):
        with tempfile.TemporaryDirectory() as d:
            repo = sup.make_repo(Path(d))
            sup.write_claim(
                repo, "LK-COMPAT-UNRES-001",
                implementation=["no_separator_here"],
            )
            result = ak.get(str(repo), "LK-COMPAT-UNRES-001")
            self.assertEqual(len(result["diagnostics"]["unresolved_references"]), 1)


if __name__ == "__main__":
    unittest.main()
