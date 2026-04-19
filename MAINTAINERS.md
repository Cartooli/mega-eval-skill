# Maintainers: sustaining the self-learning loop

> **For maintainers and contributors only.** End users should start with [README.md](README.md).

Mega-eval’s “self-learning” is **human-in-the-loop**: run logs and promotion candidates feed **reviewed** updates to `references/learnings.md`. Nothing here auto-edits `SKILL.md` or prompts.

## Planning a change

Use the repo’s [Change Planning Guide](docs/guides/change-planning.md) before starting work on a non-trivial change.

Short version:

- **Lightweight** changes (docs wording, broken links, narrow one-file fixes) usually go straight to work.
- **Standard** changes (bounded packaging, docs parity, CI adjustments) usually get a short direct plan, then work.
- **Deep** changes (new pipeline capabilities, cross-cutting behavior changes, deliverable reshaping) should usually go through brainstorm → plan → work.

When in doubt, choose the smallest amount of process that still makes scope, research needs, and PR boundaries obvious.

## Review triggers (pick what you’ll actually do)

1. **Monthly (calendar):** At least once a month, open recent `run-log.md` files (or your workspace log), find **Promotion candidates**, and decide: promote to `references/learnings.md`, drop, or defer. Update **`last_reviewed`** in `references/learnings.md` even if you promote nothing—honest staleness beats fake freshness.
2. **Merge / release gate:** On each merge to the default branch that touches `SKILL.md`, `references/`, `skills/`, or `examples/`, or when you tag a release—spend **≤5 minutes**: skim promotion candidates; update `last_reviewed` if you performed a review.

**Thin phase skills** (`skills/*/SKILL.md`) should stay **short** — they point at `references/` and the root `SKILL.md`; do not duplicate long prompt text there. If you change phase behavior, update `references/` and root `SKILL.md` first, then adjust thin skills only for I/O or path-resolution wording.
3. **Optional priority bump:** If **≥3** unchecked promotion candidates pile up in the active log, do a review before the next merge.

## Signal types (what belongs in run logs when logging is on)

Use the taxonomy in `SKILL.md` (`tool_error`, `user_correction`, `retry`, `failure_mode`, etc.). Useful types include:

- **Explicit:** user asked to rewrite a section or fix facts (`user_correction`).
- **Operational:** tool failure, retry, thin output (`tool_error`, `retry`, `quality_gate_fail`).
- **Optional outcome (forensics only):** `outcome_complete` / `outcome_abandoned`—**not** proof of methodology quality; optional one-liner in `SKILL.md`.

## Redaction and privacy

- Repo-committed bullets in `references/learnings.md` must be **redacted** (no secrets, minimal subject-identifying detail).
- Run logs may contain sensitive ideas—keep logs **local** unless you intend to share; never add analytics or network calls from this workflow.

## Assistive tooling (humans promote)

- **`scripts/suggest_learnings.py`** reads a `run-log.md` path and prints **Promotion candidates** and **Failure modes** lines to stdout. It **never** writes files. If it’s noisy or unused, delete it—docs stay authoritative.
- Usage: `python3 scripts/suggest_learnings.py path/to/run-log.md`

## 90-day success check (from project requirements)

Within ~90 days of adopting this process, either:

- **≥3** substantive bullets promoted into **Patterns** in `references/learnings.md` from real runs, **or**
- An **explicit** note in a PR or `references/learnings.md` that the file is intentionally minimal and why.

## Definition of verification

A change set implementing this maintainer story should satisfy:

- [ ] A new reader knows **when** to review, **where** `last_reviewed` lives, and **what** to redact before commit.
- [ ] No script or CI **writes** to `references/learnings.md` or `SKILL.md` without a human edit.

## GitHub Issues (skill bugs, improvements, features)

**Run logs** capture operational signals for **promotion** into `references/learnings.md`. **GitHub Issues** are for **actionable** reports about the skill itself (bugs, doc/process improvements, feature ideas). They can share the same **`run_id`** for correlation; redact before posting.

- **Templates:** [Bug](https://github.com/Cartooli/mega-eval-skill/issues/new?template=bug-report.md)
  · [Improvement](https://github.com/Cartooli/mega-eval-skill/issues/new?template=improvement.md)
  · [Feature](https://github.com/Cartooli/mega-eval-skill/issues/new?template=feature-request.md)
- **Labels:** Ensure **`bug`**, **`improvement`**, and **`feature-request`** exist under **Settings → Labels** so template defaults apply. Create them once if missing.

## Plugin marketplace releases

This repo ships a Claude Code plugin marketplace at `.claude-plugin/marketplace.json`. The plugin version lives in **two files** that must stay in sync:

- `.claude-plugin/marketplace.json` — `plugins[].version` field
- `plugins/mega-eval/.claude-plugin/plugin.json` — `version` field

**Rule:** If you change any skill content (root `SKILL.md`, `references/`, thin skills) in a way you want **existing plugin users to receive**, bump both version fields before tagging. Claude Code uses the version to decide whether to update a cached plugin — if the version does not change, cached installs will not see your changes.

Use [semver](https://semver.org/): `MAJOR.MINOR.PATCH`.
- `PATCH` — bug fixes, wording corrections, learnings additions.
- `MINOR` — new phase skills, new prompt capabilities, non-breaking methodology changes.
- `MAJOR` — breaking changes to inputs/outputs, pipeline restructure.

**Release checklist (every tag):**

1. Bump `version` in `.claude-plugin/marketplace.json` and `plugins/mega-eval/.claude-plugin/plugin.json`.
2. Confirm all symlinks in `plugins/mega-eval/` still resolve: `find plugins/mega-eval -type l | while read l; do [ -e "$l" ] || echo "BROKEN: $l"; done`.
3. Validate JSON: `python3 -m json.tool .claude-plugin/marketplace.json && python3 -m json.tool plugins/mega-eval/.claude-plugin/plugin.json`.
4. Run the monthly/merge-gate learnings review above if skipped.
5. Tag: `git tag vX.Y.Z && git push --tags`.

**Marketplace name:** `cartooli` — not in Anthropic's reserved list; kebab-case; do not change without updating README.

## See also

- [`references/learnings.md`](references/learnings.md) — promotion gates  
- [`docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md`](docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md) — original requirements  
- [`docs/plans/2026-03-24-005-feat-claude-plugin-marketplace-packaging-plan.md`](docs/plans/2026-03-24-005-feat-claude-plugin-marketplace-packaging-plan.md) — plugin packaging plan  
