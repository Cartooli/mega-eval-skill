---
title: "feat: Mega-eval improvement program"
type: feat
status: active
date: 2026-04-15
origin: docs/brainstorms/2026-04-15-mega-eval-improvement-program-requirements.md
---

# feat: Mega-eval improvement program

## Overview

Ship a **multi-PR improvement program** that makes mega-eval easier to install, safer to evolve, and easier to execute without breaking the existing full pipeline. The first tranche is **operational hardening**: bring thin-skill and plugin packaging into parity with the now-expanded Phase 1 surface, align `scripts/ingest.py` with the canonical Evaluation Brief contract, and extend CI so core skill/docs/reference changes are validated automatically.

This plan carries forward the source requirements doc as the product definition and converts it into an execution-ready build list with explicit PR boundaries, sequencing, and acceptance criteria (see origin: `docs/brainstorms/2026-04-15-mega-eval-improvement-program-requirements.md`).

## Problem Statement / Motivation

Mega-eval’s functionality has outpaced its productization:

- The full pipeline now includes Phase 1E and 1F, but thin-skill and plugin packaging do not yet fully reflect the expanded phase surface.
- Repo docs and install diagrams are at risk of drift whenever `SKILL.md`, `references/`, and `skills/` evolve at different speeds.
- `scripts/ingest.py` still emits an older brief shape than the current root `SKILL.md`, creating a contract mismatch for anyone using the helper script.
- CI currently validates plugin manifests and symlinks only; it does not exercise `SKILL.md`, `references/`, `scripts/`, or the repo’s Python tests when those change.

The right move is not a large redesign. It is a phased hardening program that preserves existing file contracts while reducing drift and making future feature work safer.

## Proposed Solution

## Program shape

Implement the work in three ordered tranches:

1. **Phase A — Operational hardening**  
   Immediate, merge-ready, low-risk work to bring packaging, docs, ingestion, and validation into parity with the current skill surface.
2. **Phase B — Execution-quality improvements**  
   Planning and workflow ergonomics that make future repo changes faster and more reliable.
3. **Phase C — Broader platform upgrades**  
   Higher-carrying-cost improvements such as rerun support, richer machine-readable outputs, and other structural enhancements.

Only **Phase A** is intended for immediate implementation from this plan. Phases B and C are deliberately captured as follow-on work so the repo has a concrete roadmap without forcing one oversized delivery.

## Phase A scope

Phase A is split into **four PR-sized implementation units**:

1. **A1 — Ingestion contract alignment**
2. **A2 — Thin-skill and plugin parity**
3. **A3 — Documentation and install parity**
4. **A4 — CI validation expansion**

Each unit is independently reviewable, non-breaking, and can land in order on top of the default branch.

## Implementation Units

## Unit A1 — Ingestion contract alignment

**Goal**  
Update `scripts/ingest.py` so its generated Evaluation Brief template matches the current canonical contract defined in root `SKILL.md`.

**Why first**  
This is a narrow contract fix with strong testability and low coupling. Landing it early gives the repo a cleaner source-of-truth boundary before packaging and docs are expanded further.

**Files**
- `scripts/ingest.py`
- `tests/test_ingest.py`
- `SKILL.md` (read only for schema parity check; edit only if a contract clarification is truly needed)

**Patterns to follow**
- Preserve the existing `generate_brief_template()` structure and test style in `tests/test_ingest.py`
- Treat the root `SKILL.md` Evaluation Brief section as the canonical schema
- Keep outputs concise and markdown-first; do not introduce implementation-specific fields not present in the skill contract

**Approach**
- Add the newer brief sections needed by the full pipeline, including the audit-decision blocks and model-fit/audit-related fields now required by the root skill.
- Keep the script backward-compatible as a markdown helper; do not turn it into an orchestration engine.
- Update tests so required sections are asserted explicitly.

**Execution note**
- Test-first / contract-first: extend tests to express the new brief shape, then update the generator.

**Test scenarios**
- Generated brief contains all current required section headers from the root skill contract
- Multiple-source and truncation behavior still work
- Existing CLI behavior remains intact

**Verification**
- `python3 -m pytest -q`
- Manual diff between `scripts/ingest.py` output template and the root `SKILL.md` Evaluation Brief section shows parity

## Unit A2 — Thin-skill and plugin parity

**Goal**  
Bring phase-slice packaging into parity with the current pipeline surface by adding the missing thin skills and plugin entries needed for the post-1E/1F world.

**Files**
- `skills/README.md`
- `skills/mega-eval-security/SKILL.md` (new)
- `skills/mega-eval-durability/SKILL.md` (new)
- `plugins/mega-eval/skills/mega-eval-design/SKILL.md` (symlink or equivalent package entry if missing)
- `plugins/mega-eval/skills/mega-eval-security/SKILL.md` (new link/entry)
- `plugins/mega-eval/skills/mega-eval-durability/SKILL.md` (new link/entry)
- `.claude-plugin/marketplace.json`
- `plugins/mega-eval/.claude-plugin/plugin.json`

