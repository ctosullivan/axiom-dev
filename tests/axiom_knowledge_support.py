"""Shared test fixtures for axiom_knowledge's test suites.

Not itself a test module (deliberately not named test_*.py, so
`unittest discover` never collects it as one). Builds small, synthetic,
git-backed repositories shaped like Ledgerkit's real
dev-docs/compat-register/ schema -- never a live Ledgerkit checkout, per
`planning/phase-02-stage-2.2-plan.md` SS2a's explicit "needs no live
Ledgerkit checkout" requirement.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

DEFAULT_REGISTER_RELATIVE = "dev-docs/compat-register"


def _run_git(repo_root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        env={
            "GIT_AUTHOR_NAME": "test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
            "HOME": str(repo_root),
            "PATH": "/usr/bin:/bin",
        },
    )


def make_repo(
    tmp_path: Path,
    register_relative: str | None = DEFAULT_REGISTER_RELATIVE,
    init_git: bool = True,
) -> Path:
    """Create a minimal Axiom-adopted repository: knowledge/README.md (the
    discovery marker, optionally naming a register: directive) plus the
    register directory itself."""
    repo_root = tmp_path / "repo"
    (repo_root / "knowledge").mkdir(parents=True)

    marker_lines = ["# Knowledge marker\n"]
    if register_relative is not None:
        marker_lines.append(f"register: {register_relative}\n")
    (repo_root / "knowledge" / "README.md").write_text("".join(marker_lines), encoding="utf-8")

    register_dir = repo_root / (register_relative or "knowledge/claims")
    register_dir.mkdir(parents=True, exist_ok=True)

    if init_git:
        _run_git(repo_root, "init", "-q")
        _run_git(repo_root, "add", "-A")
        _run_git(repo_root, "commit", "-q", "-m", "init")

    return repo_root


def write_claim(
    repo_root: Path,
    claim_id: str,
    *,
    register_relative: str = DEFAULT_REGISTER_RELATIVE,
    area: str = "parser.example",
    kind: str = "compatible",
    relationship: str | None = "equivalent",
    compatibility_target: str = "1.52.4",
    status: str = "proposed",
    verified_by: str | None = None,
    verified_date: str | None = None,
    evidence: list | None = None,
    implementation: list | None = None,
    tests: list | None = None,
    reason: str = "Synthetic fixture claim for axiom_knowledge's own tests.",
    commit: bool = True,
) -> Path:
    """Write one synthetic claim file, shaped exactly like a real
    compat-register entry (schema.md)."""
    record = {
        "id": claim_id,
        "area": area,
        "kind": kind,
        "upstream": {"project": "hledger", "compatibility_target": compatibility_target},
        "ledgerkit": {"relationship": relationship} if relationship is not None else {},
        "compatibility": {
            "upstream_syntax_preserved": True,
            "extension_requires_explicit_syntax": "n/a",
        },
        "reason": reason,
        "implementation": implementation if implementation is not None else ["pkg/mod.py:function"],
        "tests": tests if tests is not None else ["tests/test_mod.py::TestClass::test_case"],
        "evidence": evidence if evidence is not None else [
            {"kind": "manual", "ref": "https://example.invalid/spec", "pinned_at": compatibility_target}
        ],
        "status": status,
        "verified_by": verified_by,
        "verified_date": verified_date,
    }

    register_dir = repo_root / register_relative
    register_dir.mkdir(parents=True, exist_ok=True)
    path = register_dir / f"{claim_id}.yaml"
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")

    if commit:
        _run_git(repo_root, "add", "-A")
        _run_git(repo_root, "commit", "-q", "-m", f"add {claim_id}")

    return path


def write_scope_manifest(
    repo_root: Path,
    claim_id: str,
    *,
    manifest_claim_id: str | None = None,
    scope: str | None = "Synthetic reviewed scope statement for this claim.",
    source_pin: str | None = "1.52.4",
    reviewed_by: str | None = "independent-reviewer",
    reviewed_date: str | None = "2026-11-25",
    tracked: bool = True,
) -> Path:
    """Write one scope manifest, shaped per knowledge-api-design.md SS3b.1."""
    manifest: dict = {}
    if manifest_claim_id is not None or claim_id is not None:
        manifest["claim_id"] = manifest_claim_id if manifest_claim_id is not None else claim_id
    if scope is not None:
        manifest["scope"] = scope
    if source_pin is not None:
        manifest["source_pin"] = source_pin
    if reviewed_by is not None:
        manifest["reviewed_by"] = reviewed_by
    if reviewed_date is not None:
        manifest["reviewed_date"] = reviewed_date

    manifest_dir = repo_root / "knowledge" / "scope-manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    path = manifest_dir / f"{claim_id}.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    if tracked:
        _run_git(repo_root, "add", "-A")
        _run_git(repo_root, "commit", "-q", "-m", f"add scope manifest for {claim_id}")

    return path
