---
name: mega-eval-prompt-derivation
description: "Decompose any user request into a structured Prompt Derivation Engine spec — a JSON object that captures intent, task type, context, output contract, instructions, eval checks, and execution plan. Use this skill when you need to convert a vague or complex request into a precise, schema-validated prompt blueprint before execution. Trigger on: 'derive a prompt for', 'prompt spec', 'decompose this request', 'prompt derivation', 'structured prompt', 'prompt blueprint', or when an upstream orchestrator needs a machine-readable task breakdown."
---

# Prompt Derivation Engine

Convert a user request (plus any attached artifacts) into a fully populated **Prompt Derivation Engine Spec** — a single JSON object conforming to `schemas/prompt-derivation-engine.schema.json`.

## When to Use

- **Standalone:** User asks you to derive / decompose / blueprint a prompt.
- **Sub-prompt:** An orchestrator (e.g. mega-eval Phase 0) calls this skill to produce a structured spec that downstream phases can consume programmatically.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| User request text | Yes | The raw ask — can be a sentence, paragraph, or pasted document |
| Artifacts | No | Files, URLs, JSON blobs, images, etc. attached to the request |
| User preferences | No | Tone, verbosity, format, citation policy overrides |

## Procedure

### Step 1 — Parse the request

Read the user input and any artifacts. Identify:

- **What** they want (goal, task type, subject)
- **How** they want it (format, length, tone, constraints)
- **What could go wrong** (failure modes, uncertainty)
- **What tools/data are needed** (web search, retrieval, closed-book)

### Step 2 — Populate the spec

Fill every required field of the schema. Use these guidelines:

| Section | Key decisions |
|---------|--------------|
| `request` | Generate a UUID-style `request_id`. Copy `user_input` verbatim. Map stated preferences; default to `tone: "neutral"`, `verbosity: "medium"`, `format_preference: "markdown"`. |
| `task_spec` | Pick the single best `task_type`. List concrete `requested_operations` (1-4). Write `success_criteria` as testable statements. Set `freshness.required` true only if the answer depends on data newer than model training. |
| `latent_task_state` | Classify `intent_class` and `knowledge_mode`. Be honest about `uncertainty_level`. List `failure_modes` the downstream executor should watch for. |
| `context_bundle` | Include one `context_item` per meaningful input chunk (user text, each artifact, any system context). Set `compression_policy` based on total context size — `minimal` if small, `balanced` if large. |
| `output_contract` | Choose `format` matching user preference or task nature. `must_include` = things the output must contain. `must_avoid` = hallucination risks, off-topic drift, banned content. |
| `instruction_package` | Write a tight `system_instruction` (role + constraints, 2-4 sentences). Write `user_instruction` as the concrete ask (1-3 sentences). Prefer `instruction_style: "structured_minimal"`. Add `banned_patterns` for known failure modes (e.g. "Do not start with 'Sure, here is...'"). |
| `eval_plan` | Define 2-5 `checks` matching the success criteria. Pick `repair_strategy` based on what's most likely to fail. |
| `execution_plan` | List `tool_calls` if the task needs web search, file reads, etc. Write `ordered_steps` as a concise numbered plan (3-8 steps). |
| `metadata` | Set `created_at` to current ISO-8601 timestamp. `engine_version`: `"1.0.0"`. |

### Step 3 — Validate

Mentally walk the schema's `required` fields and `enum` constraints. Fix any mismatches before outputting.

### Step 4 — Output

Return the JSON object. When called as a sub-prompt, save it to:

```
<workspace>/prompt-derivation-spec.json
```

When called standalone, print it directly.

## Output Format

A single JSON object conforming to `schemas/prompt-derivation-engine.schema.json`. No wrapping markdown, no commentary — just the JSON (unless the user explicitly asks for explanation).

## Schema Reference

The full JSON Schema lives at:

```
schemas/prompt-derivation-engine.schema.json
```

Read it before your first derivation to ensure field-level compliance.

## Example (abbreviated)

```json
{
  "schema_version": "1.0.0",
  "request": {
    "request_id": "a1b2c3d4",
    "user_input": "Compare the top 3 project management tools for small teams"
  },
  "task_spec": {
    "goal": "Produce a structured comparison of project management tools suitable for teams of 2-15 people",
    "task_type": "compare",
    "subject": "project management tools for small teams",
    "requested_operations": ["compare", "rank", "evaluate"],
    "constraints": [
      { "type": "scope", "value": "limit to top 3 by market share" },
      { "type": "length", "value": "medium — 800-1200 words" }
    ],
    "success_criteria": [
      "Covers pricing, collaboration features, and integrations for each tool",
      "Includes a summary comparison table",
      "Ends with a clear recommendation"
    ],
    "freshness": { "required": true, "recency_days": 90, "notes": "Pricing may have changed recently" }
  },
  "latent_task_state": {
    "intent_class": "analysis",
    "knowledge_mode": "retrieval_augmented",
    "uncertainty_level": "medium",
    "needs_external_data": true,
    "needs_tools": true,
    "failure_modes": ["outdated pricing", "missing a major competitor", "generic pros/cons"],
    "minimal_context_keys": ["user_input"],
    "canonical_prompt_form": "compare"
  },
  "context_bundle": {
    "context_items": [
      { "key": "user_request", "value": "Compare the top 3 project management tools for small teams", "source": "user_input" }
    ],
    "compression_policy": "minimal"
  },
  "output_contract": {
    "format": "markdown",
    "sections": ["Introduction", "Tool Profiles", "Comparison Table", "Recommendation"],
    "must_include": ["pricing", "comparison table"],
    "must_avoid": ["unsupported claims", "affiliate-style language"],
    "length_target": "medium"
  },
  "instruction_package": {
    "system_instruction": "You are a product analyst writing for non-technical small-team leads. Be specific about pricing tiers and feature limits. Cite sources when possible.",
    "user_instruction": "Compare the top 3 project management tools for small teams (2-15 people). Include a comparison table and a recommendation.",
    "instruction_style": "structured_minimal",
    "banned_patterns": ["In conclusion", "As an AI"]
  },
  "eval_plan": {
    "checks": [
      { "name": "has_comparison_table", "type": "format", "severity": "high" },
      { "name": "covers_all_three_tools", "type": "coverage", "severity": "high" },
      { "name": "pricing_is_current", "type": "evidence", "severity": "medium" }
    ],
    "repair_strategy": "context_repair"
  },
  "execution_plan": {
    "tool_calls": [
      { "tool_name": "WebSearch", "purpose": "Find current pricing and feature lists for top PM tools" }
    ],
    "ordered_steps": [
      "Search for current top project management tools by market share",
      "Gather pricing, features, and integration details for each",
      "Build comparison table",
      "Write per-tool profiles",
      "Draft recommendation based on small-team fit",
      "Self-check against eval_plan"
    ]
  },
  "metadata": {
    "created_at": "2026-03-27T12:00:00Z",
    "engine_version": "1.0.0"
  }
}
```
