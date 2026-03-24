# Run log — `a1b2c3d4` (example)

Fictional mega-eval run for documentation only.

## Meta

- run_id: `a1b2c3d4`
- started: `2026-03-24T10:00:00Z`
- workspace: `/tmp/example-workspace`
- status: complete

## Events (append-only)

- `[2026-03-24T10:00:01Z]` phase_start phase0
- `[2026-03-24T10:00:45Z]` phase_complete phase0
- `[2026-03-24T10:00:46Z]` phase_start phase1
- `[2026-03-24T10:02:10Z]` tool_error web_fetch url=<redacted> message="timeout after 30s"
- `[2026-03-24T10:02:11Z]` assumption_flag note="proceeded with pasted landing copy only"
- `[2026-03-24T10:08:00Z]` phase_complete phase1
- `[2026-03-24T10:08:01Z]` phase_start phase2
- `[2026-03-24T10:12:00Z]` phase_complete phase2
- `[2026-03-24T10:12:30Z]` user_correction phase=1b note="remove Competitor X — not direct peer"
- `[2026-03-24T10:13:00Z]` implicit_signal heavy_edit target=phase1b-competitive-raw.md
- `[2026-03-24T10:14:00Z]` phase_start phase3
- `[2026-03-24T10:18:00Z]` phase_complete phase3
- `[2026-03-24T10:18:01Z]` phase_start phase4
- `[2026-03-24T10:25:00Z]` phase_complete phase4

## Failure modes (tags for promotion search)

- `[2026-03-24T10:02:10Z]` tool_timeout — web fetch landing URL
- `[2026-03-24T10:12:30Z]` grounding — competitor list corrected by user

## Promotion candidates (unchecked until reviewed)

- [ ] When primary URL fetch fails, Phase 1B should still run but must label competitive section confidence as low and avoid inventing pricing for unfetched pages.
- [ ] Add checklist reminder: user may remove competitors after Phase 1; synthesis must reflect final raw files before Phase 4.
