---
title: "feat: Mega-eval Phase 1E (security) and Phase 1F (AI durability) analysis tracks"
type: feat
status: completed
date: 2026-04-15
origin: docs/brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md
---

# feat: Mega-eval Phase 1E (security) and Phase 1F (AI durability) analysis tracks

## Overview

Extend the mega-eval pipeline with two new parallel Phase 1 analysis tracks, mirroring the already-shipped Phase 1D (live-site design audit) pattern:

- **Phase 1E — Security audit** (CSO-style): structured, observation-only security findings with a scored risk band. Always runs when inputs allow; opt-out via `MEGA_EVAL_SECURITY_AUDIT`.
- **Phase 1F — AI / agent durability audit** (durability-review-style): resilience of the subject's AI/agent surface to model/API/provider change, with a scored risk band. Gated on AI surface presence; opt-out via `MEGA_EVAL_DURABILITY_AUDIT`.

Findings fold into the existing `04-critical-fixes-and-design.docx` and executive summary — no new `.docx` files. Methodology stays single-sourced in the external `/cso` and `/durability-review` skills; this repo only ships **fallback** checklists in `references/` so the tracks still work if those skills are not installed on the host.

This plan carries forward all decisions from the origin document (see origin: `docs/brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md`). It resolves every question that was tagged `Deferred to Planning` there.

## Problem Statement / Motivation

The current pipeline covers critical feedback (1A), competitive context (1B), strengths (1C), and optional live-site design (1D). For 2026-era product critique, two dimensions are missing as structured tracks:

1. **Security posture** — public-surface tells, auth/privacy signals, third-party script exposure, LLM-specific exposure (prompt-injection surface, data-retention claims). Today these leak into 1A anecdotally and never get a risk band.
2. **AI / agent durability** — for AI-first or agent-centric subjects, resilience to model deprecations and provider shifts is often the single biggest long-term risk. The current pipeline has no lens for it.

Adding both as parallel tracks with the same shape as 1D (subagent → raw markdown → synthesis merge → exec-summary one-liner) fills both gaps without disrupting existing phases or deliverables.

## Proposed Solution

### 1. Two new parallel Phase 1 tracks, same shape as 1D

- **Phase 1E — Security audit** runs alongside 1A–1D.
  - Inputs: Evaluation Brief + Primary URL (from the existing Phase 0 selection — no new URL classification).
  - Output: `phase1e-security-raw.md` with risk band (`Low | Medium | High | Critical`), headline for synthesis, and structured findings.
  - Never attempts credential testing, rate-limit probing, or any intrusive action. Report-only.
- **Phase 1F — AI durability audit** runs alongside 1A–1D.
  - Inputs: same as 1E.
  - Output: `phase1f-durability-raw.md` with risk band (`Low | Medium | High | Critical | N/A`).
  - When the subject has no meaningful AI/LLM/agent surface, 1F writes a short "not applicable" stub (risk band `N/A`, one-line rationale, no padded content) and exits.

### 2. Applicability is owned by the subagent, not Phase 0

The origin document asked whether 1F's applicability check belongs in Phase 0's brief-generation step or inside the 1F subagent. **Decision: inside the 1F subagent.**

- Simpler seam: one place owns the AI-surface judgment, which is inherently a reading task the subagent is already doing.
- No Phase 0 heuristic to maintain or drift from the subagent's logic.
- The brief's `Live site / design audit` block in Phase 0 stays unchanged; we add two new one-line fields for audit decisions only (see § 3 below). Phase 0 **does not** pre-classify AI surface — it just records the intended run decision (`run | skipped — <reason>`).

### 3. Phase 0 changes

Extend the Evaluation Brief template (in `SKILL.md` and the brief it emits) with two new rows, symmetric to the existing 1D block:

```markdown
## Security audit (Phase 1E)
- **Audit decision:** [run | skipped] — [one-line reason: env opt-out, no usable evidence, etc.]

## AI durability audit (Phase 1F)
- **Audit decision:** [run | skipped] — [one-line reason: env opt-out, etc.]
- **AI-surface applicability note:** [orchestrator's quick guess if easy; else `defer to 1F subagent`]
```

Rules, in order of precedence:

