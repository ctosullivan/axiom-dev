"""Validation rules for the Axiom Dev documentation/knowledge validator.

Operates on already-parsed front-matter data and already-extracted
headings/links (see parsing.py) — this module has no file-reading or
Markdown-parsing regex of its own, only the ADR-path pattern and the
rule logic, so the rules can be reasoned about independently of how a
document was parsed. Split out of the original monolithic
implementation as Stage 1.4's behaviour-preserving refactor; see
planning/phase-01-foundation.md Stage 1.4.
"""
from __future__ import annotations

import re
from pathlib import Path

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
