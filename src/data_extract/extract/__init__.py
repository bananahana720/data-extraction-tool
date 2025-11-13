"""Extractor adapters and registry.

This module provides the factory pattern for selecting the appropriate
extractor adapter based on file extension.

Architecture:
    File → get_extractor() → Adapter → Document (greenfield)

Example:
    >>> from pathlib import Path
    >>> from src.data_extract.extract import get_extractor
    >>>
    >>> adapter = get_extractor(Path("document.pdf"))
    >>> document = adapter.process(Path("document.pdf"))
"""

from pathlib import Path
from typing import Dict, Type

from src.data_extract.extract.adapter import ExtractorAdapter
from src.data_extract.extract.csv import CsvExtractorAdapter
from src.data_extract.extract.docx import DocxExtractorAdapter
from src.data_extract.extract.excel import ExcelExtractorAdapter
from src.data_extract.extract.pdf import PdfExtractorAdapter
from src.data_extract.extract.pptx import PptxExtractorAdapter
from src.data_extract.extract.txt import TxtExtractorAdapter

# Extractor registry: maps file extensions to adapter classes
EXTRACTOR_REGISTRY: Dict[str, Type[ExtractorAdapter]] = {
    # PDF formats
    ".pdf": PdfExtractorAdapter,
    # Word formats
    ".docx": DocxExtractorAdapter,
    ".doc": DocxExtractorAdapter,  # Legacy Word (if supported by brownfield)
    # Excel formats
    ".xlsx": ExcelExtractorAdapter,
    ".xls": ExcelExtractorAdapter,  # Legacy Excel (if supported by brownfield)
    ".xlsm": ExcelExtractorAdapter,  # Macro-enabled Excel
    # PowerPoint formats
    ".pptx": PptxExtractorAdapter,
    ".ppt": PptxExtractorAdapter,  # Legacy PowerPoint (if supported by brownfield)
    # Plain text formats
    ".txt": TxtExtractorAdapter,
    ".text": TxtExtractorAdapter,
    ".md": TxtExtractorAdapter,  # Markdown as plain text
    ".log": TxtExtractorAdapter,  # Log files as plain text
    # CSV formats
    ".csv": CsvExtractorAdapter,
    ".tsv": CsvExtractorAdapter,  # Tab-separated values
}

# Supported extensions (for validation)
SUPPORTED_EXTENSIONS = set(EXTRACTOR_REGISTRY.keys())


def get_extractor(file_path: Path) -> ExtractorAdapter:
    """Get appropriate extractor adapter for file.

    Auto-detects file format from extension and returns the corresponding
    adapter instance. Factory pattern ensures single entry point for all
    extraction operations.

    Args:
        file_path: Path to file to extract

    Returns:
        ExtractorAdapter: Adapter instance for the file format

    Raises:
        ValueError: If file extension is not supported

    Example:
        >>> adapter = get_extractor(Path("report.pdf"))
        >>> isinstance(adapter, PdfExtractorAdapter)
        True

        >>> adapter = get_extractor(Path("data.xlsx"))
        >>> isinstance(adapter, ExcelExtractorAdapter)
        True
    """
    # Get file extension (lowercase for case-insensitive matching)
    extension = file_path.suffix.lower()

    # Look up adapter class in registry
    adapter_class = EXTRACTOR_REGISTRY.get(extension)

    if adapter_class is None:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported file extension: {extension}\n" f"Supported extensions: {supported}"
        )

    # Instantiate and return adapter
    return adapter_class()


def is_supported(file_path: Path) -> bool:
    """Check if file format is supported.

    Args:
        file_path: Path to file

    Returns:
        True if file format is supported, False otherwise

    Example:
        >>> is_supported(Path("document.pdf"))
        True
        >>> is_supported(Path("video.mp4"))
        False
    """
    extension = file_path.suffix.lower()
    return extension in SUPPORTED_EXTENSIONS


__all__ = [
    "ExtractorAdapter",
    "PdfExtractorAdapter",
    "DocxExtractorAdapter",
    "ExcelExtractorAdapter",
    "PptxExtractorAdapter",
    "CsvExtractorAdapter",
    "TxtExtractorAdapter",
    "get_extractor",
    "is_supported",
    "SUPPORTED_EXTENSIONS",
]
