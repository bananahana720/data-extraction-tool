"""Normalization configuration models and loaders.

This module defines configuration for text normalization pipeline:
- NormalizationConfig: Main configuration model with text cleaning settings
- load_config(): Configuration cascade loader (CLI > env > YAML > defaults)

Configuration cascade precedence (highest to lowest):
1. CLI flags (passed as kwargs)
2. Environment variables (DATA_EXTRACT_NORMALIZE_* prefix)
3. YAML configuration file
4. Hardcoded defaults
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class NormalizationConfig(BaseModel):
    """Configuration for text normalization pipeline.

    Defines settings for text cleaning, artifact removal, whitespace
    normalization, and header/footer detection.

    Attributes:
        remove_ocr_artifacts: Enable OCR artifact removal (AC-2.1.1)
        remove_headers_footers: Enable header/footer removal (AC-2.1.3)
        normalize_whitespace: Enable whitespace normalization (AC-2.1.2)
        header_repetition_threshold: Min pages for header/footer detection (AC-2.1.4)
        whitespace_max_consecutive_newlines: Max consecutive newlines (AC-2.1.2)
        ocr_artifact_patterns_file: Path to OCR artifact patterns YAML
        header_footer_patterns_file: Path to header/footer patterns YAML
    """

    model_config = ConfigDict(frozen=False)

    # Text Cleaning Flags (Story 2.1)
    remove_ocr_artifacts: bool = Field(
        default=True, description="Enable OCR artifact removal (AC-2.1.1)"
    )
    remove_headers_footers: bool = Field(
        default=True, description="Enable header/footer removal (AC-2.1.3)"
    )
    normalize_whitespace: bool = Field(
        default=True, description="Enable whitespace normalization (AC-2.1.2)"
    )

    # Thresholds
    header_repetition_threshold: int = Field(
        default=3,
        ge=1,
        description="Min pages for header/footer detection (AC-2.1.4)",
    )
    whitespace_max_consecutive_newlines: int = Field(
        default=2, ge=1, description="Max consecutive newlines (AC-2.1.2)"
    )

    # Configuration file paths
    ocr_artifact_patterns_file: Optional[Path] = Field(
        default=None, description="Path to OCR artifact patterns YAML (optional)"
    )
    header_footer_patterns_file: Optional[Path] = Field(
        default=None, description="Path to header/footer patterns YAML (optional)"
    )

    @field_validator("ocr_artifact_patterns_file", "header_footer_patterns_file")
    @classmethod
    def validate_file_paths(cls, v: Optional[Path]) -> Optional[Path]:
        """Validate that configuration file paths exist if specified.

        Args:
            v: Path to validate

        Returns:
            Validated path or None

        Raises:
            ValueError: If path is specified but does not exist
        """
        if v is not None and not v.exists():
            raise ValueError(f"Configuration file not found: {v}")
        return v


def load_config(
    yaml_path: Optional[Path] = None,
    env_vars: Optional[Dict[str, Any]] = None,
    cli_flags: Optional[Dict[str, Any]] = None,
) -> NormalizationConfig:
    """Load normalization configuration with cascade precedence.

    Configuration cascade (highest to lowest precedence):
    1. CLI flags (cli_flags parameter)
    2. Environment variables (DATA_EXTRACT_NORMALIZE_* prefix)
    3. YAML configuration file (yaml_path parameter)
    4. Hardcoded defaults (NormalizationConfig defaults)

    Args:
        yaml_path: Path to YAML configuration file (optional)
        env_vars: Environment variables dict (defaults to os.environ)
        cli_flags: CLI flags dict (highest precedence)

    Returns:
        NormalizationConfig: Merged configuration with cascade precedence

    Raises:
        ValueError: If YAML file is invalid or file paths don't exist

    Examples:
        >>> # Load with defaults only
        >>> config = load_config()

        >>> # Load with YAML file
        >>> config = load_config(yaml_path=Path("config/normalize/cleaning_rules.yaml"))

        >>> # Load with CLI overrides
        >>> config = load_config(
        ...     yaml_path=Path("config/normalize/cleaning_rules.yaml"),
        ...     cli_flags={"remove_ocr_artifacts": False}
        ... )
    """
    # Start with empty config dict
    merged_config: Dict[str, Any] = {}

    # Layer 4: Hardcoded defaults (handled by Pydantic defaults)

    # Layer 3: YAML configuration file
    if yaml_path is not None and yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f) or {}
            merged_config.update(yaml_config)

    # Layer 2: Environment variables (DATA_EXTRACT_NORMALIZE_* prefix)
    if env_vars is None:
        env_vars = dict(os.environ)

    env_prefix = "DATA_EXTRACT_NORMALIZE_"
    for key, value in env_vars.items():
        if key.startswith(env_prefix):
            # Convert DATA_EXTRACT_NORMALIZE_REMOVE_OCR_ARTIFACTS -> remove_ocr_artifacts
            config_key = key[len(env_prefix) :].lower()

            # Parse boolean env vars
            if value.lower() in ("true", "1", "yes"):
                merged_config[config_key] = True
            elif value.lower() in ("false", "0", "no"):
                merged_config[config_key] = False
            else:
                # Try to parse as int, else keep as string
                try:
                    merged_config[config_key] = int(value)
                except ValueError:
                    merged_config[config_key] = value

    # Layer 1: CLI flags (highest precedence)
    if cli_flags is not None:
        merged_config.update(cli_flags)

    # Convert Path strings to Path objects
    for path_field in ["ocr_artifact_patterns_file", "header_footer_patterns_file"]:
        if path_field in merged_config and isinstance(merged_config[path_field], str):
            merged_config[path_field] = Path(merged_config[path_field])

    # Create and validate NormalizationConfig
    return NormalizationConfig(**merged_config)
