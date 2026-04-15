#!/usr/bin/env python3
"""Regression checks for required Mega Eval reference files."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def test_required_reference_files_exist():
    required_files = [
        "references/pipeline-checklist.md",
        "references/subagent-prompts.md",
        "references/model-selection.md",
        "references/learnings.md",
        "references/design-audit-template.md",
        "references/security-audit-template.md",
        "references/durability-audit-template.md",
    ]

    missing = [path for path in required_files if not (REPO_ROOT / path).exists()]

    assert not missing, f"Missing required reference files: {missing}"


def test_security_durability_origin_doc_exists():
    origin_doc = REPO_ROOT / "docs/brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md"

    assert origin_doc.exists(), "Expected security/durability origin requirements doc to exist"
