# Change Planning Guide

Use this guide when deciding how much process a proposed repo change needs.

The goal is simple: **match ceremony to risk and ambiguity**. Small, obvious changes should ship quickly. Cross-cutting or behavior-changing work should get clearer requirements and explicit PR boundaries before implementation starts.

## 1. Size the change first

| Size | Use when | Typical examples in this repo | Default path |
|------|----------|-------------------------------|--------------|
| **Lightweight** | One file or one narrow concern; behavior is obvious; low ambiguity | README wording fix, typo in a thin skill, version bump only, broken link, small test fix, adding a missing doc pointer | Direct work, or a very short direct plan if you want a record |
| **Standard** | Several related files; some decisions to make; moderate coupling | New thin skill, packaging parity update, brief schema alignment, CI path-filter change, docs + plugin sync | Direct plan, then work |
| **Deep** | Cross-cutting behavior change, new phase capability, or unclear product decision | New analysis track, major pipeline restructuring, deliverable shape changes, caching/rerun architecture, workflow redesign | Brainstorm → plan → work |

If you are between two sizes, pick the larger one only when the extra clarity will materially reduce rework.

## 2. Decide whether this is planning-worthy

Use this quick filter before you start a brainstorm or deep plan:

**Usually skip straight to work when the change is:**
- docs-only and clearly scoped
- a single-file wording/config fix
- a missing link, typo, or stale count
- a narrow regression with an obvious fix and no meaningful product choice

**Usually create a direct plan when the change:**
- touches multiple files with one bounded goal
- changes packaging, install paths, or CI behavior
- needs a recorded acceptance checklist but not a product exploration pass

**Usually brainstorm first when the change:**
- introduces or removes a pipeline capability
- changes user-facing behavior or deliverable shape
- has multiple plausible product directions
- could easily sprawl unless scope boundaries are made explicit

## 3. Pick the artifact path

| Situation | Recommended artifact path |
|-----------|---------------------------|
| Obvious, low-risk maintenance change | `/ce:work` directly |
| Bounded repo change with one clear goal | Short direct plan → `/ce:work` |
| Ambiguous or strategic change | `/ce:brainstorm` → `/ce:plan` → `/ce:work` |

Use the lightest path that still prevents the planner or implementer from inventing scope later.

## 4. Research only when it changes the outcome

### Local context is usually enough when:
- this repo already has a nearby pattern to follow
- the change is packaging, docs, tests, or file-contract alignment
- you are extending an established shape rather than inventing a new one

### Deeper repo research is warranted when:
- the change touches multiple contracts at once (`SKILL.md`, `references/`, `skills/`, plugin packaging, examples)
- you suspect drift between docs and implementation
- PR boundaries depend on how tightly files are coupled

### External research is warranted when:
- the change depends on host-platform behavior outside the repo
- current guidance may be stale (for example, plugin platform docs, model docs, or third-party integration rules)
- the repo has no established precedent and the wrong call would create lasting carrying cost

If research will not change the implementation approach, skip it.

## 5. Size the PR, not just the idea

Favor **mergeable tranches** over omnibus PRs.

### Good reasons to split into multiple PRs
- one unit changes behavior/contracts and another only documents it
- one unit adds tests/validation and another changes packaging or install surfaces
- the later work depends on the earlier work becoming true first

### Good reasons to keep one PR
- all touched files support one narrow goal
- the review burden stays low
- splitting would create temporary inconsistency without real clarity benefits

### Repo-specific rule of thumb
- **Lightweight** changes: one PR
- **Standard** changes: one PR unless the docs or validation naturally follow after the code/packaging change
- **Deep** changes: assume multiple PRs unless proven otherwise

## 6. Use repo-native examples

When in doubt, classify proposed work against recent repo change types:

- **Lightweight:** fix README counts, adjust one thin-skill description, update a dead link
- **Standard:** add missing plugin skill entries, align `scripts/ingest.py` to the brief contract, add a validation workflow
- **Deep:** add a new Phase 1 track, change synthesis rules, restructure deliverables, add caching/rerun architecture

## 7. Keep the process lightweight

This guide is here to reduce wasted motion, not create a gate.

- Do not brainstorm a typo.
- Do not skip planning for a cross-cutting capability.
- Do not force a three-PR split when one clean PR will do.
- Do not let a plan become a substitute for deciding scope.

When unsure, prefer the smallest amount of process that still makes the next step obvious and safe.
