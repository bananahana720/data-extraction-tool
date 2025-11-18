"""Unit tests for PDF extractor adapter.

Tests PDF-specific adapter functionality including OCR confidence tracking,
scanned PDF detection, and native text extraction.
"""

from unittest.mock import Mock, patch

import pytest

from src.core.models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    Position,
)
from src.core.models import (
    ExtractionResult as BrownfieldExtractionResult,
)
from src.data_extract.core.models import Document, QualityFlag
from src.data_extract.extract.pdf import PdfExtractorAdapter


@pytest.fixture
def sample_pdf(tmp_path):
    """Create sample PDF file."""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\nSample PDF content")
    return pdf_file


@pytest.fixture
def native_pdf_result(sample_pdf):
    """Create extraction result for native (non-scanned) PDF."""
    return BrownfieldExtractionResult(
        success=True,
        content_blocks=(
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="Native text from PDF.",
                position=Position(page=1, sequence_index=0),
                confidence=1.0,  # Native extraction = 1.0 confidence
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=sample_pdf,
            file_format="pdf",
            page_count=1,
            word_count=4,
        ),
    )


@pytest.fixture
def scanned_pdf_result(sample_pdf):
    """Create extraction result for scanned PDF with OCR."""
    return BrownfieldExtractionResult(
        success=True,
        content_blocks=(
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="OCR extracted text from scanned PDF.",
                position=Position(page=1, sequence_index=0),
                confidence=0.93,  # OCR confidence
                metadata={"ocr_confidence": 0.93},
            ),
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="More text from page 2.",
                position=Position(page=2, sequence_index=1),
                confidence=0.89,  # Lower confidence
                metadata={"ocr_confidence": 0.89},
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=sample_pdf,
            file_format="pdf",
            page_count=2,
            word_count=11,
        ),
    )


class TestPdfExtractorAdapterInit:
    """Test PDF adapter initialization."""

    def test_init_creates_brownfield_extractor(self):
        """Test adapter initializes with brownfield PdfExtractor."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            adapter = PdfExtractorAdapter()
            mock_class.assert_called_once()
            assert adapter.format_name == "PDF"


class TestPdfExtractorAdapterProcess:
    """Test PDF adapter processing."""

    def test_process_native_pdf(self, sample_pdf, native_pdf_result):
        """Test processing native PDF (non-scanned)."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = native_pdf_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            assert isinstance(document, Document)
            assert "Native text from PDF" in document.text
            assert document.metadata.source_file == sample_pdf
            assert document.structure["page_count"] == 1

    def test_process_scanned_pdf(self, sample_pdf, scanned_pdf_result):
        """Test processing scanned PDF with OCR."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = scanned_pdf_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            assert isinstance(document, Document)
            assert "OCR extracted text" in document.text
            assert document.structure["page_count"] == 2

            # Verify OCR confidence tracking
            assert 1 in document.metadata.ocr_confidence
            assert 2 in document.metadata.ocr_confidence
            assert document.metadata.ocr_confidence[1] == 0.93
            assert document.metadata.ocr_confidence[2] == 0.89


class TestScannedPdfDetection:
    """Test scanned PDF detection logic."""

    def test_native_pdf_not_marked_scanned(self, sample_pdf, native_pdf_result):
        """Test native PDF is not marked as scanned."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = native_pdf_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            validation_report = document.metadata.validation_report
            # Native PDF has no OCR confidence scores
            assert validation_report["scanned_pdf_detected"] is False

    def test_scanned_pdf_marked_scanned(self, sample_pdf, scanned_pdf_result):
        """Test scanned PDF is correctly marked as scanned."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = scanned_pdf_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            validation_report = document.metadata.validation_report
            # Scanned PDF has OCR confidence scores
            assert validation_report["scanned_pdf_detected"] is True


class TestOCRConfidenceValidation:
    """Test OCR confidence score validation."""

    def test_low_ocr_confidence_triggers_flag(self, sample_pdf, scanned_pdf_result):
        """Test low OCR confidence triggers quality flag."""
        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = scanned_pdf_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            # Average confidence = (0.93 + 0.89) / 2 = 0.91 < 0.95
            assert QualityFlag.LOW_OCR_CONFIDENCE.value in document.metadata.quality_flags

            validation_report = document.metadata.validation_report
            assert validation_report["quarantine_recommended"] is True
            assert validation_report["document_average_confidence"] < 0.95

    def test_high_ocr_confidence_no_flag(self, sample_pdf):
        """Test high OCR confidence does not trigger flag."""
        high_confidence_result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content="High quality OCR text.",
                    position=Position(page=1, sequence_index=0),
                    confidence=0.98,
                    metadata={"ocr_confidence": 0.98},
                ),
            ),
            document_metadata=DocumentMetadata(
                source_file=sample_pdf,
                file_format="pdf",
                page_count=1,
            ),
        )

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = high_confidence_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            # Confidence 0.98 >= 0.95, should not flag
            assert QualityFlag.LOW_OCR_CONFIDENCE.value not in document.metadata.quality_flags
            validation_report = document.metadata.validation_report
            assert validation_report["quarantine_recommended"] is False


class TestPdfMetadataPreservation:
    """Test PDF metadata preservation."""

    def test_preserves_page_count(self, sample_pdf):
        """Test page count is preserved in structure metadata."""
        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_pdf,
                file_format="pdf",
                page_count=25,
                title="Multi-page Document",
                author="Test Author",
            ),
        )

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            assert document.structure["page_count"] == 25
            assert document.structure["title"] == "Multi-page Document"
            assert document.structure["author"] == "Test Author"

    def test_preserves_table_and_image_counts(self, sample_pdf):
        """Test table and image counts are preserved."""
        from src.core.models import ImageMetadata, TableMetadata

        result = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_pdf,
                file_format="pdf",
                page_count=1,
            ),
            images=(ImageMetadata(), ImageMetadata(), ImageMetadata()),
            tables=(TableMetadata(), TableMetadata()),
        )

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            assert document.structure["image_count"] == 3
            assert document.structure["table_count"] == 2


class TestPdfErrorHandling:
    """Test error handling for PDF extraction."""

    def test_extraction_failure_raises_runtime_error(self, sample_pdf):
        """Test extraction failure raises RuntimeError."""
        failed_result = BrownfieldExtractionResult(
            success=False,
            errors=("PDF decryption failed", "Password required"),
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_pdf,
                file_format="pdf",
            ),
        )

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = failed_result
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            with pytest.raises(RuntimeError, match="Extraction failed"):
                adapter.process(sample_pdf)

    def test_extraction_warnings_captured(self, sample_pdf):
        """Test extraction warnings are captured in validation report."""
        result_with_warnings = BrownfieldExtractionResult(
            success=True,
            content_blocks=(),
            document_metadata=DocumentMetadata(
                source_file=sample_pdf,
                file_format="pdf",
                page_count=1,
            ),
            warnings=("Page 5 partially corrupted", "Some images skipped"),
        )

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = result_with_warnings
            mock_class.return_value = mock_extractor

            adapter = PdfExtractorAdapter()
            document = adapter.process(sample_pdf)

            validation_report = document.metadata.validation_report
            assert QualityFlag.INCOMPLETE_EXTRACTION.value in validation_report["quality_flags"]
            assert "Page 5 partially corrupted" in validation_report["extraction_gaps"]
            assert validation_report["quarantine_recommended"] is True
