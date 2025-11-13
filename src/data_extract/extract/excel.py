"""Excel extractor adapter.

Wraps brownfield ExcelExtractor and converts output to greenfield Document model.
Preserves worksheet structure and table data.
"""

from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.excel_extractor import ExcelExtractor as BrownfieldExcelExtractor


class ExcelExtractorAdapter(ExtractorAdapter):
    """Adapter for Excel extraction using brownfield ExcelExtractor.

    Wraps src.extractors.excel_extractor.ExcelExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Multi-sheet workbook support
    - Table structure preservation
    - Formula extraction
    - Cell metadata

    Example:
        >>> adapter = ExcelExtractorAdapter()
        >>> document = adapter.process(Path("workbook.xlsx"))
        >>> print(document.structure["table_count"])
        3
    """

    def __init__(self) -> None:
        """Initialize Excel adapter with brownfield extractor."""
        extractor = BrownfieldExcelExtractor()
        super().__init__(extractor, format_name="Excel")
