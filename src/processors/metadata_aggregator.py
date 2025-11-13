"""
MetadataAggregator Processor - Compute Statistics and Extract Entities

This processor computes document-wide and block-level statistics:
- Word counts and character counts
- Content type distributions
- Statistical analysis (min, max, average)
- Entity extraction (optional with spaCy)
- Content summaries

Example Metadata Enrichment:
    Block metadata: {"word_count": 42, "char_count": 256, "entities": ["Microsoft", "Seattle"]}
    Stage metadata: {"total_words": 1234, "average_words_per_block": 42.3, ...}

Design:
- Optional: Can be skipped if it fails
- Efficient: Single pass computation
- Extensible: Easy to add new statistics
- Safe: Handles missing data gracefully
"""

from collections import defaultdict

from core import (
    BaseProcessor,
    ContentBlock,
    ContentType,
    ExtractionResult,
    ProcessingResult,
    ProcessingStage,
)


class MetadataAggregator(BaseProcessor):
    """
    Compute statistics and extract entities from content.

    This processor enriches content blocks with:
    - word_count: Number of words in block
    - char_count: Number of characters in block
    - entities: List of extracted entities (optional)

    And adds to stage_metadata:
    - total_words: Sum of all words
    - total_characters: Sum of all characters
    - average_words_per_block: Mean word count
    - min_words_per_block: Minimum word count
    - max_words_per_block: Maximum word count
    - content_type_distribution: Count by content type
    - unique_content_types: Number of unique types
    - summary: High-level document summary

    Configuration:
    - enable_entities (bool): Enable entity extraction (default: False)
    - summary_max_headings (int): Max headings in summary (default: 5)
    """

    def get_processor_name(self) -> str:
        """Return processor name."""
        return "MetadataAggregator"

    def is_optional(self) -> bool:
        """MetadataAggregator is optional - enrichment, not critical."""
        return True

    def get_dependencies(self) -> list[str]:
        """Can run independently or after ContextLinker."""
        return []  # No strict dependencies

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """
        Process extracted content to compute statistics.

        Args:
            extraction_result: Raw extraction result

        Returns:
            ProcessingResult with enriched metadata

        Processing Steps:
        1. Handle empty input
        2. Compute block-level statistics (word counts, char counts)
        3. Extract entities if configured
        4. Aggregate document-level statistics
        5. Generate summary
        """
        # Handle empty input
        if not extraction_result.content_blocks:
            return ProcessingResult(
                content_blocks=tuple(),
                document_metadata=extraction_result.document_metadata,
                images=extraction_result.images,
                tables=extraction_result.tables,
                processing_stage=ProcessingStage.METADATA_AGGREGATION,
                stage_metadata={
                    "total_words": 0,
                    "total_characters": 0,
                    "average_words_per_block": 0.0,
                    "content_type_distribution": {},
                    "unique_content_types": 0,
                },
                success=True,
            )

        # Process blocks
        enriched_blocks = []
        total_words = 0
        total_characters = 0
        word_counts = []
        content_type_counts = defaultdict(int)
        headings = []

        for block in extraction_result.content_blocks:
            # Count words and characters
            word_count = self._count_words(block.content)
            char_count = len(block.content)

            word_counts.append(word_count)
            total_words += word_count
            total_characters += char_count

            # Track content types
            content_type_counts[block.block_type.value] += 1

            # Collect headings for summary
            if block.block_type == ContentType.HEADING:
                headings.append(block.content)

            # Extract entities if enabled
            entities = []
            if self.config.get("enable_entities", False):
                entities = self._extract_entities(block.content)

            # Create enriched metadata
            enriched_metadata = {
                **block.metadata,
                "word_count": word_count,
                "char_count": char_count,
            }

            if entities:
                enriched_metadata["entities"] = entities

            # Create enriched block
            enriched_block = ContentBlock(
                block_id=block.block_id,  # Preserve original ID
                block_type=block.block_type,
                content=block.content,
                raw_content=block.raw_content,
                position=block.position,
                parent_id=block.parent_id,
                related_ids=block.related_ids,
                metadata=enriched_metadata,
                confidence=block.confidence,
                style=block.style,
            )

            enriched_blocks.append(enriched_block)

        # Compute aggregate statistics
        num_blocks = len(enriched_blocks)
        average_words = total_words / num_blocks if num_blocks > 0 else 0.0
        min_words = min(word_counts) if word_counts else 0
        max_words = max(word_counts) if word_counts else 0

        # Generate summary
        summary_max_headings = self.config.get("summary_max_headings", 5)
        summary = {
            "headings": headings[:summary_max_headings],
        }

        # Create result
        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            document_metadata=extraction_result.document_metadata,
            images=extraction_result.images,
            tables=extraction_result.tables,
            processing_stage=ProcessingStage.METADATA_AGGREGATION,
            stage_metadata={
                "total_words": total_words,
                "total_characters": total_characters,
                "average_words_per_block": average_words,
                "min_words_per_block": min_words,
                "max_words_per_block": max_words,
                "content_type_distribution": dict(content_type_counts),
                "unique_content_types": len(content_type_counts),
                "summary": summary,
            },
            success=True,
        )

    def _count_words(self, text: str) -> int:
        """
        Count words in text.

        Simple whitespace-based word counting.

        Args:
            text: Text to count words in

        Returns:
            Number of words
        """
        if not text or not text.strip():
            return 0

        return len(text.split())

    def _extract_entities(self, text: str) -> list[str]:
        """
        Extract named entities from text.

        This is a placeholder for entity extraction. In production,
        this would use spaCy or another NLP library.

        Args:
            text: Text to extract entities from

        Returns:
            List of entity strings (empty for now)

        Note:
            Actual implementation would use:
            ```python
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)
            return [ent.text for ent in doc.ents]
            ```
        """
        # Placeholder - entity extraction disabled by default
        # Would require spaCy which may not be available in enterprise env
        return []
