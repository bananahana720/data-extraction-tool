"""Chunk data models (re-exported from core for compatibility).

Story 3.1 uses Chunk model from core/models.py. This module provides
compatibility exports for tests and external code.

Story 3.2 implements ChunkMetadata for entity-aware chunking.
Story 3.3 will add QualityScore for quality scoring.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Re-export Chunk from core for compatibility
from ..core.models import Chunk, Metadata
from .entity_preserver import EntityReference


@dataclass(frozen=True)
class ChunkMetadata:
    """Chunk-level metadata for entity-aware chunking (Story 3.2).

    Extends document-level Metadata with chunk-specific fields for
    entity tracking, section context, and relationship preservation.
    Immutability enforced per ADR-001 to prevent pipeline state corruption.

    This model satisfies AC-3.2-6: "Entity tags in chunk metadata with
    EntityReference objects" by providing entity_tags as List[EntityReference].

    Attributes:
        entity_tags: List of EntityReference objects for entities in chunk
        section_context: Section breadcrumb showing chunk location (e.g., "Risk Assessment > Controls")
        entity_relationships: Relationship triples within chunk (entity1_id, relation_type, entity2_id)
        source_metadata: Original document metadata for provenance tracking

    Example:
        >>> chunk_meta = ChunkMetadata(
        ...     entity_tags=[
        ...         EntityReference(
        ...             entity_type="RISK",
        ...             entity_id="RISK-001",
        ...             start_pos=100,
        ...             end_pos=120,
        ...             is_partial=False,
        ...             context_snippet="...Data breach risk..."
        ...         )
        ...     ],
        ...     section_context="Risk Assessment > Identified Risks",
        ...     entity_relationships=[("RISK-001", "mitigated_by", "CTRL-042")],
        ...     source_metadata=document.metadata
        ... )
        >>> chunk_meta.to_dict()
        {'entity_tags': [...], 'section_context': '...', ...}
    """

    # Chunk-specific fields (Story 3.2)
    entity_tags: List[EntityReference] = field(default_factory=list)
    section_context: str = ""
    entity_relationships: List[Tuple[str, str, str]] = field(default_factory=list)

    # Document provenance (Epic 2 Metadata)
    source_metadata: Optional[Metadata] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary.

        Returns:
            Dict with all ChunkMetadata fields JSON-serializable
        """
        return {
            "entity_tags": [ref.to_dict() for ref in self.entity_tags],
            "section_context": self.section_context,
            "entity_relationships": [list(rel) for rel in self.entity_relationships],
            "source_metadata": (
                self.source_metadata.model_dump(mode="python") if self.source_metadata else None
            ),
        }


# Placeholder export for Story 3.3
QualityScore = None  # Will be implemented in Story 3.3

__all__ = ["Chunk", "ChunkMetadata", "QualityScore"]
