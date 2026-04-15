#!/usr/bin/env python3
"""Tests for scripts/log_event.py."""

import json
import subprocess
import sys
from pathlib import Path

# Add scripts/ to path so we can import log_event
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import log_event


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_build_event_with_optional_fields():
    event = log_event.build_event(
        event_type="artifact_validated",
        run_id="abc12345",
        phase="phase2",
        status="pass",
        artifact_path="phase2-synthesis.md",
        prompt_id="phase1b.competitive.v1",
        duration_ms=1234,
        fallback_used="none",
        details="contract=phase2-synthesis",
        timestamp="2026-04-15T12:00:00Z",
    )

    assert event == {
        "timestamp": "2026-04-15T12:00:00Z",
        "run_id": "abc12345",
        "event_type": "artifact_validated",
        "phase": "phase2",
        "status": "pass",
        "artifact_path": "phase2-synthesis.md",
        "prompt_id": "phase1b.competitive.v1",
        "duration_ms": 1234,
        "fallback_used": "none",
        "details": "contract=phase2-synthesis",
    }


def test_append_event_writes_jsonl(tmp_path):
    log_path = tmp_path / "run-log.jsonl"
    event = log_event.build_event(
        event_type="phase_start",
        run_id="abc12345",
        phase="phase1",
        status="ok",
        timestamp="2026-04-15T12:00:00Z",
    )

    log_event.append_event(log_path, event)

    lines = read_jsonl(log_path)
    assert lines == [event]


def test_cli_appends_event(tmp_path):
    log_path = tmp_path / "run-log.jsonl"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/log_event.py",
            str(log_path),
            "fallback_used",
            "--run-id",
            "abc12345",
            "--phase",
            "phase1d",
            "--status",
            "warn",
            "--fallback-used",
            "webfetch_only",
            "--details",
            "browser unavailable",
            "--timestamp",
            "2026-04-15T12:00:00Z",
        ],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(Path(__file__).parent.parent),
    )

    assert result.returncode == 0
    lines = read_jsonl(log_path)
    assert lines == [
        {
            "timestamp": "2026-04-15T12:00:00Z",
            "run_id": "abc12345",
            "event_type": "fallback_used",
            "phase": "phase1d",
            "status": "warn",
            "fallback_used": "webfetch_only",
            "details": "browser unavailable",
        }
    ]
