"""Validation rules for the Axiom Dev documentation/knowledge validator.

Operates on already-parsed schema data and already-extracted
headings/links (see parsing.py) for most rules, so they can be reasoned
about independently of how a document was parsed. Two exceptions read
the filesystem directly, because what they check is inherently about
files other than the one document being validated, not about already-
parsed content: load_governed_manifest (schemas/governed-documents.txt) and
find_orphaned_schemas (a repository-wide scan for *.md.schema.yaml files
with no corresponding document — contract revision rule 8, prompt 004).
Split out of the original monolithic implementation as Stage 1.4's
behaviour-preserving refactor; see planning/phase-01-foundation.md
Stage 1.4.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import parsing
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

GOVERNED_MANIFEST_PATH = "schemas/governed-documents.txt"


class GovernedManifestMissing(Exception):
    """Raised when the governed-document manifest file itself does not
    exist. Distinguished deliberately from "manifest exists but lists
    zero documents" (load_governed_manifest legitimately returns an
    empty set for that case) — a missing manifest *file* is a
    configuration-integrity failure, found worth failing closed on
    rather than silently treating as "nothing is governed" (prompt 005
    Sec 7, "Manifest integrity": "assess the current behaviour when the
    entire governed-document manifest is missing... implement an
    appropriately scoped fail-closed behaviour")."""


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


def find_orphaned_schemas(repo_root: Path, mirror_root: Path | None = None) -> list[Path]:
    """Contract revision 2, rule 8 (decisions/0007): every schema file
    under <mirror_root>/schemas/ with no corresponding mirrored
    document. Repository-wide by nature (asserting "no document exists
    here" needs a full scan of the schema tree), so this is called from
    main()'s batch entry point, not from validate_file.

    mirror_root defaults to repo_root (the production schemas/ tree).
    Tests pass FIXTURES to scan the separate fixture schema tree
    (tests/fixtures/schemas/) instead. Because that tree is never
    nested inside <repo_root>/schemas/, scanning repo_root's own
    schemas/ directory never sees a fixture at all — prompt 004's
    "exclude tests/ by name" workaround for this exact problem is no
    longer needed; the two trees simply don't overlap.
    """
    if mirror_root is None:
        mirror_root = repo_root
    mirror_root = mirror_root.resolve()
    schema_root = mirror_root / parsing.SCHEMA_ROOT_DIR
    if not schema_root.is_dir():
        return []
    orphans: list[Path] = []
    for schema_path in sorted(schema_root.rglob(f"*{SCHEMA_SUFFIX}")):
        doc_path = parsing.doc_path_for_schema(schema_path, mirror_root)
        if doc_path is not None and not doc_path.exists():
            orphans.append(schema_path)
    return orphans


def load_governed_manifest(repo_root: Path) -> set[str]:
    """Contract rule 15: repository-relative paths that must carry a
    passing schema. Raises GovernedManifestMissing if the manifest file
    itself does not exist, or exists but cannot actually be read as a
    regular file (e.g. it's a directory, or unreadable) — a
    legitimately-empty-but-present, readable manifest still returns an
    empty set (no error); only an unusable manifest fails closed
    (prompt 005, "Manifest integrity"; the not-a-regular-file case
    found by independent review of the prompt 007 batch, which
    constructed a `schemas/governed-documents.txt` *directory* and
    found it raised an unhandled `IsADirectoryError` straight out of
    `validate_file` instead of this structured failure — reading via
    try/except rather than checking `.exists()` first closes that gap
    for any OS-level reason the path isn't usable as a file, not only
    a directory)."""
    manifest_path = repo_root / GOVERNED_MANIFEST_PATH
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise GovernedManifestMissing(
            f"{GOVERNED_MANIFEST_PATH} does not exist — cannot determine which "
            "documents are governed; failing closed rather than silently "
            "treating every document as ungoverned."
        ) from None
    except OSError as exc:
        raise GovernedManifestMissing(
            f"{GOVERNED_MANIFEST_PATH} exists but could not be read ({exc}) — "
            "cannot determine which documents are governed; failing closed "
            "rather than silently treating every document as ungoverned."
        ) from exc
    lines = text.splitlines()
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
