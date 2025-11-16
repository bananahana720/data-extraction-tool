"""PDF extractor adapter.

Wraps brownfield PdfExtractor and converts output to greenfield Document model.
Preserves OCR confidence scores, page counts, and extraction metadata.
"""

from typing import Dict

from src.core.models import ExtractionResult as BrownfieldExtractionResult
from src.data_extract.core.models import ValidationReport
from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.pdf_extractor import PdfExtractor as BrownfieldPdfExtractor


class PdfExtractorAdapter(ExtractorAdapter):
    """Adapter for PDF extraction using brownfield PdfExtractor.

    Wraps src.extractors.pdf_extractor.PdfExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Native text extraction + OCR fallback
    - Per-page OCR confidence tracking
    - Table and image metadata preservation
    - Scanned PDF detection

    Example:
        >>> adapter = PdfExtractorAdapter()
        >>> document = adapter.process(Path("document.pdf"))
        >>> print(document.metadata.ocr_confidence)
        {1: 0.98, 2: 0.95, 3: 0.92}
    """

    def __init__(self) -> None:
        """Initialize PDF adapter with brownfield extractor."""
        extractor = BrownfieldPdfExtractor()
        super().__init__(extractor, format_name="PDF")

    def _generate_validation_report(
        self, result: BrownfieldExtractionResult, ocr_confidence: Dict[int, float]
    ) -> ValidationReport:
        """Override to add PDF-specific validation logic.

        Extends base validation with scanned PDF detection.

        Args:
            result: Brownfield extraction result
            ocr_confidence: Per-page OCR confidence scores

        Returns:
            ValidationReport with PDF-specific validation
        """
        # Get base validation report
        report = super()._generate_validation_report(result, ocr_confidence)

        # Detect scanned PDF: if OCR confidence exists AND is below 1.0, it's scanned
        # Native PDFs have confidence=1.0 (or no confidence data)
        scanned_pdf_detected = any(conf < 1.0 for conf in ocr_confidence.values())

        # Create new report with updated fields (ValidationReport is immutable)

        return ValidationReport(
            quarantine_recommended=report.quarantine_recommended,
            confidence_scores=report.confidence_scores,
            quality_flags=report.quality_flags,
            extraction_gaps=report.extraction_gaps,
            document_average_confidence=report.document_average_confidence,
            scanned_pdf_detected=scanned_pdf_detected,
            completeness_passed=report.completeness_passed,
            missing_images_count=report.missing_images_count,
            complex_objects_count=report.complex_objects_count,
        )
