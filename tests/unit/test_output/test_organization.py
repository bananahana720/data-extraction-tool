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
            manifest_path=Path("manifest.json"),
            files_created=[Path("file1.txt")],
            strategy_used=OrganizationStrategy.BY_DOCUMENT,
        )

        # Should raise exception when trying to modify frozen dataclass
        with pytest.raises(Exception):  # FrozenInstanceError in Python 3.10+
            result.manifest_path = Path("other.json")

    def test_fields(self):
        """Should have all required fields."""
        manifest_path = Path("output/manifest.json")
        files = [Path("output/chunk_001.txt"), Path("output/chunk_002.txt")]
        strategy = OrganizationStrategy.BY_DOCUMENT

        result = OrganizationResult(
            manifest_path=manifest_path,
            files_created=files,
            strategy_used=strategy,
        )

        assert result.manifest_path == manifest_path
        assert result.files_created == files
        assert result.strategy_used == strategy


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

        # Check files created
        assert len(result.files_created) == 3
        for i in range(1, 4):
            expected_path = output_dir / "audit_report" / f"chunk_{i:03d}.txt"
            assert expected_path in result.files_created

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

        # Check files created (2 chunks per source = 4 total)
        assert len(result.files_created) == 4

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

        # Check manifest structure
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "metadata" in manifest
        assert "files" in manifest

        # Check metadata fields
        assert manifest["metadata"]["strategy"] == "by_document"
        assert manifest["metadata"]["total_chunks"] == 3
        assert manifest["metadata"]["total_files"] == 3
        assert "created_at" in manifest["metadata"]
        assert "processing_version" in manifest["metadata"]

        # Check files list
        assert len(manifest["files"]) == 3
        for file_entry in manifest["files"]:
            assert "path" in file_entry
            assert "chunk_count" in file_entry
            assert "source" in file_entry


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

        # Check directory structure
        assert (output_dir / "risk").exists()
        assert (output_dir / "control").exists()
        assert (output_dir / "uncategorized").exists()

    def test_uncategorized_folder_for_no_entities(self, chunks_with_entities, tmp_path):
        """Should plan to put chunks without entities in uncategorized folder."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check uncategorized folder path appears in file mappings
        file_paths = [str(f) for f in result.files_created]
        assert any("uncategorized" in str(p) for p in file_paths)

    def test_manifest_includes_entity_type(self, chunks_with_entities, tmp_path):
        """Should include entity_type in manifest entries."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_with_entities, output_dir, OrganizationStrategy.BY_ENTITY
        )

        # Check manifest
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # At least one file should have entity_type
        entity_types = [f.get("entity_type", "") for f in manifest["files"]]
        assert "risk" in entity_types or "control" in entity_types


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

        # Check no subdirectories created (only manifest exists)
        subdirs = [p for p in output_dir.iterdir() if p.is_dir()]
        assert len(subdirs) == 0

        # Check file paths are flat (no directory separators in relative paths)
        for file_path in result.files_created:
            relative = file_path.relative_to(output_dir)
            # Flat structure means no parent directories
            assert relative.parent == Path(".")

    def test_flat_filenames_include_source(self, chunks_for_flat, tmp_path):
        """Should plan filenames prefixed with source document name."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_for_flat, output_dir, OrganizationStrategy.FLAT)

        # Check filename pattern in planned paths: {source}_chunk_{n:03d}.txt
        expected_patterns = [
            "audit_report_chunk_001.txt",
            "audit_report_chunk_002.txt",
            "risk_register_chunk_001.txt",
            "risk_register_chunk_002.txt",
        ]

        file_names = [f.name for f in result.files_created]
        for expected in expected_patterns:
            assert expected in file_names


class TestOrganizerEdgeCases:
    """Test Organizer edge cases and error handling."""

    def test_empty_chunks_list(self, tmp_path):
        """Should handle empty chunks list gracefully."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([], output_dir, OrganizationStrategy.BY_DOCUMENT)

        assert result.manifest_path.exists()
        assert len(result.files_created) == 0
        assert result.strategy_used == OrganizationStrategy.BY_DOCUMENT

        # Check manifest reflects empty chunks
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["metadata"]["total_chunks"] == 0
        assert manifest["metadata"]["total_files"] == 0

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

        # Should use default "unknown_source" folder
        assert (output_dir / "unknown_source").exists()
        assert len(result.files_created) == 1

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
        assert len(result.files_created) == 1
        # Directory should exist (name may be sanitized)
        dirs = list(output_dir.iterdir())
        assert any(d.is_dir() and d.name != "manifest.json" for d in dirs)

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
        assert len(result.files_created) == 1
        # Check that some directory was created
        dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        assert len(dirs) == 1

    def test_invalid_strategy_raises_error(self, tmp_path):
        """Should raise ValueError for unknown strategy."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        # Create a mock invalid strategy (bypass enum)
        with pytest.raises(ValueError, match="Unknown organization strategy"):
            organizer.organize([], output_dir, "invalid_strategy")  # type: ignore

    def test_non_list_chunks_raises_error(self, tmp_path):
        """Should raise ValueError if chunks is not a list."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        with pytest.raises(ValueError, match="chunks must be a list"):
            organizer.organize("not a list", output_dir, OrganizationStrategy.BY_DOCUMENT)  # type: ignore


