"""CLI entry point for data-extract command.

This is a minimal implementation for Story 3.5 UAT validation.
Epic 5 will replace with full Typer-based CLI with:
- Command structure (extract, batch, config, version)
- Configuration cascade (CLI flags → env vars → YAML → defaults)
- Progress indicators and error handling

Current implementation uses Click for basic functionality.
"""

import sys
from pathlib import Path
from typing import Any, Optional

import click

from data_extract.output.organization import OrganizationStrategy
from data_extract.output.writer import OutputWriter


@click.group()
@click.version_option(version="0.1.0")
def app() -> None:
    """Data Extraction Tool - Enterprise document processing for RAG workflows.

    Minimal CLI for Story 3.5 - Full implementation in Epic 5.
    """
    pass


@app.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "format_type",
    type=click.Choice(["json", "txt", "csv"], case_sensitive=False),
    default="txt",
    help="Output format (default: txt)",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    required=True,
    help="Output file or directory path",
)
@click.option(
    "--per-chunk",
    is_flag=True,
    default=False,
    help="Write each chunk to separate file (TXT only)",
)
@click.option(
    "--include-metadata",
    is_flag=True,
    default=False,
    help="Include metadata headers in output (TXT only)",
)
@click.option(
    "--organize",
    is_flag=True,
    default=False,
    help="Enable output organization (requires --strategy)",
)
@click.option(
    "--strategy",
    type=click.Choice(["by_document", "by_entity", "flat"], case_sensitive=False),
    default=None,
    help="Organization strategy (requires --organize)",
)
@click.option(
    "--delimiter",
    type=str,
    default="━━━ CHUNK {{n}} ━━━",
    help="Custom chunk delimiter (TXT only, use {{n}} for chunk number)",
)
def process(
    input_file: Path,
    format_type: str,
    output_path: Path,
    per_chunk: bool,
    include_metadata: bool,
    organize: bool,
    strategy: Optional[str],
    delimiter: str,
) -> None:
    """Process a document and generate formatted output.

    Example usage:

        \b
        # Concatenated TXT output
        data-extract process input.pdf --format txt --output chunks.txt

        \b
        # Per-chunk TXT files with metadata
        data-extract process input.pdf --format txt --output output/ --per-chunk --include-metadata

        \b
        # Organized output with BY_DOCUMENT strategy
        data-extract process input.pdf --format txt --output output/ --per-chunk --organize --strategy by_document

        \b
        # JSON output
        data-extract process input.pdf --format json --output output.json

        \b
        # CSV output
        data-extract process input.pdf --format csv --output output.csv

    Note: This is a minimal implementation for Story 3.6 UAT validation.
    Full pipeline integration will be completed in Epic 5.
    """
    try:
        # Validate organize + strategy combination
        if organize and strategy is None:
            click.echo("Error: --organize flag requires --strategy option", err=True)
            sys.exit(1)
        if not organize and strategy is not None:
            click.echo("Error: --strategy requires --organize flag", err=True)
            sys.exit(1)

        # Convert strategy string to enum if provided
        strategy_enum = None
        if strategy:
            strategy_map = {
                "by_document": OrganizationStrategy.BY_DOCUMENT,
                "by_entity": OrganizationStrategy.BY_ENTITY,
                "flat": OrganizationStrategy.FLAT,
            }
            strategy_enum = strategy_map[strategy]

        # Display processing info
        click.echo(f"Processing: {input_file}")
        click.echo(f"Output format: {format_type.upper()}")
        click.echo(f"Output path: {output_path}")

        # Import pipeline components (only when needed)
        # NOTE: Full pipeline integration deferred to Epic 5
        # For now, we demonstrate formatter functionality with mock chunks

        # Create demo chunks for UAT validation
        # Epic 5 will replace with full extraction → normalize → chunk pipeline
        demo_chunks = _create_demo_chunks(input_file)

        # Initialize writer and generate output
        writer = OutputWriter()

        # Build formatter kwargs
        formatter_kwargs: dict[str, Any] = {}
        if format_type == "txt":
            formatter_kwargs["per_chunk"] = per_chunk
            formatter_kwargs["include_metadata"] = include_metadata
            formatter_kwargs["delimiter"] = delimiter
        elif format_type == "csv":
            # CSV formatter accepts max_text_length and validate params
            formatter_kwargs["validate"] = True  # Enable parser validation by default

        # Write output
        result = writer.write(
            chunks=iter(demo_chunks),
            output_path=output_path,
            format_type=format_type,
            organize=organize,
            strategy=strategy_enum,
            **formatter_kwargs,
        )

        # Display results
        click.echo("\nProcessing complete!")
        click.echo(f"  Chunks written: {result.chunk_count}")
        click.echo(f"  Output size: {result.file_size_bytes:,} bytes")
        click.echo(f"  Duration: {result.duration_seconds:.2f}s")

        if result.errors:
            click.echo(f"\nWarnings ({len(result.errors)}):", err=True)
            for error in result.errors:
                click.echo(f"  - {error}", err=True)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def _create_demo_chunks(input_file: Path) -> list:
    """Create demo chunks for UAT validation.

    NOTE: This is a temporary helper for Story 3.5 demonstration.
    Epic 5 will replace with full extraction → normalize → chunk pipeline.

    Args:
        input_file: Input file path (used for metadata only)

    Returns:
        List of demo Chunk objects with realistic metadata
    """
    from data_extract.chunk.models import Chunk, ChunkMetadata, QualityScore

    # Create demo chunks with varied content
    demo_data: list[dict[str, Any]] = [
        {
            "text": "This is the first chunk of content from the document. "
            "It contains information about risk management processes and controls. "
            "Risk-001 has been identified as a critical risk requiring immediate attention.",
            "entities": ["Risk-001"],
        },
        {
            "text": "The second chunk discusses control frameworks and compliance requirements. "
            "Control-042 is designed to mitigate Risk-001 through automated monitoring. "
            "This control has been tested and validated by the audit team.",
            "entities": ["Control-042", "Risk-001"],
        },
        {
            "text": "Additional context about the organization's governance structure. "
            "Policy-123 establishes the framework for risk assessment and reporting. "
            "All business units must comply with quarterly review requirements.",
            "entities": ["Policy-123"],
        },
    ]

    chunks = []
    for idx, data in enumerate(demo_data, start=1):
        # Create minimal entity tags
        chunk_text: str = str(data["text"])
        chunk_entities: list[str] = data["entities"]  # type: ignore[assignment]

        entity_tags = [
            {
                "entity_id": entity,
                "entity_type": (
                    "risk"
                    if entity.startswith("Risk")
                    else "control" if entity.startswith("Control") else "policy"
                ),
                "start_pos": chunk_text.find(entity),
                "end_pos": chunk_text.find(entity) + len(entity),
            }
            for entity in chunk_entities
        ]

        # Create chunk metadata
        metadata = ChunkMetadata(
            source_file=input_file,
            processing_version="1.0.0-epic3-demo",
            entity_tags=entity_tags,
            quality=QualityScore(
                overall=0.95,
                completeness=0.98,
                coherence=0.92,
                ocr_confidence=0.98,
                readability_flesch_kincaid=8.0,
                readability_gunning_fog=9.5,
                flags=[],
            ),
        )

        # Create chunk
        chunk = Chunk(
            id=f"demo_chunk_{idx:03d}",
            text=chunk_text,
            document_id=input_file.stem,
            position_index=idx - 1,
            token_count=len(chunk_text.split()),
            word_count=len(chunk_text.split()),
            entities=[],
            section_context="",
            quality_score=0.95,
            readability_scores={"flesch_reading_ease": 65.0},
            metadata=metadata,
        )
        chunks.append(chunk)

    return chunks


@app.command()
def version() -> None:
    """Display version information."""
    click.echo("Data Extraction Tool v0.1.0")
    click.echo("Epic 3, Story 3.5 - Plain Text Output Format")
    click.echo("Full CLI implementation in Epic 5")


if __name__ == "__main__":
    app()
