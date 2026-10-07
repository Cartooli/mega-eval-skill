# Subagent Prompt Registry

This file is the **canonical prompt registry** for mega-eval subagents.

Use these templates as the source of truth when spawning subagents. `SKILL.md` should describe orchestration, required inputs, and output contracts, but should not duplicate full prompt bodies.

Replace placeholders (`<...>`) with actual values before spawning.

## Registry rules

- Each prompt has a stable **Prompt ID**.
- Bump the version suffix when a prompt changes materially enough to affect behavior or expected output shape.
- Keep the prompt body here; reference the ID from `SKILL.md`, docs, and tests.
- If you change a prompt's required output shape, update the artifact contracts, fixtures, and sample outputs in the same change.

**Models:** Before spawning, complete the **Model fit check** in the root `SKILL.md` and align subagent routing with `references/model-selection.md` (Phase 1 should use at least the **strong general** tier when the host allows separate models).

---

## Prompt ID: `phase1a.hater.v1`

**Purpose:** Hater-mode critical teardown using the external hater-mode skill.
**Inputs:** `run_id`, `run_log`, `eval_brief`, `hater_mode_skill_path`
**Output artifact:** `phase1a-hater-raw.md`

```
You are running a critical feedback analysis for a product/idea evaluation pipeline.

Run correlation (repeat these in a one-line header comment at the top of the saved file):
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

First, read the hater-mode skill instructions:
- Read: <hater-mode-skill-path>/SKILL.md
- Read: <hater-mode-skill-path>/references/audiences.md

Then analyze the following Evaluation Brief and produce the full 12-audience-lens teardown as specified in the hater-mode skill.

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

Important:
- Be SPECIFIC to this particular product/idea — no generic criticism
- Follow the exact output format from the hater-mode skill
- Include the Executive Roast Summary and Synthesis sections
- Save the complete output as markdown to: <workspace>/phase1a-hater-raw.md
```

---

## Prompt ID: `phase1b.competitive.v1`

**Purpose:** Competitive and market landscape analysis grounded in web research.
**Inputs:** `run_id`, `run_log`, `eval_brief`
**Output artifact:** `phase1b-competitive-raw.md`
**Required headings:**
- `## Direct Competitors`
- `## Adjacent Solutions`
- `## Market Trends & Size`
- `## Positioning Analysis`
- `## Risks & Considerations`

```
You are running a competitive and market landscape analysis for a product/idea evaluation pipeline.

Run correlation:
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

Your job:

1. COMPETITOR IDENTIFICATION
   - Use WebSearch to find 3-5 direct competitors or closest alternatives
   - For each: name, URL, what they do, pricing model, key strengths, key weaknesses relative to the subject
   - If the space is crowded, focus on the top 3 most relevant

2. ADJACENT SOLUTIONS
   - What are people currently using to solve this problem (even if it's not a direct competitor)?
   - Spreadsheets? Manual processes? A feature inside a larger platform?

3. MARKET TRENDS & SIZE
   - Search for market size estimates, growth projections, recent funding in this space
   - Note any recent acquisitions, pivots, or shutdowns of competitors
   - Identify whether the market is growing, contracting, or consolidating

4. POSITIONING ANALYSIS
   - Where does the subject fit in the competitive landscape?
   - What's the obvious differentiation? What's the weak differentiation?
   - Is there a clear gap in the market that this fills?

5. RISKS & CONSIDERATIONS
   - Regulatory or compliance issues
   - Platform dependency risks
   - Market timing concerns

Save the complete output as structured markdown to: <workspace>/phase1b-competitive-raw.md

Be honest about confidence levels. If web search returns limited data, say so rather than speculating.
```

---

## Prompt ID: `phase1c.strengths.v1`

**Purpose:** Positive counterweight analysis focused on strengths, upside, and success conditions.
**Inputs:** `run_id`, `run_log`, `eval_brief`
**Output artifact:** `phase1c-strengths-raw.md`
**Required headings:**
- `## Core Strengths`
- `## Growth Opportunities`
- `## Unfair Advantages`
- `## Success Conditions`
- `## Ideal Use Cases & Customer Profiles`

