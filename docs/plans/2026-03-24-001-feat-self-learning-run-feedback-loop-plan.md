---
title: "feat: Self-learning mega-eval from run artifacts, corrections, and errors"
type: feat
status: completed
date: 2026-03-24
deepened: 2026-03-24
---

## Enhancement Summary

**Deepened on:** 2026-03-24  
**Sections enhanced:** Overview, Problem, Proposed Solution, Technical Considerations, Acceptance Criteria, Dependencies, SpecFlow, Implementation Phases, MVP schema  
**Research sources:** LLM observability / feedback-loop practice (tracing + human-in-the-loop promotion), agent pipeline patterns; document-review pass for clarity and scope boundaries  

### Key Improvements

1. Mapped run-log signals to **explicit / implicit / outcome** feedback types used in production LLM systems, without adopting a hosted observability product for MVP.
2. Added **promotion gates**, **redaction rules**, and explicit **out of scope** boundaries so “self-learning” cannot be confused with model training or silent prompt mutation.
3. Expanded the **MVP schema** with trace-friendly fields (run id, parent span, phase) suitable for future JSON export if needed.

### New Considerations Discovered

- Multi-phase agent workflows benefit from **request/run IDs** that tie subagent outputs back to one evaluation—even when logs stay Markdown.
- **Implicit feedback** (retries, abandonment, heavy edit) is as valuable as explicit “user_correction” events for prioritizing prompt fixes.

---

# ✨ feat: Self-learning mega-eval from run artifacts, corrections, and errors

## Overview

Extend the mega-eval skill so each run can **capture structured signals** (errors, retries, user corrections, thin-output flags) and **periodically fold validated learnings** into the skill’s instructions, prompts, and checklists. The goal is not automatic model training but **documented, reviewable improvement** of the methodology—so future runs inherit fixes without repeating the same failure modes.

### Research Insights

**Best practices (LLM apps, 2025–2026):**

- Treat observability as three dimensions where relevant: **operational** (latency, tool failures), **quality** (thin output, generic Phase 1), **safety/privacy** (leakage of sensitive subject matter into shared learnings). Mega-eval’s Markdown-first approach maps cleanly to **quality + operational**; safety is mostly **redaction + opt-in promotion**.
- Production feedback loops distinguish **explicit** (user says “fix X”), **implicit** (retries, abandoned phase, large rewrites), and **outcome** (user ships deliverables vs discards). The run log should capture all three where detectable.
- Prompt improvement cycles in industry are **observe → classify failure mode → change artifact → re-run eval**—aligned with promotion to `references/` and checklist updates, not weight updates.

**References:**

