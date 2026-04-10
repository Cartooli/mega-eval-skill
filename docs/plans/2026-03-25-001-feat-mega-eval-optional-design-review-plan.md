---
title: "feat: Optional live-site design audit in mega-eval (design-review alignment)"
type: feat
status: active
date: 2026-03-25
---

# feat: Optional live-site design audit in mega-eval (design-review alignment)

## Overview

Answer the product question: **should mega-eval invoke something like `/design-review` when inputs include a scrapable product URL**, so evaluations surface **visual / UX / “AI slop”** feedback alongside business, competitive, and narrative analysis?

**Recommendation:** **Yes — add an optional, conditional branch**, but **not** the full gstack `/design-review` fix-and-commit loop inside mega-eval. Treat design as a **report-only audit** (or a dedicated subagent producing structured markdown), wired into Phase 1 (parallel) and Phase 2 synthesis when a **live site URL** is present and reachable.

**Related work (not the origin of this plan):** Sub-skills packaging and phase I/O are defined in [docs/plans/2026-03-24-004-feat-mega-eval-sub-skills-plan.md](2026-03-24-004-feat-mega-eval-sub-skills-plan.md) and [docs/brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md](../brainstorms/2026-03-24-mega-eval-sub-skills-requirements.md). Extending the pipeline with a design track is a **methodology addition**; if implemented, thin-skill packaging should gain a matching slice (e.g. `mega-eval-design`) and checklist rows — consistent with that plan’s “single source of truth in `references/`” rule.

## Problem Statement / Motivation

Today, Phase 0 ingests URLs via fetch-style extraction into the brief; Phase 1 is **text-first** (hater, competitive, strengths). Phase 2’s **“Design Inconsistencies”** section is inferred from those narratives, not from a **systematic visual audit** of the rendered experience.

For many products, the **marketing site or app shell** is primary evidence. Users asking for a “full picture” reasonably expect **design and credibility signals** (hierarchy, typography, interaction states, generic-template tells) to sit next to **business model and market** findings — without running a separate skill manually.

## Proposed Solution

### 1. Define a “Design Audit” track (report-only)

- **Trigger:** At Phase 0, classify inputs: if there is at least one **HTTP(S) URL** intended as the **product or marketing surface** (not a PDF host or docs-only link), set `design_audit: optional|required|skipped` (default **optional**; **skipped** if URL missing, paywall, or user opts out via prompt / env).
- **Execution:** Run **in parallel with Phase 1A–1C** as **Phase 1D** (or merge into “Phase 1 with four tracks” — naming is an implementation detail).
- **Output:** `phase1d-design-raw.md` with a **fixed template** aligned to the **evaluation** subset of `/design-review`:
  - First impression / hierarchy (marketing vs app UI classifier)
  - Typography, color/contrast (heuristic), spacing, responsive notes
  - Interaction states (what can be observed without deep auth)
  - **AI slop** checklist (the blacklist from design-review)
  - **Quick wins** (3–5 items, each actionable)
  - **Evidence:** screenshot paths or embedded links if the host supports them; if not, state “visual evidence not captured” explicitly.

### 2. Do **not** bundle the full `/design-review` remediation loop

The attached **design-review** workflow includes **clean git tree**, **browse binary setup**, **per-finding commits**, and **re-audit** — appropriate for **your repo’s frontend**, not for **evaluating someone else’s live product** inside mega-eval.

- **In mega-eval:** stop at **audit + recommendations**.
- **Optional follow-up** for the user: “Run `/design-review` on your own codebase if you have local source.”

### 3. Phase 2 synthesis changes

- Extend instructions so synthesis **must read** `phase1d-design-raw.md` when present.
- Map design findings into:
  - **Critical fixes** (e.g. trust-breaking UX, accessibility blockers)
  - **Design inconsistencies** (merge visual audit with messaging contradictions from 1A/1C)
  - **Quick wins** (dedupe against Phase 1D list)
- When Phase 1D is **skipped**, keep current behavior.

### 4. Phase 4 / executive summary

- Pull top design headline (e.g. design score band or “high/medium/low concern”) into **`04-critical-fixes-and-design.docx`** and **`00-executive-summary.docx`** when Phase 1D exists.

### 5. Thin skill / packaging (if sub-skills exist)

