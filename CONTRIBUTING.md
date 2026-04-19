# Contributing to mega-eval-skill

Thanks for your interest in contributing. This document covers where to find things and how to submit changes.

## For end users

If you just want to use the pipeline, start with **[README.md](README.md)** and **[SKILL.md](SKILL.md)**. You don't need to read anything else.

To report a bug, request a feature, or suggest an improvement:

- **[Bug report](https://github.com/Cartooli/mega-eval-skill/issues/new?template=bug-report.md)** — something broken or behaving unexpectedly
- **[Improvement](https://github.com/Cartooli/mega-eval-skill/issues/new?template=improvement.md)** — existing behaviour that could work better
- **[Feature request](https://github.com/Cartooli/mega-eval-skill/issues/new?template=feature-request.md)** — a new capability or phase

Include the **`run_id`** from your run log when relevant (see `SKILL.md` Phase 4 → Maintainer feedback). Redact any sensitive subject matter before posting.

## For contributors

### Repository layout

| Path | Audience | Purpose |
|------|----------|---------|
| `README.md`, `SKILL.md` | Everyone | User-facing docs and full pipeline instructions |
| `references/` | Everyone | Shared prompt templates, output templates, model guidance |
| `skills/` | Everyone | Thin phase-only skill entrypoints |
| `scripts/` | Everyone | Helper utilities |
| `examples/` | Everyone | Sample runs and fictional run-log examples |
| `MAINTAINERS.md` | Maintainers | Review ritual, plugin release checklist, redaction rules |
| `docs/guides/` | Maintainers | Change-planning rubric and internal process guides |
| `docs/plans/` | Maintainers | Historical implementation plans |
| `docs/brainstorms/` | Maintainers | Requirements and brainstorm artifacts |

As an external contributor, you will typically only need to touch `README.md`, `SKILL.md`, `references/`, `skills/`, or `scripts/`.

### How to contribute

1. **Open an issue first** for anything non-trivial — it avoids duplicate effort and lets maintainers flag scope concerns before you write code.
2. **Fork the repo** and create a branch from `master`.
3. Make your changes. Keep pull requests focused — one logical change per PR.
4. **Submit a pull request** using the PR template. Fill in the summary, non-breaking confirmation, and test plan sections.

### Change sizing

Follow the rubric in [`docs/guides/change-planning.md`](docs/guides/change-planning.md):

- **Lightweight** (docs wording, broken links, narrow one-file fixes) — go straight to a PR.
- **Standard** (bounded new behaviour, CI adjustments) — short plan in the issue, then PR.
- **Deep** (new pipeline phases, cross-cutting behaviour changes, deliverable restructure) — brainstorm → plan → PR.

### Thin phase skills

Skills under `skills/*/SKILL.md` should stay short — they point at `references/` and the root `SKILL.md`. Don't duplicate prompt logic there. If you change phase behaviour, update `references/` and root `SKILL.md` first; only adjust thin skills for input/output or path-resolution wording.

### Plugin version sync

If your change affects skill content (root `SKILL.md`, `references/`, thin skills) and you want plugin users to receive the update, bump the `version` field in **both**:
- `.claude-plugin/marketplace.json`
- `plugins/mega-eval/.claude-plugin/plugin.json`

These must stay in sync. See `MAINTAINERS.md` for the full release checklist.

### Learnings promotions

`references/learnings.md` holds curated methodology patterns promoted from run logs after human review. See the promotion gates in that file before adding or editing entries. Do not add entries from a single run without a second-run verification.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you agree to abide by its terms.
