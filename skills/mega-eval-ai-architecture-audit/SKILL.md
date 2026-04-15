---
name: mega-eval-ai-architecture-audit
description: "Audit an AI system, agent, or skill-based tool against the 'thin harness, fat skills' architecture — scoring skill quality, harness minimalism, resolver discipline, latent-vs-deterministic separation, and compounding-loop maturity. Use this when the evaluation subject is an AI product, agent framework, prompt system, LLM application, Claude skill, or any tool that wraps a language model. Trigger on: 'architecture audit', 'AI architecture review', 'skill system review', 'agent framework audit', 'audit this agent', 'is this skill well-designed', 'review our prompt system', 'thin harness fat skills', 'LLM architecture check', or when mega-eval is run on a subject whose core is an LLM/agent system. Produces a scored rubric plus a prioritized remediation list."
---

# AI Architecture Audit Lens

Apply the **Skills think. Tools execute. Harness orchestrates. Resolver decides.** mental model to a subject and produce a scored, evidence-backed audit.

This lens is designed for **Phase 1D** of the mega-eval pipeline (optional — runs only when the subject is an AI system / agent framework / skill tool). It can also run **standalone** against any repo, prompt system, or agent platform.

## When to Use

- **Inside mega-eval:** Spawned as a Phase 1D subagent whenever the Evaluation Brief's subject is an AI product, agent, LLM app, or skill framework. Skip this lens for non-AI subjects.
- **Standalone:** User asks you to audit an AI system's architecture, review a skill system, or check whether a codebase follows the thin-harness/fat-skills pattern.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Evaluation Brief (or raw subject description) | Yes | What the subject is, what it does, what surface it presents |
| Repo / code access | Preferred | File tree, key files (harness, skills, tools, context-loading code) |
| Prompt / skill artifacts | Preferred | The actual skill files, system prompts, tool definitions |
| Run logs or transcripts | Optional | Evidence of how the system behaves under real use |

If repo access is not available, audit on *claimed* architecture from docs/brief and flag every inferred score with `confidence: low`.

## The Six-Axis Rubric

Score each axis **0–5**. Cite concrete evidence (file paths, LOC counts, prompt excerpts) — no generic criticism.

### Axis 1 — Fat Skills

**What good looks like:** Skills are markdown "programs" that encode process, judgment, and reusable workflows. Parameterized. Composable. Same skill produces radically different outputs on different inputs.

| Score | Signal |
|-------|--------|
| 5 | Skills are parameterized, versioned, referenced from multiple entry points, encode domain judgment, and improve via feedback loop |
| 4 | Clear skill files with process + checklist; some parameterization |
| 3 | Skill files exist but are thin — mostly one-shot prompts |
| 2 | Inline prompts; no reusable skill abstraction |
| 1 | Skills are just wrappers around a single model call with no encoded process |
| 0 | No skill concept; monolithic prompt dumped into model |

Evidence to cite: skill file paths, line counts of process vs boilerplate, whether skills reference shared `references/` material.

### Axis 2 — Thin Harness

**What good looks like:** Harness does only 4 things — run model loop, read/write files, manage context, enforce safety. Small (ideally ~200 LOC of orchestration). Minimal tool surface.

| Score | Signal |
|-------|--------|
| 5 | Harness <300 LOC of orchestration, <8 tools, no business logic, no domain knowledge |
| 4 | Small harness with minor bloat |
| 3 | Harness mixes orchestration with some domain logic |
| 2 | Harness carries substantial business logic or has 15+ tools |
| 1 | Harness is where "intelligence" lives — skills/tools are afterthoughts |
| 0 | No harness/skills split; everything in one runtime |

Evidence to cite: harness LOC, tool count, where domain decisions live.

### Axis 3 — Resolver Discipline (context routing)

**What good looks like:** The right information is loaded at the right time. Mega-prompts are replaced with on-demand context. Explicit resolver layer decides what the model sees.

| Score | Signal |
|-------|--------|
| 5 | Explicit resolver / retrieval layer; context assembled per-step; no dumping |
| 4 | Context loading is layered (system + task + artifact) with pruning |
| 3 | Some dynamic context; still relies on a large static preamble |
| 2 | Mostly static mega-prompt with occasional injection |
| 1 | Everything dumped into context every turn |
| 0 | No context management; runs until the window blows |

Evidence to cite: prompt size distribution, retrieval triggers, context packing strategy.

### Axis 4 — Latent vs Deterministic Separation

**What good looks like:** LLM is used only for judgment, synthesis, reasoning. Math, queries, execution go to deterministic tools. No "ask the model to count tokens" anti-patterns.

| Score | Signal |
|-------|--------|
| 5 | Clear split; deterministic tools handle math/queries/IO; LLM only reasons |
| 4 | Mostly correct split with a few judgment calls that could be deterministic |
| 3 | LLM does some exact work (counting, date math, parsing) that should be deterministic |
| 2 | LLM routinely does work a script could do reliably |
| 1 | LLM is the execution engine; tools are decorative |
| 0 | No split; LLM generates SQL/shell and runs it unchecked |

Evidence to cite: specific tool names, places where LLM does arithmetic/exact matching, database/API access patterns.

### Axis 5 — Compounding Loop

**What good looks like:** System improves itself. Outputs analyzed → skill files updated → next run is measurably better. Human-gated promotion (not silent self-modification).

| Score | Signal |
|-------|--------|
| 5 | Explicit feedback loop (run logs → promotion gates → learnings) with human review |
| 4 | Run logs captured; periodic manual review cadence |
| 3 | Some logging; no promotion process |
| 2 | Ad-hoc "lessons learned" in README |
| 1 | No feedback loop; each run is isolated |
| 0 | System silently self-modifies prompts (anti-pattern — governance risk) |

