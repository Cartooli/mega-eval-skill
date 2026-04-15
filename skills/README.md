# Mega-eval phase skills (thin entrypoints)

These folders are **picker-friendly slices** of the full pipeline in the repo root [`SKILL.md`](../SKILL.md). Each `SKILL.md` is short; **methodology lives in** [`../references/`](../references/) — do not duplicate long prompts here.

## Resolving `references/` and the full pipeline doc

Agents should load shared files from the **first path that exists**:

| Try | Path | When |
|-----|------|------|
| 1 | `./references/` next to this skill’s `SKILL.md` | You copied the repo’s `references/` folder beside a single phase skill |
| 2 | `../../references/` | This file is at `skills/<name>/SKILL.md` inside a full **mega-eval-skill** clone |
| 3 | `../mega-eval/references/` | Phase skill is a sibling of the full `mega-eval` package (e.g. under `~/.claude/skills/`) |

Full orchestration: [`../SKILL.md`](../SKILL.md), or `../mega-eval/SKILL.md` if only the full package is installed as a sibling.

## Skills in this directory

| Folder | Phase | Output artifact |
|--------|-------|-----------------|
| `mega-eval-brief` | 0 | `eval-brief.md` |
| `mega-eval-hater` | 1A | `phase1a-hater-raw.md` |
| `mega-eval-competitive` | 1B | `phase1b-competitive-raw.md` |
| `mega-eval-strengths` | 1C | `phase1c-strengths-raw.md` |
| `mega-eval-design` | 1D (optional) | `phase1d-design-raw.md` |
| `mega-eval-security` | 1E (optional) | `phase1e-security-raw.md` |
| `mega-eval-durability` | 1F (optional) | `phase1f-durability-raw.md` |
| `mega-eval-synthesis` | 2 | `phase2-synthesis.md` |
| `mega-eval-content-outline` | 3 | `phase3-content-outline-raw.md` |
| `mega-eval-deliverables` | 4 | `01`–`05` and `00` `.docx` |

Install instructions for all layouts are in the repo [`README.md`](../README.md).
