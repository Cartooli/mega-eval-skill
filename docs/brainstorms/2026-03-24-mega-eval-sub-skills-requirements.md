---
date: 2026-03-24
topic: mega-eval-sub-skills
---

# Mega-eval: individually invokable sub-skills

## Problem Frame

The full **mega-eval** skill is a single, large orchestration doc. Users who want **one phase** (e.g. competitive scan only, or “just the brief”) still rely on the monolith or manual slicing. The primary goal is **discoverability**: separate entries in the skill picker with **clear names, descriptions, and trigger phrases**, so people find and run the slice they need without guessing.

## Requirements

- R1. **Keep the existing full pipeline skill** (`mega-eval` or equivalent) as the **one-shot** path through Phases 0–4, unchanged in intent and deliverables (still the canonical “run everything” entry).
- R2. **Add thin, separately installable skills** for each runnable slice below, each with its **own** frontmatter `name` and `description` tuned for picker search and triggers:
  - R2a. **Phase 0** — Ingestion only: normalize inputs into the **Evaluation Brief** (no Phase 1–4).
  - R2b. **Phase 1A** — Hater Mode (12 lenses) only, consuming an existing brief or minimal inline context as documented.
  - R2c. **Phase 1B** — Competitive & market landscape only.
  - R2d. **Phase 1C** — Strengths & opportunities only.
  - R2e. **Phase 2** — Synthesis only (critical fixes, design issues, next steps), consuming agreed upstream artifacts.
  - R2f. **Phase 3** — Content strategy outline only.
  - R2g. **Phase 4** — Deliverable assembly only (e.g. `.docx` generation from existing phase outputs in the workspace), with explicit **inputs required** so partial installs do not silently produce junk.
- R3. **Single source of truth for long-form methodology**: thin skills **must not fork** full prompt libraries; they **delegate** to shared **`references/`** (and existing checklists/prompts) so maintainers update prompts in one place.
- R4. **Document installation** for hosts that expect a folder per skill: how to lay out **shared `references/`** with multiple skill entrypoints (copy layout, optional script, or “co-install” rule), and what breaks if `references/` is missing.
- R5. **Scope and I/O contract per slice**: each thin skill states **what it reads** (e.g. `eval-brief.md`, prior phase files) and **what it writes**, aligned with the main pipeline’s file naming where applicable, so users can chain runs without ambiguity.

## Success Criteria

- A new user can **see** distinct mega-eval-related skills in the picker and pick the **phase they need** without opening the monolith.
- Maintainers can **change** methodology in **`references/`** once and have **all** entrypoints stay consistent (no duplicated prompt drift).
- README (or equivalent) explains **minimal install** for “one phase only” vs **full** mega-eval install.

## Scope Boundaries

- **Non-goal:** Rewriting the core methodology or changing phase semantics beyond what’s needed to define clear per-phase I/O.
- **Non-goal:** Guaranteeing identical behavior in every host (Claude Code vs Cursor vs others); document **supported** layouts and degrade gracefully where possible.
- **Non-goal:** Auto-generating `.docx` in hosts that do not support existing tooling—Phase 4 skill should state prerequisites or fallbacks.

## Key Decisions

- **Discoverability over cost savings:** Sub-skills exist so users **find** the right slice; token/cost reduction is a side benefit, not the primary driver.
- **Granularity:** **Phase-complete** set — separate skills for **Phase 0, 1A, 1B, 1C, 2, 3, 4**, plus retaining the **full** pipeline skill (covers both “minimal three-way split” of Phase 1 and full phase coverage).
- **Thin wrappers + shared references:** Avoid duplicating long instructions; point each skill at the same **`references/`** tree.

## Dependencies / Assumptions

- Assumes the repo continues to ship **`references/`** (e.g. `subagent-prompts.md`, `pipeline-checklist.md`, `learnings.md`) as the shared contract.
- Hosts must support **multiple skill folders** pointing at shared files, or documented copy/install steps—exact mechanism is a **planning** concern.

## Outstanding Questions

### Resolve Before Planning

- None blocking: product scope and success criteria are defined above.

### Deferred to Planning

- [R4][Technical] Exact directory layout for multi-skill installs (symlinks vs copies vs install script) per target (Claude Code, Cursor, Cowork).
- [R2g][Technical] Strict prerequisites for Phase 4 (which files must exist, validation before write).
- [R5][Needs research] Naming convention for picker (`mega-eval-phase-0-brief` vs `mega-eval-1b-competitive`, etc.) and consistency with existing `mega-eval` naming.

## Next Steps

→ `/ce:plan` for structured implementation planning (repo layout, README, thin `SKILL.md` templates, install instructions, optional validation checklist).
