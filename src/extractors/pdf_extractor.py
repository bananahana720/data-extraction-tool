"""
PDF Extractor - PDF Document Extraction

Extracts content from PDF files with native text extraction and OCR fallback.

Features:
- Native text extraction using pypdf
- OCR fallback using pytesseract for image-based PDFs
- Table detection and structure preservation
- Image metadata extraction
- Multi-page document support
- Infrastructure integration (ConfigManager, LoggingFramework, ErrorHandler)

Performance Targets:
- <2s/MB for native text extraction
- <15s/page for OCR extraction
- 98% accuracy for native formats
- 85% accuracy for OCR extraction
"""

import hashlib
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union

try:
    import pypdf
    from pypdf import PdfReader

    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False
    if TYPE_CHECKING:
        from pypdf import PdfReader

try:
    import pdf2image
    import pytesseract
    from PIL import Image

    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import pdfplumber

    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    BaseExtractor,
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    ImageMetadata,
    Position,
    TableMetadata,
)

# Import infrastructure components
try:
    from infrastructure import (
        ConfigManager,
        ErrorHandler,
        ProgressTracker,
        get_logger,
    )

    INFRASTRUCTURE_AVAILABLE = True
except ImportError:
    INFRASTRUCTURE_AVAILABLE = False


class PdfExtractor(BaseExtractor):
    """
    Extracts content from PDF files.

    Uses pypdf for native text extraction and pytesseract for OCR fallback
    when PDFs contain scanned images instead of native text.

    Example:
        >>> extractor = PdfExtractor()
        >>> result = extractor.extract(Path("document.pdf"))
        >>> if result.success:
        ...     for block in result.content_blocks:
        ...         print(f"Page {block.position.page}: {block.content}")
    """

    def __init__(self, config: Optional[Union[dict, object]] = None):
        """
        Initialize PDF extractor with optional configuration.

        Args:
            config: Configuration options (dict or ConfigManager):
                - use_ocr: Enable OCR fallback (default: True)
                - tesseract_cmd: Path to tesseract executable (default: None)
                - poppler_path: Path to poppler bin directory (default: None)
                - ocr_dpi: DPI for OCR image conversion (default: 300)
                - ocr_lang: Language for OCR (default: "eng")
                - extract_images: Extract image metadata (default: True)
                - extract_tables: Extract table structures (default: True)
                - min_text_threshold: Min chars to consider native text (default: 10)
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
            cfg = self._config_manager.get_section("extractors.pdf", default={})
            self.use_ocr = self._get_config_value(cfg, "use_ocr", True)
            self.tesseract_cmd = cfg.get("tesseract_cmd", None)
            self.poppler_path = cfg.get("poppler_path", None)
            self.ocr_dpi = cfg.get("ocr_dpi", 300)
            self.ocr_lang = cfg.get("ocr_lang", "eng")
            self.extract_images = self._get_config_value(cfg, "extract_images", True)
            self.extract_tables = self._get_config_value(cfg, "extract_tables", True)
            self.min_text_threshold = cfg.get("min_text_threshold", 10)
        elif isinstance(config, dict):
            self.use_ocr = config.get("use_ocr", True)
            self.tesseract_cmd = config.get("tesseract_cmd", None)
            self.poppler_path = config.get("poppler_path", None)
            self.ocr_dpi = config.get("ocr_dpi", 300)
            self.ocr_lang = config.get("ocr_lang", "eng")
            self.extract_images = config.get("extract_images", True)
            self.extract_tables = config.get("extract_tables", True)
            self.min_text_threshold = config.get("min_text_threshold", 10)
        else:
            self.use_ocr = True
            self.tesseract_cmd = None
            self.poppler_path = None
            self.ocr_dpi = 300
            self.ocr_lang = "eng"
            self.extract_images = True
            self.extract_tables = True
            self.min_text_threshold = 10

        # Configure pytesseract if custom path provided
        if self.tesseract_cmd and TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.info(f"Using custom Tesseract path: {self.tesseract_cmd}")

    def _get_config_value(self, config_dict, key, default):
        """Helper to handle False values correctly."""
        value = config_dict.get(key)
        return value if value is not None else default

    def supports_format(self, file_path: Path) -> bool:
        """
        Check if file is a PDF file.

        Args:
            file_path: Path to check

        Returns:
            True if file has .pdf extension
        """
        return file_path.suffix.lower() == ".pdf"

    def get_supported_extensions(self) -> list[str]:
        """Return supported file extensions."""
        return [".pdf"]

    def get_format_name(self) -> str:
        """Return human-readable format name."""
        return "PDF"

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract content from PDF file.

        Strategy:
        1. Validate file exists and is accessible
        2. Try native text extraction with pypdf
        3. If text is minimal, fall back to OCR
        4. Extract tables if configured
        5. Extract image metadata if configured
        6. Generate document metadata
        7. Return structured result

        Args:
            file_path: Path to PDF file

        Returns:
            ExtractionResult with content blocks and metadata

        Note:
            - Returns success=False for file-level errors
            - Returns partial results if some pages fail
            - Uses OCR fallback automatically if native text is insufficient
        """
        start_time = time.time()

        # Log extraction start
        if INFRASTRUCTURE_AVAILABLE:
            self.logger.info("Starting PDF extraction", extra={"file": str(file_path)})

        errors = []
        warnings = []
        content_blocks = []
        images = []
        tables = []

        # Step 1: Validate file
        is_valid, validation_errors = self.validate_file(file_path)
        if not is_valid:
            if self.error_handler:
                error = self.error_handler.create_error("E001", file_path=str(file_path))
                errors.append(self.error_handler.format_for_user(error))
                if INFRASTRUCTURE_AVAILABLE:
                    self.logger.error(
                        "File validation failed",
                        extra={"file": str(file_path), "errors": validation_errors},
                    )
            else:
                errors.extend(validation_errors)

            return ExtractionResult(
                success=False,
                errors=tuple(errors),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="pdf",
                ),
            )

        # Check dependencies
        if not PYPDF_AVAILABLE:
            errors.append("pypdf library not available. Install with: pip install pypdf")
            return ExtractionResult(
                success=False,
                errors=tuple(errors),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="pdf",
                ),
            )

        try:
            # Step 2: Try native text extraction
            reader = PdfReader(str(file_path))
            page_count = len(reader.pages)

            if INFRASTRUCTURE_AVAILABLE:
                self.logger.info(
                    f"PDF has {page_count} pages",
                    extra={"file": str(file_path), "pages": page_count},
                )

            # Extract text from each page
            sequence_index = 0
            native_text_extracted = False

            for page_num, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text()

                    if text and len(text.strip()) >= self.min_text_threshold:
                        native_text_extracted = True

                        # Split page text into blocks with heading detection
                        page_blocks, sequence_index = self._split_text_into_blocks(
                            text, page_num, sequence_index
                        )
                        content_blocks.extend(page_blocks)

                except Exception as e:
                    warnings.append(f"Failed to extract text from page {page_num}: {str(e)}")
                    if INFRASTRUCTURE_AVAILABLE:
                        self.logger.warning(
                            f"Page {page_num} extraction failed", extra={"error": str(e)}
                        )

            # Step 3: OCR fallback if needed
            if not native_text_extracted and self.use_ocr:
                if INFRASTRUCTURE_AVAILABLE:
                    self.logger.info(
                        "Minimal native text found, attempting OCR", extra={"file": str(file_path)}
                    )

                if self._needs_ocr(file_path):
                    ocr_blocks = self._extract_with_ocr(file_path)
                    content_blocks.extend(ocr_blocks)
                    if INFRASTRUCTURE_AVAILABLE:
                        self.logger.info(
                            f"OCR extracted {len(ocr_blocks)} blocks",
                            extra={"file": str(file_path)},
                        )
            elif not native_text_extracted and not self.use_ocr:
                warnings.append("No native text found and OCR is disabled")

            # Step 4: Extract tables if configured
            if self.extract_tables and PDFPLUMBER_AVAILABLE:
                try:
                    extracted_tables = self._extract_tables(file_path)
                    tables.extend(extracted_tables)
                except Exception as e:
                    warnings.append(f"Table extraction failed: {str(e)}")

            # Step 5: Extract image metadata if configured
            if self.extract_images:
                try:
                    extracted_images = self._extract_image_metadata(reader, file_path)
                    images.extend(extracted_images)
                except Exception as e:
                    warnings.append(f"Image extraction failed: {str(e)}")

            # Step 6: Generate document metadata
            doc_metadata = self._extract_document_metadata(file_path, reader)

            # Update statistics
            total_chars = sum(len(b.content) for b in content_blocks)
            total_words = sum(len(b.content.split()) for b in content_blocks)

            doc_metadata = DocumentMetadata(
                source_file=doc_metadata.source_file,
                file_format=doc_metadata.file_format,
                file_size_bytes=doc_metadata.file_size_bytes,
                file_hash=doc_metadata.file_hash,
                title=doc_metadata.title,
                author=doc_metadata.author,
                created_date=doc_metadata.created_date,
                modified_date=doc_metadata.modified_date,
                subject=doc_metadata.subject,
                keywords=doc_metadata.keywords,
                page_count=page_count,
                word_count=total_words,
                character_count=total_chars,
                image_count=len(images),
                table_count=len(tables),
                extracted_at=doc_metadata.extracted_at,
                extractor_version="0.1.0",
                extraction_duration_seconds=time.time() - start_time,
            )

            # Step 7: Log completion and return result
            duration = time.time() - start_time
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.info(
                    "PDF extraction complete",
                    extra={
                        "file": str(file_path),
                        "blocks": len(content_blocks),
                        "pages": page_count,
                        "tables": len(tables),
                        "images": len(images),
                        "duration_seconds": round(duration, 3),
                    },
                )

            return ExtractionResult(
                content_blocks=tuple(content_blocks),
                document_metadata=doc_metadata,
                images=tuple(images),
                tables=tuple(tables),
                success=True,
                warnings=tuple(warnings),
            )

        except Exception as e:
            if self.error_handler:
                error = self.error_handler.create_error(
                    "E130", file_path=str(file_path), original_exception=e
                )
                errors.append(self.error_handler.format_for_user(error))
            else:
                errors.append(f"PDF extraction error: {str(e)}")

            if INFRASTRUCTURE_AVAILABLE:
                self.logger.error(
                    "Extraction failed", extra={"file": str(file_path), "error": str(e)}
                )

            return ExtractionResult(
                success=False,
                errors=tuple(errors),
                warnings=tuple(warnings),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="pdf",
                ),
            )

    def _needs_ocr(self, file_path: Path) -> bool:
        """
        Determine if PDF requires OCR (is image-based).

        Args:
            file_path: Path to PDF file

        Returns:
            True if OCR is needed
        """
        try:
            reader = PdfReader(str(file_path))

            total_text = ""
            for page in reader.pages[:3]:  # Check first 3 pages
                text = page.extract_text()
                if text:
                    total_text += text

            # If very little native text, assume image-based
            return len(total_text.strip()) < self.min_text_threshold

        except Exception:
            # If we can't determine, assume OCR is needed
            return True

    def _extract_with_ocr(self, file_path: Path) -> List[ContentBlock]:
        """
        Extract text using OCR (pytesseract).

        Args:
            file_path: Path to PDF file

        Returns:
            List of ContentBlock with OCR-extracted text
        """
        blocks = []

        if not TESSERACT_AVAILABLE:
            return blocks

        try:
            # Convert PDF pages to images
            convert_kwargs = {"dpi": self.ocr_dpi}
            if self.poppler_path:
                convert_kwargs["poppler_path"] = self.poppler_path

            images = pdf2image.convert_from_path(str(file_path), **convert_kwargs)

            sequence_index = 0
            for page_num, image in enumerate(images, start=1):
                try:
                    # Run OCR
                    ocr_data = pytesseract.image_to_data(
                        image, lang=self.ocr_lang, output_type=pytesseract.Output.DICT
                    )

                    # Extract text with confidence
                    page_text = []
                    confidences = []

                    for i, text in enumerate(ocr_data["text"]):
                        if text.strip():
                            page_text.append(text)
                            conf = (
                                float(ocr_data["conf"][i]) / 100.0
                                if ocr_data["conf"][i] != -1
                                else 0.0
                            )
                            confidences.append(conf)

                    if page_text:
                        combined_text = " ".join(page_text)
                        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

                        block = ContentBlock(
                            block_type=ContentType.PARAGRAPH,
                            content=combined_text,
                            raw_content=combined_text,
                            position=Position(page=page_num, sequence_index=sequence_index),
                            confidence=avg_confidence,
                            metadata={
                                "page": page_num,
                                "extraction_method": "ocr",
                                "ocr_dpi": self.ocr_dpi,
                                "ocr_lang": self.ocr_lang,
                                "char_count": len(combined_text),
                                "word_count": len(combined_text.split()),
                            },
                        )
                        blocks.append(block)
                        sequence_index += 1

                except Exception as e:
                    if INFRASTRUCTURE_AVAILABLE:
                        self.logger.warning(
                            f"OCR failed for page {page_num}", extra={"error": str(e)}
                        )

        except Exception as e:
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.error("OCR conversion failed", extra={"error": str(e)})

        return blocks

    def _extract_tables(self, file_path: Path) -> List[TableMetadata]:
        """
        Extract tables from PDF using pdfplumber.

        Args:
            file_path: Path to PDF file

        Returns:
            List of TableMetadata
        """
        tables = []

        try:
            import pdfplumber

            with pdfplumber.open(str(file_path)) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()

                    for table_data in page_tables:
                        if table_data and len(table_data) > 0:
                            # Assume first row is header
                            has_header = True
                            header_row = tuple(table_data[0]) if has_header else None
                            cells = tuple(tuple(row) for row in table_data)

                            num_rows = len(table_data)
                            num_columns = len(table_data[0]) if table_data else 0

                            table = TableMetadata(
                                num_rows=num_rows,
                                num_columns=num_columns,
                                has_header=has_header,
                                header_row=header_row,
                                cells=cells,
                            )
                            tables.append(table)

        except Exception as e:
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.warning("Table extraction failed", extra={"error": str(e)})

        return tables

    def _extract_image_metadata(self, reader: "PdfReader", file_path: Path) -> List[ImageMetadata]:
        """
        Extract image metadata from PDF.

        Args:
            reader: PdfReader instance
            file_path: Path to PDF file

        Returns:
            List of ImageMetadata
        """
        images = []

        try:
            for page_num, page in enumerate(reader.pages, start=1):
                if "/XObject" in page["/Resources"]:
                    xobjects = page["/Resources"]["/XObject"].get_object()

                    for obj_name in xobjects:
                        obj = xobjects[obj_name]

                        if obj["/Subtype"] == "/Image":
                            try:
                                width = obj["/Width"]
                                height = obj["/Height"]

                                # Determine format
                                if "/Filter" in obj:
                                    filter_type = obj["/Filter"]
                                    if filter_type == "/DCTDecode":
                                        img_format = "JPEG"
                                    elif filter_type == "/FlateDecode":
                                        img_format = "PNG"
                                    else:
                                        img_format = str(filter_type)
                                else:
                                    img_format = "Unknown"

                                image_meta = ImageMetadata(
                                    width=width,
                                    height=height,
                                    format=img_format,
                                )
                                images.append(image_meta)

                            except Exception as e:
                                if INFRASTRUCTURE_AVAILABLE:
                                    self.logger.warning(
                                        f"Failed to extract image metadata on page {page_num}",
                                        extra={"error": str(e)},
                                    )

        except Exception as e:
            if INFRASTRUCTURE_AVAILABLE:
                self.logger.warning("Image metadata extraction failed", extra={"error": str(e)})

        return images

    def _extract_document_metadata(self, file_path: Path, reader: "PdfReader") -> DocumentMetadata:
        """
        Extract document-level metadata from PDF file.

        Args:
            file_path: Path to file
            reader: PdfReader instance

        Returns:
            DocumentMetadata with available properties
        """
        # File system metadata
        file_stat = file_path.stat()
        file_size = file_stat.st_size

        # Generate file hash
        file_hash = self._compute_file_hash(file_path)

        # Extract PDF metadata
        metadata = reader.metadata if reader.metadata else {}

        title = metadata.get("/Title", None)
        author = metadata.get("/Author", None)
        subject = metadata.get("/Subject", None)
        keywords_str = metadata.get("/Keywords", None)

        # Parse keywords
        keywords = ()
        if keywords_str:
            keywords = tuple(k.strip() for k in str(keywords_str).split(",") if k.strip())

        # Parse dates
        created_date = None
        modified_date = None

        try:
            creation_date = metadata.get("/CreationDate", None)
            if creation_date:
                # PDF dates are in format: D:YYYYMMDDHHmmSS
                date_str = str(creation_date).replace("D:", "")[:14]
                created_date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
        except Exception:
            pass

        try:
            mod_date = metadata.get("/ModDate", None)
            if mod_date:
                date_str = str(mod_date).replace("D:", "")[:14]
                modified_date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
        except Exception:
            pass

        return DocumentMetadata(
            source_file=file_path,
            file_format="pdf",
            file_size_bytes=file_size,
            file_hash=file_hash,
            title=title,
            author=author,
            created_date=created_date,
            modified_date=modified_date,
            subject=subject,
            keywords=keywords,
            extracted_at=datetime.now(tz=None),
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

    def _is_likely_heading(self, line: str, next_line: Optional[str] = None) -> tuple[bool, int]:
        """
        Heuristic to determine if a line of text is likely a heading.

        PDFs don't have explicit style information, so we use heuristics:
        - Short lines (< 80 chars)
        - Title Case or ALL CAPS patterns
        - Common heading patterns (Section N:, Chapter N, etc.)
        - Not ending with sentence punctuation
        - Standalone (surrounded by blank lines or followed by normal text)

        Args:
            line: Text line to evaluate
            next_line: Optional next line for context

        Returns:
            Tuple of (is_heading, level) where level is 1-3
        """
        line_stripped = line.strip()

        if not line_stripped or len(line_stripped) > 100:
            return (False, 0)

        # Check for common heading patterns
        import re

        # Pattern 1: Section/Chapter/Part markers
        section_pattern = r"^(Section|Chapter|Part|Article|Appendix)\s+\d+[:\.]?\s*"
        if re.match(section_pattern, line_stripped, re.IGNORECASE):
            return (True, 2)

        # Pattern 2: Numbered sections (1.0, 1.1, etc.)
        numbered_section = r"^\d+\.(\d+\.)*\s+"
        if re.match(numbered_section, line_stripped):
            # Count depth: 1.0 = level 1, 1.1 = level 2, 1.1.1 = level 3
            depth = line_stripped.split()[0].count(".")
            level = min(depth + 1, 3)
            return (True, level)

        # Pattern 3: ALL CAPS (likely heading if short)
        if line_stripped.isupper() and len(line_stripped) < 60:
            return (True, 1)

        # Pattern 4: Title Case detection
        # Count words that start with capital letters
        words = line_stripped.split()
        if len(words) >= 2 and len(words) <= 15:
            # Ignore common lowercase words
            lowercase_ok = {
                "a",
                "an",
                "and",
                "as",
                "at",
                "by",
                "for",
                "in",
                "of",
                "on",
                "or",
                "the",
                "to",
                "with",
            }
            capitalized_count = sum(1 for w in words if w[0].isupper() or w.lower() in lowercase_ok)

            # If most words are capitalized, it's likely Title Case
            if capitalized_count / len(words) >= 0.7:
                # Check that it doesn't end with sentence punctuation
                if not line_stripped.endswith((".", "!", "?")):
                    # Short lines are more likely headings
                    if len(line_stripped) < 80:
                        return (True, 2)

        return (False, 0)

    def _split_text_into_blocks(
        self, text: str, page_num: int, sequence_index: int
    ) -> tuple[List[ContentBlock], int]:
        """
        Split page text into content blocks with heading detection.

        Args:
            text: Raw page text
            page_num: Page number
            sequence_index: Starting sequence index

        Returns:
            Tuple of (list of ContentBlocks, next sequence_index)
        """
        blocks = []
        lines = text.split("\n")

        current_paragraph = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                # Flush current paragraph if any
                if current_paragraph:
                    content = "\n".join(current_paragraph)
                    block = ContentBlock(
                        block_type=ContentType.PARAGRAPH,
                        content=content,
                        position=Position(page=page_num, sequence_index=sequence_index),
                        confidence=1.0,
                        metadata={
                            "page": page_num,
                            "extraction_method": "native",
                        },
                    )
                    blocks.append(block)
                    sequence_index += 1
                    current_paragraph = []
                i += 1
                continue

            # Check if line is a heading
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else None
            is_heading, level = self._is_likely_heading(line, next_line)

            if is_heading:
                # Flush current paragraph first
                if current_paragraph:
                    content = "\n".join(current_paragraph)
                    block = ContentBlock(
                        block_type=ContentType.PARAGRAPH,
                        content=content,
                        position=Position(page=page_num, sequence_index=sequence_index),
                        confidence=1.0,
                        metadata={
                            "page": page_num,
                            "extraction_method": "native",
                        },
                    )
                    blocks.append(block)
                    sequence_index += 1
                    current_paragraph = []

                # Create heading block
                block = ContentBlock(
                    block_type=ContentType.HEADING,
                    content=line,
                    position=Position(page=page_num, sequence_index=sequence_index),
                    confidence=0.9,  # Slightly lower confidence for heuristic detection
                    metadata={
                        "page": page_num,
                        "extraction_method": "native",
                        "level": level,
                    },
                )
                blocks.append(block)
                sequence_index += 1
            else:
                # Add to current paragraph
                current_paragraph.append(line)

            i += 1

        # Flush remaining paragraph
        if current_paragraph:
            content = "\n".join(current_paragraph)
            block = ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content=content,
                position=Position(page=page_num, sequence_index=sequence_index),
                confidence=1.0,
                metadata={
                    "page": page_num,
                    "extraction_method": "native",
                },
            )
            blocks.append(block)
            sequence_index += 1

        return (blocks, sequence_index)
