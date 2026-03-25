# mega-eval

A Claude skill that runs a comprehensive, multi-phase evaluation of any idea, product, or feature set. Feed it text, docs, URLs, or any combination — it produces 6 structured Word documents covering critical feedback, competitive landscape, strengths, design issues, action items, and content strategy. When a **primary HTTPS site URL** is in scope, it can also run an **optional Phase 1D live-site design audit** (report-only markdown); set `MEGA_EVAL_DESIGN_AUDIT=off` to skip.

## What it does

```
INPUT (text / doc / URL / combo)
     │
     ▼
Phase 0: Ingest & normalize all inputs into an Evaluation Brief
     │
     ├── Phase 1A: Hater Mode (12-persona critical feedback)
     ├── Phase 1B: Competitive & Market Landscape (web research)
     ├── Phase 1C: Strengths & Opportunities
     └── Phase 1D: Live-site design audit (optional, when URL in scope)
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

### Claude Code plugin install (recommended)

> **Requires:** Claude Code 1.0.33 or later. Run `claude --version` to check.
>
> **Security note:** Only add marketplaces from sources you trust — plugins run with your user privileges.

Install the full pipeline and all phase skills via the Claude Code plugin system:

```shell
# Step 1 — register the marketplace (use owner/repo, NOT a raw URL)
/plugin marketplace add Cartooli/mega-eval-skill

# Step 2 — install the plugin
/plugin install mega-eval@cartooli

# Step 3 — activate without restarting
/reload-plugins
```

That installs the **full pipeline skill** (`mega-eval`) plus all **eight phase-only skills** (`mega-eval-brief`, `mega-eval-competitive`, `mega-eval-design`, etc.) in one shot.

**Why Git-based add (`owner/repo`) and not a direct URL?** The plugin tree uses relative paths to a shared `references/` directory. Relative paths only resolve when the marketplace is added via Git — a direct URL to the raw `marketplace.json` file cannot resolve them. Always use the `owner/repo` or `git URL` form.

**Plugin not appearing after install?** Run `/reload-plugins` first. If still missing, clear the cache and reinstall:

```shell
rm -rf ~/.claude/plugins/cache
# then re-run /plugin marketplace add ... and /plugin install ...
```

**Manage the marketplace:**

```shell
/plugin marketplace update cartooli   # pull latest version
/plugin marketplace remove cartooli   # remove marketplace + uninstalls its plugins
/plugin uninstall mega-eval@cartooli  # uninstall plugin only
```

> Third-party marketplaces (like this one) have **auto-update disabled by default.** Run `/plugin marketplace update cartooli` after new releases, or enable auto-update in the plugin UI (`/plugin` → Marketplaces → cartooli → Enable auto-update).

---

### Full pipeline only (`mega-eval`)

Copy the skill folder into your project:

```bash
# Clone this repo
git clone https://github.com/Cartooli/mega-eval-skill.git

# Copy into your Claude Code skills directory (include the whole references/ folder for learnings + prompts)
cp -r mega-eval-skill/SKILL.md mega-eval-skill/references mega-eval-skill/scripts ~/.claude/skills/mega-eval/
```

Or if you prefer, copy just the skill folder contents into any `.claude/skills/mega-eval/` directory in your project.

### Phase-only skills (thin entrypoints)

The repo includes **eight** additional skills under [`skills/`](skills/) — phases 0, 1A, 1B, 1C, optional **1D** (design audit), 2, 3, and 4 — so you can pick **e.g. competitive only** or **brief only** from the skill picker. Methodology is **not** duplicated: each thin `SKILL.md` points at the shared [`references/`](references/) folder and the [full `SKILL.md`](SKILL.md).

| Skill folder | Use when you want |
|--------------|-------------------|
| [`skills/mega-eval-brief`](skills/mega-eval-brief) | Phase 0 only → `eval-brief.md` |
| [`skills/mega-eval-hater`](skills/mega-eval-hater) | Phase 1A only → `phase1a-hater-raw.md` |
| [`skills/mega-eval-competitive`](skills/mega-eval-competitive) | Phase 1B only → `phase1b-competitive-raw.md` |
| [`skills/mega-eval-strengths`](skills/mega-eval-strengths) | Phase 1C only → `phase1c-strengths-raw.md` |
| [`skills/mega-eval-design`](skills/mega-eval-design) | Phase 1D only → `phase1d-design-raw.md` (live-site UX audit) |
| [`skills/mega-eval-synthesis`](skills/mega-eval-synthesis) | Phase 2 only → `phase2-synthesis.md` |
| [`skills/mega-eval-content-outline`](skills/mega-eval-content-outline) | Phase 3 only → `phase3-content-outline-raw.md` |
| [`skills/mega-eval-deliverables`](skills/mega-eval-deliverables) | Phase 4 only → `.docx` assembly |

**Path resolution:** Thin skills load `references/` from the first path that exists (see [skills/README.md](skills/README.md)): `./references/` next to the phase `SKILL.md`, `../../references/` when the whole **mega-eval-skill** repo is present, or `../mega-eval/references/` when the phase skill is a sibling of the full **`mega-eval`** folder.

**Install one phase skill (portable):** copy the phase folder **and** `references/` into the same install directory so `./references/` resolves:

```bash
git clone https://github.com/Cartooli/mega-eval-skill.git
mkdir -p ~/.claude/skills/mega-eval-competitive
cp mega-eval-skill/skills/mega-eval-competitive/SKILL.md ~/.claude/skills/mega-eval-competitive/
cp -r mega-eval-skill/references ~/.claude/skills/mega-eval-competitive/references
```

**Install from a full clone:** work inside `mega-eval-skill/` so `skills/<name>/SKILL.md` can resolve `../../references/` without copying.

**Install next to the full `mega-eval` package:** put `~/.claude/skills/mega-eval-brief/SKILL.md` (etc.) beside `~/.claude/skills/mega-eval/references/` and use `../mega-eval/references/` per [skills/README.md](skills/README.md).

Without **`references/`** (or a valid sibling / monorepo path), thin skills cannot load prompt templates and checklists.

See **[skills/README.md](skills/README.md)** for path resolution order and artifact names.

### Cowork (Desktop app)

If a **`mega-eval.skill`** bundle is available (e.g. from a project release or attachment), open it in Cowork and use **Copy to your skills**. **The repo root may not include a `.skill` file**—in that case install the same **`SKILL.md` + `references/` + `scripts/`** folder your app expects, using the layout under [Manual install](#manual-install).

### Manual install

The repository layout:

```
mega-eval-skill/
├── SKILL.md                 # Full pipeline skill (mega-eval)
├── references/
│   ├── pipeline-checklist.md
│   ├── subagent-prompts.md
│   └── learnings.md
├── scripts/
│   ├── ingest.py
│   └── suggest_learnings.py
└── skills/                  # Thin phase-only skills (see "Phase-only skills" above)
    ├── README.md
    ├── mega-eval-brief/
    ├── mega-eval-hater/
    ├── mega-eval-competitive/
    ├── mega-eval-strengths/
    ├── mega-eval-synthesis/
    ├── mega-eval-content-outline/
    └── mega-eval-deliverables/
