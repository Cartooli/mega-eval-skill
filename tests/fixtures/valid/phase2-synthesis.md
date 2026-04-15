# Synthesis: Critical Fixes, Design Issues & Next Steps

## Critical Fixes Needed

### Fix 1: Add artifact validation
- **What:** Introduce machine-checked contracts for the markdown artifacts that every phase emits.
- **Why it matters:** The pipeline currently relies on prose instructions alone, so weaker runs can silently ship malformed or placeholder-heavy outputs.
- **Flagged by:** Durability review, prompt architecture review, and maintainability concerns raised during synthesis.
- **Suggested approach:** Add lightweight schemas, a validator script, and fixture-based tests that fail fast in CI.

## Design Inconsistencies to Resolve
The repo documents structured artifacts in several places, but there is no single contract layer to back those promises. That mismatch between documentation and enforcement creates avoidable drift.

## Proposed Next Steps (Non-Breaking Changes)
Ship the contract layer first, then expand it phase by phase. This keeps the workflow stable for users while adding enforcement behind the scenes.

### Quick Wins (days)
Add contracts for `eval-brief.md`, `phase1b-competitive-raw.md`, and `phase2-synthesis.md`.

### Medium-Term (weeks)
Extend the same validation approach to remaining phase artifacts and connect validation events to structured run logs.

### Strategic (months)
Use validated artifacts as the basis for regression evals that catch host or model drift before users do.

## Unresolved Tensions
The pipeline needs stronger machine enforcement, but it should remain lightweight and readable for maintainers. The current compromise is a dependency-free validator with lightweight JSON contracts instead of a heavier schema stack.
