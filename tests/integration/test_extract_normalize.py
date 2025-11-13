"""Integration tests for Extract → Normalize pipeline.

Tests end-to-end flow from file extraction through adapter to normalizer.
Validates that adapted Documents pass Pydantic validation and are accepted
by the greenfield normalizer.
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
from src.data_extract.core.models import Document
from src.data_extract.extract import get_extractor


@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for all supported formats."""
    files = {
        "pdf": tmp_path / "test.pdf",
        "docx": tmp_path / "test.docx",
        "xlsx": tmp_path / "test.xlsx",
        "pptx": tmp_path / "test.pptx",
        "csv": tmp_path / "test.csv",
        "txt": tmp_path / "test.txt",
    }

    # Create minimal file content
    for file_path in files.values():
        file_path.write_bytes(b"Sample content")

    return files


@pytest.fixture
def mock_extraction_result():
    """Create mock extraction result for all extractors."""

    def _create_result(file_path):
        return BrownfieldExtractionResult(
            success=True,
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content=f"Extracted content from {file_path.name}",
                    position=Position(page=1, sequence_index=0),
                    confidence=1.0,
                ),
            ),
            document_metadata=DocumentMetadata(
                source_file=file_path,
                file_format=file_path.suffix.lstrip("."),
                page_count=1,
                word_count=5,
            ),
        )

    return _create_result