```

The **single** `mega-eval` install folder (what you copy to `~/.claude/skills/mega-eval/`) is:

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

Once installed, trigger the **full** skill with prompts like:

- `"mega eval [paste your idea]"`
- `"full evaluation of https://example.com/product"`
- `"comprehensive review"` + attach a document
- `"assess this feature set"` + describe it

For **one phase only**, install the matching skill from [`skills/`](skills/) (see [Phase-only skills](#phase-only-skills-thin-entrypoints)) and invoke it by name, e.g. competitive-only analysis after you have an `eval-brief.md`, or deliverable assembly when markdown phases already exist.

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
- **Disable optional design audit:** set `MEGA_EVAL_DESIGN_AUDIT=off` or `MEGA_EVAL_DESIGN_AUDIT=0` to skip Phase 1D even when an HTTPS URL is present (see `SKILL.md` Phase 0).
- **Privacy:** Logs are **workspace-local** by default. Redact secrets before sharing or promoting bullets.
- **Examples:** See [`examples/run-feedback/`](examples/run-feedback/) for fictional `run-log` and promotion samples.

This is **not** automatic self-modification of prompts; see promotion gates in `references/learnings.md`.

**Sustaining the loop:** If you clone or maintain this repo, use **[`MAINTAINERS.md`](MAINTAINERS.md)** for the review ritual (at least **monthly** plus a quick pass on **merge to default branch** when `SKILL.md`, `references/`, or `examples/` change), redaction rules, and the optional `scripts/suggest_learnings.py` helper (stdout only).

## Reporting issues and ideas

**GitHub Issues** (this repo): use the **[bug](https://github.com/Cartooli/mega-eval-skill/issues/new?template=bug-report.md)**, **[improvement](https://github.com/Cartooli/mega-eval-skill/issues/new?template=improvement.md)**, or **[feature request](https://github.com/Cartooli/mega-eval-skill/issues/new?template=feature-request.md)** template. **Browse:** [Issues](https://github.com/Cartooli/mega-eval-skill/issues).

When you file from a run, include **`run_id`** when you have it (see Phase 4 **Maintainer feedback** in `SKILL.md`).

**Run feedback** (`run-log.md` → promotion to `references/learnings.md`) is separate from GitHub Issues; see [Run feedback](#run-feedback-optional) above and [`MAINTAINERS.md`](MAINTAINERS.md).

## Customization

The `references/subagent-prompts.md` file contains the exact prompts sent to each parallel analysis track; `references/design-audit-template.md` defines Phase 1D output. Edit these to adjust the evaluation dimensions, add new tracks, or change the focus areas.

The `references/learnings.md` file is for **curated** methodological lessons promoted from run logs.

The root `SKILL.md` file controls the overall pipeline flow. You can reorder phases, skip phases, or add new ones.

Phase-only skills under `skills/` intentionally stay thin; after changing prompts or phase behavior in `references/` or root `SKILL.md`, update a thin skill only if **inputs, outputs, or path resolution** wording needs to change.

## License

MIT
