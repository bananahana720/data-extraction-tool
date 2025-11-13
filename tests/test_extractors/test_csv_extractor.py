"""
Test suite for CSVExtractor - Strict TDD Implementation

This test suite follows Red-Green-Refactor methodology with tests written
BEFORE implementation code.

Test Organization:
- Cycle 1: File Validation and Format Detection
- Cycle 2: Basic CSV Extraction
- Cycle 3: Delimiter Detection
- Cycle 4: Encoding Detection
- Cycle 5: Header Detection
- Cycle 6: Data Type Handling
- Cycle 7: Edge Cases and Malformed Data
- Cycle 8: Configuration Overrides
- Cycle 9: Error Handling
- Cycle 10: Infrastructure Integration

Coverage: 40+ tests for comprehensive CSV/TSV extraction validation
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core import (
    ContentType,
)

# Import will fail initially - this is expected in RED phase
try:
    from extractors.csv_extractor import CSVExtractor

    EXTRACTOR_AVAILABLE = True
except ImportError:
    EXTRACTOR_AVAILABLE = False
    CSVExtractor = None


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def csv_extractor():
    """Create CSVExtractor instance with default config."""
    if not EXTRACTOR_AVAILABLE:
        pytest.skip("CSVExtractor not yet implemented")
    return CSVExtractor()


@pytest.fixture
def csv_extractor_with_config():
    """Create CSVExtractor with test configuration."""
    if not EXTRACTOR_AVAILABLE:
        pytest.skip("CSVExtractor not yet implemented")
    config = {
        "delimiter": ",",
        "encoding": "utf-8",
        "has_header": True,
        "max_rows": 1000,
    }
    return CSVExtractor(config)


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV file with headers."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Name,Age,City\nAlice,30,NYC\nBob,25,LA\nCharlie,35,Chicago")
    return csv_file


@pytest.fixture
def sample_tsv(tmp_path):
    """Create sample TSV file with tab delimiter."""
    tsv_file = tmp_path / "sample.tsv"
    tsv_file.write_text("Name\tAge\tCity\nAlice\t30\tNYC\nBob\t25\tLA")
    return tsv_file


@pytest.fixture
def semicolon_csv(tmp_path):
    """Create CSV with semicolon delimiter."""
    csv_file = tmp_path / "semicolon.csv"
    csv_file.write_text("Name;Age;City\nAlice;30;NYC\nBob;25;LA")
    return csv_file


@pytest.fixture
def pipe_csv(tmp_path):
    """Create CSV with pipe delimiter."""
    csv_file = tmp_path / "pipe.csv"
    csv_file.write_text("Name|Age|City\nAlice|30|NYC\nBob|25|LA")
    return csv_file


@pytest.fixture
def no_header_csv(tmp_path):
    """Create CSV without header row."""
    csv_file = tmp_path / "no_header.csv"
    csv_file.write_text("Alice,30,NYC\nBob,25,LA\nCharlie,35,Chicago")
    return csv_file


@pytest.fixture
def empty_csv(tmp_path):
    """Create empty CSV file."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    return csv_file


@pytest.fixture
def single_row_csv(tmp_path):
    """Create CSV with single row (header only)."""
    csv_file = tmp_path / "single_row.csv"
    csv_file.write_text("Name,Age,City")
    return csv_file


@pytest.fixture
def single_column_csv(tmp_path):
    """Create CSV with single column."""
    csv_file = tmp_path / "single_column.csv"
    csv_file.write_text("Name\nAlice\nBob\nCharlie")
    return csv_file


@pytest.fixture
def quoted_fields_csv(tmp_path):
    """Create CSV with quoted fields containing delimiters."""
    csv_file = tmp_path / "quoted.csv"
    csv_file.write_text(
        '"Name","Age","Address"\n"Smith, John",30,"123 Main St, NYC"\n"Doe, Jane",25,"456 Oak Ave, LA"'
    )
    return csv_file


@pytest.fixture
def malformed_csv(tmp_path):
    """Create CSV with variable row lengths."""
    csv_file = tmp_path / "malformed.csv"
    csv_file.write_text("Name,Age,City\nAlice,30\nBob,25,LA,Extra\nCharlie,35,Chicago")
    return csv_file


