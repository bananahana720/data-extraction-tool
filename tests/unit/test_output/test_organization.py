"""Unit tests for output organization module (Story 3.5 - Bucket 1).

Tests OrganizationStrategy enum, OrganizationResult dataclass, and Organizer class
with comprehensive coverage of all three organization strategies.

Test Coverage:
    - OrganizationStrategy enum values
    - OrganizationResult immutability and fields
    - Organizer.organize() with BY_DOCUMENT strategy
    - Organizer.organize() with BY_ENTITY strategy
    - Organizer.organize() with FLAT strategy
    - Manifest generation and structure
    - Directory structure creation
    - File routing logic
    - Edge cases (empty chunks, missing metadata, Unicode paths)
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.output.organization import OrganizationResult, OrganizationStrategy, Organizer

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.organization]


class TestOrganizationStrategy:
    """Test OrganizationStrategy enum."""

    def test_enum_values(self):
        """Should have three strategy values."""
        assert OrganizationStrategy.BY_DOCUMENT.value == "by_document"
        assert OrganizationStrategy.BY_ENTITY.value == "by_entity"
        assert OrganizationStrategy.FLAT.value == "flat"

    def test_enum_membership(self):
        """Should support membership testing."""
        strategies = [s.value for s in OrganizationStrategy]
        assert "by_document" in strategies
        assert "by_entity" in strategies
        assert "flat" in strategies
        assert len(strategies) == 3


class TestOrganizationResult:
    """Test OrganizationResult dataclass."""

    def test_immutability(self):
        """Should be immutable (frozen dataclass)."""
        result = OrganizationResult(
            strategy=OrganizationStrategy.BY_DOCUMENT,
            output_dir=Path("output/"),
            folders_created=1,
            manifest_path=Path("manifest.json"),
            files_written=1,
        )

        # Should raise exception when trying to modify frozen dataclass
        with pytest.raises(Exception):  # FrozenInstanceError in Python 3.10+
            result.manifest_path = Path("other.json")

    def test_fields(self):
        """Should have all required fields."""
        manifest_path = Path("output/manifest.json")
        strategy = OrganizationStrategy.BY_DOCUMENT

        result = OrganizationResult(
            strategy=strategy,
            output_dir=Path("output/"),
            folders_created=2,
            manifest_path=manifest_path,
            files_written=2,
        )

        assert result.manifest_path == manifest_path
        assert result.files_written == 2
        assert result.strategy == strategy


class TestOrganizerByDocument:
    """Test Organizer with BY_DOCUMENT strategy."""

    @pytest.fixture
    def chunks_single_source(self, tmp_path) -> list:
        """Create chunks from single source document."""
        chunks = []
        for i in range(3):
            metadata = ChunkMetadata(
                source_file=Path("audit_report.pdf"),
                entity_tags=[],
                section_context="Section 1",
            )
            chunk = Chunk(
                id=f"chunk_{i+1:03d}",
                text=f"Chunk {i+1} text content.",
                document_id="doc_001",
                position_index=i,
                token_count=50,
                word_count=40,
                entities=[],
                section_context="Section 1",
                quality_score=0.9,
                readability_scores={},
                metadata=metadata,
            )
            chunks.append(chunk)
        return chunks

    @pytest.fixture
    def chunks_multi_source(self, tmp_path) -> list:
        """Create chunks from multiple source documents."""
        chunks = []
        sources = ["audit_report.pdf", "risk_register.xlsx"]

        for source_idx, source in enumerate(sources):
            for i in range(2):
                metadata = ChunkMetadata(
                    source_file=Path(source),
                    entity_tags=[],
                    section_context="Section 1",
                )
                chunk = Chunk(
                    id=f"chunk_{source_idx}_{i+1:03d}",
                    text=f"Chunk {i+1} from {source}.",
                    document_id=f"doc_{source_idx:03d}",
                    position_index=i,
                    token_count=50,
                    word_count=40,
                    entities=[],
                    section_context="Section 1",
                    quality_score=0.9,
                    readability_scores={},
                    metadata=metadata,
                )
                chunks.append(chunk)
        return chunks

    def test_single_source_creates_one_folder(self, chunks_single_source, tmp_path):
        """Should create one folder for single source document."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_single_source, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check directory structure
        assert (output_dir / "audit_report").exists()
        assert (output_dir / "audit_report").is_dir()

        # Check files written
        assert result.files_written == 3

    def test_multi_source_creates_multiple_folders(self, chunks_multi_source, tmp_path):
        """Should create separate folders for each source document."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_multi_source, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check directory structure
        assert (output_dir / "audit_report").exists()
        assert (output_dir / "risk_register").exists()

        # Check files written (2 chunks per source = 4 total)
        assert result.files_written == 4

    def test_manifest_generation(self, chunks_single_source, tmp_path):
        """Should generate manifest.json with correct structure."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_single_source, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # Check manifest exists
        assert result.manifest_path.exists()
        assert result.manifest_path == output_dir / "manifest.json"

        # Check manifest structure (Story 3.7 - enriched format)
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # Check organization metadata
        assert manifest["organization_strategy"] == "by_document"
        assert manifest["total_chunks"] == 3
        assert "folders" in manifest

        # Check processing metadata (AC-3.7-6)
        assert "generated_at" in manifest
        assert "processing_version" in manifest
        assert "config_snapshot" in manifest
        assert "source_files" in manifest
        assert "entity_summary" in manifest
        assert "quality_summary" in manifest

        # Check folder structure
        assert "audit_report" in manifest["folders"]
        assert manifest["folders"]["audit_report"]["chunk_count"] == 3


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


