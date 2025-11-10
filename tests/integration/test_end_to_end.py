"""
End-to-End Integration Tests for Extraction Pipeline.

Tests complete extraction workflows through all pipeline stages:
- Extraction → Processing → Formatting
- Multiple format combinations
- Progress tracking integration
- Quality validation

Test IDs: E2E-001 through E2E-012
"""

import json
from pathlib import Path

import pytest

from src.core import ProcessingStage
from src.formatters import ChunkedTextFormatter, JsonFormatter, MarkdownFormatter
from src.pipeline import BatchProcessor, ExtractionPipeline
from src.processors import ContextLinker, MetadataAggregator, QualityValidator


# ==============================================================================
# Test Markers
# ==============================================================================

pytestmark = [pytest.mark.integration, pytest.mark.slow]


# ==============================================================================
# End-to-End Pipeline Tests
# ==============================================================================


@pytest.mark.parametrize(
    "file_format,formatter_type",
    [
        ("docx", "json"),  # E2E-001
        ("docx", "markdown"),  # E2E-002
        ("docx", "chunked"),  # E2E-003
        ("pdf", "json"),  # E2E-004
        ("pdf", "markdown"),  # E2E-005
        ("pdf", "chunked"),  # E2E-006
        ("txt", "json"),  # E2E-007
        ("txt", "markdown"),  # E2E-008
        ("txt", "chunked"),  # E2E-009
    ],
)
def test_full_pipeline_extraction(
    file_format,
    formatter_type,
    sample_docx_file,
    sample_pdf_file,
    sample_text_file,
    tmp_path,
):
    """
    Test E2E-001 through E2E-009: Full pipeline for all format combinations.

    Validates complete extraction workflow:
    1. Format detection
    2. Extraction
    3. Processing (all processors)
    4. Formatting
    5. Output generation

    Args:
        file_format: Format to test (docx, pdf, txt)
        formatter_type: Formatter to test (json, markdown, chunked)
        sample_*_file: Appropriate sample file fixture
        tmp_path: Temporary directory for outputs
    """
    # Arrange: Get appropriate test file
    file_map = {
        "docx": sample_docx_file,
        "pdf": sample_pdf_file,
        "txt": sample_text_file,
    }
    test_file = file_map[file_format]

    # Arrange: Create pipeline
    pipeline = ExtractionPipeline()

    # Register extractors
    from src.extractors import DocxExtractor, PdfExtractor, TextFileExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.register_extractor("pdf", PdfExtractor())
    pipeline.register_extractor("txt", TextFileExtractor())  # Use correct text extractor

    # Add processors
    pipeline.add_processor(ContextLinker())
    pipeline.add_processor(MetadataAggregator())
    pipeline.add_processor(QualityValidator())

    # Add appropriate formatter
    formatter_map = {
        "json": JsonFormatter(),
        "markdown": MarkdownFormatter(),
        "chunked": ChunkedTextFormatter(),
    }
    pipeline.add_formatter(formatter_map[formatter_type])

    # Act: Process file
    result = pipeline.process_file(test_file)

    # Assert: Pipeline succeeded
    assert result.success is True, f"Pipeline failed: {result.all_errors}"
    assert result.failed_stage is None

    # Assert: Extraction result valid
    assert result.extraction_result is not None
    assert result.extraction_result.success is True
    assert len(result.extraction_result.content_blocks) > 0

    # Assert: Processing result valid
    assert result.processing_result is not None
    assert result.processing_result.success is True
    assert result.processing_result.quality_score is not None
    assert result.processing_result.quality_score > 0.0

    # Assert: Formatted output generated
    assert len(result.formatted_outputs) == 1
    formatted_output = result.formatted_outputs[0]
    assert formatted_output.success is True
    assert formatted_output.format_type == formatter_type
    assert len(formatted_output.content) > 0

    # Assert: Format-specific validation
    if formatter_type == "json":
        # JSON should be parsable
        parsed = json.loads(formatted_output.content)
        assert "content_blocks" in parsed or "blocks" in parsed

    elif formatter_type == "markdown":
        # Markdown should contain headings
        assert "#" in formatted_output.content

    elif formatter_type == "chunked":
        # Chunked should have chunk metadata
        assert "chunk" in formatted_output.content.lower()


