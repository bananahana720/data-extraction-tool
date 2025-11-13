"""
Tests for progress tracking infrastructure.

TDD approach - tests written first, implementation follows.
Target: >85% code coverage
"""

import threading
import time
from unittest.mock import Mock

# RED PHASE: These tests will fail until we implement progress_tracker module


def test_import_progress_tracker():
    """Test that progress_tracker module can be imported."""
    from src.infrastructure import progress_tracker

    assert progress_tracker is not None


def test_import_progress_tracker_class():
    """Test that ProgressTracker class exists."""
    from infrastructure.progress_tracker import ProgressTracker

    assert ProgressTracker is not None


def test_progress_tracker_initialization():
    """Test ProgressTracker can be initialized with total items."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    assert tracker.total_items == 100
    assert tracker.items_processed == 0
    assert tracker.percentage == 0.0


def test_progress_tracker_update():
    """Test ProgressTracker updates processed count."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    tracker.update(items_processed=25)

    assert tracker.items_processed == 25
    assert tracker.percentage == 25.0


def test_progress_tracker_update_with_current_item():
    """Test ProgressTracker tracks current item being processed."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=10)
    tracker.update(items_processed=5, current_item="file5.docx")

    assert tracker.current_item == "file5.docx"


def test_progress_tracker_percentage_calculation():
    """Test ProgressTracker calculates percentage correctly."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=200)

    tracker.update(items_processed=50)
    assert tracker.percentage == 25.0

    tracker.update(items_processed=100)
    assert tracker.percentage == 50.0

    tracker.update(items_processed=200)
    assert tracker.percentage == 100.0


def test_progress_tracker_handles_zero_total():
    """Test ProgressTracker handles zero total items gracefully."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=0)
    tracker.update(items_processed=0)

    assert tracker.percentage == 0.0


def test_progress_tracker_eta_calculation():
    """Test ProgressTracker calculates estimated time remaining."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    # Simulate some processing time
    tracker.update(items_processed=25)
    time.sleep(0.1)
    tracker.update(items_processed=50)

    # ETA should be available after processing has started
    eta = tracker.get_eta()
    assert eta is not None
    assert eta >= 0  # Should be non-negative


def test_progress_tracker_throughput():
    """Test ProgressTracker calculates items per second."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    tracker.update(items_processed=10)
    time.sleep(0.1)
    tracker.update(items_processed=20)

    throughput = tracker.get_throughput()
    assert throughput is not None
    assert throughput > 0


def test_progress_tracker_callback_on_update():
    """Test ProgressTracker calls callback on update."""
    from infrastructure.progress_tracker import ProgressTracker

    callback = Mock()
    tracker = ProgressTracker(total_items=100, callback=callback)

    tracker.update(items_processed=25)

    callback.assert_called_once()
    args = callback.call_args[0][0]
    assert args["items_processed"] == 25
    assert args["total_items"] == 100
    assert args["percentage"] == 25.0


def test_progress_tracker_multiple_callbacks():
    """Test ProgressTracker supports multiple callbacks."""
    from infrastructure.progress_tracker import ProgressTracker

    callback1 = Mock()
    callback2 = Mock()

    tracker = ProgressTracker(total_items=100)
    tracker.add_callback(callback1)
    tracker.add_callback(callback2)

    tracker.update(items_processed=50)

    callback1.assert_called_once()
    callback2.assert_called_once()


def test_progress_tracker_remove_callback():
    """Test ProgressTracker can remove callbacks."""
    from infrastructure.progress_tracker import ProgressTracker

    callback = Mock()
    tracker = ProgressTracker(total_items=100)
    tracker.add_callback(callback)
    tracker.remove_callback(callback)

    tracker.update(items_processed=50)

    callback.assert_not_called()


def test_progress_tracker_cancellation():
    """Test ProgressTracker supports cancellation."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    assert not tracker.is_cancelled()

    tracker.cancel()
    assert tracker.is_cancelled()


def test_progress_tracker_cancellation_callback():
    """Test ProgressTracker notifies callbacks on cancellation."""
    from infrastructure.progress_tracker import ProgressTracker

    callback = Mock()
    tracker = ProgressTracker(total_items=100, callback=callback)

    tracker.cancel()

    # Should have been called with cancellation info
    assert callback.called
    args = callback.call_args[0][0]
    assert args.get("cancelled") == True


