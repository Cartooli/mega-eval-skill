---
title: "feat: Mega-eval Phase C machine-readable bundle and resume guidance"
type: feat
status: active
date: 2026-04-15
origin: docs/brainstorms/2026-04-15-mega-eval-phase-c-platform-upgrades-requirements.md
---

# feat: Mega-eval Phase C machine-readable bundle and resume guidance

## Overview

Add a small, repo-native platform layer on top of the current mega-eval artifact contract:

1. a stdlib-only helper that inspects a workspace and emits a stable machine-readable JSON bundle
2. run-status metadata in that bundle so maintainers can resume from the first incomplete phase instead of blindly rerunning everything
3. documentation and examples that make the new flow discoverable without changing the existing markdown or `.docx` outputs

This is the final Phase C tranche from the broader improvement program. It is intentionally scoped as **one mergeable PR** because the helper, docs, example, and tests all reinforce the same contract.

## Problem Statement / Motivation

The repo’s current evaluation flow is strong for human readers but weaker for platform-level reuse:

- Markdown intermediates are easy to inspect manually but awkward for downstream tooling.
- There is no canonical helper for determining whether a workspace is partial, resumable, or effectively complete.
- The root skill and docs imply a linear rerun flow even when artifacts already exist and could be reused safely.

The highest-leverage Phase C slice is therefore not a runtime rewrite or caching system. It is a **workspace inspection/export helper** that formalizes current artifact expectations and adds lightweight resume semantics around them.

## Proposed Solution

Ship one bounded tranche with three implementation units:

1. **C1 — Add a bundle builder script with resume/status metadata**
2. **C2 — Document resume/reuse and machine-readable export**
3. **C3 — Add example output and regression tests**

The core artifact will be a JSON file such as `eval-bundle.json` containing:

- bundle metadata and schema version
- workspace path and discovered artifact paths
- per-artifact presence, size, and lightweight content metadata
- phase completion status and the next recommended phase/action
- optional `.docx` deliverable presence, when present

## Implementation Units

## Unit C1 — Add machine-readable bundle builder

**Goal**
Create a stdlib-only script that inspects a mega-eval workspace and emits a stable JSON bundle.

**Files**
- `scripts/build_eval_bundle.py` (new)

**Patterns to follow**
- Mirror the repo’s existing script style: portable, documented, low-dependency, explicit CLI usage
- Treat the current artifact filenames as the canonical contract
- Prefer deterministic metadata and simple markdown section extraction over fragile deep parsing

**Approach**
- Accept a workspace path and optional output path
- Discover standard markdown artifacts:
  - `eval-brief.md`
  - `phase1a-hater-raw.md`
  - `phase1b-competitive-raw.md`
  - `phase1c-strengths-raw.md`
  - optional `phase1d-design-raw.md`
  - optional `phase1e-security-raw.md`
  - optional `phase1f-durability-raw.md`
  - `phase2-synthesis.md`
  - `phase3-content-outline-raw.md`
  - optional `run-log.md`
- Discover Phase 4 `.docx` deliverables when present
- Emit stable JSON with:
  - `schema_version`
  - `workspace`
  - `generated_at`
  - `run_id` when recoverable from `run-log.md`
  - `artifacts` map
  - `phases` status summary
  - `next_recommended_phase`
  - `next_recommended_action`
- Include lightweight content structure for markdown artifacts (for example heading inventory, line count, word count, and short section bodies) without inventing semantic judgments

**Execution note**
- The script should be safe to run repeatedly and should only write the explicit output file the user asked for

**Verification**
- Run it against `examples/sample-run/`
- Run it against a partial temp workspace in tests
- Confirm it reports partial/incomplete states correctly

## Unit C2 — Document resume/reuse and export flow

**Goal**
Make the helper discoverable and codify a repo-native resume policy.

**Files**
- `SKILL.md`
- `README.md`
- `references/pipeline-checklist.md`

**Patterns to follow**
- Keep the user-facing quickstart intact
- Add concise advanced guidance rather than sprawling process copy
- Preserve existing artifact names and pipeline order

**Approach**
- In `SKILL.md`, add a short Phase 0 note that existing artifacts in the target workspace can be reused and that work may resume from the first incomplete phase when appropriate
- In `README.md`, add a small section describing `scripts/build_eval_bundle.py`, what it outputs, and how it helps with resume/review workflows
- In `references/pipeline-checklist.md`, add a pre-flight item reminding maintainers to inspect existing artifacts before rerunning phases

**Execution note**
- Do not imply automatic orchestration resume; this tranche adds guidance plus inspection/export, not an autonomous rerun engine