- Add **`mega-eval-design`** (or equivalent name) that only runs Phase 1D + pointers to `references/`, per [004 plan](2026-03-24-004-feat-mega-eval-sub-skills-plan.md) patterns.
- Update [references/pipeline-checklist.md](../references/pipeline-checklist.md) and [skills/README.md](../skills/README.md) artifact tables.

## Technical Considerations

- **Tooling variance:** Full parity with gstack `browse` may be unavailable in some hosts. Mitigations:
  - **Tier A:** Native browse/screenshot + structured checklist (best fidelity).
  - **Tier B:** WebFetch/HTML + limited inference (weaker for layout/motion; disclose limits).
  - **Tier C:** Skip Phase 1D with a logged reason (`browse_unavailable`, `auth_wall`, etc.).
- **Auth and SPAs:** Login-gated or client-only apps may yield **thin audits**; Phase 0 should record “authenticated flows not exercised.”
- **Cost and latency:** A fourth parallel track increases wall time slightly but preserves parallelism; cap pages audited (e.g. homepage + 2 key paths) unless user requests deep mode.
- **Overlap with Hater Mode:** Some personas may comment on “looks cheap”; Phase 2 should **dedupe** and treat Phase 1D as the **authoritative visual** source when both exist.

## System-Wide Impact

- **Interaction graph:** Phase 0 → (optional) Phase 1D alongside 1A–1C → Phase 2 reads four inputs when design runs.
- **Error propagation:** Design failures must not block business tracks; record partial output and continue (same spirit as existing subagent timeout handling in mega-eval).
- **State lifecycle:** New artifact `phase1d-design-raw.md`; Phase 4 pre-flight for thin `mega-eval-deliverables` must treat it as **optional** unless a stricter mode is chosen later.
- **API surface parity:** Full `mega-eval` and thin slices document the same filenames.

## Acceptance Criteria

- [ ] **Decision documented** in root `SKILL.md`: design is **report-only** inside mega-eval; full `/design-review` is an optional follow-up for local codebases.
- [ ] **Conditional trigger** documented: when URL present + reachable; explicit skip reasons when not.
- [ ] **`phase1d-design-raw.md`** template exists under `references/` (e.g. `references/design-audit-template.md`) — **single source of truth**, no long duplicate blocks in thin skills.
- [ ] **Phase 2** instructions updated to ingest Phase 1D when file exists.
- [ ] **Pipeline checklist** updated with Phase 1D rows and Phase 2/4 notes.
- [ ] **Sub-skills:** If repo ships thin skills, add `mega-eval-design` (or defer with explicit “not yet implemented” in README — pick one in implementation).

## Success Metrics

- Evaluations with a product URL routinely include a **scannable design section** grounded in observed UI, not only business criticism.
- Maintainers can change the design audit template **once** in `references/` without editing multiple full skills.

## Dependencies & Risks

- **Dependency:** Browser or screenshot capability for high-quality audits; otherwise honest degradation.
- **Risk:** Users confuse mega-eval design output with a **WCAG compliance audit** — mitigate with disclaimer: heuristic / qualitative, not legal certification.
- **Risk:** **Token bloat** from screenshots — prefer file paths + short captions in markdown, not huge base64 in chat.

## Research & Decision Record (ce-plan)

- **Local research:** Repo `SKILL.md` and [references/pipeline-checklist.md](../references/pipeline-checklist.md) define Phases 0–4 and Phase 2 “design inconsistencies” without live UI audit. Sub-skills plan defines artifact contracts through Phase 4 only.
- **External research:** Skipped — decision is packaging and workflow design; no external API/security unknowns.
- **SpecFlow-style gaps addressed:** Auth walls, SPAs, missing browse, dedupe with 1A, optional deliverable dependency, executive summary inclusion.

## Sources & References

- Mega-eval pipeline: [SKILL.md](../SKILL.md)
- Checklist: [references/pipeline-checklist.md](../references/pipeline-checklist.md)
- Sub-skills plan: [2026-03-24-004-feat-mega-eval-sub-skills-plan.md](2026-03-24-004-feat-mega-eval-sub-skills-plan.md)
- gstack `/design-review` (user-attached): full loop vs **rendered-site audit** — adopt audit checklist; exclude fix/commits/re-audit from mega-eval scope.
