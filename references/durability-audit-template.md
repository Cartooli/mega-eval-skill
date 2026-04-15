# AI / agent durability audit — output template (Phase 1F)

Use this structure for **`phase1f-durability-raw.md`**. This assesses **resilience of the subject’s AI/agent surface** to model/API/provider **change** — not general corporate vendor concentration (that belongs in Phase 1B unless genuinely tied to AI dependency).

When the host’s `/durability-review` skill is installed, the subagent should align framing with that methodology. **This file** is the **canonical output shape** and the **fallback checklist** when `<durability-review-skill-path>` is unavailable (`methodology: fallback` in Meta).

**Correlation header** (first lines of the saved file):

```markdown
<!-- mega-eval phase1f | run_id: <run_id> | run_log: <path> -->
```

---

## N/A stub protocol (no meaningful AI surface)

If **no** meaningful AI, LLM, or agent surface is present on public evidence, output **only**:

```markdown
<!-- mega-eval phase1f | run_id: <run_id> | run_log: <path> -->

## Meta

| Field | Value |
|--------|--------|
| **Audit URL** | [Primary URL or n/a] |
| **Evidence tier** | A \| B \| C |
| **Methodology** | `external: /durability-review` \| `fallback: embedded` |
| **AI surface present** | no |
| **AI durability risk band** | N/A |

## Applicability

[One short paragraph: why AI/agent durability does not apply — no padded filler.]

## Headline for synthesis

**AI durability risk band:** N/A

**One-line summary:** [e.g. "No public AI/agent surface observed for this subject."]
```

Then **stop** — do not fabricate findings.

---

## Meta (full audit — AI surface present)

| Field | Value |
|--------|--------|
| **Audit URL** | [canonical Primary URL] |
| **Evidence tier** | A \| B \| C |
| **Methodology** | `external: /durability-review` \| `fallback: embedded` |
| **AI surface present** | yes |
| **Limits** | [fetch-only, thin HTML, etc.] |

**Disclaimer:** Public-surface signals only; not a substitute for architecture review of private code.

---

## Model abstraction

- Locked to one model family vs portable positioning (from marketing/docs)
- Version pinning language vs “latest model” dependency

---

## Prompt architecture signals

- Fragile model-specific claims; reliance on provider-specific tool-use or proprietary features as differentiators

---

## Provider concentration

- Single-vendor AI dependency; pricing/availability fragility **for AI workloads** (keep distinct from generic SaaS lock-in unless AI-specific)

---

## Capability drift risk

- Claims that assume today’s model capabilities will hold indefinitely

---

## Evals / feedback loop presence

- Public signals of monitoring quality across model changes (eval hooks, changelogs, safety pages) — only if observable

---

## Findings table

| # | Finding | Severity | Evidence snippet | Suggested direction |
|---|---------|----------|------------------|---------------------|
| D1 | … | Low \| Medium \| High \| Critical | … | … |

Synthesis tags: **`[1F-D<n>]`** = row D*n* (e.g. `[1F-D2]`).

---

## Disclaimer

This audit is **not** a code-level durability score; it reflects **public** evidence and heuristics. Private architecture may differ.

---

## Headline for synthesis

**AI durability risk band:** Low \| Medium \| High \| Critical

**One-line summary:** [for Phase 2 synthesis and executive summary]