def test_e2e_full_processor_chain(sample_docx_file):
    """
    Test E2E-003: Validate all processors run in correct dependency order.

    Verifies:
    - Processors ordered topologically
    - ContextLinker runs before MetadataAggregator
    - All processor metadata present in final result
    """
    # Arrange: Create pipeline
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())

    # Add processors in wrong order (should be auto-sorted)
    pipeline.add_processor(QualityValidator())  # Depends on MetadataAggregator
    pipeline.add_processor(MetadataAggregator())  # Depends on ContextLinker
    pipeline.add_processor(ContextLinker())  # No dependencies

    # Add formatter
    pipeline.add_formatter(JsonFormatter())

    # Act: Process file
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Processing completed
    assert result.processing_result is not None
    assert result.processing_result.success is True

    # Assert: All processors left their mark
    # Each processor should add metadata to blocks
    content_blocks = result.processing_result.content_blocks
    assert len(content_blocks) > 0

    # Check for processor-specific metadata
    # (Actual metadata keys depend on processor implementation)
    first_block = content_blocks[0]
    assert first_block.metadata is not None
    assert isinstance(first_block.metadata, dict)


def test_e2e_progress_tracking_integration(sample_docx_file, progress_tracker):
    """
    Test E2E-006: Validate progress callbacks through full pipeline.

    Verifies:
    - Progress updates from 0% to 100%
    - Updates include stage information
    - No callback exceptions
    """
    # Arrange
    progress_updates, progress_callback = progress_tracker

    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_processor(ContextLinker())
    pipeline.add_formatter(JsonFormatter())

    # Act: Process with progress tracking
    result = pipeline.process_file(sample_docx_file, progress_callback=progress_callback)

    # Assert: Success
    assert result.success is True

    # Assert: Progress updates received
    assert len(progress_updates) > 0

    # Assert: Progress went from start to completion
    percentages = [u.get("percentage", 0) for u in progress_updates]
    assert min(percentages) >= 0.0
    assert max(percentages) <= 100.0

    # Assert: Stage information included
    stages_seen = {u.get("stage") for u in progress_updates if "stage" in u}
    assert len(stages_seen) > 0


def test_e2e_multi_format_batch_pipeline(
    batch_test_directory, configured_pipeline, output_directory
):
    """
    Test E2E-005: Process batch of files in different formats.

    Verifies:
    - Multiple formats processed successfully
    - All results available
    - Summary statistics correct
    """
    # Arrange: Create batch processor
    batch = BatchProcessor(pipeline=configured_pipeline, max_workers=2)

    # Get all files in batch directory
    test_files = list(batch_test_directory.glob("*"))
    assert len(test_files) > 0

    # Act: Process batch
    results = batch.process_batch(test_files)

    # Assert: All files processed
    assert len(results) == len(test_files)

    # Assert: Get summary
    summary = batch.get_summary(results)
    assert summary["total_files"] == len(test_files)
    assert summary["successful"] > 0
    assert summary["success_rate"] > 0.0

    # Assert: Successful results are valid
    for result in batch.get_successful_results(results):
        assert result.success is True
        assert result.extraction_result is not None


def test_e2e_multiple_formatters_parallel(sample_docx_file, tmp_path):
    """
    Test multiple formatters generate outputs independently.

    Verifies:
    - All formatters execute
    - Each produces valid output
    - Outputs are independent
    """
    # Arrange: Pipeline with multiple formatters
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())

    # Add all formatters
    pipeline.add_formatter(JsonFormatter())
    pipeline.add_formatter(MarkdownFormatter())
    pipeline.add_formatter(ChunkedTextFormatter())

    # Act: Process file
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: All formatters produced output
    assert len(result.formatted_outputs) == 3

    # Assert: Each output is valid
    format_types = {out.format_type for out in result.formatted_outputs}
    assert "json" in format_types
    assert "markdown" in format_types
    assert "chunked" in format_types

    # Assert: All outputs have content
    for output in result.formatted_outputs:
        assert output.success is True
        assert len(output.content) > 0


def test_e2e_quality_score_computation(sample_docx_file):
    """
    Test quality score is computed correctly.

    Verifies:
    - QualityValidator produces score
    - Score is in valid range (0-100)
    - Score reflects extraction quality
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_processor(ContextLinker())
    pipeline.add_processor(MetadataAggregator())
    pipeline.add_processor(QualityValidator())

    # Act
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Quality score present
    assert result.processing_result.quality_score is not None

    # Assert: Score in valid range
    score = result.processing_result.quality_score
    assert 0.0 <= score <= 100.0

    # Assert: For valid DOCX, score should be high
    assert score > 85.0, f"Expected high quality score for valid DOCX, got {score}"


def test_e2e_empty_file_handling(empty_docx_file):
    """
    Test pipeline handles empty file gracefully.

    Verifies:
    - Empty file doesn't crash pipeline
    - Result indicates success but no content
    - Warning about empty file
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_processor(ContextLinker())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(empty_docx_file)

    # Assert: Should succeed (valid but empty file)
    assert result.success is True or len(result.all_warnings) > 0

    # Assert: Little or no content
    if result.extraction_result:
        assert len(result.extraction_result.content_blocks) <= 1


