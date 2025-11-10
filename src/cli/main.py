"""
Main CLI Entry Point for Data Extraction Tool.

Provides command-line interface using Click framework with commands:
- extract: Process single file
- batch: Process multiple files
- version: Show version information
- config: Configuration management

Design:
- User-friendly for non-technical auditors
- Clear error messages in plain language
- Progress indicators for long operations
- Configurable via command-line options
"""

from pathlib import Path
from typing import Optional
import sys

import click

from .commands import (
    extract_command,
    batch_command,
    version_command,
    config_command,
)


# Version information
__version__ = "1.0.0"


@click.group()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=False, path_type=Path),
    help="Path to configuration file",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
@click.pass_context
def cli(ctx, config: Optional[Path], verbose: bool, quiet: bool):
    """
    Data Extraction Tool - Extract content from documents for AI processing.

    This tool helps you extract content from Word documents, PDFs, PowerPoint
    presentations, and Excel workbooks into AI-friendly formats.

    Examples:

        Extract a single file to JSON:
        $ data-extract extract document.docx --format json

        Process multiple files:
        $ data-extract batch ./documents/ --format json

        Show version information:
        $ data-extract version
    """
    # Store context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


# Add commands
cli.add_command(extract_command, name="extract")
cli.add_command(batch_command, name="batch")
cli.add_command(version_command, name="version")
cli.add_command(config_command, name="config")


# Alternative short flag for version
@cli.command(name="-V", hidden=True)
@click.pass_context
def version_short(ctx):
    """Show version (short flag)."""
    ctx.invoke(version_command, verbose=False)


def main():
    """Entry point for console script."""
    import signal

    # Set up signal handling for Ctrl+C
    # This ensures interrupts work even when worker threads are active
    def signal_handler(signum, frame):
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(130)  # Standard exit code for SIGINT

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        click.echo(f"\nUnexpected error: {e}", err=True)
        if "--verbose" in sys.argv:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