- [Closing the Loop: Building Practical Feedback Loops for LLM Apps](https://appropri8.com/blog/2025/11/13/feedback-loops-llm-apps/) — implicit vs explicit feedback
- [Langfuse — Evaluating LLM Applications roadmap](https://langfuse.com/blog/2025-11-12-evals) — eval + observability layering (conceptual; no vendor required for MVP)

## Problem Statement / Motivation

Today the pipeline is thorough but **stateless across sessions**: `SKILL.md` describes phases and error handling in the abstract, but there is no first-class place to record *what went wrong on run N* or *what the user had to correct before accepting deliverables*. That knowledge lives only in chat history or the user’s memory.

Without a feedback loop:

- Repeated tool failures (e.g., URL fetch, subagent timeout) do not systematically strengthen guardrails or prompts.
- User edits (“don’t use that competitor—they’re not direct”) are not captured as methodology updates.
- Quality issues (generic Phase 1 output, missing citations) recur because nothing promotes them to `references/` or checklist updates.

### Research Insights

**Classification:** When analyzing logs for promotion, tag failures using a small **failure-mode** vocabulary (e.g. `grounding`, `tool_timeout`, `scope_creep`, `format_mismatch`) so recurring issues surface in `references/learnings.md` without narrative drift.

## Proposed Solution

Introduce a **run record + learning promotion** pattern, local-first and optional:

1. **Run envelope** — For each mega-eval execution, write a small manifest under a conventional path (e.g. `sessions/<id>/run-log.md` or `.mega-eval/runs/<timestamp>/`) containing phase timestamps, tool outcomes, and explicit “correction events” (user-requested rewrites, errors fixed before final docs).
2. **Correction & error taxonomy** — Define lightweight categories: `tool_error`, `retry`, `user_correction`, `assumption_flag`, `quality_gate_fail`, `resolved_tension_edit`. The orchestrator (or a dedicated subsection in `SKILL.md`) instructs the agent to **append** to the run log when these occur—not only at the end.
3. **Seek step** — Before Phase 4 final assembly (or before declaring completion), add an explicit **“Review run log & unresolved issues”** sub-step: scan the session’s intermediate files and any logged errors; ensure the final deliverables reflect corrections; if something was corrected without updating the brief/synthesis, reconcile or document the delta.
4. **Promotion workflow** — After a run (or on a schedule), a **human-reviewed** promotion step moves stable patterns from run logs into durable artifacts:
   - `references/learnings.md` — bullet patterns (“When WebSearch returns little, Phase 1B must state confidence and avoid invented stats”).
   - Updates to `references/subagent-prompts.md`, `references/pipeline-checklist.md`, or `SKILL.md` **Error Handling** / phase instructions.
5. **Optional automation** — A script could diff `phase*` files early vs late in the session to infer edits; keep this **assistive**, not authoritative—human or explicit agent sign-off before merging learnings into the repo.

**Research decision:** The repo already encodes methodology in Markdown; **strong local context** applies. External research (LLM observability platforms, trace schemas) is **optional** for aligning field names and concepts—only needed if you adopt structured JSON logs or integrate with a host product’s telemetry.

### Research Insights

**Agent pipelines:** Subagents (Phase 1A–C) should log **the same `run_id`** so a later reviewer can see parallel tracks as one trace. If the host exposes “session id,” reuse it; otherwise generate a short id at Phase 0 and repeat in every subagent prompt template.

**UX of logging:** Logging must be **low friction**—one append per phase boundary plus on failure; avoid mandatory long forms. Offer `MEGA_EVAL_LOG=off` or a documented skip path for sensitive runs.

## Out of scope (explicit)

- **Model fine-tuning or embedding-based retrieval** over past runs.
- **Automatic rewriting** of `SKILL.md` or prompts from logs without human or explicit maintainer approval.
- **Hosted observability** (OpenTelemetry exporters, SaaS dashboards) in MVP—only hooks or field names that keep the door open.
- **Collecting end-user analytics** from installations you do not control; defaults remain local workspace only.

## Technical Considerations

- **Architecture impacts:** Purely additive: new `references/` files, new session subpaths, and new steps in `SKILL.md`. No runtime code is required for an MVP; `scripts/` could grow a log helper later.
- **Privacy:** Run logs may contain customer ideas and URLs. Default to **workspace-local** storage; never imply auto-upload. Document opt-in if copying learnings to a shared repo.
- **Security:** If logs include API errors, strip keys and tokens; redact sensitive URLs in shared learnings.
- **Portability:** Skills are copied as folders; learnings promoted to `references/` travel with the skill; raw `sessions/` data may stay user-private.

### Research Insights

**Performance:** Markdown append-only logs are negligible in size; cap individual event line length (e.g. 500 chars) to avoid accidental paste of huge tool dumps.

**Redaction before promotion:** When moving a pattern into `references/learnings.md`, **strip company names, URLs, and user identifiers**; keep only the methodological lesson.

## Promotion gates (when to merge into `references/`)

A learning is ready to promote when:

- [ ] It occurred on **at least one** run and the fix is **verified** by a second run or by maintainer review (for rare edge cases).
- [ ] It is **methodological** (prompt/checklist/skill wording), not subject-specific trivia.
- [ ] It does **not** duplicate an existing bullet; if it extends one, merge into the existing entry.
- [ ] A **redacted** one-line example is attached if it clarifies the pattern.

If any checkbox fails, keep the item in **Promotion candidates** in the run log only.

## System-Wide Impact

- **Interaction graph:** Phase 0–4 unchanged logically; an extra **logging append** after each phase boundary and a **pre-final review** gate before Phase 4 completion.
- **Error propagation:** Failed tools already noted in prose; the run log makes them **machine- and human-scannable** for promotion.
- **State lifecycle risks:** Multiple writes to the same log file suggest append-only format with timestamps; avoid destructive overwrites.
- **API surface parity:** Subagent prompts should mention logging paths so parallel tracks remain consistent.
- **Integration test scenarios:** (1) Simulated WebFetch failure → log entry → executive summary mentions gap. (2) User says “rewrite competitive section without X” → correction logged → final docs match → promotion candidate. (3) Subagent partial output → log notes incompleteness → checklist updated in a later PR.

## Acceptance Criteria

- [ ] `SKILL.md` defines **where** run artifacts and logs live, **what** to record (minimum schema), and **when** to append (per phase + on error/correction).
- [ ] A **pre-final review** step requires reconciling logged corrections/errors with deliverables (or explicitly documenting remaining gaps).
- [ ] New `references/learnings.md` (or equivalent) exists with a template for promoted patterns and **“do not promote without review”** guidance.
- [ ] `references/pipeline-checklist.md` includes checklist items for run logging and post-run promotion (optional second checklist).
- [ ] README or `SKILL.md` states **privacy defaults** and how users can disable or relocate logging.
- [ ] At least one **worked example** in `examples/` or docs showing a fictional `run-log.md` and a promoted learning entry.
- [ ] Subagent prompt templates include **placeholder line** for `run_id` / log path so Phase 1 tracks stay correlated.

## Success Metrics

- **Quantitative:** Reduction in repeated user corrections on similar inputs (subjective unless tracked); number of promoted learnings merged per month.
- **Qualitative:** Maintainers can answer “what broke last time?” from run logs; new contributors can improve prompts from `learnings.md` without replaying old chats.

## Dependencies & Risks

| Dependency / risk | Mitigation |
|-------------------|------------|
| Host environment may not persist `sessions/` paths uniformly | Document fallback: user-chosen workspace root; single `run-log.md` at project root option |
| Log noise overwhelms value | Start with minimal schema; tier “verbose” optional |
| Auto-inferred “corrections” are wrong | Human review before promoting to `references/` |
| Scope creep into full observability product | Keep MVP to Markdown + checklist; defer JSON pipelines |
| “Self-learning” misread as autonomous self-modification | Name user-facing copy “run feedback” or “learned patterns”; keep **Promotion gates** visible in README |

## SpecFlow / Edge Cases (consolidated)

- User runs mega-eval on **highly sensitive** subject → logs off by default or redacted mode.
- **Interrupted run** → partial log still useful; “status: abandoned” marker.
- **No user corrections** → log still captures phase completions for timing/debug.
- **Multiple subjects in one session** → separate run IDs or clearly separated sections in one log.
- **User approves deliverables but never promotes** → acceptable; logs remain forensic only.

## Implementation Phases (suggested)

1. **Foundation:** Add log schema + `references/learnings.md` template; update `SKILL.md` with append + review steps.
2. **Integration:** Update checklist and subagent prompts to reference logging paths and `run_id`.
3. **Examples & docs:** Add example run log + one promoted learning; README blurb.
4. **Optional:** Script to suggest promotions from diff/timestamps; still require human ack.

## Sources & References

- **Internal:** [`SKILL.md`](../../SKILL.md) — phases, error handling, deliverable paths; [`references/pipeline-checklist.md`](../../references/pipeline-checklist.md); [`references/subagent-prompts.md`](../../references/subagent-prompts.md)
- **Patterns (conceptual):** Human-in-the-loop feedback on LLM runs; append-only event logs for auditability (industry practice; no vendor lock-in required for MVP)
- **External (concepts):** [Appropri8 — Feedback loops for LLM apps](https://appropri8.com/blog/2025/11/13/feedback-loops-llm-apps/); [Langfuse — Evals roadmap](https://langfuse.com/blog/2025-11-12-evals)

---

## MVP (minimal viable logging snippet)

Illustrative only—final schema may differ:

```markdown
# Run log — <run_id>

## Meta
- run_id: <short-id>   # same id injected into Phase 1A–C prompts
- started: ISO8601
- workspace: <path>
- status: in_progress | complete | abandoned

## Events (append-only)
- [timestamp] phase_start phase0
- [timestamp] tool_error web_fetch url=<redacted> message="…"
- [timestamp] retry phase=1b attempt=2
- [timestamp] implicit_signal heavy_edit target=phase1b-competitive-raw.md
- [timestamp] user_correction phase=1b note="…"
- [timestamp] phase_complete phase4

## Failure modes (tags for promotion search)
- [timestamp] grounding | tool_timeout | … — brief note

## Promotion candidates (unchecked until reviewed)
- [ ] …
```