**Verification**
- A maintainer starting from `README.md` or `SKILL.md` can discover the helper and understand when to reuse artifacts

## Unit C3 — Example bundle and regression tests

**Goal**
Make the new JSON contract concrete and protected by tests.

**Files**
- `examples/sample-run/eval-bundle.json` (new)
- `tests/test_build_eval_bundle.py` (new)

**Patterns to follow**
- Example output should be generated from the checked-in sample run, not hand-wavy pseudo-JSON
- Tests should be focused and contract-oriented, not overly coupled to every line of output

**Approach**
- Generate `examples/sample-run/eval-bundle.json` from the checked-in sample run artifacts
- Add tests for:
  - complete sample-run export
  - partial workspace export
  - next-phase recommendation logic
  - run-id extraction when `run-log.md` is present

**Execution note**
- Prefer stable assertions on keys, statuses, and file presence over brittle snapshot testing of timestamps

**Verification**
- `pytest -q` passes locally
- Example bundle stays in sync with the script behavior

## Technical Considerations

- The JSON schema should be intentionally modest: enough for tooling and review, not a full semantic AST for every markdown document.
- Resume support is advisory in this tranche. The script can tell you where to continue; it does not drive the full pipeline automatically.
- `.docx` presence should be treated as optional metadata, because partial runs may stop before Phase 4.
- The helper should remain useful in both `examples/sample-run/` and user-created workspaces that only contain some of the expected files.

## System-Wide Impact

### Interaction Graph

- Maintainer or power user runs `scripts/build_eval_bundle.py`
- The script reads existing workspace artifacts
- The script emits `eval-bundle.json`
- Maintainers use that bundle to inspect status, share results, diff runs, or decide where to resume

### Error & Failure Propagation

- If a file is missing, the script should mark it missing rather than failing the whole export
- If `run-log.md` is malformed or absent, the script should degrade gracefully and omit `run_id`
- If markdown is unusually formatted, the helper should still export file metadata even if section extraction is shallow

### State Lifecycle Risks

- Main risk is accidental overreach into orchestration logic
  - **Mitigation:** keep the helper read-mostly and status-oriented
- Main schema risk is overfitting to current prose structure
  - **Mitigation:** prefer generic heading extraction and artifact metadata

### API Surface Parity

- No changes to existing markdown artifact names
- No changes to existing `.docx` deliverables
- One new optional artifact: `eval-bundle.json`

## Acceptance Criteria

- [ ] `scripts/build_eval_bundle.py` exists and can inspect a workspace into stable JSON
- [ ] The JSON includes artifact presence and per-phase status information
- [ ] The JSON includes a next recommended phase/action for partial runs
- [ ] The helper remains usable when optional artifacts are absent
- [ ] `README.md` documents the helper and its intended use
- [ ] `SKILL.md` documents reuse/resume guidance without implying a full orchestration rewrite
- [ ] `references/pipeline-checklist.md` reminds maintainers to inspect existing artifacts before rerunning phases
- [ ] `examples/sample-run/eval-bundle.json` exists
- [ ] Tests cover the script’s core contract and pass under pytest

## Success Metrics

- Maintainers can determine resume state in under a minute from a workspace
- Downstream tooling can consume a stable JSON representation without ad hoc scraping
- The repo gains richer platform ergonomics without changing the user-facing deliverable contract

## Dependencies & Risks

- **Dependency:** current artifact filenames remain canonical
- **Risk:** JSON schema becomes too bespoke or too noisy
  - **Mitigation:** keep it small, deterministic, and artifact-driven
- **Risk:** docs overstate what "resume support" means
  - **Mitigation:** explicitly frame this tranche as inspection/reuse guidance, not automatic rerun orchestration

## Sources & References

### Origin
- **Origin document:** [docs/brainstorms/2026-04-15-mega-eval-phase-c-platform-upgrades-requirements.md](../brainstorms/2026-04-15-mega-eval-phase-c-platform-upgrades-requirements.md)

### Internal References
- Improvement program roadmap: [docs/plans/2026-04-15-002-feat-mega-eval-improvement-program-plan.md](2026-04-15-002-feat-mega-eval-improvement-program-plan.md)
- Root skill contract: [SKILL.md](../../SKILL.md)
- Existing pipeline checklist: [references/pipeline-checklist.md](../../references/pipeline-checklist.md)
- Existing scripts: [scripts/ingest.py](../../scripts/ingest.py), [scripts/suggest_learnings.py](../../scripts/suggest_learnings.py)
- Sample run artifacts: [examples/sample-run/README.md](../../examples/sample-run/README.md)

---

Plan written to `docs/plans/2026-04-15-004-feat-mega-eval-phase-c-platform-upgrades-plan.md`.
