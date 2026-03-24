---
title: "feat: Sustain the self-learning loop (ritual, staleness, optional assistive tooling)"
type: feat
status: completed
date: 2026-03-24
deepened: 2026-03-24
origin: docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md
---

## Enhancement Summary

**Deepened on:** 2026-03-24  
**Sections enhanced:** Overview, Proposed Solution, Technical Considerations, Acceptance Criteria, Implementation Phases, SpecFlow, Sources  
**Research:** OSS maintainer guidance emphasizes **written processes** and **keeping docs honest** when they drift; formal monthly cadences are rare—pairing ritual with **release/PR checkpoints** reduces reliance on memory ([Open Source Guides — Best practices for maintainers](https://opensource.guide/best-practices/)).  
**Refine pass:** Tighter triggers, explicit verification checklist, default **skip** for optional script unless adopted.

### Key improvements

1. **Release gate** tied to **merge to default branch** or **tag** (whichever the repo actually uses)—avoids vague “notable skill change.”
2. **Definition of done** for Phase 1 so `/ce:work` can verify without interpretation.
3. **Optional script** explicitly **off by default** in planning terms: ship docs first; add script only if a maintainer commits to ownership.

### New considerations

- **CONTRIBUTING.md** is optional: link from README only if you want drive-by contributors to see the ritual; otherwise `MAINTAINERS.md` + README suffices (YAGNI).

---

# feat: Sustain the self-learning loop (ritual, staleness, optional assistive tooling)

## Overview

Close the gap between **having** run logs + `references/learnings.md` and **actually compounding** methodology over time. The origin brainstorm defined requirements R1–R5 (signal breadth, review ritual, assistive-only automation, staleness visibility, privacy defaults) and explicitly rejected model fine-tuning and unreviewed auto-edits to the skill. (see origin: [docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md](../../brainstorms/2026-03-24-self-learning-sustainability-requirements.md))

### Research insights

- **Process over tools:** Small OSS projects sustain habits when the checklist is **short** and anchored to events people already do (merge, release), not only calendar guilt ([Open Source Guides](https://opensource.guide/best-practices/)).
- **Honesty about staleness:** If `learnings.md` cannot be reviewed in a cycle, updating `last_reviewed` with “no changes” is still progress—prevents fictional freshness.

## Problem Statement / Motivation

Run feedback shipped, but **entropy** remains: logs accumulate, promotion candidates may never be reviewed, and `learnings.md` can stay a thin placeholder. Without a **named ritual** and **staleness hygiene**, “self-learning” does not compound. (see origin: Problem frame + Success criteria)

## Proposed Solution

### 1. Primary review trigger (resolves deferred brainstorm question)

**Default recommendation for v1:** Document a **dual trigger** that is cheap to remember:

- **Calendar:** At least **monthly**, skim unchecked promotion candidates from recent `run-log` files (or a single workspace log) and decide promote / drop / defer.
- **Release gate:** On each **merge to the default branch** that changes `SKILL.md`, `references/`, or `examples/`, or when **tagging a release** (if you tag), spend **≤5 minutes**: any new `learnings.md` bullets? Update `last_reviewed` in `references/learnings.md` if you reviewed (even if nothing to promote).

**Optional add-on** (document only, not required for MVP): When **≥3** unchecked promotion candidates exist in the active log, treat review as **high priority** before the next merge—still no automation.

Rationale: Matches the brainstorm table’s **“Monthly learnings review + optional suggest script”** baseline and satisfies **R2** without telemetry. (see origin: Alternatives considered + R2)

### 2. Staleness visibility (R4)

- Add **YAML frontmatter** to `references/learnings.md`: `last_reviewed: YYYY-MM-DD` (update when a review pass completes, even if zero promotions).
- **Per-bullet dates** remain the norm for new entries; retire stale bullets by moving to **Retired patterns** or removing with a one-line PR rationale.

### 3. Signal breadth (R1) — documentation-only tightening

- **`MAINTAINERS.md`** lists **signal types** to capture in run logs when logging is on: explicit correction, tool failure, retry, thin output, optional outcome note (`outcome_complete` / `outcome_abandoned`)—with explicit warning that **outcomes are not** methodological ground truth. (see origin: R1)
- **`README.md`:** One paragraph + link to `MAINTAINERS.md`.

### 4. Assistive automation (R3) — optional Phase 2

- **Default:** Do **not** add a script in the first implementation pass unless time budget allows—**manual grep** of `Promotion candidates` is acceptable.
- **If** added: `scripts/suggest_learnings.py` (stdlib only), argv = path to `run-log.md`, prints unchecked promotion lines and `failure_mode` tags to **stdout**; **never** writes files. Document in `MAINTAINERS.md`. (see origin: R3)

### 5. Privacy (R5)

- **`MAINTAINERS.md`:** Repo-committed bullets **must** be redacted; no network/analytics; logs may contain sensitive ideas—prefer local-only retention.

### Research insights

- Script is a **convenience** for maintainers who already review; it does not replace the ritual. If the script bit-rots, delete it—docs remain the source of truth.

## Technical Considerations

- **Architecture:** Markdown + optional stdlib Python; no new dependencies.
- **Performance:** N/A.
- **Security / privacy:** Script must perform **local file read only**; no network.

### Research insights

- Keep the optional script **under 50 lines** where possible so review is trivial and deletion is painless.

## System-Wide Impact

- **Interaction graph:** Optional one-line addition under **Run feedback** in `SKILL.md` for outcome signals—does not alter phase logic.
- **State lifecycle:** Git history + `last_reviewed` + dated bullets; retirements are explicit PRs.

## Acceptance Criteria

- [ ] **`MAINTAINERS.md`** exists at repo root with: monthly + merge/release ritual, **90-day** success check (from origin), redaction rules, “automation assists; humans promote,” and **Definition of verification** (see below). (see origin: R2, R3, R5)
- [ ] **`references/learnings.md`** includes YAML **`last_reviewed`** + convention for **Retired patterns** (see origin: R4)
- [ ] **`README.md`** links to `MAINTAINERS.md` and states **primary triggers** in one short paragraph
- [ ] **Optional (Phase 2):** `scripts/suggest_learnings.py` per constraints above, documented in `MAINTAINERS.md`
- [ ] **Optional:** One **`SKILL.md`** sentence on outcome lines in the run log

### Definition of verification (for `/ce:work`)

- [ ] A new reader can answer: **When** do I review? **Where** do I record `last_reviewed`? **What** must be redacted before commit?
- [ ] No new automated write path to `learnings.md` or `SKILL.md` exists in scripts or CI

## Success Metrics

- Align with origin: within **90 days**, **≥3** substantive promoted bullets **or** explicit documented decision to stay minimal; maintainer can **name** cadence and trigger. (see origin: Success criteria)

## Dependencies & Risks

| Risk | Mitigation |
|------|------------|
| Maintainer ignores ritual | Anchor to merge/release; keep MAINTAINERS.md to one screen |
| Script suggests wrong lines | Stdout-only; delete script if noisy |
| Scope creep into SaaS observability | Out of scope per origin |

## Implementation Phases

### Phase 1: Docs & learnings hygiene (required)

- Add `MAINTAINERS.md`; update `README.md`; add `last_reviewed` + retirement convention to `references/learnings.md`.

### Phase 2: Optional

- `SKILL.md` outcome line; `scripts/suggest_learnings.py` only if adopted.

### Research insights

- Ship Phase 1 before Phase 2—documentation delivers most of R2/R4 without code.

## SpecFlow / Edge Cases

- **Sensitive run (`MEGA_EVAL_LOG=off`):** Ritual can still update `last_reviewed` and retire stale repo bullets.
- **Quiet month:** Update `last_reviewed` with no content change, or add a one-line “Reviewed; nothing to promote.”
- **Forks:** `MAINTAINERS.md` applies to **this** repo; forks may ignore or adapt.

## Sources & References

- **Origin:** [docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md](../../brainstorms/2026-03-24-self-learning-sustainability-requirements.md) — R1–R5; human-in-the-loop; no auto-edit.
- **Internal:** [`SKILL.md`](../../SKILL.md), [`references/learnings.md`](../../references/learnings.md), [`README.md`](../../README.md)
- **External (process):** [Open Source Guides — Best practices for maintainers](https://opensource.guide/best-practices/)

## Research Notes

- **Deepen pass:** Added lightweight external process reference; no change to technical stack.
- Original **skipped external** research remains valid for dependencies; this pass only grounds **ritual design** in common OSS practice.