class TestOrganizerHelperMethods:
    """Test Organizer private helper methods."""

    def test_sanitize_filename_removes_invalid_chars(self):
        """Should remove invalid filename characters."""
        organizer = Organizer()

        assert organizer._sanitize_filename("audit/report") == "audit_report"
        assert organizer._sanitize_filename("file:name") == "file_name"
        assert organizer._sanitize_filename("file*name") == "file_name"
        assert organizer._sanitize_filename('file"name') == "file_name"
        assert organizer._sanitize_filename("file<>name") == "file_name"  # Collapsed underscores

    def test_sanitize_filename_handles_spaces(self):
        """Should replace spaces with underscores."""
        organizer = Organizer()

        assert organizer._sanitize_filename("audit report 2024") == "audit_report_2024"

    def test_sanitize_filename_handles_empty_string(self):
        """Should return 'unnamed' for empty string."""
        organizer = Organizer()

        assert organizer._sanitize_filename("") == "unnamed"
        assert organizer._sanitize_filename("   ") == "unnamed"  # Spaces only → stripped → unnamed

    def test_sanitize_filename_truncates_long_names(self):
        """Should truncate very long filenames."""
        organizer = Organizer()

        long_name = "a" * 250
        sanitized = organizer._sanitize_filename(long_name)

        assert len(sanitized) <= 200

    def test_extract_source_name_from_path(self):
        """Should extract source name from Path object."""
        organizer = Organizer()

        metadata = ChunkMetadata(
            source_file=Path("audit_report.pdf"),
            entity_tags=[],
        )
        chunk = Chunk(
            id="chunk_001",
            text="test",
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

        assert organizer._extract_source_name(chunk) == "audit_report"

    def test_extract_source_name_from_string(self):
        """Should extract source name from string."""
        organizer = Organizer()

        metadata = ChunkMetadata(
            source_file="audit_report.pdf",  # String instead of Path
            entity_tags=[],
        )
        chunk = Chunk(
            id="chunk_001",
            text="test",
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

        assert organizer._extract_source_name(chunk) == "audit_report"

    def test_extract_source_name_missing_metadata(self):
        """Should return 'unknown_source' when metadata missing."""
        organizer = Organizer()

        chunk = Chunk(
            id="chunk_001",
            text="test",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="",
            quality_score=0.9,
            readability_scores={},
            metadata=None,
        )

        assert organizer._extract_source_name(chunk) == "unknown_source"

    def test_get_entity_types_extracts_unique_types(self):
        """Should extract unique entity types from chunk."""
        organizer = Organizer()

        entity1 = EntityReference(
            entity_type="risk",
            entity_id="RISK-001",
            start_pos=0,
            end_pos=10,
            is_partial=False,
            context_snippet="",
        )
        entity2 = EntityReference(
            entity_type="control",
            entity_id="CTRL-001",
            start_pos=20,
            end_pos=30,
            is_partial=False,
            context_snippet="",
        )
        entity3 = EntityReference(
            entity_type="risk",  # Duplicate type
            entity_id="RISK-002",
            start_pos=40,
            end_pos=50,
            is_partial=False,
            context_snippet="",
        )

        metadata = ChunkMetadata(
            entity_tags=[entity1, entity2, entity3],
        )
        chunk = Chunk(
            id="chunk_001",
            text="test",
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

        entity_types = organizer._get_entity_types(chunk)

        assert entity_types == {"risk", "control"}
        assert len(entity_types) == 2

    def test_get_entity_types_empty_when_no_entities(self):
        """Should return empty set when no entities."""
        organizer = Organizer()

        metadata = ChunkMetadata(entity_tags=[])
        chunk = Chunk(
            id="chunk_001",
            text="test",
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

        entity_types = organizer._get_entity_types(chunk)

        assert entity_types == set()
