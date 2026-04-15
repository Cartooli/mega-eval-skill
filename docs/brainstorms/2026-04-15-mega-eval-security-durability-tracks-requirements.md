---
date: 2026-04-15
topic: mega-eval-security-durability-tracks
---

# Mega-eval: Phase 1E (security) and Phase 1F (AI durability) analysis tracks

## Problem Frame

The current mega-eval pipeline covers critical feedback (1A), competitive context (1B), strengths (1C), and optionally live-site design (1D). It does **not** produce structured findings on two increasingly important dimensions for 2026-era product critique:

1. **Security posture** — public-surface security tells, auth/privacy signals, third-party script exposure, data-handling claims vs reality. Today these get surfaced incidentally (a hater-mode persona may poke at trust) but never as structured, prioritized findings.
2. **AI / agent durability** — for AI-first or agent-centric subjects, resilience to model deprecations, provider shifts, and capability changes is often the single biggest long-term risk. The current pipeline has no lens for it.

Adding these as **parallel Phase 1 tracks** (following the 1D pattern) fills both gaps without disturbing existing phases or deliverables.

## Requirements

- R1. **Add Phase 1E — Security audit track.** Spawned as a parallel Phase 1 subagent alongside 1A–1D. Consumes the Evaluation Brief and, when available, the Primary URL for live inspection. Produces `phase1e-security-raw.md`.
- R2. **Add Phase 1F — AI/agent durability track.** Spawned as a parallel Phase 1 subagent. Consumes the Evaluation Brief and the Primary URL. Produces `phase1f-durability-raw.md`. Applies when the subject has meaningful AI/LLM/agent surface; writes a short "not applicable" stub and exits otherwise.
- R3. **Gating mirrors 1D.** Each track runs by default when inputs permit. Opt-out via env vars: `MEGA_EVAL_SECURITY_AUDIT` and `MEGA_EVAL_DURABILITY_AUDIT` (values `0`, `off`, `false` disable). Applicability decisions are recorded in the Evaluation Brief during Phase 0, same pattern as the 1D **Audit decision** line.
- R4. **Evidence sources.** Both tracks may use the Evaluation Brief and the Primary URL via WebFetch or headless browse. They **must not** invoke broad supply-chain search, repo inspection, or credential-bearing probes. If the Primary URL is unavailable, each track degrades to a brief-only pass and states the limit in its output Meta.
- R5. **Scored risk band + findings.** Each track produces:
  - A headline **risk band**: `Low` | `Medium` | `High` | `Critical` (plus `N/A` for 1F when no AI surface).
  - A one-line **headline for synthesis** capturing the dominant concern.
  - Structured findings with severity, evidence, and suggested direction — never prescriptive remediation code.
- R6. **1E scope — security.** Focus on what is observable from the public surface and stated claims:
  - Transport and headers (HTTPS posture, obvious missing security headers on the primary URL only).
  - Auth/session surface tells (login patterns, password rules visible on signup, presence/absence of MFA copy, session cookie flags on the primary URL).
  - Privacy and data-handling claims vs visible behavior (what the privacy policy promises vs what the marketing page actually loads — trackers, third-party scripts).
  - LLM/AI-specific exposure when relevant: prompt-injection surface, user-content-to-model pathways, data retention claims.
  - Red-flag patterns: secrets-in-URLs, auth tokens in client-visible code, obviously leaky share links.
- R7. **1F scope — durability.** Focus on resilience of the AI/agent surface to change:
  - Model abstraction: is the subject locked to a specific model family, or does its positioning imply portability?
  - Prompt architecture signals: fragile model-specific behavior claims, reliance on tool-use features that vary by provider.
  - Provider concentration: single-vendor AI dependency, pricing fragility.
  - Capability drift risk: marketing claims that depend on today's model capabilities holding.
  - Evals/feedback loop presence: any public signal of how the team monitors quality over model changes.
- R8. **Synthesis integration.** Phase 2 reads `phase1e-security-raw.md` and `phase1f-durability-raw.md` when present and merges findings into **Critical Fixes** (by severity) and **Proposed Next Steps** (by effort-to-impact), cross-referenced by source track. Headline risk bands feed the executive summary.
- R9. **Deliverable shape — no new .docx files.** Findings fold into the existing `04-critical-fixes-and-design.docx`. The executive summary gains two optional mini-sections (**Security Posture** and **AI Durability Posture**) that appear only when their respective tracks ran and produced non-stub output.
- R10. **Failure isolation.** A failure, timeout, or thin-output result from 1E or 1F **must not** block Phase 2. The pipeline follows the same `tool_error` / `failure_mode` run-log pattern already used for 1D.
- R11. **Run correlation.** Both tracks receive and echo the `run_id`, and append the standard phase markers to `run-log.md` when logging is enabled.
- R12. **Reference skills.** Each track's subagent prompt points at the canonical external skill for its methodology (`/cso` for 1E, `/durability-review` for 1F) and instructs the subagent to read that skill's SKILL.md at run time — so methodology stays single-sourced and we do not fork prompt content into this repo.

