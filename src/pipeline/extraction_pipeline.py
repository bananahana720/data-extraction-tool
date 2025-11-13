"""
ExtractionPipeline - Main Pipeline Orchestrator.

This module implements the main extraction pipeline that coordinates:
1. File format detection
2. Content extraction via format-specific extractors
3. Content enrichment via processor chain
4. Output formatting via multiple formatters
5. Progress tracking and error handling

Design:
- Implements BasePipeline interface
- Integrates with all infrastructure components
- Supports configurable processor chains
- Handles errors gracefully at each stage
- Provides detailed progress reporting

Example:
    >>> from pipeline import ExtractionPipeline
    >>> from extractors import DocxExtractor
    >>> from processors import ContextLinker
    >>> from formatters import JsonFormatter
    >>>
    >>> # Configure pipeline
    >>> pipeline = ExtractionPipeline()
    >>> pipeline.register_extractor("docx", DocxExtractor())
    >>> pipeline.add_processor(ContextLinker())
    >>> pipeline.add_formatter(JsonFormatter())
    >>>
    >>> # Process file
    >>> result = pipeline.process_file(Path("document.docx"))
    >>> if result.success:
    >>>     print(f"Extracted {len(result.extraction_result.content_blocks)} blocks")
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from core import (
    BaseExtractor,
    BaseFormatter,
    BasePipeline,
    BaseProcessor,
    ExtractionResult,
    PipelineResult,
    ProcessingResult,
    ProcessingStage,
)
from infrastructure import (
    ConfigManager,
    ErrorHandler,
    get_logger,
    timed,
)


class ExtractionPipeline(BasePipeline):
    """
    Main pipeline orchestrator for document extraction.

    This class coordinates the entire extraction workflow from file input
    to formatted output, integrating extractors, processors, and formatters.

    Attributes:
        config: Configuration manager instance
        error_handler: Error handling component
        logger: Structured logger instance

    Thread Safety:
        This class is not thread-safe. Create separate instances for
        concurrent processing or use BatchProcessor.
    """

    # Supported file formats and their extensions
    FORMAT_EXTENSIONS = {
        ".docx": "docx",
        ".pdf": "pdf",
        ".pptx": "pptx",
        ".xlsx": "xlsx",
        ".xls": "xlsx",  # Treat old Excel as xlsx
        ".csv": "csv",
        ".tsv": "csv",  # TSV uses same extractor as CSV
        ".txt": "txt",  # Plain text files (for testing)
    }

    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize extraction pipeline.

        Args:
            config: Optional ConfigManager instance. If None, creates default.
        """
        # Initialize configuration
        self.config = config if config is not None else self._create_default_config()

        # Initialize infrastructure components
        self.error_handler = ErrorHandler()
        self.logger = get_logger(__name__)

        # Initialize component registries
        self._extractors: dict[str, BaseExtractor] = {}
        self._processors: list[BaseProcessor] = []
        self._formatters: list[BaseFormatter] = []

        self.logger.info("ExtractionPipeline initialized")

    def _create_default_config(self) -> ConfigManager:
        """
        Create default configuration.

        Returns:
            ConfigManager with default settings
        """
        # Create in-memory config with defaults
        from tempfile import NamedTemporaryFile

        import yaml

        # Create temporary YAML file with defaults
        defaults = {
            "pipeline": {
                "max_processors": 10,
                "continue_on_error": False,
            }
        }

        with NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(defaults, f)
            temp_path = f.name

        config = ConfigManager(temp_path, defaults=defaults)

        # Clean up temp file
        Path(temp_path).unlink()

        return config

    def detect_format(self, file_path: Path) -> Optional[str]:
        """
        Detect file format from extension.

        Args:
            file_path: Path to file

        Returns:
            Format identifier (e.g., 'docx', 'pdf') or None if unknown
        """
        extension = file_path.suffix.lower()
        return self.FORMAT_EXTENSIONS.get(extension)

    def register_extractor(self, format_type: str, extractor: BaseExtractor) -> None:
        """
        Register a format-specific extractor.

        Args:
            format_type: Format identifier (e.g., "docx", "pdf")
            extractor: Extractor instance

        Example:
            >>> pipeline.register_extractor("docx", DocxExtractor())
        """
        self._extractors[format_type] = extractor
        self.logger.info(f"Registered extractor for format: {format_type}")

    def get_extractor(self, format_type: str) -> Optional[BaseExtractor]:
        """
        Get registered extractor for format.

        Args:
            format_type: Format identifier

        Returns:
            Extractor instance or None if not registered
        """
        return self._extractors.get(format_type)

    def add_processor(self, processor: BaseProcessor) -> None:
        """
        Add a processor to the pipeline.

        Processors are automatically ordered based on dependencies.

        Args:
            processor: Processor instance

        Example:
            >>> pipeline.add_processor(ContextLinker())
            >>> pipeline.add_processor(MetadataAggregator())
        """
        self._processors.append(processor)
        self.logger.info(f"Added processor: {processor.get_processor_name()}")

    def add_formatter(self, formatter: BaseFormatter) -> None:
        """
        Add an output formatter to the pipeline.

        Multiple formatters can be added to generate multiple output formats.

        Args:
            formatter: Formatter instance

        Example:
            >>> pipeline.add_formatter(JsonFormatter())
            >>> pipeline.add_formatter(MarkdownFormatter())
        """
        self._formatters.append(formatter)
        self.logger.info(f"Added formatter: {formatter.get_format_type()}")

    def _order_processors(self) -> list[BaseProcessor]:
        """
        Order processors based on dependencies using topological sort.

        Returns:
            Ordered list of processors

        Raises:
            ValueError: If circular dependency detected
        """
        if not self._processors:
            return []

        # Build dependency graph
        graph: dict[str, list[str]] = {}
        processor_map: dict[str, BaseProcessor] = {}

        for processor in self._processors:
            name = processor.get_processor_name()
            processor_map[name] = processor
            graph[name] = processor.get_dependencies()

        # Topological sort using Kahn's algorithm
        # in_degree[X] = number of processors that depend on X
        in_degree: dict[str, int] = {name: 0 for name in graph}

        # Calculate in-degrees: count how many processors have each as a dependency
        for name, deps in graph.items():
            in_degree[name] = len(deps)

        # Queue of processors with no dependencies
        queue = [name for name, degree in in_degree.items() if degree == 0]
        ordered = []

        while queue:
            current = queue.pop(0)
            ordered.append(current)

            # Find processors that depend on current and reduce their in-degree
            for name, deps in graph.items():
                if current in deps:
                    in_degree[name] -= 1
                    if in_degree[name] == 0 and name not in ordered:
                        queue.append(name)

        # Check for circular dependencies
        if len(ordered) != len(graph):
            raise ValueError(
                "Circular dependency detected in processor chain. "
                f"Processors: {list(graph.keys())}"
            )

        # Convert names back to processor instances
        return [processor_map[name] for name in ordered]

    def _report_progress(
        self,
        callback: Optional[Callable[[dict[str, Any]], None]],
        stage: str,
        percentage: float,
        message: Optional[str] = None,
    ) -> None:
        """
        Report progress to callback if provided.

        Args:
            callback: Progress callback function
            stage: Current pipeline stage
            percentage: Completion percentage (0-100)
            message: Optional progress message
        """
        if callback is None:
            return

        status = {
            "stage": stage,
            "percentage": percentage,
            "message": message or f"Processing: {stage}",
        }

        try:
            callback(status)
        except Exception as e:
            self.logger.warning(f"Progress callback failed: {e}")

    @timed(get_logger(__name__))
    def process_file(
        self, file_path: Path, progress_callback: Optional[Callable[[dict[str, Any]], None]] = None
    ) -> PipelineResult:
        """
        Process a single file through the complete pipeline.

        This is the main entry point for file processing. It coordinates:
        1. Validation
        2. Extraction
        3. Processing (all processors in dependency order)
        4. Formatting (all formatters in parallel)

        Args:
            file_path: Path to file to process
            progress_callback: Optional callback for progress updates

        Returns:
            PipelineResult with results from all stages

        Example:
            >>> result = pipeline.process_file(Path("document.docx"))
            >>> if result.success:
            >>>     print(f"Success! Generated {len(result.formatted_outputs)} outputs")
            >>> else:
            >>>     print(f"Failed at {result.failed_stage}: {result.all_errors}")
        """
        start_time = datetime.now(timezone.utc)
        all_errors: list[str] = []
        all_warnings: list[str] = []

        self.logger.info(f"Processing file: {file_path}")
        self._report_progress(progress_callback, "validation", 0.0, "Validating file")

        # Stage 1: Validation
        try:
            # Check file exists
            if not file_path.exists():
                error_msg = f"File not found: {file_path}"
                all_errors.append(error_msg)
                self.logger.error(error_msg)

                return PipelineResult(
                    source_file=file_path,
                    success=False,
                    failed_stage=ProcessingStage.VALIDATION,
                    started_at=start_time,
                    completed_at=datetime.now(timezone.utc),
                    all_errors=tuple(all_errors),
                )

            # Detect format
            format_type = self.detect_format(file_path)
            if format_type is None:
                error_msg = f"Unknown file format: {file_path.suffix}"
                all_errors.append(error_msg)
                self.logger.error(error_msg)

                return PipelineResult(
                    source_file=file_path,
                    success=False,
                    failed_stage=ProcessingStage.VALIDATION,
                    started_at=start_time,
                    completed_at=datetime.now(timezone.utc),
                    all_errors=tuple(all_errors),
                )

            # Check extractor registered
            extractor = self.get_extractor(format_type)
            if extractor is None:
                error_msg = f"No extractor registered for format: {format_type}"
                all_errors.append(error_msg)
                self.logger.error(error_msg)

                return PipelineResult(
                    source_file=file_path,
                    success=False,
                    failed_stage=ProcessingStage.VALIDATION,
                    started_at=start_time,
                    completed_at=datetime.now(timezone.utc),
                    all_errors=tuple(all_errors),
                )

        except Exception as e:
            error_msg = f"Validation failed: {e}"
            all_errors.append(error_msg)
            self.logger.exception(error_msg)

            return PipelineResult(
                source_file=file_path,
                success=False,
                failed_stage=ProcessingStage.VALIDATION,
                started_at=start_time,
                completed_at=datetime.now(timezone.utc),
                all_errors=tuple(all_errors),
            )

        # Stage 2: Extraction
        self._report_progress(progress_callback, "extraction", 20.0, "Extracting content")

        try:
            extraction_result = extractor.extract(file_path)

            # Collect errors and warnings
            all_errors.extend(extraction_result.errors)
            all_warnings.extend(extraction_result.warnings)

            if not extraction_result.success:
                self.logger.error(f"Extraction failed: {extraction_result.errors}")

                return PipelineResult(
                    source_file=file_path,
                    extraction_result=extraction_result,
                    success=False,
                    failed_stage=ProcessingStage.EXTRACTION,
                    started_at=start_time,
                    completed_at=datetime.now(timezone.utc),
                    all_errors=tuple(all_errors),
                    all_warnings=tuple(all_warnings),
                )

        except Exception as e:
            error_msg = f"Extraction raised exception: {e}"
            all_errors.append(error_msg)
            self.logger.exception(error_msg)

            return PipelineResult(
                source_file=file_path,
                success=False,
                failed_stage=ProcessingStage.EXTRACTION,
                started_at=start_time,
                completed_at=datetime.now(timezone.utc),
                all_errors=tuple(all_errors),
                all_warnings=tuple(all_warnings),
            )

        # Stage 3: Processing
        self._report_progress(progress_callback, "processing", 40.0, "Processing content")

        processing_result: Optional[ProcessingResult] = None

        try:
            # Order processors by dependencies
            ordered_processors = self._order_processors()

            # Run processors in sequence
            current_input = extraction_result

            for i, processor in enumerate(ordered_processors):
                processor_name = processor.get_processor_name()
                self.logger.info(f"Running processor: {processor_name}")

                # Calculate progress (40% to 70% range)
                progress = 40.0 + (30.0 * (i + 1) / max(len(ordered_processors), 1))
                self._report_progress(
                    progress_callback, "processing", progress, f"Running {processor_name}"
                )

                try:
                    # Convert extraction result to processing result if needed
                    if isinstance(current_input, ExtractionResult):
                        # First processor gets extraction result
                        processing_result = processor.process(current_input)
                    else:
                        # Subsequent processors get processing result
                        # But process() expects ExtractionResult, so we need to adapt
                        # Create a pseudo ExtractionResult with all media assets preserved
                        pseudo_extraction = ExtractionResult(
                            content_blocks=current_input.content_blocks,
                            document_metadata=current_input.document_metadata,
                            images=current_input.images,
                            tables=current_input.tables,
                            success=True,
                        )
                        processing_result = processor.process(pseudo_extraction)

                    # Collect errors and warnings
                    all_errors.extend(processing_result.errors)
                    all_warnings.extend(processing_result.warnings)

                    if not processing_result.success:
                        # Check if processor is optional
                        if processor.is_optional():
                            self.logger.warning(
                                f"Optional processor {processor_name} failed, continuing"
                            )
                        else:
                            self.logger.error(f"Required processor {processor_name} failed")
                            return PipelineResult(
                                source_file=file_path,
                                extraction_result=extraction_result,
                                processing_result=processing_result,
                                success=False,
                                failed_stage=ProcessingStage.CONTEXT_LINKING,  # Generic processing stage
                                started_at=start_time,
                                completed_at=datetime.now(timezone.utc),
                                all_errors=tuple(all_errors),
                                all_warnings=tuple(all_warnings),
                            )

                    # Use output as input for next processor
                    current_input = processing_result

                except Exception as e:
                    error_msg = f"Processor {processor_name} raised exception: {e}"
                    all_errors.append(error_msg)
                    self.logger.exception(error_msg)

                    if not processor.is_optional():
                        return PipelineResult(
                            source_file=file_path,
                            extraction_result=extraction_result,
                            processing_result=processing_result,
                            success=False,
                            failed_stage=ProcessingStage.CONTEXT_LINKING,
                            started_at=start_time,
                            completed_at=datetime.now(timezone.utc),
                            all_errors=tuple(all_errors),
                            all_warnings=tuple(all_warnings),
                        )

            # If no processors, create processing result from extraction result
            if processing_result is None:
                processing_result = ProcessingResult(
                    content_blocks=extraction_result.content_blocks,
                    document_metadata=extraction_result.document_metadata,
                    images=extraction_result.images,
                    tables=extraction_result.tables,
                    processing_stage=ProcessingStage.EXTRACTION,
                    success=True,
                )

        except Exception as e:
            error_msg = f"Processing stage failed: {e}"
            all_errors.append(error_msg)
            self.logger.exception(error_msg)

            return PipelineResult(
                source_file=file_path,
                extraction_result=extraction_result,
                processing_result=processing_result,
                success=False,
                failed_stage=ProcessingStage.CONTEXT_LINKING,
                started_at=start_time,
                completed_at=datetime.now(timezone.utc),
                all_errors=tuple(all_errors),
                all_warnings=tuple(all_warnings),
            )

        # Stage 4: Formatting
        self._report_progress(progress_callback, "formatting", 70.0, "Formatting output")

        formatted_outputs = []

        for i, formatter in enumerate(self._formatters):
            formatter_type = formatter.get_format_type()
            self.logger.info(f"Running formatter: {formatter_type}")

            # Calculate progress (70% to 90% range)
            progress = 70.0 + (20.0 * (i + 1) / max(len(self._formatters), 1))
            self._report_progress(
                progress_callback, "formatting", progress, f"Generating {formatter_type} output"
            )

            try:
                formatted_output = formatter.format(processing_result)

                # Collect errors and warnings
                all_errors.extend(formatted_output.errors)
                all_warnings.extend(formatted_output.warnings)

                if formatted_output.success:
                    formatted_outputs.append(formatted_output)
                else:
                    self.logger.warning(
                        f"Formatter {formatter_type} failed: {formatted_output.errors}"
                    )

            except Exception as e:
                error_msg = f"Formatter {formatter_type} raised exception: {e}"
                all_errors.append(error_msg)
                self.logger.exception(error_msg)
                # Continue with other formatters

        # Complete
        self._report_progress(progress_callback, "complete", 100.0, "Processing complete")

        completed_time = datetime.now(timezone.utc)
        duration = (completed_time - start_time).total_seconds()

        self.logger.info(f"Pipeline completed successfully in {duration:.2f}s: {file_path}")

        return PipelineResult(
            source_file=file_path,
            extraction_result=extraction_result,
            processing_result=processing_result,
            formatted_outputs=tuple(formatted_outputs),
            success=True,
            started_at=start_time,
            completed_at=completed_time,
            duration_seconds=duration,
            all_errors=tuple(all_errors),
            all_warnings=tuple(all_warnings),
        )
