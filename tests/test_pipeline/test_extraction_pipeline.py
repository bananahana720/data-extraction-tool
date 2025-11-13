"""
Test Suite for ExtractionPipeline - Orchestrates End-to-End Extraction.

This test suite validates the ExtractionPipeline class using strict TDD methodology.
Tests are organized by feature area and follow Red-Green-Refactor cycles.

Test Coverage Areas:
1. Pipeline Initialization
2. Format Detection
3. Extractor Registration and Selection
4. Processor Chain Configuration and Execution
5. Formatter Configuration and Execution
6. Error Handling and Recovery
7. Progress Tracking Integration
8. End-to-End Processing

Coverage Target: >85%
"""

from pathlib import Path
from unittest.mock import Mock

import pytest

# Import pipeline (will fail initially - RED phase)
from pipeline.extraction_pipeline import ExtractionPipeline

# Import core models and interfaces
from src.core import (
    BaseExtractor,
    BaseFormatter,
    BaseProcessor,
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    FormattedOutput,
    PipelineResult,
    ProcessingResult,
    ProcessingStage,
)

# Import infrastructure
from src.infrastructure import (
    ConfigManager,
    ErrorHandler,
)

# ==============================================================================
# Test Fixtures and Mocks
# ==============================================================================


@pytest.fixture
def mock_config():
    """Mock ConfigManager for testing."""
    config = Mock(spec=ConfigManager)
    config.get.return_value = {}
    config.get_section.return_value = {}
    config.has.return_value = False
    return config


@pytest.fixture
def mock_extractor():
    """Mock BaseExtractor for testing."""
    extractor = Mock(spec=BaseExtractor)
    extractor.supports_format.return_value = True
    extractor.get_supported_extensions.return_value = [".txt"]

    # Mock successful extraction
    extractor.extract.return_value = ExtractionResult(
        content_blocks=(ContentBlock(content="Test content", block_type=ContentType.PARAGRAPH),),
        document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="txt"),
        success=True,
    )

    return extractor


@pytest.fixture
def mock_processor():
    """Mock BaseProcessor for testing."""
    processor = Mock(spec=BaseProcessor)
    processor.get_processor_name.return_value = "MockProcessor"
    processor.get_dependencies.return_value = []
    processor.is_optional.return_value = False

    # Mock successful processing
    def process_side_effect(extraction_result):
        return ProcessingResult(
            content_blocks=extraction_result.content_blocks,
            document_metadata=extraction_result.document_metadata,
            processing_stage=ProcessingStage.CONTEXT_LINKING,
            success=True,
        )

    processor.process.side_effect = process_side_effect
    return processor


@pytest.fixture
def mock_formatter():
    """Mock BaseFormatter for testing."""
    formatter = Mock(spec=BaseFormatter)
    formatter.get_format_type.return_value = "json"
    formatter.get_file_extension.return_value = ".json"

    # Mock successful formatting
    def format_side_effect(processing_result):
        return FormattedOutput(
            content='{"test": "data"}',
            format_type="json",
            source_document=processing_result.document_metadata.source_file,
            success=True,
        )

    formatter.format.side_effect = format_side_effect
    return formatter


