"""Base formatter interface and common functionality."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List


@dataclass(frozen=True)
class FormattingResult:
    """Result of formatting operation."""

    output_path: Path
    chunk_count: int
    total_size: int
    metadata: dict


class BaseFormatter(ABC):
    """Base class for all output formatters."""

    @abstractmethod
    def format_chunks(self, chunks: List[Any], output_path: Path, **kwargs) -> FormattingResult:
        """Format chunks and write to output path.

        Args:
            chunks: List of chunks to format
            output_path: Path to write output
            **kwargs: Additional formatter-specific options

        Returns:
            FormattingResult with details of operation
        """
        pass
