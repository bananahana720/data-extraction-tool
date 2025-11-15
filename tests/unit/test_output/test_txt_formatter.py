"""Unit tests for TxtFormatter (Story 3.5 - ATDD RED PHASE).

Tests plain text formatter creation, delimiter rendering, metadata headers,
text cleaning, encoding, and artifact removal.

Test Coverage:
    - AC-3.5-1: Clean chunk text (whitespace, artifacts)
    - AC-3.5-2: Configurable delimiters with chunk numbering
    - AC-3.5-3: Optional metadata header generation
    - AC-3.5-5: UTF-8 encoding with BOM support
    - AC-3.5-6: Artifact removal (BOM, JSON, ANSI codes)

These tests WILL FAIL until TxtFormatter is implemented (GREEN phase).
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.base import FormatResult
    from data_extract.output.formatters.txt_formatter import TxtFormatter
except ImportError:
    TxtFormatter = None
    FormatResult = None

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.chunk.quality import QualityScore

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.formatting]


@pytest.fixture
def sample_clean_chunk() -> Chunk:
    """Create basic chunk with clean text for testing."""
    quality_score = QualityScore(
        readability_flesch_kincaid=8.5,
        readability_gunning_fog=10.2,
        ocr_confidence=0.99,
        completeness=0.95,
        coherence=0.88,
        overall=0.93,
        flags=[],
    )

    chunk_metadata = ChunkMetadata(
        entity_tags=[],
        section_context="Executive Summary",
        entity_relationships=[],
        quality=quality_score,
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
def sample_chunk_with_entities() -> Chunk:
    """Create chunk with entity tags for metadata header testing."""
    entity1 = EntityReference(
        entity_type="risk",
        entity_id="RISK-001",
        start_pos=20,
        end_pos=40,
        is_partial=False,
        context_snippet="...identified risk...",
    )

    entity2 = EntityReference(
        entity_type="control",
        entity_id="CTRL-042",
        start_pos=60,
        end_pos=80,
        is_partial=False,
        context_snippet="...mitigation control...",
    )

    quality_score = QualityScore(
        readability_flesch_kincaid=7.0,
        readability_gunning_fog=9.0,
        ocr_confidence=1.0,
        completeness=1.0,
        coherence=0.95,
        overall=0.96,
        flags=[],
    )

    chunk_metadata = ChunkMetadata(
        entity_tags=[entity1, entity2],
        section_context="Risk Assessment > Controls",
        entity_relationships=[("RISK-001", "mitigated_by", "CTRL-042")],
        quality=quality_score,
        source_hash="xyz789",
        document_type="audit",
        word_count=80,
        token_count=100,
        created_at=datetime(2025, 11, 15, 11, 30, 0),
        processing_version="1.0.0-epic3",
        source_file=Path("tests/fixtures/audit_report.pdf"),
        config_snapshot={"chunk_size": 512, "overlap_pct": 0.15, "entity_aware": True},
    )

    return Chunk(
        id="chunk_003",
        text="Risk RISK-001 has been identified in the authentication module. Control CTRL-042 provides mitigation through multi-factor authentication.",
        document_id="doc_002",
        position_index=0,
        token_count=100,
        word_count=80,
        entities=[],
        section_context="Risk Assessment > Controls",
        quality_score=0.96,
        readability_scores={"flesch_kincaid": 7.0, "gunning_fog": 9.0},
        metadata=chunk_metadata,
    )


@pytest.fixture
def sample_chunks(sample_clean_chunk, sample_chunk_with_entities) -> List[Chunk]:
    """Create list of chunks for multi-chunk testing."""
    return [sample_clean_chunk, sample_chunk_with_entities]


@pytest.fixture
def txt_formatter() -> TxtFormatter:
    """Create TxtFormatter instance with default configuration."""
    if TxtFormatter is None:
        pytest.skip("TxtFormatter not implemented yet (RED phase)")
    return TxtFormatter()


@pytest.fixture
def txt_formatter_with_metadata() -> TxtFormatter:
    """Create TxtFormatter with metadata headers enabled."""
    if TxtFormatter is None:
        pytest.skip("TxtFormatter not implemented yet (RED phase)")
    return TxtFormatter(include_metadata=True)


@pytest.fixture
def txt_formatter_custom_delimiter() -> TxtFormatter:
    """Create TxtFormatter with custom delimiter."""
    if TxtFormatter is None:
        pytest.skip("TxtFormatter not implemented yet (RED phase)")
    return TxtFormatter(delimiter="--- CHUNK {{n}} ---")


class TestTxtFormatterCreation:
    """Test TxtFormatter instantiation and configuration (AC-3.5-2, AC-3.5-3)."""

    def test_formatter_creation_default_settings(self):
        """Should create TxtFormatter with default delimiter and no metadata."""
        # GIVEN/WHEN: TxtFormatter instantiated with defaults
        formatter = TxtFormatter()

        # THEN: Should have default configuration
        assert formatter.include_metadata is False
        assert "━━━ CHUNK" in formatter.delimiter
        assert "{{n}}" in formatter.delimiter

    def test_formatter_creation_with_metadata_enabled(self):
        """Should create TxtFormatter with metadata headers when specified."""
        # GIVEN/WHEN: TxtFormatter instantiated with include_metadata=True
        formatter = TxtFormatter(include_metadata=True)

        # THEN: Metadata should be enabled
        assert formatter.include_metadata is True

    def test_formatter_creation_with_custom_delimiter(self):
        """Should create TxtFormatter with custom delimiter pattern."""
        # GIVEN: Custom delimiter pattern
        custom_delimiter = "--- CHUNK {{n}} ---"

        # WHEN: TxtFormatter instantiated with custom delimiter
        formatter = TxtFormatter(delimiter=custom_delimiter)

        # THEN: Custom delimiter should be stored
        assert formatter.delimiter == custom_delimiter


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


class TestDelimiterRendering:
    """Test delimiter generation and chunk numbering (AC-3.5-2)."""

    def test_default_delimiter_renders_correctly(self, txt_formatter, sample_chunks, tmp_path):
        """Should render default delimiter ━━━ CHUNK {{n}} ━━━ between chunks."""
        # GIVEN: Multiple chunks
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT in concatenated mode
        txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Delimiter should appear between chunks
        content = output_path.read_text(encoding="utf-8-sig")
        assert "━━━ CHUNK 001 ━━━" in content
        assert "━━━ CHUNK 002 ━━━" in content

    def test_custom_delimiter_renders_correctly(
        self, txt_formatter_custom_delimiter, sample_chunks, tmp_path
    ):
        """Should render custom delimiter pattern."""
        # GIVEN: Formatter with custom delimiter
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter_custom_delimiter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Custom delimiter should appear
        content = output_path.read_text(encoding="utf-8-sig")
        assert "--- CHUNK 001 ---" in content
        assert "--- CHUNK 002 ---" in content

    def test_delimiter_chunk_numbering_sequential(self, txt_formatter, sample_chunks, tmp_path):
        """Should number chunks sequentially (001, 002, 003, etc.)."""
        # GIVEN: Multiple chunks
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Numbering should be sequential with zero-padding
        content = output_path.read_text(encoding="utf-8-sig")
        assert "CHUNK 001" in content
        assert "CHUNK 002" in content
        # Verify no CHUNK 000
        assert "CHUNK 000" not in content


class TestMetadataHeaders:
    """Test optional metadata header generation (AC-3.5-3)."""

    def test_metadata_header_omitted_when_disabled(
        self, txt_formatter, sample_chunk_with_entities, tmp_path
    ):
        """Should not include metadata headers when include_metadata=False."""
        # GIVEN: Formatter with metadata disabled (default)
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        txt_formatter.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: No metadata headers should appear
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Source:" not in content
        assert "Entities:" not in content
        assert "Quality:" not in content

    def test_metadata_header_included_when_enabled(
        self, txt_formatter_with_metadata, sample_chunk_with_entities, tmp_path
    ):
        """Should include compact metadata header when include_metadata=True."""
        # GIVEN: Formatter with metadata enabled
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        txt_formatter_with_metadata.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: Metadata header should precede chunk text
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Source:" in content
        assert "audit_report.pdf" in content

    def test_metadata_header_includes_source_file(
        self, txt_formatter_with_metadata, sample_chunk_with_entities, tmp_path
    ):
        """Should include source file path in metadata header."""
        # GIVEN: Chunk with source file metadata
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting with metadata enabled
        txt_formatter_with_metadata.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: Source file should appear in header
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Source:" in content
        assert "audit_report.pdf" in content

    def test_metadata_header_includes_entity_tags(
        self, txt_formatter_with_metadata, sample_chunk_with_entities, tmp_path
    ):
        """Should include entity IDs as comma-separated list in header."""
        # GIVEN: Chunk with entity tags
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting with metadata enabled
        txt_formatter_with_metadata.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: Entity IDs should appear in header
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Entities:" in content or "Tags:" in content
        assert "RISK-001" in content
        assert "CTRL-042" in content

    def test_metadata_header_includes_quality_score(
        self, txt_formatter_with_metadata, sample_chunk_with_entities, tmp_path
    ):
        """Should include overall quality score in header."""
        # GIVEN: Chunk with quality metadata
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting with metadata enabled
        txt_formatter_with_metadata.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: Quality score should appear in header
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Quality:" in content or "Score:" in content
        assert "0.96" in content or "96" in content

    def test_metadata_header_compact_format(
        self, txt_formatter_with_metadata, sample_chunk_with_entities, tmp_path
    ):
        """Should use compact format (max 3-4 lines) for metadata header."""
        # GIVEN: Chunk with full metadata
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting with metadata
        txt_formatter_with_metadata.format_chunks(iter([sample_chunk_with_entities]), output_path)

        # THEN: Header should be compact (not verbose)
        content = output_path.read_text(encoding="utf-8-sig")
        # Extract header section (before first chunk text)
        header_end = content.index("Risk RISK-001")
        header = content[:header_end]
        header_lines = [line for line in header.split("\n") if line.strip()]
        # Should be <= 5 lines (delimiter + 3-4 metadata lines)
        assert len(header_lines) <= 6


class TestEncodingAndNewlines:
    """Test UTF-8 encoding and newline handling (AC-3.5-5)."""

    def test_utf8_sig_encoding_with_bom(self, txt_formatter, sample_clean_chunk, tmp_path):
        """Should write files with UTF-8-sig encoding (BOM present)."""
        # GIVEN: Chunk to format
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([sample_clean_chunk]), output_path)

        # THEN: File should have UTF-8 BOM
        raw_bytes = output_path.read_bytes()
        assert raw_bytes[:3] == b"\xef\xbb\xbf"  # UTF-8 BOM

    def test_unicode_character_preservation(self, txt_formatter, tmp_path):
        """Should preserve Unicode characters (emoji, accents, special chars)."""
        # GIVEN: Chunk with Unicode characters
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
            text="Café résumé 🚀 naïve Zürich €100",
            document_id="test",
            position_index=0,
            token_count=12,
            word_count=10,
            entities=[],
            quality_score=0.95,
            metadata=chunk_metadata,
        )

        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter([chunk]), output_path)

        # THEN: Unicode should be preserved
        content = output_path.read_text(encoding="utf-8-sig")
        assert "Café" in content
        assert "résumé" in content
        assert "🚀" in content
        assert "naïve" in content
        assert "Zürich" in content
        assert "€100" in content


class TestArtifactRemoval:
    """Test removal of formatting artifacts (AC-3.5-6)."""

    def test_no_bom_duplication(self, txt_formatter, sample_chunks, tmp_path):
        """Should have single BOM at file start, not duplicated per chunk."""
        # GIVEN: Multiple chunks
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Only one BOM should exist (at start)
        raw_bytes = output_path.read_bytes()
        bom_count = raw_bytes.count(b"\xef\xbb\xbf")
        assert bom_count == 1

    def test_no_json_braces_in_output(self, txt_formatter, sample_chunks, tmp_path):
        """Should not include stray JSON braces ({, }, [, ]) in plain text output."""
        # GIVEN: Chunks to format
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting to TXT
        txt_formatter.format_chunks(iter(sample_chunks), output_path)

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


class TestFormatResultContract:
    """Test FormatResult return value and BaseFormatter protocol (AC-3.5-2)."""

    def test_format_chunks_returns_format_result(self, txt_formatter, sample_chunks, tmp_path):
        """Should return FormatResult with format_type='txt'."""
        # GIVEN: Chunks to format
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        result = txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Should return FormatResult
        assert isinstance(result, FormatResult)
        assert result.format_type == "txt"

    def test_format_result_includes_statistics(self, txt_formatter, sample_chunks, tmp_path):
        """Should include chunk count and duration statistics."""
        # GIVEN: Chunks to format
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        result = txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Statistics should be populated
        assert result.chunk_count == len(sample_chunks)
        assert result.duration_seconds > 0.0
        assert result.output_path == output_path

    def test_format_result_errors_empty_on_success(self, txt_formatter, sample_chunks, tmp_path):
        """Should return empty errors list on successful formatting."""
        # GIVEN: Valid chunks
        output_path = tmp_path / "output.txt"

        # WHEN: Formatting chunks
        result = txt_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: No errors should be present
        assert len(result.errors) == 0


class TestDeterministicOutput:
    """Test output determinism and consistency (AC-3.5-1)."""

    def test_same_chunks_produce_identical_output(self, txt_formatter, sample_chunks, tmp_path):
        """Should produce byte-identical output for same input chunks."""
        # GIVEN: Same chunks formatted twice
        output_path1 = tmp_path / "output1.txt"
        output_path2 = tmp_path / "output2.txt"

        # WHEN: Formatting same chunks twice
        txt_formatter.format_chunks(iter(sample_chunks), output_path1)
        txt_formatter.format_chunks(iter(sample_chunks), output_path2)

        # THEN: Outputs should be byte-identical
        content1 = output_path1.read_bytes()
        content2 = output_path2.read_bytes()
        assert content1 == content2
