"""
Performance tests for NFR-P1 and NFR-P2 validation using GREENFIELD architecture.

Story 2.5-2.1: Pipeline Throughput Optimization

These tests validate:
- NFR-P1: 100 mixed-format files process in <10 minutes (with ProcessPoolExecutor)
- NFR-P2: Peak memory <2GB during batch processing (including all workers)
- Memory leak detection
- ADR-005 streaming architecture validation
- ADR-006 continue-on-error with parallel execution

BASELINE (Story 2.5-2.1, 2025-11-12):
- Throughput: 14.57 files/min (ProcessPoolExecutor, 4 workers)
- Duration: 6.86 minutes for 100-file batch
- Memory: 4.15GB peak (exceeds 2GB target)
- Success: 99% (99/100 files)
- OCR Quality: 95.26% average confidence

ARCHITECTURE: Uses greenfield extractors (src/data_extract/) with ProcessPoolExecutor

Usage:
    pytest -m performance tests/performance/test_throughput.py -v
    pytest tests/performance/test_throughput.py::test_batch_throughput_100_files -v
"""

import sys
import time
from pathlib import Path

import pytest

# Add project root to path (greenfield uses absolute imports with src. prefix)
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import parallelized batch processing from profile_pipeline
from scripts.profile_pipeline import (  # noqa: E402
    BatchResult,
    get_total_memory,
    process_batch,
)


@pytest.fixture(scope="module")
def batch_100_files():
    """Collect all files from the 100-file test batch."""
    batch_dir = PROJECT_ROOT / "tests" / "performance" / "batch_100_files"

    if not batch_dir.exists():
        pytest.skip(
            f"Batch directory not found: {batch_dir}. Run: python scripts/create_performance_batch.py"
        )

    # Collect all files from subdirectories
    files = []
    for subdir in ["pdfs", "docx", "xlsx", "mixed"]:
        subdir_path = batch_dir / subdir
        if subdir_path.exists():
            files.extend(list(subdir_path.glob("*")))

    files = [f for f in files if f.is_file()]

    if len(files) < 100:
        pytest.skip(
            f"Expected 100 files, found {len(files)}. Run: python scripts/create_performance_batch.py"
        )

    return files


@pytest.mark.performance
@pytest.mark.slow
def test_batch_throughput_100_files(batch_100_files):
    """
    Validate NFR-P1: Process 100 mixed-format files in <10 minutes with parallelization.

    Acceptance Criteria:
    - 100 files complete in <10 minutes (600 seconds)
    - Sustained throughput >=10 files/minute
    - Measured with real timer, not estimates
    - Uses ProcessPoolExecutor with 4 workers (default)

    Baseline (Story 2.5.1 - Sequential): 5.87 files/min (17.05 minutes) - FAIL
    Optimized (Story 2.5.2.1 - 4 workers): 14.57 files/min (6.86 minutes) - PASS
    Hardware: 4 workers (ProcessPoolExecutor) - throughput-optimized
    Note: 4 workers exceeds NFR-P2 memory limit (4.15GB vs 2GB target) - documented trade-off
    """
    # Record start time
    start_time = time.time()

    # Process batch using greenfield extractors with parallelization
    # Uses 4 workers to meet NFR-P1 (throughput) - NFR-P2 (memory) trade-off documented
    results = process_batch(batch_100_files, worker_count=4)

    # Record end time
    end_time = time.time()

    # Calculate metrics
    elapsed_seconds = end_time - start_time
    elapsed_minutes = elapsed_seconds / 60
    throughput_files_per_minute = len(batch_100_files) / elapsed_minutes

    # Count successful/failed
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful

    # Print results for baseline documentation
    print(f"\n{'=' * 70}")
    print("THROUGHPUT TEST RESULTS (NFR-P1) - PARALLELIZED")
    print(f"{'=' * 70}")
    print("Worker Processes:  4 (ProcessPoolExecutor - throughput-optimized)")
    print(f"Files Processed:   {len(results)}/{len(batch_100_files)}")
    print(f"Successful:        {successful}")
    print(f"Failed:            {failed}")
    print(f"Total Time:        {elapsed_minutes:.2f} minutes ({elapsed_seconds:.2f}s)")
    print(f"Throughput:        {throughput_files_per_minute:.2f} files/min")
    print("NFR-P1 Target:     <10 minutes (>=10 files/min)")
    print(f"NFR-P1 Status:     {'PASS' if elapsed_minutes < 10 else 'FAIL'}")
    print(
        f"Improvement:       {(throughput_files_per_minute / 5.87 - 1) * 100:.1f}% vs baseline (5.87 files/min)"
    )
    print(f"{'=' * 70}\n")

    # Assertions
    assert len(results) == len(
        batch_100_files
    ), f"Expected {len(batch_100_files)} results, got {len(results)}"
    assert elapsed_minutes < 10, (
        f"NFR-P1 FAILED: Processing took {elapsed_minutes:.2f} minutes (target: <10 min). "
        f"Throughput: {throughput_files_per_minute:.2f} files/min (target: >=10 files/min). "
        f"Baseline: 5.87 files/min (Story 2.5.1)"
    )


