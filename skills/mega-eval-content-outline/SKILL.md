---
name: mega-eval-content-outline
description: "Phase 3 only: content strategy outline (phase3-content-outline-raw.md) using long-form-outline methodology. Use for 'mega eval outline only', 'positioning outline', 'pitch narrative outline', after Phase 1–2 outputs exist."
---

# Mega-eval — Phase 3: Content strategy outline only

You are running **only Phase 3** of the mega-eval pipeline: a **content strategy outline** via the **long-form-outline** skill.

**Prerequisite skill:** **long-form-outline** (read its `SKILL.md` and follow its phases as the main pipeline specifies).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 3), `references/subagent-prompts.md` (**Phase 3** template).

Full instructions: **Phase 3: Content Strategy Outline** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | Evaluation Brief; highlights from **phase1c** (strengths), **phase1a** (criticisms to preempt), **phase1b** (positioning) — paste from files or read from disk |
| **Writes** | `phase3-content-outline-raw.md` |

Do **not** produce `.docx` here — markdown only. Use `run_id` / `run_log` in the subagent prompt when logging is enabled.

## Next steps

Run **`mega-eval-deliverables`** to assemble Word documents, or **`mega-eval`** for a full run.
