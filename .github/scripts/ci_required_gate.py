#!/usr/bin/env python3
"""Deterministic aggregate-gate logic for `.github/workflows/deterministic-checks.yml`'s
`ci-required` job.

Extracted from that job's previously-inline Python (found by native Codex
review of PR #4 to have zero committed regression coverage — see
`planning/phase-02-planning-review.md` and AGENTS.md Sec 8's "every
behavioural change needs a deterministic test" requirement) so the exact
predicate deciding merge-gate pass/fail is testable without running GitHub
Actions. Behaviour is unchanged: `needs` is a GitHub Actions `needs`
context (one entry per dependent job, each with a `result` field), and any
dependent job whose `result` is not `"success"` (covers `failure`,
`skipped`, and `cancelled` alike) fails the gate.

Run the tests with:
    PYTHONPATH=.github/scripts python3 -m unittest discover -s .github/scripts/tests -v
"""
from __future__ import annotations

import json
import os
import sys

REQUIRED_JOBS = frozenset(
    {
        "policy-evaluator-tests",
        "axiom-validator-tests",
        "validate-governed-documentation",
        "no-trailing-whitespace",
    }
)


def find_nonpassing(needs: dict[str, dict[str, str]]) -> dict[str, str]:
    """Return {job: result} for every dependent job whose result isn't "success"."""
    return {job: info["result"] for job, info in needs.items() if info["result"] != "success"}


def main(argv: list[str] | None = None) -> int:
    del argv  # input comes from NEEDS_JSON, matching the workflow's own env wiring
    needs = json.loads(os.environ["NEEDS_JSON"])
    nonpassing = find_nonpassing(needs)
    for job, info in needs.items():
        print(f"{job}: {info['result']}")
    if nonpassing:
        print("Required CI dependencies did not all succeed:", nonpassing)
        return 1
    print("All required CI dependencies succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
