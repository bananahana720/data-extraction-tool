"""
CLI Command Implementations.

Implements all CLI commands:
- extract: Single file extraction
- batch: Batch file processing
- version: Version information
- config: Configuration management

Each command provides user-friendly messages and error handling
for non-technical users.
"""

import glob as glob_module
import io
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from cli.progress_display import BatchProgress, SingleFileProgress
from extractors import DocxExtractor, PdfExtractor, TextFileExtractor
from formatters import ChunkedTextFormatter, JsonFormatter, MarkdownFormatter
from infrastructure import ConfigManager, ErrorHandler

# Use absolute imports that work both in development and installed package
# When installed via wheel, cli/extractors/etc become top-level packages
from pipeline import BatchProcessor, ExtractionPipeline
from processors import ContextLinker, MetadataAggregator, QualityValidator

# Try to import additional extractors if available
try:
    from extractors.pptx_extractor import PptxExtractor
except ImportError:
    PptxExtractor = None

try:
    from extractors.excel_extractor import ExcelExtractor
except ImportError:
    ExcelExtractor = None

try:
    from extractors.csv_extractor import CSVExtractor
except ImportError:
    CSVExtractor = None

# Configure UTF-8 encoding for Windows console
# This prevents 'charmap' codec errors when displaying Unicode characters
if sys.platform == "win32":
    # Reconfigure stdout/stderr with UTF-8 encoding, replacing unencodable chars
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    else:
        # Fallback for older Python versions
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    else:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Initialize console for rich output with UTF-8 encoding
# force_terminal=True ensures proper rendering even when output is redirected
console = Console(
    force_terminal=True,
    legacy_windows=False,  # Use modern Windows console API
)
error_handler = ErrorHandler()


def create_pipeline(config_path: Optional[Path] = None):
    """
    Create and configure extraction pipeline.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Tuple of (ExtractionPipeline, config) - pipeline and loaded config
    """
    # Load configuration
    config = None
    if config_path and config_path.exists():
        try:
            config = ConfigManager(config_path)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load config: {e}[/yellow]")
            console.print("[yellow]Using default configuration[/yellow]")

    # Create pipeline
    pipeline = ExtractionPipeline(config=config)

    # Register extractors with config
    pipeline.register_extractor("docx", DocxExtractor(config=config))
    pipeline.register_extractor("pdf", PdfExtractor(config=config))
    pipeline.register_extractor("txt", TextFileExtractor(config=config))

    # Register optional extractors if available
    if PptxExtractor is not None:
        pipeline.register_extractor("pptx", PptxExtractor(config=config))
    if ExcelExtractor is not None:
        pipeline.register_extractor("xlsx", ExcelExtractor(config=config))
    if CSVExtractor is not None:
        pipeline.register_extractor("csv", CSVExtractor(config=config))

    # Add processors with config
    pipeline.add_processor(ContextLinker(config=config))
    pipeline.add_processor(MetadataAggregator(config=config))
    pipeline.add_processor(QualityValidator(config=config))

    return pipeline, config


def add_formatters(pipeline: ExtractionPipeline, format_type: str, config=None) -> None:
    """
    Add formatters to pipeline based on format type.

    Args:
        pipeline: Pipeline to add formatters to
        format_type: Format type ('json', 'markdown', 'chunked', 'all')
        config: Optional configuration (ConfigManager or dict)
    """
    # Extract formatter configs if ConfigManager is provided
    json_config = None
    markdown_config = None
    chunked_config = None

    if config is not None:
        # Check if it's a ConfigManager (has get_section method)
        if hasattr(config, "get_section"):
            json_config = config.get_section("formatters.json", default={})
            markdown_config = config.get_section("formatters.markdown", default={})
            chunked_config = config.get_section("formatters.chunked_text", default={})
        else:
            # It's a dict, use as-is for all formatters
            json_config = config
            markdown_config = config
            chunked_config = config

    if format_type == "all" or format_type == "json":
        pipeline.add_formatter(JsonFormatter(config=json_config))

    if format_type == "all" or format_type == "markdown":
        pipeline.add_formatter(MarkdownFormatter(config=markdown_config))

    if format_type == "all" or format_type == "chunked":
        pipeline.add_formatter(ChunkedTextFormatter(config=chunked_config))


