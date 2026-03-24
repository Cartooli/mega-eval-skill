# mega-eval

A Claude skill that runs a comprehensive, multi-phase evaluation of any idea, product, or feature set. Feed it text, docs, URLs, or any combination — it produces 6 structured Word documents covering critical feedback, competitive landscape, strengths, design issues, action items, and content strategy.

## What it does

```
INPUT (text / doc / URL / combo)
     │
     ▼
Phase 0: Ingest & normalize all inputs into an Evaluation Brief
     │
     ├── Phase 1A: Hater Mode (12-persona critical feedback)
     ├── Phase 1B: Competitive & Market Landscape (web research)
     └── Phase 1C: Strengths & Opportunities
            │
            ▼
Phase 2: Synthesis — critical fixes, design issues, next steps
     │
     ▼
Phase 3: Content Strategy Outline
     │
     ▼
Phase 4: Assemble 6 deliverable .docx files
```

### Deliverables

| File | Contents |
|------|----------|
| `00-executive-summary.docx` | Standalone decision-maker document with verdict, top findings, and prioritized actions |
| `01-hater-mode-feedback.docx` | Simulated critical feedback from 12 internet audience personas |
| `02-competitive-landscape.docx` | Competitors, market size, positioning analysis, risks |
| `03-strengths-opportunities.docx` | What's working, growth angles, unfair advantages, ideal customer profiles |
| `04-critical-fixes-and-design.docx` | Prioritized fixes, design inconsistencies, non-breaking next steps |
| `05-content-strategy-outline.docx` | Long-form outline for publicly positioning/pitching the idea |

## Where it runs, privacy, and local files

