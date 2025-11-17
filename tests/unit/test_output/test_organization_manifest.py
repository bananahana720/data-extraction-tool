"""Tests for manifest enrichment and structured logging.

Tests manifest generation features from Story 3.7, including:
- Manifest metadata enrichment (AC-3.7-6)
- Structured logging for organization operations (AC-3.7-7)
- Configuration snapshot
- Entity and quality summaries
- ISO 8601 timestamps

Test Coverage:
    - Manifest configuration snapshot
    - ISO 8601 timestamp format
    - Source file hashes
    - Entity summary generation
    - Quality summary generation
    - Structured logging events
"""

import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.output.organization import OrganizationStrategy, Organizer

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.organization]


class TestStory37ManifestEnrichment:
    """Test Story 3.7 AC-3.7-6: Manifest metadata enrichment."""

    @pytest.fixture
    def chunks_with_metadata(self) -> list:
        """Create chunks with full metadata for enrichment testing."""
        entity = EntityReference(
            entity_type="risk",
            entity_id="RISK-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="risk context",
        )

        metadata = ChunkMetadata(
            source_file=Path("audit_report.pdf"),
            entity_tags=[entity],
            section_context="Risk Section",
        )

        chunk = Chunk(
            id="chunk_001",
            text="Test content",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Risk Section",
            quality_score=0.85,
            readability_scores={},
            metadata=metadata,
        )

        return [chunk]

    @pytest.fixture
    def chunks_with_multiple_entities(self) -> list:
        """Create chunks with various entity types for summary testing."""
        chunks = []

        # Chunk with risk entities
        risk_entity = EntityReference(
            entity_type="risk",
            entity_id="RISK-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="risk",
        )
        risk_metadata = ChunkMetadata(
            source_file=Path("doc1.pdf"),
            entity_tags=[risk_entity],
            section_context="Risks",
        )
        chunks.append(
            Chunk(
                id="chunk_001",
                text="Risk text",
                document_id="doc_001",
                position_index=0,
                token_count=50,
                word_count=40,
                entities=[],
                section_context="Risks",
                quality_score=0.9,
                readability_scores={},
                metadata=risk_metadata,
            )
        )

        # Chunk with control entities
        control_entity = EntityReference(
            entity_type="control",
            entity_id="CTRL-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="control",
        )
        control_metadata = ChunkMetadata(
            source_file=Path("doc2.pdf"),
            entity_tags=[control_entity],
            section_context="Controls",
        )
        chunks.append(
            Chunk(
                id="chunk_002",
                text="Control text",
                document_id="doc_002",
                position_index=0,
                token_count=45,
                word_count=38,
                entities=[],
                section_context="Controls",
                quality_score=0.75,
                readability_scores={},
                metadata=control_metadata,
            )
        )

        # Chunk with multiple entities
        process_entity = EntityReference(
            entity_type="process",
            entity_id="PROC-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="process",
        )
        mixed_metadata = ChunkMetadata(
            source_file=Path("doc3.pdf"),
            entity_tags=[risk_entity, process_entity],
            section_context="Mixed",
        )
        chunks.append(
            Chunk(
                id="chunk_003",
                text="Mixed text",
                document_id="doc_003",
                position_index=0,
                token_count=60,
                word_count=50,
                entities=[],
                section_context="Mixed",
                quality_score=0.95,
                readability_scores={},
                metadata=mixed_metadata,
            )
        )

        return chunks

    def test_manifest_includes_config_snapshot(self, chunks_with_metadata, tmp_path):
        """Should include config_snapshot in manifest (AC-3.7-6)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        config = {"chunk_size": 512, "overlap_pct": 0.15, "respect_sentences": True}

        result = organizer.organize(
            chunks_with_metadata,
            output_dir,
            OrganizationStrategy.BY_DOCUMENT,
            config_snapshot=config,
        )

        # Check manifest includes config
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "config_snapshot" in manifest
        assert manifest["config_snapshot"] == config
        assert manifest["config_snapshot"]["chunk_size"] == 512
        assert manifest["config_snapshot"]["overlap_pct"] == 0.15

    def test_manifest_iso8601_timestamp(self, chunks_with_metadata, tmp_path):
        """Should include ISO 8601 timestamp in manifest (AC-3.7-6)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_metadata, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check manifest timestamp format
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "generated_at" in manifest

        # Validate ISO 8601 format with timezone
        timestamp_str = manifest["generated_at"]
        # Should parse without error
        parsed = datetime.fromisoformat(timestamp_str)
        assert parsed is not None
        # Should have timezone info
        assert "+" in timestamp_str or "Z" in timestamp_str

    def test_manifest_source_hashes(self, chunks_with_metadata, tmp_path):
        """Should extract source file hashes in manifest (AC-3.7-6)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_metadata, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check manifest includes source_files
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "source_files" in manifest
        # Even without source_hash in metadata, should have source_files dict
        assert isinstance(manifest["source_files"], dict)

    def test_manifest_entity_summary(self, chunks_with_metadata, tmp_path):
        """Should include entity summary in manifest (AC-3.7-6)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_metadata, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check manifest includes entity summary
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "entity_summary" in manifest
        entity_summary = manifest["entity_summary"]

        # Check structure
        assert "total_entities" in entity_summary
        assert "entity_types" in entity_summary
        assert "unique_entity_ids" in entity_summary

        # Check values for our test data
        assert entity_summary["total_entities"] == 1
        assert "risk" in entity_summary["entity_types"]
        assert "RISK-001" in entity_summary["unique_entity_ids"]

    def test_manifest_quality_summary(self, chunks_with_metadata, tmp_path):
        """Should include quality summary in manifest (AC-3.7-6)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_metadata, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check manifest includes quality summary
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "quality_summary" in manifest
        quality_summary = manifest["quality_summary"]

        # Check structure
        assert "average_quality_score" in quality_summary
        assert "min_quality_score" in quality_summary
        assert "max_quality_score" in quality_summary
        assert "chunks_with_quality" in quality_summary
        assert "quality_flags" in quality_summary

    def test_comprehensive_entity_summary(self, chunks_with_multiple_entities, tmp_path):
        """Should aggregate entity summary across all chunks."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_multiple_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check comprehensive entity summary
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        entity_summary = manifest["entity_summary"]

        # Should have all entity types
        assert set(entity_summary["entity_types"]) == {"risk", "control", "process"}
        # Should count unique entities (RISK-001 appears twice)
        assert entity_summary["total_entities"] == 3
        # Should have all unique IDs
        assert "RISK-001" in entity_summary["unique_entity_ids"]
        assert "CTRL-001" in entity_summary["unique_entity_ids"]
        assert "PROC-001" in entity_summary["unique_entity_ids"]

    def test_quality_statistics_aggregation(self, chunks_with_multiple_entities, tmp_path):
        """Should calculate quality statistics across chunks."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_multiple_entities, output_dir, OrganizationStrategy.FLAT
        )

        # Check quality statistics
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        quality_summary = manifest["quality_summary"]

        # Check calculated statistics (0.9, 0.75, 0.95)
        assert quality_summary["chunks_with_quality"] == 3
        assert quality_summary["min_quality_score"] == 0.75
        assert quality_summary["max_quality_score"] == 0.95
        # Average should be (0.9 + 0.75 + 0.95) / 3 = 0.8666...
        assert 0.86 <= quality_summary["average_quality_score"] <= 0.87


class TestStory37StructuredLogging:
    """Test Story 3.7 AC-3.7-7: Structured logging for organization operations."""

    @pytest.fixture
    def simple_chunks(self) -> list:
        """Create simple chunks for logging tests."""
        metadata = ChunkMetadata(
            source_file=Path("test.pdf"),
            entity_tags=[],
            section_context="Test",
        )

        chunk = Chunk(
            id="chunk_001",
            text="Test",
            document_id="doc_001",
            position_index=0,
            token_count=10,
            word_count=5,
            entities=[],
            section_context="Test",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        return [chunk]

    @patch("data_extract.output.organization.logger")
    def test_logs_organization_start(self, mock_logger, simple_chunks, tmp_path):
        """Should log organization_start with strategy and chunk count (AC-3.7-7)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        organizer.organize(simple_chunks, output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Verify organization_start was logged
        mock_logger.info.assert_any_call(
            "organization_start",
            strategy="by_document",
            output_dir=str(output_dir),
            chunk_count=1,
            config_snapshot_provided=False,
        )

    @patch("data_extract.output.organization.logger")
    def test_logs_organization_complete(self, mock_logger, simple_chunks, tmp_path):
        """Should log organization_complete with results (AC-3.7-7)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        organizer.organize(simple_chunks, output_dir, OrganizationStrategy.FLAT)

        # Verify organization_complete was logged with results
        calls = [
            call
            for call in mock_logger.info.call_args_list
            if call[0][0] == "organization_complete"
        ]
        assert len(calls) > 0

        # Check the call has expected parameters
        call_kwargs = calls[0][1]
        assert call_kwargs["strategy"] == "flat"
        assert call_kwargs["folders_created"] == 0  # FLAT strategy
        assert call_kwargs["files_written"] == 1

    @patch("data_extract.output.organization.logger")
    def test_logs_manifest_generation(self, mock_logger, simple_chunks, tmp_path):
        """Should log manifest generation events (AC-3.7-7)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        organizer.organize(simple_chunks, output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Verify manifest_generation_start was logged
        mock_logger.debug.assert_any_call("manifest_generation_start", strategy="by_document")

    @patch("data_extract.output.organization.logger")
    def test_logging_with_config_snapshot(self, mock_logger, simple_chunks, tmp_path):
        """Should log config_snapshot_provided=True when config passed (AC-3.7-7)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        config = {"chunk_size": 512}

        organizer.organize(
            simple_chunks, output_dir, OrganizationStrategy.BY_DOCUMENT, config_snapshot=config
        )

        # Verify organization_start logged with config flag
        mock_logger.info.assert_any_call(
            "organization_start",
            strategy="by_document",
            output_dir=str(output_dir),
            chunk_count=1,
            config_snapshot_provided=True,
        )

    @patch("data_extract.output.organization.logger")
    def test_logging_error_handling(self, mock_logger, tmp_path):
        """Should log errors during organization operations."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        # Test with invalid input that might cause errors
        with pytest.raises(AttributeError):
            organizer.organize("invalid", output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Should have logged the start before error
        assert mock_logger.info.called or mock_logger.error.called