## Success Criteria

- A decision-maker reading the executive summary for an AI-first product sees an at-a-glance **security risk band** and **durability risk band** with one-line headlines, alongside the existing design/competitive signals.
- For non-AI subjects, 1F exits cleanly with a visible "not applicable" record and no padded content leaks into the final docs.
- Running mega-eval on a subject with no primary URL still produces useful brief-only security/durability passes, with limits stated in the output.
- Maintainers can update security or durability methodology by changing `/cso` or `/durability-review` once — the mega-eval skill does not hold a duplicated copy.
- A 1E or 1F subagent failure degrades the run instead of breaking it; synthesis proceeds with the tracks that did complete.

## Scope Boundaries

- **Non-goal:** Turning mega-eval into a pen-test or security compliance tool. 1E is report-only, observation-based, and never attempts credential testing, rate-limit probing, or anything intrusive.
- **Non-goal:** Supply-chain or dependency-graph analysis. That needs repo access and is a different skill.
- **Non-goal:** Broadening 1F beyond AI/agent durability into general vendor/platform risk. Platform lock-in concerns continue to live inside 1B competitive context.
- **Non-goal:** New standalone .docx deliverables. Everything flows through existing synthesis and the existing 04 doc.
- **Non-goal:** Changing 1A–1D behavior. This is purely additive.

## Key Decisions

- **Two tracks, not one combined "technical risk" track.** Security and AI durability have different reference skills, different evidence bases, and different synthesis consumers; merging them would muddy both the subagent prompts and the executive summary headlines.
- **Primary URL only for live inspection, no broad search.** Keeps the pipeline fast, portable, and defensible — no risk of the subagent wandering into unrelated domains or issuing probes.
- **Risk band + findings, not raw findings alone.** Mirrors 1D's proven pattern; gives synthesis an unambiguous prioritization signal; avoids forcing Phase 2 to re-derive severity.
- **Fold into existing deliverable, add exec-summary sections.** Keeps the file count stable, which matters for downstream consumers. Standalone docs can be revisited if specialist audiences start asking for them.
- **1F gated on AI surface, 1E not gated.** Every subject has *some* security angle even if shallow; only AI durability is genuinely "not applicable" for non-AI subjects.
- **External skill reference, not embedded prompts.** Same reasoning as the sub-skills brainstorm: shared methodology, no prompt drift.

## Dependencies / Assumptions

- Assumes `/cso` and `/durability-review` skills are available on the host where mega-eval runs. If they are not, the subagent prompts must state the fallback (proceed with the checklist embedded in the prompt; note methodology limit in output Meta).
- Assumes the existing `references/` directory remains the home for any embedded fallback checklists — consistent with R3 of the sub-skills brainstorm (shared references, no forks).
- Assumes headless browse / WebFetch remains available in the host; if not, both tracks degrade to brief-only and state it.

## Outstanding Questions

### Resolve Before Planning

*(none — all product decisions resolved during brainstorm)*

### Deferred to Planning

- [Affects R3][Technical] Where does the Phase 0 applicability check for 1F ("has AI/agent surface") live — a heuristic in the brief-generation step, or a lightweight first-pass inside the 1F subagent that can early-exit? Planning should pick the simpler seam.
- [Affects R6][Needs research] Concrete checklist contents for the 1E fallback when `/cso` is not available on the host — what is the minimum viable set of observation categories that survives without the external skill?
- [Affects R7][Needs research] Same as above for 1F fallback without `/durability-review` — pick the subset of the five durability dimensions (model abstraction, prompt architecture, etc.) that can be judged from a marketing URL alone.
- [Affects R8][Technical] Exact synthesis cross-reference format: how do Critical Fixes cite 1E/1F alongside existing 1A/1D citations without bloating the doc? Planning should propose a compact tag scheme.
- [Affects R9][Technical] Exec-summary mini-section wording template (what the "Security Posture" and "AI Durability Posture" blocks look like — sentence count, inclusion of risk band, inclusion of top finding).
- [Affects R12][Technical] Discovery mechanism for the `/cso` and `/durability-review` skill paths on the host — reuse the same lookup pattern mega-eval already uses for `hater-mode` and `long-form-outline`.

## Next Steps

→ `/ce:plan` for structured implementation planning
