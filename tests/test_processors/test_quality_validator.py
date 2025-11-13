"""
Tests for QualityValidator processor.

QualityValidator scores extraction quality by checking:
- Completeness: Are expected content types present?
- Consistency: Are blocks properly structured?
- Readability: Is text readable and not corrupted?
- Confidence: Do blocks have high extraction confidence?
- Issues: What quality problems exist?
"""

from pathlib import Path

from processors.quality_validator import QualityValidator
from src.core import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    ProcessingStage,
)


class TestQualityValidatorBasics:
    """Test basic QualityValidator functionality."""

    def test_processor_name(self):
        """RED: Processor should return correct name."""
        processor = QualityValidator()
        assert processor.get_processor_name() == "QualityValidator"

    def test_is_optional_processor(self):
        """RED: QualityValidator is optional (informational)."""
        processor = QualityValidator()
        assert processor.is_optional() is True

    def test_depends_on_metadata_aggregator(self):
        """RED: QualityValidator benefits from MetadataAggregator."""
        processor = QualityValidator()
        deps = processor.get_dependencies()
        # May or may not depend on MetadataAggregator
        assert isinstance(deps, list)


class TestQualityValidatorEmptyInput:
    """Test QualityValidator with empty input."""

    def test_empty_extraction_result(self):
        """RED: Should handle empty extraction result."""
        processor = QualityValidator()

        extraction_result = ExtractionResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert result.processing_stage == ProcessingStage.QUALITY_VALIDATION
        assert result.quality_score is not None
        # Empty document should have low quality score
        assert result.quality_score < 50.0


class TestQualityValidatorCompletenessScoring:
    """Test completeness scoring."""

    def test_document_with_headings_scores_higher(self):
        """RED: Documents with headings should score higher."""
        processor = QualityValidator()

        # Document without headings
        result_no_headings = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 1"),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 2"),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Document with headings
        result_with_headings = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.HEADING, content="Title"),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 1"),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Para 2"),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Document with headings should score higher
        assert result_with_headings.quality_score > result_no_headings.quality_score

    def test_empty_blocks_reduce_score(self):
        """RED: Empty content blocks should reduce quality score."""
        processor = QualityValidator()

        # Document with empty blocks
        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content=""),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content=""),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Empty blocks should trigger quality issues
        assert "empty_blocks" in result.stage_metadata
        assert result.stage_metadata["empty_blocks"] > 0


class TestQualityValidatorConsistencyChecking:
    """Test consistency validation."""

    def test_missing_confidence_scores(self):
        """RED: Blocks without confidence should be flagged."""
        processor = QualityValidator()

        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(
                        block_type=ContentType.PARAGRAPH,
                        content="Test",
                        confidence=None,  # Missing confidence
                    ),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        assert "blocks_without_confidence" in result.stage_metadata

    def test_low_confidence_blocks(self):
        """RED: Blocks with low confidence should reduce score."""
        processor = QualityValidator()

        # High confidence document
        result_high = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Test", confidence=0.95),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Low confidence document
        result_low = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Test", confidence=0.30),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        assert result_high.quality_score > result_low.quality_score


class TestQualityValidatorReadabilityChecking:
    """Test readability validation."""

    def test_corrupted_text_detection(self):
        """RED: Should detect potentially corrupted text."""
        processor = QualityValidator()

        # Document with corrupted-looking text
        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(
                        block_type=ContentType.PARAGRAPH, content="###!!!***&&&|||"  # Gibberish
                    ),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Should detect readability issues
        assert "readability_issues" in result.stage_metadata or result.quality_score < 70.0

    def test_normal_text_scores_well(self):
        """RED: Normal readable text should score well."""
        processor = QualityValidator()

        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.HEADING, content="Introduction"),
                    ContentBlock(
                        block_type=ContentType.PARAGRAPH,
                        content="This is a well-formed paragraph with normal text.",
                    ),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Well-formed document should score high
        assert result.quality_score >= 70.0


class TestQualityValidatorScoreCalculation:
    """Test overall quality score calculation."""

    def test_score_in_valid_range(self):
        """RED: Quality score should be 0-100."""
        processor = QualityValidator()

        result = processor.process(
            ExtractionResult(
                content_blocks=(ContentBlock(block_type=ContentType.PARAGRAPH, content="Test"),),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        assert 0.0 <= result.quality_score <= 100.0

    def test_quality_issues_list(self):
        """RED: Should provide list of specific quality issues."""
        processor = QualityValidator()

        # Document with multiple issues
        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content=""),  # Empty
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="Test"),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Should have quality_issues tuple
        assert isinstance(result.quality_issues, tuple)


class TestQualityValidatorNeedsReview:
    """Test needs_review flag."""

    def test_low_score_triggers_review(self):
        """RED: Low quality score should set needs_review flag."""
        processor = QualityValidator()

        # Document likely to score low
        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.PARAGRAPH, content=""),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content=""),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Low score should trigger review
        if result.quality_score < 50.0:
            assert result.needs_review is True

    def test_high_score_no_review(self):
        """RED: High quality score should not require review."""
        processor = QualityValidator()

        # Well-formed document
        result = processor.process(
            ExtractionResult(
                content_blocks=(
                    ContentBlock(block_type=ContentType.HEADING, content="Title"),
                    ContentBlock(block_type=ContentType.PARAGRAPH, content="This is good content."),
                ),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # High score should not trigger review
        if result.quality_score >= 80.0:
            assert result.needs_review is False


class TestQualityValidatorStageMetadata:
    """Test stage metadata population."""

    def test_stage_metadata_completeness(self):
        """RED: Stage metadata should include validation details."""
        processor = QualityValidator()

        result = processor.process(
            ExtractionResult(
                content_blocks=(ContentBlock(block_type=ContentType.PARAGRAPH, content="Test"),),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        # Should have validation statistics
        assert "completeness_score" in result.stage_metadata
        assert "consistency_score" in result.stage_metadata
        assert "readability_score" in result.stage_metadata


class TestQualityValidatorErrorHandling:
    """Test error handling."""

    def test_preserves_original_metadata(self):
        """RED: Should not overwrite existing block metadata."""
        processor = QualityValidator()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Test", metadata={"custom": "value"}
        )

        result = processor.process(
            ExtractionResult(
                content_blocks=(block,),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        processed_block = result.content_blocks[0]
        assert processed_block.metadata.get("custom") == "value"

    def test_preserves_block_ids(self):
        """RED: Should preserve original block IDs."""
        processor = QualityValidator()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Test")
        original_id = block.block_id

        result = processor.process(
            ExtractionResult(
                content_blocks=(block,),
                document_metadata=DocumentMetadata(
                    source_file=Path("test.txt"), file_format="text"
                ),
                success=True,
            )
        )

        assert result.content_blocks[0].block_id == original_id


class TestQualityValidatorConfiguration:
    """Test configuration options."""

    def test_with_custom_thresholds(self):
        """RED: Should accept custom quality thresholds."""
        config = {"needs_review_threshold": 60.0, "empty_block_penalty": 10.0}
        processor = QualityValidator(config=config)
        assert processor.config == config

    def test_with_no_config(self):
        """RED: Should work with default configuration."""
        processor = QualityValidator()
        assert processor.config == {}
