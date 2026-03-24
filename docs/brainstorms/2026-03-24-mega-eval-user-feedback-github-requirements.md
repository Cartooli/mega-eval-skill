---
date: 2026-03-24
topic: mega-eval-user-feedback-github
---

# User feedback via GitHub Issues (mega-eval)

## Problem frame

**Who:** People running the mega-eval skill and maintainers of this repo.

**What:** Runners need a **clear, low-friction** way to report **errors**, suggest **improvements**, and **request features** about the skill itself—distinct from **run-log** feedback (operational signals for methodology promotion) and without mixing those three intents in one undifferentiated stream.

**Why it matters:** Issues and ideas that stay in chat or private notes are lost; triage and search depend on **consistent labels/templates** and **correlation** with the run when something went wrong.

## Requirements

- **R1. Three issue entry points.** The GitHub repo must expose **three** issue templates (or equivalent) so reporters choose **bug / error**, **improvement** (non-bug quality or process), or **feature request**—each with a short description and fields that match the intent.
- **R2. Searchable taxonomy.** Each template is associated with **labels** (or template metadata) so maintainers and users can filter Issues by type without relying on title wording alone.
- **R3. Phase 4 wrap-up block.** Near **Phase 4 / end of run**, the skill instructions include a **short optional** block: “Something wrong or have an idea?” with **links to all three** templates, the **same `run_id`** used for that run, and a **redaction reminder** (no secrets, minimal subject-identifying detail in the issue body).
- **R4. Canonical reporting URLs.** The wrap-up uses **clickable links** to the **canonical public** mega-eval GitHub repo’s Issues/templates. **Forks:** maintainers who want a different tracker document that they **edit the wrap-up section** (or a small documented pointer) in their copy—no requirement for a second “config” layer in v1.

## Success criteria

- A new reporter can find **which template to use** in under a minute from the repo (or from the Phase 4 wrap-up).
- Issues can be filtered by **type** (bug vs improvement vs feature) using GitHub’s UI.
- When a bug reports a failed run, **run_id** or equivalent context is **often** present because the wrap-up prompts for it.

## Scope boundaries

- **Not in scope:** GitHub Discussions, hosted forms, email-only workflows, or auto-filing issues from the agent.
- **Not in scope:** Changing how **run-log.md** works or promotion to `references/learnings.md`—those stay separate; this doc only **coordinates** via shared **run_id** and redaction norms.
- **Out of scope for this requirements doc:** Exact `.github/ISSUE_TEMPLATE` filenames, YAML, label names, and CI—**planning** / implementation.

## Key decisions

- **Single home:** GitHub Issues in **one** repo with **three** templates + labels (R1–R2).
- **Structured wrap-up** at Phase 4 with links, **run_id**, redaction reminder (R3).
- **Canonical URLs in SKILL** for the simplest one-click experience; forks override locally if needed (R4).

## Dependencies / assumptions

- The repo has a **stable public GitHub** location for issue links and templates.
- Maintainers accept **occasional** URL updates when the repo moves or is renamed.

## Outstanding questions

### Resolve before planning

- [ ] None identified from this brainstorm.

### Deferred to planning

- [R1][Technical] Exact template copy, required fields (e.g. environment, skill version), and default labels.
- [R3][Technical] Precise placement in `SKILL.md` / `references/pipeline-checklist.md` so Phase 4 instructions stay consistent.
- [R4][Needs research] Whether the README should duplicate **one** “reporting hub” link for users who never open Phase 4.

## Next steps

→ `/ce:plan` for structured implementation planning (add `.github/` templates, update `SKILL.md` wrap-up, and cross-links in `README.md` / `MAINTAINERS.md` as needed).
