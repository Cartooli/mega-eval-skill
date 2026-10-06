#!/usr/bin/env python3
"""Preflight: verify mega-eval references/ can resolve and contains required files.

Usage:
    python3 scripts/check_references.py [base-path]

base-path defaults to the current working directory. Resolution follows the
same first-match order as skills/README.md:
  1. <base>/references/
  2. <base>/../../references/   (skills/<name> inside a full clone)
  3. <base>/../mega-eval/references/  (phase skill beside mega-eval package)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_REFERENCE_FILES = [
    "pipeline-checklist.md",
    "subagent-prompts.md",
    "model-selection.md",
    "learnings.md",
    "design-audit-template.md",
    "security-audit-template.md",
    "durability-audit-template.md",
]


def candidate_reference_roots(base: Path) -> list[Path]:
    base = base.resolve()
    return [
        base / "references",
        base.parent.parent / "references",
        base.parent / "mega-eval" / "references",
    ]


def resolve_references_root(base: Path) -> Path | None:
    seen: set[Path] = set()
    for candidate in candidate_reference_roots(base):
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if candidate.is_dir():
            return resolved
    return None


def missing_reference_files(references_root: Path) -> list[str]:
    return [
        name
        for name in REQUIRED_REFERENCE_FILES
        if not (references_root / name).is_file()
    ]


def check_references(base: Path) -> list[str]:
    """Return human-readable error lines; empty list means OK."""
    root = resolve_references_root(base)
    if root is None:
        tried = ", ".join(str(path) for path in candidate_reference_roots(base))
        return [f"references/ not found relative to {base.resolve()} (tried: {tried})"]
    missing = missing_reference_files(root)
    if missing:
        return [f"Missing under {root}: {name}" for name in missing]
    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fail if mega-eval references/ cannot resolve or required files are missing"
    )
    parser.add_argument(
        "base",
        nargs="?",
        default=".",
        help="Skill or install directory to resolve from (default: cwd)",
    )
    args = parser.parse_args()
    base = Path(args.base)
    if not base.exists():
        print(f"Base path not found: {base}", file=sys.stderr)
        raise SystemExit(2)

    errors = check_references(base)
    if errors:
        print("References preflight failed:", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        raise SystemExit(1)

    root = resolve_references_root(base)
    print(f"References OK: {root}")


if __name__ == "__main__":
    main()