**Patterns to follow**
- Mirror the thin-skill style of `skills/mega-eval-design/SKILL.md`
- Preserve the shared-`references/` model from `docs/plans/2026-03-24-004-feat-mega-eval-sub-skills-plan.md`
- Keep thin skills short: frontmatter, shared methodology location, reads/writes, opt-out behavior if applicable, next steps

**Approach**
- Add 1E and 1F thin skills that point to `references/security-audit-template.md`, `references/durability-audit-template.md`, `references/subagent-prompts.md`, and the root `SKILL.md`.
- Ensure plugin consumers can access the same slices by adding the matching packaged skill entries.
- Treat `mega-eval-design` plugin parity as part of this unit if it is still missing from the plugin package.
- If plugin-visible surface area changes, bump both plugin version fields together.

**Execution note**
- Pattern-following, no prompt duplication.

**Test scenarios**
- New thin-skill files resolve shared references using the documented path strategy
- Plugin skill symlinks or packaged paths resolve without breakage
- Skill inventory in `skills/README.md` matches the real directories

**Verification**
- `python3 -m json.tool .claude-plugin/marketplace.json > /dev/null`
- `python3 -m json.tool plugins/mega-eval/.claude-plugin/plugin.json > /dev/null`
- Symlink/path validation for `plugins/mega-eval/skills/*`

## Unit A3 — Documentation and install parity

**Goal**  
Make repo docs accurately describe the real skill inventory, required reference files, plugin packaging behavior, and install paths.

**Files**
- `README.md`
- `skills/README.md`
- `MAINTAINERS.md` (only if release or maintenance guidance needs parity updates)

**Patterns to follow**
- Preserve the repo’s current README tone and install-path structure
- Keep root `README.md` as the user-facing install and usage source of truth
- Use `skills/README.md` for the thin-skill inventory and path-resolution contract

**Approach**
- Update skill counts and phase coverage to include the current Phase 1 surface.
- Ensure the repository layout and manual install trees include required reference files such as `references/model-selection.md`.
- Clarify plugin vs. git/manual install parity so users understand which surfaces they get from each path.

**Execution note**
- Documentation-only, but validate against actual tree contents rather than editing prose in isolation.

**Test scenarios**
- No section claims a skill count or folder inventory that disagrees with the repo tree
- Manual install examples mention all required reference artifacts

**Verification**
- Read-through against actual repo tree and plugin layout
- Optional grep or script check for documented skill names vs actual skill directories

## Unit A4 — CI validation expansion

**Goal**  
Ensure changes to core skill assets trigger automated validation, not just plugin manifest checks.

**Files**
- `.github/workflows/validate-plugin.yml` and/or a new workflow such as `.github/workflows/validate-skill-repo.yml`
- `tests/test_reference_files.py` (or equivalent test coverage)

**Patterns to follow**
- Preserve the existing plugin validation behavior
- Keep CI repository-local and secret-free
- Favor explicit path filters over always-on broad workflows if that keeps runtime low without missing relevant changes

**Approach**
- Add test execution for the Python suite on changes to `scripts/`, `tests/`, `SKILL.md`, `references/`, and possibly relevant docs.
- Optionally add a lightweight consistency check for required reference files and packaged skill entries if pytest alone is not enough.
- Avoid auto-mutating repo content from CI; CI validates only.

**Execution note**
- Characterization-first: keep current plugin validation intact while adding new coverage around it.

**Test scenarios**
- A change to `scripts/ingest.py` triggers test execution
- A change to `references/` or root `SKILL.md` triggers validation
- Existing plugin JSON/symlink validation still passes unchanged

**Verification**
- Workflow syntax is valid
- CI path filters cover the intended files
- `python3 -m pytest -q`

## Follow-on Tranches

## Phase B — Execution-quality improvements

Capture but do not implement yet:

- clearer planning scope gates and proportionality rules
- stronger repo guidance for future skill changes
- better consistency between brainstorm/plan/work docs and repo execution reality

**Output expectation from this plan:** a concrete backlog group, not immediate code changes.

## Phase C — Broader platform upgrades

Capture but defer:

- caching or rerun support
- richer machine-readable evaluation outputs
- larger structural upgrades that raise carrying cost

**Output expectation from this plan:** explicit later-phase candidates only.

## PR Boundaries

Recommended landing order:

1. **PR 1:** Unit A1 — ingestion contract alignment
2. **PR 2:** Unit A2 — thin-skill and plugin parity
3. **PR 3:** Unit A3 — documentation and install parity
4. **PR 4:** Unit A4 — CI validation expansion

Why this order:
- A1 establishes the contract and tests early.
- A2 updates the executable/package surface next.
- A3 then documents the now-true package shape.
- A4 hardens validation last, once the intended steady-state surface exists.

