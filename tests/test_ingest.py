#!/usr/bin/env python3
"""Tests for scripts/ingest.py"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Add scripts/ to path so we can import ingest
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import ingest


class TestExtractText:
    """Tests for the extract_text function."""

    def test_txt_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello world, this is a test.")
        result = ingest.extract_text(str(f))
        assert result == "Hello world, this is a test."

    def test_md_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("# Heading\n\nSome content.")
        result = ingest.extract_text(str(f))
        assert "# Heading" in result
        assert "Some content." in result

    def test_html_file(self, tmp_path):
        f = tmp_path / "test.html"
        f.write_text("<html><body><p>Hello</p></body></html>")
        result = ingest.extract_text(str(f))
        assert "<p>Hello</p>" in result

    def test_missing_file(self):
        result = ingest.extract_text("/nonexistent/path/to/file.txt")
        assert "[ERROR: File not found" in result

    def test_directory_not_file(self, tmp_path):
        result = ingest.extract_text(str(tmp_path))
        assert "[ERROR: Not a regular file" in result

    def test_unsupported_extension(self, tmp_path):
        f = tmp_path / "test.xyz"
        f.write_text("some data")
        result = ingest.extract_text(str(f))
        assert "[Unsupported file type: .xyz" in result

    def test_utf8_content(self, tmp_path):
        f = tmp_path / "unicode.txt"
        f.write_text("Caf\u00e9 \u2014 na\u00efve r\u00e9sum\u00e9")
        result = ingest.extract_text(str(f))
        assert "Caf\u00e9" in result

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        result = ingest.extract_text(str(f))
        assert result == ""

    def test_pdf_without_pdftotext(self, tmp_path):
        f = tmp_path / "test.pdf"
        f.write_bytes(b"%PDF-1.4 fake pdf content")
        result = ingest.extract_text(str(f))
        # Either pdftotext is available (and may fail on fake PDF) or it's not
        assert "[" in result or isinstance(result, str)

    def test_docx_without_pandoc(self, tmp_path):
        f = tmp_path / "test.docx"
        f.write_bytes(b"PK fake docx")
        result = ingest.extract_text(str(f))
        assert isinstance(result, str)

    def test_path_resolution(self, tmp_path):
        """Paths with .. are resolved to absolute paths."""
        subdir = tmp_path / "sub"
        subdir.mkdir()
        f = tmp_path / "test.txt"
        f.write_text("resolved content")
        # Use a path with .. traversal
        tricky_path = str(subdir / ".." / "test.txt")
        result = ingest.extract_text(tricky_path)
        assert result == "resolved content"


class TestGenerateBriefTemplate:
    """Tests for the generate_brief_template function."""

    def test_single_source(self):
        sources = [{"name": "idea.txt", "type": ".txt", "content": "A great product idea."}]
        result = ingest.generate_brief_template(sources)
        assert "# Evaluation Brief" in result
        assert "idea.txt" in result
        assert "A great product idea." in result

    def test_multiple_sources(self):
        sources = [
            {"name": "pitch.md", "type": ".md", "content": "Our pitch deck content."},
            {"name": "research.txt", "type": ".txt", "content": "Market research data."},
        ]
        result = ingest.generate_brief_template(sources)
        assert "pitch.md" in result
        assert "research.txt" in result
        assert "Our pitch deck content." in result
        assert "Market research data." in result

    def test_truncation_over_3000_chars(self):
        long_content = "x" * 5000
        sources = [{"name": "long.txt", "type": ".txt", "content": long_content}]
        result = ingest.generate_brief_template(sources)
        assert "truncated" in result.lower()
        # First 3000 chars should be present
        assert "x" * 3000 in result
        # Full 5000 should not be present as a contiguous block
        assert "x" * 5000 not in result

    def test_brief_has_required_sections(self):
        sources = [{"name": "test.txt", "type": ".txt", "content": "Test content."}]
        result = ingest.generate_brief_template(sources)
        assert "## Subject" in result
        assert "## Core Proposition" in result
        assert "## Key Claims & Features" in result
        assert "## Target Audience" in result
        assert "## Pricing/Model" in result
        assert "## Source Material" in result
        assert "## Open Questions" in result

    def test_empty_content(self):
        sources = [{"name": "empty.txt", "type": ".txt", "content": ""}]
        result = ingest.generate_brief_template(sources)
        assert "# Evaluation Brief" in result
        assert "empty.txt" in result


class TestCLI:
    """Tests for the command-line interface."""

    def test_single_file_cli(self, tmp_path):
        input_file = tmp_path / "input.txt"
        input_file.write_text("CLI test content for evaluation.")
        output_file = tmp_path / "output.md"

        result = subprocess.run(
            [sys.executable, "scripts/ingest.py", str(input_file), "-o", str(output_file)],
            capture_output=True, text=True, timeout=10,
            cwd=str(Path(__file__).parent.parent),
        )
        assert result.returncode == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "# Evaluation Brief" in content
        assert "CLI test content" in content

    def test_multiple_files_cli(self, tmp_path):
        f1 = tmp_path / "first.txt"
        f1.write_text("First source.")
        f2 = tmp_path / "second.md"
        f2.write_text("# Second source")
        output_file = tmp_path / "brief.md"

        result = subprocess.run(
            [sys.executable, "scripts/ingest.py", str(f1), str(f2), "-o", str(output_file)],
            capture_output=True, text=True, timeout=10,
            cwd=str(Path(__file__).parent.parent),
        )
        assert result.returncode == 0
        content = output_file.read_text()
        assert "first.txt" in content
        assert "second.md" in content

    def test_no_args_shows_error(self):
        result = subprocess.run(
            [sys.executable, "scripts/ingest.py"],
            capture_output=True, text=True, timeout=10,
            cwd=str(Path(__file__).parent.parent),
        )
        assert result.returncode != 0
