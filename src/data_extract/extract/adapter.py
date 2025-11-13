"""Adapter pattern for brownfield-to-greenfield extractor integration.

This module implements the adapter pattern to bridge brownfield extractors
(src/extractors/) with greenfield Document models (src/data_extract/core/models.py).

Architecture:
    Brownfield Extractor → ExtractionResult → ExtractorAdapter → Document (greenfield)

Design Principles:
- Zero modifications to brownfield extractors (ADAPT, don't refactor)
- Thin adapter layer (only model conversion, no business logic)
- Type-safe with mypy strict mode compliance
- Immutable outputs following greenfield conventions
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Protocol, TypeVar, runtime_checkable
from uuid import uuid4

from pydantic import ValidationError

from src.core.models import ExtractionResult as BrownfieldExtractionResult
from src.data_extract.core.models import (
    Document,
    Entity,
    Metadata,
    QualityFlag,
    ValidationReport,
)

# Version information for metadata
TOOL_VERSION = "0.1.0"  # Data extraction tool version
CONFIG_VERSION = "1.0.0"  # Configuration schema version

# Type variables for Protocol (contravariant input, covariant output)
TInput = TypeVar("TInput", contravariant=True)
TOutput = TypeVar("TOutput", covariant=True)


@runtime_checkable
class PipelineStage(Protocol[TInput, TOutput]):
    """Protocol for pipeline stages in greenfield architecture.

    All pipeline stages must implement this protocol to ensure type-safe
    composition and compatibility with the greenfield pipeline runner.

    Type Parameters:
        TInput: Input type (e.g., Path for extractors)
        TOutput: Output type (e.g., Document for extractors)
    """

    def process(self, input_data: TInput) -> TOutput:
        """Process input and return output.

        Args:
            input_data: Input to process (type specified by TInput)

        Returns:
            Processed output (type specified by TOutput)

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValidationError: If output model fails Pydantic validation
            RuntimeError: If processing fails critically
        """
        ...


class ExtractorAdapter:
    """Base adapter for wrapping brownfield extractors.

    Converts brownfield ExtractionResult to greenfield Document model.
    Provides common utilities for all format-specific adapters.

    Attributes:
        extractor: Brownfield extractor instance (e.g., PdfExtractor)
        format_name: Human-readable format name (e.g., "PDF", "DOCX")
    """

    def __init__(self, extractor: Any, format_name: str) -> None:
        """Initialize adapter with brownfield extractor.

        Args:
            extractor: Brownfield extractor instance with extract(Path) method
            format_name: Human-readable format name for metadata
        """
        self.extractor = extractor
        self.format_name = format_name

    def process(self, input_data: Path) -> Document:
        """Extract and convert file to greenfield Document.

        Implements PipelineStage protocol. Delegates extraction to brownfield
        extractor, then converts result to greenfield Document model.

        Args:
            input_data: Path to file to extract

        Returns:
            Document: Greenfield document model with full metadata

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValidationError: If Document model validation fails
            RuntimeError: If extraction fails critically
        """
        if not input_data.exists():
            raise FileNotFoundError(f"File not found: {input_data}")

        # Delegate to brownfield extractor
        extraction_result = self.extractor.extract(input_data)

        # Check for critical failure
        if not extraction_result.success and extraction_result.errors:
            error_msg = "; ".join(extraction_result.errors)
            raise RuntimeError(f"Extraction failed for {input_data.name}: {error_msg}")

        # Convert to greenfield Document
        try:
            document = self._convert_to_document(extraction_result, input_data)
        except ValidationError as e:
            raise ValidationError(f"Document validation failed for {input_data.name}: {e}") from e

        return document

    def _convert_to_document(
        self, result: BrownfieldExtractionResult, source_file: Path
    ) -> Document:
        """Convert brownfield ExtractionResult to greenfield Document.

        Core conversion logic called by process(). Handles model transformation,
        metadata mapping, and validation report generation.

        Args:
            result: Brownfield extraction result
            source_file: Path to source file

        Returns:
            Document: Greenfield document model
        """
        # Generate unique document ID
        doc_id = self._generate_document_id(source_file)

        # Concatenate content blocks into document text
        text = self._concatenate_content_blocks(result)

        # Convert metadata
        metadata = self._convert_metadata(result, source_file)

        # Preserve document structure
        structure = self._extract_structure_metadata(result)

        # Entities are populated by normalizer stage (empty for now)
        entities: List[Entity] = []

        return Document(
            id=doc_id,
            text=text,
            entities=entities,
            metadata=metadata,
            structure=structure,
        )

    def _generate_document_id(self, source_file: Path) -> str:
        """Generate unique document identifier.

        Uses filename stem plus timestamp to ensure uniqueness across
        multiple processing runs of same file.

        Args:
            source_file: Path to source file

        Returns:
            Unique document identifier (format: filename_uuid)
        """
        # Use filename stem + UUID for uniqueness
        stem = source_file.stem.replace(" ", "_").replace("-", "_")
        unique_id = str(uuid4())[:8]
        return f"{stem}_{unique_id}"

    def _concatenate_content_blocks(self, result: BrownfieldExtractionResult) -> str:
        """Concatenate content blocks into document text.

        Preserves block order using sequence_index from Position metadata.
        Joins blocks with double newlines for readability.

        Args:
            result: Brownfield extraction result

        Returns:
            Concatenated text from all content blocks
        """
        # Sort blocks by sequence_index to preserve document order
        sorted_blocks = sorted(
            result.content_blocks,
            key=lambda b: (
                b.position.sequence_index if b.position and b.position.sequence_index else 0
            ),
        )

        # Join with double newlines for readability
        return "\n\n".join(block.content for block in sorted_blocks if block.content.strip())

    def _convert_metadata(self, result: BrownfieldExtractionResult, source_file: Path) -> Metadata:
        """Convert brownfield metadata to greenfield Metadata model.

        Maps document-level metadata, quality scores, OCR confidence,
        and generates validation report.

        Args:
            result: Brownfield extraction result
            source_file: Path to source file

        Returns:
            Greenfield Metadata model
        """
        # Compute file hash for integrity verification
        file_hash = self._compute_file_hash(source_file)

        # Extract OCR confidence scores by page
        ocr_confidence = self._extract_ocr_confidence(result)

        # Generate validation report
        validation_report = self._generate_validation_report(result, ocr_confidence)

        # Build quality scores dict
        quality_scores: Dict[str, float] = {}
        if validation_report.document_average_confidence is not None:
            quality_scores["ocr_confidence"] = validation_report.document_average_confidence

        # Extract quality flags (convert enum to string)
        quality_flags = [flag.value for flag in validation_report.quality_flags]

        return Metadata(
            source_file=source_file,
            file_hash=file_hash,
            processing_timestamp=datetime.now(timezone.utc),
            tool_version=TOOL_VERSION,
            config_version=CONFIG_VERSION,
            document_type=None,  # Will be set by classifier in normalize stage
            document_subtype=None,
            quality_scores=quality_scores,
            quality_flags=quality_flags,
            ocr_confidence=ocr_confidence,
            completeness_ratio=None,  # Computed by validator in normalize stage
            entity_tags=[],  # Populated by normalizer
            entity_counts={},  # Populated by normalizer
            config_snapshot={},  # Can be populated by pipeline runner
            validation_report=validation_report.model_dump(),  # Serialize ValidationReport
        )

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of file for integrity verification.

        Args:
            file_path: Path to file

        Returns:
            SHA-256 hash as hex string
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _extract_ocr_confidence(self, result: BrownfieldExtractionResult) -> Dict[int, float]:
        """Extract per-page OCR confidence scores from content blocks.

        Aggregates confidence scores by page number from ContentBlock metadata.

        Args:
            result: Brownfield extraction result

        Returns:
            Dict mapping page number to average confidence score (0.0-1.0)
        """
        page_confidences: Dict[int, List[float]] = {}

        for block in result.content_blocks:
            # Extract page number and confidence
            if not block.position or block.position.page is None:
                continue

            page_num = block.position.page
            confidence = block.confidence if block.confidence is not None else 1.0

            if page_num not in page_confidences:
                page_confidences[page_num] = []
            page_confidences[page_num].append(confidence)

        # Compute average confidence per page
        return {
            page: sum(scores) / len(scores) for page, scores in page_confidences.items() if scores
        }

    def _generate_validation_report(
        self, result: BrownfieldExtractionResult, ocr_confidence: Dict[int, float]
    ) -> ValidationReport:
        """Generate validation report from extraction result.

        Assesses quality, detects issues, and makes quarantine recommendation.

        Args:
            result: Brownfield extraction result
            ocr_confidence: Per-page OCR confidence scores

        Returns:
            ValidationReport with quality assessment
        """
        quality_flags: List[QualityFlag] = []
        extraction_gaps: List[str] = []

        # Compute document-level average confidence
        doc_avg_confidence = None
        if ocr_confidence:
            doc_avg_confidence = sum(ocr_confidence.values()) / len(ocr_confidence)
            # Flag if below 95% threshold
            if doc_avg_confidence < 0.95:
                quality_flags.append(QualityFlag.LOW_OCR_CONFIDENCE)
                extraction_gaps.append(
                    f"OCR confidence {doc_avg_confidence:.2%} below 95% threshold"
                )

        # Check for extraction warnings/errors
        if result.warnings:
            quality_flags.append(QualityFlag.INCOMPLETE_EXTRACTION)
            extraction_gaps.extend(result.warnings)

        if result.errors:
            quality_flags.append(QualityFlag.INCOMPLETE_EXTRACTION)
            extraction_gaps.extend(result.errors)

        # Count missing images (images without extraction)
        missing_images_count = len(
            [img for img in result.images if img.quality_issues or img.is_low_quality]
        )
        if missing_images_count > 0:
            quality_flags.append(QualityFlag.MISSING_IMAGES)

        # Quarantine recommendation: flag if any quality issues exist
        quarantine_recommended = len(quality_flags) > 0

        return ValidationReport(
            quarantine_recommended=quarantine_recommended,
            confidence_scores=ocr_confidence,
            quality_flags=quality_flags,
            extraction_gaps=extraction_gaps,
            document_average_confidence=doc_avg_confidence,
            scanned_pdf_detected=None,  # Format-specific adapters can set this
            completeness_passed=True,  # Default to true; validator stage will reassess
            missing_images_count=missing_images_count,
            complex_objects_count=0,  # Format-specific adapters can set this
        )

    def _extract_structure_metadata(self, result: BrownfieldExtractionResult) -> Dict[str, Any]:
        """Extract document structure metadata from extraction result.

        Preserves page counts, word counts, image/table counts, and other
        structural information for downstream stages.

        Args:
            result: Brownfield extraction result

        Returns:
            Dict with structure metadata
        """
        doc_meta = result.document_metadata

        return {
            "page_count": doc_meta.page_count,
            "word_count": doc_meta.word_count,
            "character_count": doc_meta.character_count,
            "image_count": len(result.images),
            "table_count": len(result.tables),
            "title": doc_meta.title,
            "author": doc_meta.author,
            "created_date": doc_meta.created_date.isoformat() if doc_meta.created_date else None,
            "modified_date": (
                doc_meta.modified_date.isoformat() if doc_meta.modified_date else None
            ),
            "language": doc_meta.language,
            "keywords": list(doc_meta.keywords) if doc_meta.keywords else [],
        }
