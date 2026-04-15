---
name: mega-eval
description: "Run a comprehensive, multi-phase evaluation of any idea, product, or feature set — producing multiple deliverable files covering critical feedback, competitive context, strengths & opportunities, design issues (including optional live-site visual/UX audit when an HTTPS product URL is in scope), optional security posture audit (Phase 1E), optional AI/agent durability audit (Phase 1F), proposed fixes, and a content strategy outline. Accepts any combination of raw text, uploaded documents, or crawlable URLs as input. Orchestrates parallel subagents for efficiency. Use this skill whenever someone says 'evaluate this idea', 'tear down this product', 'full analysis of', 'mega eval', 'comprehensive review', 'deep evaluation', 'assess this feature set', 'product review pipeline', or any request for a thorough multi-dimensional analysis of a concept, product, or feature. Also trigger when the user provides a URL, doc, or text block and asks for a complete picture — strengths, weaknesses, market context, and next steps."
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
│  (+ optional: primary URL for live-site tracks)   │
└────────────────────────┬───────────────────────────┘
                         │
   ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
   ▼         ▼         ▼         ▼         ▼         ▼         │
 Phase 1A  Phase 1B  Phase 1C  Phase 1D  Phase 1E  Phase 1F    │
 Hater     Comp.     Strengths Design    Security  AI dur.    │
 (always)  (always)  (always)  (opt.)    (opt.)    (opt.)     │
   └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
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

## Model fit check (required before Phase 1)

Mega Eval is **reasoning- and synthesis-heavy**; model tier directly affects depth, grounding, and whether Phase 2 surfaces real tradeoffs versus generic advice. **Do not skip this check.**

