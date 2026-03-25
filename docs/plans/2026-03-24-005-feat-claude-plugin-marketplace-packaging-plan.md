---
title: "feat: Claude Code plugin marketplace packaging (marketplace.json + manifests)"
type: feat
status: completed
date: 2026-03-24
deepened: "2026-03-24 (pass 1); 2026-03-24 (pass 2: manifest + layout + CI)"
---

# feat: Claude Code plugin marketplace packaging

## Enhancement Summary

**Deepened on:** 2026-03-24  
**Sections enhanced:** Overview, Proposed Solution (all subsections), Technical Considerations, E2E verification, Acceptance Criteria, Dependencies & Risks, Sources  
**Research basis:** Anthropic docs — [Create and distribute a plugin marketplace](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces), [Discover and install prebuilt plugins](https://docs.anthropic.com/en/docs/claude-code/discover-plugins), marketplace schema & plugin sources (official)

### Key improvements

1. **Git vs URL marketplaces:** Relative `./plugins/...` sources only resolve when users add the marketplace via **Git** (e.g. `owner/repo`); **direct URL** to `marketplace.json` breaks relative paths — document this so README never suggests URL-only add for this layout.
2. **Operational steps:** Add **`/reload-plugins`** after install; note **`claude --version`** (plugins require **1.0.33+**); add **install scopes** (user / project / local) and optional **`extraKnownMarketplaces`** for teams.
3. **Naming guardrails:** Marketplace `name` must be **kebab-case** and avoid **reserved** Anthropic names (`claude-plugins-official`, `claude-code-plugins`, etc.) — validate before merge.

### New considerations discovered

- **`metadata.pluginRoot`** can shorten plugin `source` entries if all plugins live under one directory (e.g. `"./plugins"` as root + `"formatter"` per plugin).
- **Removing a marketplace** uninstalls plugins that came from it — support docs should mention re-add if users “clean house.”
- **Symlinks** inside the plugin tree are **followed** when copying to cache — useful if choosing a symlink-based single source of truth (with caveats for Windows contributors).

### Deepening pass 2 (manifest, layout, validation)

**Focus:** [Plugins reference](https://code.claude.com/docs/en/plugins-reference) (code.claude.com) — plugin manifest schema, standard layout, CLI, debugging.

**Key additions**

1. **Layout contract:** Only `.claude-plugin/plugin.json` lives under `.claude-plugin/`; **`skills/`, `scripts/`, `agents/`, etc. must sit at the plugin root**, not inside `.claude-plugin/` ([Standard plugin layout](https://code.claude.com/docs/en/plugins-reference#standard-plugin-layout)).
2. **Skill discovery:** Skills are auto-discovered from default **`skills/`** (and `commands/`). A **`SKILL.md` at the plugin root is not the documented pattern** — the full mega-eval orchestrator today lives at **repo root** `SKILL.md`. **Implementation must resolve this:** e.g. ship the full pipeline as **`skills/mega-eval/SKILL.md`** inside the plugin (and align docs/triggers), **or** use manifest **`skills`** path fields to point at an extra directory (custom paths **supplement** defaults; paths relative to plugin root, `./`-prefixed) — verify with `claude plugin validate` after layout is chosen.
3. **Validation:** Use **`claude plugin validate`** or **`/plugin validate`** for `plugin.json`, skill frontmatter, and hooks ([Debugging](https://code.claude.com/docs/en/plugins-reference#debugging-and-development-tools)) — add to maintainer checklist and optional CI.
4. **Versioning & cache:** If `plugin.json` **version** does not bump, **existing installs may not pick up code changes** due to caching ([Distribution and versioning](https://code.claude.com/docs/en/plugins-reference#distribution-and-versioning-reference)) — align with release process (or centralize version in `marketplace.json` per docs).
5. **Manifest conflicts:** Error **“conflicting manifests: both plugin.json and marketplace entry specify components”** — avoid duplicating component paths between `marketplace.json` entries and `plugin.json` unless **`strict: false`** is understood ([Example error messages](https://code.claude.com/docs/en/plugins-reference#example-error-messages)).
6. **Script paths:** Prefer **`${CLAUDE_PLUGIN_ROOT}`** in hooks/MCP for bundled scripts; **`scripts/`** at plugin root matches the reference layout for `ingest.py` etc. ([Environment variables](https://code.claude.com/docs/en/plugins-reference#environment-variables)).
7. **CI (no Claude in GitHub by default):** Minimum: **`python3 -m json.tool`** on `.claude-plugin/marketplace.json` and each `plugin.json`. Better: run **`claude plugin validate <path>`** in CI **if** the runner installs Claude Code CLI. Document that **E2E still requires a human with Claude Code**.

## Overview

Add a **Claude Code–native distribution path** by shipping a valid **`.claude-plugin/marketplace.json`** catalog and at least one **`plugin.json`** manifest, then **verify end-to-end** install with `/plugin marketplace add` and `/plugin install`. This complements (does not replace) the existing **manual `cp`** and **Cowork** instructions in [`README.md`](../../README.md).

### Research Insights

**Best practices**

- Treat plugins as **high trust**: they run with user privileges; README should say “only add marketplaces you trust” (aligned with Anthropic security guidance).
- Prefer **Git-based** `marketplace add` for this repo so **relative** `./plugins/<id>` sources work; call out that **URL-only** catalog hosting breaks relative plugin paths ([Troubleshooting: relative paths](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)).

**References**

- [Discover and install prebuilt plugins — Security](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#security)

## Problem Statement / Motivation

- Users with Claude Code expect **plugin discovery, install, and updates** via the built-in plugin system ([Anthropic: Create and distribute a plugin marketplace](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces)).
- This repo today is documented as **skills-only** installs; there is **no** `.claude-plugin` layout ([grep confirms no matches](../../) as of this plan).
- Prior analysis: the two-step CLI flow is **not redundant** vs manual copy—it is the **official** update-friendly path for Claude Code—**but** it only works if the repo matches Anthropic’s **plugin + marketplace** structure and respects **plugin cache isolation** (no reliance on files outside the copied plugin tree).

### Research Insights

**Edge cases**

- **Auto-updates:** Third-party marketplaces default to **auto-update off**; official ones default **on**. Document how users can **refresh** (`/plugin marketplace update <name>`) or use UI toggles.
- **Plugin skills not appearing:** Official troubleshooting suggests clearing `~/.claude/plugins/cache`, restarting, reinstalling — add as “if install succeeded but skills missing.”

**References**

- [Discover plugins — Manage marketplaces / auto-updates](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#configure-auto-updates)
- [Discover plugins — Troubleshooting](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#troubleshooting)

## Proposed Solution

### 1. Package shape (single-plugin MVP — recommended)

Ship **one plugin** that contains the **full tree** needed for both the **orchestrator** and the **thin phase skills**, so relative paths in [`skills/README.md`](../../skills/README.md) keep working:

| Path in repo today | Inside plugin directory |
|--------------------|-------------------------|
| Root `SKILL.md`, `references/`, `scripts/` | Same at plugin root |
| `skills/<phase>/SKILL.md` | `skills/<phase>/SKILL.md` |

Resolution order (1) `./references/` beside a skill, (2) `../../references/` from `skills/<name>/` → both resolve to the **single embedded `references/`** at the plugin root after install.

**Avoid (for MVP):** multiple separate plugins that each need a full copy of `references/` (duplication and drift) unless you explicitly accept that maintenance cost later.

### Research Insights

**Implementation details**

- Anthropic copies each plugin into **`~/.claude/plugins/cache`**; **symlinks are followed** during copy, which can dedupe shared assets **if** the symlink lives entirely inside the plugin directory ([Plugin caching](https://docs.anthropic.com/en/plugins-reference#plugin-caching-and-file-resolution)).
- Do **not** use `../` in `marketplace.json` relative paths to climb out of the marketplace root — only `./` paths under the repo root are valid ([Relative paths](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces#relative-paths)).

### 2. Files to add

- **`.claude-plugin/marketplace.json`** — marketplace `name`, `owner`, and a `plugins[]` entry pointing at `./plugins/<plugin-id>` (exact relative path per Anthropic’s walkthrough).
- **`plugins/<plugin-id>/.claude-plugin/plugin.json`** — `name`, `description`, `version` (semver aligned with tags or `MAINTAINERS.md` release practice if any).
- **Plugin content tree** — either:
  - **Symlink or build step:** not required if the plugin directory **contains** the real files (preferred for clarity in git), or
  - **Duplicate copies:** only if unavoidable—prefer one directory of truth.

**Naming:** Pick a stable marketplace id (e.g. `mega-eval` or `cartooli-mega-eval`) and plugin id (e.g. `mega-eval`) so docs can show `plugin@marketplace` consistently.

### Research Insights

**Best practices**

- **Marketplace `name`:** Must be **kebab-case, no spaces** — this is the string after `@` in `/plugin install plugin@marketplace` ([Marketplace schema — required fields](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces#required-fields)).
- **Reserved names:** Do not use: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`, or names that impersonate Anthropic — **blocked**.
- **Optional:** `metadata.pluginRoot` (e.g. `"./plugins"`) lets plugin entries use shorter `source` values if you standardize layout.
- **Plugin entries** can include `homepage`, `repository`, `license` (SPDX), `keywords`, `category`, `tags`; optional **`strict`** ties behavior to `plugin.json` as authority ([Plugin entries](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces#plugin-entries)).

**Versioning**

- Per-plugin **`version`** can appear in the marketplace listing; align with `plugin.json` and git tags for supportability.

### 3. End-to-end verification (required)

Document and execute a **repeatable check** (manual is fine for this repo):

1. **Prerequisite:** `claude --version` — plugins require **Claude Code 1.0.33+** ([Discover plugins — troubleshooting](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#plugin-command-not-recognized)).
2. From a clean Claude Code session, run `/plugin marketplace add` against:
   - **Local path:** `./` (repo root containing `.claude-plugin/marketplace.json`), and/or
   - **GitHub:** `Cartooli/mega-eval-skill` (after merge), using **`owner/repo`** (relative plugin paths require **Git-based** add, not a raw URL to `marketplace.json` alone).
3. Run `/plugin install <plugin-name>@<marketplace-name>` (exact strings from `marketplace.json`). Optionally use UI to pick **scope** (user / project / local); CLI defaults to user scope; `claude plugin install ... --scope project` exists for automation ([Configuration scopes](https://docs.anthropic.com/en/settings#configuration-scopes)).
4. Run **`/reload-plugins`** so skills/commands load without a full restart ([Discover plugins — reload](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#apply-plugin-changes-without-restarting)).
5. Confirm the **mega-eval** skill is invocable and that at least **one thin skill** path still resolves `references/` (spot-check `skills/mega-eval-brief` or competitive).
6. Optional: `/plugin marketplace update <marketplace-name>` then confirm version bump behavior if you ship version bumps in `plugin.json`.

Record **exact commands** and **failure modes** (e.g. wrong `@` suffix, **URL-based marketplace** + relative paths, cache issues) in [`README.md`](../../README.md).

### Research Insights

**Checklist additions**

| Step | Why |
|------|-----|
| `/reload-plugins` | Picks up skills/agents after install without restart |
| Verify Git-based add | `./plugins/...` resolution for third parties |
| Test one **project-scoped** install | Matches collaborators using repo `.claude/settings.json` |

**Team distribution (optional doc bullet)**

- Project **`extraKnownMarketplaces`** in `.claude/settings.json` can prompt collaborators to trust and install your marketplace ([Discover plugins — team marketplaces](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#configure-team-marketplaces)).

### 4. Documentation updates

- Add an **“Install via Claude Code plugins”** section to [`README.md`](../../README.md): prerequisite (Claude Code), two-step commands, correct **`plugin@marketplace`** syntax, **`/reload-plugins`**, **Git `owner/repo` vs URL** caveat for this layout, link to Anthropic discover/install docs.
- Keep **manual install** as the fallback for Cursor-only users, CI, or non–Claude Code agents (per existing README framing).

### Research Insights

**Docs-only path**

- **Submitting to Anthropic’s official marketplace** is a **separate** flow (in-app forms at [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit) / Console) — out of scope for “ship our own marketplace.json” unless you add a stretch goal ([Discover plugins — official marketplace](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#official-anthropic-marketplace)).

## Technical Considerations

- **Plugin cache rule:** Anthropic states installed plugins are **copied** to a cache; paths **outside** the plugin directory break. The **single-plugin monolith** avoids `../` escapes that would fail across plugin boundaries.
- **Duplication vs DRY:** Maintaining both “raw” repo layout and `plugins/<id>/` could duplicate files. Prefer **one layout**:
  - **Option A:** Move canonical skill files under `plugins/mega-eval/` and adjust README paths (larger refactor), or
  - **Option B:** Keep current layout and have the plugin subtree be the **authoritative copy** for marketplace releases with a **checklist** on release to sync from root (simpler but manual), or
  - **Option C:** Script that copies root `SKILL.md`, `references/`, `scripts/`, `skills/` into `plugins/<id>/` pre-tag (automation, best long-term).

Defer **Option C** to implementation; the plan only requires picking one approach in `/ce:work` with explicit tradeoffs.

**Plugin layout (pass 2):** The reference standard places discoverable skills under **`skills/<name>/SKILL.md`**. This repo’s **full pipeline** currently uses **root** [`SKILL.md`](../../SKILL.md). Packaging must either **relocate** the orchestrator into `skills/mega-eval/` (inside the plugin tree), **or** override with manifest **`skills`** paths and validate — otherwise the main skill may not register. Thin skills under `skills/mega-eval-*` already match the expected pattern.

### Research Insights

**Relative path + distribution**

- Docs explicitly state: relative plugin sources **only work** when the marketplace is added via **Git**; **URL** to hosted `marketplace.json` fails for relative paths — **our README must recommend `owner/repo` or local path**, not “paste this raw JSON URL” for the default layout ([Relative paths limitation](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces#relative-paths)).

**Pinning**

- Plugin sources support **`ref`** (branch/tag) and **`sha`** (exact commit) for reproducible installs — consider documenting a stable tag for support.

## System-Wide Impact

- **Interaction graph:** None for runtime code—this is packaging and docs.
- **Error propagation:** Bad `marketplace.json` breaks **install only**; no production runtime.
- **State lifecycle:** N/A.
- **API surface:** N/A.
- **Integration tests:** E2E is **manual Claude Code** unless you add CI that shells out to Claude Code (unlikely)—accept **human verification** as the quality gate.

### Research Insights

- **Removing a marketplace** also **uninstalls** plugins installed from it — worth a one-liner in maintainer or user docs so behavior is expected ([Discover plugins — remove marketplace](https://docs.anthropic.com/en/docs/claude-code/discover-plugins#manage-marketplaces)).

## Acceptance Criteria

- [ ] `.claude-plugin/marketplace.json` exists and validates against Anthropic’s documented schema (manual or `jq` inspection).
- [ ] Marketplace **`name` is kebab-case**, not in the **reserved** list, and matches the **`@marketplace`** string in documented install commands.
- [ ] At least one `plugins/<id>/.claude-plugin/plugin.json` exists with coherent `name`, `version`, `description` (if manifest omitted, document reliance on auto-discovery and test that behavior explicitly).
- [ ] **Plugin directory layout** matches [standard layout](https://code.claude.com/docs/en/plugins-reference#standard-plugin-layout): components at **plugin root**, not nested under `.claude-plugin/`.
- [ ] **Full pipeline + thin skills** are discoverable: resolved the **root `SKILL.md` vs `skills/`** gap (see Deepening pass 2) so the orchestrator and phase skills appear after install.
- [ ] Plugin tree includes everything required for **full pipeline + thin skills** without broken `references/` resolution per [`skills/README.md`](../../skills/README.md).
- [ ] **`claude plugin validate`** (or `/plugin validate`) passes on the packaged plugin path before release.
- [ ] Maintainer has run **local** `/plugin marketplace add` + `/plugin install` + **`/reload-plugins`** successfully and recorded steps in README.
- [ ] After merge to default branch, **GitHub** `owner/repo` marketplace add is tested once; README states that **Git-based** add is required for **relative** `./plugins/...` sources (not URL-only catalog).
- [ ] [`README.md`](../../README.md) documents both **plugin install** and **manual install** without contradicting paths.
- [ ] Troubleshooting line for **“skills not appearing”** (cache clear / reinstall) if users report install glitches.
- [ ] **Version bump policy** documented: code changes that should reach users require **`plugin.json` or marketplace version** bump per [versioning reference](https://code.claude.com/docs/en/plugins-reference#distribution-and-versioning-reference).
- [ ] Optional: **CI** runs JSON parse checks on manifest files; optional job runs `claude plugin validate` when CLI is available.

## Success Metrics

- A new user can install via **plugins** without copying `cp` commands.
- No open questions about **`plugin@marketplace`** syntax in our docs.

## Dependencies & Risks

| Risk | Mitigation |
|------|------------|
| Duplicate trees drift | Choose single source of truth (see Technical Considerations) or release sync checklist. |
| Claude Code CLI changes | Link to official docs; avoid hard-coding beyond current `/plugin` verbs. |
| Thin skills break in cache | E2E test phase skills + `references/` load. |
| **URL-based marketplace** misconfiguration | README: use **Git** add for default layout; explain why. |
| **Reserved marketplace name** | Grep Anthropic list before publishing. |

### Research Insights

- **CLI drift:** Shortcut aliases exist (`/plugin market`, `rm` for remove) — optional in docs; primary commands are enough.

## Alternatives Considered

| Approach | Pros | Cons |
|----------|------|------|
| **Docs-only** (“use `/plugin` when we publish”) | Zero repo churn | Misleading until packaging exists |
| **Multi-plugin** (one plugin per phase) | Granular install | Duplicated `references/` or complex shared packages |
| **Marketplace-only** (drop manual README) | Simpler story | Excludes non–Claude Code users |

**Recommendation:** Single-plugin MVP + keep manual install in README.

## Documentation Plan

- Update [`README.md`](../../README.md) Install section.
- Optionally add one paragraph to [`MAINTAINERS.md`](../../MAINTAINERS.md) on bumping `plugin.json` version when tagging and validating marketplace name / reserved list.

## Sources & References

### Primary (Anthropic / Claude Code)

- [Create and distribute a plugin marketplace](https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces) — `marketplace.json` schema, reserved names, relative paths, plugin sources, symlink copying
- [Discover and install prebuilt plugins](https://docs.anthropic.com/en/docs/claude-code/discover-plugins) — add/install flows, scopes, `/reload-plugins`, troubleshooting, team marketplaces, security
- [**Plugins reference** (canonical manifest & layout)](https://code.claude.com/docs/en/plugins-reference) — `plugin.json` complete schema, `claude plugin validate`, standard plugin layout, `${CLAUDE_PLUGIN_ROOT}`, versioning vs cache, CLI `plugin install`, conflicting-manifest errors
- [Settings — configuration scopes](https://docs.anthropic.com/en/settings#configuration-scopes) — user / project / local install scopes

**Note:** `docs.anthropic.com/.../plugins-reference` may redirect or 404; use **code.claude.com** docs for the plugin manifest reference above.

### Internal

- [`README.md`](../../README.md), [`skills/README.md`](../../skills/README.md)
- Related plan: [`2026-03-24-004-feat-mega-eval-sub-skills-plan.md`](2026-03-24-004-feat-mega-eval-sub-skills-plan.md) (path resolution constraints for thin skills)
