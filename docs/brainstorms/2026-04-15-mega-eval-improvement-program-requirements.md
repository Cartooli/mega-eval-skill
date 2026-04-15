---
date: 2026-04-15
topic: mega-eval-improvement-program
---

# Mega-eval improvement program

## Problem Frame
The repo has grown materially in capability, but its productization and execution guardrails are lagging behind the newest skill behavior. After landing Phase 1E/1F, the highest-leverage next move is to make the system easier to ship safely: package new slices consistently, keep docs/install guidance in sync with the real artifact graph, make ingestion emit the current brief contract, and make CI validate the assets the repo actually depends on. Beyond that first tranche, the project also needs follow-on work on execution quality and larger platform capabilities, but those should be sequenced as separate, mergeable phases rather than one large risky change.

## Requirements
- R1. Define a **multi-PR improvement program** with three ordered tranches:
  - Phase A: operational hardening first
  - Phase B: execution-quality improvements second
  - Phase C: broader platform upgrades third
- R2. Phase A must be independently shippable from the default branch and scoped for **multiple small PRs** rather than one omnibus change.
- R3. Phase A must include **thin-skill parity** for the newly added Phase 1E and Phase 1F tracks, following the existing `mega-eval-*` naming and shared-`references/` contract rather than duplicating methodology.
- R4. Phase A must bring **documentation and install guidance** into parity with the current skill surface so a user reading the repo can correctly install and invoke all supported slices and required reference files.
- R5. Phase A must align **`scripts/ingest.py` output** with the current canonical Evaluation Brief contract used by the root `SKILL.md`, including the newer audit/model-fit sections needed by the pipeline.
- R6. Phase A must strengthen **automated validation** so changes to `SKILL.md`, `references/`, `scripts/`, and related docs/tests are exercised by CI or equivalent repository checks rather than relying on manual review.
- R7. Every tranche in the program must preserve the existing full `mega-eval` pipeline as the canonical path and avoid breaking current file contracts or existing example flows.
- R8. The resulting plan must produce a **feasible build list** with explicit PR boundaries, sequencing, and acceptance criteria for each tranche, favoring low-risk, production-ready work over speculative architecture.

## Success Criteria
- The first tranche can be implemented as a sequence of merge-ready PRs with no breaking changes to the full pipeline.
- Thin-skill coverage, docs, ingestion output, and CI validation are all aligned with the real current skill behavior after Phase A ships.
- The build list clearly distinguishes what lands now vs. later, so execution can proceed without re-brainstorming scope after every PR.
- Follow-on work for execution quality and broader platform upgrades is captured as concrete later phases rather than vague “future improvements.”

## Scope Boundaries
- Do not combine all improvements into one giant PR or one giant plan section with no execution boundaries.
- Do not redesign the core mega-eval methodology during Phase A; this tranche is about hardening, parity, and safe execution.
- Do not introduce breaking changes to artifact names, the canonical full-pipeline entrypoint, or the existing deliverable shape.
- Do not treat aspirational ideas like caching, rerun support, or JSON bundles as part of the first tranche unless they naturally fit a later explicitly-sequenced phase.

## Key Decisions
- **Program, not one PR:** the user wants the full improvement pass captured now, but the work should ship as multiple mergeable PRs.
- **Operational hardening first:** the repo should first become easier to trust, install, validate, and extend before broader upgrades are attempted.
- **Preserve shared references:** thin skills and supporting docs should continue pointing to shared `references/` content instead of copying prompt bodies.
- **Plan for execution:** the build list should be concrete enough that `/ce:work` can execute tranche by tranche without inventing new scope.

## Dependencies / Assumptions
- Assumes the repo will continue using the current `mega-eval` + `mega-eval-*` packaging model.
- Assumes the default branch remains the source of truth for future tranche execution.
- Assumes CI can be extended with repository-local checks without introducing hosted secrets or deployment infrastructure.

## Outstanding Questions

### Resolve Before Planning
- *(none)*

### Deferred to Planning
- [Affects R2][Technical] What is the cleanest PR split inside Phase A: parity/docs first, ingest/schema alignment second, CI validation third; or a different boundary that better matches repo coupling?
- [Affects R6][Technical] Should validation live in the existing workflow or as one additional workflow targeted at docs/skill/references/script changes?
- [Affects R8][Needs research] Which execution-quality and platform-upgrade items should be explicitly captured as Phase B and Phase C backlog entries so the program stays concrete without overcommitting implementation now?

## Next Steps
→ `/ce:plan` for structured implementation planning
