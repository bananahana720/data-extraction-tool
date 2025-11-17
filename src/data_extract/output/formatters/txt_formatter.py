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
        import time

        start_time = time.time()

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert iterator to list if necessary to allow multiple passes
        if not isinstance(chunks, list):
            chunks = list(chunks)

        # Write text file with UTF-8-sig encoding
        with open(output_path, "w", encoding="utf-8-sig") as f:
            for i, chunk in enumerate(chunks, 1):
                # Add delimiter for each chunk (including first)
                if i == 1:
                    # First chunk gets delimiter at the start
                    f.write(self.delimiter.replace("{{n}}", f"{i:03d}"))
                    f.write("\n\n")
                else:
                    # Subsequent chunks get delimiter with spacing
                    f.write("\n\n")
                    f.write(self.delimiter.replace("{{n}}", f"{i:03d}"))
                    f.write("\n\n")

                # Include metadata headers if requested
                if self.include_metadata and hasattr(chunk, "metadata"):
                    metadata = chunk.metadata
                    if metadata.source_file:
                        f.write(f"Source: {metadata.source_file}\n")
                    if metadata.entity_tags:
                        entity_ids = [e.entity_id for e in metadata.entity_tags]
                        f.write(f"Entities: {'; '.join(entity_ids)}\n")
                    if metadata.quality and metadata.quality.overall:
                        f.write(f"Quality: {metadata.quality.overall:.2f}\n")
                    f.write("\n")

                # Write chunk text - extract text attribute
                if hasattr(chunk, "text"):
                    f.write(chunk.text)
                else:
                    f.write(str(chunk))

        duration = time.time() - start_time

        return FormattingResult(
            output_path=output_path,
            chunk_count=len(chunks),
            total_size=output_path.stat().st_size if output_path.exists() else 0,
            metadata={},
            format_type="txt",
            duration_seconds=duration,
            errors=[],
        )
