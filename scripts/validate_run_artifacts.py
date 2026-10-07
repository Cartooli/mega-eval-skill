#!/usr/bin/env python3
"""Validate a mega-eval workspace against layered gate file sets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python scripts/validate_run_artifacts.py` without installing a package.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import validate_artifact  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"

# filename -> schema basename
ARTIFACT_SCHEMAS: dict[str, str] = {
    "eval-brief.md": "eval-brief.schema.json",
    "phase1b-competitive-raw.md": "phase1b-competitive.schema.json",
    "phase1c-strengths-raw.md": "phase1c-strengths.schema.json",
    "phase1d-design-raw.md": "phase1d-design.schema.json",
    "phase1e-security-raw.md": "phase1e-security.schema.json",
    "phase1f-durability-raw.md": "phase1f-durability.schema.json",
    "phase2-synthesis.md": "phase2-synthesis.schema.json",
    "phase3-content-outline-raw.md": "phase3-content-outline.schema.json",
}

REQUIRED_CORE = (
    "eval-brief.md",
    "phase1b-competitive-raw.md",
    "phase1c-strengths-raw.md",
)
OPTIONAL_RAW = (
    "phase1d-design-raw.md",
    "phase1e-security-raw.md",
    "phase1f-durability-raw.md",
)

GATE_SETS: dict[str, tuple[str, ...]] = {
    "pre-phase1": ("eval-brief.md",),
    "pre-phase2": REQUIRED_CORE + OPTIONAL_RAW,
    "pre-phase3": ("phase2-synthesis.md",),
    "pre-phase4": REQUIRED_CORE
    + OPTIONAL_RAW
    + ("phase2-synthesis.md", "phase3-content-outline-raw.md"),
}

# Filenames that must exist for a gate (optionals are present-only).
GATE_REQUIRED: dict[str, frozenset[str]] = {
    "pre-phase1": frozenset({"eval-brief.md"}),
    "pre-phase2": frozenset(REQUIRED_CORE),
    "pre-phase3": frozenset({"phase2-synthesis.md"}),
    "pre-phase4": frozenset(
        REQUIRED_CORE + ("phase2-synthesis.md", "phase3-content-outline-raw.md")
    ),
}


def resolve_targets(
    *,
    workspace: Path | None,
    explicit_files: list[Path],
    gate: str,
) -> tuple[list[Path], list[str]]:
    """Return (paths to validate, missing-required error messages)."""
    missing: list[str] = []
    targets: list[Path] = []

    if explicit_files:
        for path in explicit_files:
            name = path.name
            if name not in ARTIFACT_SCHEMAS:
                missing.append(f"Unknown artifact filename (no schema mapping): {name}")
                continue
            if not path.exists():
                missing.append(f"Missing artifact: {path}")
                continue
            targets.append(path)
        return targets, missing

    if workspace is None:
        missing.append("Provide a workspace directory or --file paths.")
        return targets, missing

    required = GATE_REQUIRED[gate]
    for name in GATE_SETS[gate]:
        path = workspace / name
        if path.exists():
            targets.append(path)
        elif name in required:
            missing.append(f"Missing required artifact for {gate}: {name}")

    return targets, missing


def validate_paths(paths: list[Path]) -> list[str]:
    """Validate each path; return human-readable error lines."""
    errors: list[str] = []
    for path in paths:
        schema_name = ARTIFACT_SCHEMAS[path.name]
        schema_path = SCHEMAS_DIR / schema_name
        if not schema_path.exists():
            errors.append(f"Schema not found for {path.name}: {schema_path}")
            continue
        file_errors = validate_artifact.validate_file(path, schema_path)
        if file_errors:
            errors.append(f"Validation failed for {path.name}:")
            errors.extend(f"- {err}" for err in file_errors)
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate mega-eval workspace artifacts for a pipeline gate."
    )
    parser.add_argument(
        "--gate",
        required=True,
        choices=sorted(GATE_SETS.keys()),
        help="Which gate file set to validate (required).",
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        help="Workspace directory containing phase markdown artifacts",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        dest="files",
        help="Explicit artifact path (repeatable). When set, skips workspace discovery.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    workspace = Path(args.workspace).resolve() if args.workspace else None
    explicit = [Path(p).resolve() for p in args.files]

    if workspace is not None and not workspace.is_dir() and not explicit:
        print(f"Workspace is not a directory: {workspace}", file=sys.stderr)
        return 2

    targets, missing = resolve_targets(
        workspace=workspace, explicit_files=explicit, gate=args.gate
    )
    if missing:
        for line in missing:
            print(line, file=sys.stderr)
        return 1 if any("Missing required" in m or "Unknown" in m for m in missing) else 2

    if not targets and not missing:
        print(f"No artifacts to validate for gate {args.gate}.", file=sys.stderr)
        return 1

    errors = validate_paths(targets)
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1

    names = ", ".join(p.name for p in targets) or "(none)"
    print(f"Validation passed for {args.gate}: {names}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
