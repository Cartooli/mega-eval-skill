#!/usr/bin/env python3
"""Sim-pack source contracts from /simulate-users (weighted operator simulation).

Each test cites a finding id/slug so the pack stays auditable across runs.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ingest  # noqa: E402
import validate_artifact  # noqa: E402


# insight: brief-1e1f-drift — Phase 0 template requires 1E/1F sections
def test_ingest_template_includes_security_and_durability_sections():
    sources = [{"name": "idea.txt", "type": ".txt", "content": "A product idea."}]
    brief = ingest.generate_brief_template(sources)
    assert "## Security audit (Phase 1E)" in brief
    assert "## AI durability audit (Phase 1F)" in brief
    assert "**AI-surface applicability note:**" in brief


# insight: brief-1e1f-drift — canonical fixtures match Phase 0 checklist
def test_valid_eval_brief_fixture_includes_1e_1f_sections():
    text = (REPO_ROOT / "tests" / "fixtures" / "valid" / "eval-brief.md").read_text(encoding="utf-8")
    assert "## Security audit (Phase 1E)" in text
    assert "## AI durability audit (Phase 1F)" in text
    assert "Audit decision:" in text


# insight: brief-1e1f-drift — sample run brief stays aligned with checklist
def test_sample_run_eval_brief_includes_1e_1f_sections():
    text = (REPO_ROOT / "examples" / "sample-run" / "eval-brief.md").read_text(encoding="utf-8")
    assert "## Security audit (Phase 1E)" in text
    assert "## AI durability audit (Phase 1F)" in text


# insight: ingest-soft-fail — CLI must not exit 0 when extraction fails
def test_ingest_cli_exits_nonzero_when_file_missing(tmp_path):
    output_file = tmp_path / "brief.md"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "ingest.py"),
            str(tmp_path / "missing.txt"),
            "-o",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 1
    assert "Ingestion failed" in result.stderr
    assert not output_file.exists()


# insight: ingest-soft-fail — helper classifies operator-visible failure markers
@pytest.mark.parametrize(
    "content",
    [
        "[ERROR: File not found: x]",
        "[pdftotext not available. Use Read tool on the PDF directly.]",
        "[Unsupported file type: .xyz. Read the file manually.]",
    ],
)
def test_is_extraction_failure_detects_markers(content):
    assert ingest.is_extraction_failure(content) is True


def test_is_extraction_failure_allows_clean_text():
    assert ingest.is_extraction_failure("Normal extracted pitch text.") is False


# insight: validate-not-in-checklist — checklist must require contract validation
def test_pipeline_checklist_requires_artifact_validation():
    text = (REPO_ROOT / "references" / "pipeline-checklist.md").read_text(encoding="utf-8")
    assert "validate_artifact.py" in text
    assert "schemas/" in text


# insight: schema-gap-documented — contracts doc names the 1E/1F schema debt
def test_artifact_contracts_doc_names_1e_1f_schema_gap():
    text = (REPO_ROOT / "docs" / "architecture" / "artifact-contracts.md").read_text(encoding="utf-8")
    assert "phase1e-security-raw.md" in text
    assert "phase1f-durability-raw.md" in text
    assert "Security audit (Phase 1E)" in text


# insight: skill-count-docs — README lists prompt-derivation among phase skills
def test_readme_lists_prompt_derivation_skill():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "mega-eval-prompt-derivation" in text
    assert "eleven" in text.lower() or "prompt-derivation" in text


# insight: bundle-sessions-opaque — docs tell operators to pass the session folder
def test_readme_documents_bundle_session_folder_requirement():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "sessions/<session>/" in text or "session folder" in text


# insight: brief-1e1f-drift — current schema still passes fixture (debt parked; do not red-assert)
def test_eval_brief_schema_still_passes_valid_fixture_without_requiring_1e_1f():
    """Documents current contract lag: schema does not yet require 1E/1F headings.

    Major Project: extend eval-brief.schema.json — do not flip this into a failing
    assertion until that schema change lands.
    """
    artifact = REPO_ROOT / "tests" / "fixtures" / "valid" / "eval-brief.md"
    schema = REPO_ROOT / "schemas" / "eval-brief.schema.json"
    errors = validate_artifact.validate_file(artifact, schema)
    assert errors == []
    schema_text = schema.read_text(encoding="utf-8")
    assert "Security audit (Phase 1E)" not in schema_text
