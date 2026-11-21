"""Parsing concerns for the Axiom Dev documentation/knowledge validator:
companion-schema-file discovery and YAML loading, embedded-front-matter
detection, heading extraction (excluding fenced code blocks), and
Markdown link extraction (excluding inline code spans).

Split out of the original monolithic implementation
(formerly src/axiom_validator.py, now this package) as Stage 1.4's
behaviour-preserving refactor. See planning/phase-01-foundation.md
Stage 1.4 and evidence/stage-1.4-baseline.md for the before/after
verification that split was checked against.

Schema loading changed from embedded front-matter to companion
`.schema.yaml` files as an explicit, authorised contract evolution
(prompt 004, decisions/0006, contracts/documentation-schema-validator.md
"Contract revision") — not a behaviour-preserving refactor. The heading/
link-extraction regexes and their fixes (fenced-code-block exclusion in
particular) are carried over unchanged from the pre-refactor baseline,
since they operate on a document's full text either way.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCED_CODE_BLOCK_RE = re.compile(r"^```[^\n]*\n.*?\n```[ \t]*$", re.DOTALL | re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")

SCHEMA_SUFFIX = ".schema.yaml"


class SchemaParseError(Exception):
    """Raised when a companion schema file exists but isn't valid YAML, or
    isn't a YAML mapping. Formerly FrontmatterParseError, before schemas
    moved out of embedded front-matter (prompt 004, decisions/0006)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def companion_schema_path(doc_path: Path) -> Path:
    """The deterministic companion-schema path for a document:
    <path>.md -> <path>.md.schema.yaml. Contract revision rule 1 — no
    separate registry, computed from the document's own path alone."""
    return doc_path.with_name(doc_path.name + SCHEMA_SUFFIX)


def has_embedded_frontmatter(text: str) -> bool:
    """True if `text` still begins with the old `---\\n...\\n---\\n`
    front-matter block. Contract revision rule 7: a document in this
    state is FAIL, never silently parsed as if it were the current
    schema, even if a companion file also exists."""
    return FRONTMATTER_RE.match(text) is not None


def parse_schema_yaml(schema_text: str) -> dict:
    """Parse companion-schema YAML text into a dict, or raise
    SchemaParseError. Formerly parse_frontmatter; same validation logic,
    now applied to a companion file's content instead of an embedded
    front-matter block (contract revision rule 3)."""
    try:
        data = yaml.safe_load(schema_text)
    except yaml.YAMLError as exc:
        raise SchemaParseError(f"invalid YAML in companion schema file: {exc}") from exc
    if not isinstance(data, dict):
        raise SchemaParseError("companion schema file must be a YAML mapping (object)")
    return data


def extract_headings(body: str) -> set[str]:
    """Return heading texts present in the body, excluding anything
    inside a fenced code block."""
    body_without_fences = FENCED_CODE_BLOCK_RE.sub("", body)
    return {h.strip() for h in HEADING_RE.findall(body_without_fences)}


def extract_links(body: str) -> list[str]:
    """Return Markdown link targets in the body, excluding inline code spans."""
    body_without_code = INLINE_CODE_RE.sub("", body)
    return LINK_RE.findall(body_without_code)
