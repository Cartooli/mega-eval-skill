# Phase 3: Content Strategy Outline — mega-eval

## The Angle

**Lead with the meta-evaluation.** The strongest content hook for mega-eval is the self-referential case study: a product evaluation tool that evaluates itself, surfaces real criticisms, and ships the fixes. This is inherently interesting because it demonstrates the tool's output quality while telling an honest story about building in public.

**Working title:** "I Built a Tool to Tear Apart Product Ideas — Then Pointed It at Itself"

---

## Outline

### I. Opening Hook — The Problem with "Evaluate My Idea"

**Purpose:** Establish the pain point that mega-eval solves — the gap between asking an LLM for feedback and getting structured, multi-perspective analysis.

- Start with a familiar scenario: you paste your idea into Claude and get one monolithic response that sounds helpful but misses angles
- The response anchors on whatever the model fixates on first — if it leads with a strength, the criticism is soft; if it leads with a flaw, the praise is performative
- What you actually need is what a good advisory board gives you: multiple independent perspectives that don't contaminate each other, then a synthesis that surfaces contradictions
- That's what mega-eval does — but the interesting part is what happened when we turned it on itself

### II. What Mega-Eval Actually Produces (The Demo)

**Purpose:** Show, don't tell. Walk through the actual output from the self-evaluation run.

- Briefly explain the pipeline: ingest, 3 parallel analysis tracks, synthesis, content strategy, 6 deliverable docs
- Show the hater-mode highlights: which of the 12 personas had the sharpest criticism? (The Software Tester: "zero tests, no validation, no way to know if a run was successful." The General Hater: "This is a README for a prompt.")
- Show the competitive landscape finding: no existing tool combines adversarial critique + competitive research + strengths analysis in a single pipeline
- Show the synthesis tension: "It's just a prompt" vs. "The methodology is the moat" — the haters and the strengths track disagree, and the synthesis surfaces that disagreement instead of resolving it
- The executive summary's verdict: honest, specific, not a score — a judgment

### III. What the Self-Evaluation Caught (Honest Reckoning)

**Purpose:** Build credibility by showing what the tool found that the builder missed or hadn't addressed.

- The recurring theme across all 12 hater personas: "Show the output." Every criticism weakens if you just demonstrate what the pipeline produces. The builder hadn't shipped sample output — the tool caught that.
- The duplicate Dependencies/Prerequisites sections — a polish issue the builder's eyes had skipped
- The unvalidated skill links — pointing to GitHub paths that might not exist
- The missing "Who is this for?" section — the README assumed the reader already knew what Claude Code skills are
- Key insight: the tool found issues that a single-prompt review would not have surfaced, because the cross-track synthesis forced contradictions into the open

### IV. Why Structured Evaluation Beats Single-Prompt Feedback

**Purpose:** Make the case for the methodology, not just the tool.

- The parallel-track design prevents anchoring bias — each analytical lens gets full attention without being colored by the others
- The synthesis phase surfaces contradictions that a single-pass review resolves prematurely (or ignores entirely)
- Deliverable output (.docx files) can be shared, forwarded, and referenced — unlike chat responses that live and die in a conversation thread
- The pipeline is transparent and editable — every prompt is in plain markdown, so you know exactly why the tool says what it says
- This isn't about mega-eval specifically; it's about treating product evaluation as a repeatable methodology rather than an ad-hoc conversation

### V. The Honest Limitations

**Purpose:** Preempt the top hater-mode criticisms so the reader knows you've heard them.

- It runs only in Claude Code (for now) — you need to be in that ecosystem
- It takes 10-15 minutes, not 30 seconds — this is a feature (thoroughness) but also a real cost
- The output is text-heavy with no visual artifacts (no positioning maps, no radar charts) — the Designer persona is right about this
- It's AI evaluating with AI — at no point does a human with domain expertise enter the picture (the Late Adopter's concern). This is a tool for structured thinking, not a replacement for advisors
- The methodology is open-source and MIT-licensed — anyone can fork it. The "moat" is in the methodology's quality, not in technical barriers to replication

### VI. How to Use It (The Call to Action)

**Purpose:** Convert interested readers into users.

- Install: 3 commands — clone, copy, run
- First run: paste a product description or URL, wait 10-15 minutes, get 6 docs
- What to do with the output: share the executive summary with your co-founder, use the critical-fixes doc as a sprint backlog, use the content strategy outline to plan your launch post
- Link to the sample output in the repo so they can preview before installing
- Customization: edit the prompts to add industry-specific lenses, change the output format, add evaluation tracks

### VII. Closing — What This Means for How We Build

**Purpose:** Zoom out to the larger point.

- The best critique comes from structured disagreement, not from asking one voice to be balanced
- Open-source evaluation methodologies are more trustworthy than proprietary black boxes — you can verify exactly why the tool says what it says
- Building in public includes being willing to turn your own tools on yourself and ship what they find
- The sample output in the repo is the tool's resume — judge it by its work, not its README

---

## Distribution Notes

**Primary channel:** GitHub README + repo — the sample output directory is the main content marketing asset
**Secondary channels:**
- Hacker News: "Show HN: I built a 6-phase product evaluation pipeline for Claude Code, then evaluated it with itself" — the self-referential angle plays well on HN
- Indie Hackers: focus on the builder journey and the honest-reckoning section
- X/Twitter: thread format — pull the sharpest hater-mode quotes and the synthesis tensions
- Claude Code community (Discord, forums): position as a reference implementation for multi-skill orchestration

**Content format:** Long-form blog post (2,500-3,500 words) with embedded examples from the actual pipeline output. Avoid screenshots of Word docs; use formatted markdown quotes instead.
