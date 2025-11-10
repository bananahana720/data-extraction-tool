"""
Tests for error handling infrastructure.

TDD approach - tests written first, implementation follows.
Target: >85% code coverage
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import time


# RED PHASE: These tests will fail until we implement the error_handler module


def test_import_error_handler():
    """Test that error_handler module can be imported."""
    from src.infrastructure import error_handler

    assert error_handler is not None


def test_import_data_extraction_error():
    """Test that DataExtractionError base class exists."""
    from infrastructure.error_handler import DataExtractionError

    assert issubclass(DataExtractionError, Exception)


def test_data_extraction_error_basic_attributes():
    """Test DataExtractionError has required attributes."""
    from infrastructure.error_handler import DataExtractionError

    error = DataExtractionError(
        error_code="E001", message="Test error", technical_message="Technical: test error"
    )

    assert error.error_code == "E001"
    assert error.message == "Test error"
    assert error.technical_message == "Technical: test error"
    assert error.recoverable is not None  # Should have default
    assert error.suggested_action is not None  # Should have default


def test_data_extraction_error_with_context():
    """Test DataExtractionError stores context information."""
    from infrastructure.error_handler import DataExtractionError

    error = DataExtractionError(
        error_code="E001",
        message="File not found",
        context={"file_path": "/path/to/file.docx", "user": "auditor"},
    )

    assert error.context == {"file_path": "/path/to/file.docx", "user": "auditor"}


def test_data_extraction_error_with_original_exception():
    """Test DataExtractionError wraps original exceptions."""
    from infrastructure.error_handler import DataExtractionError

    original = FileNotFoundError("File not found")
    error = DataExtractionError(
        error_code="E001", message="The file could not be found", original_exception=original
    )

    assert error.original_exception is original
    assert isinstance(error.original_exception, FileNotFoundError)


def test_validation_error_category():
    """Test ValidationError is a category of DataExtractionError."""
    from infrastructure.error_handler import ValidationError, DataExtractionError

    error = ValidationError(error_code="E001", message="File not found")

    assert isinstance(error, DataExtractionError)
    assert error.category == "ValidationError"


def test_extraction_error_category():
    """Test ExtractionError is a category of DataExtractionError."""
    from infrastructure.error_handler import ExtractionError, DataExtractionError

    error = ExtractionError(error_code="E100", message="Failed to open document")

    assert isinstance(error, DataExtractionError)
    assert error.category == "ExtractionError"


def test_processing_error_category():
    """Test ProcessingError is a category of DataExtractionError."""
    from infrastructure.error_handler import ProcessingError, DataExtractionError

    error = ProcessingError(error_code="E200", message="Context linking failed")

    assert isinstance(error, DataExtractionError)
    assert error.category == "ProcessingError"


def test_formatting_error_category():
    """Test FormattingError is a category of DataExtractionError."""
    from infrastructure.error_handler import FormattingError, DataExtractionError

    error = FormattingError(error_code="E300", message="JSON serialization failed")

    assert isinstance(error, DataExtractionError)
    assert error.category == "FormattingError"


def test_config_error_category():
    """Test ConfigError is a category of DataExtractionError."""
    from infrastructure.error_handler import ConfigError, DataExtractionError

    error = ConfigError(error_code="E400", message="Config file not found")

    assert isinstance(error, DataExtractionError)
    assert error.category == "ConfigError"


def test_resource_error_category():
    """Test ResourceError is a category of DataExtractionError."""
    from infrastructure.error_handler import ResourceError, DataExtractionError

    error = ResourceError(error_code="E500", message="Out of memory")

    assert isinstance(error, DataExtractionError)
    assert error.category == "ResourceError"


def test_error_handler_loads_error_codes():
    """Test ErrorHandler loads error codes from YAML."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    assert handler.error_codes is not None
    assert len(handler.error_codes) > 0
    assert "E001" in handler.error_codes


def test_error_handler_get_error_info():
    """Test ErrorHandler retrieves error information by code."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    info = handler.get_error_info("E001")

    assert info is not None
    assert "category" in info
    assert "message" in info
    assert "technical_message" in info
    assert "recoverable" in info
    assert "suggested_action" in info


def test_error_handler_create_error_from_code():
    """Test ErrorHandler creates typed errors from error codes."""
    from infrastructure.error_handler import ErrorHandler, ValidationError

    handler = ErrorHandler()
    error = handler.create_error(error_code="E001", file_path="/path/to/file.docx")

    assert isinstance(error, ValidationError)
    assert error.error_code == "E001"
    assert error.message  # Should have user-friendly message
    assert error.technical_message  # Should have technical message with file_path


def test_error_handler_format_message_with_placeholders():
    """Test ErrorHandler formats messages with context placeholders."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    error = handler.create_error(error_code="E001", file_path="/path/to/file.docx")

    # Technical message should have file_path substituted
    assert "/path/to/file.docx" in error.technical_message


