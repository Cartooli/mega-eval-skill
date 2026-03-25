---
name: mega-eval-deliverables
description: "Phase 4 only: assemble mega-eval Word deliverables (01–05 and 00 executive summary .docx) from existing markdown phases. Use for 'mega eval docx only', 'generate eval Word docs', when raw markdown already exists. Requires docx skill and all source files."
---

# Mega-eval — Phase 4: Deliverable assembly only

You are running **only Phase 4** of the mega-eval pipeline: compile **polished `.docx`** files using the **docx** skill. Do **not** re-run earlier phases unless the user asks.

**Prerequisite skill:** **docx** (read its `SKILL.md` for formatting).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 4), **Pre–Phase 4 review** and **Phase 4: Deliverable Assembly** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Required source files (fail closed)

Before generating any `.docx`, confirm these exist in the workspace (or ask the user to provide paths). If any are **missing**, **stop** and list them — do not fabricate phase content.

| Deliverable | Source markdown |
|-------------|-----------------|
| `01-hater-mode-feedback.docx` | `phase1a-hater-raw.md` |
| `02-competitive-landscape.docx` | `phase1b-competitive-raw.md` |
| `03-strengths-opportunities.docx` | `phase1c-strengths-raw.md` |
| `04-critical-fixes-and-design.docx` | `phase2-synthesis.md` |
| `05-content-strategy-outline.docx` | `phase3-content-outline-raw.md` |
| `00-executive-summary.docx` | **Written last** — synthesizes from the five documents above |

If logging is enabled: perform the **pre–Phase 4 review** in full `SKILL.md` (reconcile `run-log.md` with brief/synthesis/raw files).

## Assembly order

Generate **01 → 05** first; **`00-executive-summary.docx` last** (draws from all others).

Append `phase_start phase4` / `phase_complete phase4` to the run log when logging. Output paths and presentation: follow **File Output** in full `SKILL.md`.

## Host limitations

If **docx** or required tools are unavailable, state that limitation and offer markdown-only export or manual steps — see main `SKILL.md` error handling.
