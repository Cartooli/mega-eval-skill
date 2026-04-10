---
title: "feat: Individually invokable mega-eval sub-skills"
type: feat
status: active
date: 2026-03-24
origin: docs/brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md
---

# feat: Individually invokable mega-eval sub-skills

## Overview

Add **thin, discoverable skills**—one per pipeline slice (Phase 0, 1A, 1B, 1C, 2, 3, 4)—while keeping the existing **full mega-eval** skill as the canonical one-shot pipeline. Each thin skill has its own `name` / `description` / triggers for the skill picker; **long-form methodology stays in `references/`** so maintainers do not fork prompts (see origin: [docs/brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md](../brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md)).

## Problem Statement / Motivation

Users who need only one phase (e.g. competitive landscape or brief-only ingestion) must either run the entire monolith or manually interpret `SKILL.md`. The brainstorm decision was **discoverability first**: separate picker entries with clear triggers, shared references for maintainability (origin: R1–R5, Key Decisions).

## Proposed Solution

1. **Keep** root `SKILL.md` (or relocate without behavior change) as **`mega-eval`** — full Phases 0–4, same deliverables as today (origin: R1).
2. **Add** seven sibling skill packages, each containing **only** a thin `SKILL.md` (plus optional tiny `README.md` pointer) that:
   - Declares a **unique** frontmatter `name` and a **search-optimized** `description` with trigger phrases.
   - States **inputs** and **outputs** (files) matching [`references/pipeline-checklist.md`](../../references/pipeline-checklist.md) and the main [`SKILL.md`](../../SKILL.md).
   - Instructs the executor to **read** the relevant sections of `references/subagent-prompts.md`, `references/pipeline-checklist.md`, and (where applicable) `references/learnings.md` — **no copy-paste of those bodies** into thin skills (origin: R3).
3. **Document** install layouts for (a) **full repo clone** with relative paths to `references/`, (b) **per-skill copy** installs that include a **duplicated or copied `references/`** tree so single-folder installs work (origin: R4).
4. **Phase 4** skill: explicit **pre-flight checklist** — required upstream files before generating `.docx`; dependency on **docx** (and content sources) documented; align with existing Phase 4 ordering (raw → synthesis → outline → executive summary last) (origin: R2g, [SKILL.md Phase 4](../../SKILL.md)).

## Artifact I/O contract (from existing pipeline)

Use these as the **stable contract** for thin skills so chaining matches the full pipeline (see origin: R5; source: [`references/pipeline-checklist.md`](../../references/pipeline-checklist.md)).

