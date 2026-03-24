# Mega Eval Pipeline Checklist

Use this as a quick reference while running the pipeline. Check off each step as you go.

## Pre-Flight
- [ ] All inputs received (text, docs, URLs)
- [ ] Skill paths resolved for hater-mode, long-form-outline, docx
- [ ] Run logging decision: skip if `MEGA_EVAL_LOG` is `off` / `0`; otherwise plan `run-log.md` path and `run_id`

## Phase 0: Ingestion
- [ ] All inputs parsed and content extracted
- [ ] Evaluation Brief written to `eval-brief.md`
- [ ] Open questions noted (ask user if critical info is missing)
- [ ] If logging: `run_id` assigned, `run-log.md` initialized, `phase_start phase0` / `phase_complete phase0` appended

## Phase 1: Parallel Analysis
- [ ] Skimmed `references/learnings.md` for applicable methodological bullets (optional)
- [ ] Phase 1A subagent launched (Hater Mode) with `run_id` + `run_log` in prompt
- [ ] Phase 1B subagent launched (Competitive & Market) with `run_id` + `run_log` in prompt
- [ ] Phase 1C subagent launched (Strengths & Opportunities) with `run_id` + `run_log` in prompt
- [ ] All three subagents completed
- [ ] Raw outputs verified: `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, `phase1c-strengths-raw.md`
- [ ] If logging: Phase 1 events appended (`phase_start` / `phase_complete`, errors/retries as needed)

## Phase 2: Synthesis
- [ ] All Phase 1 outputs read
- [ ] Critical fixes identified and prioritized
- [ ] Design inconsistencies catalogued
- [ ] Non-breaking next steps ordered by effort-to-impact
- [ ] Unresolved tensions documented
- [ ] Output written to `phase2-synthesis.md`
- [ ] If logging: `phase2` start/complete (and `user_correction` if user steered synthesis)

## Phase 3: Content Strategy
- [ ] Subagent launched with long-form-outline skill (`run_id` + `run_log` in prompt)
- [ ] Output verified: `phase3-content-outline-raw.md`
- [ ] If logging: Phase 3 start/complete appended

## Phase 4: Deliverable Assembly
- [ ] **Pre-flight:** If logging, reviewed `run-log.md` and reconciled brief/synthesis with corrections
- [ ] `01-hater-mode-feedback.docx` created
- [ ] `02-competitive-landscape.docx` created
- [ ] `03-strengths-opportunities.docx` created
- [ ] `04-critical-fixes-and-design.docx` created
- [ ] `05-content-strategy-outline.docx` created
- [ ] `00-executive-summary.docx` created (LAST — draws from all others)
- [ ] All files saved to workspace output folder
- [ ] All files presented to user with links
- [ ] Optional: offered maintainer feedback links (bug / improvement / feature) with `run_id` + redaction reminder — see **Maintainer feedback** in `SKILL.md` Phase 4
- [ ] If logging: `phase4` complete, run `status` set to `complete` or `abandoned`

## Post-run promotion (optional, human-reviewed)
- [ ] Noted any **promotion candidates** in run log (patterns worth adding to `references/learnings.md`)
- [ ] Did **not** promote subject-specific trivia; redacted names/URLs before any shared bullet
- [ ] If promoting: verified [Promotion gates](learnings.md#promotion-gates) in `references/learnings.md`

## Quality Checks
- [ ] Executive summary is standalone-readable
- [ ] Critical fixes are specific and actionable (not vague)
- [ ] Competitive analysis cites real competitors (not fabricated)
- [ ] Strengths analysis is honest (not cheerleading)
- [ ] Content outline has a clear angle (not generic)
- [ ] All docs note where information was thin or assumptions were made
