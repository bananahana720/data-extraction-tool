"""
CLI module for data extraction tool.

Provides command-line interface for:
- Extract: Single file extraction
- Batch: Multiple file batch processing
- Version: Version information
- Config: Configuration management

User-friendly interface designed for non-technical auditors.
"""

from .main import cli

__all__ = ["cli"]
