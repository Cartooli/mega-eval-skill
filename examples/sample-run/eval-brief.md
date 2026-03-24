# Evaluation Brief

## Subject
mega-eval — a Claude skill that runs multi-phase product/idea evaluations

## Core Proposition
An open-source Claude Code skill that orchestrates a 6-phase evaluation pipeline, producing 6 structured Word documents covering critical feedback, competitive landscape, strengths, design issues, action items, and content strategy. Designed to replace the "just ask Claude to review my idea" single-prompt approach with a structured, multi-perspective methodology.

## Key Claims & Features
- Accepts any combination of raw text, uploaded documents (.pdf, .docx, .pptx, .txt, .md), and crawlable URLs
- Runs 3 analysis tracks in parallel via subagents (hater-mode critical feedback, competitive/market research, strengths/opportunities)
- Synthesizes findings across tracks to surface cross-cutting issues
- Produces 6 deliverable .docx files including a standalone executive summary
- 10-15 minute autonomous run time
- Customizable prompt templates and pipeline phases
- Falls back to built-in templates if dependent skills aren't installed

## Target Audience (stated or inferred)
- Founders and product managers evaluating ideas before building
- Solo builders who lack a team to pressure-test decisions
- Anyone preparing a pitch, launch, or product strategy who wants structured critical feedback
- Claude Code power users who want reusable evaluation workflows

## Pricing/Model (if known)
Free, open-source (MIT license). No hosted version or paid tier.

## Source Material
- **README.md** (markdown): Project overview, install instructions, usage, dependencies
- **SKILL.md** (markdown): Full pipeline specification — 6 phases, prompt templates, error handling
- **references/pipeline-checklist.md** (markdown): Phase-by-phase QA checklist
- **references/subagent-prompts.md** (markdown): Copy-paste prompt templates for each subagent
- **scripts/ingest.py** (python): Input file extraction helper for local files

## Open Questions
- No sample output exists yet — quality of deliverables is unverified by users
- Dependent skill paths (hater-mode, long-form-outline, docx) link to anthropics/claude-code which may not have these exact paths
- No automated tests or CI
- Single commit, no community usage data
