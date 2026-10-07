#!/usr/bin/env python3
"""Tests for scripts/validate_run_artifacts.py."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_run_artifacts.py"
FIXTURES = Path(__file__).parent / "fixtures"


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(cwd or REPO_ROOT),
    )


def _copy_core(tmp: Path, *, include_optional_invalid: bool = False, include_stale_phase2: bool = False) -> None:
    for name in ("eval-brief.md", "phase1b-competitive-raw.md", "phase1c-strengths-raw.md"):
        shutil.copy(FIXTURES / "valid" / name, tmp / name)
    if include_optional_invalid:
        shutil.copy(FIXTURES / "invalid" / "phase1e-security-raw.md", tmp / "phase1e-security-raw.md")
    if include_stale_phase2:
        shutil.copy(FIXTURES / "invalid" / "phase2-synthesis.md", tmp / "phase2-synthesis.md")


def test_pre_phase2_passes_with_core_only(tmp_path: Path):
    _copy_core(tmp_path)
    result = _run(["--gate", "pre-phase2", str(tmp_path)])
    assert result.returncode == 0, result.stderr


def test_pre_phase2_ignores_stale_invalid_phase2(tmp_path: Path):
    _copy_core(tmp_path, include_stale_phase2=True)
    result = _run(["--gate", "pre-phase2", str(tmp_path)])
    assert result.returncode == 0, result.stderr


def test_pre_phase2_fails_on_present_invalid_optional(tmp_path: Path):
    _copy_core(tmp_path, include_optional_invalid=True)
    result = _run(["--gate", "pre-phase2", str(tmp_path)])
    assert result.returncode == 1
    assert "phase1e" in result.stderr.lower() or "Validation failed" in result.stderr


def test_pre_phase3_fails_on_invalid_synthesis(tmp_path: Path):
    _copy_core(tmp_path, include_stale_phase2=True)
    result = _run(["--gate", "pre-phase3", str(tmp_path)])
    assert result.returncode == 1


def test_pre_phase2_fails_when_required_core_missing(tmp_path: Path):
    shutil.copy(FIXTURES / "valid" / "eval-brief.md", tmp_path / "eval-brief.md")
    result = _run(["--gate", "pre-phase2", str(tmp_path)])
    assert result.returncode == 1
    assert "phase1b" in result.stderr.lower() or "missing" in result.stderr.lower()


def test_unknown_explicit_file_fails(tmp_path: Path):
    (tmp_path / "mystery.md").write_text("# Mystery\n", encoding="utf-8")
    result = _run(["--gate", "pre-phase2", "--file", str(tmp_path / "mystery.md")])
    assert result.returncode != 0


def test_missing_gate_flag_exits_usage():
    result = _run([str(FIXTURES / "valid")])
    assert result.returncode == 2


def test_helper_matches_direct_validate_on_same_file(tmp_path: Path):
    shutil.copy(FIXTURES / "invalid" / "phase1b-competitive-raw.md", tmp_path / "phase1b-competitive-raw.md")
    shutil.copy(FIXTURES / "valid" / "eval-brief.md", tmp_path / "eval-brief.md")
    shutil.copy(FIXTURES / "valid" / "phase1c-strengths-raw.md", tmp_path / "phase1c-strengths-raw.md")

    helper = _run(["--gate", "pre-phase2", str(tmp_path)])
    direct = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_artifact.py"),
            str(tmp_path / "phase1b-competitive-raw.md"),
            str(REPO_ROOT / "schemas" / "phase1b-competitive.schema.json"),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
    )
    assert helper.returncode == 1
    assert direct.returncode == 1
