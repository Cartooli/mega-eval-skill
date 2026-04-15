---
name: mega-eval-design
description: "Phase 1D only: optional live-site design audit from an Evaluation Brief + primary HTTPS URL, output phase1d-design-raw.md. Report-only (no code fixes). Use for 'mega eval design audit', 'UX teardown of this URL', 'visual audit for eval', or Phase 1D without full mega-eval."
---

# Mega-eval — Phase 1D: Live site design audit only

You are running **only Phase 1D** of the mega-eval pipeline: a **report-only** visual/UX audit of a **public** marketing/product URL. This is **not** gstack `/design-review` (no fix loop or commits on a codebase).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/design-audit-template.md`, `references/subagent-prompts.md` (**Phase 1D** template), `references/pipeline-checklist.md` (Phase 1).

Full orchestration rules: **Phase 0** (design audit gate) and **Phase 1D** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** pasted Evaluation Brief; **primary `https://` URL** (from brief’s *Live site / design audit* section or user message) |
| **Writes** | `<workspace>/phase1d-design-raw.md` |

**Opt out:** If `MEGA_EVAL_DESIGN_AUDIT` is `off` / `0` / `false`, do not run — tell the user to enable or use full `mega-eval` with env unset.

Use `run_id` and `run_log` paths in the subagent prompt per `references/subagent-prompts.md`. If logging is enabled, follow the full `SKILL.md` run-log rules for Phase 1.

## Next steps

Run **`mega-eval-hater`**, **`mega-eval-competitive`**, and **`mega-eval-strengths`** if Phase 1A–1C are missing; then **`mega-eval-synthesis`** (merges `phase1d-design-raw.md` when present), or use **`mega-eval`** for the full pipeline.
