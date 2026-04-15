---
name: mega-eval-durability
description: "Phase 1F only: AI/agent durability audit from an Evaluation Brief + primary HTTPS URL, output phase1f-durability-raw.md. Use for 'mega eval durability audit', 'AI resilience for eval', or Phase 1F without the full mega-eval pipeline."
---

# Mega-eval — Phase 1F: AI durability audit only

You are running **only Phase 1F** of the mega-eval pipeline: a report-only audit of how resilient the subject’s **AI / agent surface** is to model, provider, and capability change. This is **not** a general business or platform-risk review.

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/durability-audit-template.md`, `references/subagent-prompts.md` (**Phase 1F** template), and `references/pipeline-checklist.md` (Phase 1 / Phase 2 expectations).

Full orchestration rules: **Phase 0** (durability audit gate), **Phase 1F**, and **Phase 2** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** pasted Evaluation Brief; shared primary `https://` URL from the brief’s audit section or user message |
| **Writes** | `<workspace>/phase1f-durability-raw.md` |

**Opt out:** If `MEGA_EVAL_DURABILITY_AUDIT` is `off` / `0` / `false`, do not run — tell the user to enable it or use full `mega-eval` with the env unset.

If the subject has no meaningful AI / LLM / agent surface, write the short `N/A` stub described in `references/durability-audit-template.md` and stop cleanly.

Use `run_id` and `run_log` paths in the subagent prompt per `references/subagent-prompts.md`. If logging is enabled, follow the full `SKILL.md` run-log rules for Phase 1.

## Next steps

Run **`mega-eval-synthesis`** once Phase 1A–1C are complete; it merges `phase1f-durability-raw.md` when present and omits the exec-summary posture section when the risk band is `N/A`. Use **`mega-eval`** for the full pipeline.
