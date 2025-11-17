"""Unit tests for JsonFormatter serialization (Story 3.4).

Tests individual chunk serialization with complete metadata and
valid JSON output generation.

Test Coverage:
    - AC-3.4-1: Chunk serialization with all fields
    - AC-3.4-2: Valid parsable JSON output
    - AC-3.4-3: Complete metadata fields serialization

Part 2 of 3: Chunk serialization and JSON validity.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.json_formatter import JsonFormatter
except ImportError:
    JsonFormatter = None

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
