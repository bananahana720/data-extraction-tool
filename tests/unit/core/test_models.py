"""Unit tests for core data models.

Tests cover:
- Valid model instantiation
- Field validation constraints
- Pydantic ValidationError for invalid data
- Edge cases (empty values, boundary conditions)
"""

from datetime import datetime
from pathlib import Path

import pytest
import structlog
from pydantic import ValidationError

from src.data_extract.core.models import (
    Chunk,
    Document,
    Entity,
    Metadata,
    ProcessingContext,
)


class TestEntity:
    """Test Entity model validation and instantiation."""

    def test_entity_valid_creation(self):
        """Test Entity instantiation with valid data."""
        entity = Entity(
            type="risk",
            id="RISK-001",
            text="High operational risk identified",
            confidence=0.85,
        )
        assert entity.type == "risk"
        assert entity.id == "RISK-001"
        assert entity.text == "High operational risk identified"
        assert entity.confidence == 0.85

    def test_entity_confidence_boundary_valid(self):
        """Test Entity confidence at boundary values (0.0 and 1.0)."""
        entity_min = Entity(type="control", id="C-001", text="Control", confidence=0.0)
        assert entity_min.confidence == 0.0

        entity_max = Entity(type="policy", id="P-001", text="Policy", confidence=1.0)
        assert entity_max.confidence == 1.0

    def test_entity_confidence_below_zero_invalid(self):
        """Test Entity with confidence < 0.0 raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Entity(type="risk", id="R-001", text="Risk", confidence=-0.1)
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_entity_confidence_above_one_invalid(self):
        """Test Entity with confidence > 1.0 raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Entity(type="risk", id="R-001", text="Risk", confidence=1.5)
        assert "less than or equal to 1" in str(exc_info.value).lower()

    def test_entity_missing_required_fields(self):
        """Test Entity with missing required fields raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Entity(type="risk", id="R-001")  # Missing text and confidence
        assert "field required" in str(exc_info.value).lower()

    def test_entity_empty_text_valid(self):
        """Test Entity with empty text is valid (edge case)."""
        entity = Entity(type="issue", id="I-001", text="", confidence=0.5)
        assert entity.text == ""


class TestMetadata:
    """Test Metadata model validation and instantiation."""

    def test_metadata_valid_creation(self):
        """Test Metadata instantiation with all required fields."""
        metadata = Metadata(
            source_file=Path("/path/to/document.pdf"),
            file_hash="abc123def456",
            processing_timestamp=datetime(2025, 11, 10, 10, 30),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        assert metadata.source_file == Path("/path/to/document.pdf")
        assert metadata.file_hash == "abc123def456"
        assert metadata.tool_version == "1.0.0"
        assert metadata.config_version == "v1"
        assert metadata.document_type == "pdf"
        assert metadata.quality_scores == {}
        assert metadata.quality_flags == []

    def test_metadata_with_quality_metrics(self):
        """Test Metadata with quality scores and flags."""
        metadata = Metadata(
            source_file=Path("document.pdf"),
            file_hash="hash123",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
            quality_scores={"ocr_confidence": 0.95, "text_density": 0.8},
            quality_flags=["low_contrast", "skewed_image"],
        )
        assert metadata.quality_scores["ocr_confidence"] == 0.95
        assert metadata.quality_scores["text_density"] == 0.8
        assert "low_contrast" in metadata.quality_flags
        assert "skewed_image" in metadata.quality_flags

    def test_metadata_missing_required_fields(self):
        """Test Metadata with missing required fields raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Metadata(
                source_file=Path("doc.pdf"),
                file_hash="hash",
            )  # Missing other required fields
        assert "field required" in str(exc_info.value).lower()


class TestDocument:
    """Test Document model validation and instantiation."""

    def test_document_valid_creation(self):
        """Test Document instantiation with valid data."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash123",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        document = Document(
            id="DOC-001",
            text="Document text content",
            metadata=metadata,
        )
        assert document.id == "DOC-001"
        assert document.text == "Document text content"
        assert document.entities == []
        assert document.structure == {}
        assert document.metadata.document_type == "pdf"

    def test_document_with_entities(self):
        """Test Document with embedded entities."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        entities = [
            Entity(type="risk", id="R-001", text="Risk 1", confidence=0.9),
            Entity(type="control", id="C-001", text="Control 1", confidence=0.85),
        ]
        document = Document(
            id="DOC-001",
            text="Document with entities",
            entities=entities,
            metadata=metadata,
        )
        assert len(document.entities) == 2
        assert document.entities[0].type == "risk"
        assert document.entities[1].type == "control"

    def test_document_with_structure(self):
        """Test Document with structure metadata."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        document = Document(
            id="DOC-001",
            text="Structured document",
            metadata=metadata,
            structure={"pages": 10, "sections": ["intro", "body", "conclusion"]},
        )
        assert document.structure["pages"] == 10
        assert len(document.structure["sections"]) == 3

    def test_document_empty_text_valid(self):
        """Test Document with empty text (edge case)."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        document = Document(id="DOC-001", text="", metadata=metadata)
        assert document.text == ""


