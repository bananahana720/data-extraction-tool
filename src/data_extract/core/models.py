"""Core data models for the data extraction pipeline.

This module defines Pydantic v2 models for pipeline data flow:
- Entity: Domain entities (risk, control, policy, process, regulation, issue)
- Metadata: Provenance and quality tracking for documents and chunks
- Document: Processed document after extraction with entities and metadata
- Chunk: Semantic chunk for RAG with quality scoring and readability metrics
- ProcessingContext: Shared pipeline state (config, logger, metrics)

All models use Pydantic v2 for runtime validation and type safety.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EntityType(str, Enum):
    """Audit domain entity types.

    Six entity types recognized in audit documents for consistent
    naming and cross-reference resolution.

    Values:
        PROCESS: Business or operational processes
        RISK: Identified risks or risk factors
        CONTROL: Control measures or procedures
        REGULATION: Regulatory requirements or standards
        POLICY: Organizational policies or guidelines
        ISSUE: Identified issues, findings, or audit observations
    """

    PROCESS = "process"
    RISK = "risk"
    CONTROL = "control"
    REGULATION = "regulation"
    POLICY = "policy"
    ISSUE = "issue"


class Entity(BaseModel):
    """Domain entity extracted from documents.

    Represents entities from the audit domain: risk, control, policy,
    process, regulation, issue. Used by Document and Chunk models.

    Attributes:
        type: Entity type from EntityType enum
        id: Canonical entity identifier (e.g., 'Risk-123')
        text: Entity text content as it appears in document
        confidence: Confidence score (0.0-1.0) for entity extraction
        location: Character position in document (start and end indices)
    """

    model_config = ConfigDict(frozen=False)

    type: EntityType = Field(..., description="Entity type from EntityType enum")
    id: str = Field(..., description="Canonical entity identifier (e.g., Risk-123)")
    text: str = Field(..., description="Entity text content as it appears in document")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for entity extraction (0.0-1.0)",
    )
    location: Dict[str, int] = Field(
        ...,
        description="Character position in document (start and end indices)",
    )


class Metadata(BaseModel):
    """Provenance and quality tracking metadata.

    Embedded in Document and Chunk models to track processing history,
    quality metrics, and audit trail information.

    Attributes:
        source_file: Path to original source file
        file_hash: SHA-256 hash of source file for integrity verification
        processing_timestamp: When the document/chunk was processed
        tool_version: Version of the data extraction tool
        config_version: Version of the configuration used
        document_type: Type of document (e.g., 'pdf', 'docx', 'xlsx')
        quality_scores: Quality metrics dict (e.g., {'ocr_confidence': 0.95})
        quality_flags: List of quality warnings/flags
        entity_tags: List of canonical entity IDs for RAG retrieval filtering
        entity_counts: Count of entities by type (e.g., {'risk': 5, 'control': 3})
    """

    model_config = ConfigDict(frozen=False)

    source_file: Path = Field(..., description="Path to original source file")
    file_hash: str = Field(
        ..., description="SHA-256 hash of source file for integrity verification"
    )
    processing_timestamp: datetime = Field(..., description="When the document/chunk was processed")
    tool_version: str = Field(..., description="Version of the data extraction tool")
    config_version: str = Field(..., description="Version of the configuration used")
    document_type: str = Field(..., description="Type of document (e.g., pdf, docx)")
    quality_scores: Dict[str, float] = Field(
        default_factory=dict, description="Quality metrics (e.g., ocr_confidence)"
    )
    quality_flags: List[str] = Field(
        default_factory=list, description="List of quality warnings/flags"
    )
    entity_tags: List[str] = Field(
        default_factory=list,
        description="List of canonical entity IDs for RAG retrieval filtering",
    )
    entity_counts: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of entities by type (e.g., {'risk': 5, 'control': 3})",
    )


class Document(BaseModel):
    """Processed document model.

    Type contract: Extract → Normalize stage.
    Represents a document after extraction with raw/cleaned text,
    extracted entities, and processing metadata.

    Attributes:
        id: Unique document identifier
        text: Document text content (raw or normalized)
        entities: List of extracted entities
        metadata: Processing metadata and quality tracking
        structure: Document structure metadata (e.g., sections, pages)
    """

    model_config = ConfigDict(frozen=False)

    id: str = Field(..., description="Unique document identifier")
    text: str = Field(..., description="Document text content")
    entities: List[Entity] = Field(default_factory=list, description="List of extracted entities")
    metadata: Metadata = Field(..., description="Processing metadata and quality tracking")
    structure: Dict[str, Any] = Field(
        default_factory=dict,
        description="Document structure metadata (e.g., sections, pages)",
    )


class Chunk(BaseModel):
    """Semantic chunk for RAG (Retrieval-Augmented Generation).

    Type contract: Chunk → Semantic stage.
    Represents a semantically coherent chunk with quality scoring,
    readability metrics, and full provenance tracking.

    Attributes:
        id: Unique chunk identifier (format: {source}_{index:03d})
        text: Chunk text content
        document_id: Reference to parent document
        position_index: Position in original document (0-based)
        token_count: Number of tokens in chunk
        word_count: Number of words in chunk
        entities: List of entities in this chunk
        section_context: Section/heading context for this chunk
        quality_score: Overall quality score (0.0-1.0)
        readability_scores: Readability metrics dict (e.g., flesch_reading_ease)
        metadata: Processing metadata and quality tracking
    """

    model_config = ConfigDict(frozen=False)

    id: str = Field(..., description="Unique chunk identifier (format: {source}_{index:03d})")
    text: str = Field(..., description="Chunk text content")
    document_id: str = Field(..., description="Reference to parent document")
    position_index: int = Field(..., ge=0, description="Position in original document (0-based)")
    token_count: int = Field(..., ge=0, description="Number of tokens in chunk")
    word_count: int = Field(..., ge=0, description="Number of words in chunk")
    entities: List[Entity] = Field(
        default_factory=list, description="List of entities in this chunk"
    )
    section_context: str = Field(default="", description="Section/heading context for this chunk")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Overall quality score (0.0-1.0)")
    readability_scores: Dict[str, float] = Field(
        default_factory=dict, description="Readability metrics (e.g., flesch_reading_ease)"
    )
    metadata: Metadata = Field(..., description="Processing metadata and quality tracking")


class ProcessingContext(BaseModel):
    """Shared pipeline state passed through all stages.

    Carries configuration, logger, and metrics through the entire
    pipeline to ensure deterministic processing and audit trail.

    Attributes:
        config: Configuration dictionary (three-tier precedence: CLI > env > YAML > defaults)
        logger: Structured logger instance for audit trail
        metrics: Metrics accumulation dictionary
    """

    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration dictionary (CLI > env > YAML > defaults)",
    )
    logger: Optional[Any] = Field(
        default=None, description="Structured logger instance for audit trail"
    )
    metrics: Dict[str, Any] = Field(
        default_factory=dict, description="Metrics accumulation dictionary"
    )
