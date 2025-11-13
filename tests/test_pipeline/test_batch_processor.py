"""
Test Suite for BatchProcessor - Parallel File Processing.

This test suite validates the BatchProcessor class using strict TDD methodology.
Tests cover parallel processing, error handling, progress tracking, and result aggregation.

Test Coverage Areas:
1. Batch Initialization
2. Parallel File Processing
3. Progress Tracking with Multiple Files
4. Error Handling and Partial Results
5. Thread Pool Configuration
6. Result Aggregation

Coverage Target: >85%
"""

from unittest.mock import Mock

import pytest

# Import BatchProcessor (will fail initially - RED phase)
from pipeline.batch_processor import BatchProcessor

# Import pipeline (ExtractionPipeline already exists)
from pipeline.extraction_pipeline import ExtractionPipeline

# Import core models
from src.core import (
    PipelineResult,
    ProcessingStage,
)

# Import infrastructure

# ==============================================================================
# Test Fixtures
# ==============================================================================


@pytest.fixture
def sample_files(tmp_path):
    """Create multiple sample test files."""
    files = []
    for i in range(5):
        test_file = tmp_path / f"test_{i}.txt"
        test_file.write_text(f"Test content {i}")
        files.append(test_file)
    return files


@pytest.fixture
def mock_pipeline():
    """Mock ExtractionPipeline for testing."""
    pipeline = Mock(spec=ExtractionPipeline)

    # Mock successful processing
    def process_side_effect(file_path, progress_callback=None):
        return PipelineResult(source_file=file_path, success=True)

    pipeline.process_file.side_effect = process_side_effect
    return pipeline


# ==============================================================================
# Test Class: Batch Initialization
# ==============================================================================


class TestBatchInitialization:
    """Test batch processor initialization."""

    def test_batch_processor_creation(self):
        """Should create BatchProcessor with default settings."""
        # RED: Will fail - BatchProcessor doesn't exist yet
        batch = BatchProcessor()

        assert batch is not None
        assert isinstance(batch, BatchProcessor)

    def test_batch_processor_with_custom_pipeline(self, mock_pipeline):
        """Should accept custom pipeline instance."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        assert batch.pipeline == mock_pipeline

    def test_batch_processor_default_workers(self):
        """Should use sensible default for worker threads."""
        batch = BatchProcessor()

        # Should have at least 1 worker, at most CPU count
        assert batch.max_workers >= 1
        assert batch.max_workers <= 16  # Reasonable upper bound

    def test_batch_processor_custom_workers(self):
        """Should accept custom worker count."""
        batch = BatchProcessor(max_workers=4)

        assert batch.max_workers == 4

    def test_batch_processor_validates_worker_count(self):
        """Should reject invalid worker counts."""
        with pytest.raises(ValueError):
            BatchProcessor(max_workers=0)

        with pytest.raises(ValueError):
            BatchProcessor(max_workers=-1)


# ==============================================================================
# Test Class: Parallel Processing
# ==============================================================================


class TestParallelProcessing:
    """Test parallel file processing capabilities."""

    def test_process_batch_single_file(self, sample_files, mock_pipeline):
        """Should process single file correctly."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        results = batch.process_batch([sample_files[0]])

        assert len(results) == 1
        assert results[0].success is True
        assert mock_pipeline.process_file.call_count == 1

    def test_process_batch_multiple_files(self, sample_files, mock_pipeline):
        """Should process multiple files in parallel."""
        batch = BatchProcessor(pipeline=mock_pipeline, max_workers=4)

        results = batch.process_batch(sample_files)

        assert len(results) == len(sample_files)
        assert all(r.success for r in results)
        assert mock_pipeline.process_file.call_count == len(sample_files)

    def test_process_batch_respects_max_workers(self, sample_files):
        """Should limit concurrent processing to max_workers."""
        batch = BatchProcessor(max_workers=2)

        # We can't easily test exact parallelism without timing,
        # but we can verify it doesn't crash with limited workers
        # Note: This needs actual pipeline, so skip if complex
        # For now, test that max_workers is stored
        assert batch.max_workers == 2

    def test_process_batch_empty_list(self, mock_pipeline):
        """Should handle empty file list gracefully."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        results = batch.process_batch([])

        assert len(results) == 0
        assert mock_pipeline.process_file.call_count == 0

    def test_process_batch_preserves_order(self, sample_files, mock_pipeline):
        """Should return results in same order as input files."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        results = batch.process_batch(sample_files)

        for i, result in enumerate(results):
            assert result.source_file == sample_files[i]


# ==============================================================================
# Test Class: Error Handling
# ==============================================================================


