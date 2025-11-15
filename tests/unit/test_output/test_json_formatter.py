"""Unit tests for JsonFormatter (Story 3.4 - ATDD RED PHASE).

Tests JSON formatter creation, chunk serialization, metadata header generation,
pretty-printing, and schema validation.

Test Coverage:
    - AC-3.4-1: JSON structure with chunk text and metadata
    - AC-3.4-2: Valid parsable JSON output
    - AC-3.4-3: Complete metadata fields serialization
    - AC-3.4-4: Pretty-printed output with indentation
    - AC-3.4-6: Configuration and version in JSON header

These tests WILL FAIL until JsonFormatter is implemented (GREEN phase).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.base import FormatResult
    from data_extract.output.formatters.json_formatter import JsonFormatter
except ImportError:
    JsonFormatter = None
    FormatResult = None

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


@pytest.fixture
def json_formatter_no_validation() -> JsonFormatter:
    """Create JsonFormatter instance with validation disabled."""
    if JsonFormatter is None:
        pytest.skip("JsonFormatter not implemented yet (RED phase)")
    return JsonFormatter(validate=False)


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


class TestChunkSerialization:
    """Test individual chunk serialization with complete metadata (AC-3.4-1, AC-3.4-3)."""

    def test_chunk_object_includes_required_fields(self, json_formatter, sample_chunks, tmp_path):
        """Should serialize chunk with chunk_id, text, metadata, entities, quality (AC-3.4-1)."""
        # GIVEN: JsonFormatter and sample chunk
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunk to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Each chunk should have required fields
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        chunk = json_data["chunks"][0]
        assert "chunk_id" in chunk
        assert "text" in chunk
        assert "metadata" in chunk
        assert "entities" in chunk
        assert "quality" in chunk

    def test_chunk_metadata_includes_all_fields(self, json_formatter, sample_chunks, tmp_path):
        """Should serialize all ChunkMetadata fields (AC-3.4-3)."""
        # GIVEN: JsonFormatter and enriched chunk
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunk to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Chunk metadata should include all fields from Story 3.3
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        chunk_meta = json_data["chunks"][0]["metadata"]

        # Story 3.3 fields
        assert "quality" in chunk_meta
        assert "source_hash" in chunk_meta
        assert "document_type" in chunk_meta
        assert "word_count" in chunk_meta
        assert "token_count" in chunk_meta
        assert "created_at" in chunk_meta
        assert "processing_version" in chunk_meta

        # Story 3.2 fields
        assert "entity_tags" in chunk_meta
        assert "section_context" in chunk_meta
        assert "entity_relationships" in chunk_meta

    def test_quality_score_nested_object(self, json_formatter, sample_chunks, tmp_path):
        """Should serialize quality as nested object with all subfields (AC-3.4-3)."""
        # GIVEN: JsonFormatter and chunk with quality score
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunk to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Quality should be nested object with all fields
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        quality = json_data["chunks"][0]["quality"]
        assert "readability_flesch_kincaid" in quality
        assert "readability_gunning_fog" in quality
        assert "ocr_confidence" in quality
        assert "completeness" in quality
        assert "coherence" in quality
        assert "overall" in quality
        assert "flags" in quality

    def test_entities_array_serialization(self, json_formatter, sample_chunks, tmp_path):
        """Should serialize entities as array of EntityReference objects (AC-3.4-1)."""
        # GIVEN: JsonFormatter and chunk with entities
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunk to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Entities should be array with entity fields
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        # Entities in metadata.entity_tags
        entity_tags = json_data["chunks"][0]["metadata"]["entity_tags"]
        assert isinstance(entity_tags, list)
        assert len(entity_tags) >= 1

        entity = entity_tags[0]
        assert "entity_type" in entity
        assert "entity_id" in entity
        assert "start_pos" in entity
        assert "end_pos" in entity
        assert "is_partial" in entity

    def test_datetime_fields_iso_8601_format(self, json_formatter, sample_chunks, tmp_path):
        """Should format datetime fields as ISO 8601 strings (AC-3.4-3)."""
        # GIVEN: JsonFormatter and chunk with datetime fields
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunk to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Datetime fields should be ISO 8601 strings
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        # Metadata timestamp
        timestamp = json_data["metadata"]["processing_timestamp"]
        assert isinstance(timestamp, str)
        datetime.fromisoformat(timestamp)  # Should parse without error

        # Chunk created_at
        created_at = json_data["chunks"][0]["metadata"]["created_at"]
        assert isinstance(created_at, str)
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))  # Handle Z suffix


class TestValidJsonOutput:
    """Test JSON output validity and parseability (AC-3.4-2)."""

    def test_output_is_valid_json(self, json_formatter, sample_chunks, tmp_path):
        """Should produce valid JSON parsable by json.load() (AC-3.4-2)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: JSON should parse without errors
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data is not None
        assert isinstance(json_data, dict)

    def test_output_not_json_lines_format(self, json_formatter, sample_chunks, tmp_path):
        """Should produce single JSON file, not newline-delimited JSON Lines (AC-3.4-2)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: File should contain single JSON object (not multiple lines)
        with open(output_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # Single json.loads() should parse entire file (BOM already stripped by utf-8-sig)
        json_data = json.loads(content)
        assert isinstance(json_data, dict)
        assert "chunks" in json_data

    def test_utf8_encoding_with_bom(self, json_formatter, sample_chunks, tmp_path):
        """Should write UTF-8 with BOM for Windows compatibility (AC-3.4-2)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: File should have UTF-8 encoding (with or without BOM)
        with open(output_path, "rb") as f:
            raw_bytes = f.read()

        # Check for UTF-8 BOM (optional but preferred for Windows)
        # File should at least be valid UTF-8
        content = raw_bytes.decode("utf-8-sig")  # Handles both BOM and no-BOM
        assert len(content) > 0

    def test_no_trailing_commas_strict_json(self, json_formatter, sample_chunks, tmp_path):
        """Should produce strict JSON with no trailing commas (AC-3.4-4)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: JSON should parse (strict parser rejects trailing commas)
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data is not None  # If parsing succeeds, no trailing commas


class TestPrettyPrintedOutput:
    """Test JSON pretty-printing and formatting (AC-3.4-4)."""

    def test_json_indented_with_2_spaces(self, json_formatter, sample_chunks, tmp_path):
        """Should format JSON with 2-space indentation (AC-3.4-4)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: JSON should have indentation
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for indentation (lines should start with spaces)
        lines = content.split("\n")
        indented_lines = [line for line in lines if line.startswith("  ")]
        assert len(indented_lines) > 0, "JSON should have indented lines"

    def test_fields_ordered_logically(self, json_formatter, sample_chunks, tmp_path):
        """Should order chunk fields logically: text, metadata, entities, quality (AC-3.4-4)."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Chunk fields should be in logical order
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check field order by finding positions in text
        # (Python 3.7+ dicts maintain insertion order)
        chunk_start = content.find('"chunks"')
        text_pos = content.find('"text"', chunk_start)
        metadata_pos = content.find('"metadata"', chunk_start)

        # text should come before metadata in first chunk
        assert text_pos < metadata_pos, "text should come before metadata"


class TestEmptyAndEdgeCases:
    """Test edge cases: empty chunks, single chunk, large outputs (AC-3.4-1, AC-3.4-2)."""

    def test_empty_chunks_list_valid_json(self, json_formatter, tmp_path):
        """Should handle empty chunks list and produce valid JSON with zero chunks."""
        # GIVEN: JsonFormatter and empty chunks list
        output_path = tmp_path / "output.json"

        # WHEN: Formatting empty chunks
        json_formatter.format_chunks(iter([]), output_path)

        # THEN: JSON should be valid with empty chunks array
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data["metadata"]["chunk_count"] == 0
        assert json_data["chunks"] == []

    def test_single_chunk_valid_output(self, json_formatter, sample_enriched_chunk, tmp_path):
        """Should handle single chunk correctly (minimal valid output)."""
        # GIVEN: JsonFormatter and single chunk
        output_path = tmp_path / "output.json"

        # WHEN: Formatting single chunk
        json_formatter.format_chunks(iter([sample_enriched_chunk]), output_path)

        # THEN: JSON should have exactly one chunk
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data["metadata"]["chunk_count"] == 1
        assert len(json_data["chunks"]) == 1

    def test_large_chunks_list_performance(self, json_formatter, sample_enriched_chunk, tmp_path):
        """Should handle 100+ chunks efficiently (large output test)."""
        # GIVEN: JsonFormatter and 100 chunks
        large_chunks_list = [sample_enriched_chunk] * 100
        output_path = tmp_path / "output.json"

        # WHEN: Formatting 100 chunks
        import time

        start_time = time.time()
        json_formatter.format_chunks(iter(large_chunks_list), output_path)
        duration = time.time() - start_time

        # THEN: Should complete in reasonable time (<1 second target)
        assert duration < 2.0, f"JSON generation took {duration:.2f}s (target: <1s)"

        # AND: JSON should have 100 chunks
        with open(output_path, "r", encoding="utf-8-sig") as f:
            json_data = json.load(f)

        assert json_data["metadata"]["chunk_count"] == 100


class TestFormatResultMetadata:
    """Test FormatResult return value with stats (AC-3.4-1)."""

    def test_format_result_includes_stats(self, json_formatter, sample_chunks, tmp_path):
        """Should return FormatResult with format_type, output_path, chunk_count, file_size."""
        # GIVEN: JsonFormatter and sample chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks to JSON
        result = json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: FormatResult should include required fields
        assert result.format_type == "json"
        assert result.output_path == output_path
        assert result.chunk_count == 3
        assert result.file_size_bytes > 0
        assert result.duration_seconds >= 0

    def test_format_result_errors_empty_on_success(self, json_formatter, sample_chunks, tmp_path):
        """Should return FormatResult with empty errors list on success."""
        # GIVEN: JsonFormatter and valid chunks
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks successfully
        result = json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Errors should be empty
        assert result.errors == []


class TestSchemaValidationIntegration:
    """Test schema validation during formatting (AC-3.4-7)."""

    def test_valid_output_passes_schema_validation(self, json_formatter, sample_chunks, tmp_path):
        """Should validate output against JSON schema when validation enabled."""
        # GIVEN: JsonFormatter with validation enabled
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks with valid data
        result = json_formatter.format_chunks(iter(sample_chunks), output_path)

        # THEN: Validation should pass (no errors)
        assert result.errors == []

    def test_validation_disabled_skips_schema_check(
        self, json_formatter_no_validation, sample_chunks, tmp_path
    ):
        """Should skip schema validation when validate=False."""
        # GIVEN: JsonFormatter with validation disabled
        output_path = tmp_path / "output.json"

        # WHEN: Formatting chunks
        json_formatter_no_validation.format_chunks(iter(sample_chunks), output_path)

        # THEN: Should complete successfully (validation skipped)
        assert output_path.exists()
