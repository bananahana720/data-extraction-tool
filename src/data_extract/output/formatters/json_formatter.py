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
        import time

        start_time = time.time()

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert iterator to list if necessary
        if not isinstance(chunks, list):
            chunks = list(chunks)

        # Convert chunks to JSON-serializable format
        output_data = {
            "metadata": {
                "chunk_count": len(chunks),
                "processing_version": "1.0.0",
            },
            "chunks": [],
        }

        # Process each chunk
        for chunk in chunks:
            chunk_data = {
                "id": getattr(chunk, "id", None),
                "text": getattr(chunk, "text", str(chunk)),
                "metadata": {},
            }
            output_data["chunks"].append(chunk_data)

        # Write JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        duration = time.time() - start_time

        return FormattingResult(
            output_path=output_path,
            chunk_count=len(chunks),
            total_size=output_path.stat().st_size if output_path.exists() else 0,
            metadata={},
            format_type="json",
            duration_seconds=duration,
            errors=[],
        )
