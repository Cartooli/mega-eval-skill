---
title: GitHub issue templates and Phase 4 feedback wrap-up
type: feat
status: completed
date: 2026-03-24
origin: docs/brainstorms/2026-03-24-mega-eval-user-feedback-github-requirements.md
---

# GitHub issue templates and Phase 4 feedback wrap-up

## Overview

Add three GitHub issue templates (bug/error, improvement, feature request) with a consistent label taxonomy, a short **Phase 4** optional wrap-up in `SKILL.md` with canonical links and `run_id` + redaction guidance, and cross-links in `README.md`, `MAINTAINERS.md`, and `references/pipeline-checklist.md`. (see origin: `docs/brainstorms/2026-03-24-mega-eval-user-feedback-github-requirements.md`)

## Problem Statement / Motivation

Runners and maintainers need a searchable, low-friction path to report skill issues and ideas without mixing intents. The origin doc separates this from **run-log** methodology feedback while sharing **`run_id`** for correlation.

## Proposed Solution

1. **`.github/ISSUE_TEMPLATE/`** — Three Markdown templates with YAML frontmatter (`name`, `about`, `title` prefix, `labels`). Use filenames `bug-report.md`, `improvement.md`, `feature-request.md` so `?template=` URLs are stable.
2. **`config.yml`** — `blank_issues_enabled: true` so advanced users can still file untemplated issues.
3. **`SKILL.md`** — New subsection under **Phase 4** (after deliverable assembly / file output, before efficiency notes): optional maintainer-feedback block with three `issues/new?template=...` links to **https://github.com/Cartooli/mega-eval-skill**, placeholder `<run_id>`, redaction reminder.
4. **Docs** — README: short “Reporting issues” hub. MAINTAINERS: one-time label setup note + triage pointer. Pipeline checklist: optional checkbox for the wrap-up.

## Technical Considerations

- **Canonical repo:** `origin` is `https://github.com/Cartooli/mega-eval-skill.git`; embed that owner/repo in `SKILL.md` and docs. Forks override per R4 (origin).
- **Labels:** Templates reference `bug`, `improvement`, `feature-request`. Document that maintainers should create these in GitHub **Settings → Labels** if missing (GitHub may not auto-create on all orgs).
- **No network from skill:** Links are passive URLs only; aligns with existing privacy stance in `MAINTAINERS.md`.

## System-Wide Impact

- Markdown-only skill behavior: no runtime code paths.
- Issue volume may increase slightly; triage is label/template-based.

## Acceptance Criteria

- [ ] Three issue templates exist under `.github/ISSUE_TEMPLATE/` with distinct intent and default labels.
- [ ] `config.yml` present with sensible defaults.
- [ ] `SKILL.md` Phase 4 includes optional wrap-up with three template links, `run_id` mention, redaction reminder.
- [ ] `references/pipeline-checklist.md` Phase 4 includes optional checkbox for offering feedback links.
- [ ] `README.md` links to Issues / reporting hub.
- [ ] `MAINTAINERS.md` documents label setup and relationship to run-log vs GitHub issues.

## Success Metrics

- New reporters can find template choice from README or Phase 4 wrap-up in under a minute (manual smoke check).

## Dependencies & Risks

- **Risk:** Labels missing → issues still created; labels may not auto-apply until created. **Mitigation:** MAINTAINERS note.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-03-24-mega-eval-user-feedback-github-requirements.md](../brainstorms/2026-03-24-mega-eval-user-feedback-github-requirements.md) — R1–R4, canonical URL decision, Phase 4 wrap-up.

## Implementation Units

### Unit 1: Issue templates + config

- **Files:** `.github/ISSUE_TEMPLATE/config.yml`, `bug-report.md`, `improvement.md`, `feature-request.md`
- **Verification:** Filenames match `?template=` URLs; frontmatter validates on GitHub.

### Unit 2: SKILL + checklist

- **Files:** `SKILL.md`, `references/pipeline-checklist.md`
- **Verification:** Phase 4 section reads clearly; checklist aligns.

### Unit 3: README + MAINTAINERS

- **Files:** `README.md`, `MAINTAINERS.md`
- **Verification:** Reporting path discoverable; maintainer label note present.

---

Plan written to `docs/plans/2026-03-24-003-feat-github-user-feedback-templates-plan.md`.
