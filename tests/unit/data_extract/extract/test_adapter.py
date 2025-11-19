"""Unit tests for ExtractorAdapter base class.

Tests adapter conversion logic, metadata mapping, and error handling.
Uses mocked brownfield extractors to validate adapter behavior in isolation.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.core.models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ImageMetadata,
    Position,
    TableMetadata,
)
from src.core.models import (
    ExtractionResult as BrownfieldExtractionResult,
)
from src.data_extract.core.models import Document, QualityFlag
from src.data_extract.extract.adapter import ExtractorAdapter


@pytest.fixture
def mock_extractor():
    """Create mock brownfield extractor."""
    extractor = Mock()
    return extractor


@pytest.fixture
def sample_file(tmp_path):
    """Create sample test file."""
    test_file = tmp_path / "test_document.txt"
    test_file.write_text("Sample content for testing")
    return test_file


@pytest.fixture
def simple_extraction_result(sample_file):
    """Create simple successful extraction result."""
    return BrownfieldExtractionResult(
        success=True,
        content_blocks=(
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="First paragraph content.",
                position=Position(page=1, sequence_index=0),
                confidence=1.0,
            ),
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="Second paragraph content.",
                position=Position(page=1, sequence_index=1),
                confidence=1.0,
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=sample_file,
            file_format="txt",
            page_count=1,
            word_count=6,
            character_count=50,
        ),
        images=(),
        tables=(),
        errors=(),
        warnings=(),
    )


@pytest.fixture
def ocr_extraction_result(sample_file):
    """Create extraction result with OCR confidence scores."""
    return BrownfieldExtractionResult(
        success=True,
        content_blocks=(
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="Page 1 content.",
                position=Position(page=1, sequence_index=0),
                confidence=0.92,  # Below 95% threshold
                metadata={"ocr_confidence": 0.92},
            ),
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="Page 2 content.",
                position=Position(page=2, sequence_index=1),
                confidence=0.88,  # Below 95% threshold
                metadata={"ocr_confidence": 0.88},
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=sample_file,
            file_format="pdf",
            page_count=2,
            word_count=6,
        ),
        images=(),
        tables=(),
        errors=(),
        warnings=(),
    )


class TestExtractorAdapterInit:
    """Test ExtractorAdapter initialization."""

    def test_init_with_valid_extractor(self, mock_extractor):
        """Test adapter initializes with valid extractor."""
        adapter = ExtractorAdapter(mock_extractor, "TEST")
        assert adapter.extractor is mock_extractor
        assert adapter.format_name == "TEST"


class TestExtractorAdapterProcess:
    """Test ExtractorAdapter.process() method."""

    def test_process_successful_extraction(
        self, mock_extractor, sample_file, simple_extraction_result
    ):
        """Test process with successful extraction."""
        mock_extractor.extract.return_value = simple_extraction_result
        adapter = ExtractorAdapter(mock_extractor, "TXT")

        document = adapter.process(sample_file)

        # Verify extractor was called
        mock_extractor.extract.assert_called_once_with(sample_file)

        # Verify Document structure
        assert isinstance(document, Document)
        assert document.text  # Should have concatenated text
        assert document.metadata.source_file == sample_file
        assert document.metadata.tool_version
        assert isinstance(document.entities, list)

    def test_process_file_not_found(self, mock_extractor):
        """Test process raises FileNotFoundError for missing file."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        nonexistent_file = Path("/nonexistent/file.txt")

        with pytest.raises(FileNotFoundError, match="File not found"):
            adapter.process(nonexistent_file)

    def test_process_extraction_failure(self, mock_extractor, sample_file):
        """Test process raises RuntimeError when extraction fails."""
        failed_result = BrownfieldExtractionResult(
            success=False,
            errors=("Critical extraction error",),
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_file,
                file_format="txt",
            ),
        )
        mock_extractor.extract.return_value = failed_result
        adapter = ExtractorAdapter(mock_extractor, "TXT")

        with pytest.raises(RuntimeError, match="Extraction failed"):
            adapter.process(sample_file)


class TestConvertToDocument:
    """Test _convert_to_document() conversion logic."""

    def test_document_has_unique_id(self, mock_extractor, sample_file, simple_extraction_result):
        """Test generated document ID is unique."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        doc1 = adapter._convert_to_document(simple_extraction_result, sample_file)
        doc2 = adapter._convert_to_document(simple_extraction_result, sample_file)

        # IDs should be different due to UUID component
        assert doc1.id != doc2.id
        assert "test_document" in doc1.id

    def test_text_concatenation_preserves_order(
        self, mock_extractor, sample_file, simple_extraction_result
    ):
        """Test content blocks are concatenated in sequence order."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(simple_extraction_result, sample_file)

        # Text should contain both blocks in order
        assert "First paragraph content" in document.text
        assert "Second paragraph content" in document.text
        assert document.text.index("First") < document.text.index("Second")

    def test_entities_list_empty(self, mock_extractor, sample_file, simple_extraction_result):
        """Test entities list is empty (populated by normalizer)."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(simple_extraction_result, sample_file)

        assert document.entities == []

    def test_structure_metadata_preserved(self, mock_extractor, sample_file):
        """Test structure metadata is extracted correctly."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_file,
                file_format="pdf",
                page_count=10,
                word_count=5000,
                character_count=25000,
                title="Test Document",
                author="Test Author",
                keywords=("test", "document"),
            ),
            images=(ImageMetadata(), ImageMetadata()),
            tables=(TableMetadata(), TableMetadata(), TableMetadata()),
        )
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(result, sample_file)

        assert document.structure["page_count"] == 10
        assert document.structure["word_count"] == 5000
        assert document.structure["character_count"] == 25000
        assert document.structure["image_count"] == 2
        assert document.structure["table_count"] == 3
        assert document.structure["title"] == "Test Document"
        assert document.structure["author"] == "Test Author"
        assert document.structure["keywords"] == ["test", "document"]


