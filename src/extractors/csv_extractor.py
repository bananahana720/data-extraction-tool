"""
CSV Extractor - CSV/TSV File Extraction

Extracts content from CSV/TSV files with support for:
- Auto-detection of delimiter (comma, tab, semicolon, pipe)
- Auto-detection of file encoding (UTF-8, Latin-1, CP1252, etc.)
- Auto-detection of header row presence
- Configuration overrides for all detection parameters
- Malformed data handling (variable row lengths)
- Large file support with max_rows limiting

Implementation follows strict TDD methodology with infrastructure integration.
"""

from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict, Any
from datetime import datetime, timezone
import hashlib
import logging
import time
import csv
import io

# Try to import chardet for encoding detection
try:
    import chardet

    CHARDET_AVAILABLE = True
except ImportError:
    CHARDET_AVAILABLE = False

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import (
    BaseExtractor,
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    Position,
    TableMetadata,
)

# Import infrastructure components
try:
    from src.infrastructure import (
        ConfigManager,
        get_logger,
        ErrorHandler,
        ProgressTracker,
        RecoveryAction,
    )

    INFRASTRUCTURE_AVAILABLE = True
except ImportError:
    INFRASTRUCTURE_AVAILABLE = False


class CSVExtractor(BaseExtractor):
    """
    Extracts content from CSV/TSV files.

    Supports CSV and TSV files with automatic detection of:
    - Delimiter (comma, tab, semicolon, pipe)
    - Encoding (UTF-8, Latin-1, CP1252, etc.)
    - Header row presence

    Design Notes:
    - Single TABLE ContentBlock per CSV file
    - Full grid structure stored in TableMetadata
    - All cells stored as strings (no type conversion)
    - Malformed rows normalized to consistent length
    - Configuration overrides available for all auto-detection

    Configuration:
        delimiter (str): CSV delimiter (default: auto-detect)
        encoding (str): File encoding (default: auto-detect)
        has_header (bool): First row is header (default: auto-detect)
        max_rows (int): Maximum rows to extract (default: None)
        skip_rows (int): Number of rows to skip at start (default: 0)
        quotechar (str): Quote character for fields (default: '"')
        strict (bool): Strict parsing mode (default: False)

    Example:
        >>> extractor = CSVExtractor()
        >>> result = extractor.extract(Path("data.csv"))
        >>> if result.success:
        ...     table = result.tables[0]
        ...     print(f"Rows: {table.num_rows}, Columns: {table.num_columns}")
    """

    def __init__(self, config: Optional[Union[dict, object]] = None):
        """
        Initialize CSV extractor with optional configuration.

        Args:
            config: Configuration options (dict or ConfigManager):
                - delimiter: CSV delimiter (default: auto-detect)
                - encoding: File encoding (default: auto-detect)
                - has_header: First row is header (default: auto-detect)
                - max_rows: Maximum rows to extract (default: None)
                - skip_rows: Number of rows to skip (default: 0)
                - quotechar: Quote character (default: '"')
                - strict: Strict parsing mode (default: False)
        """
        super().__init__(config if isinstance(config, dict) or config is None else {})

        # Detect ConfigManager
        is_config_manager = (
            INFRASTRUCTURE_AVAILABLE
            and hasattr(config, "__class__")
            and config.__class__.__name__ == "ConfigManager"
        )
        self._config_manager = config if is_config_manager else None

        # Initialize infrastructure
        if INFRASTRUCTURE_AVAILABLE:
            self.logger = get_logger(__name__)
            self.error_handler = ErrorHandler()
        else:
            self.logger = logging.getLogger(__name__)
            self.error_handler = None

        # Load configuration
        if self._config_manager:
            # From ConfigManager
            extractor_config = self._config_manager.get_section("extractors.csv", default={})
            self.delimiter = extractor_config.get("delimiter")
            self.encoding = extractor_config.get("encoding")
            self.has_header = extractor_config.get("has_header")
            self.max_rows = extractor_config.get("max_rows")
            self.skip_rows = extractor_config.get("skip_rows", 0)
            self.quotechar = extractor_config.get("quotechar", '"')
            self.strict = extractor_config.get("strict", False)
        elif isinstance(config, dict):
            # From dict (backward compatible)
            self.delimiter = config.get("delimiter")
            self.encoding = config.get("encoding")
            self.has_header = config.get("has_header")
            self.max_rows = config.get("max_rows")
            self.skip_rows = config.get("skip_rows", 0)
            self.quotechar = config.get("quotechar", '"')
            self.strict = config.get("strict", False)
        else:
            # Defaults
            self.delimiter = None
            self.encoding = None
            self.has_header = None
            self.max_rows = None
            self.skip_rows = 0
            self.quotechar = '"'
            self.strict = False

    def supports_format(self, file_path: Path) -> bool:
        """
        Check if file is a CSV or TSV file.

        Args:
            file_path: Path to check

        Returns:
            True if file has .csv or .tsv extension
        """
        return file_path.suffix.lower() in [".csv", ".tsv"]

    def get_supported_extensions(self) -> list[str]:
        """Return supported file extensions."""
        return [".csv", ".tsv"]

    def get_format_name(self) -> str:
        """Return human-readable format name."""
        return "CSV"

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract content from CSV file.

        Strategy:
        1. Validate file exists and is accessible
        2. Detect encoding (or use configured)
        3. Detect delimiter (or use configured)
        4. Read all rows using csv.reader
        5. Skip rows if configured
        6. Detect header row (or use configured)
        7. Normalize row lengths
        8. Apply max_rows limit if configured
        9. Create TableMetadata with full grid
        10. Create single TABLE ContentBlock
        11. Generate document metadata
        12. Return structured result

        Args:
            file_path: Path to CSV file

        Returns:
            ExtractionResult with single TABLE ContentBlock and metadata
        """
        start_time = time.time()

        # Log extraction start
        if INFRASTRUCTURE_AVAILABLE:
            self.logger.info("Starting CSV extraction", extra={"file": str(file_path)})

        errors = []
        warnings = []
        content_blocks = []
        tables = []

        # Step 1: Validate file
        is_valid, validation_errors = self.validate_file(file_path)
        if not is_valid:
            if self.error_handler:
                error = self.error_handler.create_error("E001", file_path=str(file_path))
                errors.append(self.error_handler.format_for_user(error))
                if INFRASTRUCTURE_AVAILABLE:
                    self.logger.error("File validation failed", extra={"file": str(file_path)})
            else:
                errors.extend(validation_errors)

            return ExtractionResult(
                success=False,
                errors=tuple(errors),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="csv",
                ),
            )

        try:
            # Step 2: Detect encoding
            detected_encoding = self.encoding or self._detect_encoding(file_path)

            # Step 3: Detect delimiter
            detected_delimiter = self.delimiter or self._detect_delimiter(
                file_path, detected_encoding
            )

            # Step 4: Read CSV file
            rows = self._read_csv_file(file_path, detected_encoding, detected_delimiter)

            # Handle empty file
            if not rows or len(rows) == 0:
                return ExtractionResult(
                    success=False,
                    errors=("CSV file is empty",),
                    document_metadata=DocumentMetadata(
                        source_file=file_path,
                        file_format="csv",
                    ),
                )

            # Step 5: Skip rows if configured
            if self.skip_rows > 0:
                rows = rows[self.skip_rows :]
                if not rows:
                    return ExtractionResult(
                        success=False,
                        errors=(f"No data remaining after skipping {self.skip_rows} rows",),
                        document_metadata=DocumentMetadata(
                            source_file=file_path,
                            file_format="csv",
                        ),
                    )

            # Step 6: Detect header
            detected_has_header = (
                self.has_header if self.has_header is not None else self._detect_header(rows)
            )

            # Extract header and data rows
            header_row = None
            data_rows = rows
            if detected_has_header and rows:
                header_row = rows[0]
                data_rows = rows[1:]

            # Step 7: Determine column count and normalize rows
            if header_row:
                column_count = len(header_row)
            elif data_rows:
                column_count = max(len(row) for row in data_rows)
            else:
                column_count = 0

            # Normalize all rows to same length
            normalized_data_rows = [self._normalize_row(row, column_count) for row in data_rows]

            # Step 8: Apply max_rows limit
            if self.max_rows is not None and len(normalized_data_rows) > self.max_rows:
                normalized_data_rows = normalized_data_rows[: self.max_rows]

            # Step 9: Create TableMetadata
            table_metadata = TableMetadata(
                num_rows=len(normalized_data_rows),
                num_columns=column_count,
                has_header=detected_has_header,
                header_row=tuple(header_row) if header_row else None,
                cells=tuple(tuple(row) for row in normalized_data_rows),
            )

            # Step 10: Create ContentBlock
            block_metadata = {
                "source_type": "csv",
                "file_path": str(file_path),
                "encoding": detected_encoding,
                "delimiter": detected_delimiter,
                "has_header": detected_has_header,
                "row_count": len(normalized_data_rows),
                "column_count": column_count,
                "table_id": str(table_metadata.table_id),
            }

            block = ContentBlock(
                block_type=ContentType.TABLE,
                content="",
                position=Position(sequence_index=0),
                confidence=1.0,
                metadata=block_metadata,
            )

            content_blocks.append(block)
            tables.append(table_metadata)

            # Step 11: Generate document metadata
            doc_metadata = self._extract_document_metadata(file_path, table_metadata)

            # Step 12: Log completion and return result
            duration = time.time() - start_time
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.info(
                    "CSV extraction complete",
                    extra={
                        "file": str(file_path),
                        "rows": len(normalized_data_rows),
                        "columns": column_count,
                        "duration_seconds": round(duration, 3),
                    },
                )

            return ExtractionResult(
                content_blocks=tuple(content_blocks),
                document_metadata=doc_metadata,
                tables=tuple(tables),
                success=True,
                warnings=tuple(warnings),
            )

        except PermissionError as e:
            if self.error_handler:
                error = self.error_handler.create_error("E500", file_path=str(file_path))
                errors.append(self.error_handler.format_for_user(error))
            else:
                errors.append(f"Permission denied reading file: {file_path}")

            if INFRASTRUCTURE_AVAILABLE:
                self.logger.error("Permission denied", extra={"file": str(file_path)})

        except Exception as e:
            if self.error_handler:
                error = self.error_handler.create_error(
                    "E170", file_path=str(file_path), original_exception=e
                )
                errors.append(self.error_handler.format_for_user(error))
            else:
                errors.append(f"Unexpected error during extraction: {str(e)}")

            if INFRASTRUCTURE_AVAILABLE:
                self.logger.error(
                    "Extraction failed", extra={"file": str(file_path), "error": str(e)}
                )

        # Return failed result
        return ExtractionResult(
            success=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
            document_metadata=DocumentMetadata(
                source_file=file_path,
                file_format="csv",
            ),
        )

    def _detect_encoding(self, file_path: Path) -> str:
        """
        Detect file encoding with UTF-8 → chardet → Latin-1 cascade.

        Algorithm:
        1. Try UTF-8 (most common)
        2. Check for UTF-8 BOM
        3. Use chardet on first 100KB if available
        4. Fallback to Latin-1 (always works)

        Args:
            file_path: Path to CSV file

        Returns:
            Detected encoding name
        """
        # Try UTF-8 first (most common)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                f.read(1024)
            return "utf-8"
        except UnicodeDecodeError:
            pass

        # Check for UTF-8 BOM
        try:
            with open(file_path, "rb") as f:
                first_bytes = f.read(3)
                if first_bytes == b"\xef\xbb\xbf":
                    return "utf-8-sig"
        except:
            pass

        # Use chardet if available
        if CHARDET_AVAILABLE:
            try:
                with open(file_path, "rb") as f:
                    raw_data = f.read(102400)  # 100KB

                detection = chardet.detect(raw_data)
                if detection["confidence"] > 0.7 and detection["encoding"]:
                    return detection["encoding"].lower()
            except Exception:
                pass

        # Fallback to Latin-1 (always works)
        return "latin-1"

    def _detect_delimiter(self, file_path: Path, encoding: str) -> str:
        """
        Detect CSV delimiter using csv.Sniffer with fallback.

        Algorithm:
        1. Read first 8KB of file
        2. Try csv.Sniffer.sniff()
        3. If fails, count delimiter candidates
        4. Return most common valid delimiter
        5. Default to comma if all fail

        Args:
            file_path: Path to CSV file
            encoding: File encoding to use

        Returns:
            Detected delimiter: ",", "\t", ";", "|"
        """
        try:
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                sample = f.read(8192)

            # Try csv.Sniffer
            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=",\t;|")
                return dialect.delimiter
            except csv.Error:
                pass

            # Fallback: count delimiter candidates
            delimiter_counts = {
                ",": sample.count(","),
                "\t": sample.count("\t"),
                ";": sample.count(";"),
                "|": sample.count("|"),
            }

            # Return most common delimiter
            max_delimiter = max(delimiter_counts, key=delimiter_counts.get)
            if delimiter_counts[max_delimiter] > 0:
                return max_delimiter

            # Default to comma
            return ","

        except Exception:
            return ","

    def _detect_header(self, rows: List[List[str]]) -> bool:
        """
        Detect header presence using multi-check heuristic.

        Algorithm:
        1. Check if first row has different data types than second row
        2. Check if first row values are unique
        3. Check if first row has longer strings (typical header pattern)
        4. Combine checks with weighted scoring

        Target accuracy: ≥95%

        Args:
            rows: List of rows (list of lists)

        Returns:
            True if header detected
        """
        if len(rows) < 2:
            return False

        first_row = rows[0]
        second_row = rows[1]

        score = 0.0

        # Check 1: Type consistency (headers are usually all text/non-numeric)
        first_numeric = sum(1 for cell in first_row if self._is_numeric(cell))
        second_numeric = sum(1 for cell in second_row if self._is_numeric(cell))

        if first_numeric < second_numeric:
            score += 0.4

        # Check 2: Uniqueness (headers are usually unique)
        if len(first_row) == len(set(first_row)):
            score += 0.3

        # Check 3: Length patterns (headers often longer, more descriptive)
        first_avg_len = (
            sum(len(str(cell)) for cell in first_row) / len(first_row) if first_row else 0
        )
        second_avg_len = (
            sum(len(str(cell)) for cell in second_row) / len(second_row) if second_row else 0
        )

        if first_avg_len > second_avg_len * 1.2:
            score += 0.3

        # Threshold: 0.5 = has header
        return score >= 0.5

    def _is_numeric(self, value: str) -> bool:
        """
        Check if string value is numeric.

        Args:
            value: String to check

        Returns:
            True if value is numeric
        """
        if not value or not isinstance(value, str):
            return False

        # Remove whitespace
        value = value.strip()

        # Check if it's a number (int or float)
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _normalize_row(self, row: List[str], expected_columns: int) -> List[str]:
        """
        Normalize row length by padding or truncating.

        Args:
            row: Input row
            expected_columns: Target column count

        Returns:
            Row with exactly expected_columns elements
        """
        if len(row) == expected_columns:
            return row
        elif len(row) < expected_columns:
            # Pad with empty strings
            return row + [""] * (expected_columns - len(row))
        else:
            # Truncate (log warning if infrastructure available)
            if INFRASTRUCTURE_AVAILABLE and self.logger:
                self.logger.warning(f"Truncating row from {len(row)} to {expected_columns} columns")
            return row[:expected_columns]

    def _read_csv_file(self, file_path: Path, encoding: str, delimiter: str) -> List[List[str]]:
        """
        Read CSV file and return rows.

        Args:
            file_path: Path to CSV file
            encoding: File encoding
            delimiter: CSV delimiter

        Returns:
            List of rows (each row is a list of strings)
        """
        rows = []

        try:
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                reader = csv.reader(
                    f, delimiter=delimiter, quotechar=self.quotechar, strict=self.strict
                )
                rows = list(reader)

            # Strip BOM from first cell of first row if present
            if rows and rows[0] and rows[0][0].startswith("\ufeff"):
                rows[0] = [rows[0][0][1:]] + list(rows[0][1:])

        except Exception as e:
            if INFRASTRUCTURE_AVAILABLE and self.logger:
                self.logger.error(f"Error reading CSV file: {str(e)}")
            raise

        return rows

    def _extract_document_metadata(
        self, file_path: Path, table_metadata: TableMetadata
    ) -> DocumentMetadata:
        """
        Extract document-level metadata from CSV file.

        Args:
            file_path: Path to file
            table_metadata: Table metadata for statistics

        Returns:
            DocumentMetadata with available properties
        """
        # File system metadata
        file_stat = file_path.stat()
        file_size = file_stat.st_size

        # Generate file hash
        file_hash = self._compute_file_hash(file_path)

        return DocumentMetadata(
            source_file=file_path,
            file_format="csv",
            file_size_bytes=file_size,
            file_hash=file_hash,
            table_count=1,
            extracted_at=datetime.now(timezone.utc),
            extractor_version="1.0.6",
        )

    def _compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA256 hash of file for deduplication.

        Args:
            file_path: Path to file

        Returns:
            Hex string of SHA256 hash
        """
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()