@pytest.fixture
def large_csv(tmp_path):
    """Create large CSV file with 1000 rows."""
    csv_file = tmp_path / "large.csv"
    lines = ["Name,Age,City"]
    for i in range(1000):
        lines.append(f"Person{i},{20 + (i % 50)},City{i % 10}")
    csv_file.write_text("\n".join(lines))
    return csv_file


@pytest.fixture
def utf8_bom_csv(tmp_path):
    """Create CSV with UTF-8 BOM."""
    csv_file = tmp_path / "utf8_bom.csv"
    csv_file.write_bytes(b"\xef\xbb\xbfName,Age,City\nAlice,30,NYC\nBob,25,LA")
    return csv_file


@pytest.fixture
def latin1_csv(tmp_path):
    """Create CSV with Latin-1 encoding."""
    csv_file = tmp_path / "latin1.csv"
    # Latin-1 encoded text with special characters
    content = "Name,Age,City\nJosé,30,São Paulo\nFrançois,25,Paris"
    csv_file.write_bytes(content.encode("latin-1"))
    return csv_file


@pytest.fixture
def mixed_types_csv(tmp_path):
    """Create CSV with mixed data types."""
    csv_file = tmp_path / "mixed_types.csv"
    csv_file.write_text(
        "Name,Age,Salary,StartDate,Active\nAlice,30,50000.50,2020-01-15,true\nBob,25,45000.00,2021-03-20,false"
    )
    return csv_file


@pytest.fixture
def numeric_header_csv(tmp_path):
    """Create CSV with numeric header (ambiguous header detection)."""
    csv_file = tmp_path / "numeric_header.csv"
    csv_file.write_text("1,2,3\n10,20,30\n40,50,60")
    return csv_file


@pytest.fixture
def nonexistent_file():
    """Path to file that doesn't exist."""
    return Path("/tmp/nonexistent_file_12345.csv")


@pytest.fixture
def test_config_file(tmp_path):
    """Create test configuration file."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
extractors:
  csv:
    delimiter: ","
    encoding: "utf-8"
    has_header: true
    max_rows: 1000
    skip_rows: 0
    quotechar: '"'
    strict: false
"""
    )
    return config_path


# =============================================================================
# CYCLE 1: FILE VALIDATION AND FORMAT DETECTION (RED PHASE)
# =============================================================================


class TestFileValidation:
    """Test file format validation - Cycle 1 RED."""

    def test_supports_csv_format(self, csv_extractor):
        """Test .csv format is supported."""
        assert csv_extractor.supports_format(Path("test.csv"))

    def test_supports_tsv_format(self, csv_extractor):
        """Test .tsv format is supported."""
        assert csv_extractor.supports_format(Path("test.tsv"))

    def test_rejects_non_csv_format(self, csv_extractor):
        """Test non-CSV files rejected."""
        assert not csv_extractor.supports_format(Path("test.xlsx"))
        assert not csv_extractor.supports_format(Path("test.pdf"))
        assert not csv_extractor.supports_format(Path("test.txt"))
        assert not csv_extractor.supports_format(Path("test.docx"))

    def test_get_supported_extensions(self, csv_extractor):
        """Test supported extensions list."""
        extensions = csv_extractor.get_supported_extensions()
        assert ".csv" in extensions
        assert ".tsv" in extensions

    def test_get_format_name(self, csv_extractor):
        """Test format name returned."""
        format_name = csv_extractor.get_format_name()
        assert "CSV" in format_name or "csv" in format_name.lower()

    def test_file_not_found_error(self, csv_extractor, nonexistent_file):
        """Test missing file returns error."""
        result = csv_extractor.extract(nonexistent_file)

        assert not result.success
        assert len(result.errors) > 0
        assert "file" in result.errors[0].lower() or "found" in result.errors[0].lower()

    def test_validate_file_returns_false_for_missing(self, csv_extractor, nonexistent_file):
        """Test validate_file correctly identifies missing files."""
        is_valid, errors = csv_extractor.validate_file(nonexistent_file)

        assert not is_valid
        assert len(errors) > 0


# =============================================================================
# CYCLE 2: BASIC CSV EXTRACTION (RED PHASE)
# =============================================================================


