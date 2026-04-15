# Live site design audit — output template (Phase 1D)

Use this structure for **`phase1d-design-raw.md`**. This is a **qualitative, heuristic** audit of the **rendered** marketing/product experience — **not** WCAG legal certification, not a substitute for user research.

**Correlation header** (first lines of the saved file):

```markdown
<!-- mega-eval phase1d | run_id: <run_id> | run_log: <path> -->
```

---

## Meta

| Field | Value |
|--------|--------|
| **Audit URL** | [canonical URL audited] |
| **Also attempted** | [other paths, or none] |
| **Classifier** | MARKETING/LANDING \| APP UI \| HYBRID |
| **Evidence tier** | A (browse/screenshots) \| B (fetch/HTML only) \| C (skipped/thin) |
| **Limits** | [auth wall, SPA shell, tool unavailable, rate limit, etc., or none] |

**Disclaimer:** Findings reflect a snapshot in time and one viewport/session unless noted otherwise.

---

## First impression

- **Communicates:** [what the first screen signals — competence, clarity, confusion, …]
- **Notices:** [specific observations, positive or negative]
- **Eye goes to:** [1], [2], [3] — [are these intentional?]
- **One word:** [gut verdict]

---

## Inferred design system (from what’s rendered)

- **Typography:** [families, scale issues, body size, heading hierarchy skips]
- **Color & contrast:** [palette coherence; flag likely contrast risks — heuristic only]
- **Spacing & layout:** [scale vs arbitrary; max width; mobile horizontal scroll if observed]
- **Components:** [CTA clarity, card overuse, decorative noise]

---

## Checklist highlights (sampled)

Cover what you could verify; mark **not observed** where unknown.

- **Hierarchy:** focal point, one primary CTA per view, above-fold clarity
- **Interaction:** hover/focus visible where applicable; touch targets (if mobile width tested)
- **Responsive:** [notes — or not tested]
- **Content / microcopy:** empty states, specificity of labels, placeholder text
- **Motion:** [reduced-motion not assumed; note if unknown]
- **Performance feel:** [LCP/CLS only if measured; else subjective load feel]

---

## AI slop & template tells

Flag any that apply (be direct):

- Generic gradient / purple-blue SaaS palette
- Symmetric 3-column feature grid (icon circle + title + blurb × 3)
- Icons in colored circles as decoration
- Everything centered; uniform large border-radius everywhere
- Decorative blobs / waves with weak content
- Emoji-as-design in hero or bullets
- Colored left border cards
- Generic hero copy (“Unlock the power…”, “All-in-one…”)
- Cookie-cutter section rhythm (same-height sections)

**Verdict:** [e.g. “Reads intentional / Reads template / Mixed”]

---

## Litmus checks (YES/NO)

1. Brand/product unmistakable on first screen?
2. One strong visual anchor?
3. Understandable by scanning headlines only?
4. Each section has one job?
5. Cards only where interaction warrants?
6. Motion (if any) supports hierarchy?
7. Would it feel premium with decorative shadows removed?

---

## Quick wins (3–5)

| # | Fix | Impact | Effort guess |
|---|-----|--------|----------------|
| 1 | … | high/medium/polish | days/weeks |
| 2 | … | | |

---

## Evidence

- **Screenshots / paths:** [list workspace-relative paths, or “none — Tier B/C”]
- **Pages/views covered:** [e.g. homepage + pricing + /login redirect]

---

## Headline for synthesis

**Design risk band:** Low \| Medium \| High (trust/premium/clarity)

**One-line summary:** [for executive summary]
