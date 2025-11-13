"""
Logging framework for structured logging with performance timing.

Provides:
- Structured JSON logging for machine parsing
- Performance timing decorators and context managers
- Correlation ID tracking for request tracing
- Multi-sink support (console, file, rotating file)
- Thread-safe logging
- YAML configuration loading

Design Principles:
- Minimal performance overhead (<5%)
- Safe for parallel execution
- Rich context data in logs
- Configurable log levels and handlers

Example:
    >>> from infrastructure import get_logger, timed, timer
    >>> logger = get_logger(__name__)
    >>>
    >>> @timed(logger)
    >>> def extract_file(path):
    >>>     logger.info("Extracting", file=path)
    >>>     # ... extraction logic ...
    >>>
    >>> with timer(logger, "batch_processing"):
    >>>     for file in files:
    >>>         extract_file(file)
"""

import json
import logging
import logging.handlers
import time
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import yaml

# Context variable for correlation ID (thread-safe)
_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

# Cache for loggers (avoid recreating)
_loggers: dict[str, logging.Logger] = {}


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs JSON structured logs.

    Includes standard fields plus any extra fields from log records.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add correlation ID if present
        correlation_id = _correlation_id.get()
        if correlation_id:
            log_data["correlation_id"] = correlation_id

        # Add any extra fields from record
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
            ]:
                log_data[key] = value

        return json.dumps(log_data)


def get_logger(
    name: str,
    level: int = logging.INFO,
    json_format: bool = True,
    file_path: Optional[Path] = None,
    console: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Get or create a logger with specified configuration.

    Loggers are cached - calling with same name returns same instance.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON structured logging (default: True)
        file_path: Optional file path for file logging
        console: Enable console logging (default: False)
        max_bytes: Max bytes per log file before rotation (default: 10MB)
        backup_count: Number of backup log files to keep (default: 5)

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing file", file="document.docx", size=1024)
    """
    # Return cached logger if exists
    if name in _loggers:
        return _loggers[name]

    # Create new logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Don't propagate to root logger

    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Add file handler if path specified
    if file_path:
        # Use rotating file handler to manage log size
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Cache logger
    _loggers[name] = logger

    return logger


@contextmanager
def correlation_context(correlation_id: str):
    """
    Context manager for setting correlation ID for request tracking.

    The correlation ID is automatically included in all log messages
    within the context. Uses context variables for thread-safety.

    Args:
        correlation_id: Unique identifier for this request/operation

    Example:
        >>> logger = get_logger(__name__)
        >>> with correlation_context("req-12345"):
        >>>     logger.info("Processing request")  # Includes correlation_id
        >>>     process_file()
    """
    token = _correlation_id.set(correlation_id)
    try:
        yield
    finally:
        _correlation_id.reset(token)


@contextmanager
def timer(logger: logging.Logger, operation: str, level: int = logging.INFO):
    """
    Context manager for timing operations.

    Automatically logs duration when context exits.

    Args:
        logger: Logger instance to use
        operation: Name of operation being timed
        level: Log level (default: INFO)

    Example:
        >>> with timer(logger, "file_extraction"):
        >>>     extract_content(file_path)
        # Logs: {"operation": "file_extraction", "duration_seconds": 1.234, ...}
    """
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        logger.log(
            level,
            f"Operation completed: {operation}",
            extra={"operation": operation, "duration_seconds": duration},
        )


def timed(logger: logging.Logger, level: int = logging.INFO) -> Callable:
    """
    Decorator for timing functions.

    Automatically logs function duration.

    Args:
        logger: Logger instance to use
        level: Log level (default: INFO)

    Returns:
        Decorated function

    Example:
        >>> @timed(logger)
        >>> def extract_document(path):
        >>>     # ... extraction logic ...
        >>>     return result
        # Logs: {"function": "extract_document", "duration_seconds": 2.345, ...}
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                logger.log(
                    level,
                    f"Function completed: {func.__name__}",
                    extra={"function": func.__name__, "duration_seconds": duration},
                )

        return wrapper

    return decorator


def configure_from_yaml(config_path: Path, logger_name: str) -> logging.Logger:
    """
    Configure logger from YAML configuration file.

    Args:
        config_path: Path to YAML configuration file
        logger_name: Name for the logger

    Returns:
        Configured logger instance

    Configuration format:
        logging:
          version: 1
          level: DEBUG
          format: json
          handlers:
            file:
              enabled: true
              path: logs/app.log
              max_bytes: 10485760
              backup_count: 5
            console:
              enabled: true

    Example:
        >>> logger = configure_from_yaml(Path("log_config.yaml"), __name__)
        >>> logger.info("Logger configured from YAML")
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    logging_config = config.get("logging", {})

    # Parse level
    level_str = logging_config.get("level", "INFO")
    level = getattr(logging, level_str, logging.INFO)

    # Parse format
    json_format = logging_config.get("format", "json") == "json"

    # Parse handlers
    handlers = logging_config.get("handlers", {})

    # File handler config
    file_config = handlers.get("file", {})
    file_enabled = file_config.get("enabled", False)
    file_path = Path(file_config.get("path", "app.log")) if file_enabled else None
    max_bytes = file_config.get("max_bytes", 10 * 1024 * 1024)
    backup_count = file_config.get("backup_count", 5)

    # Console handler config
    console_config = handlers.get("console", {})
    console = console_config.get("enabled", False)

    return get_logger(
        logger_name,
        level=level,
        json_format=json_format,
        file_path=file_path,
        console=console,
        max_bytes=max_bytes,
        backup_count=backup_count,
    )
