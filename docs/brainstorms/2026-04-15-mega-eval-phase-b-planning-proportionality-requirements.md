---
date: 2026-04-15
topic: mega-eval-phase-b-planning-proportionality
---

# Mega-eval Phase B: planning proportionality

## Problem Frame
Phase A made the repo safer to package and validate, but the maintainer workflow for future changes is still under-specified. The project now has enough moving parts that maintainers need a **right-sized planning rubric**: when a change needs a brainstorm, when a plan is warranted, when research is necessary, and when a small docs/config fix should skip planning entirely and go straight to work. Without that guidance, the repo risks either over-planning trivial changes or under-planning cross-cutting ones.

## Requirements
- R1. Add a **maintainer-facing planning proportionality guide** for this repo that classifies work into at least three sizes (for example: lightweight, standard, deep) using repo-relevant examples.
- R2. The guide must define **artifact selection rules**: when to use only `/ce:work`, when to run `/ce:brainstorm` then `/ce:plan`, and when a short direct plan is sufficient.
- R3. The guide must include an explicit **planning-worthiness / skip-planning** path for trivial changes such as doc wording, single-line config fixes, or obvious non-cross-cutting maintenance work.
- R4. The guide must include a concise **research decision rubric** so maintainers know when local context is enough versus when deeper repo or external research is justified.
- R5. The guide must include **PR sizing and sequencing guidance** that reinforces the repo’s existing preference for mergeable tranches over omnibus change sets.
- R6. The guide must be integrated into existing maintainer-facing docs so it is discoverable from the repo’s current workflow surface rather than living as an orphan file.
- R7. The changes must stay **repo-native**: improve this repository’s documented process, not the external `/ce-plan` skill implementation itself.

## Success Criteria
- A maintainer can classify a proposed change in under a minute and know whether to brainstorm, plan, or implement directly.
- Trivial repo changes have a documented low-ceremony path.
- Cross-cutting repo changes have a documented higher-ceremony path with research and PR-boundary expectations.
- The guidance is visible from `MAINTAINERS.md` and any other repo-facing entrypoint used by contributors.

## Scope Boundaries
- Do not modify the external `/ce-plan`, `/ce:brainstorm`, or `/ce:work` skill definitions from this repo.
- Do not add CI enforcement for process choices in this phase; this tranche is guidance, not automation.
- Do not redesign the repo’s release/versioning model; only reference the existing packaging rules where they matter for scoping.

## Key Decisions
- **Repo process, not skill surgery:** the best bounded Phase B slice is documentation and workflow clarity for this repo’s maintainers.
- **Single-PR tranche:** this phase should be one clean documentation/process PR unless implementation reveals unexpected coupling.
- **Use repo examples:** guidance should reference real change types this repo already sees, such as new phase tracks, docs-only corrections, packaging changes, and workflow/checklist updates.

## Dependencies / Assumptions
- Assumes `MAINTAINERS.md` remains the primary maintainer-facing document.
- Assumes the repo can add one new guide document under `docs/` without introducing tooling changes.

## Outstanding Questions

### Resolve Before Planning
- *(none)*

### Deferred to Planning
- [Affects R6][Technical] What is the best file location for the proportionality guide so it stays discoverable but doesn’t clutter end-user docs?
- [Affects R5][Technical] Should the PR sizing guidance live entirely in the new guide, or should `MAINTAINERS.md` carry a short embedded summary with a link out?

## Next Steps
→ `/ce:plan` for structured implementation planning
