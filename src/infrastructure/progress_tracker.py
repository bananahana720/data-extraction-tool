"""
Progress Tracking Infrastructure for Data Extraction System.

Provides progress reporting for long-running operations with callbacks,
percentage calculation, ETA estimation, and thread-safe operations.

Design Principles:
- Thread-safe for parallel operations
- Callback-based notifications
- ETA and throughput calculations
- Cancellation support
- Context manager support for automatic completion

Usage:
    >>> tracker = ProgressTracker(total_items=100)
    >>> for item in items:
    >>>     process(item)
    >>>     tracker.increment()
    >>>     print(f"Progress: {tracker.percentage:.1f}%")

    >>> # With callbacks
    >>> def on_progress(status):
    >>>     print(f"{status['percentage']:.1f}% - {status['current_item']}")
    >>>
    >>> tracker = ProgressTracker(total_items=100, callback=on_progress)
    >>> for item in items:
    >>>     process(item)
    >>>     tracker.increment(current_item=item.name)

    >>> # As context manager
    >>> with ProgressTracker(total_items=100) as tracker:
    >>>     for item in items:
    >>>         process(item)
    >>>         tracker.increment()
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import logging
import threading
import time


@dataclass
class ProgressTracker:
    """
    Thread-safe progress tracker for long-running operations.

    Tracks:
    - Items processed / total items
    - Percentage completion
    - Elapsed time
    - Estimated time remaining (ETA)
    - Throughput (items/second)
    - Current item being processed
    - Cancellation status

    Attributes:
        total_items: Total number of items to process
        items_processed: Number of items processed so far
        percentage: Completion percentage (0.0-100.0)
        current_item: Description of current item being processed
        description: Operation description
        callback: Callback function called on updates
        cancelled: Whether operation has been cancelled
    """

    total_items: int
    description: str = ""
    callback: Optional[Callable[[dict[str, Any]], None]] = None

    def __post_init__(self):
        """Initialize progress tracker."""
        self.items_processed = 0
        self.current_item: Optional[str] = None
        self.cancelled = False

        # Timing
        self._start_time = time.time()
        self._last_update_time = self._start_time

        # Thread safety - use RLock for reentrant locking
        # (get_status() calls methods that also acquire the lock)
        self._lock = threading.RLock()

        # Callbacks
        self._callbacks: list[Callable[[dict[str, Any]], None]] = []
        if self.callback:
            self._callbacks.append(self.callback)

        # Logger
        self.logger = logging.getLogger(__name__)

    @property
    def percentage(self) -> float:
        """
        Get completion percentage.

        Returns:
            Percentage complete (0.0-100.0)
        """
        if self.total_items == 0:
            return 0.0
        return (self.items_processed / self.total_items) * 100.0

    def update(self, items_processed: int, current_item: Optional[str] = None) -> None:
        """
        Update progress with new item count.

        Args:
            items_processed: Total items processed so far
            current_item: Description of current item (optional)

        Thread-safe: Yes
        """
        with self._lock:
            self.items_processed = items_processed
            if current_item is not None:
                self.current_item = current_item
            self._last_update_time = time.time()

        # Notify callbacks
        self._notify_callbacks()

    def increment(self, n: int = 1, current_item: Optional[str] = None) -> None:
        """
        Increment progress by n items.

        Args:
            n: Number of items to increment by (default: 1)
            current_item: Description of current item (optional)

        Thread-safe: Yes
        """
        with self._lock:
            self.items_processed += n
            if current_item is not None:
                self.current_item = current_item
            self._last_update_time = time.time()

        # Notify callbacks
        self._notify_callbacks()

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time since tracker started.

        Returns:
            Elapsed time in seconds

        Thread-safe: Yes
        """
        with self._lock:
            return time.time() - self._start_time

    def get_throughput(self) -> Optional[float]:
        """
        Calculate items processed per second.

        Returns:
            Items per second, or None if no time elapsed

        Thread-safe: Yes
        """
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return None

        with self._lock:
            return self.items_processed / elapsed

    def get_eta(self) -> Optional[float]:
        """
        Estimate time remaining in seconds.

        Returns:
            Estimated seconds remaining, or None if cannot estimate

        Thread-safe: Yes
        """
        with self._lock:
            if self.items_processed == 0 or self.total_items == 0:
                return None

            elapsed = time.time() - self._start_time
            items_remaining = self.total_items - self.items_processed

            if items_remaining <= 0:
                return 0.0

            rate = self.items_processed / elapsed
            if rate == 0:
                return None

            return items_remaining / rate

    def format_eta(self) -> str:
        """
        Format ETA as human-readable string.

        Returns:
            ETA string (e.g., "2 minutes 30 seconds")

        Thread-safe: Yes
        """
        eta = self.get_eta()
        if eta is None:
            return "Unknown"

        if eta < 1:
            return "Less than a second"
        elif eta < 60:
            return f"{int(eta)} second{'s' if int(eta) != 1 else ''}"
        elif eta < 3600:
            minutes = int(eta / 60)
            seconds = int(eta % 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"
        else:
            hours = int(eta / 3600)
            minutes = int((eta % 3600) / 60)
            return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"

    def format_throughput(self) -> str:
        """
        Format throughput as human-readable string.

        Returns:
            Throughput string (e.g., "42.5 items/sec")

        Thread-safe: Yes
        """
        throughput = self.get_throughput()
        if throughput is None:
            return "Unknown"

        return f"{throughput:.1f} items/sec"

    def add_callback(self, callback: Callable[[dict[str, Any]], None]) -> None:
        """
        Add a progress callback.

        Args:
            callback: Function to call on progress updates

        Thread-safe: Yes
        """
        with self._lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[dict[str, Any]], None]) -> None:
        """
        Remove a progress callback.

        Args:
            callback: Function to remove

        Thread-safe: Yes
        """
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def cancel(self) -> None:
        """
        Cancel the operation.

        Thread-safe: Yes
        """
        with self._lock:
            self.cancelled = True

        # Notify callbacks of cancellation
        self._notify_callbacks()

    def is_cancelled(self) -> bool:
        """
        Check if operation has been cancelled.

        Returns:
            True if cancelled

        Thread-safe: Yes
        """
        with self._lock:
            return self.cancelled

    def is_complete(self) -> bool:
        """
        Check if operation is complete.

        Returns:
            True if all items processed

        Thread-safe: Yes
        """
        with self._lock:
            return self.items_processed >= self.total_items

    def reset(self) -> None:
        """
        Reset progress tracker to initial state.

        Thread-safe: Yes
        """
        with self._lock:
            self.items_processed = 0
            self.current_item = None
            self.cancelled = False
            self._start_time = time.time()
            self._last_update_time = self._start_time

    def update_description(self, description: str) -> None:
        """
        Update operation description.

        Args:
            description: New description

        Thread-safe: Yes
        """
        with self._lock:
            self.description = description

    def get_status(self) -> dict[str, Any]:
        """
        Get complete status dictionary.

        Returns:
            Dictionary with all progress information

        Thread-safe: Yes
        """
        with self._lock:
            status = {
                "items_processed": self.items_processed,
                "total_items": self.total_items,
                "percentage": self.percentage,
                "current_item": self.current_item,
                "description": self.description,
                "elapsed_time": self.get_elapsed_time(),
                "eta": self.get_eta(),
                "throughput": self.get_throughput(),
                "cancelled": self.cancelled,
                "complete": self.is_complete(),
            }

        return status

    def _notify_callbacks(self) -> None:
        """
        Notify all registered callbacks of progress update.

        Handles callback errors gracefully without stopping progress tracking.
        """
        status = self.get_status()

        # Get callbacks to notify (copy to avoid lock during callbacks)
        with self._lock:
            callbacks = list(self._callbacks)

        # Call callbacks outside lock to prevent deadlock
        for callback in callbacks:
            try:
                callback(status)
            except Exception as e:
                self.logger.error(f"Progress callback failed: {e}")

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager, marking as complete."""
        if not self.is_cancelled() and not self.is_complete():
            # Auto-complete if not already done
            with self._lock:
                self.items_processed = self.total_items
            self._notify_callbacks()

        return False  # Don't suppress exceptions
