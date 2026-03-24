#!/usr/bin/env python3
"""Print promotion-candidate and failure-mode lines from a mega-eval run-log (stdout only; never writes)."""
from __future__ import annotations

import re
import sys


def section_after_heading(text: str, heading_starts_with: str) -> str | None:
    """Match ## headings that begin with heading_starts_with (allows parentheticals)."""
    pattern = rf"^##\s+{re.escape(heading_starts_with)}[^\n]*\n(.*?)(?=^##\s|\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else None


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: suggest_learnings.py <path-to-run-log.md>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()

    found = False
    promo = section_after_heading(text, "Promotion candidates")
    if promo:
        for line in promo.splitlines():
            s = line.strip()
            if s.startswith("- [ ]") or s.startswith("- [x]"):
                print(s)
                found = True

    fail = section_after_heading(text, "Failure modes")
    if fail:
        for line in fail.splitlines():
            s = line.strip()
            if s.startswith("-") and len(s) > 1:
                print(s)
                found = True

    if not found:
        print("(no matching lines in Promotion candidates or Failure modes)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
