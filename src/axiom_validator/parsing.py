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
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")

# Fence-open: up to 3 leading spaces (CommonMark), then 3+ of the same
# fence character (backtick or tilde), then anything (an info string).
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(?:.*)?$")

SCHEMA_SUFFIX = ".schema.yaml"
SCHEMA_ROOT_DIR = "schemas"


class SchemaParseError(Exception):
    """Raised when a schema file exists but isn't valid YAML, or
    isn't a YAML mapping. Formerly FrontmatterParseError, before schemas
    moved out of embedded front-matter (prompt 004, decisions/0006)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PathEscapesMirrorRoot(Exception):
    """Raised when a document path does not resolve under the mirror
    root its schema would be computed relative to (decisions/0007) —
    schema lookup cannot be computed, let alone escape, for a path
    outside the tree it's supposed to mirror."""


def schema_path_for(doc_path: Path, mirror_root: Path) -> Path:
    """The deterministic schema path for a document, mirrored under
    <mirror_root>/schemas/ (decisions/0007, superseding the colocated
    `<path>.md.schema.yaml` convention of decisions/0006):
    <mirror_root>/<rel> -> <mirror_root>/schemas/<rel>.schema.yaml.
    No registry — computed from the document's own path and
    `mirror_root` alone.

    `mirror_root` is normally the repository root (production schemas
    live at `<repo_root>/schemas/...`). Test fixtures pass a different
    `mirror_root` (their own `tests/fixtures/` directory) so their
    schemas live in a wholly separate `tests/fixtures/schemas/` tree,
    never inside the production `schemas/` tree — contract revision 2's
    explicit requirement not to confuse production schemas with
    deliberately invalid test fixtures, and what keeps the production
    orphan scan (rules.find_orphaned_schemas) from ever seeing a
    fixture at all, rather than needing to exclude `tests/` by name
    (prompt 004's now-superseded fix for the same underlying problem).

    Raises PathEscapesMirrorRoot if `doc_path` does not resolve under
    `mirror_root` — found necessary per prompt 005's path-safety
    requirement ("schema lookup cannot escape the intended schema root
    through manipulated relative paths").
    """
    mirror_root = mirror_root.resolve()
    try:
        rel = doc_path.resolve().relative_to(mirror_root)
    except ValueError:
        raise PathEscapesMirrorRoot(
            f"{doc_path} does not resolve under mirror root {mirror_root}"
        ) from None
    return mirror_root / SCHEMA_ROOT_DIR / rel.parent / (rel.name + SCHEMA_SUFFIX)


def doc_path_for_schema(schema_path: Path, mirror_root: Path) -> Path | None:
    """Reverse of schema_path_for: given a schema file, return the
    document path it would mirror, or None if `schema_path` isn't
    actually under `<mirror_root>/schemas/` or doesn't carry the schema
    suffix. Used by rules.find_orphaned_schemas — the only place this
    reverse mapping is needed, since detecting an orphan is inherently
    "work backwards from a schema file to ask whether its document
    exists," not a per-document question."""
    mirror_root = mirror_root.resolve()
    schema_root = mirror_root / SCHEMA_ROOT_DIR
    try:
        rel = schema_path.resolve().relative_to(schema_root)
    except ValueError:
        return None
    if not rel.name.endswith(SCHEMA_SUFFIX):
        return None
    doc_name = rel.name[: -len(SCHEMA_SUFFIX)]
    return mirror_root / rel.parent / doc_name


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


def _strip_fenced_code_blocks(text: str) -> str:
    """Remove every fenced code block's lines (including its fence
    lines) from `text`, line by line, tracking fence state rather than
    matching a single regex against the whole document.

    Replaces a three-backtick-only regex that let a required heading
    hiding inside a tilde-fenced or 4-plus-backtick-fenced example
    wrongly count as present — found by native Codex review of PR #1
    (src/axiom_validator/parsing.py, "Exclude all supported fenced code
    blocks from heading checks"), reproduced directly before this fix
    (a document containing only a `~~~`-fenced "# Required" example
    satisfied `required_sections: [Required]`), not merely asserted.

    CommonMark fence rules this follows: an opening fence is up to 3
    leading spaces then 3+ of the same character (backtick or tilde);
    a closing fence must use the *same* character, be *at least as
    long* as the opening fence, and contain nothing else but that
    character (plus leading/trailing whitespace) — no info string. A
    fence that is never closed consumes the rest of the document, same
    as CommonMark; nothing after an unterminated fence is treated as
    outside it.
    """
    kept_lines: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    for line in text.split("\n"):
        if fence_char is None:
            match = FENCE_OPEN_RE.match(line)
            if match:
                fence_char = match.group(1)[0]
                fence_len = len(match.group(1))
                continue
            kept_lines.append(line)
        else:
            close_match = re.match(
                r"^ {0,3}(" + re.escape(fence_char) + r"{3,})\s*$", line
            )
            if close_match and len(close_match.group(1)) >= fence_len:
                fence_char = None
                fence_len = 0
            # Every line while inside a fence is dropped, whether or
            # not it's the closing fence line itself.
    return "\n".join(kept_lines)


def extract_headings(body: str) -> set[str]:
    """Return heading texts present in the body, excluding anything
    inside a fenced code block (any supported fence form — see
    _strip_fenced_code_blocks)."""
    body_without_fences = _strip_fenced_code_blocks(body)
    return {h.strip() for h in HEADING_RE.findall(body_without_fences)}


def extract_links(body: str) -> list[str]:
    """Return Markdown link targets in the body, excluding inline code spans."""
    body_without_code = INLINE_CODE_RE.sub("", body)
    return LINK_RE.findall(body_without_code)