```
You are running a strengths and opportunities analysis for a product/idea evaluation pipeline. This is deliberately the POSITIVE counterweight to the critical feedback track — but honest, not cheerleading.

Run correlation:
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

Your job:

1. CORE STRENGTHS
   - What's genuinely strong about this idea/product?
   - What would a fan or early adopter point to as the best thing about it?
   - What's the "aha moment" for the target user?

2. GROWTH OPPORTUNITIES
   - Adjacent markets or use cases not yet addressed
   - Feature extensions that would create compounding value
   - Partnership or integration angles
   - Community or ecosystem plays

3. UNFAIR ADVANTAGES
   - Unique data access, network effects, timing advantages
   - Team/founder expertise (if known)
   - Technical moats or switching costs
   - If none exist, say so — not every idea has unfair advantages

4. SUCCESS CONDITIONS
   - What would need to be true for this to succeed at scale?
   - What are the key assumptions that must hold?
   - What's the minimum viable traction signal?

5. IDEAL USE CASES & CUSTOMER PROFILES
   - The 2-3 strongest use cases
   - Profile of the ideal early adopter
   - Profile of the ideal scale customer (might be different from early adopter)

Save the complete output as structured markdown to: <workspace>/phase1c-strengths-raw.md
```

---

## Prompt ID: `phase1d.design.v1`

**Purpose:** Report-only live-site design audit for a public marketing or product surface.
**Inputs:** `run_id`, `run_log`, `eval_brief`, `primary_url`, `references_path`
**Output artifact:** `phase1d-design-raw.md`
**Required template source:** `references/design-audit-template.md`

**When to use:** Parent run selected a **primary HTTPS URL** for a public marketing/product surface and did **not** opt out (`MEGA_EVAL_DESIGN_AUDIT` off). This track is **report-only** — no repo edits, no `/design-review` fix loop.

```
You are running a LIVE SITE DESIGN AUDIT for a product/idea evaluation pipeline (Phase 1D).

Run correlation (repeat in a one-line HTML comment at the top of the saved file):
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

Read the output template and rules:
- Read: <references-path>/design-audit-template.md

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

=== PRIMARY URL TO AUDIT ===
<single https URL — marketing or product home>
=== END URL ===

Your job:

1. **Evidence tier (pick honestly)**
   - **Tier A:** Use headless browse / screenshot tools if the host provides them (e.g. gstack browse). Capture 1–3 screenshots to the workspace and reference paths in the doc. Visit homepage + up to 2 key paths (e.g. /pricing, /product) if reachable without login.
   - **Tier B:** If no browser is available, use WebFetch/HTML-visible content only. State limits prominently in Meta (layout, motion, and many interaction states may be unknown).
   - **Tier C:** If the URL fails, requires auth, or returns no meaningful HTML, write a short `phase1d-design-raw.md` explaining why and stop — do not block other pipeline tracks.

2. **Content**
   - Follow `design-audit-template.md` sections exactly (Meta, First impression, Inferred design system, Checklist highlights, AI slop, Litmus, Quick wins, Evidence, Headline for synthesis).
   - Classify **MARKETING/LANDING** vs **APP UI** vs **HYBRID** from what you see.
   - Be specific to this site — no generic design platitudes.

3. **Scope discipline**
   - This is NOT WCAG compliance certification. Say so in the disclaimer.
   - Do NOT read or assume access to the product’s source repository unless the parent explicitly provided it.
   - Do NOT claim you tested authenticated flows unless you actually did.

Save the complete markdown to: <workspace>/phase1d-design-raw.md
```

---

## Prompt ID: `phase1e.security.v1`

**Purpose:** Observation-only security posture audit (optional live-site track).
**Inputs:** `run_id`, `run_log`, `eval_brief`, `primary_url`, `cso_skill_path`, `references_path`
**Output artifact:** `phase1e-security-raw.md` (plus optional `phase1e-malicious-signals.md`)
**When to use:** Parent run recorded **Audit decision: run** under **Security audit (Phase 1E)** and did **not** opt out (`MEGA_EVAL_SECURITY_AUDIT` off). **Observation-only** — not a penetration test, not compliance certification. **No** credential testing, rate-limit probing, or intrusive actions.

