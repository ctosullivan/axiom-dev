"""Axiom Dev documentation/knowledge validator — package entry point.

Implements contracts/documentation-schema-validator.md. This is the
Stage 1.4 behaviour-preserving refactor of what was originally one
monolithic file (src/axiom_validator.py) into separate parsing
(parsing.py), rule-checking (rules.py), and reporting (reporting.py)
modules. See planning/phase-01-foundation.md Stage 1.4 and
evidence/stage-1.4-baseline.md for the before/after verification this
refactor was checked against.

Public API, unchanged by the refactor: validate_file(path, repo_root)
and main(argv) — the same names, same signatures, same return shapes
that tests/test_axiom_validator.py already imports and asserts against,
checksum-protected and untouched by this change.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import parsing, reporting, rules


def validate_file(path: Path, repo_root: Path, governed_manifest: set[str] | None = None) -> dict:
    """Validate one Markdown file against its own declared schema.

    Returns a dict with keys: file, result (SKIPPED|INVALID_SCHEMA|PASS|FAIL),
    errors (list of human-readable strings).

    governed_manifest: repository-relative paths that must carry a schema
    (contract rule 15, prompt 003 Amendment C). Defaults to the real
    docs/governed-documents.txt manifest when not given; tests may pass
    an explicit set to exercise the rule without real repository files.

    repo_root is resolved internally (callers may pass an unresolved
    relative path, e.g. Path(".")) — found necessary by independent
    review: the containment check (rules.is_within) compares a resolved
    absolute path against repo_root, which only works if repo_root is
    itself resolved. This was a latent defect present identically in the
    pre-refactor monolith (not introduced by the Stage 1.4 refactor),
    masked because every existing caller (the CLI, the test suite)
    happened to already pass a resolved repo_root.
    """
    repo_root = repo_root.resolve()
    text = path.read_text(encoding="utf-8")

    try:
        frontmatter_text, body = parsing.split_frontmatter(text)
    except parsing.NoFrontmatter:
        manifest = (
            rules.load_governed_manifest(repo_root)
            if governed_manifest is None
            else governed_manifest
        )
        try:
            rel = str(path.resolve().relative_to(repo_root.resolve()))
        except ValueError:
            rel = str(path)
        if rel in manifest:
            return reporting.build_report(
                path,
                "FAIL",
                [f"{rel} is a governed document ({rules.GOVERNED_MANIFEST_PATH}) with no front-matter schema"],
            )
        return reporting.build_report(path, "SKIPPED", [])

    try:
        data = parsing.parse_frontmatter(frontmatter_text)
    except parsing.FrontmatterParseError as exc:
        return reporting.build_report(path, "INVALID_SCHEMA", [exc.message])

    missing_field_errors = rules.check_required_fields(data)
    if missing_field_errors:
        return reporting.build_report(path, "INVALID_SCHEMA", missing_field_errors)

    type_content_errors = rules.check_field_types_and_content(data)
    if type_content_errors:
        return reporting.build_report(path, "INVALID_SCHEMA", type_content_errors)

    errors: list[str] = []
    present_headings = parsing.extract_headings(body)
    errors.extend(rules.check_required_sections(data, present_headings))
    errors.extend(rules.check_authoritative_sources(data, repo_root))
    links = parsing.extract_links(body)
    errors.extend(rules.check_links(links, path, repo_root))

    result = "FAIL" if errors else "PASS"
    return reporting.build_report(path, result, errors)


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
    print(reporting.format_results(results))
    return reporting.exit_code_for(results)
