"""
Core interface contracts for the extraction system.

These abstract base classes define the contracts that all modules must follow.
This enables modularity - new extractors, processors, and formatters can be
added without modifying the core pipeline.

Design Principles:
- Clear contracts with documented expectations
- Type-safe with full type hints
- Minimal required methods, optional hooks for advanced features
- Error handling built into contracts
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from .models import (
    ExtractionResult,
    FormattedOutput,
    ProcessingResult,
)


class BaseExtractor(ABC):
    """
    Abstract base class for all format-specific extractors.

    Each file format (DOCX, PDF, PPTX, etc.) implements this interface.
    The pipeline uses these extractors without knowing format-specific details.

    Contract:
    - extract() must return ExtractionResult with success flag
    - If extraction fails, return ExtractionResult with success=False and errors
    - Never raise exceptions for file-level failures (network issues, corrupted files)
    - DO raise exceptions for programming errors (bugs, invalid arguments)
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize extractor with optional configuration.

        Args:
            config: Format-specific configuration options
        """
        self.config = config or {}

    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract content from file.

        This is the core method every extractor must implement.

        Args:
            file_path: Path to file to extract

        Returns:
            ExtractionResult with content blocks and metadata

        Note:
            - If extraction fails, return ExtractionResult with success=False
            - Populate errors tuple with descriptive error messages
            - Partial extraction is acceptable (return what you can)
        """
        pass

    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """
        Check if this extractor can handle the given file.

        Args:
            file_path: Path to file to check

        Returns:
            True if this extractor can handle the file
        """
        pass

    def supports_streaming(self) -> bool:
        """
        Whether this extractor can process files incrementally.

        Streaming extractors can handle very large files without loading
        entire file into memory. Not all formats support this.

        Returns:
            True if streaming is supported
        """
        return False

    def validate_file(self, file_path: Path) -> tuple[bool, list[str]]:
        """
        Pre-extraction validation.

        Optional hook for format-specific validation before extraction.
        This can catch issues early and provide better error messages.

        Args:
            file_path: Path to file to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
        elif not file_path.is_file():
            errors.append(f"Path is not a file: {file_path}")
        elif file_path.stat().st_size == 0:
            errors.append(f"File is empty: {file_path}")

        return (len(errors) == 0, errors)

    def get_format_name(self) -> str:
        """
        Return human-readable format name.

        Returns:
            Format name (e.g., "Microsoft Word", "PDF", "PowerPoint")
        """
        return self.__class__.__name__.replace("Extractor", "")

    def get_supported_extensions(self) -> list[str]:
        """
        Return list of supported file extensions.

        Returns:
            List of extensions (e.g., [".docx", ".doc"])
        """
        return []


class BaseProcessor(ABC):
    """
    Abstract base class for content processors.

    Processors enrich extracted content. Examples:
    - Context linking (create document tree)
    - Metadata aggregation (compute statistics)
    - Image analysis (detect image types)
    - Quality validation (score extraction quality)

    Contract:
    - process() takes ExtractionResult, returns ProcessingResult
    - Processors are composable (output of one is input to next)
    - Processors declare dependencies (which processors must run first)
    - Failed processing returns ProcessingResult with success=False
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize processor with optional configuration.

        Args:
            config: Processor-specific configuration options
        """
        self.config = config or {}

    @abstractmethod
    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """
        Process extracted content.

        Args:
            extraction_result: Result from extraction stage

        Returns:
            ProcessingResult with enriched content

        Note:
            - If processing fails, return ProcessingResult with success=False
            - Partial processing is acceptable (return what you can)
            - Preserve original content_blocks, add enrichments to metadata
        """
        pass

    def get_dependencies(self) -> list[str]:
        """
        Return list of processors that must run before this one.

        This enables the pipeline to order processors correctly.
        Use processor class names (e.g., ["ContextLinker", "MetadataAggregator"]).

        Returns:
            List of processor class names
        """
        return []

    def get_processor_name(self) -> str:
        """
        Return human-readable processor name.

        Returns:
            Processor name
        """
        return self.__class__.__name__

    def is_optional(self) -> bool:
        """
        Whether this processor can be skipped if it fails.

        Optional processors don't block the pipeline if they fail.

        Returns:
            True if processor is optional
        """
        return False


class BaseFormatter(ABC):
    """
    Abstract base class for output formatters.

    Formatters convert processed content to AI-ready formats.
    Examples: JSON, Markdown, chunked text, etc.

    Contract:
    - format() takes ProcessingResult, returns FormattedOutput
    - Formatters are independent (can run in parallel)
    - Failed formatting returns FormattedOutput with success=False
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize formatter with optional configuration.

        Args:
            config: Formatter-specific configuration options
        """
        self.config = config or {}

    @abstractmethod
    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """
        Convert processed content to target format.

        Args:
            processing_result: Result from processing stage

        Returns:
            FormattedOutput with formatted content

        Note:
            - If formatting fails, return FormattedOutput with success=False
            - Include additional files (images, metadata) in additional_files
        """
        pass

    @abstractmethod
    def get_format_type(self) -> str:
        """
        Return format type identifier.

        This is used for file extensions and format selection.

        Returns:
            Format type (e.g., "json", "markdown", "chunked")
        """
        pass

    def supports_streaming(self) -> bool:
        """
        Whether this formatter can write output incrementally.

        Streaming formatters can handle very large documents without loading
        entire output into memory.

        Returns:
            True if streaming is supported
        """
        return False

    def get_file_extension(self) -> str:
        """
        Return appropriate file extension for this format.

        Returns:
            File extension (e.g., ".json", ".md")
        """
        format_type = self.get_format_type()
        return f".{format_type}"

    def get_formatter_name(self) -> str:
        """
        Return human-readable formatter name.

        Returns:
            Formatter name
        """
        return self.__class__.__name__.replace("Formatter", "")


class BasePipeline(ABC):
    """
    Abstract base class for extraction pipelines.

    Pipelines orchestrate the extraction workflow:
    1. Detect file format
    2. Extract content
    3. Process content (multiple stages)
    4. Format output
    5. Export results

    Contract:
    - process_file() takes file path, returns PipelineResult
    - Pipeline manages error propagation and recovery
    - Pipeline tracks progress and metrics
    """

    @abstractmethod
    def process_file(self, file_path: Path) -> "PipelineResult":
        """
        Process a single file through the complete pipeline.

        Args:
            file_path: Path to file to process

        Returns:
            PipelineResult with results from all stages
        """
        pass

    @abstractmethod
    def register_extractor(self, format_type: str, extractor: BaseExtractor) -> None:
        """
        Register a format-specific extractor.

        Args:
            format_type: Format identifier (e.g., "docx", "pdf")
            extractor: Extractor instance
        """
        pass

    @abstractmethod
    def add_processor(self, processor: BaseProcessor) -> None:
        """
        Add a processor to the pipeline.

        Processors are automatically ordered based on dependencies.

        Args:
            processor: Processor instance
        """
        pass

    @abstractmethod
    def add_formatter(self, formatter: BaseFormatter) -> None:
        """
        Add an output formatter to the pipeline.

        Multiple formatters can be added to generate multiple output formats.

        Args:
            formatter: Formatter instance
        """
        pass


# Import PipelineResult here to avoid circular import
from .models import PipelineResult  # noqa: E402
