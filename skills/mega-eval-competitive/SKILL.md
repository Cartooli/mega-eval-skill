---
name: mega-eval-competitive
description: "Phase 1B only: competitive and market landscape analysis from an Evaluation Brief, output phase1b-competitive-raw.md. Use for 'mega eval competitive only', 'competitor landscape', 'market analysis without full eval', or running Phase 1B standalone."
---

# Mega-eval — Phase 1B: Competitive & market only

You are running **only Phase 1B** of the mega-eval pipeline: **competitive and market landscape** analysis (web research as specified in the main pipeline).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 1), `references/subagent-prompts.md` (**Phase 1B** template), optionally `references/learnings.md`.

Full instructions: **Phase 1B** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** Evaluation Brief pasted by the user |
| **Writes** | `<workspace>/phase1b-competitive-raw.md` |

Be honest when web search returns thin data; do not fabricate competitors. Include `run_id` / `run_log` in prompts when logging is enabled.

## Next steps

Pair with **`mega-eval-hater`** and **`mega-eval-strengths`** for a full Phase 1 set, then **`mega-eval-synthesis`**, or run **`mega-eval`** end-to-end.
