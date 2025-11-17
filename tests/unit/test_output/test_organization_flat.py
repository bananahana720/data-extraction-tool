"""Tests for FLAT organization strategy.

Tests Organizer functionality specifically for the FLAT strategy,
which creates all files in a single directory with prefixed filenames.

Test Coverage:
    - Flat structure with no subdirectories
    - Filename prefixing with source document
    - Manifest generation for FLAT strategy
    - File naming conventions
    - Edge cases for flat organization
"""

import json
from pathlib import Path

import pytest

from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.output.organization import OrganizationStrategy, Organizer

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.organization]


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

    @pytest.fixture
    def chunks_single_source(self) -> list:
        """Create chunks from single source for flat testing."""
        chunks = []
        for i in range(3):
            metadata = ChunkMetadata(
                source_file=Path("report.pdf"),
                entity_tags=[],
                section_context="Section 1",
            )
            chunk = Chunk(
                id=f"chunk_{i+1:03d}",
                text=f"Chunk {i+1} content.",
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

    def test_manifest_generation_for_flat(self, chunks_single_source, tmp_path):
        """Should generate proper manifest for flat organization."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_single_source, output_dir, OrganizationStrategy.FLAT)

        # Check manifest exists
        assert result.manifest_path.exists()
        assert result.manifest_path == output_dir / "manifest.json"

        # Check manifest structure
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["organization_strategy"] == "flat"
        assert manifest["total_chunks"] == 3
        assert "folders" in manifest
        assert len(manifest["folders"]) == 0  # No folders in flat structure

        # Check enriched metadata (AC-3.7-6)
        assert "generated_at" in manifest
        assert "processing_version" in manifest
        assert "config_snapshot" in manifest
        assert "source_files" in manifest
        assert "entity_summary" in manifest
        assert "quality_summary" in manifest

    def test_flat_with_config_snapshot(self, chunks_single_source, tmp_path):
        """Should include configuration snapshot in flat manifest."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        config = {
            "chunk_size": 1024,
            "overlap_pct": 0.20,
            "respect_sentences": True,
        }

        result = organizer.organize(
            chunks_single_source,
            output_dir,
            OrganizationStrategy.FLAT,
            config_snapshot=config,
        )

        # Check manifest includes config
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["config_snapshot"] == config
        assert manifest["config_snapshot"]["chunk_size"] == 1024

    def test_flat_preserves_source_information(self, chunks_for_flat, tmp_path):
        """Should preserve source document information in flat structure."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_for_flat, output_dir, OrganizationStrategy.FLAT)

        # Check manifest preserves source files
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert "source_files" in manifest
        # Should track both source documents
        assert manifest["total_chunks"] == 4

    def test_flat_empty_chunks_list(self, tmp_path):
        """Should handle empty chunks list in flat organization."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize([], output_dir, OrganizationStrategy.FLAT)

        # Should create manifest even with no chunks
        assert result.manifest_path.exists()
        assert result.files_written == 0
        assert result.folders_created == 0

        # Check manifest reflects empty state
        with open(result.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["total_chunks"] == 0
        assert manifest["organization_strategy"] == "flat"

    def test_flat_with_unicode_filenames(self, tmp_path):
        """Should handle Unicode source names in flat organization."""
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

        result = organizer.organize([chunk], output_dir, OrganizationStrategy.FLAT)

        # Should handle Unicode in flat structure
        assert result.files_written == 1
        assert result.folders_created == 0

    def test_flat_quality_summary_in_manifest(self, chunks_single_source, tmp_path):
        """Should include quality summary in flat manifest."""
        organizer = Organizer()
        output_dir = tmp_path / "output"

        result = organizer.organize(chunks_single_source, output_dir, OrganizationStrategy.FLAT)

        # Check manifest quality summary
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
