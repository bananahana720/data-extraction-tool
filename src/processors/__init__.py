"""
Content processors for enriching extracted data.

Processors add value to raw extracted content:
- ContextLinker: Build hierarchical document structure
- MetadataAggregator: Compute statistics and extract entities
- QualityValidator: Score extraction quality
"""

from .context_linker import ContextLinker
from .metadata_aggregator import MetadataAggregator
from .quality_validator import QualityValidator

__all__ = [
    "ContextLinker",
    "MetadataAggregator",
    "QualityValidator",
]
