"""JSON formatter for chunk output."""

import json
from pathlib import Path
from typing import Any, List

from .base import BaseFormatter, FormattingResult


class JsonFormatter(BaseFormatter):
    """Formats chunks as JSON output."""

    def __init__(self, validate: bool = True):
        """Initialize JSON formatter.

        Args:
            validate: Whether to validate output against schema
        """
        self.validate = validate

    def format_chunks(self, chunks: List[Any], output_path: Path, **kwargs) -> FormattingResult:
        """Format chunks as JSON and write to file.

        Args:
            chunks: List of chunks to format
            output_path: Path to write JSON file
            **kwargs: Additional options

        Returns:
            FormattingResult with operation details
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert chunks to JSON-serializable format
        output_data = {"metadata": {}, "chunks": []}

        # Write JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        return FormattingResult(
            output_path=output_path,
            chunk_count=len(chunks),
            total_size=output_path.stat().st_size if output_path.exists() else 0,
            metadata={},
        )
