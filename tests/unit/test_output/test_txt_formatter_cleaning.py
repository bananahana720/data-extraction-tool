"""Unit tests for TxtFormatter text cleaning functionality (Story 3.5).

Tests text cleaning, artifact removal, and UTF-8 encoding with BOM support.

Test Coverage:
    - AC-3.5-1: Clean chunk text (whitespace, artifacts)
    - AC-3.5-5: UTF-8 encoding with BOM support
    - AC-3.5-6: Artifact removal (BOM, JSON, ANSI codes)

Part 2 of 3: Text cleaning and encoding.
"""

import re
from datetime import datetime
from pathlib import Path

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.txt_formatter import TxtFormatter
except ImportError:
    TxtFormatter = None

from data_extract.chunk.models import Chunk, ChunkMetadata

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.formatting]


@pytest.fixture
def sample_clean_chunk() -> Chunk:
    """Create basic chunk with clean text for testing."""
    chunk_metadata = ChunkMetadata(
        entity_tags=[],
        section_context="Executive Summary",
        entity_relationships=[],
        quality=None,
        source_hash="a1b2c3d4e5f6",
        document_type="report",
        word_count=50,
        token_count=65,
        created_at=datetime(2025, 11, 15, 10, 0, 0),
        processing_version="1.0.0-epic3",
        source_file=Path("tests/fixtures/sample.pdf"),
        config_snapshot={"chunk_size": 512, "overlap_pct": 0.15},
    )

    return Chunk(
        id="chunk_001",
        text="This is clean plain text for testing. It has proper paragraph spacing.\n\nThis is a second paragraph.",
        document_id="doc_001",
        position_index=0,
        token_count=65,
        word_count=50,
        entities=[],
        section_context="Executive Summary",
        quality_score=0.93,
        readability_scores={"flesch_kincaid": 8.5, "gunning_fog": 10.2},
        metadata=chunk_metadata,
    )


@pytest.fixture
def sample_chunk_with_artifacts() -> Chunk:
    """Create chunk with markdown/HTML artifacts that need cleaning."""
    chunk_metadata = ChunkMetadata(
        entity_tags=[],
        section_context="Introduction",
        quality=None,
        source_hash="abc123",
        document_type="report",
        word_count=30,
        token_count=40,
        created_at=datetime(2025, 11, 15, 10, 0, 0),
        processing_version="1.0.0-epic3",
        source_file=Path("tests/fixtures/sample.pdf"),
        config_snapshot={},
    )

    return Chunk(
        id="chunk_002",
        text="# Heading\n\nThis has **bold** and *italic* markdown.\n\n<p>HTML tags</p> should be removed.",
        document_id="doc_001",
        position_index=1,
        token_count=40,
        word_count=30,
        entities=[],
        section_context="Introduction",
        quality_score=0.85,
        readability_scores={},
        metadata=chunk_metadata,
    )


@pytest.fixture
def txt_formatter() -> TxtFormatter:
    """Create TxtFormatter instance with default configuration."""
    if TxtFormatter is None:
        pytest.skip("TxtFormatter not implemented yet (RED phase)")
    return TxtFormatter()


