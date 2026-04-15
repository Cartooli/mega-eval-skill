#!/usr/bin/env python3
"""Append structured run events to a JSONL file."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    """Return the current UTC time in ISO-8601 format with Z suffix."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_event(
    *,
    event_type: str,
    run_id: str,
    phase: str | None = None,
    status: str | None = None,
    artifact_path: str | None = None,
    prompt_id: str | None = None,
    duration_ms: int | None = None,
    fallback_used: str | None = None,
    details: str | None = None,
    timestamp: str | None = None,
) -> dict:
    """Build one structured event payload."""
    event = {
        "timestamp": timestamp or utc_now_iso(),
        "run_id": run_id,
        "event_type": event_type,
    }

    optional_fields = {
        "phase": phase,
        "status": status,
        "artifact_path": artifact_path,
        "prompt_id": prompt_id,
        "duration_ms": duration_ms,
        "fallback_used": fallback_used,
        "details": details,
    }

    for key, value in optional_fields.items():
        if value is not None:
            event[key] = value

    return event


def append_event(log_path: Path, event: dict) -> None:
    """Append one JSON event line to a JSONL file."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Append a structured event to run-log.jsonl")
    parser.add_argument("log_path", help="Path to the JSONL log file")
    parser.add_argument("event_type", help="Structured event type, eg phase_start")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    parser.add_argument("--phase", help="Phase name, eg phase1")
    parser.add_argument("--status", help="Status label, eg ok/pass/warn/fail")
    parser.add_argument("--artifact-path", help="Artifact path associated with the event")
    parser.add_argument("--prompt-id", help="Prompt registry ID associated with the event")
    parser.add_argument("--duration-ms", type=int, help="Duration in milliseconds")
    parser.add_argument("--fallback-used", help="Fallback path used by the runtime")
    parser.add_argument("--details", help="Short string with extra event context")
    parser.add_argument("--timestamp", help="Explicit timestamp override for testing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    event = build_event(
        event_type=args.event_type,
        run_id=args.run_id,
        phase=args.phase,
        status=args.status,
        artifact_path=args.artifact_path,
        prompt_id=args.prompt_id,
        duration_ms=args.duration_ms,
        fallback_used=args.fallback_used,
        details=args.details,
        timestamp=args.timestamp,
    )
    append_event(Path(args.log_path).resolve(), event)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
