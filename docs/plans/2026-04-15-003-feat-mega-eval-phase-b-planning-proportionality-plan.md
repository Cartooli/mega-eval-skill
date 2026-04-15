---
title: "feat: Mega-eval Phase B planning proportionality guide"
type: feat
status: active
date: 2026-04-15
origin: docs/brainstorms/2026-04-15-mega-eval-phase-b-planning-proportionality-requirements.md
---

# feat: Mega-eval Phase B planning proportionality guide

## Overview

Add a **repo-native planning proportionality guide** so maintainers can right-size future changes without over-planning or under-planning. This is Phase B of the broader improvement program, but it is intentionally scoped as a **single mergeable documentation/process PR**. The goal is not to change the external `/ce-plan` skill from inside this repository; it is to make this repo’s own maintenance workflow clearer and faster.

## Problem Statement / Motivation

After Phase A, the repo is better packaged and validated, but maintainers still lack a simple operating rubric for future changes:

- Some changes are obviously small and should skip brainstorm/plan overhead.
- Some changes are cross-cutting and deserve more deliberate requirements and PR splitting.
- The current repo documents release and packaging expectations, but not **when** to choose brainstorm vs. plan vs. direct work.
- An existing review (`docs/reviews/CE-PLAN-SKILL-ENHANCEMENT-REVIEW.md`) already identifies strong proportionality ideas, but those ideas are not translated into repo-facing guidance.

The highest-leverage Phase B slice is to codify a right-sized process for this repo’s maintainers using the repo’s own change patterns as examples.

## Proposed Solution

Ship one documentation/process tranche with three tightly related implementation units:

1. **B1 — New maintainers’ planning proportionality guide**
2. **B2 — Integrate the guide into `MAINTAINERS.md`**
3. **B3 — Cross-link from repo-facing docs where discovery matters**

The guide should answer four concrete questions:

1. Is this change planning-worthy?
2. Which artifact should I produce first: brainstorm, plan, or direct work?
3. How much research is justified?
4. How should I size PRs for this class of change?

## Implementation Units

## Unit B1 — Add planning proportionality guide

**Goal**  
Create a short, repo-native guide that classifies changes by size and recommends the appropriate workflow.

**Files**
- `docs/guides/change-planning.md` (new)

**Patterns to follow**
- Keep it concise and maintainer-usable, not a generic process manifesto
- Ground examples in real repo work: docs-only updates, new phase tracks, plugin packaging changes, workflow/reference changes
- Reuse the strongest ideas from `docs/reviews/CE-PLAN-SKILL-ENHANCEMENT-REVIEW.md` without copying that review wholesale

**Approach**
- Define three sizes: **lightweight**, **standard**, **deep**
- Add a **planning-worthiness** filter for trivial changes
- Add an **artifact selection** matrix:
  - direct work only
  - short direct plan
  - brainstorm → plan → work
- Add a **research decision rubric** tuned to this repo
- Add a **PR sizing guide** emphasizing mergeable tranches

**Execution note**
- Documentation-first. Keep the guide practical enough that a maintainer can use it during active work, not just read it once.

**Verification**
- Read the guide top to bottom and confirm it answers the four questions above in under ~2 pages of markdown

## Unit B2 — Integrate the guide into MAINTAINERS

**Goal**  
Make the new guidance discoverable from the main maintainer surface rather than leaving it as an orphan doc.

**Files**
- `MAINTAINERS.md`

**Patterns to follow**
- Preserve the current tone and release/checklist structure
- Keep `MAINTAINERS.md` focused; add a concise summary plus a clear link to the deeper guide

**Approach**
- Add a short **Planning a change** section or equivalent summary
- Link to `docs/guides/change-planning.md`
- Reference existing packaging/versioning rules where they affect scoping decisions

**Execution note**
- Do not duplicate the full guide inside `MAINTAINERS.md`; summarize and link out

**Verification**
- A reader starting in `MAINTAINERS.md` can discover the guide immediately

## Unit B3 — Cross-link from repo-facing docs

**Goal**  
Ensure the process guidance is discoverable from at least one additional repo-facing place beyond `MAINTAINERS.md`.

