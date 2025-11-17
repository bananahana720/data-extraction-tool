"""Tests for BY_DOCUMENT organization strategy.

Tests Organizer functionality specifically for the BY_DOCUMENT strategy,
which creates one folder per source document.

Test Coverage:
    - Single source document organization
    - Multiple source document organization
    - Manifest generation for BY_DOCUMENT strategy
    - Folder structure validation
    - File routing logic
"""

import json
from pathlib import Path

import pytest

from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.output.organization import OrganizationStrategy, Organizer

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.organization]


class TestOrganizerByDocument:
    """Test Organizer with BY_DOCUMENT strategy."""

    @pytest.fixture
    def chunks_single_source(self) -> list:
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
    def chunks_multi_source(self) -> list:
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

    def test_document_folder_naming(self, tmp_path):
        """Should sanitize document names for folder creation."""
        metadata = ChunkMetadata(
            source_file=Path("2024 Annual Report (Final).pdf"),
            entity_tags=[],
            section_context="Executive Summary",
        )
        chunk = Chunk(
            id="chunk_001",
            text="Annual report content",
            document_id="doc_001",
            position_index=0,
            token_count=50,
            word_count=40,
            entities=[],
            section_context="Executive Summary",
            quality_score=0.9,
            readability_scores={},
            metadata=metadata,
        )

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Should create sanitized folder name
        assert result.files_written == 1
        # Check that directory was created with sanitized name
        dirs = [d for d in output_dir.iterdir() if d.is_dir()]
        assert len(dirs) == 1
        # Name should be sanitized (lowercase, special chars replaced)
        assert "2024" in dirs[0].name.lower()
        assert "annual" in dirs[0].name.lower()
        assert "report" in dirs[0].name.lower()

    def test_multiple_chunks_same_document(self, chunks_single_source, tmp_path):
        """Should group all chunks from same document in single folder."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(
            chunks_single_source, output_dir, OrganizationStrategy.BY_DOCUMENT
        )

        # All chunks should be in same folder
        assert (output_dir / "audit_report").exists()
        assert result.files_written == 3
        assert result.folders_created == 1

    def test_preserves_document_hierarchy(self, tmp_path):
        """Should preserve document-based hierarchy in manifest."""
        # Create chunks from nested document paths
        chunks = []
        paths = ["reports/audit/2024.pdf", "reports/risk/assessment.xlsx"]

        for idx, path in enumerate(paths):
            metadata = ChunkMetadata(
                source_file=Path(path),
                entity_tags=[],
                section_context="Section 1",
            )
            chunk = Chunk(
                id=f"chunk_{idx:03d}",
                text=f"Content from {path}",
                document_id=f"doc_{idx:03d}",
                position_index=0,
                token_count=50,
                word_count=40,
                entities=[],
                section_context="Section 1",
                quality_score=0.9,
                readability_scores={},
                metadata=metadata,
            )
            chunks.append(chunk)

        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks, output_dir, OrganizationStrategy.BY_DOCUMENT)

        # Check manifest preserves source information
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["total_chunks"] == 2
        assert len(manifest["folders"]) == 2
        assert result.folders_created == 2