class TestTextCleaning:
    """Test text cleaning and artifact removal (AC-3.5-1, AC-3.5-6)."""

    def test_clean_text_preserves_paragraph_spacing(
        self, txt_formatter, sample_clean_chunk, tmp_path
    ):
        """Should preserve intentional paragraph spacing (double newlines)."""
        # GIVEN: Chunk with paragraph spacing
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_clean_chunk]), output_path)

        # THEN: Paragraph spacing should be preserved
        content = output_path.read_text(encoding="utf-8-sig")
        assert "\n\nThis is a second paragraph" in content

    def test_clean_text_removes_markdown_headers(
        self, txt_formatter, sample_chunk_with_artifacts, tmp_path
    ):
        """Should remove markdown # headers while preserving text."""
        # GIVEN: Chunk with markdown header
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_chunk_with_artifacts]), output_path)

        # THEN: Hash symbols should be removed but text preserved
        content = output_path.read_text(encoding="utf-8-sig")
        assert "# Heading" not in content
        assert "Heading" in content

    def test_clean_text_removes_markdown_bold_italic(
        self, txt_formatter, sample_chunk_with_artifacts, tmp_path
    ):
        """Should remove markdown ** and * while preserving text."""
        # GIVEN: Chunk with markdown formatting
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_chunk_with_artifacts]), output_path)

        # THEN: Markdown symbols removed, text preserved
        content = output_path.read_text(encoding="utf-8-sig")
        assert "**bold**" not in content
        assert "*italic*" not in content
        assert "bold" in content
        assert "italic" in content

    def test_clean_text_removes_html_tags(
        self, txt_formatter, sample_chunk_with_artifacts, tmp_path
    ):
        """Should remove HTML tags like <p>, <div>, etc."""
        # GIVEN: Chunk with HTML tags
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_chunk_with_artifacts]), output_path)

        # THEN: HTML tags removed, text preserved
        content = output_path.read_text(encoding="utf-8-sig")
        assert "<p>" not in content
        assert "</p>" not in content
        assert "HTML tags" in content

    def test_clean_text_normalizes_whitespace(self, txt_formatter, tmp_path):
        """Should collapse multiple spaces while preserving paragraph breaks."""
        # GIVEN: Chunk with excessive whitespace
        chunk_metadata = ChunkMetadata(
            entity_tags=[],
            quality=None,
            source_hash="test",
            document_type="text",
            word_count=10,
            token_count=12,
            created_at=datetime(2025, 11, 15, 10, 0, 0),
            processing_version="1.0.0",
            source_file=Path("test.txt"),
            config_snapshot={},
        )

        chunk = Chunk(
            id="test",
            text="Text    with     excessive      spacing.\n\n\n\nToo many newlines.",
            document_id="test",
            position_index=0,
            token_count=12,
            word_count=10,
            entities=[],
            quality_score=0.85,
            metadata=chunk_metadata,
        )

        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([chunk]), output_path)

        # THEN: Whitespace should be normalized
        content = output_path.read_text(encoding="utf-8-sig")
        assert "    with" not in content  # Multiple spaces collapsed
        assert "Text with excessive spacing" in content


class TestArtifactRemoval:
    """Test removal of formatting artifacts (AC-3.5-6)."""

    def test_no_bom_duplication(self, txt_formatter, tmp_path):
        """Should have single BOM at file start, not duplicated per chunk."""
        # GIVEN: Multiple chunks
        chunks = [sample_clean_chunk(), sample_clean_chunk()]  # Two chunks
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter(chunks), output_path)

        # THEN: Only one BOM should exist (at start)
        raw_bytes = output_path.read_bytes()
        bom_count = raw_bytes.count(b"\xef\xbb\xbf")
        assert bom_count == 1

    def test_no_json_braces_in_output(self, txt_formatter, sample_clean_chunk, tmp_path):
        """Should not include stray JSON braces ({, }, [, ]) in plain text output."""
        # GIVEN: Chunks to format
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_clean_chunk]), output_path)

        # THEN: No JSON syntax should appear
        content = output_path.read_text(encoding="utf-8-sig")
        # Remove delimiter lines and metadata (they may have structured content)
        text_lines = [
            line
            for line in content.split("\n")
            if not line.startswith("━━━") and not line.startswith("Source:")
        ]
        text_content = "\n".join(text_lines)
        # Should not have JSON array/object brackets (unless in actual chunk text)
        assert not re.search(r"^\s*[\{\}\[\]]\s*$", text_content, re.MULTILINE)

    def test_no_ansi_escape_codes(self, txt_formatter, tmp_path):
        """Should not include ANSI escape sequences (CLI color codes)."""
        # GIVEN: Chunk that might trigger colored output
        chunk_metadata = ChunkMetadata(
            entity_tags=[],
            quality=None,
            source_hash="test",
            document_type="text",
            word_count=10,
            token_count=12,
            created_at=datetime(2025, 11, 15, 10, 0, 0),
            processing_version="1.0.0",
            source_file=Path("test.txt"),
            config_snapshot={},
        )

        chunk = Chunk(
            id="test",
            text="ERROR: Critical failure detected",
            document_id="test",
            position_index=0,
            token_count=12,
            word_count=10,
            entities=[],
            quality_score=0.88,
            metadata=chunk_metadata,
        )

        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([chunk]), output_path)

        # THEN: No ANSI escape codes should appear
        content = output_path.read_text(encoding="utf-8-sig")
        assert "\x1b[" not in content  # ANSI escape sequence prefix
        assert "\033[" not in content  # Octal representation
