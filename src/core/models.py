"""
Core data models for the extraction system.

These are the foundation data structures that flow through the entire pipeline.
Every module (extractors, processors, formatters) uses these models.

Design Principles:
- Immutable (frozen dataclasses) to prevent accidental mutations
- Rich metadata to support tracking and debugging
- Type-safe with full type hints
- Serializable for persistence and debugging
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4


class ContentType(str, Enum):
    """Types of content blocks in extracted documents."""

    # Text content
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    LIST_ITEM = "list_item"
    QUOTE = "quote"
    CODE = "code"

    # Structured content
    TABLE = "table"
    TABLE_CELL = "table_cell"

    # Media content
    IMAGE = "image"
    CHART = "chart"

    # Metadata content
    METADATA = "metadata"
    FOOTNOTE = "footnote"
    COMMENT = "comment"
    HYPERLINK = "hyperlink"

    # Unknown/fallback
    UNKNOWN = "unknown"


class ProcessingStage(str, Enum):
    """Stages in the extraction pipeline."""

    VALIDATION = "validation"
    EXTRACTION = "extraction"
    CONTEXT_LINKING = "context_linking"
    METADATA_AGGREGATION = "metadata_aggregation"
    IMAGE_ANALYSIS = "image_analysis"
    QUALITY_VALIDATION = "quality_validation"
    FORMATTING = "formatting"
    EXPORT = "export"


@dataclass(frozen=True)
class Position:
    """Location information for content within a document."""

    page: Optional[int] = None  # Page number (1-indexed)
    slide: Optional[int] = None  # Slide number for presentations
    sheet: Optional[str] = None  # Sheet name for spreadsheets

    # Bounding box (when available)
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None

    # Sequence information
    sequence_index: Optional[int] = None  # Order within document

    def __repr__(self) -> str:
        parts = []
        if self.page is not None:
            parts.append(f"page={self.page}")
        if self.slide is not None:
            parts.append(f"slide={self.slide}")
        if self.sheet is not None:
            parts.append(f"sheet={self.sheet}")
        if self.sequence_index is not None:
            parts.append(f"seq={self.sequence_index}")
        return f"Position({', '.join(parts)})"


@dataclass(frozen=True)
class ContentBlock:
    """
    A single unit of extracted content.

    This is the atomic unit - everything is composed of ContentBlocks.
    Immutable to prevent accidental modification during processing.
    """

    # Core identity
    block_id: UUID = field(default_factory=uuid4)
    block_type: ContentType = ContentType.UNKNOWN

    # Content
    content: str = ""  # Primary text content
    raw_content: Optional[str] = None  # Original content before processing

    # Location
    position: Optional[Position] = None

    # Relationships
    parent_id: Optional[UUID] = None  # Parent block (e.g., heading for paragraph)
    related_ids: tuple[UUID, ...] = field(
        default_factory=tuple
    )  # Related blocks (captions, footnotes)

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    confidence: Optional[float] = None  # Extraction confidence (0.0-1.0)

    # Style information (optional, format-dependent)
    style: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"ContentBlock(type={self.block_type.value}, content='{content_preview}')"


@dataclass(frozen=True)
class ImageMetadata:
    """Metadata for extracted images."""

    image_id: UUID = field(default_factory=uuid4)
    file_path: Optional[Path] = None  # Where image is saved

    # Image properties
    format: Optional[str] = None  # PNG, JPEG, etc.
    width: Optional[int] = None
    height: Optional[int] = None
    color_mode: Optional[str] = None  # RGB, RGBA, L, etc.
    dpi: Optional[int] = None

    # Content metadata
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    image_type: Optional[str] = None  # photo, diagram, chart, screenshot

    # Hashing for deduplication
    content_hash: Optional[str] = None

    # Quality indicators
    is_low_quality: bool = False
    quality_issues: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TableMetadata:
    """Metadata for extracted tables."""

    table_id: UUID = field(default_factory=uuid4)

    # Structure
    num_rows: int = 0
    num_columns: int = 0
    has_header: bool = False
    header_row: Optional[tuple[str, ...]] = None

    # Content
    cells: tuple[tuple[str, ...], ...] = field(default_factory=tuple)  # Row-major order

    # Formatting
    merged_cells: tuple[tuple[int, int, int, int], ...] = field(
        default_factory=tuple
    )  # (row, col, rowspan, colspan)


@dataclass(frozen=True)
class DocumentMetadata:
    """Document-level metadata extracted or computed."""

    # Source information
    source_file: Path
    file_format: str
    file_size_bytes: int = 0
    file_hash: Optional[str] = None

    # Document properties
    title: Optional[str] = None
    author: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    subject: Optional[str] = None
    keywords: tuple[str, ...] = field(default_factory=tuple)

    # Statistics
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    character_count: Optional[int] = None
    image_count: int = 0
    table_count: int = 0

    # Language and content analysis
    language: Optional[str] = None  # ISO 639-1 code (en, es, fr, etc.)
    content_summary: Optional[str] = None

    # Extraction metadata
    extracted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    extractor_version: Optional[str] = None
    extraction_duration_seconds: Optional[float] = None


@dataclass(frozen=True)
class ExtractionResult:
    """
    Result of extraction stage.

    This is what extractors produce - raw content blocks without enrichment.
    """

    # Core data
    content_blocks: tuple[ContentBlock, ...] = field(default_factory=tuple)
    document_metadata: DocumentMetadata = field(
        default_factory=lambda: DocumentMetadata(source_file=Path("unknown"), file_format="unknown")
    )

    # Media assets
    images: tuple[ImageMetadata, ...] = field(default_factory=tuple)
    tables: tuple[TableMetadata, ...] = field(default_factory=tuple)

    # Extraction status
    success: bool = True
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def __len__(self) -> int:
        """Number of content blocks."""
        return len(self.content_blocks)

    def __repr__(self) -> str:
        return (
            f"ExtractionResult(blocks={len(self.content_blocks)}, "
            f"images={len(self.images)}, tables={len(self.tables)}, "
            f"success={self.success})"
        )


@dataclass(frozen=True)
class ProcessingResult:
    """
    Result of processing stage.

    Processing stages take ExtractionResult and enrich it.
    This includes context linking, metadata aggregation, quality validation.
    """

    # Enriched data (replaces content_blocks in ExtractionResult)
    content_blocks: tuple[ContentBlock, ...] = field(default_factory=tuple)
    document_metadata: DocumentMetadata = field(
        default_factory=lambda: DocumentMetadata(source_file=Path("unknown"), file_format="unknown")
    )

    # Media assets (preserved from ExtractionResult)
    images: tuple[ImageMetadata, ...] = field(default_factory=tuple)
    tables: tuple[TableMetadata, ...] = field(default_factory=tuple)

    # Processing metadata
    processing_stage: ProcessingStage = ProcessingStage.EXTRACTION
    stage_metadata: dict[str, Any] = field(default_factory=dict)

    # Quality information
    quality_score: Optional[float] = None  # 0.0-100.0
    quality_issues: tuple[str, ...] = field(default_factory=tuple)
    needs_review: bool = False

    # Status
    success: bool = True
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class FormattedOutput:
    """
    Result of formatting stage.

    This is what formatters produce - ready for export.
    """

    # Output content
    content: str  # Formatted output (JSON, Markdown, etc.)
    format_type: str  # json, markdown, chunked, etc.

    # Output metadata
    source_document: Path
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Additional files (e.g., extracted images, metadata sidecars)
    additional_files: tuple[Path, ...] = field(default_factory=tuple)

    # Status
    success: bool = True
    errors: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class PipelineResult:
    """
    Complete result of running the extraction pipeline.

    This is the final output that includes all stages.
    """

    # Source
    source_file: Path

    # Results from each stage
    extraction_result: Optional[ExtractionResult] = None
    processing_result: Optional[ProcessingResult] = None
    formatted_outputs: tuple[FormattedOutput, ...] = field(default_factory=tuple)

    # Overall status
    success: bool = True
    failed_stage: Optional[ProcessingStage] = None

    # Timing information
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None

    # Aggregated errors and warnings
    all_errors: tuple[str, ...] = field(default_factory=tuple)
    all_warnings: tuple[str, ...] = field(default_factory=tuple)

    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else f"FAILED at {self.failed_stage}"
        return f"PipelineResult(file={self.source_file.name}, status={status})"


# Type aliases for clarity
ExtractionInput = Path  # Input to extraction is always a file path
ProcessingInput = ExtractionResult  # Input to processing is extraction result
FormattingInput = ProcessingResult  # Input to formatting is processing result
