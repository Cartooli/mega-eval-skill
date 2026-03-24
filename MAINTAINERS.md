# Maintainers: sustaining the self-learning loop

Mega-eval’s “self-learning” is **human-in-the-loop**: run logs and promotion candidates feed **reviewed** updates to `references/learnings.md`. Nothing here auto-edits `SKILL.md` or prompts.

## Review triggers (pick what you’ll actually do)

1. **Monthly (calendar):** At least once a month, open recent `run-log.md` files (or your workspace log), find **Promotion candidates**, and decide: promote to `references/learnings.md`, drop, or defer. Update **`last_reviewed`** in `references/learnings.md` even if you promote nothing—honest staleness beats fake freshness.
2. **Merge / release gate:** On each merge to the default branch that touches `SKILL.md`, `references/`, or `examples/`, or when you tag a release—spend **≤5 minutes**: skim promotion candidates; update `last_reviewed` if you performed a review.
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

## See also

- [`references/learnings.md`](references/learnings.md) — promotion gates  
- [`docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md`](docs/brainstorms/2026-03-24-self-learning-sustainability-requirements.md) — original requirements  
