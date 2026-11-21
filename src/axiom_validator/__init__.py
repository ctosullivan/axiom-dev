"""Axiom Dev documentation/knowledge validator — package entry point.

Implements contracts/documentation-schema-validator.md, including its
"Contract revision" section (prompt 004, decisions/0006): schemas load
from a companion `<path>.md.schema.yaml` file, not embedded front-matter.
This is the second architectural change to this orchestrator — the
first was the Stage 1.4 behaviour-preserving refactor (monolithic file
into parsing/rules/reporting modules); this one is explicitly an
authorised contract evolution, not behaviour-preserving, per the prompt
004 Amendment C requirement to say so plainly.

Public API: validate_file(path, repo_root, governed_manifest=None) and
main(argv) — same names and call shape as before this change (CLI usage
is unchanged: `python3 -m axiom_validator <paths> --repo-root .`); the
*return values* for a document that used to carry front-matter change,
since front-matter is no longer where its schema lives — that is the
intended, documented behaviour change this revision authorises, not a
compatibility break to be hidden.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import parsing, reporting, rules


def validate_file(path: Path, repo_root: Path, governed_manifest: set[str] | None = None) -> dict:
    """Validate one Markdown file against its companion schema file.

    Returns a dict with keys: file, result (SKIPPED|INVALID_SCHEMA|PASS|FAIL),
    errors (list of human-readable strings).

    governed_manifest: repository-relative paths that must carry a schema
    (contract rule 15, prompt 003 Amendment C — now triggered by a
    missing companion schema file rather than missing front-matter, per
    the prompt 004 contract revision). Defaults to the real
    docs/governed-documents.txt manifest when not given; tests may pass
    an explicit set to exercise the rule without real repository files.

    Does NOT check for orphaned schemas — that is inherently a
    repository-wide question (see rules.find_orphaned_schemas), not
    something answerable about one named document; main() runs it
    separately as part of its batch CLI pass.

    repo_root is resolved internally (callers may pass an unresolved
    relative path, e.g. Path(".")) — found necessary by independent
    review in the prompt 003 batch: the containment check
    (rules.is_within) compares a resolved absolute path against
    repo_root, which only works if repo_root is itself resolved.
    """
    repo_root = repo_root.resolve()
    text = path.read_text(encoding="utf-8")

    if parsing.has_embedded_frontmatter(text):
        return reporting.build_report(
            path,
            "FAIL",
            [
                f"{path} begins with a '---'-delimited block, which this validator "
                f"treats as the deprecated embedded-front-matter documentation-schema "
                f"convention (decisions/0006) and never parses as a live schema — "
                f"move it to the companion file {parsing.companion_schema_path(path)} "
                f"if it IS meant to be this document's schema. (Scope note: this check "
                f"cannot distinguish that case from an unrelated '---'-delimited block "
                f"used for something else entirely, e.g. planning/prompts/'s provenance "
                f"headers — those are not schema-bearing documents and are not governed, "
                f"so this result is expected and harmless for them, not a sign they need "
                f"migrating.)"
            ],
        )

    schema_path = parsing.companion_schema_path(path)
    if not schema_path.exists():
        manifest = (
            rules.load_governed_manifest(repo_root)
            if governed_manifest is None
            else governed_manifest
        )
        try:
            rel = str(path.resolve().relative_to(repo_root))
        except ValueError:
            rel = str(path)
        if rel in manifest:
            return reporting.build_report(
                path,
                "FAIL",
                [f"{rel} is a governed document ({rules.GOVERNED_MANIFEST_PATH}) with no companion schema file ({schema_path.name})"],
            )
        return reporting.build_report(path, "SKIPPED", [])

    try:
        data = parsing.parse_schema_yaml(schema_path.read_text(encoding="utf-8"))
    except parsing.SchemaParseError as exc:
        return reporting.build_report(path, "INVALID_SCHEMA", [exc.message])

    missing_field_errors = rules.check_required_fields(data)
    if missing_field_errors:
        return reporting.build_report(path, "INVALID_SCHEMA", missing_field_errors)

    type_content_errors = rules.check_field_types_and_content(data)
    if type_content_errors:
        return reporting.build_report(path, "INVALID_SCHEMA", type_content_errors)

    errors: list[str] = []
    present_headings = parsing.extract_headings(text)
    errors.extend(rules.check_required_sections(data, present_headings))
    errors.extend(rules.check_authoritative_sources(data, repo_root))
    links = parsing.extract_links(text)
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
    results.extend(
        reporting.build_report(
            schema_path,
            "FAIL",
            [f"orphaned schema: no corresponding document at {schema_path.with_name(schema_path.name[: -len(parsing.SCHEMA_SUFFIX)])}"],
        )
        for schema_path in rules.find_orphaned_schemas(repo_root)
    )
    print(reporting.format_results(results))
    return reporting.exit_code_for(results)