@pytest.fixture
def sample_file(tmp_path):
    """Create a sample test file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content for extraction")
    return test_file


# ==============================================================================
# Test Class: Pipeline Initialization
# ==============================================================================


class TestPipelineInitialization:
    """Test pipeline initialization and configuration."""

    def test_pipeline_creation_with_default_config(self):
        """Pipeline should initialize with default configuration."""
        # RED: This will fail - ExtractionPipeline doesn't exist yet
        pipeline = ExtractionPipeline()

        assert pipeline is not None
        assert isinstance(pipeline, ExtractionPipeline)

    def test_pipeline_creation_with_custom_config(self, mock_config):
        """Pipeline should accept custom ConfigManager."""
        pipeline = ExtractionPipeline(config=mock_config)

        assert pipeline is not None
        assert pipeline.config == mock_config

    def test_pipeline_initializes_error_handler(self):
        """Pipeline should initialize ErrorHandler."""
        pipeline = ExtractionPipeline()

        assert hasattr(pipeline, "error_handler")
        assert isinstance(pipeline.error_handler, ErrorHandler)

    def test_pipeline_initializes_empty_extractors(self):
        """Pipeline should start with no registered extractors."""
        pipeline = ExtractionPipeline()

        assert hasattr(pipeline, "_extractors")
        assert len(pipeline._extractors) == 0

    def test_pipeline_initializes_empty_processors(self):
        """Pipeline should start with no registered processors."""
        pipeline = ExtractionPipeline()

        assert hasattr(pipeline, "_processors")
        assert len(pipeline._processors) == 0

    def test_pipeline_initializes_empty_formatters(self):
        """Pipeline should start with no registered formatters."""
        pipeline = ExtractionPipeline()

        assert hasattr(pipeline, "_formatters")
        assert len(pipeline._formatters) == 0


# ==============================================================================
# Test Class: Format Detection
# ==============================================================================


class TestFormatDetection:
    """Test automatic file format detection."""

    def test_detect_format_from_docx_extension(self, tmp_path):
        """Should detect DOCX format from .docx extension."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.docx"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type == "docx"

    def test_detect_format_from_pdf_extension(self, tmp_path):
        """Should detect PDF format from .pdf extension."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.pdf"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type == "pdf"

    def test_detect_format_from_pptx_extension(self, tmp_path):
        """Should detect PPTX format from .pptx extension."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.pptx"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type == "pptx"

    def test_detect_format_from_xlsx_extension(self, tmp_path):
        """Should detect XLSX format from .xlsx extension."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.xlsx"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type == "xlsx"

    def test_detect_format_case_insensitive(self, tmp_path):
        """Format detection should be case-insensitive."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.DOCX"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type == "docx"

    def test_detect_format_unknown_extension(self, tmp_path):
        """Should return None for unknown extensions."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test.unknown"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type is None

    def test_detect_format_no_extension(self, tmp_path):
        """Should return None for files without extension."""
        pipeline = ExtractionPipeline()
        test_file = tmp_path / "test"
        test_file.touch()

        format_type = pipeline.detect_format(test_file)

        assert format_type is None


# ==============================================================================
# Test Class: Extractor Registration
# ==============================================================================


class TestExtractorRegistration:
    """Test extractor registration and selection."""

    def test_register_extractor_for_format(self, mock_extractor):
        """Should register extractor for specific format."""
        pipeline = ExtractionPipeline()

        pipeline.register_extractor("txt", mock_extractor)

        assert "txt" in pipeline._extractors
        assert pipeline._extractors["txt"] == mock_extractor

    def test_register_multiple_extractors(self, mock_extractor):
        """Should register multiple extractors for different formats."""
        pipeline = ExtractionPipeline()
        extractor2 = Mock(spec=BaseExtractor)

        pipeline.register_extractor("txt", mock_extractor)
        pipeline.register_extractor("pdf", extractor2)

        assert len(pipeline._extractors) == 2
        assert pipeline._extractors["txt"] == mock_extractor
        assert pipeline._extractors["pdf"] == extractor2

    def test_register_extractor_replaces_existing(self, mock_extractor):
        """Registering same format should replace existing extractor."""
        pipeline = ExtractionPipeline()
        extractor2 = Mock(spec=BaseExtractor)

        pipeline.register_extractor("txt", mock_extractor)
        pipeline.register_extractor("txt", extractor2)

        assert len(pipeline._extractors) == 1
        assert pipeline._extractors["txt"] == extractor2

    def test_get_extractor_for_registered_format(self, mock_extractor):
        """Should retrieve registered extractor for format."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)

        extractor = pipeline.get_extractor("txt")

        assert extractor == mock_extractor

    def test_get_extractor_for_unregistered_format(self):
        """Should return None for unregistered format."""
        pipeline = ExtractionPipeline()

        extractor = pipeline.get_extractor("unknown")

        assert extractor is None


# ==============================================================================
# Test Class: Processor Chain
# ==============================================================================


class TestProcessorChain:
    """Test processor registration and chain execution."""

    def test_add_processor(self, mock_processor):
        """Should add processor to chain."""
        pipeline = ExtractionPipeline()

        pipeline.add_processor(mock_processor)

        assert len(pipeline._processors) == 1
        assert mock_processor in pipeline._processors

    def test_add_multiple_processors(self, mock_processor):
        """Should add multiple processors in order."""
        pipeline = ExtractionPipeline()
        processor2 = Mock(spec=BaseProcessor)
        processor2.get_processor_name.return_value = "Processor2"
        processor2.get_dependencies.return_value = []

        pipeline.add_processor(mock_processor)
        pipeline.add_processor(processor2)

        assert len(pipeline._processors) == 2

    def test_processor_chain_respects_dependencies(self):
        """Processors should be ordered by dependencies."""
        pipeline = ExtractionPipeline()

        # Create processors with dependencies
        proc1 = Mock(spec=BaseProcessor)
        proc1.get_processor_name.return_value = "Processor1"
        proc1.get_dependencies.return_value = []

        proc2 = Mock(spec=BaseProcessor)
        proc2.get_processor_name.return_value = "Processor2"
        proc2.get_dependencies.return_value = ["Processor1"]

        # Add in wrong order
        pipeline.add_processor(proc2)
        pipeline.add_processor(proc1)

        # Should be reordered based on dependencies
        ordered = pipeline._order_processors()

        assert ordered[0] == proc1
        assert ordered[1] == proc2

    def test_processor_chain_circular_dependency_detection(self):
        """Should detect circular dependencies in processor chain."""
        pipeline = ExtractionPipeline()

        proc1 = Mock(spec=BaseProcessor)
        proc1.get_processor_name.return_value = "Processor1"
        proc1.get_dependencies.return_value = ["Processor2"]

        proc2 = Mock(spec=BaseProcessor)
        proc2.get_processor_name.return_value = "Processor2"
        proc2.get_dependencies.return_value = ["Processor1"]

        pipeline.add_processor(proc1)
        pipeline.add_processor(proc2)

        # Should raise error when trying to order
        with pytest.raises(ValueError, match="Circular dependency"):
            pipeline._order_processors()


