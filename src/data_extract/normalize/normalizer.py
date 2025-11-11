"""Normalizer orchestrator for text normalization pipeline.

This module implements the main Normalizer class that orchestrates
text cleaning using TextCleaner and integrates with the pipeline architecture.

Key classes:
- Normalizer: Main orchestrator implementing PipelineStage[Document, Document]
"""

import structlog

from src.data_extract.core.exceptions import CriticalError, ProcessingError
from src.data_extract.core.models import Document, ProcessingContext
from src.data_extract.normalize.cleaning import TextCleaner
from src.data_extract.normalize.config import NormalizationConfig


class Normalizer:
    """Main normalization orchestrator (Story 2.1).

    Implements PipelineStage[Document, Document] protocol for integration
    with the modular pipeline architecture from Epic 1.

    Orchestrates:
    - Text cleaning via TextCleaner
    - Metadata enrichment with cleaning metrics
    - Error handling (ProcessingError, CriticalError)
    - Structured logging via structlog

    Type Contract: Document (raw text) → Document (cleaned text)

    Design:
    - Stateless: All state in ProcessingContext
    - Deterministic: Same input + config → same output
    - Auditable: All cleaning decisions logged

    Example:
        >>> config = NormalizationConfig()
        >>> normalizer = Normalizer(config)
        >>> context = ProcessingContext(config={}, logger=logger)
        >>> cleaned_doc = normalizer.process(raw_doc, context)
    """

    def __init__(self, config: NormalizationConfig):
        """Initialize Normalizer with configuration.

        Args:
            config: Normalization configuration
        """
        self.config = config
        self.text_cleaner = TextCleaner(config)

    def process(self, document: Document, context: ProcessingContext) -> Document:
        """Normalize document through all stages (PipelineStage protocol).

        Main pipeline method that cleans document text, enriches metadata,
        and logs cleaning metrics.

        Args:
            document: Document with raw text from extraction stage
            context: Processing context (config, logger, metrics)

        Returns:
            Document with cleaned text and enriched metadata

        Raises:
            ProcessingError: For recoverable errors (malformed text, etc.)
            CriticalError: For fatal errors (invalid config, missing dependencies)

        Pipeline Flow:
            1. Extract text from document
            2. Clean text using TextCleaner
            3. Aggregate CleaningResults
            4. Update document metadata
            5. Log metrics to context.logger
            6. Return normalized document

        Example:
            >>> doc = Document(
            ...     id="doc1",
            ...     text="Text ^^^^^ with noise",
            ...     metadata=metadata,
            ... )
            >>> cleaned = normalizer.process(doc, context)
            >>> assert "^^^^^" not in cleaned.text
        """
        try:
            # Get logger from context (or create fallback)
            logger = context.logger if context.logger else structlog.get_logger()

            # Extract text from document
            raw_text = document.text

            # Clean text using TextCleaner
            cleaned_text, cleaning_result = self.text_cleaner.clean_text(
                raw_text, doc_type=document.metadata.document_type
            )

            # Log cleaning metrics
            logger.info(
                "text_cleaning_complete",
                document_id=document.id,
                original_length=cleaning_result.original_length,
                cleaned_length=cleaning_result.cleaned_length,
                artifacts_removed=cleaning_result.artifacts_removed,
                whitespace_normalized=cleaning_result.whitespace_normalized,
            )

            # Update context metrics (accumulate)
            context.metrics["total_artifacts_removed"] = (
                context.metrics.get("total_artifacts_removed", 0)
                + cleaning_result.artifacts_removed
            )
            context.metrics["documents_normalized"] = (
                context.metrics.get("documents_normalized", 0) + 1
            )

            # Update document metadata with cleaning summary
            updated_metadata = document.metadata.model_copy(deep=True)
            updated_metadata.quality_scores["cleaning_artifacts_removed"] = float(
                cleaning_result.artifacts_removed
            )
            updated_metadata.quality_scores["cleaning_length_reduction"] = float(
                cleaning_result.original_length - cleaning_result.cleaned_length
            )

            # Add quality flags if significant changes were made
            if cleaning_result.artifacts_removed > 10:
                updated_metadata.quality_flags.append("high_ocr_artifact_count")

            # Create and return normalized document
            normalized_document = document.model_copy(
                update={
                    "text": cleaned_text,
                    "metadata": updated_metadata,
                }
            )

            return normalized_document

        except Exception as e:
            # Catch unexpected errors and wrap in ProcessingError
            error_msg = f"Text cleaning failed for document {document.id}: {e}"
            logger.error("text_cleaning_error", document_id=document.id, error=str(e))

            # Determine if error is recoverable
            if isinstance(e, (CriticalError, KeyboardInterrupt, SystemExit)):
                # Re-raise critical errors
                raise

            # Wrap as ProcessingError (recoverable - log, skip, continue batch)
            raise ProcessingError(error_msg) from e


class NormalizerFactory:
    """Factory for creating Normalizer instances with different configurations.

    Provides convenience methods for common normalization scenarios.

    Example:
        >>> # Default normalizer
        >>> normalizer = NormalizerFactory.create_default()
        >>>
        >>> # Custom normalizer
        >>> config = NormalizationConfig(remove_ocr_artifacts=False)
        >>> normalizer = NormalizerFactory.create(config)
    """

    @staticmethod
    def create_default() -> Normalizer:
        """Create normalizer with default configuration.

        Returns:
            Normalizer with default NormalizationConfig

        Example:
            >>> normalizer = NormalizerFactory.create_default()
            >>> assert normalizer.config.remove_ocr_artifacts is True
        """
        config = NormalizationConfig()
        return Normalizer(config)

    @staticmethod
    def create(config: NormalizationConfig) -> Normalizer:
        """Create normalizer with custom configuration.

        Args:
            config: Custom normalization configuration

        Returns:
            Normalizer with provided configuration

        Example:
            >>> config = NormalizationConfig(remove_headers_footers=False)
            >>> normalizer = NormalizerFactory.create(config)
            >>> assert normalizer.config.remove_headers_footers is False
        """
        return Normalizer(config)

    @staticmethod
    def create_from_yaml(yaml_path: str) -> Normalizer:
        """Create normalizer from YAML configuration file.

        Args:
            yaml_path: Path to YAML configuration file

        Returns:
            Normalizer with configuration loaded from YAML

        Example:
            >>> normalizer = NormalizerFactory.create_from_yaml(
            ...     "config/normalize/cleaning_rules.yaml"
            ... )
        """
        from pathlib import Path

        from src.data_extract.normalize.config import load_config

        config = load_config(yaml_path=Path(yaml_path))
        return Normalizer(config)
