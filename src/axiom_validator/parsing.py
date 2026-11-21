"""Parsing concerns for the Axiom Dev documentation/knowledge validator:
front-matter extraction, YAML loading, heading extraction (excluding
fenced code blocks), and Markdown link extraction (excluding inline
code spans).

Split out of the original monolithic implementation
(formerly src/axiom_validator.py, now this package) as Stage 1.4's
behaviour-preserving refactor. See planning/phase-01-foundation.md
Stage 1.4 and evidence/stage-1.4-baseline.md for the before/after
verification this split must satisfy — the regexes and their fixes
(fenced-code-block exclusion in particular) are carried over unchanged
from the pre-refactor baseline, not re-derived.
"""
from __future__ import annotations

import re

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCED_CODE_BLOCK_RE = re.compile(r"^```[^\n]*\n.*?\n```[ \t]*$", re.DOTALL | re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


class NoFrontmatter(Exception):
    """Raised when a document has no YAML front-matter block at all."""


class FrontmatterParseError(Exception):
    """Raised when a front-matter block exists but isn't a usable YAML mapping."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body), or raise NoFrontmatter."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise NoFrontmatter()
    return match.group(1), text[match.end():]


def parse_frontmatter(frontmatter_text: str) -> dict:
    """Parse front-matter YAML text into a dict, or raise FrontmatterParseError."""
    try:
        data = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        raise FrontmatterParseError(f"invalid YAML front-matter: {exc}") from exc
    if not isinstance(data, dict):
        raise FrontmatterParseError("front-matter must be a YAML mapping (object)")
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
