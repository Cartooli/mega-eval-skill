---
date: 2026-03-24
topic: self-learning-sustainability
---

# Sustaining self-learning for mega-eval (and similar agent skills)

## Problem frame

**Who:** Maintainers and power users of the mega-eval pipeline (and analogous “methodology in Markdown” skills).

**What:** “Self-learning” here means the **evaluation methodology improves over time** from real runs—not model fine-tuning or silent prompt mutation. You already shipped **run logs** and **human-reviewed promotion** to `references/learnings.md`. The risk is **entropy**: logs pile up, `learnings.md` stays nearly empty, and the same failure modes repeat because **no habit or system** closes the loop.

**Why it matters:** Without sustained closure, “self-learning” is a one-time feature announcement, not a compounding asset.

## Requirements

- **R1. Signal breadth.** Self-learning must draw from **more than one signal type** where feasible: explicit corrections, tool failures/retries, thin-output flags, and (optionally) **outcome** signals—e.g. “user accepted deliverables” vs “abandoned mid-pipeline”—without treating outcomes as ground truth for methodology.
- **R2. Review ritual.** There must be a **defined cadence or trigger** for turning raw signals into decisions—e.g. time-boxed review (weekly/monthly), or “after N runs with unchecked promotion candidates,” or “before each skill release.” Picking one primary trigger is enough for v1.
- **R3. Assistive automation only.** Any tooling (scripts, CI, bots) may **suggest** promotions or surface patterns; it must **not** append to `references/learnings.md` or edit `SKILL.md` without **human or maintainer** explicit action.
- **R4. Staleness visibility.** Learned patterns should remain **auditable over time**—e.g. dates on bullets, or a short “last reviewed” note for the file—so outdated rules can be retired without guessing.
- **R5. Privacy and safety defaults.** Learning artifacts stay **workspace-local by default**; shared or repo-committed bullets stay **redacted** of subject-specific secrets; opt-in for any external aggregation.

## Success criteria

- Within **90 days** of adopting this frame: either **≥3** substantive bullets in `references/learnings.md` promoted from real runs, or an **explicit documented decision** that the skill stays minimal (with rationale).
- A maintainer can **name the review cadence/trigger** and **where** raw signals live (run log path, optional backlog).
- No incident of **unreviewed** auto-write to curated learnings or core skill instructions.

## Scope boundaries

- **Not in scope:** Fine-tuning or embedding models on user content; hosted product analytics from end-user installs; replacing human judgment on methodological changes.
- **Out of scope for this requirements doc:** Exact script language, CI vendor, or file layout—those belong in planning.

## Key decisions

- **“Self-learning” = human-in-the-loop methodology improvement**, aligned with existing promotion gates—not autonomous self-modification.
- **Compounding requires a ritual** (R2); technology alone (logging) is insufficient.
- **Automation is a librarian, not an author** (R3).

## Dependencies / assumptions

- **Assumption:** Primary “app” in question is the mega-eval skill repo; the same pattern applies to other Markdown-first agent skills with minor wording changes.
- **Dependency:** Continued use of optional `run-log.md` (or equivalent) when users want traceability.

## Alternatives considered

| Direction | Pros | Cons | When to use |
|-----------|------|------|-------------|
| **Logs only, no ritual** | Zero process | Entropy; learnings stay empty | Too weak for “sustained” learning |
| **Full observability SaaS** | Rich traces | Cost, privacy, overkill for a skill | If you later productize a host app |
| **Monthly “learnings review” + optional suggest script** | Simple, matches R2–R3 | Needs calendar discipline | **Recommended baseline** |

## Outstanding questions

### Resolve before planning

- *(none — product scope is bounded enough to plan concrete habits/tooling.)*

### Deferred to planning

- **[Needs research]** Which single **primary trigger** (calendar vs run-count vs release gate) fits maintainer workflow best?
- **[Technical]** Whether a **small script** (diff-based promotion hints) justifies its maintenance cost in this repo.
- **[Technical]** Whether to add a **CHANGELOG** entry style for learnings or only per-bullet dates.

## Next steps

→ **`/ce:plan`** when you want an implementation plan (e.g. review ritual doc, optional script, learnings file hygiene).

If you prefer to **decide the review trigger first** in chat, say so and we can update this doc’s R2 before planning.
