---
name: mega-eval-security
description: "Phase 1E only: observation-only security posture audit from an Evaluation Brief + primary HTTPS URL, output phase1e-security-raw.md. Use for 'mega eval security audit', 'security posture for eval', or Phase 1E without the full mega-eval pipeline."
---

# Mega-eval — Phase 1E: Security audit only

You are running **only Phase 1E** of the mega-eval pipeline: a **report-only**, observation-only security posture review of a **public** product or marketing surface. This is **not** a penetration test and never includes credential testing, intrusive probing, or broad supply-chain analysis.

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/security-audit-template.md`, `references/subagent-prompts.md` (**Phase 1E** template), and `references/pipeline-checklist.md` (Phase 1 / Phase 2 expectations).

Full orchestration rules: **Phase 0** (security audit gate), **Phase 1E**, and **Phase 2** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `eval-brief.md` **or** pasted Evaluation Brief; shared primary `https://` URL from the brief’s audit section or user message |
| **Writes** | `<workspace>/phase1e-security-raw.md` |

**Opt out:** If `MEGA_EVAL_SECURITY_AUDIT` is `off` / `0` / `false`, do not run — tell the user to enable it or use full `mega-eval` with the env unset.

Use `run_id` and `run_log` paths in the subagent prompt per `references/subagent-prompts.md`. If logging is enabled, follow the full `SKILL.md` run-log rules for Phase 1.

## Next steps

Run **`mega-eval-synthesis`** once Phase 1A–1C are complete; it merges `phase1e-security-raw.md` when present. Use **`mega-eval`** for the full pipeline.
