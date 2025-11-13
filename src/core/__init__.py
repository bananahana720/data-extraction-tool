"""
Core module - Foundation data models and interfaces.

This module defines the contracts that all other modules must follow.

Public API:
    Data Models:
        - ContentBlock: Atomic unit of extracted content
        - ExtractionResult: Output from extractors
        - ProcessingResult: Output from processors
        - FormattedOutput: Output from formatters
        - PipelineResult: Complete pipeline output

    Interfaces:
        - BaseExtractor: Interface for format extractors
        - BaseProcessor: Interface for content processors
        - BaseFormatter: Interface for output formatters
        - BasePipeline: Interface for pipeline orchestrators

    Enums:
        - ContentType: Types of content blocks
        - ProcessingStage: Pipeline stages
"""

# Data models
# Interfaces
from .interfaces import (
    BaseExtractor,
    BaseFormatter,
    BasePipeline,
    BaseProcessor,
)
from .models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    FormattedOutput,
    ImageMetadata,
    PipelineResult,
    Position,
    ProcessingResult,
    ProcessingStage,
    TableMetadata,
)

__all__ = [
    # Data models
    "ContentBlock",
    "ContentType",
    "DocumentMetadata",
    "ExtractionResult",
    "FormattedOutput",
    "ImageMetadata",
    "PipelineResult",
    "Position",
    "ProcessingResult",
    "ProcessingStage",
    "TableMetadata",
    # Interfaces
    "BaseExtractor",
    "BaseFormatter",
    "BasePipeline",
    "BaseProcessor",
]
