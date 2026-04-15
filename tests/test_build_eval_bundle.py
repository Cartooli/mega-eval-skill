#!/usr/bin/env python3
"""Tests for scripts/build_eval_bundle.py."""

import json
import subprocess
import sys
from pathlib import Path

# Add scripts/ to path so we can import build_eval_bundle
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import build_eval_bundle


REPO_ROOT = Path(__file__).parent.parent


class TestBuildBundle:
    """Contract tests for the eval bundle builder."""

    def test_sample_run_bundle_reports_phase_progress(self):
        sample_run = REPO_ROOT / "examples" / "sample-run"

        bundle = build_eval_bundle.build_bundle(sample_run)

        assert bundle["schema_version"] == "1.0"
        assert bundle["artifacts"]["eval_brief"]["exists"] is True
        assert bundle["artifacts"]["phase1a_hater"]["exists"] is True
        assert bundle["artifacts"]["phase2_synthesis"]["exists"] is True
        assert bundle["phases"]["phase0"]["complete"] is True
        assert bundle["phases"]["phase1"]["complete"] is True
        assert bundle["phases"]["phase2"]["complete"] is True
        assert bundle["phases"]["phase3"]["complete"] is True
        assert bundle["phases"]["phase4"]["complete"] is True
        assert bundle["phases"]["next_recommended_phase"] == "complete"

    def test_partial_workspace_points_to_missing_phase1(self, tmp_path):
        (tmp_path / "eval-brief.md").write_text("# Evaluation Brief\n\n## Subject\nTest\n", encoding="utf-8")
        (tmp_path / "phase1a-hater-raw.md").write_text("# Hater\n\ncontent\n", encoding="utf-8")

        bundle = build_eval_bundle.build_bundle(tmp_path)

        assert bundle["phases"]["phase0"]["complete"] is True
        assert bundle["phases"]["phase1"]["complete"] is False
        assert bundle["phases"]["next_recommended_phase"] == "phase1"
        assert "phase1b-competitive-raw.md" in bundle["phases"]["next_recommended_action"]
        assert "phase1c-strengths-raw.md" in bundle["phases"]["next_recommended_action"]

    def test_run_id_extracted_from_run_log(self, tmp_path):
        (tmp_path / "eval-brief.md").write_text("# Evaluation Brief\n", encoding="utf-8")
        (tmp_path / "run-log.md").write_text(
            "# Run log\n\n## Meta\n- run_id: `abc123xy`\n- status: in_progress\n",
            encoding="utf-8",
        )

        bundle = build_eval_bundle.build_bundle(tmp_path)

        assert bundle["run_id"] == "abc123xy"
        assert bundle["artifacts"]["run_log"]["exists"] is True

    def test_sections_are_exposed_for_markdown_artifacts(self, tmp_path):
        (tmp_path / "eval-brief.md").write_text(
            "# Evaluation Brief\n\n## Subject\nExample\n\n## Core Proposition\nUseful product\n",
            encoding="utf-8",
        )

        bundle = build_eval_bundle.build_bundle(tmp_path)
        sections = bundle["artifacts"]["eval_brief"]["sections"]

        assert sections[0]["title"] == "Evaluation Brief"
        assert any(section["title"] == "Subject" for section in sections)
        assert any(section["title"] == "Core Proposition" for section in sections)


class TestCLI:
    """CLI tests for bundle generation."""

    def test_cli_writes_output_file(self, tmp_path):
        (tmp_path / "eval-brief.md").write_text("# Evaluation Brief\n\n## Subject\nCLI\n", encoding="utf-8")
        output_path = tmp_path / "bundle.json"

        result = subprocess.run(
            [sys.executable, "scripts/build_eval_bundle.py", str(tmp_path), "-o", str(output_path)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(REPO_ROOT),
        )

        assert result.returncode == 0
        assert output_path.exists()

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["artifacts"]["eval_brief"]["exists"] is True
        assert payload["phases"]["next_recommended_phase"] == "phase1"
