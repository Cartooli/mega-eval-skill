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

## Malicious / suspicious code signals

Inspect fetched HTML and any **inline or directly linked** JavaScript visible in the tool output. Flag any of the following — each item found should appear as a row in the Findings table with **Remediation needed: Yes** and a short explanatory note.

- **Unexpected external script sources** — `<script src="...">` tags loading from domains unrelated to the product or its known CDN/analytics vendors (especially newly-registered or typosquatted domains)
- **Obfuscated JavaScript** — heavy use of `eval()`, `Function(…)`, `atob()` chains, packed/minified blobs with non-standard variable names (`_0x…`), or hex/unicode escape sequences used to hide readable strings
- **Cryptominer patterns** — `WebWorker` blobs performing arithmetic loops, references to known miner libraries, or sustained CPU-spike indicators in comments
- **Keylogger / form-scraping indicators** — event listeners attached to `document` or `body` for `keydown`/`keypress`/`input` outside of a legitimate form; script tags pointing to known data-harvesting domains
- **Malicious iframes** — zero-size or hidden `<iframe>` tags pointing to third-party origins, especially with `sandbox` removed or `allow="payment"` on unexpected frames
- **Drive-by download triggers** — `window.location` reassignments, auto-download `<a download>` tags, or `navigator.serviceWorker.register` calls pointing to off-origin scripts
- **Suspicious redirect chains** — meta-refresh or JS redirects (`window.location.replace`) to domains not obviously affiliated with the product

### Known-bad domain quick-reference

Cross-check all `<script src>`, `<iframe src>`, and `fetch`/`XHR` target domains against this curated list of confirmed malicious or defunct-but-still-exploited origins. A match is an automatic **Critical** finding.

| Domain / pattern | Category |
|---|---|
| `coinhive.com`, `coin-hive.com`, `authedmine.com` | Cryptominer (Coinhive) |
| `cryptoloot.pro`, `cryptoloot.com` | Cryptominer |
| `jsecoin.com` | Cryptominer |
| `minero.cc`, `webmine.cz`, `miner.pr0gramm.com` | Cryptominer |
| `reasedoper.pw`, `adnxs-simple.com` | Malvertising CDN |
| `cloudfronts.net`, `cloudflare-cdn.com` | Cloudfront/Cloudflare typosquats |
| `stat-count.com`, `statcounters.org` | Statcounter typosquats (data harvesting) |
| `google-analytics.cm`, `googletagmanager.co` | GA/GTM typosquats |

For Tier A (headless browse) runs, cross-reference unfamiliar script domains against public threat-intel feeds:
- [URLhaus](https://urlhaus.abuse.ch/) — abuse.ch URL blocklist (malware distribution)
- [PhishTank](https://www.phishtank.com/) — community phishing URL database
- [Google Safe Browsing Transparency Report](https://transparencyreport.google.com/safe-browsing/search) — domain reputation lookup

**Scope:** Only flag signals visible in the fetched HTML/JS. Do not claim detection of server-side or authenticated-only code. If no suspicious signals are found, write "No malicious/suspicious code signals observed in fetched surface."

### Stub file rule

**If 1 or more malicious/suspicious code signals are found:** write a dedicated `phase1e-malicious-signals.md` alongside the main security file. Put full evidence detail there (exact redacted code snippet, domain, why flagged, severity, step-by-step remediation). In `phase1e-security-raw.md` replace the section body with a one-line reference:

```
⚠ Malicious signals detected — full detail in `phase1e-malicious-signals.md`.
[N] signal(s) found. Highest severity: [Critical | High | Medium].
```

The stub file format is defined in `references/security-audit-template.md` under **Malicious signals stub format** below.

---

## Findings table

| # | Finding | Severity | Remediation needed | Evidence snippet | Suggested direction |
|---|---------|----------|--------------------|------------------|---------------------|
| S1 | … | Low \| Medium \| High \| Critical | Yes \| No | [short quote or describe; redact secrets] | … |
| S2 | … | | | | |

Finding IDs in synthesis: **`[1E-S<n>]`** refers to row **Sn** above (e.g. `[1E-S3]` = finding S3).

---

## Disclaimer

This audit reflects a **point-in-time** snapshot of **public** evidence. It does not replace a professional security assessment, code review, or compliance audit.

---

## Malicious signals stub format

Use this structure for **`phase1e-malicious-signals.md`** — only create this file when 1+ signals were found. Do not create it for a clean run.

```markdown
<!-- mega-eval phase1e malicious-signals | run_id: <run_id> | run_log: <path> -->

# Malicious / Suspicious Code Signals — [Audit URL]

**Highest severity:** Critical | High | Medium
**Signal count:** [N]
**Requires immediate remediation:** Yes

---

## Signal [n]: [Short label]

| Field | Detail |
|---|---|
| **Type** | [Cryptominer \| Obfuscated JS \| Keylogger \| Malicious iframe \| Drive-by download \| Suspicious redirect \| Known-bad domain] |
| **Severity** | Critical \| High \| Medium |
| **Location** | [line/element in HTML, or inline script block] |
| **Remediation needed** | Yes |

**Evidence** (redact secrets/tokens):
```
[exact code snippet — truncate at ~10 lines, replace sensitive values with [REDACTED]]
```

**Why this is suspicious:** [one or two sentences]

**Recommended remediation:**
1. [Step 1]
2. [Step 2]

---

## Remediation checklist

- [ ] Signal 1 — [label] removed / investigated
- [ ] Signal 2 — [label] removed / investigated
- [ ] Full source audit by a qualified security engineer recommended
```

---

## Headline for synthesis

**Security risk band:** Low \| Medium \| High \| Critical

**One-line summary:** [for Phase 2 synthesis and executive summary]
