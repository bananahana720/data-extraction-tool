"""Base tests for output organization module.

Tests OrganizationStrategy enum, OrganizationResult dataclass, and common
functionality that is shared across all organization strategies.

Test Coverage:
    - OrganizationStrategy enum values and membership
    - OrganizationResult immutability and fields
    - Common edge cases and error handling
    - Helper method validation
"""

from pathlib import Path

import pytest

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

        # Should use document_id as folder name
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
    """Test Organizer private helper methods."""

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