1. **Read** `references/model-selection.md` in this skill’s package (phase mapping, minimum tiers, deprecation notes).
2. **Consult vendor docs** when verifying IDs or aliases: [OpenAI Models](https://developers.openai.com/api/docs/models), [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
3. **Discover** what the host allows: one global model, per-subagent routing, or fixed defaults you cannot change.
4. **Verify selections:**
   - **Phase 2 (synthesis)** must use the **frontier / flagship** text model for the active provider when available (e.g. `gpt-5.4`, `claude-opus-4-6`). Never run synthesis on **mini / nano / haiku–class** models unless the user **explicitly** asked for a cost-saving run.
   - **Phase 1 (1A–1C, optional 1D)** should use at least the **strong general** tier when the host can split models (e.g. `gpt-5.4-mini`, `claude-sonnet-4-6`). If the host exposes **only one** model for all steps, use the **frontier** tier for the entire pipeline.
   - **Phase 3** should not use a weaker tier than Phase 1 unless the same constraint as Phase 2 applies.
5. **If models are constrained** (locked mini tier, deprecated snapshot, or unknown routing): add a short **Model limitation** bullet under **Open Questions** in `eval-brief.md`, and if run logging is on append a `model_check` line to `run-log.md` (see [Run feedback & run log](#run-feedback--run-log-optional)).

---

## Deliverables (Multiple Files)

The pipeline produces these files in the workspace folder:

1. **`01-hater-mode-feedback.docx`** — Full 12-lens critical teardown
2. **`02-competitive-landscape.docx`** — Market context, competitors, positioning gaps
3. **`03-strengths-opportunities.docx`** — What's working, where the upside is
4. **`04-critical-fixes-and-design.docx`** — Critical fixes needed, design inconsistencies, non-breaking next steps
5. **`05-content-strategy-outline.docx`** — Long-form outline for publicly writing about or pitching the idea
6. **`00-executive-summary.docx`** — Master rollup: key findings, priority-ranked action items, go/no-go signals (optional **Security Posture** and **AI Durability Posture** mini-sections when Phase 1E / 1F ran and apply)

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

At **Phase 0**, generate a short `run_id` (e.g. 8 alphanumeric characters) or reuse the host session id when exposed. Pass the **same** `run_id` into every Phase 1 subagent prompt (1A/1B/1C, and **1D** / **1E** / **1F** when run) and Phase 3 so parallel work correlates to one evaluation.

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
| `model_check` | Model fit verified vs `references/model-selection.md` — include `pass`, `compromise`, or `host_locked` and observed model names (redact tenant-specific secrets) |
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

## Live site / design audit (Phase 1D)
- **Primary URL for Phase 1D:** [Single `https://` marketing/product URL, or `n/a`]
- **Audit decision:** [run | skipped] — [one-line reason: no URL, user opt-out, PDF-only inputs, etc.]

## Security audit (Phase 1E)
- **Audit decision:** [run | skipped] — [one-line reason: env opt-out, no usable evidence, no Primary URL, etc.]

## AI durability audit (Phase 1F)
- **Audit decision:** [run | skipped] — [one-line reason: env opt-out, no Primary URL, etc.]
- **AI-surface applicability note:** [orchestrator's quick guess if easy; else `defer to 1F subagent`]
```

If critical information is missing (e.g., the user gave a vague one-liner), ask ONE clarifying question before proceeding. Otherwise, infer what you can and note assumptions in the brief.

### Optional live-site tracks (Phase 1D, 1E, 1F) — Phase 0 decisions

Use the **same** primary **`https://`** URL for 1D, 1E, and 1F when more than one track runs (the brief’s **Primary URL for Phase 1D** field is the shared **Primary URL** for all live-site tracks). If there is no usable URL, record **skipped** for each affected track with an explicit reason.

**Env opt-out parity** — treat each variable as disabled when its value is `0`, `off`, or `false` (case-insensitive). When unset, defaults below apply.

| Env var | Track | When skipped in Phase 0 |
|--------|--------|-------------------------|
| `MEGA_EVAL_DESIGN_AUDIT` | Phase 1D (design) | Set **Audit decision: skipped** (reason: env opt-out). Do **not** launch 1D. |
| `MEGA_EVAL_SECURITY_AUDIT` | Phase 1E (security) | Set **Audit decision: skipped** under **Security audit** (reason: env opt-out). Do **not** launch 1E. |
| `MEGA_EVAL_DURABILITY_AUDIT` | Phase 1F (AI durability) | Set **Audit decision: skipped** under **AI durability audit** (reason: env opt-out). Do **not** launch 1F. |

#### Phase 1D — live-site design audit

**Purpose:** When the subject has a **public web surface**, add a **report-only** visual/UX audit (`phase1d-design-raw.md`) in parallel with Phase 1A–1C. This is **not** the gstack `/design-review` fix-and-commit loop (which targets **your** codebase). Phase 1D only produces **markdown + optional screenshots** for synthesis.

**Default when env is unset:** **Run** Phase 1D when you can name **one** primary **`https://`** URL that reasonably represents the **marketing or product** experience. Prefer the URL the user highlighted; otherwise infer from **Source Material** (exclude obvious non-surfaces: direct `.pdf` links, raw file hosts, or pages that are clearly not the product).

#### Phase 1E — security audit (CSO-style)

**Purpose:** Structured, **observation-only** security findings with a scored risk band (`phase1e-security-raw.md`). **Never** credential testing, rate-limit probing, or intrusive action — report-only, Primary URL (+ optional single privacy-policy page for cross-check).

**Default when env is unset:** **Run** Phase 1E whenever inputs allow (same Primary URL rule as 1D). If there is no Primary URL, set **Audit decision: skipped** or **run** with Tier C / limits documented in the subagent output (brief should state the decision in one line).

#### Phase 1F — AI / agent durability audit

**Purpose:** Resilience of the subject’s **AI/agent surface** to model/API/provider change (`phase1f-durability-raw.md`), with risk band `Low | Medium | High | Critical | N/A`.

**Applicability** is judged **inside the 1F subagent** (not in Phase 0). Phase 0 only records **AI-surface applicability note** as a quick guess or `defer to 1F subagent`.

**Default when env is unset:** **Launch** 1F when allowed; the subagent writes a short **N/A** stub (no padded content) if there is no meaningful AI/LLM/agent surface.

**Ambiguity:** If multiple URLs qualify for the primary site, pick **one** and note the others under Open Questions — do not spawn multiple primary-url tracks.

When Phase 0 finishes, append `phase_complete phase0` to the run log (if logging).

---

## Phase 1: Parallel Analysis (use subagents)

Launch **three** analysis tracks **always** (1A–1C). In the **same wave**, also launch:

- **Phase 1D** only when Phase 0 recorded **Audit decision: run** under **Live site / design audit**.
- **Phase 1E** only when Phase 0 recorded **Audit decision: run** under **Security audit (Phase 1E)**.
- **Phase 1F** only when Phase 0 recorded **Audit decision: run** under **AI durability audit (Phase 1F)**.

Each subagent receives the Evaluation Brief as input; Phase 1D/1E/1F also receive the **Primary URL** explicitly when the brief has one.

The key efficiency principle: each subagent does ONE job thoroughly. Don't duplicate work across tracks.

**Phase 1D / 1E / 1F failure isolation:** If any of 1D, 1E, or 1F fails, times out, or produces Tier C “thin” output, log `tool_error` or `failure_mode` when logging is on (scope the line to the track, e.g. 1E or 1F) — **do not** block Phase 2. Proceed once **1A–1C are complete**. **Do not** block Phase 2 on 1D, 1E, or 1F alone.

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

### Phase 1D: Live site design audit (optional)

**Only if** Phase 0 **Audit decision** was **run**. Use the template in `references/design-audit-template.md` and the ready-made prompt in `references/subagent-prompts.md` (**Phase 1D**).

Spawn a subagent with instructions equivalent to:

```
You are running a LIVE SITE DESIGN AUDIT (Phase 1D) — report only; no code changes.

Run correlation:
- run_id: <run_id>
- log path: <workspace>/<run-log.md path>

Read: <references-path>/design-audit-template.md

Evaluation Brief:
<paste eval-brief content>

Primary URL to audit (HTTPS):
<paste Primary URL for Phase 1D from brief>

Tier A: use headless browse / screenshot tools if available; save screenshots under the workspace and reference paths.
Tier B: if no browser, use WebFetch/HTML and state limits in the output Meta.
Tier C: if the URL is unusable, write a short markdown explaining why.

Save the output to: <workspace>/phase1d-design-raw.md

Follow design-audit-template.md sections. This is not a WCAG compliance certificate.
```

### Phase 1E: Security audit (optional)

**Only if** Phase 0 **Audit decision** was **run** under **Security audit (Phase 1E)**. Use `references/security-audit-template.md` and the prompt in `references/subagent-prompts.md` (**Phase 1E**). The orchestrator resolves `<cso-skill-path>` to the host’s `/cso` skill (same placeholder pattern as `<hater-mode-skill-path>`). If unavailable, the subagent follows the embedded fallback checklist in `security-audit-template.md` and sets `methodology: fallback` in Meta.

Spawn a subagent with instructions equivalent to the **Phase 1E** block in `references/subagent-prompts.md` (correlation header, Primary URL only — no broad WebSearch, no repo inspection, no credentialed probes; redact secrets before saving).

**Output:** `<workspace>/phase1e-security-raw.md`

### Phase 1F: AI / agent durability audit (optional)

**Only if** Phase 0 **Audit decision** was **run** under **AI durability audit (Phase 1F)**. Use `references/durability-audit-template.md` and the prompt in `references/subagent-prompts.md` (**Phase 1F**). Resolve `<durability-review-skill-path>` like other skill placeholders. If the external skill is missing, use the template as fallback and set `methodology: fallback` in Meta.

**Applicability** (whether the subject has a meaningful AI/agent surface) is decided **inside this subagent**. If none, write the **N/A** stub per template and stop — not a pipeline failure.

**Output:** `<workspace>/phase1f-durability-raw.md`

### Waiting for Phase 1

After launching subagents, wait until:

- **`phase1a-hater-raw.md`**, **`phase1b-competitive-raw.md`**, and **`phase1c-strengths-raw.md`** exist (required), and
- **If Phase 1D was launched:** `phase1d-design-raw.md` exists **or** you have logged abandonment / thin output for 1D and chosen to proceed.
- **If Phase 1E was launched:** `phase1e-security-raw.md` exists **or** you have logged abandonment / thin output for 1E and chosen to proceed.
- **If Phase 1F was launched:** `phase1f-durability-raw.md` exists **or** you have logged abandonment / thin output for 1F and chosen to proceed.

While waiting, you can start drafting the structure of the Phase 2 synthesis document. Check on subagent progress periodically using read_transcript.

If logging: append `phase_start phase1` before launch and `phase_complete phase1` when the conditions above are met (note `tool_error` / `retry` / `failure_mode` / partial output for any track, including 1D, 1E, and 1F, as needed).

---

## Phase 2: Synthesis — Critical Fixes, Design Issues, Next Steps

Once Phase 1 **required** tracks (1A–1C) complete, read the Phase 1 raw outputs and synthesize them into a single actionable document. This is the most judgment-intensive phase — do it yourself, not via subagent. **Optional** tracks (1D–1F) may be missing, thin, or failed — proceed with synthesis regardless; note limits where relevant.

### Read All Phase 1 Outputs

Read `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, and `phase1c-strengths-raw.md`.

**If `phase1d-design-raw.md` exists** (Phase 1D ran or produced a thin-failure stub), read it. Treat it as the **authoritative source for rendered-site visual/UX** observations. **Deduplicate** against Phase 1A where personas commented on “looks” — prefer Phase 1D for layout, typography, template tells, and interaction affordances; keep 1A for **reception / credibility narratives** that are not purely visual.

**If `phase1e-security-raw.md` exists**, read it. Treat it as the **authoritative source for structured security findings** (risk band, findings table). **Deduplicate** against Phase 1A: if 1A personas touched trust/security, keep narrative in 1A but **do not** duplicate 1E’s Critical/High items as separate critical fixes — prefer **1E** for security specifics.

**If `phase1f-durability-raw.md` exists** and the risk band is **not** `N/A`, read it. Treat it as the **authoritative source for AI/agent durability** (model abstraction, prompt architecture, provider concentration, evals). **Deduplicate** against Phase 1B: general vendor/platform lock-in stays in 1B; 1F is strictly AI/agent durability. If a finding is genuinely cross-cutting, cite both.

### Cross-reference tags (compact citations)

Use this format so readers can jump back to raw findings tables:

- **`[1E-S<n>]`** — Security finding row `<n>` from `phase1e-security-raw.md` (e.g. `[1E-S3]`).
- **`[1F-D<n>]`** — Durability finding row `<n>` from `phase1f-durability-raw.md` (e.g. `[1F-D2]`).
- **Phase 1A** may still use persona labels, e.g. `[1A(Skeptical Engineer)]`.

**Example:** “Harden OAuth callback handling `[1E-S3]` before expanding enterprise pilots; 1A’s skepticism on enterprise readiness `[1A(Skeptical Engineer)]` aligns but defers implementation detail to 1E.”

### Produce the Synthesis

Create `phase2-synthesis.md` with these sections:

```markdown
# Synthesis: Critical Fixes, Design Issues & Next Steps

## Critical Fixes Needed
[Issues that must be addressed before shipping or pitching. Cross-reference which Phase 1 tracks flagged each issue. Prioritize by severity and frequency of mention across tracks.]

**Merge order when 1E/1F exist:** Add **Phase 1E** `Critical` and `High` findings first (with `[1E-S<n>]` tags); then **Phase 1F** `Critical` and `High` (with `[1F-D<n>]` tags); then other tracks. Dedupe against 1A as above.

### Fix 1: [Name]
- **What:** [Specific issue]
- **Why it matters:** [Impact if not fixed]
- **Flagged by:** [Which Phase 1 tracks — use tags above when citing 1E/1F rows]
- **Suggested approach:** [How to fix it]

### Fix 2: ...

## Design Inconsistencies to Resolve
[UI/UX issues, branding mismatches, messaging contradictions, experience gaps. Be specific — "the onboarding flow contradicts the pricing page's promise of simplicity."]

**When Phase 1D exists:** Incorporate **live-site audit** findings here (and in Critical Fixes if severity warrants). Cite **Headline for synthesis** / **Design risk band** from `phase1d-design-raw.md`. Merge **Quick wins** from 1D into **Proposed Next Steps** where they do not duplicate.

**1E/1F:** Security and durability findings **do not** belong in this section unless they are purely presentational (rare). Default: 1E/1F → Critical Fixes / Next Steps / Unresolved Tensions only.

## Proposed Next Steps (Non-Breaking Changes)
[Changes that improve the product/idea without disrupting what's working. Ordered by effort-to-impact ratio — quick wins first, then medium-term, then strategic.]

**When 1E/1F exist:** Add 1E and 1F **Medium** (and low-effort) items here under the appropriate effort buckets, tagged `[1E-S<n>]` / `[1F-D<n>]` where helpful.

### Quick Wins (days)
### Medium-Term (weeks)
### Strategic (months)

## Unresolved Tensions
[Legitimate disagreements between the analysis tracks. Where the hater feedback conflicts with the strengths analysis, name the tension and present both sides.]

**When relevant:** Name tensions such as security vs. speed-to-market, or durability vs. model-chasing, using 1E/1F evidence.
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
6. **`00-executive-summary.docx`** — Write fresh, drawing from all 5 documents above (include **Live Site / Product Surface** when `phase1d-design-raw.md` informed `phase2-synthesis.md`; include **Security Posture** / **AI Durability Posture** when Phase 1E / Phase 1F ran with non-stub output — see structure below)

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

### Live Site / Product Surface (only if Phase 1D ran)
[2–4 bullets: design risk band, first-impression verdict, top UX credibility issue, top quick win — or state that Phase 1D was skipped/thin]

### Security Posture (only if Phase 1E ran)
**Risk band:** Low | Medium | High | Critical
[One-line headline from `phase1e-security-raw.md` **Headline for synthesis**]
[Top finding, one line with `[1E-S<n>]` citation]
[Top quick-win next step, one line — or omit if none]

### AI Durability Posture (only if Phase 1F ran and risk band is not N/A)
**Risk band:** Low | Medium | High | Critical
[One-line headline from `phase1f-durability-raw.md` **Headline for synthesis**]
[Top finding, one line with `[1F-D<n>]` citation]
[Top quick-win next step, one line — or omit if none]

When Phase 1F exited with **N/A**, **omit** the AI Durability Posture section entirely — do not include a “not applicable” stub in the executive summary.
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

- **Phase 1 parallelism** is the main time saver — three analysis tracks always; **optional** live-site tracks (1D design, 1E security, 1F AI durability) when Phase 0 decisions and env allow
- **Phase 2 synthesis** is done inline (no subagent) because it requires reading across all three tracks and exercising judgment
- **Phase 3** can run as a subagent while you start Phase 4 assembly
- **Phase 4 docs** can be produced sequentially — no need for parallel doc generation since each is independent and relatively quick
- If the input is simple (just a text block, no URLs to crawl), Phase 0 takes seconds
- If subagents are unavailable, run phases sequentially: 1A → 1B → 1C → (optional 1D, 1E, 1F) → 2 → 3 → 4. Slower but still works.

---

## Error Handling

- **URL crawl fails:** Note it in the brief, proceed with available inputs
- **Web search returns little:** Be honest — "Limited competitive data found" is better than fabrication
- **Subagent timeout:** Read whatever partial output exists, note incompleteness, continue
- **Input is extremely vague:** Ask the user ONE question, then proceed with assumptions noted
- **Too many inputs:** Summarize each, then merge. Don't try to hold 10 documents in full context.
- **Phase 1D unavailable or thin:** Record in `phase1d-design-raw.md` and proceed; synthesis should note **design audit limits** rather than inventing visual claims.
- **Phase 1E unavailable or thin:** Record in `phase1e-security-raw.md` (or log and proceed without blocking Phase 2); synthesis should note **security audit limits** rather than inventing findings. Do not block Phase 2 on 1E alone.
- **Phase 1F unavailable, thin, or N/A stub:** Record in `phase1f-durability-raw.md`; if **N/A**, omit **AI Durability Posture** from the executive summary. Do not block Phase 2 on 1F alone.

When logging is enabled, record the corresponding `tool_error`, `retry`, or `failure_mode` lines in `run-log.md` for each of the above (redact URLs and secrets).