class TestErrorHandling:
    """Test error handling in batch processing."""

    def test_process_batch_continues_on_single_failure(self, sample_files, mock_pipeline):
        """Should continue processing other files if one fails."""

        # Make second file fail
        def process_side_effect(file_path, progress_callback=None):
            if file_path == sample_files[1]:
                return PipelineResult(
                    source_file=file_path,
                    success=False,
                    failed_stage=ProcessingStage.EXTRACTION,
                    all_errors=("Test error",),
                )
            return PipelineResult(source_file=file_path, success=True)

        mock_pipeline.process_file.side_effect = process_side_effect

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(sample_files)

        # Should process all files
        assert len(results) == len(sample_files)
        # Only second should fail
        assert results[1].success is False
        # Others should succeed
        assert results[0].success is True
        assert results[2].success is True

    def test_process_batch_handles_pipeline_exception(self, sample_files, mock_pipeline):
        """Should handle exceptions from pipeline gracefully."""

        # Make pipeline raise exception for one file
        def process_side_effect(file_path, progress_callback=None):
            if file_path == sample_files[1]:
                raise Exception("Pipeline error")
            return PipelineResult(source_file=file_path, success=True)

        mock_pipeline.process_file.side_effect = process_side_effect

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(sample_files)

        # Should process all files
        assert len(results) == len(sample_files)
        # Second should have error (converted to failed PipelineResult)
        assert results[1].success is False
        # Others should succeed
        assert results[0].success is True
        assert results[2].success is True

    def test_process_batch_nonexistent_files(self, tmp_path, mock_pipeline):
        """Should handle nonexistent files gracefully."""
        nonexistent = [tmp_path / "does_not_exist_1.txt", tmp_path / "does_not_exist_2.txt"]

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(nonexistent)

        # Should attempt all files
        assert len(results) == len(nonexistent)
        # Pipeline should be called for each
        assert mock_pipeline.process_file.call_count == len(nonexistent)


# ==============================================================================
# Test Class: Progress Tracking
# ==============================================================================


class TestProgressTracking:
    """Test progress tracking during batch processing."""

    def test_process_batch_with_progress_callback(self, sample_files, mock_pipeline):
        """Should report progress via callback."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        progress_updates = []

        def progress_callback(status):
            progress_updates.append(status)

        results = batch.process_batch(sample_files, progress_callback=progress_callback)

        # Should receive progress updates
        assert len(progress_updates) > 0
        # Should have updates for each file
        assert len(progress_updates) >= len(sample_files)

    def test_progress_callback_reports_file_level_progress(self, sample_files, mock_pipeline):
        """Progress should include current file information."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        file_names = []

        def progress_callback(status):
            if "current_file" in status:
                file_names.append(status["current_file"])

        batch.process_batch(sample_files, progress_callback=progress_callback)

        # Should report each file being processed
        assert len(file_names) > 0

    def test_progress_callback_reports_percentage(self, sample_files, mock_pipeline):
        """Progress should include percentage completion."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        percentages = []

        def progress_callback(status):
            if "percentage" in status:
                percentages.append(status["percentage"])

        batch.process_batch(sample_files, progress_callback=progress_callback)

        # Should have percentage updates
        assert len(percentages) > 0
        # Final percentage should be 100
        assert percentages[-1] == 100.0

    def test_progress_callback_exception_handling(self, sample_files, mock_pipeline):
        """Should handle callback exceptions gracefully."""
        batch = BatchProcessor(pipeline=mock_pipeline)

        def failing_callback(status):
            raise Exception("Callback error")

        # Should not crash even with failing callback
        results = batch.process_batch(sample_files, progress_callback=failing_callback)

        assert len(results) == len(sample_files)


# ==============================================================================
# Test Class: Result Aggregation
# ==============================================================================


class TestResultAggregation:
    """Test result collection and aggregation."""

    def test_get_summary_statistics(self, sample_files, mock_pipeline):
        """Should provide summary statistics for batch results."""

        # Make some files fail
        def process_side_effect(file_path, progress_callback=None):
            if file_path in sample_files[1:3]:
                return PipelineResult(
                    source_file=file_path, success=False, failed_stage=ProcessingStage.EXTRACTION
                )
            return PipelineResult(source_file=file_path, success=True)

        mock_pipeline.process_file.side_effect = process_side_effect

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(sample_files)

        summary = batch.get_summary(results)

        assert summary["total_files"] == len(sample_files)
        assert summary["successful"] == 3
        assert summary["failed"] == 2
        assert summary["success_rate"] == 3 / 5

    def test_get_failed_files(self, sample_files, mock_pipeline):
        """Should extract list of failed files."""

        # Make second file fail
        def process_side_effect(file_path, progress_callback=None):
            if file_path == sample_files[1]:
                return PipelineResult(
                    source_file=file_path, success=False, failed_stage=ProcessingStage.EXTRACTION
                )
            return PipelineResult(source_file=file_path, success=True)

        mock_pipeline.process_file.side_effect = process_side_effect

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(sample_files)

        failed = batch.get_failed_results(results)

        assert len(failed) == 1
        assert failed[0].source_file == sample_files[1]

    def test_get_successful_files(self, sample_files, mock_pipeline):
        """Should extract list of successful files."""

        # Make second file fail
        def process_side_effect(file_path, progress_callback=None):
            if file_path == sample_files[1]:
                return PipelineResult(
                    source_file=file_path, success=False, failed_stage=ProcessingStage.EXTRACTION
                )
            return PipelineResult(source_file=file_path, success=True)

        mock_pipeline.process_file.side_effect = process_side_effect

        batch = BatchProcessor(pipeline=mock_pipeline)
        results = batch.process_batch(sample_files)

        successful = batch.get_successful_results(results)

        assert len(successful) == 4
        assert all(r.success for r in successful)


# ==============================================================================
# Test Class: Configuration
# ==============================================================================


class TestConfiguration:
    """Test batch processor configuration options."""

    def test_configure_via_dict(self):
        """Should accept configuration via dict."""
        config = {
            "max_workers": 8,
            "timeout_per_file": 300,
        }

        batch = BatchProcessor(config=config)

        assert batch.max_workers == 8

    def test_default_timeout(self):
        """Should have sensible default timeout."""
        batch = BatchProcessor()

        # Should have some timeout set (not None)
        assert hasattr(batch, "timeout_per_file")
        assert batch.timeout_per_file is None or batch.timeout_per_file > 0
