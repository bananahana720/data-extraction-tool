"""
Format-specific extractors for various document types.

This package contains extractors for different file formats.
Each extractor implements the BaseExtractor interface.

Available Extractors:
- DocxExtractor: Microsoft Word documents (.docx)
- PdfExtractor: PDF documents (.pdf)
- PptxExtractor: PowerPoint presentations (.pptx)
- ExcelExtractor: Excel spreadsheets (.xlsx, .xls)
- CSVExtractor: CSV/TSV files (.csv, .tsv)
- TextFileExtractor: Plain text files (.txt, .md, .log)

Usage:
    >>> from extractors import DocxExtractor, PdfExtractor, CSVExtractor
    >>> docx_extractor = DocxExtractor()
    >>> pdf_extractor = PdfExtractor()
    >>> csv_extractor = CSVExtractor()
"""

from .csv_extractor import CSVExtractor
from .docx_extractor import DocxExtractor
from .excel_extractor import ExcelExtractor
from .pdf_extractor import PdfExtractor
from .pptx_extractor import PptxExtractor
from .txt_extractor import TextFileExtractor

__all__ = [
    "CSVExtractor",
    "DocxExtractor",
    "ExcelExtractor",
    "PdfExtractor",
    "PptxExtractor",
    "TextFileExtractor",
]
