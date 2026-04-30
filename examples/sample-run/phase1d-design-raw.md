## Meta
| Field | Value |
|--------|--------|
| **Audit URL** | https://github.com/Cartooli/mega-eval-skill |
| **Also attempted** | none |
| **Classifier** | DOCS / REPO README |
| **Evidence tier** | B (HTML/text via fetch; not a marketing landing) |
| **Limits** | Primary surface is documentation, not a full product UI |

**Disclaimer:** This audit treats the public GitHub README and repo chrome as the “product surface” for mega-eval itself — appropriate for an OSS skill whose storefront is docs and examples.

## First impression
- **Communicates:** methodology-heavy evaluation pipeline with clear install paths and artifact contracts
- **Notices:** dense README optimized for practitioners; light visual branding by nature of GitHub
- **Eye goes to:** deliverables table and install commands before narrative context
- **One word:** capable

## Inferred design system
- **Typography:** GitHub system fonts and markdown hierarchy (not custom brand typography)
- **Color & contrast:** platform defaults; code blocks and tables readable in light theme
- **Spacing & layout:** standard GitHub markdown stack; long-scroll documentation pattern
- **Components:** headings, tables, fenced code — few bespoke UI components on this surface

## Checklist highlights
- **Hierarchy:** README sections progress install → usage → validation → customization sensibly
- **Interaction:** links to schemas, scripts, and examples support verification-minded readers
- **Responsive:** inherits GitHub mobile layout; tables may wrap hard on narrow viewports
- **Content / microcopy:** precise technical wording; assumes Claude Code familiarity
- **Motion:** none meaningful on static README
- **Performance feel:** determined by GitHub delivery, not mega-eval

## AI slop & template tells
Repository presents as earnest OSS documentation rather than a generic SaaS landing; limited opportunity for “AI template” tells on this tier.

**Verdict:** Acceptable — honesty about constraints matches the pipeline’s methodology.

## Litmus checks (YES/NO)
1. Brand/product unmistakable on first screen? YES (skill name and purpose in title area)
2. One strong visual anchor? NO (GitHub chrome dominates)
3. Understandable by scanning headlines only? MOSTLY
4. Each section has one job? MOSTLY
5. Cards only where interaction warrants? N/A (no marketing cards)
6. Motion (if any) supports hierarchy? N/A
7. Would it feel premium with decorative shadows removed? N/A

## Quick wins (3–5)
| # | Fix | Impact | Effort guess |
|---|-----|--------|----------------|
| 1 | Add a single hero diagram or screenshot of deliverables in README | high | hours |
| 2 | Link artifact validation commands in one copy-paste block | medium | minutes |
| 3 | Surface “time to first eval” estimate earlier for busy readers | medium | minutes |

## Evidence
- **Screenshots / paths:** Tier B — README markdown and repo metadata as fetched HTML-equivalent text
- **Pages/views covered:** default branch README view as primary URL proxy for mega-eval’s public face

## Headline for synthesis
**Design risk band:** Low–Medium

**One-line summary:** The public surface is documentation-forward on GitHub rather than a polished marketing site; visual differentiation is minimal but acceptable for the audience.
