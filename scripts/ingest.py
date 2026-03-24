#!/usr/bin/env python3
"""
Input ingestion helper for Mega Eval.
Extracts text content from various file types and produces a unified brief template.

Usage:
    python ingest.py <file_path> [<file_path2> ...] [--output eval-brief.md]

Supports: .txt, .md, .pdf (via pdftotext), .docx (via pandoc), .pptx (via pandoc), .html
For URLs, use WebFetch directly — this script handles local files only.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_text(file_path: str) -> str:
    """Extract text content from a file based on its extension."""
    p = Path(file_path)
    ext = p.suffix.lower()

    if not p.exists():
        return f"[ERROR: File not found: {file_path}]"

    if ext in ('.txt', '.md', '.html'):
        return p.read_text(encoding='utf-8', errors='replace')

    if ext == '.pdf':
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', str(p), '-'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            # Fallback to python
            return f"[PDF extraction via pdftotext failed. Use Read tool on the PDF directly.]"
        except FileNotFoundError:
            return f"[pdftotext not available. Use Read tool on the PDF directly.]"

    if ext == '.docx':
        try:
            result = subprocess.run(
                ['pandoc', str(p), '-t', 'plain', '--wrap=none'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            return f"[pandoc extraction failed for {file_path}. Use Read tool directly.]"
        except FileNotFoundError:
            return f"[pandoc not available. Use Read tool on the docx directly.]"

    if ext == '.pptx':
        try:
            result = subprocess.run(
                ['pandoc', str(p), '-t', 'plain', '--wrap=none'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            return f"[pandoc extraction failed for {file_path}.]"
        except FileNotFoundError:
            return f"[pandoc not available for pptx extraction.]"

    return f"[Unsupported file type: {ext}. Read the file manually.]"


def generate_brief_template(sources: list[dict]) -> str:
    """Generate an evaluation brief template with extracted content."""
    source_sections = []
    all_content = []

    for s in sources:
        source_sections.append(f"- **{s['name']}** ({s['type']}): {len(s['content'].split())} words extracted")
        all_content.append(f"### Source: {s['name']}\n\n{s['content'][:3000]}")
        if len(s['content']) > 3000:
            all_content[-1] += f"\n\n[... truncated, {len(s['content'].split())} total words ...]"

    template = f"""# Evaluation Brief

## Subject
[TO BE FILLED: Name of the idea/product/feature set]

## Core Proposition
[TO BE FILLED: 1-2 sentences — what is this, and what problem does it solve?]

## Key Claims & Features
[TO BE FILLED: Extract from source material below]

## Target Audience (stated or inferred)
[TO BE FILLED]

## Pricing/Model (if known)
[TO BE FILLED]

## Source Material
{chr(10).join(source_sections)}

## Open Questions
[TO BE FILLED: Anything unclear or missing]

---

# Raw Extracted Content

{chr(10).join(all_content)}
"""
    return template


def main():
    parser = argparse.ArgumentParser(description='Mega Eval input ingestion')
    parser.add_argument('files', nargs='+', help='Input file paths')
    parser.add_argument('--output', '-o', default='eval-brief.md', help='Output file path')
    args = parser.parse_args()

    sources = []
    for f in args.files:
        p = Path(f)
        content = extract_text(f)
        sources.append({
            'name': p.name,
            'type': p.suffix.lower() or 'text',
            'content': content
        })
        print(f"Extracted: {p.name} ({len(content.split())} words)", file=sys.stderr)

    brief = generate_brief_template(sources)
    Path(args.output).write_text(brief)
    print(f"\nBrief template written to: {args.output}", file=sys.stderr)
    print(f"Total sources: {len(sources)}", file=sys.stderr)


if __name__ == '__main__':
    main()
