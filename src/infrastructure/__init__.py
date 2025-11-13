"""
Infrastructure components for the extraction system.

This package provides cross-cutting concerns like logging, configuration,
error handling, and progress tracking.
"""

from .config_manager import ConfigManager, ConfigurationError
from .error_handler import (
    ConfigError,
    DataExtractionError,
    ErrorHandler,
    ExternalServiceError,
    ExtractionError,
    FormattingError,
    PipelineError,
    ProcessingError,
    RecoveryAction,
    ResourceError,
    UnknownError,
    ValidationError,
)
from .progress_tracker import ProgressTracker

# Logging framework imports (when implemented)
try:
    from .logging_framework import (
        configure_from_yaml,
        correlation_context,
        get_logger,
        timed,
        timer,
    )

    __all__ = [
        "ConfigManager",
        "ConfigurationError",
        "DataExtractionError",
        "ValidationError",
        "ExtractionError",
        "ProcessingError",
        "FormattingError",
        "ConfigError",
        "ResourceError",
        "ExternalServiceError",
        "PipelineError",
        "UnknownError",
        "ErrorHandler",
        "RecoveryAction",
        "ProgressTracker",
        "get_logger",
        "configure_from_yaml",
        "correlation_context",
        "timer",
        "timed",
    ]
except ImportError:
    # Logging framework not yet implemented
    __all__ = [
        "ConfigManager",
        "ConfigurationError",
        "DataExtractionError",
        "ValidationError",
        "ExtractionError",
        "ProcessingError",
        "FormattingError",
        "ConfigError",
        "ResourceError",
        "ExternalServiceError",
        "PipelineError",
        "UnknownError",
        "ErrorHandler",
        "RecoveryAction",
        "ProgressTracker",
    ]
