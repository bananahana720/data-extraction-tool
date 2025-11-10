"""
Configuration Manager - Centralized Configuration System

Provides centralized configuration management with:
- YAML/JSON file loading
- Pydantic validation for type safety
- Environment variable overrides
- Nested configuration access
- Thread-safe operations
- Graceful fallback to defaults

Design:
- Immutable configuration (reload creates new instance internally)
- Thread-safe using RLock
- Type coercion for environment variables
- Clear error messages for configuration issues

Example:
    >>> from infrastructure.config_manager import ConfigManager
    >>>
    >>> # Load with defaults
    >>> config = ConfigManager("config.yaml", defaults={"logging": {"level": "INFO"}})
    >>>
    >>> # Access nested values
    >>> log_level = config.get("logging.level")
    >>> extractor_config = config.get_section("extractors.docx")
    >>>
    >>> # Check existence
    >>> if config.has("extractors.pdf"):
    >>>     pdf_config = config.get_section("extractors.pdf")
"""

import copy
import json
import os
import threading
from pathlib import Path
from typing import Any, Optional, Type, Union

import yaml
from pydantic import BaseModel, ValidationError


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""

    pass


class ConfigManager:
    """
    Thread-safe configuration manager with validation and env var support.

    This class provides centralized configuration management for the data
    extraction tool. It supports loading from YAML/JSON files, validating
    against pydantic schemas, and overriding values with environment variables.

    Attributes:
        config_file: Path to configuration file
        env_prefix: Prefix for environment variable overrides
        schema: Optional pydantic model for validation

    Thread Safety:
        All public methods are thread-safe. Internal state is protected
        by a reentrant lock.
    """

    def __init__(
        self,
        config_file: Optional[Union[str, Path, dict]] = None,
        schema: Optional[Type[BaseModel]] = None,
        defaults: Optional[dict] = None,
        env_prefix: Optional[str] = None,
    ):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to YAML or JSON configuration file, or dict for testing.
                        If None, defaults to './config.yaml' in current working directory.
            schema: Optional pydantic model for validation
            defaults: Default configuration values
            env_prefix: Prefix for environment variable overrides (e.g., "DATA_EXTRACTOR")

        Raises:
            ConfigurationError: If file cannot be loaded or validation fails

        Example:
            >>> # With explicit path
            >>> config = ConfigManager(
            ...     "config.yaml",
            ...     schema=AppConfig,
            ...     defaults={"logging": {"level": "INFO"}},
            ...     env_prefix="DATA_EXTRACTOR"
            ... )
            >>> # With default path (./config.yaml)
            >>> config = ConfigManager()
            >>> # With dict (for testing)
            >>> config = ConfigManager({"key": "value"})
        """
        # Handle dict parameter (backward compatibility for test_installation.py)
        if isinstance(config_file, dict):
            self.config_file = None
            # Merge dict into defaults
            defaults = {**(defaults or {}), **config_file}
        # Handle None → default to current working directory config.yaml
        elif config_file is None:
            self.config_file = Path.cwd() / "config.yaml"
        else:
            self.config_file = Path(config_file)
        self.schema = schema
        self.env_prefix = env_prefix
        self._lock = threading.RLock()

        # Load configuration with priority: env vars > config file > defaults
        # Note: Load file first so env var path matching can work
        defaults_config = defaults or {}
        file_config = self._load_file()

        # Merge defaults and file config first
        self._config = self._merge_configs(defaults_config, file_config)

        # Now load env vars (which can use _config for path matching)
        env_config = self._load_env_vars()

        # Final merge with env vars taking highest priority
        self._config = self._merge_configs(self._config, env_config)

        # Validate if schema provided
        if self.schema:
            self._validate()

    def _load_file(self) -> dict:
        """
        Load configuration from file.

        Returns:
            Configuration dict from file, or empty dict if file doesn't exist

        Raises:
            ConfigurationError: If file exists but cannot be parsed
        """
        # Handle case where config_file is None (dict parameter was passed)
        if self.config_file is None:
            return {}

        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                content = f.read()

                # Empty file is OK
                if not content.strip():
                    return {}

                # Determine format from extension
                suffix = self.config_file.suffix.lower()

                if suffix in [".yaml", ".yml"]:
                    data = yaml.safe_load(content)
                    return data if data is not None else {}
                elif suffix == ".json":
                    return json.loads(content)
                else:
                    raise ConfigurationError(
                        f"Unsupported configuration file format: {suffix}. "
                        f"Supported formats: .yaml, .yml, .json"
                    )

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Failed to parse configuration file {self.config_file}: {e}")
        except PermissionError as e:
            raise ConfigurationError(
                f"Permission denied reading configuration file {self.config_file}: {e}"
            )
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration file {self.config_file}: {e}")

    def _load_env_vars(self) -> dict:
        """
        Load configuration overrides from environment variables.

        Environment variables are converted to nested dict keys using underscores:
        DATA_EXTRACTOR_LOGGING_LEVEL -> logging.level

        For keys with underscores (like skip_empty), tries multiple split patterns
        to find the best match against existing config structure.

        Returns:
            Configuration dict from environment variables
        """
        if not self.env_prefix:
            return {}

        env_config = {}
        prefix = f"{self.env_prefix}_"

        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue

            # Remove prefix and convert to lowercase path
            config_path = key[len(prefix) :].lower()

            # Type coercion for common types
            typed_value = self._coerce_type(value)

            # Try to intelligently split the path
            # For EXTRACTORS_DOCX_SKIP_EMPTY, we want to check if
            # extractors.docx.skip_empty exists vs extractors.docx.skip.empty
            parts = self._split_env_var_path(config_path)

            # Build nested dict
            current = env_config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = typed_value

        return env_config

    def _split_env_var_path(self, path: str) -> list[str]:
        """
        Split environment variable path intelligently.

        Tries to match against existing configuration structure to handle
        keys that contain underscores (like skip_empty).

        Args:
            path: Lowercase env var path (e.g., "extractors_docx_skip_empty")

        Returns:
            List of path components
        """
        # Simple split on underscores
        parts = path.split("_")

        # If we have loaded config, try to find better split
        # by checking if multi-word keys exist
        if hasattr(self, "_config") and self._config:
            # Try progressively longer combinations from the end
            # E.g., for [extractors, docx, skip, empty]:
            # Try: [..., skip_empty], [..., docx_skip, empty], etc.
            for i in range(len(parts) - 1, 0, -1):
                # Try combining last parts
                test_parts = parts[:i] + ["_".join(parts[i:])]
                if self._path_exists_in_config(test_parts):
                    return test_parts

        return parts

    def _path_exists_in_config(self, parts: list[str]) -> bool:
        """Check if a path exists in the current configuration."""
        current = self._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        return True

    def _coerce_type(self, value: str) -> Union[str, int, float, bool]:
        """
        Coerce string value to appropriate Python type.

        Args:
            value: String value from environment variable

        Returns:
            Coerced value (str, int, float, or bool)
        """
        # Empty string stays as string
        if not value:
            return value

        # Boolean - must check before numbers to avoid "0" being treated as int
        value_lower = value.lower()
        if value_lower in ("true", "yes"):
            return True
        if value_lower in ("false", "no"):
            return False

        # Integer (but not if it would lose info as float)
        if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            return int(value)

        # Float
        try:
            # Only treat as float if it has decimal point
            if "." in value:
                return float(value)
        except ValueError:
            pass

        # String (default)
        return value

    def _merge_configs(self, *configs: dict) -> dict:
        """
        Merge multiple configuration dicts with later configs taking precedence.

        Args:
            *configs: Variable number of configuration dicts

        Returns:
            Merged configuration dict
        """
        result = {}

        for config in configs:
            result = self._deep_merge(result, config)

        return result

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """
        Deep merge two dicts, with override taking precedence.

        Args:
            base: Base configuration dict
            override: Override configuration dict

        Returns:
            Merged dict
        """
        result = copy.deepcopy(base)

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)

        return result

    def _validate(self) -> None:
        """
        Validate configuration against pydantic schema.

        Raises:
            ConfigurationError: If validation fails
        """
        try:
            self.schema(**self._config)
        except ValidationError as e:
            raise ConfigurationError(f"Configuration validation failed:\n{e}")

    def _navigate_path(self, path: str) -> tuple[dict, list[str]]:
        """
        Navigate to a configuration path.

        Args:
            path: Dot-separated path (e.g., "extractors.docx.skip_empty")

        Returns:
            Tuple of (current_dict, remaining_parts)
        """
        parts = path.split(".")
        current = self._config

        for i, part in enumerate(parts[:-1]):
            if not isinstance(current, dict) or part not in current:
                return current, parts[i:]
            current = current[part]

        return current, [parts[-1]] if parts else []

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated path.

        Args:
            path: Dot-separated configuration path (e.g., "logging.level")
            default: Default value if path not found (default: None)

        Returns:
            Configuration value

        Raises:
            ConfigurationError: If path not found and no default provided

        Example:
            >>> config.get("logging.level")
            'INFO'
            >>> config.get("missing.key", default="fallback")
            'fallback'
        """
        with self._lock:
            current, remaining = self._navigate_path(path)

            if not remaining:
                return current

            final_key = remaining[0]

            if isinstance(current, dict) and final_key in current:
                return current[final_key]

            if default is not None:
                return default

            raise ConfigurationError(f"Configuration key not found: {path}")

    def get_section(self, path: str, default: Optional[dict] = None) -> dict:
        """
        Get configuration section as dict.

        Args:
            path: Dot-separated path to section
            default: Default dict if section not found

        Returns:
            Configuration section as dict

        Example:
            >>> config.get_section("extractors.docx")
            {'max_paragraph_length': 1000, 'skip_empty': True}
        """
        value = self.get(path, default=default)

        if not isinstance(value, dict):
            if default is not None:
                return default
            raise ConfigurationError(f"Configuration path {path} is not a section (dict)")

        return copy.deepcopy(value)

    def has(self, path: str) -> bool:
        """
        Check if configuration key exists.

        Args:
            path: Dot-separated configuration path

        Returns:
            True if key exists, False otherwise

        Example:
            >>> config.has("logging.level")
            True
            >>> config.has("nonexistent.key")
            False
        """
        try:
            self.get(path)
            return True
        except ConfigurationError:
            return False

    def get_all(self) -> dict:
        """
        Get complete configuration as dict.

        Returns:
            Copy of entire configuration dict

        Example:
            >>> all_config = config.get_all()
            >>> print(all_config.keys())
            dict_keys(['extractors', 'logging', 'general'])
        """
        with self._lock:
            return copy.deepcopy(self._config)

    def reload(self) -> None:
        """
        Reload configuration from file.

        This re-reads the configuration file and re-applies environment
        variable overrides. Useful for picking up configuration changes
        without restarting the application.

        Raises:
            ConfigurationError: If reload fails

        Example:
            >>> config.reload()
        """
        with self._lock:
            # Reload from file
            defaults = {}  # We don't store original defaults
            file_config = self._load_file()
            env_config = self._load_env_vars()

            self._config = self._merge_configs(defaults, file_config, env_config)

            # Re-validate if schema provided
            if self.schema:
                self._validate()

    def __repr__(self) -> str:
        """String representation of ConfigManager."""
        return (
            f"ConfigManager(file={self.config_file}, "
            f"env_prefix={self.env_prefix}, "
            f"schema={self.schema.__name__ if self.schema else None})"
        )
