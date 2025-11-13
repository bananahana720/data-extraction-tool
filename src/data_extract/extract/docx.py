"""DOCX extractor adapter.

Wraps brownfield DocxExtractor and converts output to greenfield Document model.
Preserves document structure (headings, tables, comments).
"""

from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.docx_extractor import DocxExtractor as BrownfieldDocxExtractor


class DocxExtractorAdapter(ExtractorAdapter):
    """Adapter for DOCX extraction using brownfield DocxExtractor.

    Wraps src.extractors.docx_extractor.DocxExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Heading hierarchy preservation
    - Table structure extraction
    - Comments and tracked changes
    - Style metadata

    Example:
        >>> adapter = DocxExtractorAdapter()
        >>> document = adapter.process(Path("document.docx"))
        >>> print(document.structure["table_count"])
        5
    """

    def __init__(self) -> None:
        """Initialize DOCX adapter with brownfield extractor."""
        extractor = BrownfieldDocxExtractor()
        super().__init__(extractor, format_name="DOCX")