class TestOrganizerFlat:
    """Test Organizer with FLAT strategy."""

    @pytest.fixture
    def chunks_for_flat(self) -> list:
        """Create chunks for flat organization."""
        chunks = []
        sources = ["audit_report.pdf", "risk_register.xlsx"]

        for source_idx, source in enumerate(sources):
            for i in range(2):
                metadata = ChunkMetadata(
                    source_file=Path(source),
                    entity_tags=[],
                    section_context="Section 1",
                )
                chunk = Chunk(
                    id=f"chunk_{source_idx}_{i+1:03d}",
                    text=f"Chunk {i+1} from {source}.",
                    document_id=f"doc_{source_idx:03d}",
                    position_index=i,
                    token_count=50,
                    word_count=40,
                    entities=[],
                    section_context="Section 1",
                    quality_score=0.9,
                    readability_scores={},
                    metadata=metadata,
                )
                chunks.append(chunk)
        return chunks

    def test_flat_structure_no_subdirectories(self, chunks_for_flat, tmp_path):
        """Should plan flat structure with all files in output directory."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_for_flat, output_dir, OrganizationStrategy.FLAT)

        # Check no subdirectories created (manifest is a file, not directory)
        subdirs = [p for p in output_dir.iterdir() if p.is_dir()]
        assert len(subdirs) == 0

        # Check files were written
        assert result.files_written == 4
        assert result.folders_created == 0

    def test_flat_filenames_include_source(self, chunks_for_flat, tmp_path):
        """Should organize in flat structure (no file writing in organizer)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_for_flat, output_dir, OrganizationStrategy.FLAT)

        # Check result metadata
        assert result.files_written == 4
        assert result.folders_created == 0  # Flat = no subdirectories

        # Check manifest has flat structure
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["organization_strategy"] == "flat"
        assert manifest["total_chunks"] == 4