class TestExtractToDocumentConversion:
    """Test extraction to Document conversion for all formats."""

    def test_pdf_extract_to_document(self, sample_files, mock_extraction_result):
        """Test PDF extraction produces valid Document."""
        pdf_file = sample_files["pdf"]

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pdf_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pdf_file)
            document = adapter.process(pdf_file)

            # Verify Document is valid Pydantic model
            assert isinstance(document, Document)
            document.model_validate(document.model_dump())  # Validate serialization

            # Verify required fields
            assert document.id
            assert document.text
            assert isinstance(document.entities, list)
            assert document.metadata
            assert document.structure

    def test_docx_extract_to_document(self, sample_files, mock_extraction_result):
        """Test DOCX extraction produces valid Document."""
        docx_file = sample_files["docx"]

        with patch("src.data_extract.extract.docx.BrownfieldDocxExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(docx_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(docx_file)
            document = adapter.process(docx_file)

            assert isinstance(document, Document)
            assert "test.docx" in document.text

    def test_excel_extract_to_document(self, sample_files, mock_extraction_result):
        """Test Excel extraction produces valid Document."""
        xlsx_file = sample_files["xlsx"]

        with patch("src.data_extract.extract.excel.BrownfieldExcelExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(xlsx_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(xlsx_file)
            document = adapter.process(xlsx_file)

            assert isinstance(document, Document)
            assert "test.xlsx" in document.text

    def test_pptx_extract_to_document(self, sample_files, mock_extraction_result):
        """Test PPTX extraction produces valid Document."""
        pptx_file = sample_files["pptx"]

        with patch("src.data_extract.extract.pptx.BrownfieldPptxExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pptx_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pptx_file)
            document = adapter.process(pptx_file)

            assert isinstance(document, Document)
            assert "test.pptx" in document.text

    def test_csv_extract_to_document(self, sample_files, mock_extraction_result):
        """Test CSV extraction produces valid Document."""
        csv_file = sample_files["csv"]

        with patch("src.data_extract.extract.csv.BrownfieldCSVExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(csv_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(csv_file)
            document = adapter.process(csv_file)

            assert isinstance(document, Document)
            assert "test.csv" in document.text

    def test_txt_extract_to_document(self, sample_files, mock_extraction_result):
        """Test TXT extraction produces valid Document."""
        txt_file = sample_files["txt"]

        with patch("src.data_extract.extract.txt.BrownfieldTextExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(txt_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(txt_file)
            document = adapter.process(txt_file)

            assert isinstance(document, Document)
            assert "test.txt" in document.text


class TestDocumentPydanticValidation:
    """Test Document passes Pydantic v2 validation."""

    def test_document_serialization(self, sample_files, mock_extraction_result):
        """Test Document can be serialized and deserialized."""
        pdf_file = sample_files["pdf"]

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pdf_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pdf_file)
            document = adapter.process(pdf_file)

            # Serialize to dict
            doc_dict = document.model_dump()
            assert isinstance(doc_dict, dict)
            assert "id" in doc_dict
            assert "text" in doc_dict
            assert "metadata" in doc_dict

            # Deserialize back to Document
            restored_document = Document.model_validate(doc_dict)
            assert restored_document.id == document.id
            assert restored_document.text == document.text

    def test_document_json_serialization(self, sample_files, mock_extraction_result):
        """Test Document can be serialized to JSON."""
        pdf_file = sample_files["pdf"]

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pdf_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pdf_file)
            document = adapter.process(pdf_file)

            # Serialize to JSON
            json_str = document.model_dump_json()
            assert isinstance(json_str, str)
            assert document.id in json_str

            # Deserialize from JSON
            restored_document = Document.model_validate_json(json_str)
            assert restored_document.id == document.id


class TestNormalizerCompatibility:
    """Test adapted Documents are compatible with normalizer."""

    def test_document_has_normalizer_required_fields(self, sample_files, mock_extraction_result):
        """Test Document has all fields required by normalizer."""
        pdf_file = sample_files["pdf"]

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pdf_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pdf_file)
            document = adapter.process(pdf_file)

            # Verify normalizer contract fields
            assert hasattr(document, "id")
            assert hasattr(document, "text")
            assert hasattr(document, "entities")
            assert hasattr(document, "metadata")
            assert hasattr(document, "structure")

            # Verify types
            assert isinstance(document.text, str)
            assert isinstance(document.entities, list)
            assert document.metadata is not None

    def test_metadata_has_required_provenance(self, sample_files, mock_extraction_result):
        """Test metadata has required provenance fields."""
        pdf_file = sample_files["pdf"]

        with patch("src.data_extract.extract.pdf.BrownfieldPdfExtractor") as mock_class:
            mock_extractor = Mock()
            mock_extractor.extract.return_value = mock_extraction_result(pdf_file)
            mock_class.return_value = mock_extractor

            adapter = get_extractor(pdf_file)
            document = adapter.process(pdf_file)

            metadata = document.metadata
            assert metadata.source_file
            assert metadata.file_hash
            assert metadata.processing_timestamp
            assert metadata.tool_version
            assert metadata.config_version


class TestEndToEndPipeline:
    """Test complete extract → normalize pipeline flow."""

    def test_all_formats_produce_valid_documents(self, sample_files, mock_extraction_result):
        """Test all formats produce valid Documents for normalizer."""
        formats_tested = []

        for format_name, file_path in sample_files.items():
            # Mock the brownfield extractor for this format
            extractor_mapping = {
                "pdf": ("src.data_extract.extract.pdf", "BrownfieldPdfExtractor"),
                "docx": ("src.data_extract.extract.docx", "BrownfieldDocxExtractor"),
                "xlsx": ("src.data_extract.extract.excel", "BrownfieldExcelExtractor"),
                "pptx": ("src.data_extract.extract.pptx", "BrownfieldPptxExtractor"),
                "csv": ("src.data_extract.extract.csv", "BrownfieldCSVExtractor"),
                "txt": ("src.data_extract.extract.txt", "BrownfieldTextExtractor"),
            }
            extractor_module, extractor_class = extractor_mapping[format_name]

            with patch(f"{extractor_module}.{extractor_class}") as mock_class:
                mock_extractor = Mock()
                mock_extractor.extract.return_value = mock_extraction_result(file_path)
                mock_class.return_value = mock_extractor

                # Extract and convert
                adapter = get_extractor(file_path)
                document = adapter.process(file_path)

                # Verify valid Document
                assert isinstance(document, Document)
                assert document.text
                assert document.metadata.source_file == file_path

                formats_tested.append(format_name)

        # Verify all formats were tested
        assert len(formats_tested) == 6
        assert set(formats_tested) == {"pdf", "docx", "xlsx", "pptx", "csv", "txt"}
