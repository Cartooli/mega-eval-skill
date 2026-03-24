---
name: mega-eval
description: "Run a comprehensive, multi-phase evaluation of any idea, product, or feature set — producing multiple deliverable files covering critical feedback, competitive context, strengths & opportunities, design issues, proposed fixes, and a content strategy outline. Accepts any combination of raw text, uploaded documents, or crawlable URLs as input. Orchestrates parallel subagents for efficiency. Use this skill whenever someone says 'evaluate this idea', 'tear down this product', 'full analysis of', 'mega eval', 'comprehensive review', 'deep evaluation', 'assess this feature set', 'product review pipeline', or any request for a thorough multi-dimensional analysis of a concept, product, or feature. Also trigger when the user provides a URL, doc, or text block and asks for a complete picture — strengths, weaknesses, market context, and next steps."
---

# Mega Eval — Multi-Phase Product & Idea Evaluation Pipeline

This skill orchestrates a complete evaluation of an idea, product, or feature set through six phases, producing multiple deliverable files. It is designed to run autonomously — slower and resource-efficient is fine; thoroughness matters more than speed.

## Overview of the Pipeline

```
INPUT (text / doc / URL / combo)
        │
        ▼
┌─ Phase 0: Ingestion ──────────────────────────────┐
│  Parse all inputs into a unified brief             │
└────────────────────────┬───────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌─ Phase 1A ──┐  ┌─ Phase 1B ──┐  ┌─ Phase 1C ──┐
│ Hater Mode  │  │ Competitive │  │ Strengths & │
│ (12 lenses) │  │ & Market    │  │ Opportunities│
└──────┬──────┘  └──────┬──────┘  └──────┬───────┘
       │                │               │
       └────────────────┼───────────────┘
                        ▼
┌─ Phase 2: Synthesis ──────────────────────────────┐
│  Critical fixes, design issues, next steps         │
└────────────────────────┬───────────────────────────┘
                         ▼
┌─ Phase 3: Content Strategy Outline ────────────────┐
│  Long-form outline for how to pitch/write about it │
└────────────────────────┬───────────────────────────┘
                         ▼
┌─ Phase 4: Deliverable Assembly ────────────────────┐
│  Compile all outputs into final files               │
└─────────────────────────────────────────────────────┘
```

## Deliverables (Multiple Files)

The pipeline produces these files in the workspace folder:

1. **`01-hater-mode-feedback.docx`** — Full 12-lens critical teardown
2. **`02-competitive-landscape.docx`** — Market context, competitors, positioning gaps
3. **`03-strengths-opportunities.docx`** — What's working, where the upside is
4. **`04-critical-fixes-and-design.docx`** — Critical fixes needed, design inconsistencies, non-breaking next steps
5. **`05-content-strategy-outline.docx`** — Long-form outline for publicly writing about or pitching the idea
6. **`00-executive-summary.docx`** — Master rollup: key findings, priority-ranked action items, go/no-go signals

---

## Run feedback & run log (optional)

This is **run feedback**, not model training: an **append-only Markdown log** so you can improve prompts and checklists over time. **Do not** silently rewrite `SKILL.md` or subagent prompts from logs—promotion goes through human review into `references/learnings.md` (see that file for promotion gates).

### Opt out and privacy

- **Disable logging:** If `MEGA_EVAL_LOG` is `0`, `off`, or `false`, skip creating or updating `run-log.md`. The pipeline runs unchanged.
- **Default:** Logs stay **workspace-local** only. Never upload run logs or paste secrets into shared learnings.
- **Redaction:** In logs and in promoted patterns, redact API keys, tokens, and sensitive URLs. Cap each log line at ~500 characters to avoid dumping huge tool output.

### Where to write `run-log.md`

Use one path consistently for the run (in order of preference):

1. `<workspace>/sessions/<session>/run-log.md` (alongside `eval-brief.md`)
2. `<workspace>/run-log.md` if session folders are not available
3. `<workspace>/.mega-eval/runs/<ISO-timestamp>/run-log.md` if you need multiple runs in one repo

### Run ID

At **Phase 0**, generate a short `run_id` (e.g. 8 alphanumeric characters) or reuse the host session id when exposed. Pass the **same** `run_id` into every Phase 1 subagent prompt (1A/1B/1C) and Phase 3 so parallel work correlates to one evaluation.

### What to append (taxonomy)

Append a timestamped line when any of these occur (not only at the end):

