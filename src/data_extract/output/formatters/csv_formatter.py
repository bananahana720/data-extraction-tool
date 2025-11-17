"""CSV formatter for chunk output."""

import csv
from pathlib import Path
from typing import Any, List, Optional

from .base import BaseFormatter, FormattingResult


class CsvFormatter(BaseFormatter):
    """Formats chunks as CSV output."""

    def __init__(self, max_text_length: Optional[int] = None, validate: bool = True):
        """Initialize CSV formatter.

        Args:
            max_text_length: Maximum text length before truncation
            validate: Whether to validate output
        """
        self.max_text_length = max_text_length
        self.validate = validate

    def format_chunks(self, chunks: List[Any], output_path: Path, **kwargs) -> FormattingResult:
        """Format chunks as CSV and write to file.

        Args:
            chunks: List of chunks to format
            output_path: Path to write CSV file
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

        # Write CSV file with UTF-8-sig encoding
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(
                [
                    "chunk_id",
                    "source_file",
                    "section_context",
                    "chunk_text",
                    "entity_tags",
                    "quality_score",
                    "word_count",
                    "token_count",
                    "processing_version",
                    "warnings",
                ]
            )
            # Write chunk data (simplified for stub)
            for i, chunk in enumerate(chunks, 1):
                chunk_text = getattr(chunk, "text", str(chunk))
                if self.max_text_length and len(chunk_text) > self.max_text_length:
                    chunk_text = chunk_text[: self.max_text_length] + "..."
                writer.writerow([f"chunk_{i:03d}", "", "", chunk_text, "", "", "", "", "", ""])

        duration = time.time() - start_time

        return FormattingResult(
            output_path=output_path,
            chunk_count=len(chunks),
            total_size=output_path.stat().st_size if output_path.exists() else 0,
            metadata={},
            format_type="csv",
            duration_seconds=duration,
            errors=[],
        )
