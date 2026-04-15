# QA Skill — Functional Specification

## Purpose

The QA skill automates the testing and bug fixing workflow. When you change code and want to verify it works, run `/qa`. The skill will:

1. Browse your application like a real user
2. Find bugs in what you changed
3. Fix bugs in the source code
4. Verify the fixes work
5. Write a report

This turns manual QA (hours of clicking and documenting) into a 5-15 minute automated workflow.

## User Workflow

**Invoke:** `/qa` (on a feature branch with code changes)

**No manual setup required.** The skill detects:
- What code changed (via git diff)
- Which pages were affected
- Which local server to test against (`:3000`, `:4000`, etc.)
- Whether tests exist and how to run them

**Output:** 
- A markdown report with evidence (screenshots, console errors, repro steps)
- Fixed bugs as atomic git commits
- Updated test suite (regression tests for each fix)

## Core Features

### 1. Diff-Aware Testing (Primary Mode)

You're on a feature branch. You run `/qa`. The skill automatically:

- Analyzes your git diff to find changed files
- Maps those files to affected URL routes and pages
- Tests only those pages
- Reports findings scoped to your changes

No URL required. No manual page navigation needed. The skill knows what you changed and tests exactly that.

**Example:** You changed `src/checkout/payment.tsx` and `src/checkout/receipt.tsx`. The skill navigates to `/checkout` and `/checkout/receipt`, fills the form, processes payment, and checks the receipt. It takes screenshots at each step.

### 2. Full QA Mode

Provide a URL. The skill systematically explores every page:
- Homepage → all navigation links → every reachable page
- Tests forms, buttons, links, error states, edge cases
- Checks console for JavaScript errors
- Computes a health score (0-100)

**Example:** `/qa https://myapp.com` explores 15 pages, finds 8 issues, produces a structured report.

### 3. Quick Mode

30-second smoke test. Visits homepage + top 5 navigation targets. Checks if the app loads and console is clean.

```
/qa --quick
```

### 4. Auto-Fix

For each bug found:

1. The skill locates the source file causing the bug (via grep, file inspection)
2. Reads the code, understands context
3. Makes the minimal fix (smallest change that resolves it)
4. Commits the fix as a single atomic commit
5. Re-tests to verify the fix works
6. Takes before/after screenshots as evidence

**Example:** You have a typo in a form label. The skill:
- Finds the component file
- Changes `"Emai Address"` to `"Email Address"`
- Commits: `fix(qa): ISSUE-001 — typo in form label`
- Re-navigates to the form, takes a screenshot showing the corrected label

### 5. Regression Testing

After fixing a bug in code, the skill automatically writes a test that would catch that bug in the future. Tests are generated to match your project's existing conventions (same file naming, imports, assertions, setup patterns).

**Example:** You fix a bug where empty arrays crash the UI. The skill writes a unit test with an empty array input and verifies the UI renders correctly. The test is committed: `test(qa): regression test for ISSUE-NNN`.

### 6. Test Framework Bootstrap

If your project has no tests yet, `/qa` can set them up automatically:

1. Detects your project language (Node, Ruby, Python, Go, etc.)
2. Researches current best-practice frameworks for that language
3. Asks you which framework to use
4. Installs packages, creates directories, writes example tests
5. Creates GitHub Actions CI to run tests on every push

**Example:** Python project with no tests. The skill sets up pytest, creates `test/` directory, writes 5 example tests, adds `.github/workflows/test.yml`.

## Severity Tiers

- **Quick:** Fix only critical + high-severity bugs
- **Standard** (default): Fix critical + high + medium
- **Exhaustive:** Fix all bugs including cosmetic/low-severity

Bugs that can't be fixed from source (third-party widget bugs, infrastructure issues) are marked "deferred" regardless of tier.

## Self-Regulation

The skill stops if:

- It has reverted more than one fix (something is breaking the codebase)
- Too many fixes are modifying unrelated files (scope creep)
- More than 50 fixes have been applied (hard cap to prevent runaway sessions)

When any stop condition is met, it reports what it's done and asks if you want to continue.

## Safety

- **Clean working tree required.** If you have uncommitted changes, the skill asks: commit, stash, or abort. This prevents losing work.
- **One commit per fix.** Never bundles multiple fixes into one commit. If a fix causes a regression, it's reverted immediately.
- **Only modifies source files** for actual bug fixes. Never touches CI config, never modifies existing tests, never refactors unrelated code.
- **Every fix is re-tested.** Before/after screenshots prove the fix works.

## Report Format

Each QA run produces a markdown report:

```
.gstack/qa-reports/qa-report-myapp-com-2026-03-10.md
```

