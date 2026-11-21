"""Reporting concerns for the Axiom Dev documentation/knowledge validator:
turning a (result, errors) pair into the report dict shape callers and
tests expect, and formatting a batch of results for the CLI.

Split out of the original monolithic implementation as Stage 1.4's
behaviour-preserving refactor; see planning/phase-01-foundation.md
Stage 1.4.
"""
from __future__ import annotations

import json
from pathlib import Path


def build_report(path: Path, result: str, errors: list[str]) -> dict:
    """The report dict shape: file, result (SKIPPED|INVALID_SCHEMA|PASS|FAIL), errors."""
    return {"file": str(path), "result": result, "errors": errors}


def format_results(results: list[dict]) -> str:
    """Render a batch of reports as indented JSON for the CLI."""
    return json.dumps(results, indent=2)


def exit_code_for(results: list[dict]) -> int:
    """0 if every result is PASS/SKIPPED, 1 if any is FAIL/INVALID_SCHEMA."""
    return 1 if any(r["result"] in ("FAIL", "INVALID_SCHEMA") for r in results) else 0
