#!/usr/bin/env python3
"""Build a machine-readable bundle for a mega-eval workspace.

Usage:
    python build_eval_bundle.py <workspace> [--session <name>] [--output eval-bundle.json]
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


MARKDOWN_ARTIFACTS = [
    ("eval_brief", "eval-brief.md", True, "phase0"),
    ("phase1a_hater", "phase1a-hater-raw.md", True, "phase1"),
    ("phase1b_competitive", "phase1b-competitive-raw.md", True, "phase1"),
    ("phase1c_strengths", "phase1c-strengths-raw.md", True, "phase1"),
    ("phase1d_design", "phase1d-design-raw.md", False, "phase1_optional"),
    ("phase1e_security", "phase1e-security-raw.md", False, "phase1_optional"),
    ("phase1f_durability", "phase1f-durability-raw.md", False, "phase1_optional"),
    ("phase2_synthesis", "phase2-synthesis.md", True, "phase2"),
    ("phase3_content_outline", "phase3-content-outline-raw.md", True, "phase3"),
    ("run_log", "run-log.md", False, "meta"),
]

DOCX_ARTIFACTS = [
    ("executive_summary", "00-executive-summary.docx"),
    ("hater_mode_feedback", "01-hater-mode-feedback.docx"),
    ("competitive_landscape", "02-competitive-landscape.docx"),
    ("strengths_opportunities", "03-strengths-opportunities.docx"),
    ("critical_fixes_and_design", "04-critical-fixes-and-design.docx"),
    ("content_strategy_outline", "05-content-strategy-outline.docx"),
]


def line_count(text: str) -> int:
    return 0 if not text else len(text.splitlines())


def word_count(text: str) -> int:
    return len(text.split())


def parse_markdown_sections(text: str) -> list[dict]:
    """Split markdown into generic heading-based sections."""
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
    matches = list(heading_pattern.finditer(text))
    sections: list[dict] = []

    if not matches:
        body = text.strip()
        if body:
            sections.append(
                {
                    "level": 0,
                    "title": "document",
                    "body": body,
                    "word_count": word_count(body),
                    "line_count": line_count(body),
                }
            )
        return sections

    preamble = text[: matches[0].start()].strip()
    if preamble:
        sections.append(
            {
                "level": 0,
                "title": "preamble",
                "body": preamble,
                "word_count": word_count(preamble),
                "line_count": line_count(preamble),
            }
        )

    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        title = match.group(2).strip()
        sections.append(
            {
                "level": len(match.group(1)),
                "title": title,
                "body": body,
                "word_count": word_count(body),
                "line_count": line_count(body),
            }
        )

    return sections


def extract_run_id(text: str) -> str | None:
    match = re.search(r"run_id:\s*`?([A-Za-z0-9._-]+)`?", text, re.IGNORECASE)
    return match.group(1) if match else None


def markdown_artifact_payload(workspace: Path, filename: str, required: bool, phase: str) -> dict:
    path = workspace / filename
    payload = {
        "file_name": filename,
        "path": filename,
        "required": required,
        "phase": phase,
        "exists": path.exists(),
    }
    if not path.exists():
        return payload

    text = path.read_text(encoding="utf-8")
    sections = parse_markdown_sections(text)
    payload.update(
        {
            "bytes": path.stat().st_size,
            "line_count": line_count(text),
            "word_count": word_count(text),
            "headings": [section["title"] for section in sections if section["level"] > 0],
            "sections": sections,
        }
    )
    return payload


def binary_artifact_payload(workspace: Path, filename: str) -> dict:
    path = workspace / filename
    payload = {
        "file_name": filename,
        "path": filename,
        "required": True,
        "phase": "phase4",
        "exists": path.exists(),
    }
    if not path.exists():
        return payload

    payload["bytes"] = path.stat().st_size
    return payload


def build_phase_summary(artifacts: dict[str, dict]) -> dict:
    required_phase1 = ["phase1a_hater", "phase1b_competitive", "phase1c_strengths"]
    optional_phase1 = ["phase1d_design", "phase1e_security", "phase1f_durability"]
    docx_keys = [key for key, _ in DOCX_ARTIFACTS]

    phase0_complete = artifacts["eval_brief"]["exists"]
    phase1_required_count = sum(1 for key in required_phase1 if artifacts[key]["exists"])
    phase1_complete = phase1_required_count == len(required_phase1)
    phase2_complete = artifacts["phase2_synthesis"]["exists"]
    phase3_complete = artifacts["phase3_content_outline"]["exists"]
    phase4_count = sum(1 for key in docx_keys if artifacts[key]["exists"])
    phase4_complete = phase4_count == len(docx_keys)

    if not phase0_complete:
        next_phase = "phase0"
        next_action = "Create or refresh eval-brief.md before launching downstream phases."
    elif not phase1_complete:
        next_phase = "phase1"
        missing = [artifacts[key]["file_name"] for key in required_phase1 if not artifacts[key]["exists"]]
        next_action = f"Run the missing Phase 1 required tracks: {', '.join(missing)}."
    elif not phase2_complete:
        next_phase = "phase2"
        next_action = "Synthesize Phase 1 outputs into phase2-synthesis.md."
    elif not phase3_complete:
        next_phase = "phase3"
        next_action = "Generate phase3-content-outline-raw.md from the completed synthesis."
    elif not phase4_complete:
        next_phase = "phase4"
        next_action = "Assemble the Phase 4 .docx deliverables from the existing markdown artifacts."
    else:
        next_phase = "complete"
        next_action = "All standard markdown and .docx deliverables are present."

    return {
        "phase0": {
            "complete": phase0_complete,
            "required_files": [artifacts["eval_brief"]["file_name"]],
        },
        "phase1": {
            "complete": phase1_complete,
            "required_present": phase1_required_count,
            "required_total": len(required_phase1),
            "optional_present": [
                artifacts[key]["file_name"] for key in optional_phase1 if artifacts[key]["exists"]
            ],
        },
        "phase2": {
            "complete": phase2_complete,
            "required_files": [artifacts["phase2_synthesis"]["file_name"]],
        },
        "phase3": {
            "complete": phase3_complete,
            "required_files": [artifacts["phase3_content_outline"]["file_name"]],
        },
        "phase4": {
            "complete": phase4_complete,
            "present_count": phase4_count,
            "required_total": len(docx_keys),
            "present_files": [artifacts[key]["file_name"] for key in docx_keys if artifacts[key]["exists"]],
        },
        "resume_ready": next_phase not in {"phase0", "complete"},
        "next_recommended_phase": next_phase,
        "next_recommended_action": next_action,
    }


def list_session_dirs(workspace: Path) -> list[Path]:
    sessions = workspace / "sessions"
    if not sessions.is_dir():
        return []
    return sorted(path for path in sessions.iterdir() if path.is_dir() and not path.name.startswith("."))


def session_has_artifacts(session_dir: Path) -> bool:
    return any((session_dir / filename).exists() for _, filename, _, _ in MARKDOWN_ARTIFACTS)


def has_root_artifacts(workspace: Path) -> bool:
    return (workspace / "eval-brief.md").exists()


def resolve_artifact_root(workspace: Path, session: str | None = None) -> Path:
    """Resolve the directory that holds mega-eval artifacts.

    See plan KTD3: prefer --session; fail closed on ambiguous root+sessions;
    auto-pick only when exactly one populated session exists and the root is empty.
    """
    workspace = workspace.resolve()
    session_dirs = list_session_dirs(workspace)
    populated = [path for path in session_dirs if session_has_artifacts(path)]

    if session is not None:
        candidate = workspace / "sessions" / session
        if not candidate.is_dir():
            available = ", ".join(path.name for path in session_dirs) or "(none)"
            raise SystemExit(
                f"Session not found: sessions/{session}\nAvailable sessions: {available}"
            )
        return candidate.resolve()

    root_has = has_root_artifacts(workspace)

    if root_has and populated:
        names = ", ".join(path.name for path in populated)
        raise SystemExit(
            "Ambiguous workspace: eval-brief.md exists at the workspace root and "
            f"populated sessions/ dirs were found ({names}). "
            "Pass --session <name> to choose a session, or remove the root artifacts."
        )

    if root_has:
        return workspace

    if len(populated) == 1:
        return populated[0].resolve()

    if len(populated) > 1:
        names = ", ".join(path.name for path in populated)
        raise SystemExit(
            f"Multiple populated sessions found ({names}). Pass --session <name>."
        )

    return workspace


def build_bundle(workspace: Path, session: str | None = None) -> dict:
    requested = workspace.resolve()
    artifact_root = resolve_artifact_root(requested, session=session)
    artifacts: dict[str, dict] = {}

    for key, filename, required, phase in MARKDOWN_ARTIFACTS:
        artifacts[key] = markdown_artifact_payload(artifact_root, filename, required, phase)

    for key, filename in DOCX_ARTIFACTS:
        artifacts[key] = binary_artifact_payload(artifact_root, filename)

    run_id = None
    if artifacts["run_log"]["exists"]:
        run_log_path = artifact_root / artifacts["run_log"]["file_name"]
        run_id = extract_run_id(run_log_path.read_text(encoding="utf-8"))

    phase_summary = build_phase_summary(artifacts)
    present_files = [payload["file_name"] for payload in artifacts.values() if payload["exists"]]

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(requested),
        "artifact_root": str(artifact_root),
        "run_id": run_id,
        "present_file_count": len(present_files),
        "present_files": sorted(present_files),
        "artifacts": artifacts,
        "phases": phase_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a machine-readable mega-eval bundle")
    parser.add_argument("workspace", help="Workspace directory containing mega-eval artifacts")
    parser.add_argument(
        "--session",
        help="Session directory name under sessions/ when artifacts live in sessions/<name>/",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON path (defaults to <artifact-root>/eval-bundle.json)",
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise SystemExit(f"Workspace directory not found: {workspace}")

    bundle = build_bundle(workspace, session=args.session)
    artifact_root = Path(bundle["artifact_root"])
    output_path = Path(args.output).resolve() if args.output else artifact_root / "eval-bundle.json"
    output_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote bundle to: {output_path}")


if __name__ == "__main__":
    main()
