"""
BatchProcessor - Parallel File Processing for Large Batches.

This module provides parallel batch processing capabilities for processing
multiple files concurrently using a thread pool.

Design:
- Thread pool for parallel execution
- Progress tracking across all files
- Error handling without stopping batch
- Result aggregation and statistics
- Configurable worker count and timeouts

Example:
    >>> from pipeline import ExtractionPipeline, BatchProcessor
    >>> from pathlib import Path
    >>>
    >>> # Configure pipeline
    >>> pipeline = ExtractionPipeline()
    >>> # ... register extractors, processors, formatters
    >>>
    >>> # Create batch processor
    >>> batch = BatchProcessor(pipeline=pipeline, max_workers=4)
    >>>
    >>> # Process multiple files
    >>> files = [Path("doc1.docx"), Path("doc2.pdf"), Path("doc3.pptx")]
    >>> results = batch.process_batch(files)
    >>>
    >>> # Get summary
    >>> summary = batch.get_summary(results)
    >>> print(f"Processed {summary['successful']}/{summary['total_files']} files")
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from core import PipelineResult, ProcessingStage
from infrastructure import (
    ErrorHandler,
    ProgressTracker,
    get_logger,
)

from .extraction_pipeline import ExtractionPipeline


class BatchProcessor:
    """
    Parallel batch processor for multiple files.

    This class coordinates parallel processing of multiple files using
    a thread pool, providing progress tracking and result aggregation.

    Attributes:
        pipeline: ExtractionPipeline instance to use for processing
        max_workers: Maximum number of concurrent worker threads
        timeout_per_file: Optional timeout in seconds per file
        logger: Structured logger instance
        error_handler: Error handling component

    Thread Safety:
        This class is thread-safe. The pipeline instances should also
        be thread-safe or use separate instances per thread.
    """

    def __init__(
        self,
        pipeline: Optional[ExtractionPipeline] = None,
        max_workers: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize batch processor.

        Args:
            pipeline: Optional ExtractionPipeline instance. Creates default if None.
            max_workers: Maximum concurrent workers. Defaults to CPU count.
            config: Optional configuration dict with keys:
                - max_workers: Worker count override
                - timeout_per_file: Timeout per file in seconds

        Raises:
            ValueError: If max_workers is <= 0

        Example:
            >>> batch = BatchProcessor(max_workers=4)
            >>> batch = BatchProcessor(config={'max_workers': 8, 'timeout_per_file': 300})
        """
        # Initialize configuration
        config = config or {}

        # Set max workers
        if max_workers is not None:
            if max_workers <= 0:
                raise ValueError("max_workers must be > 0")
            self.max_workers = max_workers
        elif "max_workers" in config:
            if config["max_workers"] <= 0:
                raise ValueError("max_workers must be > 0")
            self.max_workers = config["max_workers"]
        else:
            # Default to CPU count, capped at reasonable limit
            self.max_workers = min(os.cpu_count() or 4, 8)

        # Set timeout
        self.timeout_per_file = config.get("timeout_per_file", None)

        # Initialize pipeline
        self.pipeline = pipeline if pipeline is not None else ExtractionPipeline()

        # Initialize infrastructure
        self.logger = get_logger(__name__)
        self.error_handler = ErrorHandler()

        self.logger.info(f"BatchProcessor initialized with {self.max_workers} workers")

    def process_batch(
        self,
        file_paths: List[Path],
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[PipelineResult]:
        """
        Process multiple files in parallel.

        This method processes all files concurrently using a thread pool,
        tracking progress and collecting results.

        Args:
            file_paths: List of file paths to process
            progress_callback: Optional callback for progress updates

        Returns:
            List of PipelineResult in same order as input files

        Example:
            >>> files = [Path("doc1.docx"), Path("doc2.pdf")]
            >>> results = batch.process_batch(files)
            >>> for result in results:
            >>>     if result.success:
            >>>         print(f"Success: {result.source_file}")
            >>>     else:
            >>>         print(f"Failed: {result.source_file}")
        """
        if not file_paths:
            self.logger.info("No files to process in batch")
            return []

        self.logger.info(f"Starting batch processing of {len(file_paths)} files")

        # Initialize progress tracking
        tracker = ProgressTracker(
            total_items=len(file_paths),
            description="Batch processing files",
            callback=progress_callback,
        )

        # Store results with file path as key to preserve order
        results_map: Dict[Path, PipelineResult] = {}

        # Process files in parallel using thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self._process_single_file, file_path, tracker): file_path
                for file_path in file_paths
            }

            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]

                try:
                    result = future.result(timeout=self.timeout_per_file)
                    results_map[file_path] = result

                except Exception as e:
                    # Handle unexpected exceptions
                    self.logger.exception(f"Unexpected error processing {file_path}: {e}")

                    # Create failed result
                    results_map[file_path] = PipelineResult(
                        source_file=file_path,
                        success=False,
                        failed_stage=ProcessingStage.VALIDATION,
                        all_errors=(f"Batch processing error: {e}",),
                        started_at=datetime.now(timezone.utc),
                        completed_at=datetime.now(timezone.utc),
                    )

                # Update progress
                tracker.increment(current_item=str(file_path.name))

        # Return results in original order
        results = [results_map[file_path] for file_path in file_paths]

        self.logger.info(
            f"Batch processing complete: {sum(1 for r in results if r.success)}/{len(results)} successful"
        )

        return results

    def _process_single_file(self, file_path: Path, tracker: ProgressTracker) -> PipelineResult:
        """
        Process a single file within the batch.

        This is called by worker threads. It wraps pipeline processing
        with error handling.

        Args:
            file_path: Path to file to process
            tracker: Progress tracker instance

        Returns:
            PipelineResult for this file
        """
        self.logger.info(f"Processing file: {file_path}")

        # Create per-file progress callback
        # Note: We don't forward every file-level update to the batch tracker
        # to avoid flooding the progress display. Only batch-level increments
        # (via tracker.increment()) will update the overall batch progress.
        def file_progress_callback(status):
            # File-level progress is handled internally by the pipeline
            # We don't need to forward it to the batch tracker
            pass

        try:
            # Process through pipeline
            result = self.pipeline.process_file(file_path, progress_callback=file_progress_callback)

            return result

        except Exception as e:
            # Handle pipeline exceptions
            self.logger.exception(f"Pipeline raised exception for {file_path}: {e}")

            return PipelineResult(
                source_file=file_path,
                success=False,
                failed_stage=ProcessingStage.EXTRACTION,
                all_errors=(f"Pipeline exception: {e}",),
                started_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
            )

    def get_summary(self, results: List[PipelineResult]) -> Dict[str, Any]:
        """
        Get summary statistics for batch results.

        Args:
            results: List of pipeline results

        Returns:
            Dictionary with summary statistics:
                - total_files: Total number of files processed
                - successful: Number of successful files
                - failed: Number of failed files
                - success_rate: Fraction of successful files (0.0-1.0)
                - failed_stages: Count of failures by stage

        Example:
            >>> summary = batch.get_summary(results)
            >>> print(f"Success rate: {summary['success_rate']:.1%}")
        """
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful

        # Count failures by stage
        failed_stages: Dict[str, int] = {}
        for result in results:
            if not result.success and result.failed_stage:
                stage_name = result.failed_stage.value
                failed_stages[stage_name] = failed_stages.get(stage_name, 0) + 1

        return {
            "total_files": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0.0,
            "failed_stages": failed_stages,
        }

    def get_failed_results(self, results: List[PipelineResult]) -> List[PipelineResult]:
        """
        Extract failed results from batch.

        Args:
            results: List of pipeline results

        Returns:
            List of failed results only

        Example:
            >>> failed = batch.get_failed_results(results)
            >>> for result in failed:
            >>>     print(f"Failed: {result.source_file} - {result.all_errors}")
        """
        return [r for r in results if not r.success]

    def get_successful_results(self, results: List[PipelineResult]) -> List[PipelineResult]:
        """
        Extract successful results from batch.

        Args:
            results: List of pipeline results

        Returns:
            List of successful results only

        Example:
            >>> successful = batch.get_successful_results(results)
            >>> print(f"Processed {len(successful)} files successfully")
        """
        return [r for r in results if r.success]