# ==============================================================================
# Test Class: Formatter Integration
# ==============================================================================


class TestFormatterIntegration:
    """Test formatter registration and execution."""

    def test_add_formatter(self, mock_formatter):
        """Should add formatter to pipeline."""
        pipeline = ExtractionPipeline()

        pipeline.add_formatter(mock_formatter)

        assert len(pipeline._formatters) == 1
        assert mock_formatter in pipeline._formatters

    def test_add_multiple_formatters(self, mock_formatter):
        """Should support multiple formatters."""
        pipeline = ExtractionPipeline()
        formatter2 = Mock(spec=BaseFormatter)
        formatter2.get_format_type.return_value = "markdown"

        pipeline.add_formatter(mock_formatter)
        pipeline.add_formatter(formatter2)

        assert len(pipeline._formatters) == 2


# ==============================================================================
# Test Class: End-to-End Processing
# ==============================================================================


class TestEndToEndProcessing:
    """Test complete pipeline execution."""

    def test_process_file_successful(
        self, sample_file, mock_extractor, mock_processor, mock_formatter
    ):
        """Should process file through complete pipeline."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        result = pipeline.process_file(sample_file)

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.source_file == sample_file
        assert result.extraction_result is not None
        assert result.processing_result is not None
        assert len(result.formatted_outputs) == 1

    def test_process_file_unknown_format(self, tmp_path):
        """Should fail gracefully for unknown file format."""
        pipeline = ExtractionPipeline()
        unknown_file = tmp_path / "test.unknown"
        unknown_file.touch()

        result = pipeline.process_file(unknown_file)

        assert isinstance(result, PipelineResult)
        assert result.success is False
        assert result.failed_stage == ProcessingStage.VALIDATION
        assert len(result.all_errors) > 0

    def test_process_file_no_extractor_registered(self, sample_file):
        """Should fail if no extractor registered for format."""
        pipeline = ExtractionPipeline()
        # Don't register any extractors

        result = pipeline.process_file(sample_file)

        assert isinstance(result, PipelineResult)
        assert result.success is False
        assert result.failed_stage == ProcessingStage.VALIDATION

    def test_process_file_extraction_failure(self, sample_file, mock_processor, mock_formatter):
        """Should handle extraction failure gracefully."""
        pipeline = ExtractionPipeline()

        # Create failing extractor
        failing_extractor = Mock(spec=BaseExtractor)
        failing_extractor.supports_format.return_value = True
        failing_extractor.extract.return_value = ExtractionResult(
            success=False, errors=("Extraction failed",)
        )

        pipeline.register_extractor("txt", failing_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        result = pipeline.process_file(sample_file)

        assert isinstance(result, PipelineResult)
        assert result.success is False
        assert result.failed_stage == ProcessingStage.EXTRACTION
        assert len(result.all_errors) > 0

    def test_process_file_nonexistent_file(self, tmp_path):
        """Should fail for nonexistent file."""
        pipeline = ExtractionPipeline()
        nonexistent = tmp_path / "does_not_exist.txt"

        result = pipeline.process_file(nonexistent)

        assert isinstance(result, PipelineResult)
        assert result.success is False
        assert len(result.all_errors) > 0

    def test_process_file_with_progress_callback(
        self, sample_file, mock_extractor, mock_processor, mock_formatter
    ):
        """Should support progress tracking with callbacks."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        # Track progress updates
        progress_updates = []

        def progress_callback(status):
            progress_updates.append(status)

        result = pipeline.process_file(sample_file, progress_callback=progress_callback)

        assert result.success is True
        # Should have received progress updates
        assert len(progress_updates) > 0

    def test_process_file_calls_stages_in_order(
        self, sample_file, mock_extractor, mock_processor, mock_formatter
    ):
        """Should call pipeline stages in correct order."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        result = pipeline.process_file(sample_file)

        # Verify call order
        assert mock_extractor.extract.called
        assert mock_processor.process.called
        assert mock_formatter.format.called

        # Extractor called before processor
        assert mock_extractor.extract.call_count == 1
        # Processor called with extraction result
        assert mock_processor.process.call_count == 1
        # Formatter called with processing result
        assert mock_formatter.format.call_count == 1

    def test_process_file_aggregates_errors_from_all_stages(self, sample_file):
        """Should aggregate errors from all pipeline stages."""
        pipeline = ExtractionPipeline()

        # Extractor with warnings
        extractor = Mock(spec=BaseExtractor)
        extractor.supports_format.return_value = True
        extractor.extract.return_value = ExtractionResult(
            content_blocks=(ContentBlock(content="test", block_type=ContentType.PARAGRAPH),),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="txt"),
            success=True,
            warnings=("Extractor warning",),
        )

        # Processor with warnings
        processor = Mock(spec=BaseProcessor)
        processor.get_processor_name.return_value = "TestProcessor"
        processor.get_dependencies.return_value = []
        processor.process.return_value = ProcessingResult(
            content_blocks=(ContentBlock(content="test", block_type=ContentType.PARAGRAPH),),
            document_metadata=DocumentMetadata(source_file=sample_file, file_format="txt"),
            success=True,
            warnings=("Processor warning",),
        )

        pipeline.register_extractor("txt", extractor)
        pipeline.add_processor(processor)

        result = pipeline.process_file(sample_file)

        # Should aggregate warnings from both stages
        assert len(result.all_warnings) >= 2
        assert any("Extractor warning" in w for w in result.all_warnings)
        assert any("Processor warning" in w for w in result.all_warnings)


# ==============================================================================
# Test Class: Error Handling
# ==============================================================================


class TestErrorHandling:
    """Test error handling and recovery patterns."""

    def test_pipeline_handles_extractor_exception(self, sample_file):
        """Should handle extractor exceptions gracefully."""
        pipeline = ExtractionPipeline()

        # Create extractor that raises exception
        failing_extractor = Mock(spec=BaseExtractor)
        failing_extractor.supports_format.return_value = True
        failing_extractor.extract.side_effect = Exception("Unexpected error")

        pipeline.register_extractor("txt", failing_extractor)

        result = pipeline.process_file(sample_file)

        # Should not crash, should return failed result
        assert isinstance(result, PipelineResult)
        assert result.success is False
        assert len(result.all_errors) > 0

    def test_pipeline_handles_processor_exception(self, sample_file, mock_extractor):
        """Should handle processor exceptions gracefully."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)

        # Create processor that raises exception
        failing_processor = Mock(spec=BaseProcessor)
        failing_processor.get_processor_name.return_value = "FailingProcessor"
        failing_processor.get_dependencies.return_value = []
        failing_processor.is_optional.return_value = False  # Required processor
        failing_processor.process.side_effect = Exception("Processor error")

        pipeline.add_processor(failing_processor)

        result = pipeline.process_file(sample_file)

        assert isinstance(result, PipelineResult)
        assert result.success is False

    def test_pipeline_handles_formatter_exception(
        self, sample_file, mock_extractor, mock_processor
    ):
        """Should handle formatter exceptions gracefully."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)

        # Create formatter that raises exception
        failing_formatter = Mock(spec=BaseFormatter)
        failing_formatter.get_format_type.return_value = "json"
        failing_formatter.format.side_effect = Exception("Formatter error")

        pipeline.add_formatter(failing_formatter)

        result = pipeline.process_file(sample_file)

        # Formatting errors should not fail entire pipeline
        # (we got extraction and processing results)
        assert isinstance(result, PipelineResult)
        # May still succeed if partial results acceptable
        assert result.extraction_result is not None
        assert result.processing_result is not None


# ==============================================================================
# Test Class: Progress Tracking
# ==============================================================================


class TestProgressTracking:
    """Test progress tracking integration."""

    def test_pipeline_reports_progress_at_each_stage(
        self, sample_file, mock_extractor, mock_processor, mock_formatter
    ):
        """Should report progress at extraction, processing, formatting stages."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        progress_stages = []

        def progress_callback(status):
            if "stage" in status:
                progress_stages.append(status["stage"])

        pipeline.process_file(sample_file, progress_callback=progress_callback)

        # Should have reported multiple stages
        assert len(progress_stages) >= 3

    def test_pipeline_reports_percentage_progress(
        self, sample_file, mock_extractor, mock_processor, mock_formatter
    ):
        """Should report percentage completion."""
        pipeline = ExtractionPipeline()
        pipeline.register_extractor("txt", mock_extractor)
        pipeline.add_processor(mock_processor)
        pipeline.add_formatter(mock_formatter)

        percentages = []

        def progress_callback(status):
            if "percentage" in status:
                percentages.append(status["percentage"])

        pipeline.process_file(sample_file, progress_callback=progress_callback)

        # Percentages should increase
        assert len(percentages) > 0
        # Final percentage should be 100
        assert percentages[-1] == 100.0