@pytest.mark.performance
@pytest.mark.slow
def test_memory_usage_within_limits(batch_100_files):
    """
    Validate NFR-P2: Peak memory <2GB during batch processing (all workers).

    Acceptance Criteria:
    - Peak memory <2048MB (2GB) during 100-file batch
    - Measured with psutil monitoring main + all worker processes
    - Validates ADR-005 streaming architecture with parallelization

    Baseline (Story 2.5.1 - Sequential): 1,734 MB peak - PASS
    Optimized (Story 2.5.2.1 - 4 workers): 4,247 MB peak - FAIL (exceeds 2GB target)
    Trade-off: 4 workers required for NFR-P1 throughput, memory optimization deferred
    """
    # Record baseline memory (main process only initially)
    baseline_memory = get_total_memory() / (1024 * 1024)  # MB
    peak_memory = baseline_memory

    # Track memory during processing (main + all workers)
    files_processed = 0

    def memory_tracker(result: BatchResult):
        nonlocal peak_memory, files_processed
        current_memory = get_total_memory() / (1024 * 1024)  # MB (main + workers)
        peak_memory = max(peak_memory, current_memory)
        files_processed += 1

    # Process batch with memory monitoring (4 workers for throughput)
    _ = process_batch(batch_100_files, progress_callback=memory_tracker, worker_count=4)

    # Record final memory
    final_memory = get_total_memory() / (1024 * 1024)  # MB

    # Print results
    print(f"\n{'=' * 70}")
    print("MEMORY USAGE TEST RESULTS (NFR-P2) - PARALLELIZED")
    print(f"{'=' * 70}")
    print("Worker Processes:  4 (ProcessPoolExecutor - throughput-optimized)")
    print(f"Baseline Memory:   {baseline_memory:.2f} MB")
    print(f"Peak Memory:       {peak_memory:.2f} MB (main + all workers)")
    print(f"Final Memory:      {final_memory:.2f} MB")
    print(f"Memory Delta:      {final_memory - baseline_memory:.2f} MB")
    print("NFR-P2 Target:     <2048 MB (2GB)")
    print(f"NFR-P2 Status:     {'PASS' if peak_memory < 2048 else 'FAIL'}")
    print(
        f"Headroom:          {2048 - peak_memory:.2f} MB ({((2048 - peak_memory) / 2048 * 100):.1f}%)"
    )
    print(f"{'=' * 70}\n")

    # Assertions
    assert peak_memory < 2048, (
        f"NFR-P2 FAILED: Peak memory {peak_memory:.2f}MB exceeds 2048MB target. "
        f"Memory across main + all worker processes exceeded limit. "
        f"ADR-005 streaming architecture may not be working with parallelization."
    )


@pytest.mark.performance
@pytest.mark.slow
def test_no_memory_leaks(batch_100_files):
    """
    Validate no memory leaks: memory returns to baseline after batch (with workers).

    Acceptance Criteria:
    - Memory returns to within 15% of baseline after processing (relaxed for workers)
    - Validates proper memory cleanup after worker pool shutdown
    - ADR-005 streaming with ProcessPoolExecutor: proper cleanup

    Note: Worker pool overhead may cause slightly higher baseline after first run.
    This is expected behavior (worker process startup/teardown).
    """
    # Record baseline memory before processing (main + any existing workers)
    baseline_memory = get_total_memory() / (1024 * 1024)  # MB

    # Process batch using greenfield extractors with parallelization (4 workers)
    _ = process_batch(batch_100_files, worker_count=4)

    # Record final memory after processing (workers should be cleaned up)
    final_memory = get_total_memory() / (1024 * 1024)  # MB

    # Calculate memory delta
    memory_delta = final_memory - baseline_memory
    memory_delta_pct = (memory_delta / baseline_memory) * 100 if baseline_memory > 0 else 0

    # Print results
    print(f"\n{'=' * 70}")
    print("MEMORY LEAK TEST RESULTS - PARALLELIZED")
    print(f"{'=' * 70}")
    print("Worker Processes:  4 (ProcessPoolExecutor with context manager cleanup)")
    print(f"Baseline Memory:   {baseline_memory:.2f} MB")
    print(f"Final Memory:      {final_memory:.2f} MB")
    print(f"Memory Delta:      {memory_delta:.2f} MB ({memory_delta_pct:+.1f}%)")
    print("Leak Threshold:    ±15% of baseline (relaxed for worker pool overhead)")
    print(
        f"Leak Status:       {'PASS (No leak detected)' if abs(memory_delta_pct) < 15 else 'WARNING (Possible leak)'}"
    )
    print(f"{'=' * 70}\n")

    # Assertion with 15% tolerance (relaxed for worker pool overhead)
    assert abs(memory_delta_pct) < 15, (
        f"Possible memory leak detected: {memory_delta_pct:+.1f}% change from baseline. "
        f"Baseline: {baseline_memory:.2f}MB, Final: {final_memory:.2f}MB, Delta: {memory_delta:+.2f}MB. "
        f"Worker pool should clean up memory after context manager exit."
    )


@pytest.mark.performance
def test_performance_batch_exists():
    """
    Verify 100-file test batch exists and is properly structured.

    This is a quick smoke test to ensure the batch is ready for performance testing.
    """
    batch_dir = PROJECT_ROOT / "tests" / "performance" / "batch_100_files"

    assert batch_dir.exists(), (
        f"Batch directory not found: {batch_dir}. "
        f"Run: python scripts/create_performance_batch.py"
    )

    # Check subdirectories
    subdirs = ["pdfs", "docx", "xlsx", "mixed"]
    for subdir in subdirs:
        subdir_path = batch_dir / subdir
        assert subdir_path.exists(), f"Subdirectory missing: {subdir_path}"

    # Count files
    all_files = [f for subdir in subdirs for f in (batch_dir / subdir).glob("*") if f.is_file()]

    assert len(all_files) == 100, (
        f"Expected 100 files, found {len(all_files)}. "
        f"Run: python scripts/create_performance_batch.py"
    )

    print(f"\n[OK] Performance batch ready: {len(all_files)} files in {batch_dir}\n")
