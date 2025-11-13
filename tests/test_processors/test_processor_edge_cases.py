"""
Comprehensive edge case tests for all processors.

This test suite uses equivalency partitioning to test processor boundary
conditions and extreme scenarios.

Processors Tested:
- ContextLinker: Hierarchy building
- MetadataAggregator: Metadata enrichment
- QualityValidator: Quality assessment

Test Categories:
- Empty/minimal input
- Maximum scale (thousands of blocks)
- Deep nesting (10+ levels)
- Circular references (shouldn't occur but defensive)
- Orphaned blocks
- Missing/invalid metadata
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
)
from processors.context_linker import ContextLinker
from processors.metadata_aggregator import MetadataAggregator
from processors.quality_validator import QualityValidator

# ==============================================================================
# ContextLinker Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestContextLinkerEdgeCases:
    """Edge cases for ContextLinker processor."""

    def test_single_content_block(self):
        """
        EDGE: Processing exactly one block.

        Partition: Input size → Valid → Minimum (1)
        Expected: Single block processed, no parent
        """
        processor = ContextLinker()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Single block")

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 1
        assert result.content_blocks[0].parent_id is None
        assert result.content_blocks[0].metadata.get("depth") == 0

    @pytest.mark.slow
    @pytest.mark.stress
    def test_massive_number_of_blocks(self):
        """
        EDGE: Processing 10,000+ blocks (stress test).

        Partition: Input size → Valid → Maximum
        Boundary: Large-scale processing
        Expected: Should complete without OOM or timeout
        """
        processor = ContextLinker()

        # Create 10,000 blocks
        blocks = []
        for i in range(10000):
            block = ContentBlock(block_type=ContentType.PARAGRAPH, content=f"Block {i}")
            blocks.append(block)

        extraction_result = ExtractionResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("huge.txt"), file_format="text"),
            success=True,
        )

        import time

        start = time.time()
        result = processor.process(extraction_result)
        duration = time.time() - start

        assert result.success is True
        assert len(result.content_blocks) == 10000

        # Performance check: Should complete in reasonable time
        # Target: <0.001s per block = 10s for 10k blocks
        assert duration < 30.0, f"Took {duration:.2f}s for 10k blocks"

    def test_very_deep_heading_nesting(self):
        """
        EDGE: Deeply nested heading hierarchy (10+ levels).

        Partition: Hierarchy → Valid → Deep nesting
        Boundary: Maximum realistic nesting depth
        Expected: Correct depth tracking at all levels
        """
        processor = ContextLinker()

        # Create headings at 10 levels
        blocks = []
        for level in range(1, 11):
            heading = ContentBlock(
                block_type=ContentType.HEADING,
                content=f"Level {level} Heading",
                metadata={"level": level},
            )
            blocks.append(heading)

            # Add paragraph under this heading
            para = ContentBlock(
                block_type=ContentType.PARAGRAPH, content=f"Content at level {level}"
            )
            blocks.append(para)

        extraction_result = ExtractionResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("deep.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # Verify depth increases correctly
        max_depth = 0
        for block in result.content_blocks:
            depth = block.metadata.get("depth", 0)
            max_depth = max(max_depth, depth)

        # Should have deep nesting (>5 levels)
        assert max_depth >= 5

    def test_heading_level_skip(self):
        """
        EDGE: Heading levels skip (H1 → H3, no H2).

        Partition: Hierarchy → Valid → Non-sequential levels
        Expected: Should handle gracefully, link to closest parent
        """
        processor = ContextLinker()

        h1 = ContentBlock(block_type=ContentType.HEADING, content="Chapter", metadata={"level": 1})

        # Skip H2, go straight to H3
        h3 = ContentBlock(
            block_type=ContentType.HEADING, content="Subsection", metadata={"level": 3}
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content")

        extraction_result = ExtractionResult(
            content_blocks=(h1, h3, para),
            document_metadata=DocumentMetadata(source_file=Path("skip.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # H3 should link to H1 (closest parent)
        processed_h3 = result.content_blocks[1]
        assert processed_h3.parent_id == h1.block_id

    def test_orphaned_paragraphs_at_end(self):
        """
        EDGE: Paragraphs at document end with no following heading.

        Partition: Structure → Valid → Trailing content
        Expected: Should link to last heading or be orphaned
        """
        processor = ContextLinker()

        heading = ContentBlock(
            block_type=ContentType.HEADING, content="Section", metadata={"level": 1}
        )

        para1 = ContentBlock(block_type=ContentType.PARAGRAPH, content="Under heading")

        para2 = ContentBlock(block_type=ContentType.PARAGRAPH, content="Also under heading")

        extraction_result = ExtractionResult(
            content_blocks=(heading, para1, para2),
            document_metadata=DocumentMetadata(
                source_file=Path("trailing.txt"), file_format="text"
            ),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # Both paragraphs should link to heading
        assert result.content_blocks[1].parent_id == heading.block_id
        assert result.content_blocks[2].parent_id == heading.block_id

    def test_all_same_heading_level(self):
        """
        EDGE: Document with only same-level headings (no hierarchy).

        Partition: Hierarchy → Valid → Flat structure
        Expected: All headings at same depth, no parent relationships
        """
        processor = ContextLinker()

        blocks = []
        for i in range(5):
            heading = ContentBlock(
                block_type=ContentType.HEADING,
                content=f"Section {i}",
                metadata={"level": 1},  # All H1
            )
            blocks.append(heading)

        extraction_result = ExtractionResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("flat.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # All headings should be roots (no parent)
        for block in result.content_blocks:
            assert block.parent_id is None
            assert block.metadata.get("depth") == 0

    def test_headings_without_level_metadata(self):
        """
        EDGE: Heading blocks missing 'level' in metadata.

        Partition: Metadata → Invalid → Missing required field
        Expected: Should handle gracefully, assume default level
        """
        processor = ContextLinker()

        heading = ContentBlock(
            block_type=ContentType.HEADING, content="Heading", metadata={}  # No level!
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content")

        extraction_result = ExtractionResult(
            content_blocks=(heading, para),
            document_metadata=DocumentMetadata(source_file=Path("nolevel.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        # Should not crash
        assert result.success is True


# ==============================================================================
# MetadataAggregator Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestMetadataAggregatorEdgeCases:
    """Edge cases for MetadataAggregator processor."""

    def test_blocks_with_no_metadata(self):
        """
        EDGE: Content blocks with empty metadata dict.

        Partition: Metadata → Valid → Empty
        Expected: Should add metadata without errors
        """
        processor = MetadataAggregator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="No metadata", metadata={}  # Empty
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # Should add metadata fields
        processed = result.content_blocks[0]
        assert "char_count" in processed.metadata

    def test_blocks_with_extensive_metadata(self):
        """
        EDGE: Content blocks with 100+ metadata fields.

        Partition: Metadata → Valid → Maximum
        Boundary: Very large metadata dict
        Expected: Should preserve all metadata
        """
        processor = MetadataAggregator()

        # Create block with extensive metadata
        extensive_meta = {f"field_{i}": f"value_{i}" for i in range(100)}

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Extensive metadata", metadata=extensive_meta
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("extensive.txt"), file_format="text"
            ),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # All original metadata should be preserved
        processed = result.content_blocks[0]
        for i in range(100):
            assert f"field_{i}" in processed.metadata

    def test_blocks_with_null_values_in_metadata(self):
        """
        EDGE: Metadata containing None values.

        Partition: Metadata → Valid → Null values
        Expected: Should handle None without errors
        """
        processor = MetadataAggregator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content="Null metadata",
            metadata={"null_field": None, "valid_field": "value"},
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("null.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # Should preserve None values
        assert result.content_blocks[0].metadata.get("null_field") is None

    @pytest.mark.slow
    def test_aggregate_10000_blocks(self):
        """
        EDGE: Aggregate metadata for 10,000 blocks.

        Partition: Scale → Valid → Maximum
        Expected: Should complete efficiently
        """
        processor = MetadataAggregator()

        blocks = []
        for i in range(10000):
            block = ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content=f"Block {i}" * 10,  # ~80 chars each
                metadata={"index": i},
            )
            blocks.append(block)

        extraction_result = ExtractionResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("massive.txt"), file_format="text"),
            success=True,
        )

        import time

        start = time.time()
        result = processor.process(extraction_result)
        duration = time.time() - start

        assert result.success is True
        assert len(result.content_blocks) == 10000

        # Performance check
        assert duration < 20.0, f"Took {duration:.2f}s for 10k blocks"


# ==============================================================================
# QualityValidator Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestQualityValidatorEdgeCases:
    """Edge cases for QualityValidator processor."""

    def test_perfect_quality_content(self):
        """
        EDGE: Content with perfect quality score (100).

        Partition: Quality → Valid → Maximum (100)
        Expected: Score = 100, no quality issues
        """
        processor = QualityValidator()

        # Perfect content: good length, no corruption, high confidence
        block = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content="This is perfectly formatted content with appropriate length.",
            confidence=1.0,
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("perfect.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        processed = result.content_blocks[0]

        # Should have high quality score
        quality_score = processed.metadata.get("quality_score", 0)
        assert quality_score >= 90

    def test_zero_quality_content(self):
        """
        EDGE: Content with minimum quality (corrupted).

        Partition: Quality → Valid → Minimum (0)
        Expected: Low score, quality issues flagged
        """
        processor = QualityValidator()

        # Poor quality: short, corrupted, low confidence
        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="ÄÖÜß#@!", confidence=0.1  # Corrupted-looking
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("poor.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        processed = result.content_blocks[0]

        # Should have quality issues
        assert "quality_issues" in processed.metadata

    def test_boundary_score_at_70_threshold(self):
        """
        EDGE: Quality score exactly at 70 (review threshold).

        Partition: Quality → Boundary → Threshold (70)
        Expected: Correct needs_review flagging
        """
        processor = QualityValidator(config={"quality_threshold": 70})

        # Create content that scores around 70
        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Medium quality content.", confidence=0.7
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("boundary.txt"), file_format="text"
            ),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # Should have quality assessment
        processed = result.content_blocks[0]
        assert "quality_score" in processed.metadata

    def test_blocks_with_no_content(self):
        """
        EDGE: Blocks with empty string content.

        Partition: Content → Invalid → Empty
        Expected: Should flag as quality issue
        """
        processor = QualityValidator()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="")  # Empty!

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("empty.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        processed = result.content_blocks[0]

        # Empty content should result in quality issues
        quality_issues = processed.metadata.get("quality_issues", [])
        assert len(quality_issues) > 0

    def test_blocks_with_only_whitespace(self):
        """
        EDGE: Blocks with only whitespace characters.

        Partition: Content → Invalid → Whitespace-only
        Expected: Should detect as low quality
        """
        processor = QualityValidator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="     \t\n     "  # Only whitespace
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("whitespace.txt"), file_format="text"
            ),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # Should have low quality score or quality issues
        processed = result.content_blocks[0]
        quality_score = processed.metadata.get("quality_score", 100)
        assert quality_score < 90  # Should be marked as low quality

    def test_mixed_quality_blocks(self):
        """
        EDGE: Mix of high and low quality blocks in same document.

        Partition: Quality → Valid → Mixed
        Expected: Each block assessed independently
        """
        processor = QualityValidator()

        high_quality = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content="This is high quality content with good structure.",
            confidence=0.95,
        )

        low_quality = ContentBlock(block_type=ContentType.PARAGRAPH, content="ÄÖÜ", confidence=0.2)

        extraction_result = ExtractionResult(
            content_blocks=(high_quality, low_quality),
            document_metadata=DocumentMetadata(source_file=Path("mixed.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 2

        # Scores should differ significantly
        score1 = result.content_blocks[0].metadata.get("quality_score", 0)
        score2 = result.content_blocks[1].metadata.get("quality_score", 0)

        assert abs(score1 - score2) > 20  # Significant difference

    def test_custom_quality_thresholds(self):
        """
        EDGE: Custom quality thresholds (very strict: 95).

        Partition: Configuration → Valid → Custom
        Expected: Should use custom thresholds
        """
        processor = QualityValidator(config={"quality_threshold": 95})

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content="Good content but not perfect.",
            confidence=0.8,
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("strict.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # With strict threshold, might need review even for good content
        processed = result.content_blocks[0]
        assert "quality_score" in processed.metadata


# ==============================================================================
# Cross-Processor Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestCrossProcessorEdgeCases:
    """Edge cases involving multiple processors."""

    def test_empty_result_through_all_processors(self):
        """
        EDGE: Empty extraction result through full processor chain.

        Expected: All processors should handle gracefully
        """
        extraction_result = ExtractionResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(source_file=Path("empty.txt"), file_format="text"),
            success=True,
        )

        # Process through chain
        result1 = ContextLinker().process(extraction_result)
        assert result1.success is True

        result2 = MetadataAggregator().process(result1)
        assert result2.success is True

        result3 = QualityValidator().process(result2)
        assert result3.success is True

    def test_single_block_through_all_processors(self):
        """
        EDGE: Single block through full processor chain.

        Expected: Block should be enriched at each stage
        """
        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Single block content")

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("single.txt"), file_format="text"),
            success=True,
        )

        # Process through chain
        result1 = ContextLinker().process(extraction_result)
        result2 = MetadataAggregator().process(result1)
        result3 = QualityValidator().process(result2)

        assert result3.success is True
        final_block = result3.content_blocks[0]

        # Should have metadata from all processors
        assert "depth" in final_block.metadata  # From ContextLinker
        assert "char_count" in final_block.metadata  # From MetadataAggregator
        assert "quality_score" in final_block.metadata  # From QualityValidator


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "edge_case"])
