"""
Error Handling Infrastructure for Data Extraction System.

Provides standardized error handling with error codes, categories, recovery
patterns, and user-friendly messages for non-technical users.

Design Principles:
- Error codes (E001-E999) for documentation and troubleshooting
- Category-based exceptions for type-safe error handling
- Recovery patterns (retry, skip, abort) for automated error handling
- User-friendly messages for non-technical auditors
- Technical messages with context for developers
- Context propagation through error chain

Usage:
    >>> handler = ErrorHandler()
    >>> error = handler.create_error("E001", file_path="/docs/report.docx")
    >>> print(handler.format_for_user(error))
    The file you specified could not be found...

    >>> action = handler.get_recovery_action("E001")
    >>> if action == RecoveryAction.RETRY:
    >>>     handler.retry_with_backoff(operation, max_retries=3)
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar
import logging
import time
import traceback
import yaml


T = TypeVar("T")


class RecoveryAction(str, Enum):
    """Recovery actions for different error types."""

    RETRY = "retry"  # Retry operation with backoff
    SKIP = "skip"  # Skip and continue with next item
    ABORT = "abort"  # Abort operation, cannot recover


@dataclass
class DataExtractionError(Exception):
    """
    Base exception for all data extraction errors.

    All errors in the system inherit from this class, providing:
    - Standardized error codes
    - User-friendly and technical messages
    - Recovery information
    - Context propagation
    - Original exception chaining

    Attributes:
        error_code: Error code (E001-E999) for documentation
        message: User-friendly message for non-technical users
        technical_message: Technical message with details for developers
        category: Error category (ValidationError, ExtractionError, etc.)
        recoverable: Whether error can be recovered from
        suggested_action: What user should do to resolve
        context: Additional context information
        original_exception: Original exception if wrapping another error
    """

    error_code: str
    message: str
    technical_message: Optional[str] = None
    category: str = "DataExtractionError"
    recoverable: bool = False
    suggested_action: str = "Please contact support for assistance."
    context: dict[str, Any] = field(default_factory=dict)
    original_exception: Optional[Exception] = None

    def __str__(self) -> str:
        """Return user-friendly message."""
        return self.message

    def __repr__(self) -> str:
        """Return detailed representation for debugging."""
        return (
            f"{self.__class__.__name__}(error_code='{self.error_code}', "
            f"message='{self.message[:50]}...', recoverable={self.recoverable})"
        )


class ValidationError(DataExtractionError):
    """Errors during input validation (E001-E099)."""

    def __init__(self, **kwargs):
        super().__init__(category="ValidationError", **kwargs)


class ExtractionError(DataExtractionError):
    """Errors during content extraction (E100-E199)."""

    def __init__(self, **kwargs):
        super().__init__(category="ExtractionError", **kwargs)


class ProcessingError(DataExtractionError):
    """Errors during content processing (E200-E299)."""

    def __init__(self, **kwargs):
        super().__init__(category="ProcessingError", **kwargs)


class FormattingError(DataExtractionError):
    """Errors during output formatting (E300-E399)."""

    def __init__(self, **kwargs):
        super().__init__(category="FormattingError", **kwargs)


class ConfigError(DataExtractionError):
    """Errors in configuration (E400-E499)."""

    def __init__(self, **kwargs):
        super().__init__(category="ConfigError", **kwargs)


class ResourceError(DataExtractionError):
    """Resource errors - memory, disk, timeout (E500-E599)."""

    def __init__(self, **kwargs):
        super().__init__(category="ResourceError", **kwargs)


class ExternalServiceError(DataExtractionError):
    """Errors from external services like OCR (E600-E699)."""

    def __init__(self, **kwargs):
        super().__init__(category="ExternalServiceError", **kwargs)


class PipelineError(DataExtractionError):
    """Pipeline orchestration errors (E700-E799)."""

    def __init__(self, **kwargs):
        super().__init__(category="PipelineError", **kwargs)


class UnknownError(DataExtractionError):
    """Unknown or unexpected errors (E900-E999)."""

    def __init__(self, **kwargs):
        super().__init__(category="UnknownError", **kwargs)


# Map error code prefixes to exception classes
ERROR_CATEGORY_MAP = {
    "E0": ValidationError,
    "E1": ExtractionError,
    "E2": ProcessingError,
    "E3": FormattingError,
    "E4": ConfigError,
    "E5": ResourceError,
    "E6": ExternalServiceError,
    "E7": PipelineError,
    "E9": UnknownError,
}


class ErrorHandler:
    """
    Central error handling system.

    Responsibilities:
    - Load error code registry from YAML
    - Create typed exceptions from error codes
    - Determine recovery actions
    - Implement retry with backoff
    - Format errors for users and developers
    - Log errors appropriately

    Example:
        >>> handler = ErrorHandler()
        >>> error = handler.create_error("E001", file_path="/docs/report.docx")
        >>> print(handler.format_for_user(error))
        >>> if error.recoverable:
        >>>     handler.retry_with_backoff(operation)
    """

    def __init__(self, error_codes_path: Optional[Path] = None):
        """
        Initialize error handler.

        Args:
            error_codes_path: Path to error_codes.yaml (defaults to package location)
        """
        self.logger = logging.getLogger(__name__)

        # Load error codes from YAML
        if error_codes_path is None:
            error_codes_path = Path(__file__).parent / "error_codes.yaml"

        self.error_codes = self._load_error_codes(error_codes_path)

    def _load_error_codes(self, path: Path) -> dict[str, dict]:
        """
        Load error code registry from YAML file.

        Args:
            path: Path to error_codes.yaml

        Returns:
            Dictionary mapping error codes to error information
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load error codes from {path}: {e}")
            return {}

    def get_error_info(self, error_code: str) -> dict[str, Any]:
        """
        Get error information for a specific error code.

        Args:
            error_code: Error code (e.g., "E001")

        Returns:
            Dictionary with error information (category, message, etc.)
        """
        if error_code in self.error_codes:
            return self.error_codes[error_code]

        # Return default for unknown codes
        return {
            "category": "UnknownError",
            "message": "An unexpected error occurred.",
            "technical_message": f"Unknown error code: {error_code}",
            "recoverable": False,
            "suggested_action": "Please contact support.",
        }

    def create_error(
        self,
        error_code: str,
        original_exception: Optional[Exception] = None,
        custom_message: Optional[str] = None,
        **context,
    ) -> DataExtractionError:
        """
        Create a typed exception from an error code.

        Args:
            error_code: Error code (e.g., "E001")
            original_exception: Original exception if wrapping
            custom_message: Override default message
            **context: Context variables for message formatting

        Returns:
            Typed exception (ValidationError, ExtractionError, etc.)

        Example:
            >>> error = handler.create_error(
            >>>     "E001",
            >>>     file_path="/docs/report.docx",
            >>>     user="auditor"
            >>> )
        """
        info = self.get_error_info(error_code)

        # Determine exception class based on error code prefix
        exception_class = DataExtractionError
        for prefix, cls in ERROR_CATEGORY_MAP.items():
            if error_code.startswith(prefix):
                exception_class = cls
                break

        # Format messages with context
        message = custom_message or info.get("message", "An error occurred")
        technical_message = self._format_message(info.get("technical_message", message), context)

        return exception_class(
            error_code=error_code,
            message=message,
            technical_message=technical_message,
            recoverable=info.get("recoverable", False),
            suggested_action=info.get("suggested_action", "Please contact support."),
            context=context,
            original_exception=original_exception,
        )

    def _format_message(self, template: str, context: dict[str, Any]) -> str:
        """
        Format message template with context variables.

        Args:
            template: Message template with {placeholders}
            context: Context variables for substitution

        Returns:
            Formatted message
        """
        try:
            return template.format(**context)
        except KeyError:
            # If placeholder missing, return template as-is
            return template

    def get_recovery_action(self, error_code: str) -> RecoveryAction:
        """
        Determine recovery action for an error code.

        Args:
            error_code: Error code (e.g., "E001")

        Returns:
            RecoveryAction (RETRY, SKIP, or ABORT)

        Logic:
        - Recoverable errors with transient nature → RETRY (E104, E600, E601)
        - Recoverable errors that can be skipped → SKIP (E105, E203)
        - Non-recoverable errors → ABORT
        """
        info = self.get_error_info(error_code)

        if not info.get("recoverable", False):
            return RecoveryAction.ABORT

        # Transient errors that should be retried
        retry_codes = ["E104", "E600", "E601"]
        if error_code in retry_codes:
            return RecoveryAction.RETRY

        # Recoverable errors that can be skipped
        return RecoveryAction.SKIP

    def retry_with_backoff(
        self,
        operation: Callable[[], T],
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
    ) -> T:
        """
        Retry an operation with exponential backoff.

        Args:
            operation: Callable to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Multiplier for each retry (exponential backoff)

        Returns:
            Result from operation

        Raises:
            Exception: If all retries exhausted

        Example:
            >>> result = handler.retry_with_backoff(
            >>>     lambda: extract_file(path),
            >>>     max_retries=3,
            >>>     initial_delay=1.0
            >>> )
        """
        delay = initial_delay

        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    # Last attempt failed, re-raise
                    raise

                self.logger.warning(
                    f"Operation failed (attempt {attempt + 1}/{max_retries}), "
                    f"retrying in {delay}s: {e}"
                )

                time.sleep(delay)
                delay *= backoff_factor

        # Should not reach here, but for type checking
        raise RuntimeError("Retry logic error")

    def format_for_user(self, error: DataExtractionError) -> str:
        """
        Format error for non-technical users.

        Provides:
        - User-friendly message
        - Suggested action
        - No technical jargon or stack traces

        Args:
            error: Error to format

        Returns:
            User-friendly error message

        Example:
            >>> print(handler.format_for_user(error))
            The file you specified could not be found. Please check
            the file path and try again.
        """
        parts = [
            error.message,
        ]

        if error.suggested_action:
            parts.append(f"\n\nWhat to do: {error.suggested_action}")

        return "".join(parts)

    def format_for_developer(self, error: DataExtractionError) -> str:
        """
        Format error for developers with debug information.

        Provides:
        - Error code
        - Technical message
        - Context information
        - Original exception details
        - Stack trace if available

        Args:
            error: Error to format

        Returns:
            Detailed error message for debugging

        Example:
            >>> print(handler.format_for_developer(error))
            [E001] File not found: /docs/report.docx
            Context: user=auditor, operation=extraction
            Original: FileNotFoundError: No such file
        """
        parts = [f"[{error.error_code}] {error.technical_message or error.message}"]

        if error.context:
            context_str = ", ".join(f"{k}={v}" for k, v in error.context.items())
            parts.append(f"\nContext: {context_str}")

        if error.original_exception:
            parts.append(
                f"\nOriginal: {type(error.original_exception).__name__}: "
                f"{str(error.original_exception)}"
            )

            # Include traceback if available
            tb = traceback.format_exception(
                type(error.original_exception),
                error.original_exception,
                error.original_exception.__traceback__,
            )
            if tb:
                parts.append("\nTraceback:\n" + "".join(tb))

        return "".join(parts)

    def log_error(self, error: DataExtractionError, level: int = logging.ERROR) -> None:
        """
        Log error appropriately based on severity.

        Args:
            error: Error to log
            level: Logging level (default: ERROR)

        Logs:
        - Error code and category
        - Technical message
        - Context information
        - Original exception if present
        """
        log_data = {
            "error_code": error.error_code,
            "category": error.category,
            "message": error.technical_message or error.message,
            "recoverable": error.recoverable,
        }

        if error.context:
            log_data["context"] = error.context

        self.logger.log(level, f"Error: {log_data}")

        if error.original_exception:
            self.logger.log(
                level,
                f"Original exception: {error.original_exception}",
                exc_info=error.original_exception,
            )
