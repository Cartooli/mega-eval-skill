# Runtime Contract

This document defines the runtime assumptions for mega-eval.

The goal is not to pretend the skill is host-agnostic. The goal is to make host coupling explicit so maintainers can reason about portability, degradation paths, and documentation drift.

## Contract summary

Mega-eval is designed for **Claude Code** first. Other hosts may be able to run parts of the workflow, but they should be treated as partial implementations unless they satisfy the capability contract below.

## Capability classes

### Required capabilities

These are required for the full markdown pipeline to run as designed.

- **Local file read/write**
  - Needed for `eval-brief.md`, phase raw outputs, optional `run-log.md`, and final artifacts.
- **Subagent execution**
  - Needed for Phase 1 parallel analysis and Phase 3 content-outline generation.
- **Skill-readable repo files**
  - The runtime must be able to read `SKILL.md`, `references/`, and sibling skill files.
- **Markdown artifact generation**
  - Every phase depends on emitting markdown outputs to stable file paths.

If any required capability is missing, mega-eval should be treated as a manual or partial workflow, not a fully supported runtime.

### Recommended capabilities

These materially improve output quality and completeness, but the core markdown pipeline can still proceed without them.

- **WebFetch or equivalent URL retrieval**
  - Used in Phase 0 for product pages and supporting URLs.
- **WebSearch or equivalent live search**
  - Used in Phase 1B to ground competitor and market analysis.
- **External built-in skills**
  - `hater-mode`
  - `long-form-outline`
  - `docx`

Without these, mega-eval can still run partially, but quality or deliverable completeness drops.

### Optional capabilities

These unlock higher-quality or more polished outputs but are not required.

- **Browser or screenshot tooling**
  - Used by Phase 1D Tier A live-site audits.
- **Local extraction tools**
  - `pdftotext` for PDFs
  - `pandoc` for `.docx` / `.pptx`
- **Plugin marketplace support**
  - Helpful for installation and updates, not required for execution.

## Fallback rules

When a capability is missing, the pipeline should degrade in a predictable way rather than silently pretending nothing changed.

### No subagents

- Run phases sequentially instead of in parallel.
- Preserve the same artifact names and output contracts.
- Expect slower runtime and weaker separation between tracks.

### No WebFetch

- Phase 0 should rely on pasted text or uploaded documents.
- URL-derived claims should be treated as unavailable rather than inferred.

### No WebSearch

- Phase 1B should still produce the required headings.
- The output should explicitly state that competitive and market confidence is limited.
- The pipeline should prefer honesty over speculation.

### No browser tooling

- Phase 1D should use Tier B (`WebFetch` / HTML-visible evidence only) when possible.
- If the URL is unusable, emit the Tier C stub and proceed without blocking synthesis.

### No `docx` skill

- The markdown phases can still run and be validated.
- Phase 4 becomes partial: stop at validated markdown artifacts or document that `.docx` output is unavailable.

### No `hater-mode` or `long-form-outline` skill

- The host may still attempt a reduced-quality run using built-in prompt templates, but this is not the preferred path.
- Maintainers should treat this as degraded output quality, not equivalent behavior.

## Non-goals

- Mega-eval does **not** provide a provider-neutral LLM runtime abstraction.
- Mega-eval does **not** guarantee equivalent behavior across Claude Code, Cursor, Codex, or generic chat interfaces.
- Mega-eval does **not** promise browser-based design audit fidelity when only HTML retrieval is available.

## Maintainer rule

If you change host assumptions, capability requirements, or fallback behavior in `SKILL.md`, `README.md`, or `references/`, update this file in the same change.