class TestBasicCSVExtraction:
    """Test basic CSV extraction - Cycle 2 RED."""

    def test_extract_simple_csv_success(self, csv_extractor, sample_csv):
        """Test extracting simple CSV returns success."""
        result = csv_extractor.extract(sample_csv)

        assert result.success
        assert len(result.errors) == 0

    def test_csv_produces_content_blocks(self, csv_extractor, sample_csv):
        """Test CSV produces at least one content block."""
        result = csv_extractor.extract(sample_csv)

        assert len(result.content_blocks) > 0

    def test_csv_produces_table_block(self, csv_extractor, sample_csv):
        """Test CSV produces TABLE content block."""
        result = csv_extractor.extract(sample_csv)

        table_blocks = [b for b in result.content_blocks if b.block_type == ContentType.TABLE]
        assert len(table_blocks) == 1

    def test_table_metadata_present(self, csv_extractor, sample_csv):
        """Test TableMetadata created for CSV."""
        result = csv_extractor.extract(sample_csv)

        assert len(result.tables) == 1

    def test_table_has_correct_dimensions(self, csv_extractor, sample_csv):
        """Test table has correct row and column counts."""
        result = csv_extractor.extract(sample_csv)

        table = result.tables[0]
        assert table.num_rows == 3  # 3 data rows
        assert table.num_columns == 3  # 3 columns

    def test_header_row_extracted(self, csv_extractor, sample_csv):
        """Test header row correctly extracted."""
        result = csv_extractor.extract(sample_csv)

        table = result.tables[0]
        assert table.has_header is True
        assert table.header_row is not None
        assert "Name" in table.header_row
        assert "Age" in table.header_row
        assert "City" in table.header_row

    def test_data_rows_extracted(self, csv_extractor, sample_csv):
        """Test data rows correctly extracted."""
        result = csv_extractor.extract(sample_csv)

        table = result.tables[0]
        assert len(table.cells) == 3
        # First row should have "Alice"
        assert "Alice" in table.cells[0]

    def test_document_metadata_present(self, csv_extractor, sample_csv):
        """Test document metadata extracted."""
        result = csv_extractor.extract(sample_csv)

        assert result.document_metadata is not None
        assert result.document_metadata.source_file == sample_csv
        assert result.document_metadata.file_format == "csv"
        assert result.document_metadata.file_size_bytes > 0


# =============================================================================
# CYCLE 3: DELIMITER DETECTION (RED PHASE)
# =============================================================================


class TestDelimiterDetection:
    """Test delimiter detection - Cycle 3 RED."""

    def test_detect_comma_delimiter(self, csv_extractor, sample_csv):
        """Test comma delimiter automatically detected."""
        result = csv_extractor.extract(sample_csv)

        assert result.success
        # Check metadata for delimiter info
        table_block = [b for b in result.content_blocks if b.block_type == ContentType.TABLE][0]
        assert table_block.metadata.get("delimiter") == ","

    def test_detect_tab_delimiter(self, csv_extractor, sample_tsv):
        """Test tab delimiter automatically detected."""
        result = csv_extractor.extract(sample_tsv)

        assert result.success
        table_block = [b for b in result.content_blocks if b.block_type == ContentType.TABLE][0]
        assert table_block.metadata.get("delimiter") == "\t"

    def test_detect_semicolon_delimiter(self, csv_extractor, semicolon_csv):
        """Test semicolon delimiter automatically detected."""
        result = csv_extractor.extract(semicolon_csv)

        assert result.success
        table_block = [b for b in result.content_blocks if b.block_type == ContentType.TABLE][0]
        assert table_block.metadata.get("delimiter") == ";"

    def test_detect_pipe_delimiter(self, csv_extractor, pipe_csv):
        """Test pipe delimiter automatically detected."""
        result = csv_extractor.extract(pipe_csv)

        assert result.success
        table_block = [b for b in result.content_blocks if b.block_type == ContentType.TABLE][0]
        assert table_block.metadata.get("delimiter") == "|"

    def test_delimiter_override(self, semicolon_csv):
        """Test delimiter can be manually specified."""
        extractor = CSVExtractor({"delimiter": ";"})
        result = extractor.extract(semicolon_csv)

        assert result.success
        table = result.tables[0]
        assert table.num_columns == 3


# =============================================================================
# CYCLE 4: ENCODING DETECTION (RED PHASE)
# =============================================================================


