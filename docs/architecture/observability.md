# Observability

PR 5 adds a lightweight structured observability layer on top of the existing narrative `run-log.md`.

The design goal is simple:

- keep `run-log.md` readable for humans
- add `run-log.jsonl` for machine-readable event reconstruction
- avoid introducing a database, analytics service, or mandatory external dependency

## Logging model

Mega-eval now has two complementary log formats when run logging is enabled:

- **`run-log.md`**
  - human-facing
  - good for promotion review and qualitative notes
- **`run-log.jsonl`**
  - machine-facing
  - one JSON object per line
  - good for reconstructing what happened during a run

The JSONL sidecar is intended to answer questions the markdown log is bad at:

- which prompt was selected?
- which artifact was being written?
- what fallback path was used?
- how long did a phase take?
- which run produced this file?

## Event shape

Each JSONL line is an object with this baseline shape:

```json
{
  "timestamp": "2026-04-15T12:00:00Z",
  "run_id": "a1b2c3d4",
  "event_type": "phase_start",
  "phase": "phase1",
  "status": "ok"
}
```

Optional fields:

- `artifact_path`
- `prompt_id`
- `duration_ms`
- `fallback_used`
- `details`

## Recommended event types

- `phase_start`
- `phase_complete`
- `prompt_selected`
- `artifact_written`
- `artifact_validated`
- `tool_error`
- `retry`
- `fallback_used`
- `quality_gate_fail`
- `user_correction`

## Usage

Append one event:

```bash
python3 scripts/log_event.py run-log.jsonl phase_start \
  --run-id a1b2c3d4 \
  --phase phase1 \
  --status ok
```

Append a validation event:

```bash
python3 scripts/log_event.py run-log.jsonl artifact_validated \
  --run-id a1b2c3d4 \
  --phase phase2 \
  --artifact-path phase2-synthesis.md \
  --status pass \
  --details "contract=phase2-synthesis"
```

## Maintainer expectations

- If `run-log.md` exists, prefer a matching `run-log.jsonl` beside it when the runtime can append structured files.
- Keep the JSONL log local and redact sensitive material before sharing examples.
- Do not treat JSONL as product analytics. It is local execution telemetry only.
