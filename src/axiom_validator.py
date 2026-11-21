#!/usr/bin/env python3
"""Axiom Dev documentation/knowledge validator — initial implementation.

Implements contracts/documentation-schema-validator.md. Deliberately
monolithic: parsing, rule-checking, and reporting all live in one
function here, so Stage 1.4's planned refactor (splitting these
concerns) is a real structural change to verify, not a renamed copy of
this file. See planning/phase-01-foundation.md Stage 1.4.

Requires PyYAML (not vendored — a conventional, widely available
dependency; see requirements.txt).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REQUIRED_FIELDS = {
    "audience",
    "purpose",
    "required_sections",
    "authoritative_sources",
    "acceptance_criteria",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCED_CODE_BLOCK_RE = re.compile(r"^```[^\n]*\n.*?\n```[ \t]*$", re.DOTALL | re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
ADR_PATH_RE = re.compile(r"decisions/(\d+)-[^/]*\.md$")


def _is_within(resolved: Path, root: Path) -> bool:
    """True if `resolved` is `root` or a descendant of it.

    Added after independent review found that a path with enough `../`
    segments to escape the repository (e.g. into the filesystem outside
    it) was reported PASS as long as it happened to exist — contract
    rules 5/6 require rejecting such paths outright, existent or not.
    """
    try:
        resolved.relative_to(root)
        return True
    except ValueError:
        return False


def validate_file(path: Path, repo_root: Path) -> dict:
    """Validate one Markdown file against its own declared schema.

    Returns a dict with keys: file, result (SKIPPED|INVALID_SCHEMA|PASS|FAIL),
    errors (list of human-readable strings).
    """
    text = path.read_text(encoding="utf-8")

    match = FRONTMATTER_RE.match(text)
    if not match:
        return {"file": str(path), "result": "SKIPPED", "errors": []}

    frontmatter_text = match.group(1)
    body = text[match.end():]

    try:
        data = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        return {
            "file": str(path),
            "result": "INVALID_SCHEMA",
            "errors": [f"invalid YAML front-matter: {exc}"],
        }

    if not isinstance(data, dict):
        return {
            "file": str(path),
            "result": "INVALID_SCHEMA",
            "errors": ["front-matter must be a YAML mapping (object)"],
        }

    missing_fields = REQUIRED_FIELDS - data.keys()
    if missing_fields:
        return {
            "file": str(path),
            "result": "INVALID_SCHEMA",
            "errors": [f"missing required field(s): {sorted(missing_fields)}"],
        }

    errors: list[str] = []
    body_without_code = INLINE_CODE_RE.sub("", body)

    # Rule 4: required_sections — a heading at any level matching the
    # exact text must appear somewhere in the body. Fenced code blocks
    # are excluded first: independent review found that a `#`-prefixed
    # line inside a ``` fenced example was being counted as a real
    # heading, a false positive the contract gives no exemption for.
    body_without_fences = FENCED_CODE_BLOCK_RE.sub("", body)
    present_headings = {h.strip() for h in HEADING_RE.findall(body_without_fences)}
    missing_headings = [
        heading
        for heading in data["required_sections"]
        if heading not in present_headings
    ]
    if missing_headings:
        errors.append(f"missing required section(s): {missing_headings}")

    # Rule 5: authoritative_sources — bare paths resolving from repo
    # root, and (per independent review) must not escape the repository
    # via `../` even if the resolved target happens to exist.
    for source in data["authoritative_sources"]:
        if not isinstance(source, str) or "§" in source or source.strip() != source:
            errors.append(
                f"authoritative_sources entry is not a bare path: {source!r}"
            )
            continue
        resolved = (repo_root / source).resolve()
        if not _is_within(resolved, repo_root):
            errors.append(
                f"authoritative_sources path resolves outside the repository: {source!r}"
            )
        elif not resolved.exists():
            adr_match = ADR_PATH_RE.search(source)
            if adr_match:
                errors.append(
                    f"authoritative_sources references a non-existent ADR "
                    f"number {adr_match.group(1)!r}: {source!r}"
                )
            else:
                errors.append(
                    f"authoritative_sources path does not resolve: {source!r}"
                )

    # Rules 6/7: body Markdown relative links resolving from the
    # document's own location, also required to stay within the
    # repository; a resolved-or-unresolved decisions/ path gets
    # ADR-specific error detail either way.
    for link in LINK_RE.findall(body_without_code):
        if link.startswith("http://") or link.startswith("https://"):
            continue
        link_path = link.split("#")[0]
        if not link_path:
            continue
        resolved = (path.parent / link_path).resolve()
        if not _is_within(resolved, repo_root):
            errors.append(f"link resolves outside the repository: {link!r}")
        elif not resolved.exists():
            adr_match = ADR_PATH_RE.search(link_path)
            if adr_match:
                errors.append(
                    f"body link references a non-existent ADR number "
                    f"{adr_match.group(1)!r}: {link!r}"
                )
            else:
                errors.append(f"broken link: {link!r}")

    result = "FAIL" if errors else "PASS"
    return {"file": str(path), "result": result, "errors": errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown files to validate.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root that authoritative_sources paths resolve against.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    results = [validate_file(Path(p), repo_root) for p in args.paths]
    print(json.dumps(results, indent=2))
    return 1 if any(r["result"] == "FAIL" or r["result"] == "INVALID_SCHEMA" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
