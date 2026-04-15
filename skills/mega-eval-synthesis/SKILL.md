---
name: mega-eval-synthesis
description: "Phase 2 only: synthesize phase1a/1b/1c raw outputs into phase2-synthesis.md (critical fixes, design issues, next steps); merges phase1d-design-raw.md when present. Use when Phase 1 is done and you want 'mega eval synthesis only', 'merge critique competitive strengths', or judgment-heavy synthesis without Phase 3–4."
---

# Mega-eval — Phase 2: Synthesis only

You are running **only Phase 2** of the mega-eval pipeline: read Phase **1A–1C** raw files and produce **one** synthesis document. **If `phase1d-design-raw.md` exists**, read it and merge per full `SKILL.md` Phase 2 (Phase 1D is authoritative for rendered-site UX). Do **not** use a subagent — this phase requires cross-track judgment (per main `SKILL.md`).

## Shared methodology location

Resolve `references/` per [skills/README.md](../README.md). **Read:** `references/pipeline-checklist.md` (Phase 2).

Full section structure: **Phase 2: Synthesis** in full `SKILL.md` (`../../SKILL.md` or `../mega-eval/SKILL.md`).

## Inputs and outputs

| | |
|--|--|
| **Reads** | `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, `phase1c-strengths-raw.md`; **optional** `phase1d-design-raw.md` |
| **Writes** | `phase2-synthesis.md` |

If any **required** Phase 1 file (1A/1B/1C) is missing, **stop** and list what is missing — do not invent prior phases. **Absence of `phase1d-design-raw.md` is OK** (design audit skipped or not yet run).

If logging is enabled, append `phase_start phase2` / `phase_complete phase2` per full `SKILL.md`.

## Next steps

Run **`mega-eval-content-outline`** then **`mega-eval-deliverables`**, or **`mega-eval`** for the remainder of the pipeline.
