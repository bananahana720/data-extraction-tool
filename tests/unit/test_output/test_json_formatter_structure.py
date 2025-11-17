"""Unit tests for JsonFormatter structure and metadata (Story 3.4).

Tests JSON formatter creation, JSON structure generation with metadata header,
and FormattingResult return values.

Test Coverage:
    - AC-3.4-1: JSON structure with chunk text and metadata
    - AC-3.4-6: Configuration and version in JSON header
    - FormattingResult metadata

Part 1 of 3: JSON structure and configuration.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.base import FormattingResult
    from data_extract.output.formatters.json_formatter import JsonFormatter
except ImportError:
    JsonFormatter = None
    FormattingResult = None

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.chunk.quality import QualityScore

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.formatting]


@pytest.fixture
def sample_enriched_chunk() -> Chunk:
    """Create enriched chunk with metadata, entities, and quality scores."""
    entity_ref = EntityReference(
        entity_type="risk",
        entity_id="RISK-001",
        start_pos=50,
        end_pos=70,
        is_partial=False,
        context_snippet="...identified risk of data breach...",
    )

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
        entity_tags=[entity_ref],
        section_context="Risk Assessment > Identified Risks",
        entity_relationships=[("RISK-001", "mitigated_by", "CTRL-042")],
        quality=quality_score,
        source_hash="63c038826f241106a3c8aa1a3416f3698f6d541effa8aef852648f1112c166f6",
        document_type="report",
        word_count=150,
        token_count=200,
        created_at=datetime(2025, 11, 14, 20, 30, 0),
        processing_version="1.0.0-epic3",
        source_file=Path("tests/fixtures/audit_report.pdf"),
        config_snapshot={"chunk_size": 512, "overlap_pct": 0.15, "entity_aware": True},
    )

    return Chunk(
        id="test_doc_001",
        text="Risk Assessment Section. We have identified risk of data breach in the customer database. This risk requires immediate attention and mitigation controls.",
        document_id="test_doc",
        position_index=0,
        token_count=200,
        word_count=150,
        entities=[],
        section_context="Risk Assessment > Identified Risks",
        quality_score=0.93,
        readability_scores={"flesch_kincaid": 8.5, "gunning_fog": 10.2},
        metadata=chunk_metadata,
    )


@pytest.fixture
def sample_chunks(sample_enriched_chunk) -> List[Chunk]:
    """Create list of enriched chunks for testing."""
    return [sample_enriched_chunk] * 3  # 3 identical chunks for testing


@pytest.fixture
def json_formatter() -> JsonFormatter:
    """Create JsonFormatter instance with validation enabled."""
    if JsonFormatter is None:
        pytest.skip("JsonFormatter not implemented yet (RED phase)")
    return JsonFormatter(validate=True)


class TestJsonFormatterCreation:
    """Test JsonFormatter instantiation and configuration (AC-3.4-1)."""

    def test_formatter_creation_with_validation(self):
        """Should create JsonFormatter with validation enabled by default."""
        # GIVEN/WHEN: JsonFormatter instantiated with default settings
        formatter = JsonFormatter()

        # THEN: Validation should be enabled
        assert formatter.validate is True

    def test_formatter_creation_without_validation(self):
        """Should create JsonFormatter with validation disabled when specified."""
        # GIVEN/WHEN: JsonFormatter instantiated with validate=False
        formatter = JsonFormatter(validate=False)

        # THEN: Validation should be disabled
        assert formatter.validate is False

    def test_formatter_creation_with_custom_schema_path(self, tmp_path):
        """Should accept custom schema path for validation."""
        # GIVEN: Custom schema path
        schema_path = tmp_path / "custom_schema.json"

        # WHEN: JsonFormatter instantiated with custom schema
        formatter = JsonFormatter(schema_path=schema_path, validate=True)

        # THEN: Schema path should be stored
        assert formatter.schema_path == schema_path


class TestJsonStructureGeneration:
    """Test JSON structure creation with metadata and chunks (AC-3.4-1, AC-3.4-6)."""

    def test_json_structure_has_metadata_and_chunks(self, json_formatter, sample_chunks, tmp_path):
        """Should generate JSON with root metadata object and chunks array."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: JSON file should exist
        assert output_path.exists()

        # AND: JSON should have metadata and chunks keys
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert "metadata" in json_data
        assert "chunks" in json_data
        assert isinstance(json_data["metadata"], dict)
        assert isinstance(json_data["chunks"], list)

    def test_metadata_header_includes_required_fields(
        self, json_formatter, sample_chunks, tmp_path
    ):
        """Should include processing version, timestamp, configuration in metadata header (AC-3.4-6)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Metadata header should include required fields
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        metadata = json_data["metadata"]
        assert "processing_version" in metadata
        assert "processing_timestamp" in metadata
        assert "configuration" in metadata
        assert "source_documents" in metadata
        assert "chunk_count" in metadata

    def test_metadata_configuration_includes_chunking_params(
        self, json_formatter, sample_chunks, tmp_path
    ):
        """Should include chunk_size, overlap_pct, flags in configuration (AC-3.4-6)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Configuration should include chunking parameters
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        config = json_data["metadata"]["configuration"]
        assert "chunk_size" in config
        assert "overlap_pct" in config
        assert "entity_aware" in config
        assert "quality_enrichment" in config

    def test_chunk_count_matches_actual_chunks(self, json_formatter, sample_chunks, tmp_path):
        """Should set chunk_count to actual number of chunks in output (AC-3.4-6)."""
        # GIVEN: JsonFormatter and 3 sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: chunk_count should be 3
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data["metadata"]["chunk_count"] == 3
        assert len(json_data["chunks"]) == 3


class TestFormattingResultMetadata:
    """Test FormattingResult return value with stats (AC-3.4-1)."""

    def test_format_result_includes_stats(self, json_formatter, sample_chunks, tmp_path):
        """Should return FormattingResult with format_type, output_path, chunk_count, file_size."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        result = json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: FormattingResult should include required fields
        assert result.format_type == "json"
        assert result.output_path == output_path
        assert result.chunk_count == 3
        assert result.file_size_bytes > 0
        assert result.duration_seconds >= 0

    def test_format_result_errors_empty_on_success(self, json_formatter, sample_chunks, tmp_path):
        """Should return FormattingResult with empty errors list on success."""
        # GIVEN: JsonFormatter and valid chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks successfully
        result = json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Errors should be empty
        assert result.errors == []
