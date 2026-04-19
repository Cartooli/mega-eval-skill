---
last_reviewed: 2026-03-24
---

# Mega-eval learned patterns (promoted from run feedback)

This file holds **methodological** lessons promoted from `run-log` artifacts after human review. It is **not** model training data and **does not** auto-update the skill.

Update YAML **`last_reviewed`** above whenever you complete a review pass (even if you add zero new bullets).

## Do not promote without review

- Never append here directly from a single run without checking [Promotion gates](#promotion-gates).
- **Redact** company names, URLs, API keys, and user-identifying details from examples. Keep the lesson, drop the subject.
- If a bullet duplicates an existing one, merge or extend the existing entry instead of adding a duplicate.

## Promotion gates

A pattern is ready to promote when:

- [ ] It is **methodological** (prompts, checklist, skill wording)—not one-off subject trivia.
- [ ] It was **verified** by a second run with the improved wording, or a maintainer explicitly accepts a rare edge case.
- [ ] It does **not** duplicate an existing bullet (or you merged into an existing bullet).
- [ ] Optional: a **redacted** one-line example clarifies the pattern.

## How entries are formatted

Each entry is a short **imperative** rule the orchestrator or subagent prompts should follow. Date is optional.

---

## Patterns

<!-- Entries below are promoted from real or illustrative run feedback after human review. -->
<!-- The first entry is a seed/example to demonstrate format. Replace with real promotions as they land. -->

- **2026-03-24 (example):** When web search returns thin data for Phase 1B, state confidence explicitly and avoid inventing market statistics; say "limited public data" instead of padding.

*This file grows as real runs surface and validate improvements. Initial methodology comes from [SKILL.md](../SKILL.md) and [subagent-prompts.md](subagent-prompts.md). First real promotion is expected after substantive pilot runs; see promotion gates above.*

---

## Retired patterns

*Move superseded bullets here with a one-line reason, or delete in a PR with a short rationale.*

- (none)

---

## Deferred / candidates

*Use this subsection during review to park candidates that are not yet promoted.*

- (none)