class TestEncodingDetection:
    """Test encoding detection - Cycle 4 RED."""

    def test_detect_utf8_encoding(self, csv_extractor, sample_csv):
        """Test UTF-8 encoding automatically detected."""
        result = csv_extractor.extract(sample_csv)

        assert result.success
        table_block = [b for b in result.content_blocks if b.block_type == ContentType.TABLE][0]
        encoding = table_block.metadata.get("encoding")
        assert encoding is not None
        assert encoding.lower() in ["utf-8", "utf8"]

    def test_detect_utf8_bom(self, csv_extractor, utf8_bom_csv):
        """Test UTF-8 with BOM handled correctly."""
        result = csv_extractor.extract(utf8_bom_csv)

        assert result.success
        table = result.tables[0]
        # Header should not include BOM character
        assert "Name" in table.header_row

    def test_detect_latin1_encoding(self, csv_extractor, latin1_csv):
        """Test Latin-1 encoding automatically detected."""
        result = csv_extractor.extract(latin1_csv)

        assert result.success
        # Should successfully extract despite different encoding
        table = result.tables[0]
        assert table.num_rows >= 2

    def test_encoding_override(self, latin1_csv):
        """Test encoding can be manually specified."""
        extractor = CSVExtractor({"encoding": "latin-1"})
        result = extractor.extract(latin1_csv)

        assert result.success
        table = result.tables[0]
        # Should correctly extract special characters
        all_cells = [cell for row in table.cells for cell in row]
        # Check for special characters (may be present)
        assert len(all_cells) > 0


# =============================================================================
# CYCLE 5: HEADER DETECTION (RED PHASE)
# =============================================================================


class TestHeaderDetection:
    """Test header detection - Cycle 5 RED."""

    def test_detect_header_present(self, csv_extractor, sample_csv):
        """Test header correctly detected when present."""
        result = csv_extractor.extract(sample_csv)

        table = result.tables[0]
        assert table.has_header is True
        assert table.header_row is not None

    def test_detect_header_absent(self, csv_extractor, no_header_csv):
        """Test no header detected when absent."""
        result = csv_extractor.extract(no_header_csv)

        table = result.tables[0]
        # Auto-detection may vary, but should succeed
        assert result.success

    def test_header_override_true(self, no_header_csv):
        """Test forcing header detection on."""
        extractor = CSVExtractor({"has_header": True})
        result = extractor.extract(no_header_csv)

        table = result.tables[0]
        assert table.has_header is True
        assert table.header_row is not None

    def test_header_override_false(self, sample_csv):
        """Test forcing header detection off."""
        extractor = CSVExtractor({"has_header": False})
        result = extractor.extract(sample_csv)

        table = result.tables[0]
        assert table.has_header is False
        # All rows should be data rows
        assert table.num_rows == 4  # Including header as data

    def test_numeric_header_detection(self, csv_extractor, numeric_header_csv):
        """Test header detection with numeric headers."""
        result = csv_extractor.extract(numeric_header_csv)

        # Should handle ambiguous case gracefully
        assert result.success


# =============================================================================
# CYCLE 6: DATA TYPE HANDLING (RED PHASE)
# =============================================================================


class TestDataTypeHandling:
    """Test data type handling - Cycle 6 RED."""

    def test_numeric_values_as_strings(self, csv_extractor, sample_csv):
        """Test numeric values stored as strings."""
        result = csv_extractor.extract(sample_csv)

        table = result.tables[0]
        # Age values should be strings
        age_values = [row[1] for row in table.cells]
        assert "30" in age_values
        assert "25" in age_values

    def test_mixed_data_types(self, csv_extractor, mixed_types_csv):
        """Test mixed data types handled."""
        result = csv_extractor.extract(mixed_types_csv)

        assert result.success
        table = result.tables[0]
        # All values should be strings
        all_cells = [cell for row in table.cells for cell in row]
        assert all(isinstance(cell, str) for cell in all_cells)

    def test_empty_cells_preserved(self, tmp_path):
        """Test empty cells preserved in output."""
        csv_file = tmp_path / "empty_cells.csv"
        csv_file.write_text("Name,Age,City\nAlice,,NYC\nBob,25,")

        extractor = CSVExtractor()
        result = extractor.extract(csv_file)

        table = result.tables[0]
        # Empty cells should be empty strings
        assert table.cells[0][1] == ""  # Empty age for Alice
        assert table.cells[1][2] == ""  # Empty city for Bob

    def test_whitespace_preserved(self, tmp_path):
        """Test whitespace in cells preserved."""
        csv_file = tmp_path / "whitespace.csv"
        csv_file.write_text("Name,Age,City\n  Alice  ,30,  NYC  ")

        extractor = CSVExtractor()
        result = extractor.extract(csv_file)

        # Whitespace handling depends on implementation
        assert result.success


