# Mega Eval Pipeline Checklist

Use this as a quick reference while running the pipeline. Check off each step as you go.

## Pre-Flight
- [ ] All inputs received (text, docs, URLs)
- [ ] Skill paths resolved for hater-mode, long-form-outline, docx

## Phase 0: Ingestion
- [ ] All inputs parsed and content extracted
- [ ] Evaluation Brief written to `eval-brief.md`
- [ ] Open questions noted (ask user if critical info is missing)

## Phase 1: Parallel Analysis
- [ ] Phase 1A subagent launched (Hater Mode)
- [ ] Phase 1B subagent launched (Competitive & Market)
- [ ] Phase 1C subagent launched (Strengths & Opportunities)
- [ ] All three subagents completed
- [ ] Raw outputs verified: `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, `phase1c-strengths-raw.md`

## Phase 2: Synthesis
- [ ] All Phase 1 outputs read
- [ ] Critical fixes identified and prioritized
- [ ] Design inconsistencies catalogued
- [ ] Non-breaking next steps ordered by effort-to-impact
- [ ] Unresolved tensions documented
- [ ] Output written to `phase2-synthesis.md`

## Phase 3: Content Strategy
- [ ] Subagent launched with long-form-outline skill
- [ ] Output verified: `phase3-content-outline-raw.md`

## Phase 4: Deliverable Assembly
- [ ] `01-hater-mode-feedback.docx` created
- [ ] `02-competitive-landscape.docx` created
- [ ] `03-strengths-opportunities.docx` created
- [ ] `04-critical-fixes-and-design.docx` created
- [ ] `05-content-strategy-outline.docx` created
- [ ] `00-executive-summary.docx` created (LAST — draws from all others)
- [ ] All files saved to workspace output folder
- [ ] All files presented to user with links

## Quality Checks
- [ ] Executive summary is standalone-readable
- [ ] Critical fixes are specific and actionable (not vague)
- [ ] Competitive analysis cites real competitors (not fabricated)
- [ ] Strengths analysis is honest (not cheerleading)
- [ ] Content outline has a clear angle (not generic)
- [ ] All docs note where information was thin or assumptions were made
