---
name: mega-eval-strengths
description: "Phase 1C only: strengths and opportunities analysis from an Evaluation Brief, output phase1c-strengths-raw.md. Use for 'mega eval strengths only', 'upside analysis', 'growth angles without critique track', or Phase 1C standalone."
---

# Mega-eval — Phase 1C: Strengths & opportunities only

You are running **only Phase 1C** of the mega-eval pipeline: **strengths and opportunities** (honest positive counterweight to hater mode).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 1), `references/subagent-prompts.md` (**Phase 1C** template), optionally `references/learnings.md`.

Full instructions: **Phase 1C** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** Evaluation Brief pasted by the user |
| **Writes** | `<workspace>/phase1c-strengths-raw.md` |

Include `run_id` / `run_log` in prompts when logging is enabled.

## Next steps

After all three Phase 1 files exist, run **`mega-eval-synthesis`** or the full **`mega-eval`** pipeline.