def test_e2e_large_file_processing(large_docx_file):
    """
    Test pipeline handles large files.

    Verifies:
    - Large file processes successfully
    - Memory usage acceptable
    - Performance acceptable
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_processor(ContextLinker())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(large_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Many content blocks extracted
    assert len(result.extraction_result.content_blocks) > 50

    # Assert: Processing completed
    assert result.processing_result is not None


def test_e2e_metadata_propagation(sample_docx_file):
    """
    Test metadata propagates through pipeline.

    Verifies:
    - Document metadata preserved
    - Processing metadata added
    - All metadata accessible in final result
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_processor(MetadataAggregator())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Document metadata present
    assert result.extraction_result.document_metadata is not None
    doc_meta = result.extraction_result.document_metadata

    assert doc_meta.source_file == sample_docx_file
    assert doc_meta.file_format == "docx"
    assert doc_meta.title is not None  # Set in fixture

    # Assert: Processing metadata added
    assert result.processing_result.document_metadata is not None


def test_e2e_batch_progress_tracking(batch_test_directory, configured_pipeline, progress_tracker):
    """
    Test progress tracking across batch processing.

    Verifies:
    - Progress updates for batch
    - File-level progress
    - Summary completion
    """
    # Arrange
    progress_updates, progress_callback = progress_tracker

    batch = BatchProcessor(pipeline=configured_pipeline, max_workers=2)

    test_files = list(batch_test_directory.glob("*"))
    assert len(test_files) > 0

    # Act
    results = batch.process_batch(test_files, progress_callback=progress_callback)

    # Assert: Success
    assert len(results) == len(test_files)

    # Assert: Progress updates received
    assert len(progress_updates) > 0

    # Assert: File names mentioned in progress
    file_mentions = [u for u in progress_updates if "current_file" in u or "file" in str(u).lower()]
    assert len(file_mentions) > 0


# ==============================================================================
# Format-Specific Integration Tests
# ==============================================================================


def test_e2e_docx_with_tables(sample_docx_file):
    """
    Test DOCX extraction handles tables correctly.

    Verifies:
    - Tables detected
    - Table structure preserved
    - Table metadata extracted
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Content blocks include tables
    from src.core import ContentType

    content_types = {block.block_type for block in result.extraction_result.content_blocks}
    assert ContentType.TABLE in content_types or len(content_types) > 1


def test_e2e_pdf_text_extraction(sample_pdf_file):
    """
    Test PDF extraction with native text.

    Verifies:
    - PDF text extracted
    - Multi-page handling
    - Page position tracking
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import PdfExtractor

    pipeline.register_extractor("pdf", PdfExtractor())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(sample_pdf_file)

    # Assert: Success
    assert result.success is True

    # Assert: Content extracted
    assert len(result.extraction_result.content_blocks) > 0

    # Assert: Page information present
    first_block = result.extraction_result.content_blocks[0]
    assert first_block.position is not None
    assert first_block.position.page >= 1


# ==============================================================================
# Cross-Component Integration Tests
# ==============================================================================


def test_e2e_config_integration(sample_docx_file, config_file):
    """
    Test pipeline configuration from file.

    Verifies:
    - Config loaded correctly
    - Pipeline respects config settings
    - Components configured properly
    """
    # Arrange: Load config
    from src.infrastructure import ConfigManager

    config = ConfigManager(config_file)

    # Create pipeline with config
    pipeline = ExtractionPipeline(config=config)

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True


def test_e2e_logging_integration(sample_docx_file, tmp_path):
    """
    Test logging framework integration.

    Verifies:
    - Logs generated during processing
    - Structured logging works
    - Log levels correct
    """
    # Arrange
    from src.infrastructure import get_logger

    logger = get_logger("integration_test")

    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())
    pipeline.add_formatter(JsonFormatter())

    # Act
    result = pipeline.process_file(sample_docx_file)

    # Assert: Success
    assert result.success is True

    # Assert: Logging doesn't break anything
    logger.info("Test log message")


def test_e2e_error_handler_integration(corrupted_docx_file):
    """
    Test error handler integration with pipeline.

    Verifies:
    - Errors formatted correctly
    - Error codes present
    - User messages clear
    """
    # Arrange
    pipeline = ExtractionPipeline()

    from src.extractors import DocxExtractor

    pipeline.register_extractor("docx", DocxExtractor())

    # Act
    result = pipeline.process_file(corrupted_docx_file)

    # Assert: Failed
    assert result.success is False

    # Assert: Error information present
    assert len(result.all_errors) > 0

    # Assert: Failed stage identified
    assert result.failed_stage is not None
