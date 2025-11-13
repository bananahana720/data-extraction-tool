"""CSV extractor adapter.

Wraps brownfield CSVExtractor and converts output to greenfield Document model.
Preserves table structure and header information.
"""

from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.csv_extractor import CSVExtractor as BrownfieldCSVExtractor


class CsvExtractorAdapter(ExtractorAdapter):
    """Adapter for CSV extraction using brownfield CSVExtractor.

    Wraps src.extractors.csv_extractor.CSVExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Header detection
    - Delimiter auto-detection
    - Encoding handling
    - Table structure preservation

    Example:
        >>> adapter = CsvExtractorAdapter()
        >>> document = adapter.process(Path("data.csv"))
        >>> print(document.structure["table_count"])
        1
    """

    def __init__(self) -> None:
        """Initialize CSV adapter with brownfield extractor."""
        extractor = BrownfieldCSVExtractor()
        super().__init__(extractor, format_name="CSV")