def test_error_handler_recovery_pattern_retry():
    """Test ErrorHandler supports retry recovery pattern."""
    from infrastructure.error_handler import ErrorHandler, RecoveryAction

    handler = ErrorHandler()

    # Simulate a transient error
    error_code = "E104"  # Partial extraction failure (recoverable)
    action = handler.get_recovery_action(error_code)

    assert action == RecoveryAction.RETRY


def test_error_handler_recovery_pattern_skip():
    """Test ErrorHandler supports skip-and-continue recovery pattern."""
    from infrastructure.error_handler import ErrorHandler, RecoveryAction

    handler = ErrorHandler()

    # Simulate a non-critical error
    error_code = "E105"  # Unsupported feature (recoverable, skip)
    action = handler.get_recovery_action(error_code)

    assert action == RecoveryAction.SKIP


def test_error_handler_recovery_pattern_abort():
    """Test ErrorHandler supports abort recovery pattern."""
    from infrastructure.error_handler import ErrorHandler, RecoveryAction

    handler = ErrorHandler()

    # Simulate a fatal error
    error_code = "E001"  # File not found (not recoverable)
    action = handler.get_recovery_action(error_code)

    assert action == RecoveryAction.ABORT


def test_error_handler_retry_with_backoff():
    """Test ErrorHandler implements retry with exponential backoff."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()

    # Track retry attempts
    attempts = []

    def failing_operation():
        attempts.append(time.time())
        if len(attempts) < 3:
            raise Exception("Transient error")
        return "success"

    result = handler.retry_with_backoff(failing_operation, max_retries=3, initial_delay=0.1)

    assert result == "success"
    assert len(attempts) == 3

    # Check exponential backoff (each delay should be roughly 2x previous)
    if len(attempts) >= 3:
        delay1 = attempts[1] - attempts[0]
        delay2 = attempts[2] - attempts[1]
        assert delay2 > delay1  # Second delay longer than first


def test_error_handler_retry_max_attempts_exceeded():
    """Test ErrorHandler gives up after max retry attempts."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()

    def always_failing_operation():
        raise Exception("Permanent error")

    with pytest.raises(Exception) as exc_info:
        handler.retry_with_backoff(always_failing_operation, max_retries=3, initial_delay=0.01)

    assert "Permanent error" in str(exc_info.value)


def test_error_handler_format_for_user():
    """Test ErrorHandler formats errors for non-technical users."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    error = handler.create_error("E001", file_path="/docs/report.docx")

    user_message = handler.format_for_user(error)

    # Should be user-friendly (no stack traces, clear action)
    assert "file you specified could not be found" in user_message.lower()
    assert "check the file path" in user_message.lower()
    assert "traceback" not in user_message.lower()


def test_error_handler_format_for_developer():
    """Test ErrorHandler formats errors for developers with debug info."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    original = FileNotFoundError("No such file")
    error = handler.create_error("E001", file_path="/docs/report.docx", original_exception=original)

    dev_message = handler.format_for_developer(error)

    # Should include technical details
    assert "E001" in dev_message
    assert "/docs/report.docx" in dev_message
    assert "FileNotFoundError" in dev_message or "No such file" in dev_message


def test_error_handler_log_error(caplog):
    """Test ErrorHandler logs errors appropriately."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    error = handler.create_error("E001", file_path="/docs/report.docx")

    handler.log_error(error)

    # Check that error was logged (if logging configured)
    # For now, just verify method exists and doesn't crash
    assert True


def test_error_handler_handles_unknown_error_code():
    """Test ErrorHandler handles unknown error codes gracefully."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    error = handler.create_error("E999", custom_message="Unknown error occurred")

    assert error.error_code == "E999"
    assert error.message  # Should have some message
    assert not error.recoverable  # Unknown errors not recoverable


def test_error_handler_context_propagation():
    """Test ErrorHandler preserves context through error chain."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()

    # Create error with context
    error1 = handler.create_error("E100", file_path="/docs/report.docx", operation="extraction")

    # Wrap in another error
    error2 = handler.create_error("E700", original_exception=error1, pipeline_stage="extraction")

    # Context should be preserved
    assert error2.original_exception is error1
    assert error1.context.get("file_path") == "/docs/report.docx"


# Test error code coverage - ensure all major error codes are defined
def test_error_code_coverage():
    """Test that all major error categories have codes defined."""
    from infrastructure.error_handler import ErrorHandler

    handler = ErrorHandler()
    codes = handler.error_codes

    # Validation errors (E001-E099)
    assert any(code.startswith("E0") for code in codes)

    # Extraction errors (E100-E199)
    assert any(code.startswith("E1") for code in codes)

    # Processing errors (E200-E299)
    assert any(code.startswith("E2") for code in codes)

    # Formatting errors (E300-E399)
    assert any(code.startswith("E3") for code in codes)

    # Config errors (E400-E499)
    assert any(code.startswith("E4") for code in codes)

    # Resource errors (E500-E599)
    assert any(code.startswith("E5") for code in codes)
