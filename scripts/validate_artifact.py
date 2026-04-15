#!/usr/bin/env python3
"""Validate markdown artifacts against lightweight JSON contracts."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+")


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    line_index: int


def extract_headings(lines: list[str]) -> list[Heading]:
    """Return markdown headings in document order."""
    headings: list[Heading] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append(
                Heading(level=len(match.group(1)), title=match.group(2).strip(), line_index=index)
            )
    return headings


def first_heading_title(text: str) -> str | None:
    """Return the first markdown heading title, if any."""
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            return match.group(2).strip()
    return None


def build_section_map(text: str) -> dict[str, str]:
    """Map heading titles to their section bodies."""
    lines = text.splitlines()
    headings = extract_headings(lines)
    section_map: dict[str, str] = {}

    for index, heading in enumerate(headings):
        end_index = len(lines)
        for later in headings[index + 1 :]:
            if later.level <= heading.level:
                end_index = later.line_index
                break

        body = "\n".join(lines[heading.line_index + 1 : end_index]).strip()
        section_map[heading.title] = body

    return section_map


def count_words(text: str) -> int:
    """Count words using a simple alphanumeric matcher."""
    return len(re.findall(r"\b\w+\b", text))


def has_bullet_list(text: str) -> bool:
    """Return True when a section contains at least one markdown bullet."""
    return any(BULLET_RE.match(line) for line in text.splitlines())


def load_schema(schema_path: Path) -> dict:
    """Load a JSON artifact schema."""
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_text(text: str, schema: dict) -> list[str]:
    """Return validation errors for a markdown artifact."""
    errors: list[str] = []
    sections = build_section_map(text)
    headings = set(sections.keys())

    required_title = schema.get("required_title")
    if required_title:
        actual_title = first_heading_title(text)
        if actual_title != required_title:
            errors.append(
                f"Expected first heading '{required_title}', found '{actual_title or '<none>'}'."
            )

    for heading in schema.get("required_headings", []):
        if heading not in headings:
            errors.append(f"Missing required heading: '{heading}'.")

    for heading in schema.get("required_nonempty_sections", []):
        content = sections.get(heading, "")
        if not content.strip():
            errors.append(f"Section '{heading}' must not be empty.")

    for heading in schema.get("required_bullet_sections", []):
        content = sections.get(heading, "")
        if content and not has_bullet_list(content):
            errors.append(f"Section '{heading}' must contain at least one markdown bullet.")

    for heading, minimum in schema.get("section_min_words", {}).items():
        content = sections.get(heading, "")
        if content and count_words(content) < int(minimum):
            errors.append(
                f"Section '{heading}' must contain at least {minimum} words; found {count_words(content)}."
            )

    for heading, substrings in schema.get("section_required_substrings", {}).items():
        content = sections.get(heading, "")
        if not content:
            continue
        for substring in substrings:
            if substring not in content:
                errors.append(f"Section '{heading}' must include '{substring}'.")

    for pattern in schema.get("forbidden_patterns", []):
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"Artifact matched forbidden pattern: {pattern}")

    return errors


def validate_file(artifact_path: Path, schema_path: Path) -> list[str]:
    """Validate one markdown artifact file."""
    text = artifact_path.read_text(encoding="utf-8")
    schema = load_schema(schema_path)
    return validate_text(text, schema)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_artifact.py <artifact-path> <schema-path>", file=sys.stderr)
        return 2

    artifact_path = Path(sys.argv[1]).resolve()
    schema_path = Path(sys.argv[2]).resolve()

    if not artifact_path.exists():
        print(f"Artifact not found: {artifact_path}", file=sys.stderr)
        return 2

    if not schema_path.exists():
        print(f"Schema not found: {schema_path}", file=sys.stderr)
        return 2

    errors = validate_file(artifact_path, schema_path)
    if errors:
        print(f"Validation failed for {artifact_path.name}:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validation passed for {artifact_path.name}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
