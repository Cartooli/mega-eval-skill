#!/usr/bin/env python3
"""Tests for the canonical subagent prompt registry."""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
PROMPT_REGISTRY_PATH = REPO_ROOT / "references" / "subagent-prompts.md"
SKILL_PATH = REPO_ROOT / "SKILL.md"


PROMPT_ID_RE = re.compile(r"^## Prompt ID: `([^`]+)`\s*$", re.MULTILINE)
SKILL_REFERENCE_RE = re.compile(r"Use \*\*Prompt ID\*\* `([^`]+)`")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_prompt_registry_ids_are_unique():
    registry_text = load_text(PROMPT_REGISTRY_PATH)
    prompt_ids = PROMPT_ID_RE.findall(registry_text)

    assert prompt_ids
    assert len(prompt_ids) == len(set(prompt_ids))


def test_skill_prompt_references_exist_in_registry():
    registry_text = load_text(PROMPT_REGISTRY_PATH)
    registry_ids = set(PROMPT_ID_RE.findall(registry_text))
    skill_text = load_text(SKILL_PATH)
    referenced_ids = SKILL_REFERENCE_RE.findall(skill_text)

    assert referenced_ids
    assert set(referenced_ids).issubset(registry_ids)


def test_registry_contains_expected_prompt_ids():
    registry_text = load_text(PROMPT_REGISTRY_PATH)
    registry_ids = set(PROMPT_ID_RE.findall(registry_text))

    assert registry_ids == {
        "phase1a.hater.v1",
        "phase1b.competitive.v1",
        "phase1c.strengths.v1",
        "phase1d.design.v1",
        "phase3.content-outline.v1",
    }
