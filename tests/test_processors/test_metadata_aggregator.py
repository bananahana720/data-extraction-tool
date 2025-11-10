"""
Tests for MetadataAggregator processor.

MetadataAggregator computes statistics and extracts entities:
- Word counts and character counts
- Content type distributions
- Entity extraction (optional with spaCy)
- Summary generation
- Computed statistics in document metadata
"""

import pytest
from pathlib import Path

from src.core import (
    ContentBlock,
    ContentType,
    ExtractionResult,
    DocumentMetadata,
    ProcessingStage,
)
from processors.metadata_aggregator import MetadataAggregator


class TestMetadataAggregatorBasics:
    """Test basic MetadataAggregator functionality."""

    def test_processor_name(self):
        """RED: Processor should return correct name."""
        processor = MetadataAggregator()
        assert processor.get_processor_name() == "MetadataAggregator"

    def test_is_optional_processor(self):
        """RED: MetadataAggregator is optional (non-critical)."""
        processor = MetadataAggregator()
        assert processor.is_optional() is True

    def test_no_dependencies(self):
        """RED: MetadataAggregator can run independently."""
        processor = MetadataAggregator()
        # Could depend on ContextLinker but not required
        assert isinstance(processor.get_dependencies(), list)


class TestMetadataAggregatorEmptyInput:
    """Test MetadataAggregator with empty input."""

    def test_empty_extraction_result(self):
        """RED: Should handle empty extraction result gracefully."""
        processor = MetadataAggregator()

        extraction_result = ExtractionResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 0
        assert result.processing_stage == ProcessingStage.METADATA_AGGREGATION
        assert "total_words" in result.stage_metadata
        assert result.stage_metadata["total_words"] == 0


class TestMetadataAggregatorWordCounts:
    """Test word and character counting."""

    def test_single_paragraph_word_count(self):
        """RED: Should count words in content blocks."""
        processor = MetadataAggregator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="This is a test paragraph with seven words."
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        processed_block = result.content_blocks[0]
        assert processed_block.metadata.get("word_count") == 8
        assert processed_block.metadata.get("char_count") > 0

    def test_multiple_blocks_total_words(self):
        """RED: Should aggregate word counts across blocks."""
        processor = MetadataAggregator()

        block1 = ContentBlock(block_type=ContentType.PARAGRAPH, content="First paragraph.")

        block2 = ContentBlock(block_type=ContentType.PARAGRAPH, content="Second paragraph here.")

        extraction_result = ExtractionResult(
            content_blocks=(block1, block2),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "total_words" in result.stage_metadata
        assert result.stage_metadata["total_words"] == 5  # 2 + 3
        assert "total_characters" in result.stage_metadata

    def test_empty_content_blocks(self):
        """RED: Should handle empty content gracefully."""
        processor = MetadataAggregator()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="")

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        processed_block = result.content_blocks[0]
        assert processed_block.metadata.get("word_count") == 0
        assert processed_block.metadata.get("char_count") == 0