1. `MEGA_EVAL_SECURITY_AUDIT` in (`0`, `off`, `false`) → 1E **skipped** (reason: env opt-out).
2. `MEGA_EVAL_DURABILITY_AUDIT` in (`0`, `off`, `false`) → 1F **skipped** (reason: env opt-out).
3. Otherwise → both **run**. For 1F, the applicability call happens inside the subagent; if it finds no AI surface it writes the stub and exits cleanly (not a failure).

### 4. New subagent prompts

Add Phase 1E and Phase 1F prompt templates to `references/subagent-prompts.md`, following the exact pattern used for 1D (run correlation header, read external skill, consume brief, emit markdown to named file).

Both prompts must:

- Echo `run_id` + `run_log` in a one-line HTML comment at the top of the saved file.
- Read the canonical external skill at `<cso-skill-path>/SKILL.md` (1E) or `<durability-review-skill-path>/SKILL.md` (1F) when available. Placeholders resolve at run time on the host, identical to the existing `<hater-mode-skill-path>` pattern.
- **Fallback behavior:** if the external skill is not available, follow the embedded checklist inside the corresponding template in `references/` (see § 5) and state `methodology: fallback` in Meta.
- Use **only** the Primary URL for live inspection (WebFetch or headless browse). **No** broad WebSearch, **no** repo inspection, **no** credentialed probes, **no** rate-limit tests.
- Produce the fixed template sections (see § 5), including the risk band.

### 5. New reference templates

Add two new files under `references/`, each serving double duty as the output template **and** the minimum-viable fallback checklist when the external skill is unavailable:

- **`references/security-audit-template.md`** — output template for `phase1e-security-raw.md`:
  - Correlation header comment
  - **Meta** table: audit URL, evidence tier (A/B/C mirroring 1D), methodology (`external: /cso` or `fallback: embedded`), limits
  - **Transport & headers** (HTTPS posture, obvious missing headers on primary URL only)
  - **Auth & session surface** (signup/login copy, MFA claims, cookie flags observable without login)
  - **Privacy & data handling** (marketing claims vs observable third-party scripts/trackers; privacy policy cross-check)
  - **LLM / AI exposure** (prompt-injection surface, user-content-to-model pathways, retention claims — skip section if no AI surface)
  - **Red flags** (secrets in URLs, auth tokens in client-visible code, leaky share links)
  - **Findings table**: `#`, finding, severity (`Low | Medium | High | Critical`), evidence snippet, suggested direction
  - **Disclaimer**: heuristic and observation-only; not a pen-test, not compliance certification
  - **Headline for synthesis**: `Security risk band: <band>` + one-line summary
