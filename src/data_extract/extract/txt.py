"""Text file extractor adapter.

Wraps brownfield TextFileExtractor and converts output to greenfield Document model.
"""

from src.data_extract.extract.adapter import ExtractorAdapter
from src.extractors.txt_extractor import TextFileExtractor as BrownfieldTextExtractor


class TxtExtractorAdapter(ExtractorAdapter):
    """Adapter for text file extraction using brownfield TextFileExtractor.

    Wraps src.extractors.txt_extractor.TextFileExtractor and converts brownfield
    ExtractionResult to greenfield Document model.

    Features:
    - Encoding detection
    - Line break preservation
    - Paragraph detection

    Example:
        >>> adapter = TxtExtractorAdapter()
        >>> document = adapter.process(Path("document.txt"))
        >>> print(len(document.text))
        5000
    """

    def __init__(self) -> None:
        """Initialize TXT adapter with brownfield extractor."""
        extractor = BrownfieldTextExtractor()
        super().__init__(extractor, format_name="TXT")