```
You are running a SECURITY AUDIT for a product/idea evaluation pipeline (Phase 1E) — report only; no intrusive testing.

Run correlation (repeat in a one-line HTML comment at the top of the saved file):
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

Methodology (read in order):
1. If the file exists, read the host’s CSO-style security skill: <cso-skill-path>/SKILL.md (and any references it requires for *observation-only* posture). Use it to structure analysis and severity language.
2. Regardless, read the output template: <references-path>/security-audit-template.md — this file is the **canonical output shape** and the **fallback checklist** when the external skill is unavailable. If you could not use the external skill, set Meta **methodology** to `fallback: embedded` (and state `methodology: fallback` in Meta); otherwise `external: /cso` or equivalent.

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

=== PRIMARY URL (ONLY LIVE SURFACE FOR INSPECTION) ===
<single https URL — same Primary URL as other live-site tracks, or note if n/a>
=== END URL ===

Evidence tier (pick honestly; mirror Phase 1D):
- **Tier A:** Headless browse / screenshot tools if available — Primary URL only; optionally **one** linked privacy-policy page if clearly reachable from the primary site (no crawling).
- **Tier B:** WebFetch / HTML-visible content only — state limits in Meta.
- **Tier C:** URL missing or unusable — short stub per template; do not block other tracks.

**Strict scope:**
- Use **only** the Primary URL for live inspection (WebFetch or browse). Do **not** run broad WebSearch, do **not** inspect private repos, do **not** attempt logins or authenticated flows unless the parent explicitly provided credentials (default: no).
- **Redact** anything resembling secrets, tokens, API keys, or sensitive query params before saving — replace with `[REDACTED]` in evidence snippets.

Output sections must follow `security-audit-template.md` (Meta, Transport & headers, Auth & session surface, Privacy & data handling, LLM/AI exposure, Red flags, **Malicious / suspicious code signals**, Findings table with severities and **Remediation needed** column, Disclaimer, Headline for synthesis with **Security risk band**).

For the **Malicious / suspicious code signals** section:
- Scan all inline and directly linked JavaScript visible in the fetched HTML for obfuscated code, unexpected external script sources, cryptominer patterns, keylogger/form-scraping indicators, malicious iframes, drive-by download triggers, and suspicious redirects.
- Cross-check all external script/iframe/fetch domains against the **Known-bad domain quick-reference table** in `security-audit-template.md`. A match is automatic **Critical** severity.
- For Tier A runs: cross-reference unfamiliar domains against URLhaus (urlhaus.abuse.ch), PhishTank, and Google Safe Browsing Transparency Report where feasible.
- Each signal found must appear as a row in the Findings table with `Remediation needed: Yes` and a short note explaining the risk. If none found, state that explicitly.

**Stub file rule:** If 1 or more signals are found, also write `<workspace>/phase1e-malicious-signals.md` using the stub format defined in `security-audit-template.md` (full evidence, redacted snippets, step-by-step remediation, checklist). In the main `phase1e-security-raw.md` Malicious / suspicious code signals section, replace detail with the one-line reference summary (signal count + highest severity + pointer to stub file).

Save the main security audit to: <workspace>/phase1e-security-raw.md
Save the malicious signals stub (only if signals found) to: <workspace>/phase1e-malicious-signals.md
```

---

## Prompt ID: `phase1f.durability.v1`

**Purpose:** AI/agent durability audit of the public surface (optional live-site track).
**Inputs:** `run_id`, `run_log`, `eval_brief`, `primary_url`, `durability_review_skill_path`, `references_path`
**Output artifact:** `phase1f-durability-raw.md`
**When to use:** Parent run recorded **Audit decision: run** under **AI durability audit (Phase 1F)** and did **not** opt out (`MEGA_EVAL_DURABILITY_AUDIT` off). Focus: resilience to model/API/provider **change** for AI/agent surfaces — not general business vendor risk (that stays in Phase 1B).

