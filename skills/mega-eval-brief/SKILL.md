---
name: mega-eval-brief
description: "Phase 0 only: ingest text, documents, and/or URLs and produce a single Evaluation Brief (eval-brief.md). Use for 'mega eval brief only', 'normalize inputs for evaluation', 'create evaluation brief', or when you need the mega-eval brief without running analysis phases."
---

# Mega-eval — Phase 0: Evaluation Brief only

You are running **only Phase 0** of the mega-eval pipeline: normalize inputs into one **Evaluation Brief**. Do **not** run Phases 1A–4 unless the user explicitly asks.

## Shared methodology location

Read checklists and context from the mega-eval `references/` directory. Use the **first path that exists**:

1. `./references/` — copied next to this `SKILL.md`
2. `../../references/` — this file at `skills/mega-eval-brief/SKILL.md` in a full **mega-eval-skill** repo clone
3. `../mega-eval/references/` — this skill installed as a sibling of the full `mega-eval` package

Full pipeline (for cross-links): `../../SKILL.md` or `../mega-eval/SKILL.md`.

**Read before running:** `references/pipeline-checklist.md` (Phase 0 section) and the **Phase 0: Input Ingestion** section of the full `SKILL.md` (includes **Live site / design audit** fields and `MEGA_EVAL_DESIGN_AUDIT` opt-out).

## Inputs and outputs

| | |
|--|--|
| **Reads** | User text, uploaded files (`.pdf`, `.docx`, etc.), URLs — per full `SKILL.md` Phase 0 |
| **Writes** | `eval-brief.md` (prefer `<workspace>/sessions/<session>/eval-brief.md` when using sessions) |

## Run log (optional)

If `MEGA_EVAL_LOG` is not `off` / `0` / `false`: create `run_id`, initialize `run-log.md`, append `phase_start phase0` / `phase_complete phase0` per full `SKILL.md`.

## Next steps

Chain with other mega-eval phase skills (`mega-eval-hater`, `mega-eval-competitive`, …) or run the full **`mega-eval`** skill for the complete pipeline.
