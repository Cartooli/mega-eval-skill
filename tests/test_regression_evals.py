#!/usr/bin/env python3
"""Deterministic regression corpus checks for representative mega-eval runs."""

import sys
from pathlib import Path

# Add scripts/ to path so we can import validate_artifact
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import validate_artifact


REPO_ROOT = Path(__file__).parent.parent
EVALS_DIR = REPO_ROOT / "tests" / "evals"
SCHEMAS_DIR = REPO_ROOT / "schemas"


def read_text(relative_path: str) -> str:
    return (EVALS_DIR / relative_path).read_text(encoding="utf-8")


def test_text_only_case_skips_phase_1d_explicitly():
    text = read_text("text_only/eval-brief.md")
    assert "**Primary URL for Phase 1D:** n/a" in text
    assert "**Audit decision:** skipped" in text


def test_sparse_input_case_preserves_open_questions():
    text = read_text("sparse_input/eval-brief.md")
    assert "## Open Questions" in text
    assert text.count("- ") >= 4
    assert "Unknown" in text or "inferred" in text.lower()


def test_limited_data_competitive_case_states_confidence_limits():
    text = read_text("limited_data_competitive/phase1b-competitive-raw.md")
    lowered = text.lower()
    assert "limited public data" in lowered
    assert "confidence" in lowered


def test_design_audit_fallback_case_avoids_false_visual_claims():
    text = read_text("design_audit_fallback/phase1d-design-raw.md")
    lowered = text.lower()
    assert "tier c" in lowered
    assert "not to invent visual feedback" in lowered
    assert "could not verify layout" in lowered


def test_synthesis_tension_case_preserves_unresolved_tension():
    text = read_text("synthesis_tension/phase2-synthesis.md")
    assert "## Unresolved Tensions" in text
    assert "both can be true" in text.lower()


def test_eval_corpus_artifacts_still_pass_relevant_contracts():
    cases = [
        ("text_only/eval-brief.md", "eval-brief.schema.json"),
        ("sparse_input/eval-brief.md", "eval-brief.schema.json"),
        ("limited_data_competitive/phase1b-competitive-raw.md", "phase1b-competitive.schema.json"),
        ("synthesis_tension/phase2-synthesis.md", "phase2-synthesis.schema.json"),
    ]

    for artifact_rel, schema_name in cases:
        errors = validate_artifact.validate_file(EVALS_DIR / artifact_rel, SCHEMAS_DIR / schema_name)
        assert errors == [], f"{artifact_rel} failed contract validation: {errors}"