```
You are running an AI / AGENT DURABILITY AUDIT for a product/idea evaluation pipeline (Phase 1F) — report only.

Run correlation (repeat in a one-line HTML comment at the top of the saved file):
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

Methodology (read in order):
1. If the file exists, read: <durability-review-skill-path>/SKILL.md — use it to frame dimensions (model abstraction, prompts/tools, state, evals) as they apply to the **subject’s public surface** (marketing/docs), not the subject’s private codebase unless publicly linked.
2. Always read: <references-path>/durability-audit-template.md — **output shape** and **fallback checklist**. If the external skill was unavailable, follow the embedded checklist and set Meta **methodology** to `fallback: embedded`; else `external: /durability-review` or equivalent.

=== EVALUATION BRIEF ===
<paste eval-brief content here>
=== END BRIEF ===

=== PRIMARY URL (ONLY LIVE SURFACE FOR INSPECTION) ===
<single https URL — same Primary URL as other live-site tracks, or note if n/a>
=== END URL ===

**Applicability (you own this judgment):** If the subject has **no** meaningful AI, LLM, or agent surface on the public evidence available, write the **N/A stub** per `durability-audit-template.md` (risk band `N/A`, short rationale, no padded content) and **stop**. This is success, not failure.

Evidence tier: same Tier A / B / C pattern as Phase 1D (Primary URL only; no broad WebSearch; no repo cloning).

**Strict scope:**
- Do **not** run broad WebSearch; do **not** inspect private repos. Public marketing, docs, and fetched HTML only.
- **Redact** secrets in evidence snippets.

Output sections follow `durability-audit-template.md` including Findings table, Disclaimer, and **Headline for synthesis** with **AI durability risk band** (or N/A stub).

Save the complete markdown to: <workspace>/phase1f-durability-raw.md
```

---

## Phase 3: Content Strategy Outline Subagent

## Prompt ID: `phase3.content-outline.v1`

**Purpose:** Produce the raw content strategy outline using the external long-form-outline skill.
**Inputs:** `run_id`, `run_log`, `subject_name`, `eval_brief`, `top_strengths`, `top_criticisms`, `competitive_positioning`, `long_form_outline_skill_path`
**Output artifact:** `phase3-content-outline-raw.md`

```
You are creating a content strategy outline using the long-form-outline methodology.

Run correlation:
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

First, read the long-form-outline skill instructions:
- Read: <long-form-outline-skill-path>/SKILL.md

The topic for the outline is: How to position and communicate <subject name> to its target audience.

Use these inputs to ground the outline in real analysis (not speculation):

=== EVALUATION BRIEF ===
<paste brief>
=== END BRIEF ===

=== TOP STRENGTHS ===
<paste top 3-5 strengths from Phase 1C>
=== END STRENGTHS ===

=== TOP CRITICISMS TO PREEMPT ===
<paste top 3-5 critical issues from Phase 1A synthesis>
=== END CRITICISMS ===

=== COMPETITIVE POSITIONING ===
<paste positioning analysis from Phase 1B>
=== END POSITIONING ===

The outline should help the user write a compelling public piece (blog post, launch announcement, pitch narrative) that:
1. Leads with the strongest value proposition
2. Preemptively addresses the top criticisms
3. Differentiates from competitors
4. Tells a narrative arc that makes people care

Follow all phases from the long-form-outline skill (Panel Deconstruction, Working Outline, Abstract, Full Outline, Resolution).

Save the full outline as markdown to: <workspace>/phase3-content-outline-raw.md

Note: Do NOT produce a .docx yet — just the raw markdown. The parent pipeline handles final formatting.
```

---

## Prompt ID: `prompt.derivation.v1`

**Purpose:** Decompose a request into a schema-validated Prompt Derivation Engine JSON spec.
**Inputs:** `run_id`, `run_log`, `user_request`, `artifacts`, `preferences`, `prompt_derivation_skill_path`, `repo_root`
**Output artifact:** `prompt-derivation-spec.json`
**When to use:** Decompose a request into a structured prompt spec before execution. Can be called at any phase boundary or standalone.

