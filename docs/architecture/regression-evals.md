# Regression Evals

PR 6 adds a small deterministic regression corpus under `tests/evals/`.

The purpose is to catch behavior drift that structural validation alone cannot see. These checks are still lightweight and offline:

- no model calls
- no network access
- no golden exact-output matching

Instead, the corpus checks a few high-value behavioral guarantees:

- text-only runs skip Phase 1D explicitly rather than implying a live-site audit happened
- sparse inputs preserve uncertainty and open questions instead of overclaiming confidence
- limited-data competitive analysis states confidence limits rather than fabricating authority
- design-audit fallback stubs explicitly say what was not tested
- synthesis artifacts preserve disagreements in `## Unresolved Tensions`

## Corpus layout

Each case lives in its own folder under `tests/evals/`.

Current cases:

- `text_only`
- `sparse_input`
- `limited_data_competitive`
- `design_audit_fallback`
- `synthesis_tension`

## What these tests are not

- They are not benchmark scores.
- They are not semantic judges.
- They are not replacements for artifact contracts.

They are deterministic guardrails for the repo's most important qualitative promises.

## Maintainer rule

When you change expected run behavior, update:

- the relevant files in `tests/evals/`
- `tests/test_regression_evals.py`
- this document if the corpus purpose or case list changes