| Kind | When |
|------|------|
| `phase_start` / `phase_complete` | Entering or finishing a phase (0–4) |
| `tool_error` | Web fetch, search, or other tool failed |
| `retry` | Subagent or tool rerun |
| `user_correction` | User asked to rewrite a section or fix factual content |
| `assumption_flag` | Proceeded on explicit inference |
| `quality_gate_fail` | Output too thin/generic before rework |
| `implicit_signal` | Large rewrite of a raw file (if you observe it) |
| `failure_mode` | Short tag for search: `grounding`, `tool_timeout`, `scope_creep`, `format_mismatch`, etc. |
| `outcome_note` | Optional forensics only: e.g. `outcome_complete` or `outcome_abandoned` after Phase 4 (or if the user stops early)—**not** a measure of methodology quality |

### Learned patterns (human-curated)

Before **Phase 1**, skim `references/learnings.md` for methodological bullets that apply to this run (optional but recommended for maintainers).

### Pre–Phase 4 review (required when logging is on)

Before generating `.docx` files: read `run-log.md` (if present). Ensure final narrative deliverables **reflect** logged corrections and recovery paths. If `eval-brief.md` or `phase2-synthesis.md` is stale relative to corrections, reconcile them or call out the delta in the executive summary.

---

## Phase 0: Input Ingestion

Before anything else, normalize all inputs into a single **Evaluation Brief** — a structured text block that every downstream phase consumes. This ensures consistency regardless of input format.

If run logging is enabled (`MEGA_EVAL_LOG` not opted out): generate a `run_id`, create `run-log.md` at the chosen path with a **Meta** section (`run_id`, `started` ISO time, `workspace`, `status: in_progress`), and append `phase_start phase0`.

### Handling Input Types

**Raw text block:** Use directly. Extract the core idea, feature list, value proposition, and any claims made.

**Uploaded document (.pdf, .docx, .pptx, .txt, .md):** Read the file using appropriate tools (Read tool, pandoc, pdf extraction). Extract the content and summarize it into the brief format.

**URL:** Use WebFetch to crawl the page. Extract the key content — product description, features, pricing, positioning. If the URL fails, note it and proceed with whatever text the user provided.

**Combination:** Merge all sources. Deduplicate overlapping information. Note which source contributed which claims.

### Evaluation Brief Format

Produce a structured brief saved as a working file (`/sessions/<session>/eval-brief.md`):

```markdown
# Evaluation Brief

## Subject
[Name of the idea/product/feature set]

## Core Proposition
[1-2 sentences: what is this, and what problem does it solve?]

## Key Claims & Features
- [Feature/claim 1]
- [Feature/claim 2]
- ...

## Target Audience (stated or inferred)
[Who is this for?]

## Pricing/Model (if known)
[How does it make money?]

## Source Material
- [Source 1: type, key contribution]
- [Source 2: type, key contribution]

## Open Questions
- [Anything unclear or missing from the inputs]
```

If critical information is missing (e.g., the user gave a vague one-liner), ask ONE clarifying question before proceeding. Otherwise, infer what you can and note assumptions in the brief.

When Phase 0 finishes, append `phase_complete phase0` to the run log (if logging).

---

## Phase 1: Parallel Analysis (use subagents)

Launch three analysis tracks simultaneously using subagents. Each subagent receives the Evaluation Brief as input.

The key efficiency principle: each subagent does ONE job thoroughly. Don't duplicate work across tracks.

### Phase 1A: Hater Mode Critical Feedback

Spawn a subagent with these instructions:

```
You are running a critical feedback analysis. Read the hater-mode skill at:
<hater-mode-skill-path>/SKILL.md
and its references/audiences.md file.

Run correlation (include in your output header comment or first line):
- run_id: <run_id>
- log path for this pipeline: <workspace>/<run-log.md path>

Then analyze this Evaluation Brief:
<paste eval-brief content>

Produce the full 12-audience-lens teardown as specified in the hater-mode skill.
Save the output as markdown to: <workspace>/phase1a-hater-raw.md

Focus on being SPECIFIC to this particular product/idea — no generic criticism.
```

### Phase 1B: Competitive & Market Context

Spawn a subagent with these instructions:

```
You are running a competitive and market landscape analysis.

Run correlation:
- run_id: <run_id>
- log path: <workspace>/<run-log.md path>

Evaluation Brief:
<paste eval-brief content>

Your job:
1. Use WebSearch to find 3-5 direct competitors or closest alternatives
2. For each competitor, note: what they do, pricing, strengths, weaknesses relative to the subject
3. Search for market trends, market size estimates, and recent news in this space
4. Identify positioning gaps — where does the subject fit (or not fit) in the market?
5. Note any regulatory, legal, or compliance considerations

Save the output as structured markdown to: <workspace>/phase1b-competitive-raw.md

Structure:
## Direct Competitors
## Adjacent Solutions
## Market Trends & Size
## Positioning Analysis
## Risks & Considerations
```

