"""PPTX extractor adapter.

Wraps brownfield PptxExtractor and converts output to greenfield Document model.
Preserves slide structure and notes.
"""

from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.pptx_extractor import PptxExtractor as BrownfieldPptxExtractor


class PptxExtractorAdapter(ExtractorAdapter):
    """Adapter for PPTX extraction using brownfield PptxExtractor.

    Wraps src.extractors.pptx_extractor.PptxExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Slide order preservation
    - Speaker notes extraction
    - Image and chart metadata
    - Layout information

    Example:
        >>> adapter = PptxExtractorAdapter()
        >>> document = adapter.process(Path("presentation.pptx"))
        >>> print(document.structure["page_count"])  # slide count
        25
    """

    def __init__(self) -> None:
        """Initialize PPTX adapter with brownfield extractor."""
        extractor = BrownfieldPptxExtractor()
        super().__init__(extractor, format_name="PPTX")
