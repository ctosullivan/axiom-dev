"""Validation rules for the Axiom Dev documentation/knowledge validator.

Operates on already-parsed schema data and already-extracted
headings/links (see parsing.py) for most rules, so they can be reasoned
about independently of how a document was parsed. Two exceptions read
the filesystem directly, because what they check is inherently about
files other than the one document being validated, not about already-
parsed content: load_governed_manifest (docs/governed-documents.txt) and
find_orphaned_schemas (a repository-wide scan for *.md.schema.yaml files
with no corresponding document — contract revision rule 8, prompt 004).
Split out of the original monolithic implementation as Stage 1.4's
behaviour-preserving refactor; see planning/phase-01-foundation.md
Stage 1.4.
"""
from __future__ import annotations

import re
from pathlib import Path

from .parsing import SCHEMA_SUFFIX

REQUIRED_FIELDS = {
    "audience",
    "purpose",
    "required_sections",
    "authoritative_sources",
    "acceptance_criteria",
}

ADR_PATH_RE = re.compile(r"decisions/(\d+)-[^/]*\.md$")


def is_within(resolved: Path, root: Path) -> bool:
    """True if `resolved` is `root` or a descendant of it.

    Carried over unchanged from the pre-refactor fix for the
    "no paths outside the repository" rule (contract rules 5/6) found by
    independent review — see evidence/stage-1.4-baseline.md.
    """
    try:
        resolved.relative_to(root)
        return True
    except ValueError:
        return False


def check_required_fields(data: dict) -> list[str]:
    """Contract rule 3."""
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return [f"missing required field(s): {sorted(missing)}"]
    return []


NON_EMPTY_STRING_FIELDS = ("audience", "purpose")
LIST_OF_STRINGS_FIELDS = ("required_sections", "authoritative_sources", "acceptance_criteria")

GOVERNED_MANIFEST_PATH = "docs/governed-documents.txt"


def check_field_types_and_content(data: dict) -> list[str]:
    """Contract rules 10-13 (prompt 003 Amendment C).

    Assumes check_required_fields(data) already returned no errors, i.e.
    every field in NON_EMPTY_STRING_FIELDS/LIST_OF_STRINGS_FIELDS is
    present. Called before rules 4-7, which assume well-typed data.
    """
    errors: list[str] = []

    for field in NON_EMPTY_STRING_FIELDS:
        value = data[field]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string, got {value!r}")

    for field in LIST_OF_STRINGS_FIELDS:
        value = data[field]
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            errors.append(f"{field} must be a list of strings, got {value!r}")
            continue
        if field in ("required_sections", "acceptance_criteria") and not value:
            errors.append(f"{field} must not be empty")
        if field == "acceptance_criteria" and any(not v.strip() for v in value):
            errors.append("acceptance_criteria entries must be non-empty strings")

    return errors


def find_orphaned_schemas(
    repo_root: Path, exclude_prefixes: tuple[str, ...] = ("tests",)
) -> list[Path]:
    """Contract revision rule 8: every *.md.schema.yaml under repo_root
    with no corresponding <path>.md document. Repository-wide by nature
    (asserting "no document exists here" needs a full scan), so this is
    called from main()'s batch entry point, not from validate_file.

    exclude_prefixes: top-level path components (relative to repo_root)
    to skip. Defaults to excluding tests/ — fixtures deliberately
    include a real orphaned schema (tests/fixtures/invalid/orphaned.md.schema.yaml)
    to test this very function; without this exclusion, scanning the
    real repository root would report that fixture as a real orphan on
    every CI run, forever — found by actually running main() against the
    real repo root before committing, not left as a hypothetical.
    Callers testing against FIXTURES directly (not the full repo root)
    are unaffected, since "tests" is never the first path component
    relative to FIXTURES itself.
    """
    orphans: list[Path] = []
    for schema_path in sorted(repo_root.rglob(f"*{SCHEMA_SUFFIX}")):
        rel_parts = schema_path.relative_to(repo_root).parts
        if rel_parts and rel_parts[0] in exclude_prefixes:
            continue
        doc_path = schema_path.with_name(schema_path.name[: -len(SCHEMA_SUFFIX)])
        if not doc_path.exists():
            orphans.append(schema_path)
    return orphans


def load_governed_manifest(repo_root: Path) -> set[str]:
    """Contract rule 15: repository-relative paths that must carry a
    passing schema. Missing manifest file => empty set (nothing governed),
    not an error."""
    manifest_path = repo_root / GOVERNED_MANIFEST_PATH
    if not manifest_path.exists():
        return set()
    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    return {
        stripped
        for line in lines
        if (stripped := line.strip()) and not stripped.startswith("#")
    }


def check_required_sections(data: dict, present_headings: set[str]) -> list[str]:
    """Contract rule 4."""
    missing_headings = [
        heading
        for heading in data["required_sections"]
        if heading not in present_headings
    ]
    if missing_headings:
        return [f"missing required section(s): {missing_headings}"]
    return []


def check_authoritative_sources(data: dict, repo_root: Path) -> list[str]:
    """Contract rules 5 and 7 (the authoritative_sources half)."""
    errors: list[str] = []
    for source in data["authoritative_sources"]:
        if not isinstance(source, str) or "§" in source or source.strip() != source:
            errors.append(
                f"authoritative_sources entry is not a bare path: {source!r}"
            )
            continue
        resolved = (repo_root / source).resolve()
        if not is_within(resolved, repo_root):
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
    return errors


def check_links(links: list[str], document_path: Path, repo_root: Path) -> list[str]:
    """Contract rules 6 and 7 (the body-link half)."""
    errors: list[str] = []
    for link in links:
        if link.startswith("http://") or link.startswith("https://"):
            continue
        link_path = link.split("#")[0]
        if not link_path:
            continue
        resolved = (document_path.parent / link_path).resolve()
        if not is_within(resolved, repo_root):
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
    return errors