If coupling discovered during execution is lower than expected, A3 and A4 can be combined. Do not combine all four by default.

## Requirements Trace

| Requirement | Plan coverage |
|-------------|---------------|
| R1 | Program structure section and follow-on tranches |
| R2 | PR-sized Implementation Units and landing order |
| R3 | Unit A2 thin-skill parity |
| R4 | Unit A3 documentation/install parity |
| R5 | Unit A1 ingestion contract alignment |
| R6 | Unit A4 CI validation expansion |
| R7 | Scope boundaries, shared references, and non-breaking constraints across all units |
| R8 | Explicit PR boundaries, sequencing, and verification per unit |

## System-Wide Impact

### Interaction Graph

- Root `SKILL.md` defines the canonical pipeline contract.
- `scripts/ingest.py` emits a brief that downstream manual users and maintainers rely on.
- `skills/mega-eval-*` expose phase slices in the picker and plugin package.
- `README.md` and `skills/README.md` explain how users install and invoke those slices.
- GitHub workflows validate whether the packaged/plugin/doc surface is coherent.

### Error & Failure Propagation

- Drift between `SKILL.md` and `ingest.py` causes incorrect brief scaffolding and weakens downstream runs.
- Drift between `skills/`, `plugins/`, and docs causes install or discoverability failures for plugin users.
- Missing CI coverage lets contract drift land silently.

### State Lifecycle Risks

- Packaging and docs changes are low runtime risk but high maintainability risk if partial.
- CI changes that miss the intended path filters create false confidence.
- Version bumps must stay synchronized across plugin manifests when plugin-visible surface changes.

### API Surface Parity

- Full `mega-eval` remains the canonical pipeline.
- Thin skills must stay aligned with the same artifact and reference contracts.
- Plugin consumers and git/manual users should see the same skill surface.

### Integration Test Scenarios

- Full repo clone with phase-only skill invocation resolves `../../references/`
- Plugin package resolves all skill entries and symlinks correctly
- `scripts/ingest.py` generates a brief that matches the root skill contract after the 1E/1F additions

## Acceptance Criteria

### Phase A functional requirements
- [ ] `scripts/ingest.py` emits the current canonical Evaluation Brief shape required by root `SKILL.md`
- [ ] `tests/test_ingest.py` and any new repo consistency tests cover the updated contract
- [ ] Thin skills exist for the current Phase 1 surface, including 1E and 1F
- [ ] Plugin packaging exposes the same intended thin-skill surface as the repo
- [ ] README and `skills/README.md` accurately describe the real skill inventory and required reference files
- [ ] CI validates skill/docs/reference/script changes, not just plugin manifests

### Non-functional requirements
- [ ] No breaking changes to existing artifact names or the canonical full pipeline
- [ ] Each Phase A unit can land independently as a reviewable PR
- [ ] No prompt-body duplication is introduced into thin skills

## Dependencies & Risks

- **Dependency:** root `SKILL.md` is the canonical schema; execution must read it before changing `ingest.py`
- **Dependency:** plugin packaging changes may require version bumps in two places
- **Risk:** doc changes can drift again if they land before packaging changes; mitigated by the PR order above
- **Risk:** adding CI coverage without the right path filters gives false confidence; mitigated by explicit trigger review
- **Risk:** expanding thin skills without preserving shared references creates long-term prompt drift; mitigated by enforcing the existing thin-skill pattern

## Sources & References

### Origin
- **Origin document:** [docs/brainstorms/2026-04-15-mega-eval-improvement-program-requirements.md](../brainstorms/2026-04-15-mega-eval-improvement-program-requirements.md)

### Internal References
- Root pipeline contract: [SKILL.md](../../SKILL.md)
- Thin-skill contract and packaging precedent: [docs/plans/2026-03-24-004-feat-mega-eval-sub-skills-plan.md](2026-03-24-004-feat-mega-eval-sub-skills-plan.md)
- Thin-skill inventory: [skills/README.md](../../skills/README.md)
- Example thin skill pattern: [skills/mega-eval-design/SKILL.md](../../skills/mega-eval-design/SKILL.md)
- Maintainer and release guidance: [MAINTAINERS.md](../../MAINTAINERS.md)
- Ingestion helper: [scripts/ingest.py](../../scripts/ingest.py)
- Existing tests: [tests/test_ingest.py](../../tests/test_ingest.py)
- Existing plugin validation workflow: [.github/workflows/validate-plugin.yml](../../.github/workflows/validate-plugin.yml)

### Research Notes
- Repo research confirmed plugin validation currently focuses on manifest JSON and symlink integrity, leaving root skill/docs/scripts changes unvalidated.
- Learnings research found no `docs/solutions/` tree; the applicable governance lives in `references/learnings.md`, `MAINTAINERS.md`, and the prior sub-skills / packaging plans.

---

Plan written to `docs/plans/2026-04-15-002-feat-mega-eval-improvement-program-plan.md`.
