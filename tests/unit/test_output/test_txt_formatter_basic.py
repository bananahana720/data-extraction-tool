"""Unit tests for TxtFormatter basic functionality (Story 3.5).

Tests plain text formatter creation, delimiter rendering, output contract,
and deterministic output generation.

Test Coverage:
    - AC-3.5-2: Configurable delimiters with chunk numbering
    - AC-3.5 Output Contract: FormatResult protocol compliance
    - Deterministic output generation

Part 1 of 3: Basic formatter functionality.
"""

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