### Phase 1C: Strengths & Opportunities

Spawn a subagent with these instructions:

```
You are running a strengths and opportunities analysis. This is deliberately the POSITIVE counterweight to the critical feedback track.

Run correlation:
- run_id: <run_id>
- log path: <workspace>/<run-log.md path>

Evaluation Brief:
<paste eval-brief content>

Your job:
1. Identify what's genuinely strong about this idea/product — be specific and honest, not cheerleading
2. Map out growth opportunities: adjacent markets, feature extensions, partnership angles
3. Identify the "unfair advantages" (if any): unique data, network effects, timing, team expertise
4. Note what would need to be true for this to succeed at scale
5. Identify the strongest use cases and ideal customer profiles

Save the output as structured markdown to: <workspace>/phase1c-strengths-raw.md

Structure:
## Core Strengths
## Growth Opportunities
## Unfair Advantages
## Success Conditions
## Ideal Use Cases & Customer Profiles
```

### Waiting for Phase 1

After launching all three subagents, wait for them to complete. While waiting, you can start drafting the structure of the Phase 2 synthesis document. Check on subagent progress periodically using read_transcript.

If logging: append `phase_start phase1` before launch and `phase_complete phase1` when all three raw files exist (or note `tool_error` / `retry` / partial output as needed).

---

## Phase 2: Synthesis — Critical Fixes, Design Issues, Next Steps

Once all Phase 1 tracks complete, read all three raw outputs and synthesize them into a single actionable document. This is the most judgment-intensive phase — do it yourself, not via subagent.

### Read All Phase 1 Outputs

Read `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, and `phase1c-strengths-raw.md`.

### Produce the Synthesis

Create `phase2-synthesis.md` with these sections:

```markdown
# Synthesis: Critical Fixes, Design Issues & Next Steps

## Critical Fixes Needed
[Issues that must be addressed before shipping or pitching. Cross-reference which Phase 1 tracks flagged each issue. Prioritize by severity and frequency of mention across tracks.]

### Fix 1: [Name]
- **What:** [Specific issue]
- **Why it matters:** [Impact if not fixed]
- **Flagged by:** [Which Phase 1 tracks and specific audiences]
- **Suggested approach:** [How to fix it]

### Fix 2: ...

## Design Inconsistencies to Resolve
[UI/UX issues, branding mismatches, messaging contradictions, experience gaps. Be specific — "the onboarding flow contradicts the pricing page's promise of simplicity."]

