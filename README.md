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

## Install

### Claude Code (CLI)

Copy the skill folder into your project:

```bash
# Clone this repo
git clone https://github.com/YOUR_USERNAME/mega-eval-skill.git

# Copy into your Claude Code skills directory
cp -r mega-eval-skill/SKILL.md mega-eval-skill/references mega-eval-skill/scripts ~/.claude/skills/mega-eval/
```

Or if you prefer, copy just the skill folder contents into any `.claude/skills/mega-eval/` directory in your project.

### Cowork (Desktop app)

Download the `mega-eval.skill` file from this repo's root and open it in Cowork — it will show a "Copy to your skills" install button.

### Manual install

The skill is just a folder with this structure:

```
mega-eval/
├── SKILL.md              # Main skill instructions
├── references/
│   ├── pipeline-checklist.md    # Phase-by-phase checklist
│   └── subagent-prompts.md      # Ready-to-use prompt templates
└── scripts/
    └── ingest.py          # Input file extraction helper
```

Copy that folder into wherever your Claude instance reads skills from.

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

## Dependencies

The skill orchestrates other skills that should be available in your Claude environment:

- **hater-mode** — Used for Phase 1A critical feedback
- **long-form-outline** — Used for Phase 3 content strategy
- **docx** — Used for Phase 4 document assembly

If these aren't installed, the skill will still run but will use its built-in prompt templates instead.

## Customization

The `references/subagent-prompts.md` file contains the exact prompts sent to each parallel analysis track. Edit these to adjust the evaluation dimensions, add new tracks, or change the focus areas.

The `SKILL.md` file controls the overall pipeline flow. You can reorder phases, skip phases, or add new ones.

## License

MIT
