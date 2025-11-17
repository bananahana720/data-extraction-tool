"""Output writer for coordinating formatters and organization."""

from pathlib import Path
from typing import Any, List, Optional

from .formatters import CsvFormatter, JsonFormatter, TxtFormatter
from .organization import OrganizationStrategy, Organizer


class OutputWriter:
    """Main entry point for writing formatted output."""

    def __init__(self):
        """Initialize output writer."""
        self.organizer = Organizer()

    def write(
        self,
        chunks: List[Any],
        output_path: Path,
        format_type: str = "txt",
        per_chunk: bool = False,
        organize: bool = False,
        strategy: Optional[OrganizationStrategy] = None,
        **kwargs,
    ) -> Any:
        """Write chunks to output with specified format and organization.

        Args:
            chunks: List of chunks to write
            output_path: Output file or directory path
            format_type: Output format (json, txt, csv)
            per_chunk: Write each chunk to separate file
            organize: Enable output organization
            strategy: Organization strategy if organize is True
            **kwargs: Additional formatter options

        Returns:
            FormattingResult or OrganizationResult
        """
        # Select formatter based on format type
        if format_type == "json":
            formatter = JsonFormatter(validate=kwargs.get("validate", True))
        elif format_type == "txt":
            formatter = TxtFormatter(
                include_metadata=kwargs.get("include_metadata", False),
                delimiter=kwargs.get("delimiter", "━━━ CHUNK {{n}} ━━━"),
            )
        elif format_type == "csv":
            formatter = CsvFormatter(
                max_text_length=kwargs.get("max_text_length"), validate=kwargs.get("validate", True)
            )
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

        # Handle organization if requested
        if organize and strategy:
            return self.organizer.organize(
                chunks=chunks,
                output_dir=Path(output_path),
                strategy=strategy,
                format_type=format_type,
                **kwargs,
            )

        # Direct formatting
        return formatter.format_chunks(chunks, Path(output_path), **kwargs)
