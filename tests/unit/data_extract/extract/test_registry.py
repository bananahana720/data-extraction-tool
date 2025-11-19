"""Unit tests for extractor registry and factory pattern.

Tests format detection, adapter selection, and error handling.
"""

from pathlib import Path

import pytest

from src.data_extract.extract import (
    SUPPORTED_EXTENSIONS,
    CsvExtractorAdapter,
    DocxExtractorAdapter,
    ExcelExtractorAdapter,
    PdfExtractorAdapter,
    PptxExtractorAdapter,
    TxtExtractorAdapter,
    get_extractor,
    is_supported,
)


class TestGetExtractor:
    """Test get_extractor() factory function."""

    def test_get_pdf_extractor(self):
        """Test PDF file returns PdfExtractorAdapter."""
        adapter = get_extractor(Path("document.pdf"))
        assert isinstance(adapter, PdfExtractorAdapter)
        assert adapter.format_name == "PDF"

    def test_get_docx_extractor(self):
        """Test DOCX file returns DocxExtractorAdapter."""
        adapter = get_extractor(Path("document.docx"))
        assert isinstance(adapter, DocxExtractorAdapter)
        assert adapter.format_name == "DOCX"

    def test_get_excel_extractor(self):
        """Test XLSX file returns ExcelExtractorAdapter."""
        adapter = get_extractor(Path("workbook.xlsx"))
        assert isinstance(adapter, ExcelExtractorAdapter)
        assert adapter.format_name == "Excel"

    def test_get_pptx_extractor(self):
        """Test PPTX file returns PptxExtractorAdapter."""
        adapter = get_extractor(Path("presentation.pptx"))
        assert isinstance(adapter, PptxExtractorAdapter)
        assert adapter.format_name == "PPTX"

    def test_get_csv_extractor(self):
        """Test CSV file returns CsvExtractorAdapter."""
        adapter = get_extractor(Path("data.csv"))
        assert isinstance(adapter, CsvExtractorAdapter)
        assert adapter.format_name == "CSV"

    def test_get_txt_extractor(self):
        """Test TXT file returns TxtExtractorAdapter."""
        adapter = get_extractor(Path("notes.txt"))
        assert isinstance(adapter, TxtExtractorAdapter)
        assert adapter.format_name == "TXT"

    def test_case_insensitive_extension(self):
        """Test extension matching is case-insensitive."""
        adapter_upper = get_extractor(Path("DOCUMENT.PDF"))
        adapter_lower = get_extractor(Path("document.pdf"))
        adapter_mixed = get_extractor(Path("Document.PdF"))

        assert isinstance(adapter_upper, PdfExtractorAdapter)
        assert isinstance(adapter_lower, PdfExtractorAdapter)
        assert isinstance(adapter_mixed, PdfExtractorAdapter)

    def test_unsupported_extension_raises_error(self):
        """Test unsupported file extension raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported file extension"):
            get_extractor(Path("video.mp4"))

    def test_error_message_lists_supported_formats(self):
        """Test error message includes list of supported formats."""
        with pytest.raises(ValueError, match="Supported extensions"):
            get_extractor(Path("unknown.xyz"))


class TestLegacyFormats:
    """Test support for legacy Office formats."""

    def test_doc_format(self):
        """Test legacy .doc format."""
        adapter = get_extractor(Path("legacy.doc"))
        assert isinstance(adapter, DocxExtractorAdapter)

    def test_xls_format(self):
        """Test legacy .xls format."""
        adapter = get_extractor(Path("legacy.xls"))
        assert isinstance(adapter, ExcelExtractorAdapter)

    def test_xlsm_format(self):
        """Test macro-enabled .xlsm format."""
        adapter = get_extractor(Path("macros.xlsm"))
        assert isinstance(adapter, ExcelExtractorAdapter)

    def test_ppt_format(self):
        """Test legacy .ppt format."""
        adapter = get_extractor(Path("legacy.ppt"))
        assert isinstance(adapter, PptxExtractorAdapter)


class TestTextFormatVariants:
    """Test various text format extensions."""

    def test_text_extension(self):
        """Test .text extension."""
        adapter = get_extractor(Path("notes.text"))
        assert isinstance(adapter, TxtExtractorAdapter)

    def test_markdown_extension(self):
        """Test .md markdown extension."""
        adapter = get_extractor(Path("README.md"))
        assert isinstance(adapter, TxtExtractorAdapter)

    def test_log_extension(self):
        """Test .log log file extension."""
        adapter = get_extractor(Path("application.log"))
        assert isinstance(adapter, TxtExtractorAdapter)

    def test_tsv_extension(self):
        """Test .tsv tab-separated values extension."""
        adapter = get_extractor(Path("data.tsv"))
        assert isinstance(adapter, CsvExtractorAdapter)


class TestIsSupported:
    """Test is_supported() helper function."""

    def test_supported_pdf(self):
        """Test PDF format is supported."""
        assert is_supported(Path("document.pdf")) is True

    def test_supported_docx(self):
        """Test DOCX format is supported."""
        assert is_supported(Path("document.docx")) is True

    def test_supported_xlsx(self):
        """Test XLSX format is supported."""
        assert is_supported(Path("workbook.xlsx")) is True

    def test_supported_pptx(self):
        """Test PPTX format is supported."""
        assert is_supported(Path("presentation.pptx")) is True

    def test_supported_csv(self):
        """Test CSV format is supported."""
        assert is_supported(Path("data.csv")) is True

    def test_supported_txt(self):
        """Test TXT format is supported."""
        assert is_supported(Path("notes.txt")) is True

    def test_unsupported_format(self):
        """Test unsupported format returns False."""
        assert is_supported(Path("video.mp4")) is False
        assert is_supported(Path("audio.mp3")) is False
        assert is_supported(Path("image.png")) is False

    def test_case_insensitive(self):
        """Test is_supported is case-insensitive."""
        assert is_supported(Path("DOCUMENT.PDF")) is True
        assert is_supported(Path("Document.PdF")) is True


class TestSupportedExtensions:
    """Test SUPPORTED_EXTENSIONS constant."""

    def test_contains_all_formats(self):
        """Test SUPPORTED_EXTENSIONS contains all expected formats."""
        expected_formats = {
            ".pdf",
            ".docx",
            ".doc",
            ".xlsx",
            ".xls",
            ".xlsm",
            ".pptx",
            ".ppt",
            ".txt",
            ".text",
            ".md",
            ".log",
            ".csv",
            ".tsv",
        }
        assert expected_formats.issubset(SUPPORTED_EXTENSIONS)

    def test_is_set_type(self):
        """Test SUPPORTED_EXTENSIONS is a set."""
        assert isinstance(SUPPORTED_EXTENSIONS, set)

    def test_no_duplicates(self):
        """Test no duplicate extensions."""
        # Sets automatically prevent duplicates, but verify count matches registry
        from src.data_extract.extract import EXTRACTOR_REGISTRY

        assert len(SUPPORTED_EXTENSIONS) == len(EXTRACTOR_REGISTRY)


class TestFactoryPatternBehavior:
    """Test factory pattern characteristics."""

    def test_returns_new_instance_each_call(self):
        """Test each call returns a new adapter instance."""
        adapter1 = get_extractor(Path("doc1.pdf"))
        adapter2 = get_extractor(Path("doc2.pdf"))

        # Should be same type but different instances
        assert isinstance(adapter1, type(adapter2))
        assert adapter1 is not adapter2

    def test_adapter_has_process_method(self):
        """Test returned adapter has process() method."""
        adapter = get_extractor(Path("document.pdf"))
        assert hasattr(adapter, "process")
        assert callable(adapter.process)

    def test_adapter_has_extractor_attribute(self):
        """Test returned adapter has extractor attribute."""
        adapter = get_extractor(Path("document.pdf"))
        assert hasattr(adapter, "extractor")

    def test_adapter_has_format_name(self):
        """Test returned adapter has format_name attribute."""
        adapter = get_extractor(Path("document.pdf"))
        assert hasattr(adapter, "format_name")
        assert isinstance(adapter.format_name, str)
