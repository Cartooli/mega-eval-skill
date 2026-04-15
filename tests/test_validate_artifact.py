#!/usr/bin/env python3
"""Tests for scripts/validate_artifact.py."""

import subprocess
import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import validate_artifact
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import validate_artifact


FIXTURES_DIR = Path(__file__).parent / "fixtures"
SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


@pytest.mark.parametrize(
    ("fixture_name", "schema_name"),
    [
        ("eval-brief.md", "eval-brief.schema.json"),
        ("phase1b-competitive-raw.md", "phase1b-competitive.schema.json"),
        ("phase1c-strengths-raw.md", "phase1c-strengths.schema.json"),
        ("phase1d-design-raw.md", "phase1d-design.schema.json"),
        ("phase2-synthesis.md", "phase2-synthesis.schema.json"),
        ("phase3-content-outline-raw.md", "phase3-content-outline.schema.json"),
    ],
)
def test_valid_artifacts_pass(fixture_name, schema_name):
    artifact_path = FIXTURES_DIR / "valid" / fixture_name
    schema_path = SCHEMAS_DIR / schema_name

    errors = validate_artifact.validate_file(artifact_path, schema_path)

    assert errors == []


@pytest.mark.parametrize(
    ("fixture_name", "schema_name"),
    [
        ("eval-brief.md", "eval-brief.schema.json"),
        ("phase1b-competitive-raw.md", "phase1b-competitive.schema.json"),
        ("phase1c-strengths-raw.md", "phase1c-strengths.schema.json"),
        ("phase1d-design-raw.md", "phase1d-design.schema.json"),
        ("phase2-synthesis.md", "phase2-synthesis.schema.json"),
        ("phase3-content-outline-raw.md", "phase3-content-outline.schema.json"),
    ],
)
def test_invalid_artifacts_fail(fixture_name, schema_name):
    artifact_path = FIXTURES_DIR / "invalid" / fixture_name
    schema_path = SCHEMAS_DIR / schema_name

    errors = validate_artifact.validate_file(artifact_path, schema_path)

    assert errors


def test_cli_passes_for_valid_fixture():
    artifact_path = FIXTURES_DIR / "valid" / "eval-brief.md"
    schema_path = SCHEMAS_DIR / "eval-brief.schema.json"

    result = subprocess.run(
        [sys.executable, "scripts/validate_artifact.py", str(artifact_path), str(schema_path)],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(Path(__file__).parent.parent),
    )

    assert result.returncode == 0
    assert "Validation passed" in result.stderr


def test_cli_fails_for_invalid_fixture():
    artifact_path = FIXTURES_DIR / "invalid" / "eval-brief.md"
    schema_path = SCHEMAS_DIR / "eval-brief.schema.json"

    result = subprocess.run(
        [sys.executable, "scripts/validate_artifact.py", str(artifact_path), str(schema_path)],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(Path(__file__).parent.parent),
    )

    assert result.returncode == 1
    assert "Validation failed" in result.stderr