| Slice | Reads (minimum) | Writes |
|-------|------------------|--------|
| Phase 0 | User inputs (text / files / URLs) | `eval-brief.md` (path per session convention in main SKILL) |
| Phase 1A | `eval-brief.md` (or embedded brief if single-shot) | `phase1a-hater-raw.md` |
| Phase 1B | `eval-brief.md` | `phase1b-competitive-raw.md` |
| Phase 1C | `eval-brief.md` | `phase1c-strengths-raw.md` |
| Phase 2 | `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, `phase1c-strengths-raw.md` | `phase2-synthesis.md` |
| Phase 3 | Brief + Phase 1 highlights (per subagent template in main SKILL) | `phase3-content-outline-raw.md` |
| Phase 4 | Raw + synthesis + outline markdown files; optional `run-log.md` for reconciliation | `01-`…`05-` `.docx`, `00-executive-summary.docx` last |

**Phase 4 prerequisites (strict):** Do not assemble final `.docx` unless the corresponding **source markdown** exists for each deliverable (map in main SKILL Phase 4: `phase1a` → `01`, `phase1b` → `02`, `phase1c` → `03`, `phase2-synthesis` → `04`, `phase3-content-outline-raw` → `05`; `00` draws from all). If a file is missing, the skill must **stop** with a clear list of missing inputs (addresses deferred [R2g] from origin).

**External skills (unchanged):** Phase 1A references **hater-mode**; Phase 3 references **long-form-outline**; Phase 4 references **docx** — thin skills must repeat these prerequisites verbatim from the main `SKILL.md` / checklist (origin: Scope Boundaries — no guarantee in unsupported hosts).

## Suggested naming convention (deferred item from origin)

Use a **shared prefix** for picker grouping:

| Skill folder / `name` | Purpose |
|------------------------|---------|
| `mega-eval` | Full pipeline (existing) |
| `mega-eval-brief` | Phase 0 only |
| `mega-eval-hater` | Phase 1A |
| `mega-eval-competitive` | Phase 1B |
| `mega-eval-strengths` | Phase 1C |
| `mega-eval-synthesis` | Phase 2 |
| `mega-eval-content-outline` | Phase 3 |
| `mega-eval-deliverables` | Phase 4 |

Alternative: `mega-eval-phase-0-brief` style — pick one scheme in implementation for consistency (origin: Deferred [R5]).

## Repository layout options

**Recommended for git (single source of truth):**

- Keep **`references/`** and **`scripts/`** at repository root.
- Add **`skills/<name>/SKILL.md`** for each thin skill; each file uses **relative** links to `../../references/...` **when the skill is loaded from a full clone**. Document that **single-folder** installs must run a **copy script** that places `references/` next to each `SKILL.md` or duplicates the tree (addresses [R4]).

**Alternative:** Flat top-level siblings `mega-eval/SKILL.md`, `mega-eval-brief/SKILL.md`, … each with copied `references/` — heavier, only if required by a specific host.

## Technical Considerations

- **Architecture:** No change to evaluation methodology; **documentation + packaging** change with thin entrypoints (origin: Scope Boundaries).
- **Drift prevention:** CI or maintainer checklist: thin skills contain **only** pointers + I/O tables; grep guard optional to ensure no duplicated "Phase 1B" prompt blocks.
- **Performance:** N/A — same runtime as today per phase.
- **Security:** Same as today — redaction / `MEGA_EVAL_LOG` behavior inherited from main `SKILL.md`; thin Phase 0/1B skills that use web search should reference main doc’s honesty / no-fabrication rules.

## System-Wide Impact

- **Interaction graph:** Thin Phase 1 skills may launch **one** subagent (or inline) instead of three; no change to hater-mode / long-form-outline / docx contracts.
- **Error propagation:** Phase 4 thin skill must **fail closed** on missing inputs.
- **State lifecycle:** Partial runs produce partial markdown; user completes remaining phases with other skills — file naming must stay consistent with checklist.
- **API surface parity:** One full `mega-eval` + seven slices — all describe the **same** files where they overlap.
- **Integration test scenarios:** (1) Brief-only → competitive-only → synthesis with manually present 1A/1C files from prior runs. (2) Full raw set → Phase 2 only → Phase 3 only → Phase 4 only. (3) Install only `mega-eval-competitive` + copied `references/` — skill loads prompts from local `references/`.

## Acceptance Criteria

- [ ] Full **`mega-eval`** behavior and deliverables remain documented as the **complete** pipeline (origin: R1).
- [ ] Seven thin **`SKILL.md`** files exist with distinct **`name`** / **`description`** / triggers (origin: R2a–R2g).
- [ ] Each thin skill documents **inputs**, **outputs**, and **pointers** to `references/` (no duplicated long prompt text) (origin: R3, R5).
- [ ] **README** (and **MAINTAINERS.md** if needed) describe **full clone** vs **single-skill** install and what fails without `references/` (origin: R4).
- [ ] **Phase 4** thin skill lists **required files** before `.docx` generation and ordering of `00-executive-summary.docx` last (origin: R2g; aligned with [pipeline checklist](../../references/pipeline-checklist.md)).
- [ ] **Examples** (`examples/sample-run/`) cross-linked or noted for manual verification of file names.

## Success Metrics

- New users can discover **phase-specific** skills by name in the picker.
- One edit to **`references/subagent-prompts.md`** does not require editing seven full prompt copies (spot-check: thin skills are under ~N lines, mostly pointers).

## Dependencies & Risks

- **Dependency:** Existing **`references/`** tree remains the source of truth (origin: Dependencies).
- **Risk:** Hosts that only load a single `SKILL.md` without repo context — mitigated by install script or bundled `references/` per published artifact.
- **Risk:** Naming collision with other projects — mitigated by `mega-eval-*` prefix.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md](../brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md) — discoverability-first; thin wrappers; phases 0–4 + full pipeline; shared references; documented install.
- **Artifact contract:** [references/pipeline-checklist.md](../../references/pipeline-checklist.md)
- **Prompt templates:** [references/subagent-prompts.md](../../references/subagent-prompts.md)
- **Phase 4 assembly order:** [SKILL.md — Phase 4](../../SKILL.md) (Deliverable Assembly)

## Documentation Plan

- Update **README.md**: install matrix (full vs thin-only), folder diagram, prerequisite skills for Phase 1A/3/4.
- Optional: **MAINTAINERS.md** — how to add a new slice without duplicating prompts.

---

Plan written to `docs/plans/2026-03-24-004-feat-mega-eval-sub-skills-plan.md`.