## Proposed Next Steps (Non-Breaking Changes)
[Changes that improve the product/idea without disrupting what's working. Ordered by effort-to-impact ratio — quick wins first, then medium-term, then strategic.]

### Quick Wins (days)
### Medium-Term (weeks)
### Strategic (months)

## Unresolved Tensions
[Legitimate disagreements between the analysis tracks. Where the hater feedback conflicts with the strengths analysis, name the tension and present both sides.]
```

If logging: append `phase_start phase2` and `phase_complete phase2` around synthesis. Log `user_correction` if the user steers synthesis before Phase 3.

---

## Phase 3: Content Strategy Outline

Spawn a subagent that uses the long-form-outline skill to create a content strategy outline. This helps the user think about how to publicly position and communicate the idea.

```
You are creating a content strategy outline. Read the long-form-outline skill at:
<long-form-outline-skill-path>/SKILL.md

Run correlation:
- run_id: <run_id>
- log path: <workspace>/<run-log.md path>

The topic is: How to position and communicate [subject name] to its target audience.

Use these inputs to inform the outline:
- Evaluation Brief: <paste>
- Key strengths: <paste top 3-5 from phase1c>
- Key criticisms to preempt: <paste top 3-5 from phase1a synthesis>
- Competitive positioning: <paste positioning analysis from phase1b>

The outline should help the user write a compelling public piece (blog post, launch announcement, pitch narrative) that:
1. Leads with the strongest value proposition
2. Preemptively addresses the top criticisms
3. Differentiates from competitors
4. Tells a narrative that makes people care

Save the full outline to: <workspace>/phase3-content-outline-raw.md
```

If logging: append `phase_start phase3` / `phase_complete phase3` around the subagent.

---

## Phase 4: Deliverable Assembly

Perform the **pre–Phase 4 review** from [Run feedback & run log](#run-feedback--run-log-optional) if logging is enabled: reconcile `run-log.md` with the latest brief/synthesis/raw files.

Now compile all raw outputs into polished .docx files. Use the docx skill (read its SKILL.md for formatting instructions) to produce each deliverable.

If logging: append `phase_start phase4`, then `phase_complete phase4`, and set `status: complete` (or `abandoned` if stopped early) in the run log Meta section.

### Assembly Order

Process deliverables in this order — the executive summary comes LAST because it draws from everything else:

1. **`01-hater-mode-feedback.docx`** — Clean up phase1a-hater-raw.md into a formatted Word doc
2. **`02-competitive-landscape.docx`** — Format phase1b-competitive-raw.md
3. **`03-strengths-opportunities.docx`** — Format phase1c-strengths-raw.md
4. **`04-critical-fixes-and-design.docx`** — Format phase2-synthesis.md
5. **`05-content-strategy-outline.docx`** — Format phase3-content-outline-raw.md
6. **`00-executive-summary.docx`** — Write fresh, drawing from all 5 documents above

### Executive Summary Structure

The executive summary is a standalone document that a decision-maker can read without opening anything else:

```markdown
# Mega Eval: [Subject Name]
## Executive Summary

### The Idea in One Paragraph
[What it is, who it's for, why it matters]

### Verdict
[Honest 2-3 sentence assessment. Not a score — a judgment.]

### Top 3 Strengths
### Top 3 Critical Issues
### Top 3 Opportunities

### Priority Action Items
[Numbered list, ordered by urgency. Each item references which detailed document has more info.]

### Competitive Position
[One paragraph summary]

### Content Strategy Hook
[The single strongest angle for publicly talking about this]
```

### File Output

All final .docx files go to the workspace output folder:
- Save to `/sessions/<session>/mnt/.claude/` so the user can access them
- Present each file with a computer:// link

### Efficiency Notes

- For the .docx files: if the raw markdown output from a phase is already well-structured, you can produce simpler docs (clean headings, body text, basic tables). Don't over-format — content quality matters more than visual polish.
- If you're running into context limits, produce the executive summary and the critical-fixes doc first (highest value), then the remaining docs.
- If a phase produced thin results (e.g., web search found little competitive data), note that honestly in the doc rather than padding.

### Maintainer feedback (optional)

After presenting the final deliverables, you may offer this block so runners can report problems or ideas on the **canonical** repo. **Forks:** if you use a different GitHub tracker, edit these URLs in your copy of `SKILL.md`.

**Something wrong or have an idea?** Open a new issue (pick the template that matches). Include this run’s **`run_id`** in the issue when you have it so maintainers can correlate with `run-log.md` or session files. **Redact** secrets, tokens, and sensitive subject matter in the issue body.

| Intent | Link |
|--------|------|
| Bug / error | [New issue — Bug](https://github.com/Cartooli/mega-eval-skill/issues/new?template=bug-report.md) |
| Improvement | [New issue — Improvement](https://github.com/Cartooli/mega-eval-skill/issues/new?template=improvement.md) |
| Feature request | [New issue — Feature](https://github.com/Cartooli/mega-eval-skill/issues/new?template=feature-request.md) |

**This run:** `run_id` = `<run_id>` (paste the same value passed to Phase 1 subagents and used in the run log if logging is on).

---

## Resource Optimization Notes

This pipeline is designed to be efficient with tokens and time:

- **Phase 1 parallelism** is the main time saver — three analysis tracks run simultaneously
- **Phase 2 synthesis** is done inline (no subagent) because it requires reading across all three tracks and exercising judgment
- **Phase 3** can run as a subagent while you start Phase 4 assembly
- **Phase 4 docs** can be produced sequentially — no need for parallel doc generation since each is independent and relatively quick
- If the input is simple (just a text block, no URLs to crawl), Phase 0 takes seconds
- If subagents are unavailable, run phases sequentially: 1A → 1B → 1C → 2 → 3 → 4. Slower but still works.

---

## Error Handling

- **URL crawl fails:** Note it in the brief, proceed with available inputs
- **Web search returns little:** Be honest — "Limited competitive data found" is better than fabrication
- **Subagent timeout:** Read whatever partial output exists, note incompleteness, continue
- **Input is extremely vague:** Ask the user ONE question, then proceed with assumptions noted
- **Too many inputs:** Summarize each, then merge. Don't try to hold 10 documents in full context.

When logging is enabled, record the corresponding `tool_error`, `retry`, or `failure_mode` lines in `run-log.md` for each of the above (redact URLs and secrets).
