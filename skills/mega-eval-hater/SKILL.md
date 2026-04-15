---
name: mega-eval-hater
description: "Phase 1A only: 12-persona critical feedback (hater mode) from an Evaluation Brief, output phase1a-hater-raw.md. Use for 'mega eval hater only', 'roast this product', '12 lens critique', 'adversarial feedback without full eval', or competitive run of Phase 1A alone."
---

# Mega-eval — Phase 1A: Hater Mode only

You are running **only Phase 1A** of the mega-eval pipeline: **Hater Mode** critical feedback (12 audience lenses). Requires an **Evaluation Brief** (from Phase 0 or pasted).

**Prerequisite skill:** **hater-mode** (read `hater-mode` `SKILL.md` and `references/audiences.md` as the main pipeline does).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 1), `references/subagent-prompts.md` (**Phase 1A** template), optionally `references/learnings.md`.

Full Phase 1A instructions: **Phase 1A** section of full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** Evaluation Brief pasted by the user |
| **Writes** | `<workspace>/phase1a-hater-raw.md` |

Use `run_id` and `run_log` paths in the subagent prompt per `references/subagent-prompts.md`. If logging is enabled, follow the full `SKILL.md` run-log rules for Phase 1.

## Next steps

Run **`mega-eval-competitive`** and **`mega-eval-strengths`** for parallel Phase 1B/1C, or use **`mega-eval`** for the full pipeline.