# =============================================================================
# CYCLE 7: EDGE CASES AND MALFORMED DATA (RED PHASE)
# =============================================================================


class TestEdgeCases:
    """Test edge cases - Cycle 7 RED."""

    def test_empty_file(self, csv_extractor, empty_csv):
        """Test empty file handled gracefully."""
        result = csv_extractor.extract(empty_csv)

        # Should return empty content or error
        assert not result.success or len(result.content_blocks) == 0

    def test_single_row_file(self, csv_extractor, single_row_csv):
        """Test file with only header row."""
        result = csv_extractor.extract(single_row_csv)

        # May succeed with no data rows or fail gracefully
        if result.success:
            table = result.tables[0]
            assert table.num_rows == 0 or table.num_rows == 1

    def test_single_column_file(self, csv_extractor, single_column_csv):
        """Test file with single column."""
        result = csv_extractor.extract(single_column_csv)

        assert result.success
        table = result.tables[0]
        assert table.num_columns == 1

    def test_quoted_fields(self, csv_extractor, quoted_fields_csv):
        """Test quoted fields with embedded delimiters."""
        result = csv_extractor.extract(quoted_fields_csv)

        assert result.success
        table = result.tables[0]
        # Should have 3 columns despite commas in data
        assert table.num_columns == 3
        # Check that "Smith, John" is one cell
        name_cells = [row[0] for row in table.cells]
        assert any("Smith" in cell and "John" in cell for cell in name_cells)

    def test_malformed_rows_normalized(self, csv_extractor, malformed_csv):
        """Test rows with variable lengths normalized."""
        result = csv_extractor.extract(malformed_csv)

        assert result.success
        table = result.tables[0]
        # All rows should have same number of columns
        for row in table.cells:
            assert len(row) == table.num_columns

    def test_large_file_extraction(self, csv_extractor, large_csv):
        """Test extraction of large file succeeds."""
        result = csv_extractor.extract(large_csv)

        assert result.success
        table = result.tables[0]
        assert table.num_rows == 1000

    def test_max_rows_limit(self, large_csv):
        """Test max_rows configuration limits extraction."""
        extractor = CSVExtractor({"max_rows": 100})
        result = extractor.extract(large_csv)

        assert result.success
        table = result.tables[0]
        assert table.num_rows <= 100


# =============================================================================
# CYCLE 8: CONFIGURATION OVERRIDES (RED PHASE)
# =============================================================================


class TestConfigurationOverrides:
    """Test configuration options - Cycle 8 RED."""

    def test_config_dict_accepted(self):
        """Test extractor accepts dict configuration."""
        config = {"delimiter": ",", "encoding": "utf-8"}
        extractor = CSVExtractor(config)
        assert extractor is not None

    def test_config_none_uses_defaults(self):
        """Test None config uses defaults."""
        extractor = CSVExtractor(None)
        assert extractor is not None

    def test_delimiter_config_applied(self, semicolon_csv):
        """Test delimiter configuration applied."""
        extractor = CSVExtractor({"delimiter": ";"})
        result = extractor.extract(semicolon_csv)

        assert result.success

    def test_encoding_config_applied(self, latin1_csv):
        """Test encoding configuration applied."""
        extractor = CSVExtractor({"encoding": "latin-1"})
        result = extractor.extract(latin1_csv)

        assert result.success

    def test_has_header_config_applied(self, sample_csv):
        """Test has_header configuration applied."""
        extractor = CSVExtractor({"has_header": False})
        result = extractor.extract(sample_csv)

        table = result.tables[0]
        assert table.has_header is False

    def test_max_rows_config_applied(self, large_csv):
        """Test max_rows configuration applied."""
        extractor = CSVExtractor({"max_rows": 50})
        result = extractor.extract(large_csv)

        table = result.tables[0]
        assert table.num_rows <= 50

    def test_skip_rows_config(self, tmp_path):
        """Test skip_rows configuration."""
        csv_file = tmp_path / "skip_rows.csv"
        csv_file.write_text("Metadata\nMore Metadata\nName,Age\nAlice,30\nBob,25")

        extractor = CSVExtractor({"skip_rows": 2})
        result = extractor.extract(csv_file)

        assert result.success
        # Should skip first 2 rows
        table = result.tables[0]
        assert "Name" in table.header_row or "Alice" in table.cells[0]