Evidence to cite: presence of run-log, promotion rules, cadence, `learnings.md`-equivalent, review ritual docs.

### Axis 6 — Diarization (multi-source synthesis)

**What good looks like:** System reads many sources, produces structured judgment, detects contradictions, preserves provenance. This is the hidden superpower for real knowledge work.

| Score | Signal |
|-------|--------|
| 5 | Multi-source ingestion, structured synthesis output, contradiction detection, source attribution |
| 4 | Multi-source with attribution but no contradiction detection |
| 3 | Multi-source but outputs a blended narrative without provenance |
| 2 | Single-source focus; synthesis is narrow |
| 1 | No synthesis — just pass-through summarization |
| 0 | Not applicable / not attempted (cite "N/A" — don't score 0 falsely) |

Evidence to cite: ingestion surface, attribution in outputs, contradiction handling.

## Anti-Pattern Scan (flag any that apply)

Scan for these explicitly — each one found subtracts 0.5 from the relevant axis score (floor at 0):

- **Overbuilt harness** — 1000+ LOC of orchestration
- **Tool sprawl** — 20+ tools where 6 would do
- **Mega-prompt** — system prompt > 8k tokens with everything in it
- **LLM-as-calculator** — model doing arithmetic/counting in prod
- **LLM-generated SQL executed unchecked** — injection + correctness risk
- **Silent self-modification** — model rewrites its own prompts with no human review
- **Skill-as-task** — "skill" is actually a one-off task, not a reusable process
- **No resolver** — entire context is static, grows with conversation length
- **No deterministic checks** — LLM's output trusted without eval_plan validation
- **One-shot everything** — no pattern of turning repeated work into reusable skills

## Output Format

Save to `<workspace>/phase1d-architecture-audit-raw.md` (or print if standalone).

```markdown
# AI Architecture Audit — <Subject>

**Run ID:** <run_id>
**Confidence:** <high | medium | low>  (based on artifact access)
**Overall score:** <sum of 6 axes> / 30

## Scorecard

| Axis | Score | Confidence | Key evidence |
|------|-------|------------|--------------|
| 1. Fat Skills | x/5 | h/m/l | file:line or prompt excerpt |
| 2. Thin Harness | x/5 | h/m/l | ... |
| 3. Resolver Discipline | x/5 | h/m/l | ... |
| 4. Latent vs Deterministic | x/5 | h/m/l | ... |
| 5. Compounding Loop | x/5 | h/m/l | ... |
| 6. Diarization | x/5 or N/A | h/m/l | ... |

## Per-Axis Findings

### Axis 1 — Fat Skills (score: x/5)
**Evidence:**
- [specific file/line]
- [specific pattern]

**What's working:** [concrete]
**What's missing:** [concrete]
**Top fix:** [1 action, 1 sentence]

### Axis 2 — Thin Harness (score: x/5)
[...same structure...]

### Axis 3 — Resolver Discipline (score: x/5)
[...]

### Axis 4 — Latent vs Deterministic (score: x/5)
[...]

### Axis 5 — Compounding Loop (score: x/5)
[...]

### Axis 6 — Diarization (score: x/5 or N/A)
[...]

## Anti-Patterns Detected

- [ ] Overbuilt harness
- [ ] Tool sprawl
- [ ] Mega-prompt
- [ ] LLM-as-calculator
- [ ] LLM-generated SQL executed unchecked
- [ ] Silent self-modification
- [ ] Skill-as-task
- [ ] No resolver
- [ ] No deterministic checks
- [ ] One-shot everything

For each checked item, cite evidence in one line.

## Prioritized Remediation List

Ordered by impact-to-effort ratio:

1. **[Quick win — days]** [action]  — addresses Axis <n>, anti-pattern <name>
2. **[Medium — weeks]** [action] — addresses Axis <n>
3. **[Strategic — months]** [action] — addresses Axis <n>

## Unresolved Questions

- [Things you could not score without more access — name exact artifact needed]
```

## Procedure

1. **Read the Evaluation Brief** (or raw subject description).
2. **Decide applicability.** If the subject is not an AI/LLM/agent system, output a single-line `N/A — subject is not an AI system` and exit. Do not score.
3. **Collect evidence.** Prefer repo access. If absent, use docs/brief and set confidence accordingly.
4. **Score each axis** with at least one cited piece of evidence per axis. No evidence → score is `unknown` (not 0).
5. **Run the anti-pattern scan.** Flag each that applies.
6. **Write the output** using the format above. Be specific — "the harness has 1,847 LOC and 23 tools" beats "harness is bloated."
7. **If logging is enabled** (mega-eval run), append `phase_start phase1d` / `phase_complete phase1d` / `failure_mode` events to `run-log.md`.

## Failure Modes to Avoid

- **Cheerleading or trashing.** Score honestly. Anchor every axis to cited evidence.
- **Scoring 0 for missing info.** Use `unknown` or `N/A` — zero is for *bad*, not *absent*.
- **Generic advice.** "Use fewer tools" is useless; "remove tools `foo`, `bar`, `baz` — they duplicate `qux`" is a fix.
- **Auditing the wrong layer.** The model is not the subject. The system around the model is.
- **Scope creep into product review.** If the brief is a full mega-eval, stay in your lane — product-market and UX critique belong in other phases (1A / 1B / 1C).

## Mental Model (always)

> Skills think. Tools execute. Harness orchestrates. Resolver decides.

If the subject violates this split, name where and how.