class TestMetadataAggregatorContentTypeDistribution:
    """Test content type distribution statistics."""

    def test_content_type_counts(self):
        """RED: Should count blocks by type."""
        processor = MetadataAggregator()

        blocks = (
            ContentBlock(block_type=ContentType.HEADING, content="Title"),
            ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 1"),
            ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 2"),
            ContentBlock(block_type=ContentType.TABLE, content="[table]"),
        )

        extraction_result = ExtractionResult(
            content_blocks=blocks,
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "content_type_distribution" in result.stage_metadata
        distribution = result.stage_metadata["content_type_distribution"]
        assert distribution.get("paragraph") == 2
        assert distribution.get("heading") == 1
        assert distribution.get("table") == 1

    def test_unique_content_types_count(self):
        """RED: Should count number of unique content types."""
        processor = MetadataAggregator()

        blocks = (
            ContentBlock(block_type=ContentType.HEADING, content="Title"),
            ContentBlock(block_type=ContentType.PARAGRAPH, content="Para"),
        )

        extraction_result = ExtractionResult(
            content_blocks=blocks,
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "unique_content_types" in result.stage_metadata
        assert result.stage_metadata["unique_content_types"] == 2


class TestMetadataAggregatorStatistics:
    """Test statistical computations."""

    def test_average_words_per_block(self):
        """RED: Should compute average word count."""
        processor = MetadataAggregator()

        blocks = (
            ContentBlock(block_type=ContentType.PARAGRAPH, content="One two three"),  # 3
            ContentBlock(block_type=ContentType.PARAGRAPH, content="Four five"),  # 2
        )

        extraction_result = ExtractionResult(
            content_blocks=blocks,
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "average_words_per_block" in result.stage_metadata
        assert result.stage_metadata["average_words_per_block"] == 2.5

    def test_longest_and_shortest_blocks(self):
        """RED: Should track longest and shortest content blocks."""
        processor = MetadataAggregator()

        blocks = (
            ContentBlock(block_type=ContentType.PARAGRAPH, content="Short."),
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content="This is a much longer paragraph with many more words.",
            ),
        )

        extraction_result = ExtractionResult(
            content_blocks=blocks,
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "min_words_per_block" in result.stage_metadata
        assert "max_words_per_block" in result.stage_metadata
        assert result.stage_metadata["min_words_per_block"] == 1
        assert result.stage_metadata["max_words_per_block"] == 10


class TestMetadataAggregatorEntityExtraction:
    """Test entity extraction (optional feature with spaCy)."""

    def test_without_spacy_no_entities(self):
        """RED: Without spaCy, should not extract entities."""
        processor = MetadataAggregator(config={"enable_entities": False})

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="John Smith works at Microsoft in Seattle."
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        # Should not have entities if disabled
        processed_block = result.content_blocks[0]
        assert (
            "entities" not in processed_block.metadata
            or processed_block.metadata.get("entities") == []
        )


class TestMetadataAggregatorSummaryGeneration:
    """Test content summary generation."""

    def test_summary_in_stage_metadata(self):
        """RED: Should generate document summary."""
        processor = MetadataAggregator()

        blocks = (
            ContentBlock(block_type=ContentType.HEADING, content="Introduction"),
            ContentBlock(block_type=ContentType.PARAGRAPH, content="This is the intro."),
            ContentBlock(block_type=ContentType.HEADING, content="Conclusion"),
            ContentBlock(block_type=ContentType.PARAGRAPH, content="This is the conclusion."),
        )

        extraction_result = ExtractionResult(
            content_blocks=blocks,
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "summary" in result.stage_metadata
        summary = result.stage_metadata["summary"]
        assert "headings" in summary
        assert len(summary["headings"]) == 2


class TestMetadataAggregatorErrorHandling:
    """Test error handling and edge cases."""

    def test_preserves_original_metadata(self):
        """RED: Should not overwrite existing metadata fields."""
        processor = MetadataAggregator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Test", metadata={"custom_field": "value"}
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        processed_block = result.content_blocks[0]
        # Original metadata preserved
        assert processed_block.metadata.get("custom_field") == "value"
        # New metadata added
        assert "word_count" in processed_block.metadata

    def test_preserves_block_ids(self):
        """RED: Should preserve original block IDs."""
        processor = MetadataAggregator()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Test")
        original_id = block.block_id

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        processed_block = result.content_blocks[0]
        assert processed_block.block_id == original_id


class TestMetadataAggregatorConfiguration:
    """Test configuration options."""

    def test_with_custom_config(self):
        """RED: Should accept configuration dict."""
        config = {"enable_entities": True, "summary_max_headings": 10}
        processor = MetadataAggregator(config=config)
        assert processor.config == config

    def test_with_no_config(self):
        """RED: Should work with no configuration."""
        processor = MetadataAggregator()
        assert processor.config == {}