- **`references/durability-audit-template.md`** — output template for `phase1f-durability-raw.md`:
  - Correlation header
  - **Meta** table: audit URL, evidence tier, methodology, limits, **AI surface present** (yes/no — if no, emit stub and stop)
  - **Model abstraction** (locked to one model family, or portable positioning)
  - **Prompt architecture signals** (fragile model-specific claims, reliance on provider-specific tool-use)
  - **Provider concentration** (single-vendor AI dependency, pricing fragility)
  - **Capability drift risk** (claims that assume today's model capabilities hold)
  - **Evals / feedback loop presence** (public signals of how quality is monitored over model changes)
  - **Findings table**: same shape as 1E
  - **Disclaimer**
  - **Headline for synthesis**: `AI durability risk band: <band>` + one-line summary

Each template explicitly states it is the **fallback** methodology when `/cso` or `/durability-review` is unavailable on the host, so maintainers know what to preserve if the external skills change.

### 6. Phase 2 synthesis integration

Extend `SKILL.md` Phase 2 instructions so synthesis reads `phase1e-security-raw.md` and `phase1f-durability-raw.md` when present, and folds findings into existing sections:

- **Critical Fixes Needed** — add 1E `Critical` and `High` findings first; 1F `Critical` and `High` findings next. Dedupe against 1A persona commentary where relevant (prefer 1E/1F as authoritative for security/durability specifics, keep 1A for reception/credibility narrative).
- **Design Inconsistencies to Resolve** — unchanged; 1E/1F findings do **not** go here.
- **Proposed Next Steps (Non-Breaking Changes)** — add 1E/1F `Medium` findings and any quick wins under the existing effort-to-impact buckets.
- **Unresolved Tensions** — add security vs. speed-to-market, durability vs. model-chasing, etc., when they genuinely surface.

**Cross-reference tag format:** the origin document's deferred question on compact citation is resolved as:

```
[Flagged by: 1E-S3, 1F-D2, 1A(Skeptical Engineer)]
```

`1E-S<n>` = Security finding `<n>` from 1E's findings table. `1F-D<n>` = Durability finding `<n>`. This keeps synthesis compact and lets a reader jump back to the raw file by table row.

### 7. Phase 4 deliverable changes

- **No new `.docx` files.** Findings continue to route through `04-critical-fixes-and-design.docx` via Phase 2 synthesis.
- **Executive summary** (`00-executive-summary.docx`) gains two new **optional** mini-sections, placed after `Live Site / Product Surface` when the tracks ran. Template (resolves origin's deferred "exec-summary wording" question):

  ```markdown
  ### Security Posture (only if Phase 1E ran)
  **Risk band:** Low | Medium | High | Critical
  [One-line headline from `phase1e-security-raw.md`]
  [Top finding, one line with `[1E-S<n>]` citation]
  [Top quick-win next step, one line — or omit if none]

  ### AI Durability Posture (only if Phase 1F ran and risk band is not N/A)
  **Risk band:** Low | Medium | High | Critical
  [One-line headline from `phase1f-durability-raw.md`]
  [Top finding, one line with `[1F-D<n>]` citation]
  [Top quick-win next step, one line — or omit if none]
  ```

  When 1F exits with `N/A`, the AI Durability Posture section is omitted entirely — no "not applicable" stub in the exec summary.

### 8. Pipeline checklist updates

Add rows to `references/pipeline-checklist.md`:

- Pre-Flight: two new bullets for `MEGA_EVAL_SECURITY_AUDIT` and `MEGA_EVAL_DURABILITY_AUDIT` handling, symmetric to the existing `MEGA_EVAL_DESIGN_AUDIT` row.
- Phase 0: note the two new brief sections.
- Phase 1: two new launch bullets (1E always when allowed; 1F always when allowed), and a "do not block Phase 2 on 1E/1F alone" bullet.
- Phase 2: a bullet confirming synthesis read of 1E/1F when present and dedupe rule against 1A.
- Phase 4: a bullet confirming exec-summary Security / AI Durability sections appear when the tracks ran with non-stub output.
- Quality Checks: a bullet that 1E/1F findings cite concrete evidence (URL snippet, observed text) rather than speculation.

### 9. Failure isolation & run logging

- A failure, timeout, or Tier C thin output from 1E or 1F **must not** block Phase 2. Synthesis proceeds with the tracks that did complete, mirroring existing 1D handling.
- When `MEGA_EVAL_LOG` is on, append `phase_start phase1`/`phase_complete phase1` as today, plus `tool_error` / `retry` / `failure_mode` lines scoped to 1E or 1F as they occur. No new event taxonomy needed.

### 10. External skill discovery

The origin document's deferred question on skill-path discovery is resolved by reusing the existing placeholder convention: subagent prompts include `<cso-skill-path>` and `<durability-review-skill-path>` exactly like `<hater-mode-skill-path>` and `<long-form-outline-skill-path>` today. The orchestrator substitutes before spawning. If the host cannot resolve either path, the subagent falls back to the embedded template checklist and records `methodology: fallback` in Meta. No new discovery mechanism is introduced.

## Technical Considerations

- **Tier A/B/C evidence handling** mirrors 1D. 1E and 1F share the same browse/WebFetch capability discovery; if browse is unavailable, Tier B with HTML-visible content is acceptable (disclose limits). Tier C is a short stub file.
- **Dedupe vs 1A** (security): 1E is authoritative for structured security findings; 1A personas that touch on trust stay in 1A but should not re-appear as Critical Fixes if 1E already surfaced them. Synthesis rule codified in § 6.
- **Dedupe vs 1B** (durability): 1F stays strictly on AI/agent durability. General vendor/platform lock-in stays inside 1B per origin scope boundary. If a finding is genuinely cross-cutting, synthesis cites both.
- **Token / wall-time cost:** adding two parallel subagents slightly raises wall time but preserves parallelism. Each track is capped to the Primary URL + at most one privacy-policy page (1E only) — no crawling.
- **Opt-out symmetry:** every new env var follows the same `0|off|false` parsing as `MEGA_EVAL_LOG` and `MEGA_EVAL_DESIGN_AUDIT`. Document in `SKILL.md` "Optional live-site design audit" region, renamed or extended to cover all three.
- **Thin-skill packaging:** consistent with the sub-skills brainstorm (see `docs/brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md`), this plan does **not** add new thin skills. If `mega-eval-security` and `mega-eval-durability` are desired later, they plug into the same `references/` tree without duplicating methodology — same rule that already governs 1D.
- **Sensitive subject matter**: 1E findings may touch on redactable details (URLs with tokens, visible email addresses). Run-log redaction rules already in SKILL.md cover this; call it out explicitly in the 1E subagent prompt so the subagent does not paste secrets into raw output.

## System-Wide Impact

- **Interaction graph:** Phase 0 emits brief + two new audit-decision rows → Phase 1 spawns 1A/1B/1C (+ 1D, 1E, 1F when allowed) in parallel → Phase 2 reads up to six raw files → Phase 4 exec summary pulls three optional posture sections (Design, Security, AI Durability) when their tracks ran.
- **Error propagation:** 1E/1F errors are isolated. Same pattern as 1D: log and continue. Synthesis notes which tracks were skipped or thin.
- **State lifecycle:** two new workspace artifacts (`phase1e-security-raw.md`, `phase1f-durability-raw.md`). Phase 4 pre-flight treats both as optional inputs.
- **API surface parity:** The full `mega-eval` SKILL.md, the pipeline checklist, and `subagent-prompts.md` all gain matching rows. If thin sub-skills are added later, they must be added in lockstep — flagged explicitly in § 5's template docs.

## Acceptance Criteria

- [x] `SKILL.md` Phase 0 documents the two new brief rows and env-var opt-out rules.
- [x] `SKILL.md` Phase 1 documents 1E and 1F tracks (purpose, inputs, output filenames, failure isolation) — placed after the existing Phase 1D block.
- [x] `SKILL.md` Phase 2 synthesis instructions reference `phase1e-security-raw.md` and `phase1f-durability-raw.md` and the dedupe rule against 1A.
- [x] `SKILL.md` Phase 4 executive summary spec gains optional `Security Posture` and `AI Durability Posture` mini-sections with the wording from § 7.
- [x] `SKILL.md` Error Handling section gains a 1E/1F bullet mirroring the existing 1D bullet.
- [x] `references/subagent-prompts.md` contains full Phase 1E and Phase 1F prompt templates, including run correlation header, external-skill placeholder, fallback instruction, URL-only evidence constraint, and output filename.
- [x] `references/security-audit-template.md` exists with the sections listed in § 5 and doubles as the fallback checklist.
- [x] `references/durability-audit-template.md` exists with the sections listed in § 5 and the `N/A` stub protocol for non-AI subjects.
- [x] `references/pipeline-checklist.md` gains rows in Pre-Flight, Phase 0, Phase 1, Phase 2, Phase 4, and Quality Checks per § 8.
- [x] Env vars `MEGA_EVAL_SECURITY_AUDIT` and `MEGA_EVAL_DURABILITY_AUDIT` are documented with `0|off|false` opt-out parity.
- [x] Cross-reference tag format `[1E-S<n>]` / `[1F-D<n>]` appears in the synthesis section of `SKILL.md` with at least one worked example.
- [x] No new `.docx` files are introduced; `04-critical-fixes-and-design.docx` remains the single destination for merged findings.
- [ ] Dry-run sanity check: running mega-eval on (a) a non-AI subject with a marketing URL produces a clean 1F `N/A` stub and a meaningful 1E output; (b) a subject with no Primary URL produces brief-only 1E and 1F passes that state their limits; (c) env opt-out produces skipped decisions recorded in the brief and no raw files.
- [x] Origin cross-check: every requirement `R1`–`R12` from the origin document is reflected above.

## Success Metrics

- Evaluations of AI-first products consistently include Security and AI Durability posture sections in the executive summary, grounded in observed evidence from the Primary URL.
- Non-AI subjects produce clean `N/A` for 1F without padded content leaking into Phase 2 or Phase 4.
- Maintainers updating CSO or durability-review methodology change one external skill; mega-eval stays in sync without edits here (except when the fallback templates themselves need updating).
- A 1E or 1F subagent failure degrades the run without breaking Phase 2 or Phase 4.

## Dependencies & Risks

- **Dependency:** `/cso` and `/durability-review` skills ideally installed on the host for highest-fidelity output. Mitigated by embedded fallback checklists in the two new template files; fallback mode is explicitly labelled in Meta.
- **Dependency:** WebFetch or headless browse available for Tier A/B evidence. Missing capability downgrades to Tier C + stated limits — same degradation path as 1D.
- **Risk — scope creep:** 1E might drift toward broader vulnerability scanning or 1F toward general platform risk. Mitigation: strict scope boundaries in § 5 templates plus the Non-goals section of the origin doc referenced here.
- **Risk — false precision in risk bands:** four-point bands (`Low/Medium/High/Critical`) can feel over-precise. Mitigation: template guidance requires explicit evidence per finding and a stated confidence line next to the band.
- **Risk — secrets in raw output:** 1E observing URLs or form HTML could capture tokens. Mitigation: subagent prompt explicitly instructs redaction for anything that looks like a token or key before saving the raw file.
- **Risk — drift between `SKILL.md` and `references/`:** multiple files change together. Mitigation: acceptance checklist above enumerates all touch points; PR review must verify parity.

## Research & Decision Record (ce-plan)

- **Origin:** `docs/brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md`. All `R1`–`R12` requirements carried forward; every `Deferred to Planning` question resolved above (§§ 2, 5, 6, 7, 10).
- **Local research:** Read `SKILL.md` (full pipeline), `references/subagent-prompts.md`, `references/design-audit-template.md`, `references/pipeline-checklist.md`, `references/learnings.md`, and the 1D precedent plan `docs/plans/2026-03-25-001-feat-mega-eval-optional-design-review-plan.md`. 1D gives the exact pattern to mirror for gating, failure isolation, synthesis hooks, and exec-summary inclusion.
- **External research:** Skipped — this is a packaging / methodology extension. External methodology lives in the `/cso` and `/durability-review` skills the plan explicitly delegates to, so external docs research would duplicate those skills' own sources.
- **SpecFlow-style gaps addressed:** env-var opt-out, no-URL degradation, 1F applicability stub, secrets redaction in raw output, dedupe against 1A/1B, failure isolation, exec-summary optional sections, citation compactness.

## Sources & References

### Origin

- **Origin document:** [docs/brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md](../brainstorms/2026-04-15-mega-eval-security-durability-tracks-requirements.md) — carried forward: two-track split (1E + 1F), risk-band-plus-findings output shape, fold into existing `04` deliverable, URL-only evidence, 1F gated on AI surface.

### Internal References

- Pipeline spec: [SKILL.md](../../SKILL.md)
- Existing subagent prompts: [references/subagent-prompts.md](../../references/subagent-prompts.md) — 1D block is the nearest template
- 1D output template: [references/design-audit-template.md](../../references/design-audit-template.md) — structural parent of the two new templates
- Pipeline checklist: [references/pipeline-checklist.md](../../references/pipeline-checklist.md)
- Learnings (methodological): [references/learnings.md](../../references/learnings.md)
- 1D precedent plan: [docs/plans/2026-03-25-001-feat-mega-eval-optional-design-review-plan.md](2026-03-25-001-feat-mega-eval-optional-design-review-plan.md)
- Sub-skills packaging contract: [docs/plans/2026-03-24-004-feat-mega-eval-sub-skills-plan.md](2026-03-24-004-feat-mega-eval-sub-skills-plan.md)

### External References

- `/cso` skill — infrastructure-first security audit methodology (host-resolved at run time)
- `/durability-review` skill — AI agent codebase durability methodology (host-resolved at run time)