- **Host environment:** Mega-eval targets **Claude Code** (skills + **hater-mode**, **long-form-outline**, **docx**, and parallel subagents). Other Claude apps or agents may run the steps **partially** or need you to follow `SKILL.md` by hand—do not assume identical behavior.
- **Sensitive data:** You may pass URLs, pitch text, or confidential documents into the pipeline. Treat generated `.docx` files, raw markdown intermediates, and optional **`run-log.md`** as **sensitive** unless you redact them. To skip writing a run log, set `MEGA_EVAL_LOG=off` (see [Run feedback](#run-feedback-optional)).
- **PDF / Office inputs:** Extracting text from local `.pdf`, `.docx`, or `.pptx` via `scripts/ingest.py` requires **pdftotext** and **pandoc** ([optional tools](#optional-system-tools) below). Plain text, Markdown, pasted content, and many URLs work without them.

## Install

### Claude Code (CLI)

Copy the skill folder into your project:

```bash
# Clone this repo
git clone https://github.com/Cartooli/mega-eval-skill.git

# Copy into your Claude Code skills directory (include the whole references/ folder for learnings + prompts)
cp -r mega-eval-skill/SKILL.md mega-eval-skill/references mega-eval-skill/scripts ~/.claude/skills/mega-eval/
```

Or if you prefer, copy just the skill folder contents into any `.claude/skills/mega-eval/` directory in your project.

### Cowork (Desktop app)

If a **`mega-eval.skill`** bundle is available (e.g. from a project release or attachment), open it in Cowork and use **Copy to your skills**. **The repo root may not include a `.skill` file**—in that case install the same **`SKILL.md` + `references/` + `scripts/`** folder your app expects, using the layout under [Manual install](#manual-install).

### Manual install

The skill is just a folder with this structure:

```
mega-eval/
├── SKILL.md              # Main skill instructions
├── references/
│   ├── pipeline-checklist.md    # Phase-by-phase checklist
│   ├── subagent-prompts.md      # Ready-to-use prompt templates
│   └── learnings.md             # Human-reviewed methodology patterns (from run feedback)
└── scripts/
    ├── ingest.py                  # Input file extraction helper
    └── suggest_learnings.py       # Optional: print promotion candidates from run-log (stdout only)
```

At the **repository root** (when you clone this repo), see [`MAINTAINERS.md`](MAINTAINERS.md) for how to review and promote learnings over time.

Copy that folder into wherever your Claude instance reads skills from.

## Prerequisites

### Required skills

The pipeline orchestrates these Claude skills — install them before running:

- **hater-mode** — Phase 1A critical feedback (12-persona teardown). Ships with Claude Code as a built-in skill.
- **long-form-outline** — Phase 3 content strategy outline. Ships with Claude Code as a built-in skill.
- **docx** — Phase 4 Word document assembly. Ships with Claude Code as a built-in skill.

These are available out of the box in Claude Code. If they're missing from your environment for any reason, the skill will still run using built-in prompt templates, but output quality will be lower.

### Optional system tools

**Required only** when you want `scripts/ingest.py` to read **local** `.pdf`, `.docx`, or `.pptx` files:

- **pdftotext** (poppler) — `.pdf` extraction. Example: `brew install poppler`
- **pandoc** — `.docx` and `.pptx` extraction. Example: `brew install pandoc`

Without these tools, use plain text, Markdown, pasted content, or URLs instead—or extract text another way before running mega-eval.

## Usage

Once installed, trigger it with prompts like:

- `"mega eval [paste your idea]"`
- `"full evaluation of https://example.com/product"`
- `"comprehensive review"` + attach a document
- `"assess this feature set"` + describe it

It accepts any combination of:
- Raw text blocks
- Uploaded documents (`.pdf`, `.docx`, `.pptx`, `.txt`, `.md`)
- Crawlable URLs

The pipeline runs autonomously. Expect ~10-15 minutes for a full run. It parallelizes where possible (Phase 1 tracks run simultaneously) and sequences where judgment is needed (Phase 2 synthesis).

## Example output

The [`examples/sample-run/`](examples/sample-run/) directory contains a complete pipeline run where mega-eval evaluated itself. Every file was generated by the pipeline — nothing was hand-edited.

**What the self-evaluation found:**
- The #1 criticism across all 12 hater personas: "Show the output" — which this example now addresses
- No existing competitor combines adversarial critique + competitive research + strengths analysis + synthesis in a single free pipeline
- The cross-track synthesis surfaced genuine tensions (e.g., "it's just a prompt" vs. "the methodology is the moat") that a single-prompt review would have glossed over
- Concrete fixes: duplicate README sections, unvalidated links, missing audience clarity

Browse the `.docx` files to see what the pipeline produces, or read the raw `.md` intermediates for the unformatted analysis.

## Run feedback (optional)

Mega-eval can write an **append-only** `run-log.md` during a run so you can capture tool errors, retries, and user corrections—not for model training, but to **promote** stable methodology fixes into `references/learnings.md` after human review.

- **Disable logging:** set `MEGA_EVAL_LOG=off` or `MEGA_EVAL_LOG=0` in the environment before running.
- **Privacy:** Logs are **workspace-local** by default. Redact secrets before sharing or promoting bullets.
- **Examples:** See [`examples/run-feedback/`](examples/run-feedback/) for fictional `run-log` and promotion samples.

This is **not** automatic self-modification of prompts; see promotion gates in `references/learnings.md`.

**Sustaining the loop:** If you clone or maintain this repo, use **[`MAINTAINERS.md`](MAINTAINERS.md)** for the review ritual (at least **monthly** plus a quick pass on **merge to default branch** when `SKILL.md`, `references/`, or `examples/` change), redaction rules, and the optional `scripts/suggest_learnings.py` helper (stdout only).

## Reporting issues and ideas

**GitHub Issues** (this repo): use the **[bug](https://github.com/Cartooli/mega-eval-skill/issues/new?template=bug-report.md)**, **[improvement](https://github.com/Cartooli/mega-eval-skill/issues/new?template=improvement.md)**, or **[feature request](https://github.com/Cartooli/mega-eval-skill/issues/new?template=feature-request.md)** template. **Browse:** [Issues](https://github.com/Cartooli/mega-eval-skill/issues).

When you file from a run, include **`run_id`** when you have it (see Phase 4 **Maintainer feedback** in `SKILL.md`).

**Run feedback** (`run-log.md` → promotion to `references/learnings.md`) is separate from GitHub Issues; see [Run feedback](#run-feedback-optional) above and [`MAINTAINERS.md`](MAINTAINERS.md).

## Customization

The `references/subagent-prompts.md` file contains the exact prompts sent to each parallel analysis track. Edit these to adjust the evaluation dimensions, add new tracks, or change the focus areas.

The `references/learnings.md` file is for **curated** methodological lessons promoted from run logs.

The `SKILL.md` file controls the overall pipeline flow. You can reorder phases, skip phases, or add new ones.

## License

MIT
