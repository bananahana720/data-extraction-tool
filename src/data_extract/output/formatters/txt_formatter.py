"""Plain text formatter for chunk output."""

from pathlib import Path
from typing import Any, List

from .base import BaseFormatter, FormattingResult


class TxtFormatter(BaseFormatter):
    """Formats chunks as plain text output."""

    def __init__(self, include_metadata: bool = False, delimiter: str = "━━━ CHUNK {{n}} ━━━"):
        """Initialize text formatter.

        Args:
            include_metadata: Whether to include metadata headers
            delimiter: Delimiter between chunks
        """
        self.include_metadata = include_metadata
        self.delimiter = delimiter

    def format_chunks(self, chunks: List[Any], output_path: Path, **kwargs) -> FormattingResult:
        """Format chunks as plain text and write to file.

        Args:
            chunks: List of chunks to format
            output_path: Path to write text file
            **kwargs: Additional options

        Returns:
            FormattingResult with operation details
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write text file with UTF-8-sig encoding
        with open(output_path, "w", encoding="utf-8-sig") as f:
            for i, chunk in enumerate(chunks, 1):
                if i > 1:
                    f.write("\n\n")
                    f.write(self.delimiter.replace("{{n}}", f"{i:03d}"))
                    f.write("\n\n")
                # Write chunk text (simplified for stub)
                f.write(str(chunk))

        return FormattingResult(
            output_path=output_path,
            chunk_count=len(chunks),
            total_size=output_path.stat().st_size if output_path.exists() else 0,
            metadata={},
        )