def test_progress_tracker_reset():
    """Test ProgressTracker can be reset."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    tracker.update(items_processed=50)

    tracker.reset()

    assert tracker.items_processed == 0
    assert tracker.percentage == 0.0
    assert not tracker.is_cancelled()


def test_progress_tracker_thread_safety():
    """Test ProgressTracker is thread-safe for parallel operations."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=1000)
    errors = []

    def worker():
        try:
            for i in range(10):
                tracker.increment()  # Atomic increment
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    # Start multiple threads
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Should have processed 100 items (10 threads * 10 items)
    assert tracker.items_processed == 100
    assert len(errors) == 0


def test_progress_tracker_increment():
    """Test ProgressTracker supports atomic increment."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    tracker.increment()
    assert tracker.items_processed == 1

    tracker.increment()
    assert tracker.items_processed == 2


def test_progress_tracker_increment_by_n():
    """Test ProgressTracker can increment by N items."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    tracker.increment(5)
    assert tracker.items_processed == 5

    tracker.increment(10)
    assert tracker.items_processed == 15


def test_progress_tracker_elapsed_time():
    """Test ProgressTracker tracks elapsed time."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    time.sleep(0.1)
    tracker.update(items_processed=50)

    elapsed = tracker.get_elapsed_time()
    assert elapsed >= 0.1  # At least 100ms elapsed


def test_progress_tracker_completion_detection():
    """Test ProgressTracker detects when complete."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)

    assert not tracker.is_complete()

    tracker.update(items_processed=100)

    assert tracker.is_complete()
    assert tracker.percentage == 100.0


def test_progress_tracker_completion_callback():
    """Test ProgressTracker calls callback on completion."""
    from infrastructure.progress_tracker import ProgressTracker

    callback = Mock()
    tracker = ProgressTracker(total_items=100, callback=callback)

    tracker.update(items_processed=100)

    # Should have been called with completion info
    assert callback.called
    args = callback.call_args[0][0]
    assert args["percentage"] == 100.0
    assert args["complete"] == True


def test_progress_tracker_context_manager():
    """Test ProgressTracker can be used as context manager."""
    from infrastructure.progress_tracker import ProgressTracker

    callback = Mock()

    with ProgressTracker(total_items=10, callback=callback) as tracker:
        for i in range(10):
            tracker.increment()

    # Should be marked complete after context exit
    assert tracker.is_complete()


def test_progress_tracker_format_eta():
    """Test ProgressTracker formats ETA as human-readable string."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    tracker.update(items_processed=25)
    time.sleep(0.1)
    tracker.update(items_processed=50)

    eta_str = tracker.format_eta()
    assert eta_str is not None
    # Should contain time unit (seconds, minutes, etc.)
    assert any(unit in eta_str.lower() for unit in ["second", "minute", "hour"])


def test_progress_tracker_format_throughput():
    """Test ProgressTracker formats throughput as human-readable string."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    tracker.update(items_processed=50)
    time.sleep(0.1)
    tracker.update(items_processed=100)

    throughput_str = tracker.format_throughput()
    assert throughput_str is not None
    assert "items/sec" in throughput_str.lower() or "items per second" in throughput_str.lower()


def test_progress_tracker_get_status():
    """Test ProgressTracker returns complete status dictionary."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100)
    tracker.update(items_processed=50, current_item="file50.docx")

    status = tracker.get_status()

    assert status["items_processed"] == 50
    assert status["total_items"] == 100
    assert status["percentage"] == 50.0
    assert status["current_item"] == "file50.docx"
    assert "elapsed_time" in status
    assert "eta" in status
    assert "throughput" in status


def test_progress_tracker_callback_error_handling():
    """Test ProgressTracker handles callback errors gracefully."""
    from infrastructure.progress_tracker import ProgressTracker

    def failing_callback(status):
        raise Exception("Callback error")

    tracker = ProgressTracker(total_items=100, callback=failing_callback)

    # Should not raise exception, just log error
    tracker.update(items_processed=50)

    # Tracker should continue working
    assert tracker.items_processed == 50


def test_progress_tracker_with_description():
    """Test ProgressTracker supports operation description."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100, description="Extracting documents")

    assert tracker.description == "Extracting documents"

    status = tracker.get_status()
    assert status["description"] == "Extracting documents"


def test_progress_tracker_update_description():
    """Test ProgressTracker can update description during processing."""
    from infrastructure.progress_tracker import ProgressTracker

    tracker = ProgressTracker(total_items=100, description="Processing")

    tracker.update_description("Extracting content")
    assert tracker.description == "Extracting content"

    tracker.update_description("Formatting output")
    assert tracker.description == "Formatting output"