class TestMetadataConversion:
    """Test metadata conversion logic."""

    def test_file_hash_computation(self, mock_extractor, sample_file, simple_extraction_result):
        """Test file hash is computed correctly."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(simple_extraction_result, sample_file)

        # Compute expected hash
        expected_hash = hashlib.sha256(sample_file.read_bytes()).hexdigest()
        assert document.metadata.file_hash == expected_hash

    def test_processing_timestamp_set(self, mock_extractor, sample_file, simple_extraction_result):
        """Test processing timestamp is set to current time."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        before = datetime.now(timezone.utc)
        document = adapter._convert_to_document(simple_extraction_result, sample_file)
        after = datetime.now(timezone.utc)

        assert before <= document.metadata.processing_timestamp <= after

    def test_version_info_populated(self, mock_extractor, sample_file, simple_extraction_result):
        """Test tool and config versions are populated."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(simple_extraction_result, sample_file)

        assert document.metadata.tool_version
        assert document.metadata.config_version


class TestOCRConfidenceExtraction:
    """Test OCR confidence score extraction."""

    def test_ocr_confidence_by_page(self, mock_extractor, sample_file, ocr_extraction_result):
        """Test OCR confidence scores extracted per page."""
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(ocr_extraction_result, sample_file)

        # Should have confidence scores for pages 1 and 2
        assert 1 in document.metadata.ocr_confidence
        assert 2 in document.metadata.ocr_confidence
        assert document.metadata.ocr_confidence[1] == 0.92
        assert document.metadata.ocr_confidence[2] == 0.88

    def test_low_ocr_confidence_flagged(self, mock_extractor, sample_file, ocr_extraction_result):
        """Test low OCR confidence triggers quality flag."""
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(ocr_extraction_result, sample_file)

        # Should flag low OCR confidence (below 95%)
        assert QualityFlag.LOW_OCR_CONFIDENCE.value in document.metadata.quality_flags
        assert "ocr_confidence" in document.metadata.quality_scores
        assert document.metadata.quality_scores["ocr_confidence"] < 0.95


class TestValidationReport:
    """Test validation report generation."""

    def test_validation_report_clean_document(
        self, mock_extractor, sample_file, simple_extraction_result
    ):
        """Test validation report for clean document (no issues)."""
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(simple_extraction_result, sample_file)

        report = document.metadata.validation_report
        assert report["quarantine_recommended"] is False
        assert report["completeness_passed"] is True
        assert len(report["quality_flags"]) == 0

    def test_validation_report_with_warnings(self, mock_extractor, sample_file):
        """Test validation report includes extraction warnings."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="pdf"),
            warnings=("Page 5 extraction incomplete", "Table parsing failed"),
            errors=(),
        )
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(result, sample_file)

        report = document.metadata.validation_report
        assert report["quarantine_recommended"] is True
        assert QualityFlag.INCOMPLETE_EXTRACTION.value in report["quality_flags"]
        assert "Page 5 extraction incomplete" in report["extraction_gaps"]

    def test_validation_report_with_errors(self, mock_extractor, sample_file):
        """Test validation report includes extraction errors."""
        result = BrownfieldExtractionResult(
            success=True,  # Partial success
            content_blocks=(),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="pdf"),
            errors=("Critical page error",),
            warnings=(),
        )
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(result, sample_file)

        report = document.metadata.validation_report
        assert report["quarantine_recommended"] is True
        assert "Critical page error" in report["extraction_gaps"]

    def test_validation_report_missing_images(self, mock_extractor, sample_file):
        """Test validation report detects missing images."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="pdf"),
            images=(
                ImageMetadata(is_low_quality=True, quality_issues=("blurry",)),
                ImageMetadata(is_low_quality=False),
            ),
        )
        adapter = ExtractorAdapter(mock_extractor, "PDF")
        document = adapter._convert_to_document(result, sample_file)

        report = document.metadata.validation_report
        assert report["missing_images_count"] == 1
        assert QualityFlag.MISSING_IMAGES.value in report["quality_flags"]


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_content_blocks(self, mock_extractor, sample_file):
        """Test handling of empty content blocks."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="txt"),
        )
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(result, sample_file)

        assert document.text == ""
        assert isinstance(document, Document)

    def test_blocks_without_position(self, mock_extractor, sample_file):
        """Test handling of blocks without position metadata."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content="Content without position",
                    position=None,
                ),
            ),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="txt"),
        )
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(result, sample_file)

        assert "Content without position" in document.text

    def test_blocks_without_confidence(self, mock_extractor, sample_file):
        """Test handling of blocks without confidence scores."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content="Content without confidence",
                    position=Position(page=1),
                    confidence=None,
                ),
            ),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="txt"),
        )
        adapter = ExtractorAdapter(mock_extractor, "TXT")
        document = adapter._convert_to_document(result, sample_file)

        # Should default to 1.0 confidence
        assert 1 in document.metadata.ocr_confidence
        assert document.metadata.ocr_confidence[1] == 1.0
