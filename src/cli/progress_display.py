"""
CLI Progress Display Module.

Provides Rich-based progress visualization for file extraction operations.
Integrates with ProgressTracker for real-time updates and supports both
single-file and batch processing modes.

Design:
- Stage-based progress for single files (extraction → processing → formatting)
- Table-based progress for batch operations
- Respects quiet/verbose modes
- Thread-safe updates
- Clean cleanup on interruption
- ETA and throughput display

Example Single File:
    >>> from src.cli.progress_display import SingleFileProgress
    >>> from pathlib import Path
    >>>
    >>> with SingleFileProgress(Path("doc.docx"), verbose=False) as progress:
    >>>     def callback(status):
    >>>         progress.update(status)
    >>>
    >>>     result = pipeline.process_file(file_path, progress_callback=callback)

Example Batch:
    >>> from src.cli.progress_display import BatchProgress
    >>>
    >>> files = [Path("doc1.docx"), Path("doc2.pdf")]
    >>> with BatchProgress(files, verbose=False) as progress:
    >>>     def callback(status):
    >>>         progress.update(status)
    >>>
    >>>     results = batch_processor.process_batch(files, progress_callback=callback)
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import time
import sys
import threading

from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TaskID,
)
from rich.table import Table
from rich.live import Live
from rich.console import Console


def _create_safe_console(**kwargs) -> Console:
    """
    Create a Console instance with safe encoding for Windows.

    Ensures UTF-8 encoding is used to prevent 'charmap' codec errors
    when displaying Unicode characters (e.g., from PDF icons or special fonts).

    Args:
        **kwargs: Additional Console constructor arguments

    Returns:
        Configured Console instance
    """
    # Merge default safe settings with user-provided kwargs
    safe_kwargs = {
        "force_terminal": True,
        "legacy_windows": False,  # Use modern Windows console API
    }
    safe_kwargs.update(kwargs)

    return Console(**safe_kwargs)


class SingleFileProgress:
    """
    Progress display for single file extraction.

    Shows stage-based progress with spinner, progress bar, and ETA.

    Attributes:
        file_path: Path to file being processed
        console: Rich Console instance
        verbose: Show detailed stage information
        quiet: Suppress all output
    """

    def __init__(
        self,
        file_path: Path,
        console: Optional[Console] = None,
        verbose: bool = False,
        quiet: bool = False,
    ):
        """
        Initialize single file progress display.

        Args:
            file_path: Path to file being processed
            console: Optional Rich Console instance
            verbose: Show detailed progress information
            quiet: Suppress all output
        """
        self.file_path = file_path
        self.console = console if console is not None else _create_safe_console()
        self.verbose = verbose
        self.quiet = quiet

        # Progress components
        self._progress: Optional[Progress] = None
        self._task_id: Optional[TaskID] = None
        self._current_stage: str = "starting"
        self._start_time = time.time()

        # Thread safety for Rich progress updates
        self._lock = threading.Lock()

    def __enter__(self):
        """Enter context manager."""
        if not self.quiet:
            # Create progress display with appropriate columns
            columns = [
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            ]

            # Add ETA column if not in verbose mode (verbose shows per-stage info)
            if not self.verbose:
                columns.append(TimeRemainingColumn())

            self._progress = Progress(*columns, console=self.console)
            self._progress.start()

            # Add main task
            self._task_id = self._progress.add_task(f"Processing {self.file_path.name}", total=100)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self._progress is not None:
            self._progress.stop()

        return False  # Don't suppress exceptions

    def update(self, status: Dict[str, Any]) -> None:
        """
        Update progress display with status information.

        Thread-safe: Can be called from worker threads.

        Args:
            status: Status dict from progress callback with keys:
                - stage: Current pipeline stage
                - percentage: Completion percentage (0-100)
                - message: Optional status message
        """
        if self.quiet or self._progress is None or self._task_id is None:
            return

        # Thread-safe update using lock
        with self._lock:
            try:
                # Extract status information
                stage = status.get("stage", "processing")
                percentage = status.get("percentage", 0)
                message = status.get("message", "")

                # Update current stage
                if stage != self._current_stage:
                    self._current_stage = stage

                    if self.verbose:
                        # Show stage transitions
                        elapsed = time.time() - self._start_time
                        self.console.print(
                            f"  [{percentage:>3.0f}%] {stage.capitalize()} " f"({elapsed:.1f}s)",
                            style="dim",
                        )

                # Update progress bar description
                description = f"Processing {self.file_path.name}"
                if self.verbose and message:
                    description = f"{description} - {message}"

                # Update progress
                self._progress.update(self._task_id, completed=percentage, description=description)
            except Exception as e:
                # Silently ignore progress update errors to prevent deadlock
                # (worker thread exceptions should not crash the process)
                pass

    def complete(self, success: bool = True) -> None:
        """
        Mark progress as complete.

        Args:
            success: Whether operation succeeded
        """
        if self.quiet or self._progress is None or self._task_id is None:
            return

        self._progress.update(self._task_id, completed=100)


class BatchProgress:
    """
    Progress display for batch file processing.

    Shows table with per-file status, progress, and overall batch progress.

    Attributes:
        file_paths: List of files being processed
        console: Rich Console instance
        verbose: Show detailed information
        quiet: Suppress all output
    """

    def __init__(
        self,
        file_paths: List[Path],
        console: Optional[Console] = None,
        verbose: bool = False,
        quiet: bool = False,
    ):
        """
        Initialize batch progress display.

        Args:
            file_paths: List of file paths being processed
            console: Optional Rich Console instance
            verbose: Show detailed progress information
            quiet: Suppress all output
        """
        self.file_paths = file_paths
        self.console = console if console is not None else _create_safe_console()
        self.verbose = verbose
        self.quiet = quiet

        # Track file status
        self._file_status: Dict[Path, Dict[str, Any]] = {
            path: {
                "status": "Pending",
                "progress": 0,
                "stage": "",
                "style": "dim",
            }
            for path in file_paths
        }

        # Progress components
        self._progress: Optional[Progress] = None
        self._task_id: Optional[TaskID] = None
        self._live: Optional[Live] = None
        self._start_time = time.time()
        self._completed_count = 0

        # Thread safety for Rich progress updates from worker threads
        self._lock = threading.Lock()

    def __enter__(self):
        """Enter context manager."""
        if not self.quiet:
            # Create overall progress bar
            self._progress = Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total} files)"),
                TimeRemainingColumn(),
                console=self.console,
            )
            self._progress.start()

            self._task_id = self._progress.add_task("Processing files", total=len(self.file_paths))

            # Show initial message
            self.console.print(f"\n[cyan]Processing {len(self.file_paths)} files...[/cyan]\n")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        if self._live is not None:
            self._live.stop()

        if self._progress is not None:
            self._progress.stop()

        return False  # Don't suppress exceptions

    def update(self, status: Dict[str, Any]) -> None:
        """
        Update progress display with status information.

        Thread-safe: Can be called from worker threads in batch processing.

        Args:
            status: Status dict from progress callback with keys:
                - current_file: Name of current file (optional)
                - batch_percentage: Overall batch percentage (optional)
                - stage: Current stage for file (optional)
                - percentage: File progress percentage (optional)
                - items_processed: Number of files completed (optional)
        """
        if self.quiet or self._progress is None or self._task_id is None:
            return

        # Thread-safe update using lock
        with self._lock:
            try:
                # Update overall progress if available
                if "items_processed" in status:
                    completed = status["items_processed"]
                    self._completed_count = completed
                    self._progress.update(self._task_id, completed=completed)

                # Update current file status
                current_file = status.get("current_file")
                if current_file:
                    # Find matching file path
                    for path in self.file_paths:
                        if path.name == current_file or str(path) == current_file:
                            file_status = self._file_status[path]

                            # Update file progress
                            file_progress = status.get("percentage", 0)
                            stage = status.get("stage", "")

                            if file_progress >= 100:
                                file_status["status"] = "[OK] Complete"
                                file_status["progress"] = 100
                                file_status["style"] = "green"
                            elif file_progress > 0:
                                file_status["status"] = "Processing"
                                file_status["progress"] = file_progress
                                file_status["stage"] = stage
                                file_status["style"] = "yellow"

                            break

                # Show verbose file-level updates
                if self.verbose and current_file and "stage" in status:
                    percentage = status.get("percentage", 0)
                    stage = status.get("stage", "processing")
                    self.console.print(
                        f"  [{percentage:>3.0f}%] {current_file}: {stage}", style="dim"
                    )
            except Exception as e:
                # Silently ignore progress update errors to prevent deadlock
                # (worker thread exceptions should not crash the process)
                pass

    def mark_file_complete(self, file_path: Path, success: bool = True) -> None:
        """
        Mark a specific file as complete.

        Thread-safe: Can be called from worker threads.

        Args:
            file_path: Path to file that completed
            success: Whether file processed successfully
        """
        with self._lock:
            if file_path in self._file_status:
                status = self._file_status[file_path]
                status["progress"] = 100

                if success:
                    status["status"] = "[OK] Complete"
                    status["style"] = "green"
                else:
                    status["status"] = "[ERR] Failed"
                    status["style"] = "red"

    def mark_file_failed(self, file_path: Path, error: str = "") -> None:
        """
        Mark a specific file as failed.

        Thread-safe: Can be called from worker threads.

        Args:
            file_path: Path to file that failed
            error: Optional error message
        """
        self.mark_file_complete(file_path, success=False)

        if self.verbose and error:
            with self._lock:
                try:
                    self.console.print(f"  [red][ERR] {file_path.name}: {error}[/red]")
                except Exception:
                    pass  # Ignore console errors

    def get_summary_table(self) -> Table:
        """
        Create summary table for batch progress.

        Returns:
            Rich Table with per-file status
        """
        table = Table(title=f"Batch Processing - {len(self.file_paths)} Files")
        table.add_column("File", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Progress", justify="right")

        for path, status in self._file_status.items():
            # Format progress
            progress_pct = status["progress"]
            if progress_pct >= 100:
                progress_str = "100%"
            elif progress_pct > 0:
                progress_str = f"{progress_pct:.0f}%"
            else:
                progress_str = "0%"

            # Add row
            table.add_row(path.name, status["status"], progress_str, style=status["style"])

        return table


@contextmanager
def create_progress_display(
    file_path: Optional[Path] = None,
    file_paths: Optional[List[Path]] = None,
    console: Optional[Console] = None,
    verbose: bool = False,
    quiet: bool = False,
):
    """
    Context manager factory for progress displays.

    Creates SingleFileProgress or BatchProgress based on arguments.

    Args:
        file_path: Single file path (creates SingleFileProgress)
        file_paths: List of file paths (creates BatchProgress)
        console: Optional Rich Console instance
        verbose: Show detailed information
        quiet: Suppress all output

    Yields:
        Progress display instance (SingleFileProgress or BatchProgress)

    Raises:
        ValueError: If neither file_path nor file_paths provided

    Example:
        >>> # Single file
        >>> with create_progress_display(file_path=Path("doc.docx")) as progress:
        >>>     def callback(status):
        >>>         progress.update(status)
        >>>     result = pipeline.process_file(file_path, progress_callback=callback)
        >>>
        >>> # Batch
        >>> with create_progress_display(file_paths=files) as progress:
        >>>     def callback(status):
        >>>         progress.update(status)
        >>>     results = batch.process_batch(files, progress_callback=callback)
    """
    if file_path is not None:
        # Single file mode
        with SingleFileProgress(
            file_path=file_path, console=console, verbose=verbose, quiet=quiet
        ) as progress:
            yield progress

    elif file_paths is not None:
        # Batch mode
        with BatchProgress(
            file_paths=file_paths, console=console, verbose=verbose, quiet=quiet
        ) as progress:
            yield progress

    else:
        raise ValueError("Must provide either file_path or file_paths")
