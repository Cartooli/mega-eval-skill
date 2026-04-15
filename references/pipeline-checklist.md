# Mega Eval Pipeline Checklist

Use this as a quick reference while running the pipeline. Check off each step as you go.

## Pre-Flight
- [ ] **Model fit:** Read `references/model-selection.md`; confirm Phase 2 uses **frontier** tier when available; Phase 1+3 at least **strong general** (or single **frontier** if one knob). Log `model_check` if logging; else note **Model limitation** in brief when host is constrained.
- [ ] All inputs received (text, docs, URLs)
- [ ] Skill paths resolved for hater-mode, long-form-outline, docx (optional: `/cso`, `/durability-review` for 1E/1F — fallback templates apply if unresolved)
- [ ] Design audit: skip Phase 1D if `MEGA_EVAL_DESIGN_AUDIT` is `off` / `0` / `false` (otherwise default **on** when a primary `https://` URL is chosen in Phase 0)
- [ ] Security audit: skip Phase 1E if `MEGA_EVAL_SECURITY_AUDIT` is `off` / `0` / `false` (otherwise default **run** when Phase 0 allows — Tier C if no URL)
- [ ] AI durability audit: skip Phase 1F if `MEGA_EVAL_DURABILITY_AUDIT` is `off` / `0` / `false` (otherwise default **run**; applicability decided in subagent; N/A stub OK)
- [ ] Run logging decision: skip if `MEGA_EVAL_LOG` is `off` / `0`; otherwise plan `run-log.md` path and `run_id`
- [ ] If the workspace already has mega-eval artifacts, inspect them first (for example with `python3 scripts/build_eval_bundle.py <workspace>`) and resume from the first incomplete phase when appropriate

## Phase 0: Ingestion
- [ ] All inputs parsed and content extracted
- [ ] Evaluation Brief written to `eval-brief.md` (includes **Live site / design audit** — primary URL or `n/a`, and run vs skipped)
- [ ] Brief includes **Security audit (Phase 1E)** and **AI durability audit (Phase 1F)** rows (audit decision + 1F AI-surface note or `defer to 1F subagent`)
- [ ] Open questions noted (ask user if critical info is missing)
- [ ] If logging: `run_id` assigned, `run-log.md` initialized, `phase_start phase0` / `phase_complete phase0` appended

## Phase 1: Parallel Analysis
- [ ] Skimmed `references/learnings.md` for applicable methodological bullets (optional)
- [ ] Phase 1A subagent launched (Hater Mode) with `run_id` + `run_log` in prompt
- [ ] Phase 1B subagent launched (Competitive & Market) with `run_id` + `run_log` in prompt
- [ ] Phase 1C subagent launched (Strengths & Opportunities) with `run_id` + `run_log` in prompt
- [ ] Phase 1D subagent launched **only if** brief says **Audit decision: run** (live-site design audit; prompt in `references/subagent-prompts.md`, template `references/design-audit-template.md`)
- [ ] Phase 1E subagent launched **only if** brief says **Audit decision: run** under Security audit (prompt `references/subagent-prompts.md` **Phase 1E**, template `references/security-audit-template.md`)
- [ ] Phase 1F subagent launched **only if** brief says **Audit decision: run** under AI durability audit (prompt **Phase 1F**, template `references/durability-audit-template.md`)
- [ ] Required subagents completed (1A–1C); Phase 1D / 1E / 1F completed **or** logged thin failure — **do not** block Phase 2 on 1D, 1E, or 1F alone
- [ ] Raw outputs verified: `phase1a-hater-raw.md`, `phase1b-competitive-raw.md`, `phase1c-strengths-raw.md` (+ optional `phase1d-design-raw.md`, `phase1e-security-raw.md`, `phase1f-durability-raw.md` when those tracks ran)
- [ ] If logging: Phase 1 events appended (`phase_start` / `phase_complete`, errors/retries as needed)

## Phase 2: Synthesis
- [ ] All Phase 1 outputs read (including `phase1d-design-raw.md` **if present** — authoritative for rendered-site UX vs text-only inference)
- [ ] `phase1e-security-raw.md` read **if present** — merge Critical/High into **Critical Fixes** first with `[1E-S<n>]` tags; dedupe vs 1A (1E authoritative for security specifics)
- [ ] `phase1f-durability-raw.md` read **if present** and not **N/A** — merge Critical/High with `[1F-D<n>]` tags; keep general vendor lock-in in 1B unless AI-specific
- [ ] Critical fixes identified and prioritized
- [ ] Design inconsistencies catalogued (merge Phase 1D quick wins / risk band when applicable; dedupe vs Phase 1A “looks” commentary); **do not** park 1E/1F findings here unless purely visual (rare)
- [ ] Non-breaking next steps ordered by effort-to-impact (include 1E/1F Medium items when present)
- [ ] Unresolved tensions documented (security vs speed, durability vs model-chasing when surfaced)
- [ ] Output written to `phase2-synthesis.md`
- [ ] If logging: `phase2` start/complete (and `user_correction` if user steered synthesis)

## Phase 3: Content Strategy
- [ ] Subagent launched with long-form-outline skill (`run_id` + `run_log` in prompt)
- [ ] Output verified: `phase3-content-outline-raw.md`
- [ ] If logging: Phase 3 start/complete appended

## Phase 4: Deliverable Assembly
- [ ] **Pre-flight:** If logging, reviewed `run-log.md` and reconciled brief/synthesis with corrections
- [ ] Executive summary includes **Live Site / Product Surface** when Phase 1D informed synthesis (see full `SKILL.md`)
- [ ] Executive summary includes optional **Security Posture** when Phase 1E ran with non-stub output, and **AI Durability Posture** when Phase 1F ran with risk band **not** `N/A` (omit AI section entirely when `N/A`)
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
- [ ] Executive summary is standalone-readable (and reflects optional design audit when run)
- [ ] Critical fixes are specific and actionable (not vague)
- [ ] Phase 1E / 1F findings cite **concrete** evidence (URL-visible text, snippet, or tier disclosure) — not pure speculation
- [ ] Competitive analysis cites real competitors (not fabricated)
- [ ] Strengths analysis is honest (not cheerleading)
- [ ] Content outline has a clear angle (not generic)
- [ ] All docs note where information was thin or assumptions were made