Contains:
- Summary (pages tested, bugs found, health score)
- Issue list (severity, category, repro steps, screenshots, fix status)
- Console errors (aggregated)
- Performance observations
- Regression test commits (if any)

Screenshots are saved separately:
```
.gstack/qa-reports/screenshots/
├── initial.png (landing page)
├── issue-001-before.png
├── issue-001-after.png
└── ...
```

## Health Score

Computed across 8 categories:
- Console (JavaScript errors)
- Links (broken hyperlinks)
- Visual (layout, alignment, contrast)
- Functional (forms, buttons, interactive features)
- UX (flows, state management, edge cases)
- Performance (slow loading, janky animations)
- Content (typos, missing text, formatting)
- Accessibility (keyboard navigation, screen reader support)

Each category starts at 100. Deducted per finding:
- Critical: -25
- High: -15
- Medium: -8
- Low: -3

Final score is a weighted average (console: 15%, links: 10%, visual: 10%, functional: 20%, UX: 15%, performance: 10%, content: 5%, accessibility: 15%).

**0-50:** Major issues; app is broken or unusable for core flows.
**51-75:** Moderate issues; usable but rough edges.
**76-100:** Polished; few or no issues.

## Modes & Scope

| Scenario | Mode | Behavior |
|----------|------|----------|
| `git checkout -b feat/login` → change login form → `/qa` | Diff-aware | Test only the login form |
| `/qa https://myapp.com` | Full | Explore all 20+ pages systematically |
| `/qa --quick` | Quick | Smoke test (30 sec) |
| `/qa --regression baseline.json` | Regression | Compare against prior QA run |
| `composer.json with no test framework` + `/qa` | Bootstrap | Set up PHPUnit, write example tests |

## Common Patterns

**Pattern: Verify a feature works end-to-end**
```
git checkout -b feat/payment-retry
# Make changes to payment retry logic
/qa
```
Skill tests: customer makes payment → payment fails → retry button works → payment succeeds.

**Pattern: Health check an app**
```
/qa https://staging.myapp.com
```
Skill explores all pages, reports health score and top 3 issues to fix.

**Pattern: Before shipping to production**
```
git checkout main
/qa --quick
```
30-second smoke test to verify no obvious breakage.

## Output & Artifacts

- **Report:** Markdown file, can be committed to git or shared with team
- **Screenshots:** PNG evidence for each bug, before/after for fixes
- **Commits:** Each fix is its own git commit with message format `fix(qa): ISSUE-NNN — description`
- **Tests:** New regression tests committed as `test(qa): regression test for ISSUE-NNN`
- **Learnings:** Cross-session patterns logged (e.g., "this form validation breaks on mobile")

## Interaction with Codebase

- **Read:** Reads changed files, source code (to locate bugs), test files (to learn conventions), git history
- **Write:** Commits bug fixes, adds regression tests, creates reports and screenshots in `.gstack/qa-reports/`
- **Never:** Modifies CI/CD config, refactors unrelated code, deletes test files, destructively edits git history

## Success Criterion

A QA run is successful when:

1. All affected pages load without JavaScript errors
2. Forms submit without errors
3. Navigation links work
4. No console errors or warnings
5. Health score is 75+
6. Fixed bugs are verified with before/after evidence
7. Regression tests are added for each fix
8. All changes are committed atomically

## Edge Cases Handled

- **No local server running:** Checks common ports, asks user for URL
- **Requires authentication:** Prompts for credentials or cookie import
- **CAPTCHA blocks testing:** Asks user to complete it manually, then continues
- **SPA with client-side routing:** Uses snapshot inspection instead of link crawler
- **Framework-specific bugs:** Knows Next.js hydration errors, Rails N+1 queries, Vue state issues, etc.
- **No test framework:** Bootstraps one automatically
- **Dirty working tree:** Asks to commit/stash before starting

## Constraints

- **Maximum 50 fixes per run.** After 50, stops and asks if you want to continue. Prevents runaway sessions.
- **Reverts on regression.** If a fix breaks something, it's automatically reverted.
- **Must have clean git history.** Each fix is one commit. Can't proceed if working tree is dirty.
- **Browser-based only.** Tests the running application, not source code. Never mocks the database.

## Related Skills

- **`/review`** — Code review (peer review, not testing)
- **`/investigate`** — Debug a specific bug
- **`/ship`** — Push to production safely
- **`/plan`** — Design implementation before building
- **`/test-strategy`** — Plan how to test a feature

---

**Version:** 1.0  
**Last Updated:** 2026-04-10  
**Status:** Stable
