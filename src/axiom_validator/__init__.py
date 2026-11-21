"""Axiom Dev documentation/knowledge validator — package entry point.

Implements contracts/documentation-schema-validator.md, including its
two "Contract revision" sections: prompt 004/decisions/0006 (schemas
load from a companion file, not embedded front-matter) and prompt
005/decisions/0007 (that companion file lives in a mirrored path under
a top-level schemas/ directory, not colocated beside its document).
Both are explicitly authorised contract evolutions, not
behaviour-preserving refactors — the only behaviour-preserving
refactor in this component's history is the original Stage 1.4 module
split (monolithic file into parsing/rules/reporting modules).

Public API: validate_file(path, repo_root, governed_manifest=None,
schema_mirror_root=None) and main(argv) — same names and call shape as
before (CLI usage is unchanged: `python3 -m axiom_validator <paths>
--repo-root .`); the one new parameter is optional and defaults to
`repo_root`, so every existing call site is unaffected. The *return
values* for a document whose schema moved change, since the schema is
no longer where it used to be — that is the intended, documented
behaviour change each revision authorises, not a compatibility break
to be hidden.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import parsing, reporting, rules


def validate_file(
    path: Path,
    repo_root: Path,
    governed_manifest: set[str] | None = None,
    schema_mirror_root: Path | None = None,
) -> dict:
    """Validate one Markdown file against its schema file.

    Returns a dict with keys: file, result (SKIPPED|INVALID_SCHEMA|PASS|FAIL),
    errors (list of human-readable strings).

    governed_manifest: repository-relative paths that must carry a schema
    (contract rule 15). Defaults to loading the real
    schemas/governed-documents.txt manifest when not given — which
    raises (as a FAIL result for this document, not an uncaught
    exception) if that manifest file is missing entirely, per the
    prompt 005 "Manifest integrity" fail-closed requirement; tests may
    pass an explicit set to bypass that and exercise the rule directly.

    schema_mirror_root: the root `path`'s schema is mirrored under
    (decisions/0007) — defaults to `repo_root`, so production documents
    get schemas at `<repo_root>/schemas/<rel>.schema.yaml`. Test
    fixtures pass their own `tests/fixtures/` directory here instead,
    so fixture schemas live under `tests/fixtures/schemas/`, in a tree
    wholly separate from the production `schemas/` tree it would
    otherwise be confused with (prompt 005 Sec 5, "do not confuse
    production schemas with deliberately invalid test fixtures").

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
    if schema_mirror_root is None:
        schema_mirror_root = repo_root
    text = path.read_text(encoding="utf-8")

    if parsing.has_embedded_frontmatter(text):
        try:
            schema_hint = str(parsing.schema_path_for(path, schema_mirror_root))
        except parsing.PathEscapesMirrorRoot:
            schema_hint = "its mirrored schemas/ location"
        return reporting.build_report(
            path,
            "FAIL",
            [
                f"{path} begins with a '---'-delimited block, which this validator "
                f"treats as the deprecated embedded-front-matter documentation-schema "
                f"convention (decisions/0006) and never parses as a live schema — "
                f"move it to {schema_hint} if it IS meant to be this document's "
                f"schema. (Scope note: this check cannot distinguish that case from "
                f"an unrelated '---'-delimited block used for something else "
                f"entirely, e.g. planning/prompts/'s provenance headers — those are "
                f"not schema-bearing documents and are not governed, so this result "
                f"is expected and harmless for them, not a sign they need migrating.)"
            ],
        )

    try:
        schema_path = parsing.schema_path_for(path, schema_mirror_root)
    except parsing.PathEscapesMirrorRoot as exc:
        return reporting.build_report(path, "FAIL", [str(exc)])

    # Manifest-missing fail-closed (contract revision 2 rule 4) must be
    # checked unconditionally here, not only inside the "schema absent"
    # branch below — found by native Codex review of PR #1 ("governed-
    # document manifest integrity is not checked when a companion
    # schema exists"): a document whose own schema file happens to
    # exist could previously still return PASS even when
    # schemas/governed-documents.txt was missing entirely, since the
    # manifest was never loaded at all in that code path. Moving the
    # load here means a missing manifest fails closed for *every*
    # document checked through the default (non-overridden) path,
    # regardless of whether that document's own schema exists.
    if governed_manifest is not None:
        manifest = governed_manifest
    else:
        try:
            manifest = rules.load_governed_manifest(repo_root)
        except rules.GovernedManifestMissing as exc:
            return reporting.build_report(path, "FAIL", [str(exc)])

    if not schema_path.exists():
        try:
            rel = str(path.resolve().relative_to(repo_root))
        except ValueError:
            rel = str(path)
        if rel in manifest:
            return reporting.build_report(
                path,
                "FAIL",
                [f"{rel} is a governed document ({rules.GOVERNED_MANIFEST_PATH}) with no schema file ({schema_path})"],
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
            [
                "orphaned schema: no corresponding document at "
                f"{parsing.doc_path_for_schema(schema_path, repo_root)}"
            ],
        )
        for schema_path in rules.find_orphaned_schemas(repo_root)
    )
    print(reporting.format_results(results))
    return reporting.exit_code_for(results)
