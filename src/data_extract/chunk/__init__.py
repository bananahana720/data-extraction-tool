"""Semantic chunking pipeline stage.

This module contains chunking strategies for RAG:
- Semantic boundary-aware chunking engine (Story 3.1)
- Entity-aware chunking (Story 3.2)
- Chunk metadata and quality scoring (Story 3.3)

Type Contract: Document (normalized) → List[Chunk] (with metadata)
"""

from .engine import ChunkingConfig, ChunkingEngine
from .metadata_enricher import MetadataEnricher
from .models import ChunkMetadata, QualityScore
from .sentence_segmenter import SentenceSegmenter

__all__ = [
    "ChunkingEngine",
    "ChunkingConfig",
    "SentenceSegmenter",
    "ChunkMetadata",
    "QualityScore",
    "MetadataEnricher",
]
