"""Unit tests for TxtFormatter metadata functionality (Story 3.5).

Tests optional metadata header generation with source file, entity tags,
and quality scores.

Test Coverage:
    - AC-3.5-3: Optional metadata header generation
    - Compact metadata format (3-4 lines max)

Part 3 of 3: Metadata header functionality.
"""

from datetime import datetime
from pathlib import Path

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.txt_formatter import TxtFormatter
except ImportError:
    TxtFormatter = None

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.chunk.quality import QualityScore

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.formatting]


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