def write_outputs(result, output_path: Path, format_type: str) -> None:
    """
    Write formatted outputs to files with proper UTF-8 encoding.

    Handles Unicode characters safely to prevent encoding errors on Windows.

    Args:
        result: PipelineResult with formatted outputs
        output_path: Base output path
        format_type: Format type for naming
    """
    if not result.formatted_outputs:
        return

    # Ensure output directory exists
    if output_path.suffix:
        # It's a file path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write single format
        if len(result.formatted_outputs) == 1:
            # Write with UTF-8 encoding, replacing unencodable chars
            output_path.write_text(
                result.formatted_outputs[0].content, encoding="utf-8", errors="replace"
            )
        else:
            # Multiple formats, use base name
            base_path = output_path.with_suffix("")
            for formatted in result.formatted_outputs:
                ext = get_extension_for_format(formatted.format_type)
                file_path = base_path.with_suffix(ext)
                file_path.write_text(formatted.content, encoding="utf-8", errors="replace")
    else:
        # It's a directory path
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filenames based on source
        base_name = result.source_file.stem if result.source_file else "output"

        for formatted in result.formatted_outputs:
            ext = get_extension_for_format(formatted.format_type)
            file_path = output_path / f"{base_name}{ext}"
            file_path.write_text(formatted.content, encoding="utf-8", errors="replace")


def get_extension_for_format(format_type: str) -> str:
    """
    Get file extension for format type.

    Args:
        format_type: Format type name

    Returns:
        File extension including dot
    """
    extensions = {
        "json": ".json",
        "markdown": ".md",
        "chunked_text": ".txt",
    }
    return extensions.get(format_type, ".txt")


def format_user_error(error_msg: str, suggestion: Optional[str] = None) -> str:
    """
    Format error message for non-technical users.

    Args:
        error_msg: Technical error message
        suggestion: Optional suggestion for fixing

    Returns:
        User-friendly error message
    """
    # Convert technical errors to user-friendly messages
    user_msg = error_msg

    if "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
        user_msg = (
            "The file you specified could not be found. Please check the file path and try again."
        )
    elif "unknown file format" in error_msg.lower() or "unsupported" in error_msg.lower():
        user_msg = "This file format is not supported. Supported formats: DOCX, PDF, PPTX, XLSX"
    elif "permission" in error_msg.lower() or "access" in error_msg.lower():
        user_msg = "Cannot access the file. Please check file permissions."

    if suggestion:
        user_msg += f"\n\nSuggestion: {suggestion}"

    return user_msg


