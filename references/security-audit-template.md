# Security audit — output template (Phase 1E)

Use this structure for **`phase1e-security-raw.md`**. This is a **qualitative, heuristic, observation-only** security posture review from **public** signals — **not** a penetration test, not compliance certification, not guaranteed vulnerability discovery.

When the host’s `/cso` (CSO) skill is installed, the subagent should follow that skill for depth and severity calibration. **This file** remains the **canonical output shape** and the **minimum-viable fallback checklist** when `<cso-skill-path>` is unavailable (`methodology: fallback` in Meta).

**Correlation header** (first lines of the saved file):

```markdown
<!-- mega-eval phase1e | run_id: <run_id> | run_log: <path> -->
```

---

## Meta

| Field | Value |
|--------|--------|
| **Audit URL** | [canonical Primary URL audited] |
| **Also attempted** | [privacy policy URL if one page was opened; else none] |
| **Evidence tier** | A (browse/screenshots) \| B (fetch/HTML only) \| C (skipped/thin) |
| **Methodology** | `external: /cso` \| `fallback: embedded` |
| **Security risk band (confidence)** | Low \| Medium \| High \| Critical — [brief confidence note: what evidence supports this band] |
| **Limits** | [no browser, auth wall, SPA shell, Tier C, etc.] |

**Disclaimer:** Heuristic and observation-only; not a pen-test; not legal/compliance advice.

---

## Transport & headers

- **HTTPS posture** on Primary URL (redirects, mixed-content signals visible in HTML)
- **Obvious missing headers** only if visible via fetch/tool output (do not claim full header audit without evidence)

---

## Auth & session surface

- Signup/login **copy**, MFA claims, session wording **observable without login**
- Cookie names/flags **only** if visible in tool output (no guessing)

---

## Privacy & data handling

- Marketing claims vs **observable** third-party scripts/trackers on Primary URL
- **Privacy policy cross-check** (if one policy page was opened): retention, subprocessors, AI data use — quote short snippets

---

## LLM / AI exposure

- Prompt-injection or untrusted user content → model pathways **as inferable from public copy**
- Data retention / training claims for AI features
- **Skip this section** if there is clearly no AI surface

---

## Red flags

- Secrets in URLs, tokens in client-visible HTML/JS snippets (redact in place)
- Leaky share links, obvious auth anti-patterns in markup

---

## Findings table

| # | Finding | Severity | Evidence snippet | Suggested direction |
|---|---------|----------|------------------|---------------------|
| S1 | … | Low \| Medium \| High \| Critical | [short quote or describe; redact secrets] | … |
| S2 | … | | | |

Finding IDs in synthesis: **`[1E-S<n>]`** refers to row **Sn** above (e.g. `[1E-S3]` = finding S3).

---

## Disclaimer

This audit reflects a **point-in-time** snapshot of **public** evidence. It does not replace a professional security assessment, code review, or compliance audit.

---

## Headline for synthesis

**Security risk band:** Low \| Medium \| High \| Critical

**One-line summary:** [for Phase 2 synthesis and executive summary]