```
You are running the Prompt Derivation Engine — converting a user request into a
structured, schema-validated JSON spec.

Run correlation:
- run_id: <run_id>
- run_log: <workspace>/<path-to-run-log.md>

First, read the prompt-derivation skill and schema:
- Read: <prompt-derivation-skill-path>/SKILL.md
- Read: <repo-root>/schemas/prompt-derivation-engine.schema.json

Then derive a full Prompt Derivation Engine Spec for the following request:

=== USER REQUEST ===
<paste user request or upstream phase output here>
=== END REQUEST ===

=== ARTIFACTS (if any) ===
<list artifact references: file paths, URLs, inline content>
=== END ARTIFACTS ===

=== PREFERENCES (if any) ===
<tone, verbosity, format overrides — omit section if none>
=== END PREFERENCES ===

Important:
- Every required field in the schema MUST be populated
- Use the enum values defined in the schema — do not invent new ones
- Be honest about uncertainty_level and failure_modes
- Save the complete JSON spec to: <workspace>/prompt-derivation-spec.json
```


---

## Prompt ID: `phase0.brief.v1`

**Purpose:** Normalize inputs into a single Evaluation Brief markdown artifact.
**Inputs:** user text, uploaded documents, URLs, env opt-out flags
**Output artifact:** `eval-brief.md`

```
Produce a structured Evaluation Brief saved as markdown (prefer /sessions/<session>/eval-brief.md when using sessions).

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
- **Primary URL for Phase 1D:** [Single https:// marketing/product URL, or n/a]
- **Audit decision:** [run | skipped] — [one-line reason]

## Security audit (Phase 1E)
- **Audit decision:** [run | skipped] — [one-line reason]

## AI durability audit (Phase 1F)
- **Audit decision:** [run | skipped] — [one-line reason]
- **AI-surface applicability note:** [quick guess or defer to 1F subagent]

Follow root SKILL.md Phase 0 for ingestion rules, env opt-outs, and clarifying questions. After writing, run Gate A: validate_run_artifacts.py --gate pre-phase1.
```


---

## Prompt ID: `phase2.synthesis.v1`

**Purpose:** Output shape for Phase 2 synthesis markdown (orchestrator-authored; not a subagent spawn).
**Inputs:** phase1a/1b/1c raw outputs; optional phase1d/1e/1f; merge rules from root SKILL.md Phase 2
**Output artifact:** `phase2-synthesis.md`

```
# Synthesis: Critical Fixes, Design Issues & Next Steps

## Critical Fixes Needed
[Issues that must be addressed before shipping or pitching. Cross-reference which Phase 1 tracks flagged each issue. Prioritize by severity and frequency of mention across tracks.]

**Merge order when 1E/1F exist:** Add Phase 1E Critical and High findings first (with [1E-S<n>] tags); then Phase 1F Critical and High (with [1F-D<n>] tags); then other tracks. Dedupe against 1A as in SKILL.md.

### Fix 1: [Name]
- **What:** [Specific issue]
- **Why it matters:** [Impact if not fixed]
- **Flagged by:** [Which Phase 1 tracks — use tags when citing 1E/1F rows]
- **Suggested approach:** [How to fix it]

### Fix 2: ...

## Design Inconsistencies to Resolve
[UI/UX issues, branding mismatches, messaging contradictions, experience gaps.]

**When Phase 1D exists:** Incorporate live-site audit findings here (and in Critical Fixes if severity warrants). Cite Headline for synthesis / Design risk band from phase1d-design-raw.md.

**1E/1F:** Security and durability findings do not belong in this section unless purely presentational (rare).

## Proposed Next Steps (Non-Breaking Changes)
[Ordered by effort-to-impact. When 1E/1F exist, add Medium items tagged [1E-S<n>] / [1F-D<n>].]

### Quick Wins (days)
### Medium-Term (weeks)
### Strategic (months)

## Unresolved Tensions
[Legitimate disagreements between analysis tracks.]

Follow root SKILL.md Phase 2 for read order, dedupe, and malicious-signals merge. After writing, run Gate C: validate_run_artifacts.py --gate pre-phase3.
```