@click.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output file or directory path"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown", "chunked", "all"], case_sensitive=False),
    default="json",
    help="Output format (default: json)",
)
@click.option("--force", is_flag=True, help="Overwrite existing files without asking")
@click.pass_context
def extract_command(ctx, file_path: Path, output: Optional[Path], format: str, force: bool):
    """
    Extract content from a single file.

    Processes the specified file and generates output in the requested format.

    Examples:

        Extract to JSON:
        $ data-extract extract document.docx --format json

        Extract to Markdown with custom output:
        $ data-extract extract report.pdf --output result.md --format markdown

        Extract to all formats:
        $ data-extract extract presentation.pptx --format all
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)
    config_path = ctx.obj.get("config_path")

    try:
        # Validate file exists (already done by Click, but double-check)
        if not file_path.exists():
            console.print(f"[red]Error: File not found: {file_path}[/red]")
            console.print("\nPlease check the file path and try again.")
            sys.exit(1)

        # Determine output path
        if output is None:
            # Default output path: same name as input, different extension
            output = file_path.with_suffix(get_extension_for_format(format))

        # Check for existing file
        if not force and output.exists() and output.is_file():
            if not click.confirm(f"\nFile {output} already exists. Overwrite?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                sys.exit(0)

        # Create and configure pipeline
        if not quiet:
            console.print(f"[cyan]Processing file: {file_path.name}[/cyan]")

        pipeline, config = create_pipeline(config_path)
        add_formatters(pipeline, format, config)

        # Process file with enhanced progress tracking
        if not quiet:
            with SingleFileProgress(
                file_path=file_path, console=console, verbose=verbose, quiet=quiet
            ) as progress_display:

                def progress_callback(status):
                    progress_display.update(status)

                result = pipeline.process_file(file_path, progress_callback=progress_callback)
        else:
            result = pipeline.process_file(file_path)

        # Check result
        if not result.success:
            console.print("[red]Error: Extraction failed[/red]")
            if result.all_errors:
                error_msg = result.all_errors[0]
                user_msg = format_user_error(error_msg)
                console.print(f"\n{user_msg}")
            sys.exit(1)

        # Write outputs
        write_outputs(result, output, format)

        # Success message
        if not quiet:
            console.print(f"\n[green]SUCCESS: Extracted {file_path.name}[/green]")
            console.print(f"  Output: {output}")

            if verbose:
                console.print(f"  Blocks extracted: {len(result.extraction_result.content_blocks)}")
                console.print(f"  Processing time: {result.duration_seconds:.2f}s")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            raise
        sys.exit(1)


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), required=True, help="Output directory path"
)
@click.option("--pattern", "-p", type=str, help='Glob pattern to filter files (e.g., "*.pdf")')
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown", "chunked", "all"], case_sensitive=False),
    default="json",
    help="Output format (default: json)",
)
@click.option(
    "--workers", "-w", type=int, default=4, help="Number of parallel workers (default: 4)"
)
@click.pass_context
def batch_command(
    ctx, paths: tuple, output: Path, pattern: Optional[str], format: str, workers: int
):
    """
    Process multiple files in batch.

    Processes all files in specified directories or file list, using parallel
    workers for faster processing.

    Examples:

        Process all files in directory:
        $ data-extract batch ./documents/ --output ./results/

        Process only PDF files:
        $ data-extract batch ./documents/ --pattern "*.pdf" --output ./results/

        Process with custom worker count:
        $ data-extract batch ./documents/ --output ./results/ --workers 8
    """
    verbose = ctx.obj.get("verbose", False)
    quiet = ctx.obj.get("quiet", False)
    config_path = ctx.obj.get("config_path")

    try:
        # Validate workers
        if workers <= 0:
            console.print("[red]Error: Number of workers must be greater than 0[/red]")
            sys.exit(1)

        # Collect files to process
        files_to_process = []

        for path in paths:
            if path.is_file():
                files_to_process.append(path)
            elif path.is_dir():
                # Find files in directory
                if pattern:
                    search_pattern = str(path / pattern)
                    files_to_process.extend([Path(f) for f in glob_module.glob(search_pattern)])
                else:
                    # All files with supported extensions
                    for ext in ["*.docx", "*.pdf", "*.pptx", "*.xlsx", "*.txt"]:
                        files_to_process.extend(path.glob(ext))

        if not files_to_process:
            console.print("[yellow]No files found to process.[/yellow]")
            if pattern:
                console.print(f"  Pattern: {pattern}")
            sys.exit(0)

        # Create output directory
        output.mkdir(parents=True, exist_ok=True)

        # Create and configure pipeline
        pipeline, config = create_pipeline(config_path)
        add_formatters(pipeline, format, config)

        # Create batch processor
        batch_processor = BatchProcessor(pipeline=pipeline, max_workers=workers)

        if not quiet:
            console.print(
                f"[cyan]Processing {len(files_to_process)} files with {workers} workers...[/cyan]"
            )

        # Process batch with enhanced progress tracking
        if not quiet:
            with BatchProgress(
                file_paths=files_to_process, console=console, verbose=verbose, quiet=quiet
            ) as progress_display:

                def progress_callback(status):
                    progress_display.update(status)

                results = batch_processor.process_batch(
                    files_to_process, progress_callback=progress_callback
                )
        else:
            results = batch_processor.process_batch(files_to_process)

        # Write outputs
        for result in results:
            if result.success:
                # For batch processing, write directly to output directory
                # write_outputs will create properly named files with extensions
                write_outputs(result, output, format)

        # Display summary
        summary = batch_processor.get_summary(results)

        if not quiet:
            console.print("\n[bold]Summary:[/bold]")
            console.print(f"  Total files: {summary['total_files']}")
            console.print(f"  [green]Successful: {summary['successful']}[/green]")
            console.print(f"  [red]Failed: {summary['failed']}[/red]")
            console.print(f"  Success rate: {summary['success_rate']:.1%}")

            if verbose and summary["failed"] > 0:
                console.print("\n[bold]Failed files:[/bold]")
                for result in batch_processor.get_failed_results(results):
                    console.print(f"  [red]FAILED: {result.source_file.name}[/red]")
                    if result.all_errors:
                        console.print(f"    {result.all_errors[0]}")

        # Exit with appropriate code
        if summary["failed"] > 0:
            sys.exit(1)  # Some failures
        else:
            sys.exit(0)  # All success

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            raise
        sys.exit(1)


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed version information")
def version_command(verbose: bool):
    """
    Show version information.

    Displays the version number and optionally detailed component information.

    Examples:

        Show version:
        $ data-extract version

        Show detailed version info:
        $ data-extract version --verbose
    """
    from cli.main import __version__

    console.print(f"[bold]Data Extraction Tool[/bold] version {__version__}")

    if verbose:
        import platform
        import sys

        console.print(f"\nPython version: {sys.version.split()[0]}")
        console.print(f"Platform: {platform.platform()}")

        # Show component versions
        console.print("\n[bold]Components:[/bold]")
        try:
            import click

            console.print(f"  click: {click.__version__}")
        except:
            pass

        try:
            import rich

            console.print(f"  rich: {rich.__version__}")
        except:
            pass


@click.group()
def config_command():
    """
    Configuration management commands.

    Manage and validate configuration files.
    """
    pass


@config_command.command(name="show")
@click.pass_context
def config_show(ctx):
    """Show current configuration."""
    config_path = ctx.obj.get("config_path")

    if config_path and config_path.exists():
        console.print(f"[bold]Configuration from:[/bold] {config_path}\n")
        content = config_path.read_text()
        console.print(content)
    else:
        console.print("[yellow]No configuration file specified. Using defaults.[/yellow]")

        if config_path:
            console.print(f"  Specified file not found: {config_path}")


@config_command.command(name="validate")
@click.pass_context
def config_validate(ctx):
    """Validate configuration file."""
    config_path = ctx.obj.get("config_path")

    if not config_path:
        console.print("[yellow]No configuration file specified. Nothing to validate.[/yellow]")
        sys.exit(0)

    if not config_path.exists():
        console.print(f"[red]Error: Configuration file not found: {config_path}[/red]")
        sys.exit(1)

    try:
        config = ConfigManager(config_path)
        console.print("[green]VALID: Configuration is valid[/green]")
        console.print(f"  File: {config_path}")
    except Exception as e:
        console.print("[red]INVALID: Configuration is invalid[/red]")
        console.print(f"\nError: {e}")
        sys.exit(1)


@config_command.command(name="path")
@click.pass_context
def config_path_command(ctx):
    """Show configuration file path."""
    config_path = ctx.obj.get("config_path")

    if config_path:
        console.print(f"Configuration file: {config_path}")
        if config_path.exists():
            console.print("  [green](exists)[/green]")
        else:
            console.print("  [yellow](not found)[/yellow]")
    else:
        console.print("No configuration file specified. Using defaults.")
