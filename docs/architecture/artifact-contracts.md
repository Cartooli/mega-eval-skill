# Artifact Contracts

PR 1 introduces lightweight, machine-checked contracts for the highest-value markdown artifacts in the mega-eval pipeline.

The goal is not to replace human judgment. The goal is to catch structural drift early:

- missing required sections
- unresolved placeholders that leaked into output
- list sections with no bullets
- thin sections that are effectively blank

## Current scope

Covered artifacts:

- `eval-brief.md`
- `phase1b-competitive-raw.md`
- `phase1c-strengths-raw.md`
- `phase1d-design-raw.md`
- `phase1e-security-raw.md`
- `phase1f-durability-raw.md`
- `phase2-synthesis.md`
- `phase3-content-outline-raw.md`

The contracts live under `schemas/` as JSON files and are enforced by `scripts/validate_artifact.py`. Pipeline hard-stops use `scripts/validate_run_artifacts.py` with `--gate pre-phase1|pre-phase2|pre-phase3|pre-phase4` (see root `SKILL.md`). Optional 1D/1E/1F files are validated only when present. `phase1a-hater-raw.md` remains outside schema enforcement until mega-eval owns that contract.

## Contract model

The schema files are intentionally lightweight. They are JSON-based artifact contracts rather than a full JSON Schema implementation.

Each schema can define:

- `required_title`: expected top-level heading
- `required_headings`: headings that must exist
- `required_nonempty_sections`: headings whose content must not be blank
- `required_bullet_sections`: headings that must contain at least one markdown bullet
- `section_min_words`: minimum word counts for specific sections
- `section_required_substrings`: section-specific strings that must appear
- `forbidden_patterns`: regexes that must not appear anywhere in the artifact

This keeps the validator dependency-free and easy to evolve while still giving the repo real enforcement.

## Validation workflow

Run a single-file validator:

```bash
python3 scripts/validate_artifact.py path/to/artifact.md path/to/schema.json
```

Or validate a workspace for a pipeline gate:

```bash
python3 scripts/validate_run_artifacts.py --gate pre-phase2 path/to/workspace
```

Successful validation exits `0`. Validation failures print a readable error list and exit nonzero (`1` for contract failures / missing required files; `2` for usage errors).

## Why these three artifacts first

`eval-brief.md` is the root contract for every downstream phase.

`phase1b-competitive-raw.md` is a representative structured phase output with both bullet-heavy and prose-heavy sections.

`phase1c-strengths-raw.md` and `phase3-content-outline-raw.md` extend contract coverage to positive analysis and narrative output, not just critique and synthesis.

`phase1d-design-raw.md` covers the report-only design audit path, including thin fallback behavior.

`phase2-synthesis.md` is the most judgment-heavy artifact and the place where drift is likely to show up as missing action structure.

## Near-term follow-up

The most notable remaining gaps are:

- `phase1a-hater-raw.md`, whose output shape is currently governed largely by the external hater-mode skill. If mega-eval takes ownership of that contract later, it should reuse the same validator unless a more formal schema engine becomes necessary.
