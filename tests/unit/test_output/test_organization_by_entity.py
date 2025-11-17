"""Tests for BY_ENTITY organization strategy.

Tests Organizer functionality specifically for the BY_ENTITY strategy,
which creates one folder per entity type (risks/, controls/, processes/, unclassified/).

Test Coverage:
    - Entity type folder creation
    - Chunks with entity tags routing
    - Unclassified folder for chunks without entities
    - Mixed entity handling
    - Manifest generation for BY_ENTITY strategy
"""

import json
from pathlib import Path

import pytest

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.output.organization import OrganizationStrategy, Organizer

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.organization]


class TestOrganizerByEntity:
    """Test Organizer with BY_ENTITY strategy."""

    @pytest.fixture
    def chunks_with_entities(self) -> list:
        """Create chunks with entity tags."""
        chunks = []

        # Chunk with risk entities
        entity1 = EntityReference(
            entity_type="risk",
            entity_id="RISK-001",
            start_pos=0,
            end_pos=20,
            is_partial=False,
            context_snippet="risk context",
        )
        metadata1 = ChunkMetadata(
            source_file=Path("audit_report.pdf"),
            entity_tags=[entity1],
            section_context="Risk Section",
        )
        chunk1 = Chunk(
            id="chunk_001",
            text="Risk content",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Risk Section",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata1,
        )
        chunks.append(chunk1)

        # Chunk with control entities
        entity2 = EntityReference(
            entity_type="control",
            entity_id="CTRL-001",
            start_pos=0,
            end_pos=20,
            is_partial=False,
            context_snippet="control context",
        )
        metadata2 = ChunkMetadata(
            source_file=Path("audit_report.pdf"),
            entity_tags=[entity2],
            section_context="Control Section",
        )
        chunk2 = Chunk(
            id="chunk_002",
            text="Control content",
            document_id="doc_001",
            position_index=1,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Control Section",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata2,
        )
        chunks.append(chunk2)

        # Chunk with no entities
        metadata3 = ChunkMetadata(
            source_file=Path("audit_report.pdf"),
            entity_tags=[],
            section_context="General Section",
        )
        chunk3 = Chunk(
            id="chunk_003",
            text="General content",
            document_id="doc_001",
            position_index=2,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="General Section",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata3,
        )
        chunks.append(chunk3)

        return chunks

    @pytest.fixture
    def chunks_mixed_entities(self) -> list:
        """Create chunks with multiple entity types."""
        chunks = []

        # Chunk with multiple entity types
        entity1 = EntityReference(
            entity_type="risk",
            entity_id="RISK-002",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="risk",
        )
        entity2 = EntityReference(
            entity_type="control",
            entity_id="CTRL-002",
            start_pos=20,
            end_pos=30,
            is_partial=False,
            context_snippet="control",
        )
        metadata = ChunkMetadata(
            source_file=Path("combined.pdf"),
            entity_tags=[entity1, entity2],
            section_context="Mixed Section",
        )
        chunk = Chunk(
            id="chunk_mixed",
            text="Risk and control content",
            document_id="doc_002",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Mixed Section",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )
        chunks.append(chunk)

        # Chunk with process entity
        entity3 = EntityReference(
            entity_type="process",
            entity_id="PROC-001",
            start_pos=0,
            end_pos=15,
            is_partial=False,
            context_snippet="process",
        )
        metadata2 = ChunkMetadata(
            source_file=Path("process_doc.pdf"),
            entity_tags=[entity3],
            section_context="Process Section",
        )
        chunk2 = Chunk(
            id="chunk_process",
            text="Process content",
            document_id="doc_003",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Process Section",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata2,
        )
        chunks.append(chunk2)

        return chunks

    def test_creates_folders_per_entity_type(self, chunks_with_entities, tmp_path):
        """Should create separate folders for each entity type."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        organizer.organize(chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY)

        # Check directory structure (Story 3.7 uses "unclassified" not "uncategorized")
        assert (output_dir / "risk").exists()
        assert (output_dir / "control").exists()
        assert (output_dir / "unclassified").exists()

    def test_uncategorized_folder_for_no_entities(self, chunks_with_entities, tmp_path):
        """Should put chunks without entities in unclassified folder."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check unclassified folder exists (Story 3.7 uses "unclassified")
        assert (output_dir / "unclassified").exists()
        assert result.files_written == 3

    def test_manifest_includes_entity_type(self, chunks_with_entities, tmp_path):
        """Should include entity types in manifest."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check manifest (Story 3.7 enriched format)
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Check folders contain entity types
        folder_names = list(manifest["folders"].keys())
        assert "risk" in folder_names
        assert "control" in folder_names

    def test_chunks_with_multiple_entities(self, chunks_mixed_entities, tmp_path):
        """Should handle chunks with multiple entity types."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_mixed_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check that folders are created for all entity types
        assert (output_dir / "risk").exists()
        assert (output_dir / "control").exists()
        assert (output_dir / "process").exists()

        # Chunk with multiple entities should be in primary entity folder
        assert result.files_written == 2

    def test_entity_summary_in_manifest(self, chunks_with_entities, tmp_path):
        """Should include entity summary in manifest for BY_ENTITY strategy."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check manifest entity summary
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "entity_summary" in manifest
        entity_summary = manifest["entity_summary"]

        # Check structure
        assert "total_entities" in entity_summary
        assert "entity_types" in entity_summary
        assert "unique_entity_ids" in entity_summary

        # Check values match test data
        assert entity_summary["total_entities"] == 2  # RISK-001, CTRL-001
        assert set(entity_summary["entity_types"]) == {"risk", "control"}
        assert "RISK-001" in entity_summary["unique_entity_ids"]
        assert "CTRL-001" in entity_summary["unique_entity_ids"]

    def test_entity_folder_naming_sanitization(self, tmp_path):
        """Should sanitize entity type names for folder creation."""
        # Create chunk with special entity type name
        entity = EntityReference(
            entity_type="risk/control",  # Invalid folder name
            entity_id="SPECIAL-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="special",
        )
        metadata = ChunkMetadata(
            source_file=Path("test.pdf"),
            entity_tags=[entity],
            section_context="Test",
        )
        chunk = Chunk(
            id="chunk_001",
            text="Special entity test",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Test",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_ENTITY)

        # Should create sanitized folder
        assert result.files_written == 1
        # Check that directory was created with sanitized name
        dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        assert len(dirs) == 1

    def test_empty_entity_tags_goes_to_unclassified(self, tmp_path):
        """Should route chunks with empty entity_tags to unclassified folder."""
        metadata = ChunkMetadata(
            source_file=Path("test.pdf"),
            entity_tags=[],  # Empty entity tags
            section_context="Test",
        )
        chunk = Chunk(
            id="chunk_001",
            text="No entities",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Test",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_ENTITY)

        # Should have unclassified folder
        assert (output_dir / "unclassified").exists()
        assert result.files_written == 1
