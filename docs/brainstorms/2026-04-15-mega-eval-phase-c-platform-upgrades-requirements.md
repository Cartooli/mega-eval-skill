---
date: 2026-04-15
topic: mega-eval-phase-c-platform-upgrades
---

# Mega-eval Phase C: platform upgrades

## Problem Frame
Mega-eval now has stronger packaging, validation, and maintainer process guidance, but the repo still assumes a mostly linear "run everything fresh" workflow and primarily human-readable outputs. That creates two remaining platform gaps:

1. Maintainers and power users do not have a lightweight, repo-native way to inspect a workspace and determine what phase outputs already exist, what is missing, and where a rerun should resume.
2. Downstream tooling has no stable machine-readable export of a completed or partial run; today, the outputs are mostly markdown intermediates plus `.docx` deliverables.

Phase C should close those gaps in a non-breaking way by adding a workspace inspection/export path rather than redesigning the core skill runtime.

## Requirements
- R1. Add a **repo-native machine-readable bundle/export path** that can summarize a mega-eval workspace or sample run into stable JSON.
- R2. The JSON export must include enough **run status metadata** to support resume/reuse decisions: which standard artifacts exist, which phases are complete, and what the next recommended phase is.
- R3. The export path must work for both **complete** and **partial** runs without requiring `.docx` generation.
- R4. The implementation must stay **non-breaking**: do not change the existing markdown artifact names or the current `.docx` deliverable contract.
- R5. Add **rerun/resume guidance** to repo docs so maintainers know they can reuse existing artifacts and continue from the first incomplete phase when appropriate.
- R6. Provide at least one **checked-in example** of the machine-readable output so users can see the shape without running the script first.
- R7. Add **automated tests** covering the new export logic and the resume-status behavior.
- R8. Keep the implementation **stdlib-only** (or equivalently low-dependency) so the helper remains portable for repo users.

## Success Criteria
- A maintainer can point a helper at a workspace and quickly see whether the run is incomplete, resumable, or effectively complete.
- A downstream tool or reviewer can consume a stable JSON bundle without scraping markdown ad hoc.
- The new capability complements the existing markdown/docx flow instead of replacing it.

## Scope Boundaries
- Do not add hosted storage, a database, or a persistent caching layer in this tranche.
- Do not redesign the core mega-eval phase sequence or replace markdown intermediates with JSON-native generation.
- Do not introduce automatic mutation of existing run artifacts; inspection/export should be safe and explicit.
- Do not add CI workflows beyond the repo’s existing pytest-based validation unless the new script specifically requires test coverage updates.

## Key Decisions
- **Inspection/export, not orchestration rewrite:** the bounded Phase C slice is a helper layer over the existing artifact contract.
- **One mergeable tranche:** machine-readable export and resume guidance are tightly coupled enough to ship together.
- **Favor stable metadata over fancy parsing:** the JSON should be useful for tooling and review, but it should not depend on brittle, phase-specific NLP extraction.

## Dependencies / Assumptions
- Assumes the repo’s canonical artifact names remain the current ones documented in `SKILL.md`, `README.md`, and `skills/README.md`.
- Assumes a helper script under `scripts/` is an acceptable repo-native interface for advanced users and maintainers.
- Assumes `examples/sample-run/` remains the best location for a checked-in example bundle.

## Outstanding Questions

### Resolve Before Planning
- *(none)*

### Deferred to Planning
- [Affects R1/R2][Technical] What is the minimum useful JSON schema that supports both tooling and resume decisions without overfitting to the current markdown prose?
- [Affects R5][Docs] Where should resume/reuse guidance live so it is discoverable for maintainers without cluttering the end-user quickstart too heavily?

## Next Steps
→ `/ce:plan` for structured implementation planning
