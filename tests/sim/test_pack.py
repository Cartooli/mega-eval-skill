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
    assert "validate_run_artifacts.py" in text
    assert "schemas/" in text
    assert "pre-phase1" in text
    assert "pre-phase2" in text
    assert "pre-phase3" in text
    assert "pre-phase4" in text
    assert "phase1e" in text
    assert "phase1f" in text
    assert "resume" in text.lower() or "resuming" in text.lower()


def test_example_jsonl_phase_complete_has_duration_ms():
    path = REPO_ROOT / "examples" / "run-feedback" / "run-log.example.jsonl"
    import json

    completes = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and '"phase_complete"' in line
    ]
    assert completes
    for event in completes:
        assert "duration_ms" in event
        assert isinstance(event["duration_ms"], int)


# insight: schema-gap-documented — phase1a remains deferred; 1E/1F schemas now exist
def test_artifact_contracts_doc_names_remaining_phase1a_gap():
    text = (REPO_ROOT / "docs" / "architecture" / "artifact-contracts.md").read_text(encoding="utf-8")
    assert "phase1a-hater-raw.md" in text
    assert (REPO_ROOT / "schemas" / "phase1e-security.schema.json").exists()
    assert (REPO_ROOT / "schemas" / "phase1f-durability.schema.json").exists()


# insight: skill-count-docs — README lists prompt-derivation among phase skills
def test_readme_lists_prompt_derivation_skill():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "mega-eval-prompt-derivation" in text
    assert "eleven" in text.lower() or "prompt-derivation" in text


# insight: bundle-sessions — docs describe session discovery / --session
def test_readme_documents_bundle_session_folder_requirement():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "sessions/<session>/" in text or "sessions/<name>/" in text
    assert "--session" in text


# insight: brief-1e1f-drift — schema requires Phase 1E/1F brief headings
def test_eval_brief_schema_requires_1e_1f_headings():
    artifact = REPO_ROOT / "tests" / "fixtures" / "valid" / "eval-brief.md"
    schema = REPO_ROOT / "schemas" / "eval-brief.schema.json"
    errors = validate_artifact.validate_file(artifact, schema)
    assert errors == []
    schema_text = schema.read_text(encoding="utf-8")
    assert "Security audit (Phase 1E)" in schema_text
    assert "AI durability audit (Phase 1F)" in schema_text

    stripped = artifact.read_text(encoding="utf-8")
    stripped = stripped.split("## Security audit (Phase 1E)")[0].rstrip() + "\n"
    stripped_errors = validate_artifact.validate_text(stripped, validate_artifact.load_schema(schema))
    assert any("Security audit (Phase 1E)" in err for err in stripped_errors)


# insight: gate-explicit-outside-set — a file outside the gate must not schema-pass that gate
def test_explicit_file_outside_gate_is_rejected(tmp_path):
    source = REPO_ROOT / "tests" / "fixtures" / "valid" / "phase2-synthesis.md"
    target = tmp_path / "phase2-synthesis.md"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_run_artifacts.py"),
            "--gate",
            "pre-phase2",
            "--file",
            str(target),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode != 0
    assert "outside gate" in result.stderr
    assert "Validation passed" not in result.stderr


# insight: duplicate-heading-hides-section — repeated titles must not validate as one section
def test_duplicate_heading_is_rejected():
    text = "# Evaluation Brief\n\n## Subject\n\nAlpha product\n\n## Subject\n\nBeta product\n"
    schema = validate_artifact.load_schema(REPO_ROOT / "schemas" / "eval-brief.schema.json")
    errors = validate_artifact.validate_text(text, schema)
    assert any("Duplicate heading 'Subject'" in err for err in errors)


# insight: phase-complete-requires-duration — CLI rejects phase_complete without duration_ms
def test_phase_complete_without_duration_exits_nonzero(tmp_path):
    log_path = tmp_path / "run-log.jsonl"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "log_event.py"),
            str(log_path),
            "phase_complete",
            "--run-id",
            "abc12345",
            "--phase",
            "phase0",
            "--status",
            "ok",
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 1
    assert "duration-ms" in result.stderr
    assert not log_path.exists()


# insight: log-details-capped — details cannot exceed the 500-character log cap
def test_log_event_caps_details_at_500_chars():
    import log_event

    event = log_event.build_event(
        event_type="tool_error",
        run_id="abc12345",
        details="x" * 800,
    )
    assert len(event["details"]) == 500
    assert event["details"].endswith("...")


# insight: suggest-learnings-missing-file — missing run log exits 2 with a message
def test_suggest_learnings_missing_file_exits_2(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "suggest_learnings.py"), str(tmp_path / "missing-run-log.md")],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 2
    assert "Run log not found" in result.stderr


# insight: log-opt-out-false — checklist and README treat MEGA_EVAL_LOG=false as off
def test_log_opt_out_includes_false():
    checklist = (REPO_ROOT / "references" / "pipeline-checklist.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "`MEGA_EVAL_LOG` is `off` / `0` / `false`" in checklist
    assert "`off`, `0`, or `false`" in readme


# insight: manual-install-omits-schemas — install instructions copy schemas next to scripts
def test_readme_manual_install_copies_schemas():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "mega-eval-skill/schemas" in readme
    assert "validate_run_artifacts.py" in readme


# insight: deliverable-path-workspace — Phase 4 writes docx beside the markdown artifacts
def test_skill_docx_path_is_workspace_relative():
    text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "<workspace>/sessions/<session>/eval-brief.md" in text
    assert "same workspace directory as the markdown artifacts" in text
    assert "pre-phase4" in text


# insight: stale-example-not-gate-valid — Future Builders README discloses schema drift
def test_future_builders_readme_discloses_schema_drift():
    text = (REPO_ROOT / "examples" / "future-builders-live" / "README.md").read_text(encoding="utf-8")
    assert "validate_run_artifacts.py" in text
    assert "schemas/" in text