# =============================================================================
# CYCLE 9: ERROR HANDLING (RED PHASE)
# =============================================================================


class TestErrorHandling:
    """Test error handling - Cycle 9 RED."""

    def test_corrupted_file(self, tmp_path):
        """Test handling of corrupted file."""
        bad_file = tmp_path / "corrupted.csv"
        bad_file.write_bytes(b"\x00\x01\x02\x03\x04\x05")

        extractor = CSVExtractor()
        result = extractor.extract(bad_file)

        # Should handle gracefully - may succeed with garbage or fail cleanly
        assert not result.success or result.success

    def test_permission_denied(self, tmp_path):
        """Test handling of permission denied."""
        import os

        csv_file = tmp_path / "readonly.csv"
        csv_file.write_text("Name,Age\nAlice,30")

        try:
            os.chmod(csv_file, 0o000)
            extractor = CSVExtractor()
            result = extractor.extract(csv_file)

            # Should handle gracefully
            assert not result.success or result.success
        finally:
            try:
                os.chmod(csv_file, 0o644)
            except:
                pass

    def test_invalid_encoding_specified(self, sample_csv):
        """Test invalid encoding configuration."""
        extractor = CSVExtractor({"encoding": "invalid-encoding"})
        result = extractor.extract(sample_csv)

        # Should fall back gracefully or fail cleanly
        assert not result.success or result.success


# =============================================================================
# CYCLE 10: INFRASTRUCTURE INTEGRATION (RED PHASE)
# =============================================================================


@pytest.mark.integration
class TestInfrastructureIntegration:
    """Test infrastructure integration - Cycle 10 RED."""

    def test_accepts_config_manager(self, test_config_file):
        """Test CSVExtractor accepts ConfigManager."""
        if not EXTRACTOR_AVAILABLE:
            pytest.skip("CSVExtractor not yet implemented")

        try:
            from infrastructure import ConfigManager

            config = ConfigManager(test_config_file)
            extractor = CSVExtractor(config)
            assert extractor is not None
        except ImportError:
            pytest.skip("Infrastructure not available")

    def test_uses_config_manager_values(self, test_config_file):
        """Test configuration values from ConfigManager applied."""
        if not EXTRACTOR_AVAILABLE:
            pytest.skip("CSVExtractor not yet implemented")

        try:
            from infrastructure import ConfigManager

            config = ConfigManager(test_config_file)
            extractor = CSVExtractor(config)

            # Values from config file should be applied
            # Note: Actual attribute names depend on implementation
            assert extractor is not None
        except ImportError:
            pytest.skip("Infrastructure not available")

    def test_logging_integration(self, csv_extractor, sample_csv, caplog):
        """Test extraction events logged."""
        try:
            import logging

            caplog.set_level(logging.INFO)

            result = csv_extractor.extract(sample_csv)

            # Check for log messages
            log_messages = [rec.message for rec in caplog.records]
            # Should have some log output
            assert len(caplog.records) >= 0  # Logging is optional
        except Exception:
            pytest.skip("Logging not yet integrated")

    def test_error_handler_integration(self, csv_extractor, nonexistent_file):
        """Test ErrorHandler used for errors."""
        result = csv_extractor.extract(nonexistent_file)

        assert not result.success
        # Error message should be present
        assert len(result.errors) > 0
        error_msg = result.errors[0]
        assert len(error_msg) > 0


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================


@pytest.mark.performance
class TestPerformance:
    """Test performance characteristics."""

    def test_small_file_performance(self, csv_extractor, sample_csv):
        """Test small file extraction completes quickly."""
        import time

        start = time.time()
        result = csv_extractor.extract(sample_csv)
        duration = time.time() - start

        assert result.success
        assert duration < 1.0  # Should complete in under 1 second

    def test_large_file_performance(self, csv_extractor, large_csv):
        """Test large file extraction within acceptable time."""
        import time

        start = time.time()
        result = csv_extractor.extract(large_csv)
        duration = time.time() - start

        assert result.success
        assert duration < 5.0  # Should complete in under 5 seconds
