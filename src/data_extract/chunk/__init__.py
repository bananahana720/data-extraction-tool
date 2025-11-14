"""Semantic chunking pipeline stage.

This module contains chunking strategies for RAG:
- Semantic boundary-aware chunking engine (Story 3.1)
- Entity-aware chunking (Story 3.2 - planned)
- Chunk metadata and quality scoring (Story 3.3 - planned)

Type Contract: Document (normalized) → List[Chunk] (with metadata)
"""

from .engine import ChunkingEngine
from .sentence_segmenter import SentenceSegmenter

__all__ = ["ChunkingEngine", "SentenceSegmenter"]
