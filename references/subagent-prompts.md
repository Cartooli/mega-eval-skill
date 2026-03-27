# Subagent Prompt Templates

These are ready-to-use prompt templates for each parallel subagent. Replace placeholders (`<...>`) with actual values before spawning.

---

## Phase 1A: Hater Mode Subagent

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

## Phase 1B: Competitive & Market Context Subagent

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

## Phase 1C: Strengths & Opportunities Subagent

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

## Phase 3: Content Strategy Outline Subagent

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

## Prompt Derivation Engine Subagent

Use this when you need to decompose a request into a structured prompt spec before execution. Can be called at any phase boundary or standalone.

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
