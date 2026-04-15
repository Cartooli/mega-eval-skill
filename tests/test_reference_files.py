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


def test_phase_c_origin_doc_and_sample_bundle_exist():
    origin_doc = REPO_ROOT / "docs/brainstorms/2026-04-15-mega-eval-phase-c-platform-upgrades-requirements.md"
    sample_bundle = REPO_ROOT / "examples/sample-run/eval-bundle.json"

    assert origin_doc.exists(), "Expected Phase C origin requirements doc to exist"
    assert sample_bundle.exists(), "Expected sample eval bundle to exist"


def test_phase_skill_files_exist():
    required_skill_files = [
        "skills/mega-eval-brief/SKILL.md",
        "skills/mega-eval-hater/SKILL.md",
        "skills/mega-eval-competitive/SKILL.md",
        "skills/mega-eval-strengths/SKILL.md",
        "skills/mega-eval-design/SKILL.md",
        "skills/mega-eval-security/SKILL.md",
        "skills/mega-eval-durability/SKILL.md",
        "skills/mega-eval-synthesis/SKILL.md",
        "skills/mega-eval-content-outline/SKILL.md",
        "skills/mega-eval-deliverables/SKILL.md",
    ]

    missing = [path for path in required_skill_files if not (REPO_ROOT / path).exists()]

    assert not missing, f"Missing expected phase skill files: {missing}"


def test_plugin_packaged_skill_entries_exist():
    required_plugin_entries = [
        "plugins/mega-eval/skills/mega-eval/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-brief/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-competitive/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-hater/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-strengths/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-design/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-security/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-durability/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-synthesis/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-content-outline/SKILL.md",
        "plugins/mega-eval/skills/mega-eval-deliverables/SKILL.md",
    ]

    missing = [path for path in required_plugin_entries if not (REPO_ROOT / path).exists()]

    assert not missing, f"Missing expected plugin-packaged skill entries: {missing}"


def test_expected_scripts_exist():
    required_scripts = [
        "scripts/ingest.py",
        "scripts/suggest_learnings.py",
        "scripts/build_eval_bundle.py",
    ]

    missing = [path for path in required_scripts if not (REPO_ROOT / path).exists()]

    assert not missing, f"Missing expected helper scripts: {missing}"
