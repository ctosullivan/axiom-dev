#!/usr/bin/env python3
"""Deterministic policy evaluator for the Codex PR-review gate.

Reads a structured review-finding document and the PR's actual current
head SHA, and decides PASS / BLOCK / FAIL_CLOSED. This is the piece of
the Stage 1.3 gate that is fully buildable and testable without live
Codex access or any credentials — see
contracts/codex-gate-policy-evaluator.md for the behavioural contract
this module implements, and
planning/phase-01-foundation.md Stage 1.3 for why this is split from the
live GitHub/Codex integration.

Fails closed: any input that isn't a clean, current, well-formed,
no-P0/P1 review is BLOCK or FAIL_CLOSED, never a silent PASS.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    PASS = "PASS"
    BLOCK = "BLOCK"
    FAIL_CLOSED = "FAIL_CLOSED"


BLOCKING_SEVERITIES = {"P0", "P1"}
REQUIRED_FIELDS = {"schema_version", "pr_head_sha", "status", "findings"}


@dataclass
class EvaluationResult:
    decision: Decision
    reasons: list[str] = field(default_factory=list)
    blocking_findings: list[dict] = field(default_factory=list)
    advisory_findings: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "decision": self.decision.value,
            "reasons": self.reasons,
            "blocking_findings": self.blocking_findings,
            "advisory_findings": self.advisory_findings,
        }


def evaluate(review_json_text: str | None, actual_head_sha: str) -> EvaluationResult:
    """Evaluate a structured review document against policy.

    review_json_text: the raw text that was supposed to be the Codex
      review's structured output. None or empty means the review did not
      run or did not produce output — this fails closed, it never passes
      by default.
    actual_head_sha: the PR's real current head commit SHA, obtained
      independently of the review document (e.g. from the GitHub Actions
      event context), used to detect a stale review of an obsolete commit.
    """
    if review_json_text is None or review_json_text.strip() == "":
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=["No review output was provided (missing or failed review run)."],
        )

    try:
        data = json.loads(review_json_text)
    except json.JSONDecodeError as exc:
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=[f"Review output is not valid JSON: {exc}"],
        )

    if not isinstance(data, dict):
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=["Review output JSON must be an object at the top level."],
        )

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=[f"Review output missing required field(s): {sorted(missing)}"],
        )

    if data["status"] != "completed":
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=[f"Review did not complete (status={data['status']!r})."],
        )

    if data["pr_head_sha"] != actual_head_sha:
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=[
                "Review was run against a different commit than the PR's "
                f"current head (reviewed={data['pr_head_sha']!r}, "
                f"current={actual_head_sha!r}). A passing review of an "
                "obsolete commit does not authorise a later unreviewed "
                "change."
            ],
        )

    findings = data["findings"]
    if not isinstance(findings, list):
        return EvaluationResult(
            decision=Decision.FAIL_CLOSED,
            reasons=["Review output 'findings' must be a list."],
        )

    blocking: list[dict] = []
    advisory: list[dict] = []
    for finding in findings:
        if not isinstance(finding, dict) or "severity" not in finding:
            return EvaluationResult(
                decision=Decision.FAIL_CLOSED,
                reasons=[f"Malformed finding entry: {finding!r}"],
            )
        if finding["severity"] in BLOCKING_SEVERITIES:
            blocking.append(finding)
        else:
            advisory.append(finding)

    if blocking:
        return EvaluationResult(
            decision=Decision.BLOCK,
            reasons=[
                f"{len(blocking)} blocking (P0/P1) finding(s) must be "
                "resolved before merge."
            ],
            blocking_findings=blocking,
            advisory_findings=advisory,
        )

    return EvaluationResult(
        decision=Decision.PASS,
        reasons=["No P0/P1 findings. Advisory findings (if any) are recorded, not blocking."],
        advisory_findings=advisory,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review-file",
        required=True,
        help="Path to the Codex review JSON output. Missing file is treated as a missing/failed review.",
    )
    parser.add_argument(
        "--actual-head-sha",
        required=True,
        help="The PR's real current head commit SHA (not read from the review file).",
    )
    args = parser.parse_args(argv)

    try:
        with open(args.review_file, "r", encoding="utf-8") as fh:
            text: str | None = fh.read()
    except FileNotFoundError:
        text = None

    result = evaluate(text, args.actual_head_sha)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.decision == Decision.PASS else 1


if __name__ == "__main__":
    sys.exit(main())