class TestChunk:
    """Test Chunk model validation and instantiation."""

    def test_chunk_valid_creation(self):
        """Test Chunk instantiation with valid data."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        chunk = Chunk(
            id="doc_001",
            text="Chunk text content",
            document_id="DOC-001",
            position_index=0,
            token_count=100,
            word_count=80,
            quality_score=0.85,
            metadata=metadata,
        )
        assert chunk.id == "doc_001"
        assert chunk.text == "Chunk text content"
        assert chunk.document_id == "DOC-001"
        assert chunk.position_index == 0
        assert chunk.token_count == 100
        assert chunk.word_count == 80
        assert chunk.quality_score == 0.85
        assert chunk.entities == []
        assert chunk.section_context == ""
        assert chunk.readability_scores == {}

    def test_chunk_quality_score_boundary_valid(self):
        """Test Chunk quality_score at boundary values (0.0 and 1.0)."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        chunk_min = Chunk(
            id="doc_001",
            text="Low quality",
            document_id="DOC-001",
            position_index=0,
            token_count=10,
            word_count=8,
            quality_score=0.0,
            metadata=metadata,
        )
        assert chunk_min.quality_score == 0.0

        chunk_max = Chunk(
            id="doc_002",
            text="High quality",
            document_id="DOC-001",
            position_index=1,
            token_count=10,
            word_count=8,
            quality_score=1.0,
            metadata=metadata,
        )
        assert chunk_max.quality_score == 1.0

    def test_chunk_quality_score_below_zero_invalid(self):
        """Test Chunk with quality_score < 0.0 raises ValidationError."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        with pytest.raises(ValidationError) as exc_info:
            Chunk(
                id="doc_001",
                text="Chunk",
                document_id="DOC-001",
                position_index=0,
                token_count=10,
                word_count=8,
                quality_score=-0.1,
                metadata=metadata,
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_chunk_quality_score_above_one_invalid(self):
        """Test Chunk with quality_score > 1.0 raises ValidationError."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        with pytest.raises(ValidationError) as exc_info:
            Chunk(
                id="doc_001",
                text="Chunk",
                document_id="DOC-001",
                position_index=0,
                token_count=10,
                word_count=8,
                quality_score=1.5,
                metadata=metadata,
            )
        assert "less than or equal to 1" in str(exc_info.value).lower()

    def test_chunk_with_entities_and_readability(self):
        """Test Chunk with entities and readability scores."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        entities = [Entity(type="risk", id="R-001", text="Risk", confidence=0.9)]
        chunk = Chunk(
            id="doc_001",
            text="Chunk with metrics",
            document_id="DOC-001",
            position_index=0,
            token_count=50,
            word_count=40,
            quality_score=0.9,
            entities=entities,
            section_context="Section 1: Introduction",
            readability_scores={"flesch_reading_ease": 65.0, "grade_level": 8.5},
            metadata=metadata,
        )
        assert len(chunk.entities) == 1
        assert chunk.section_context == "Section 1: Introduction"
        assert chunk.readability_scores["flesch_reading_ease"] == 65.0
        assert chunk.readability_scores["grade_level"] == 8.5

    def test_chunk_position_index_negative_invalid(self):
        """Test Chunk with negative position_index raises ValidationError."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        with pytest.raises(ValidationError) as exc_info:
            Chunk(
                id="doc_001",
                text="Chunk",
                document_id="DOC-001",
                position_index=-1,
                token_count=10,
                word_count=8,
                quality_score=0.5,
                metadata=metadata,
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_chunk_token_count_negative_invalid(self):
        """Test Chunk with negative token_count raises ValidationError."""
        metadata = Metadata(
            source_file=Path("doc.pdf"),
            file_hash="hash",
            processing_timestamp=datetime.now(),
            tool_version="1.0.0",
            config_version="v1",
            document_type="pdf",
        )
        with pytest.raises(ValidationError) as exc_info:
            Chunk(
                id="doc_001",
                text="Chunk",
                document_id="DOC-001",
                position_index=0,
                token_count=-10,
                word_count=8,
                quality_score=0.5,
                metadata=metadata,
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()


class TestProcessingContext:
    """Test ProcessingContext model validation and instantiation."""

    def test_processing_context_valid_creation(self):
        """Test ProcessingContext instantiation with config dict."""
        context = ProcessingContext(
            config={"batch_size": 100, "max_workers": 4},
            metrics={"processed_files": 0, "errors": 0},
        )
        assert context.config["batch_size"] == 100
        assert context.config["max_workers"] == 4
        assert context.metrics["processed_files"] == 0
        assert context.logger is None

    def test_processing_context_with_logger(self):
        """Test ProcessingContext with structlog logger."""
        logger = structlog.get_logger().bind(component="test")
        context = ProcessingContext(
            config={"mode": "batch"},
            logger=logger,
            metrics={},
        )
        assert context.logger is not None
        assert context.config["mode"] == "batch"

    def test_processing_context_empty_config(self):
        """Test ProcessingContext with empty config (edge case)."""
        context = ProcessingContext()
        assert context.config == {}
        assert context.metrics == {}
        assert context.logger is None

    def test_processing_context_metrics_accumulation(self):
        """Test ProcessingContext metrics can be mutated (for accumulation)."""
        context = ProcessingContext(metrics={"count": 0})
        assert context.metrics["count"] == 0

        # Metrics should be mutable for accumulation
        context.metrics["count"] += 1
        assert context.metrics["count"] == 1

        context.metrics["errors"] = 5
        assert context.metrics["errors"] == 5
