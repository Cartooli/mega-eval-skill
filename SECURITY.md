# Security Policy

## Reporting a vulnerability

If you find a security issue in the skill logic, prompt templates, or scripts in this repository, please **do not** open a public GitHub issue.

Instead, use GitHub's private [Security Advisories](https://github.com/Cartooli/mega-eval-skill/security/advisories/new) to report it confidentially. Include:

- A clear description of the issue
- Steps to reproduce or a minimal example
- The potential impact

Maintainers will acknowledge the report within 5 business days and work with you on a resolution and disclosure timeline.

## Scope

**In scope:**
- Bugs in `scripts/` that could cause unintended file writes or data exposure
- Prompt injection risks in skill templates that could cause the pipeline to exfiltrate data or act outside its declared scope
- Plugin packaging issues that could allow a malicious marketplace entry to masquerade as this skill

**Out of scope:**
- Vulnerabilities discovered *in the products being evaluated* by mega-eval (report those to the respective product vendors)
- General Claude / Claude Code platform security (report those to [Anthropic](https://www.anthropic.com/security))
- Social engineering or phishing attempts

## Supported versions

Only the latest release on `master` is actively maintained.