**Files**
- `README.md` (only if a short maintainer/contributor pointer is warranted)
- Optional related docs if a better discovery point exists

**Patterns to follow**
- Keep end-user install docs user-focused
- Add only a lightweight maintainer pointer if it improves discovery without clutter

**Approach**
- Prefer a short “Maintaining / evolving this repo” pointer rather than a large new README section
- If README feels too user-facing, keep this unit no-op and rely on `MAINTAINERS.md` plus the guide itself

**Execution note**
- Keep this unit optional in spirit but decide explicitly during implementation

**Verification**
- Process guidance is discoverable without forcing end-user docs to carry contributor-heavy content

## Technical Considerations

- This is a **repo-process** change, not a runtime or pipeline behavior change.
- No CI or automation changes are required in this tranche.
- The guide should reference, not override, existing release/versioning constraints in `MAINTAINERS.md`.
- The guide should stay compatible with the repo’s current branching and PR practices: small, mergeable, low-risk changes first.

## System-Wide Impact

### Interaction Graph

- Maintainers read `MAINTAINERS.md`
- `MAINTAINERS.md` points to `docs/guides/change-planning.md`
- The guide helps choose whether a future repo change goes straight to work, to a compact plan, or through brainstorm → plan → work

### Error & Failure Propagation

- Today’s failure mode is mostly process drift: inconsistent planning depth and oversized or under-specified change sets
- This tranche reduces those process errors by making the expected path explicit

### State Lifecycle Risks

- Minimal: documentation-only change set
- Main risk is adding too much ceremony; mitigate by keeping the guide short and example-driven

### API Surface Parity

- No runtime API changes
- No artifact filename changes
- No plugin/package changes

## Acceptance Criteria

- [ ] `docs/guides/change-planning.md` exists and defines at least three change sizes with repo-relevant examples
- [ ] The guide includes a clear planning-worthiness / skip-planning path
- [ ] The guide includes artifact-selection guidance for direct work vs. direct plan vs. brainstorm → plan → work
- [ ] The guide includes a research decision rubric for this repo
- [ ] The guide includes PR sizing guidance that favors mergeable tranches
- [ ] `MAINTAINERS.md` links to the guide and carries a short embedded summary
- [ ] At least one repo-facing entrypoint besides the guide itself makes the new process discoverable, if that can be done without cluttering user-facing docs

## Success Metrics

- A maintainer can classify a proposed repo change in under a minute
- Trivial changes have an explicit low-ceremony path
- Larger changes have an explicit higher-ceremony path with research and PR-boundary expectations

## Dependencies & Risks

- **Dependency:** `MAINTAINERS.md` remains the maintainer entrypoint
- **Risk:** Over-documenting process and creating more friction instead of less
  - **Mitigation:** keep the guide concise, repo-specific, and example-driven
- **Risk:** README clutter
  - **Mitigation:** add only a small maintainer pointer if it genuinely improves discovery

## Sources & References

### Origin
- **Origin document:** [docs/brainstorms/2026-04-15-mega-eval-phase-b-planning-proportionality-requirements.md](../brainstorms/2026-04-15-mega-eval-phase-b-planning-proportionality-requirements.md)

### Internal References
- Maintainer workflow and release guidance: [MAINTAINERS.md](../../MAINTAINERS.md)
- Improvement program roadmap: [docs/plans/2026-04-15-002-feat-mega-eval-improvement-program-plan.md](2026-04-15-002-feat-mega-eval-improvement-program-plan.md)
- Planning proportionality review source: [docs/reviews/CE-PLAN-SKILL-ENHANCEMENT-REVIEW.md](../reviews/CE-PLAN-SKILL-ENHANCEMENT-REVIEW.md)
- Plugin packaging constraints: [docs/plans/2026-03-24-005-feat-claude-plugin-marketplace-packaging-plan.md](2026-03-24-005-feat-claude-plugin-marketplace-packaging-plan.md)

---

Plan written to `docs/plans/2026-04-15-003-feat-mega-eval-phase-b-planning-proportionality-plan.md`.
