"""
Unit tests for ConfigManager - Configuration Management System

Tests verify:
- YAML/JSON file loading
- Pydantic validation
- Environment variable overrides
- Nested configuration access
- Thread-safe access
- Graceful fallback to defaults
- Error handling
"""

import json
import os
import sys
import tempfile
import threading
from pathlib import Path
from typing import Optional

import pytest
import yaml
from pydantic import BaseModel, Field, ValidationError

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from infrastructure import ConfigManager, ConfigurationError


# Pydantic models for validation testing
class ExtractorConfig(BaseModel):
    """Configuration for an individual extractor."""

    max_paragraph_length: Optional[int] = Field(None, ge=1)
    skip_empty: bool = True
    extract_styles: bool = True


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field("INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    output: str = Field("console", pattern="^(console|file|both)$")


class AppConfig(BaseModel):
    """Root application configuration."""

    extractors: dict[str, ExtractorConfig] = Field(default_factory=dict)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    general: dict = Field(default_factory=dict)


class TestConfigManagerBasicLoading:
    """Test basic configuration file loading."""

    def test_default_path_discovery_loads_values_correctly(self, tmp_path):
        """Test that None parameter discovers and loads ./config.yaml correctly"""
        # Arrange: Create config.yaml with nested structure
        config_file = tmp_path / "config.yaml"
        config_content = """app:
  name: TestApp
  version: "1.0"
logging:
  level: DEBUG
  file: app.log
"""
        config_file.write_text(config_content)

        # Change to temp directory
        original_cwd = Path.cwd()
        os.chdir(tmp_path)

        try:
            # Act: Create ConfigManager with None
            config = ConfigManager(config_file=None)

            # Assert: Nested values accessible
            assert config.get("app.name") == "TestApp"
            assert config.get("app.version") == "1.0"
            assert config.get("logging.level") == "DEBUG"
            assert config.get("logging.file") == "app.log"

            # Assert: Config file path is set correctly
            assert config.config_file == Path.cwd() / "config.yaml"
            assert config.config_file.exists()
        finally:
            os.chdir(original_cwd)

    def test_load_yaml_config_file(self, tmp_path):
        """Should load configuration from YAML file."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "extractors": {
                "docx": {"max_paragraph_length": 1000, "skip_empty": True, "extract_styles": True}
            },
            "logging": {"level": "INFO"},
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        assert manager.get("extractors.docx.max_paragraph_length") == 1000
        assert manager.get("extractors.docx.skip_empty") is True
        assert manager.get("logging.level") == "INFO"

    def test_load_json_config_file(self, tmp_path):
        """Should load configuration from JSON file."""
        config_file = tmp_path / "config.json"
        config_data = {
            "extractors": {"pdf": {"use_ocr": True, "dpi": 300}},
            "logging": {"level": "DEBUG"},
        }

        with open(config_file, "w") as f:
            json.dump(config_data, f)

        manager = ConfigManager(config_file)

        assert manager.get("extractors.pdf.use_ocr") is True
        assert manager.get("extractors.pdf.dpi") == 300
        assert manager.get("logging.level") == "DEBUG"

    def test_load_nonexistent_file_uses_defaults(self, tmp_path):
        """Should use defaults when config file doesn't exist."""
        config_file = tmp_path / "nonexistent.yaml"

        manager = ConfigManager(config_file)

        # Should not raise error
        assert manager.get("logging.level", default="INFO") == "INFO"

    def test_load_empty_yaml_file(self, tmp_path):
        """Should handle empty YAML file gracefully."""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        manager = ConfigManager(config_file)

        # Should work with defaults
        assert manager.get("any.key", default="default") == "default"

    def test_load_invalid_yaml_raises_error(self, tmp_path):
        """Should raise ConfigurationError for invalid YAML."""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")

        with pytest.raises(ConfigurationError, match="Failed to parse"):
            ConfigManager(config_file)


class TestConfigManagerPydanticValidation:
    """Test pydantic validation integration."""

    def test_validate_config_with_valid_data(self, tmp_path):
        """Should validate configuration against pydantic model."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "extractors": {
                "docx": {"max_paragraph_length": 1000, "skip_empty": True, "extract_styles": True}
            },
            "logging": {"level": "INFO", "format": "%(message)s", "output": "console"},
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file, schema=AppConfig)

        # Should validate without error
        assert manager.get("extractors.docx.max_paragraph_length") == 1000

    def test_validate_config_with_invalid_data_raises_error(self, tmp_path):
        """Should raise error when config doesn't match schema."""
        config_file = tmp_path / "config.yaml"
        config_data = {"logging": {"level": "INVALID_LEVEL"}}  # Not in allowed values

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        with pytest.raises(ConfigurationError, match="validation"):
            ConfigManager(config_file, schema=AppConfig)

    def test_validate_nested_config_section(self, tmp_path):
        """Should validate nested configuration sections."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "extractors": {"docx": {"max_paragraph_length": -100}}  # Invalid: must be >= 1
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        with pytest.raises(ConfigurationError):
            ConfigManager(config_file, schema=AppConfig)


class TestConfigManagerEnvironmentOverrides:
    """Test environment variable override functionality."""

    def test_env_var_overrides_config_value(self, tmp_path, monkeypatch):
        """Should override config value with environment variable."""
        config_file = tmp_path / "config.yaml"
        config_data = {"logging": {"level": "INFO"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Set environment variable
        monkeypatch.setenv("DATA_EXTRACTOR_LOGGING_LEVEL", "DEBUG")

        manager = ConfigManager(config_file, env_prefix="DATA_EXTRACTOR")

        # Should use env var value
        assert manager.get("logging.level") == "DEBUG"

    def test_env_var_creates_new_config_key(self, tmp_path, monkeypatch):
        """Should create config key from environment variable."""
        config_file = tmp_path / "config.yaml"
        config_data = {}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        monkeypatch.setenv("DATA_EXTRACTOR_NEW_KEY", "value")

        manager = ConfigManager(config_file, env_prefix="DATA_EXTRACTOR")

        # Should have new key from env var
        assert manager.get("new.key") == "value"

    def test_env_var_nested_path_override(self, tmp_path, monkeypatch):
        """Should handle nested paths in environment variable names."""
        config_file = tmp_path / "config.yaml"
        config_data = {"extractors": {"docx": {"skip_empty": True}}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        monkeypatch.setenv("DATA_EXTRACTOR_EXTRACTORS_DOCX_SKIP_EMPTY", "false")

        manager = ConfigManager(config_file, env_prefix="DATA_EXTRACTOR")

        # Should parse "false" as boolean
        assert manager.get("extractors.docx.skip_empty") is False

    def test_env_var_type_coercion(self, tmp_path, monkeypatch):
        """Should coerce environment variable string values to appropriate types."""
        config_file = tmp_path / "config.yaml"
        config_data = {}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        monkeypatch.setenv("DATA_EXTRACTOR_INT_VALUE", "42")
        monkeypatch.setenv("DATA_EXTRACTOR_FLOAT_VALUE", "3.14")
        monkeypatch.setenv("DATA_EXTRACTOR_BOOL_TRUE", "true")
        monkeypatch.setenv("DATA_EXTRACTOR_BOOL_FALSE", "false")

        manager = ConfigManager(config_file, env_prefix="DATA_EXTRACTOR")

        assert manager.get("int.value") == 42
        assert manager.get("float.value") == 3.14
        assert manager.get("bool.true") is True
        assert manager.get("bool.false") is False


class TestConfigManagerNestedAccess:
    """Test nested configuration access patterns."""

    def test_get_nested_value_with_dot_notation(self, tmp_path):
        """Should access nested values using dot notation."""
        config_file = tmp_path / "config.yaml"
        config_data = {"level1": {"level2": {"level3": {"value": "deep"}}}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        assert manager.get("level1.level2.level3.value") == "deep"

    def test_get_section_returns_dict(self, tmp_path):
        """Should return entire section as dict."""
        config_file = tmp_path / "config.yaml"
        config_data = {"extractors": {"docx": {"max_paragraph_length": 1000, "skip_empty": True}}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        section = manager.get_section("extractors.docx")

        assert isinstance(section, dict)
        assert section["max_paragraph_length"] == 1000
        assert section["skip_empty"] is True

    def test_get_nonexistent_key_with_default(self, tmp_path):
        """Should return default value for nonexistent key."""
        config_file = tmp_path / "config.yaml"
        config_data = {}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        assert manager.get("nonexistent.key", default="default") == "default"

    def test_get_nonexistent_key_without_default_raises_error(self, tmp_path):
        """Should raise error for nonexistent key without default."""
        config_file = tmp_path / "config.yaml"
        config_data = {}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        with pytest.raises(ConfigurationError, match="not found"):
            manager.get("nonexistent.key")

    def test_has_key_returns_true_for_existing_key(self, tmp_path):
        """Should return True for existing configuration key."""
        config_file = tmp_path / "config.yaml"
        config_data = {"existing": {"key": "value"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        assert manager.has("existing.key") is True
        assert manager.has("nonexistent.key") is False


class TestConfigManagerThreadSafety:
    """Test thread-safe configuration access."""

    def test_concurrent_reads_are_safe(self, tmp_path):
        """Should handle concurrent reads safely."""
        config_file = tmp_path / "config.yaml"
        config_data = {"test": {"value": 42}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)
        results = []
        errors = []

        def read_config():
            try:
                value = manager.get("test.value")
                results.append(value)
            except Exception as e:
                errors.append(e)

        # Create 10 threads that read concurrently
        threads = [threading.Thread(target=read_config) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # All reads should succeed with same value
        assert len(errors) == 0
        assert len(results) == 10
        assert all(v == 42 for v in results)

    def test_reload_during_concurrent_reads(self, tmp_path):
        """Should handle reload during concurrent reads safely."""
        config_file = tmp_path / "config.yaml"
        config_data = {"test": {"value": 1}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)
        errors = []

        def read_config():
            try:
                for _ in range(100):
                    manager.get("test.value", default=0)
            except Exception as e:
                errors.append(e)

        def reload_config():
            try:
                for i in range(10):
                    config_data = {"test": {"value": i}}
                    with open(config_file, "w") as f:
                        yaml.dump(config_data, f)
                    manager.reload()
            except Exception as e:
                errors.append(e)

        # Multiple readers + one reloader
        threads = [threading.Thread(target=read_config) for _ in range(5)]
        threads.append(threading.Thread(target=reload_config))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Should not raise any errors
        assert len(errors) == 0


class TestConfigManagerDefaults:
    """Test default configuration handling."""

    def test_provides_defaults_for_missing_config(self, tmp_path):
        """Should provide default configuration when file missing."""
        config_file = tmp_path / "nonexistent.yaml"

        defaults = {"logging": {"level": "INFO"}}

        manager = ConfigManager(config_file, defaults=defaults)

        assert manager.get("logging.level") == "INFO"

    def test_config_file_overrides_defaults(self, tmp_path):
        """Should override defaults with config file values."""
        config_file = tmp_path / "config.yaml"
        config_data = {"logging": {"level": "DEBUG"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        defaults = {"logging": {"level": "INFO", "format": "%(message)s"}}

        manager = ConfigManager(config_file, defaults=defaults)

        # File overrides defaults
        assert manager.get("logging.level") == "DEBUG"
        # But missing keys come from defaults
        assert manager.get("logging.format") == "%(message)s"

    def test_env_var_overrides_both_config_and_defaults(self, tmp_path, monkeypatch):
        """Should prioritize env vars over both config and defaults."""
        config_file = tmp_path / "config.yaml"
        config_data = {"logging": {"level": "DEBUG"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        defaults = {"logging": {"level": "INFO"}}

        monkeypatch.setenv("DATA_EXTRACTOR_LOGGING_LEVEL", "ERROR")

        manager = ConfigManager(config_file, defaults=defaults, env_prefix="DATA_EXTRACTOR")

        # Env var has highest priority
        assert manager.get("logging.level") == "ERROR"


class TestConfigManagerUtilityMethods:
    """Test utility methods and edge cases."""

    def test_get_all_returns_complete_config(self, tmp_path):
        """Should return complete configuration as dict."""
        config_file = tmp_path / "config.yaml"
        config_data = {"section1": {"key1": "value1"}, "section2": {"key2": "value2"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        all_config = manager.get_all()

        assert all_config["section1"]["key1"] == "value1"
        assert all_config["section2"]["key2"] == "value2"

    def test_reload_updates_configuration(self, tmp_path):
        """Should reload configuration from file."""
        config_file = tmp_path / "config.yaml"

        # Initial config
        config_data = {"value": 1}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)
        assert manager.get("value") == 1

        # Update file
        config_data = {"value": 2}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager.reload()
        assert manager.get("value") == 2

    def test_to_dict_returns_copy_not_reference(self, tmp_path):
        """Should return copy of config, not reference."""
        config_file = tmp_path / "config.yaml"
        config_data = {"test": "value"}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        manager = ConfigManager(config_file)

        config_dict = manager.get_all()
        config_dict["test"] = "modified"

        # Original should not be affected
        assert manager.get("test") == "value"


class TestConfigManagerNoneParameter:
    """Test None parameter handling for default path behavior."""

    def test_config_manager_accepts_none_parameter_with_existing_file(self, tmp_path):
        """Should load ./config.yaml when None passed and file exists."""
        # Arrange: Create config.yaml in temp directory
        config_file = tmp_path / "config.yaml"
        config_file.write_text("key: value\n")

        # Change to temp directory so Path.cwd() points there
        original_cwd = Path.cwd()
        os.chdir(tmp_path)

        try:
            # Act: Pass None to ConfigManager
            config = ConfigManager(config_file=None)

            # Assert: Config loaded from ./config.yaml
            assert config.get("key") == "value"
            assert config.config_file == Path.cwd() / "config.yaml"
        finally:
            os.chdir(original_cwd)

    def test_none_parameter_missing_config_uses_defaults(self, tmp_path):
        """Should use defaults when None passed and ./config.yaml doesn't exist."""
        # Arrange: No config.yaml in temp directory
        original_cwd = Path.cwd()
        os.chdir(tmp_path)

        try:
            # Act: Pass None with defaults
            config = ConfigManager(config_file=None, defaults={"fallback": "default_value"})

            # Assert: Falls back to defaults
            assert config.get("fallback") == "default_value"
            assert config.config_file == Path.cwd() / "config.yaml"
        finally:
            os.chdir(original_cwd)

    def test_dict_parameter_backward_compatibility(self):
        """Should accept dict parameter for backward compatibility."""
        # Arrange: Pass dict instead of file path
        test_config = {"test_key": "test_value", "nested": {"key": "value"}}

        # Act: Pass dict to ConfigManager
        config = ConfigManager(config_file=test_config)

        # Assert: Config contains dict values
        assert config.get("test_key") == "test_value"
        assert config.get("nested.key") == "value"
        assert config.config_file is None  # No file when dict passed


class TestConfigManagerErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_json_raises_error(self, tmp_path):
        """Should raise error for invalid JSON."""
        config_file = tmp_path / "invalid.json"
        config_file.write_text("{invalid json")

        with pytest.raises(ConfigurationError, match="Failed to parse"):
            ConfigManager(config_file)

    def test_unsupported_file_format_raises_error(self, tmp_path):
        """Should raise error for unsupported file format."""
        config_file = tmp_path / "config.txt"
        config_file.write_text("some content")

        with pytest.raises(ConfigurationError, match="Unsupported"):
            ConfigManager(config_file)

    @pytest.mark.skipif(
        sys.platform == "win32", reason="File permission test not supported on Windows"
    )
    def test_permission_error_provides_clear_message(self, tmp_path):
        """Should provide clear error message for permission errors."""
        config_file = tmp_path / "config.yaml"
        config_data = {"test": "value"}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Make file unreadable (Unix-only)
        try:
            os.chmod(config_file, 0o000)

            with pytest.raises(ConfigurationError, match="[Pp]ermission"):
                ConfigManager(config_file)
        finally:
            # Restore permissions for cleanup
            os.chmod(config_file, 0o644)