class TestOrganizerEdgeCases:
    """Test Organizer edge cases and error handling."""

    def test_empty_chunks_list(self, tmp_path):
        """Should handle empty chunks list gracefully."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([], output_dir, OrganizationStrategy.BY_DOCUMENT)

        assert result.manifest_path.exists()
        assert result.files_written == 0
        assert result.strategy == OrganizationStrategy.BY_DOCUMENT

        # Check manifest reflects empty chunks (Story 3.7 format)
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["total_chunks"] == 0
        assert len(manifest["folders"]) == 0

    def test_chunk_without_metadata(self, tmp_path):
        """Should handle chunks without metadata gracefully."""
        chunk = Chunk(
            id="chunk_001",
            text="Content without metadata",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="",
            quality_score=0.9,
            readability_scores={},
            metadata=None,  # No metadata
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Should use document_id as folder name (Story 3.7: "doc_001" or "unknown")
        assert (output_dir / "doc_001").exists()
        assert result.files_written == 1

    def test_unicode_source_names(self, tmp_path):
        """Should handle Unicode characters in source names."""
        metadata = ChunkMetadata(
            source_file=Path("报告_2024.pdf"),  # Chinese characters
            entity_tags=[],
            section_context="",
        )
        chunk = Chunk(
            id="chunk_001",
            text="Unicode test",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Should create sanitized directory
        assert result.files_written == 1
        # Directory should exist (name may be sanitized)
        dirs = list(output_dir.iterdir())
        assert any(d.is_dir() for d in dirs)

    def test_invalid_filename_characters(self, tmp_path):
        """Should sanitize invalid filename characters."""
        metadata = ChunkMetadata(
            source_file=Path("audit/report:2024.pdf"),  # Invalid chars: / and :
            entity_tags=[],
            section_context="",
        )
        chunk = Chunk(
            id="chunk_001",
            text="Sanitization test",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Should sanitize to valid filename (replace invalid chars with _)
        assert result.files_written == 1
        # Check that some directory was created
        dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        assert len(dirs) == 1

    def test_invalid_strategy_raises_error(self, tmp_path):
        """Should handle invalid strategy (enum enforcement)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        # Invalid strategy will raise AttributeError when trying to access .value
        # since OrganizationStrategy is an Enum, passing string directly fails
        with pytest.raises(AttributeError):
            organizer.organize([], output_dir, "invalid_strategy")  # type: ignore

    def test_non_list_chunks_raises_error(self, tmp_path):
        """Should handle non-iterable chunks (materialization fails)."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        # Passing string instead of chunks will fail when trying to access .metadata
        with pytest.raises(AttributeError):
            organizer.organize("not a list", output_dir, OrganizationStrategy.BY_DOCUMENT)  # type: ignore


class TestOrganizerHelperMethods:
    """Test Organizer private helper methods (Story 3.7 - updated API)."""

    def test_sanitize_path_removes_invalid_chars(self):
        """Should remove invalid path characters and convert to lowercase."""
        organizer = Organizer()

        assert organizer._sanitize_path("Audit/Report") == "audit_report"
        assert organizer._sanitize_path("File:Name") == "file_name"
        assert organizer._sanitize_path("File*Name") == "file_name"
        assert organizer._sanitize_path('File"Name') == "file_name"
        # Multiple consecutive special chars → multiple underscores (not collapsed)
        assert organizer._sanitize_path("File<>Name") == "file__name"

    def test_sanitize_path_handles_spaces(self):
        """Should replace spaces with underscores and convert to lowercase."""
        organizer = Organizer()

        assert organizer._sanitize_path("Audit Report 2024") == "audit_report_2024"

    def test_sanitize_path_handles_empty_string(self):
        """Should return 'unnamed' for empty string."""
        organizer = Organizer()

        assert organizer._sanitize_path("") == "unnamed"
        assert organizer._sanitize_path("   ") == "unnamed"  # Spaces only → stripped → unnamed

    def test_sanitize_path_handles_special_chars(self):
        """Should sanitize various special characters."""
        organizer = Organizer()

        assert organizer._sanitize_path("Risk-Assessment-2024") == "risk_assessment_2024"
        # Parentheses and dots → underscores (not collapsed)
        assert organizer._sanitize_path("Report (Final).pdf") == "report__final__pdf"
        assert organizer._sanitize_path("Data@2024#Final!") == "data_2024_final"


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

        # Validate ISO 8601 format with timezone (e.g., "2025-11-16T01:40:40.277671+00:00")
        from datetime import datetime

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

        # Check structure (may be None/null if no quality metadata)
        assert "average_quality_score" in quality_summary
        assert "min_quality_score" in quality_summary
        assert "max_quality_score" in quality_summary
        assert "chunks_with_quality" in quality_summary
        assert "quality_flags" in quality_summary


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
