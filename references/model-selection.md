# Model selection for Mega Eval

Mega Eval is **reasoning- and synthesis-heavy**. Model choice materially affects depth, contradiction-handling, and competitive-grounding quality. Use this file when running the pipeline to verify the active host is on a **best-fit** tier for each phase.

Official catalogs (check periodically — IDs and defaults change):

- OpenAI: [Models](https://developers.openai.com/api/docs/models)
- Anthropic: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)

---

## Default stance

1. **If the environment exposes one model for everything:** use each provider’s **current flagship / frontier** text model for the whole run (this pipeline is not a good fit for “cheapest possible” defaults).
2. **If orchestrator and subagents can differ:** reserve the **strongest** model for **Phase 2 synthesis** (and Phase 0 brief quality if the host allows); parallel Phase 1 tracks can use **one step down** only if cost/latency require it — never use the smallest tier for Phase 2.

---

## OpenAI (API / ChatGPT / Codex where GPT-* IDs apply)

Per [OpenAI Models](https://developers.openai.com/api/docs/models):

| Tier | Example model IDs | Use in Mega Eval |
|------|-------------------|------------------|
| **Frontier** | `gpt-5.4` | **Preferred** for orchestration, Phase 2 synthesis, and Phase 1 when a single model is forced. |
| **Strong / lower cost** | `gpt-5.4-mini` | Acceptable for **parallel Phase 1 subagents** and Phase 3 outline **if** Phase 2 uses `gpt-5.4` or equivalent. |
| **High volume / simple** | `gpt-5.4-nano` | **Avoid** for Mega Eval’s main paths unless the user explicitly requests minimum cost; too thin for 12-lens critique + synthesis. |

**Reasoning controls:** When the host exposes reasoning effort for GPT-5.x-class models, prefer **medium or higher** for Phase 2 synthesis; Phase 1 can be **low–medium** if splitting effort to save latency.

---

## Anthropic (Claude API / Claude Code)

Per [Anthropic Models overview](https://platform.claude.com/docs/en/about-claude/models/overview):

| Tier | Claude API ID (examples) | Use in Mega Eval |
|------|---------------------------|------------------|
| **Frontier** | `claude-opus-4-6` | **Preferred** for Phase 2 synthesis and for single-model-all-phases runs. |
| **Speed + quality** | `claude-sonnet-4-6` | **Default** for Phase 1A–1C, 1D, and Phase 3 subagents when Opus is reserved for synthesis. |
| **Fast / economical** | `claude-haiku-4-5` (or dated snapshot ID) | **Avoid** for Phase 2; optional only for narrow, low-risk sub-tasks if the user demands cost savings. |

**Aliases:** Prefer stable **aliases** (e.g. `claude-sonnet-4-6`) over pinned snapshots unless you need reproducibility for a specific audit.

**Deprecations:** Follow [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — do not pin retired models (e.g. legacy Sonnet/Opus 4.0 snapshots with announced retirement dates) for new mega-eval runs.

---

## Phase mapping (quick)

| Phase | Minimum acceptable | Recommended |
|-------|---------------------|-------------|
| Phase 0 (brief) | Strong general | Frontier |
| Phase 1A–1C, 1D | Strong general | Sonnet 4.6+ / GPT-5.4-mini+ (or frontier if one knob) |
| Phase 2 synthesis | **Frontier or best available** | Opus 4.6 / GPT-5.4 |
| Phase 3 outline | Strong general | Sonnet 4.6 / GPT-5.4-mini+ |
| Phase 4 assembly | Same as orchestrator | Usually same model as Phase 2 context |

---

## What to record when logging

If `MEGA_EVAL_LOG` is on, append a single `model_check` line (see `SKILL.md`) with: provider, models used for orchestrator vs subagents (if known), and **pass** / **compromise** / **host_locked**.
