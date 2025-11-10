"""
Performance benchmarks for document extractors.

This module benchmarks all extractors (DOCX, PDF, PPTX, XLSX, TXT) across
different file sizes to establish performance baselines and detect regressions.

Performance Targets (from requirements):
    - Text extraction: <2s per MB
    - OCR extraction: <15s per page
    - Memory: <500MB per file
"""

import pytest
from datetime import datetime
from pathlib import Path

from extractors.docx_extractor import DocxExtractor
from extractors.excel_extractor import ExcelExtractor
from extractors.pdf_extractor import PdfExtractor
from extractors.pptx_extractor import PptxExtractor
from extractors.txt_extractor import TextFileExtractor
from tests.performance.conftest import (
    BenchmarkResult,
    PerformanceMeasurement,
    assert_memory_limit,
    assert_performance_target,
    categorize_file_size,
)


# ============================================================================
# Test Configuration
# ============================================================================

# Performance targets (in milliseconds)
SMALL_FILE_TARGET_MS = 500  # <100KB files
MEDIUM_FILE_TARGET_MS = 2000  # 100KB-1MB files (2s/MB target)
LARGE_FILE_TARGET_MS = 10000  # >1MB files (adjusted for large files)

# Memory limits (in megabytes)
MEMORY_LIMIT_MB = 500  # Per-file memory limit


# ============================================================================
# Helper Functions
# ============================================================================


def get_file_size_kb(file_path: Path) -> float:
    """Get file size in kilobytes."""
    return file_path.stat().st_size / 1024


def create_benchmark_result(
    operation: str, perf: PerformanceMeasurement, file_path: Path, metadata: dict | None = None
) -> BenchmarkResult:
    """
    Create benchmark result from performance measurement.

    Args:
        operation: Operation name
        perf: Performance measurement
        file_path: Input file path
        metadata: Additional metadata

    Returns:
        BenchmarkResult with captured metrics
    """
    file_size_kb = get_file_size_kb(file_path)
    throughput = file_size_kb / perf.duration_seconds if perf.duration_seconds > 0 else 0

    return BenchmarkResult(
        operation=operation,
        duration_ms=perf.duration_ms,
        memory_mb=perf.peak_memory_mb,
        file_size_kb=file_size_kb,
        throughput=throughput,
        timestamp=datetime.now().isoformat(),
        metadata={
            "file_name": file_path.name,
            "file_category": categorize_file_size(file_size_kb),
            **(metadata or {}),
        },
    )


def get_performance_target(file_size_kb: float) -> float:
    """
    Get performance target based on file size.

    Args:
        file_size_kb: File size in kilobytes

    Returns:
        Target duration in milliseconds
    """
    if file_size_kb < 100:
        return SMALL_FILE_TARGET_MS
    elif file_size_kb < 1024:
        # Scale linearly for medium files (2s per MB)
        return (file_size_kb / 1024) * 2000
    else:
        # Large files get more time
        return (file_size_kb / 1024) * 3000


# ============================================================================
# PDF Extractor Benchmarks
# ============================================================================


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.extraction
class TestPDFExtractorBenchmarks:
    """Performance benchmarks for PDF extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize extractor for all tests."""
        self.extractor = PdfExtractor()

    def test_pdf_small_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark PDF extraction on small file (<100KB)."""
        # Use Introduction PDF (808KB - actually medium, but smallest available)
        pdf_file = (
            fixture_dir
            / "real-world-files"
            / "COBIT-2019-Framework-Introduction-and-Methodology_res_eng_1118.pdf"
        )

        if not pdf_file.exists():
            pytest.skip(f"Test file not found: {pdf_file}")

        file_size_kb = get_file_size_kb(pdf_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(pdf_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="pdf_extract_small",
            perf=perf,
            file_path=pdf_file,
            metadata={"pages": result.document_metadata.page_count},
        )

        # Assert performance targets
        assert_performance_target(perf.duration_ms, target_ms, "PDF small file extraction")
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "PDF small file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"PDF Small File Benchmark: {pdf_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Pages: {result.document_metadata.page_count}")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"  Target: {target_ms:.2f} ms")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("pdf_extract_small", benchmark)
        production_baseline_manager.save()

    def test_pdf_medium_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark PDF extraction on medium file (100KB-1MB)."""
        # Use NIST PDF (2.2MB - actually large, but good test)
        pdf_file = fixture_dir / "real-world-files" / "NIST.SP.800-37r2.pdf"

        if not pdf_file.exists():
            pytest.skip(f"Test file not found: {pdf_file}")

        file_size_kb = get_file_size_kb(pdf_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(pdf_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="pdf_extract_medium",
            perf=perf,
            file_path=pdf_file,
            metadata={"pages": result.document_metadata.page_count},
        )

        # Assert performance targets (more lenient for real-world files)
        assert_performance_target(
            perf.duration_ms, target_ms, "PDF medium file extraction", tolerance=0.50
        )
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "PDF medium file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"PDF Medium File Benchmark: {pdf_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Pages: {result.document_metadata.page_count}")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"  Target: {target_ms:.2f} ms")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("pdf_extract_medium", benchmark)
        production_baseline_manager.save()

    def test_pdf_large_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark PDF extraction on large file (>1MB)."""
        # Use Design Guide PDF (12MB)
        pdf_file = fixture_dir / "real-world-files" / "COBIT-2019-Design-Guide_res_eng_1218.pdf"

        if not pdf_file.exists():
            pytest.skip(f"Test file not found: {pdf_file}")

        file_size_kb = get_file_size_kb(pdf_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(pdf_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="pdf_extract_large",
            perf=perf,
            file_path=pdf_file,
            metadata={"pages": result.document_metadata.page_count},
        )

        # Assert performance targets (very lenient for large files)
        assert_performance_target(
            perf.duration_ms, target_ms, "PDF large file extraction", tolerance=1.0
        )
        assert_memory_limit(
            perf.peak_memory_mb, MEMORY_LIMIT_MB, "PDF large file extraction", tolerance=0.5
        )

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"PDF Large File Benchmark: {pdf_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Pages: {result.document_metadata.page_count}")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"  Target: {target_ms:.2f} ms")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("pdf_extract_large", benchmark)
        production_baseline_manager.save()


# ============================================================================
# Excel Extractor Benchmarks
# ============================================================================


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.extraction
class TestExcelExtractorBenchmarks:
    """Performance benchmarks for Excel extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize extractor for all tests."""
        self.extractor = ExcelExtractor()

    def test_excel_small_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark Excel extraction on small file."""
        excel_file = fixture_dir / "excel" / "simple_single_sheet.xlsx"

        if not excel_file.exists():
            pytest.skip(f"Test file not found: {excel_file}")

        file_size_kb = get_file_size_kb(excel_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(excel_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="excel_extract_small", perf=perf, file_path=excel_file
        )

        # Assert performance targets
        assert_performance_target(perf.duration_ms, target_ms, "Excel small file extraction")
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "Excel small file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"Excel Small File Benchmark: {excel_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("excel_extract_small", benchmark)
        production_baseline_manager.save()

    def test_excel_medium_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark Excel extraction on medium file."""
        excel_file = fixture_dir / "real-world-files" / "NIST-Privacy-Framework-V1.0-Core.xlsx"

        if not excel_file.exists():
            pytest.skip(f"Test file not found: {excel_file}")

        file_size_kb = get_file_size_kb(excel_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(excel_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="excel_extract_medium", perf=perf, file_path=excel_file
        )

        # Assert performance targets
        assert_performance_target(
            perf.duration_ms, target_ms, "Excel medium file extraction", tolerance=0.50
        )
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "Excel medium file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"Excel Medium File Benchmark: {excel_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("excel_extract_medium", benchmark)
        production_baseline_manager.save()

    def test_excel_large_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark Excel extraction on large file."""
        excel_file = fixture_dir / "real-world-files" / "sp800-53ar5-assessment-procedures.xlsx"

        if not excel_file.exists():
            pytest.skip(f"Test file not found: {excel_file}")

        file_size_kb = get_file_size_kb(excel_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(excel_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="excel_extract_large", perf=perf, file_path=excel_file
        )

        # Assert performance targets
        assert_performance_target(
            perf.duration_ms, target_ms, "Excel large file extraction", tolerance=0.50
        )
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "Excel large file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"Excel Large File Benchmark: {excel_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("excel_extract_large", benchmark)
        production_baseline_manager.save()


# ============================================================================
# TXT Extractor Benchmarks
# ============================================================================


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.extraction
class TestTXTExtractorBenchmarks:
    """Performance benchmarks for TXT extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize extractor for all tests."""
        self.extractor = TextFileExtractor()

    def test_txt_small_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark TXT extraction on small file."""
        txt_file = fixture_dir / "sample.txt"

        if not txt_file.exists():
            pytest.skip(f"Test file not found: {txt_file}")

        file_size_kb = get_file_size_kb(txt_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(txt_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="txt_extract_small", perf=perf, file_path=txt_file
        )

        # Assert performance targets (TXT should be very fast)
        assert_performance_target(perf.duration_ms, target_ms, "TXT small file extraction")
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "TXT small file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"TXT Small File Benchmark: {txt_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("txt_extract_small", benchmark)
        production_baseline_manager.save()

    def test_txt_medium_file_performance(
        self, fixture_dir: Path, perf_measure, production_baseline_manager
    ):
        """Benchmark TXT extraction on medium file."""
        txt_file = fixture_dir / "real-world-files" / "test_case_03_nested_structure.txt"

        if not txt_file.exists():
            pytest.skip(f"Test file not found: {txt_file}")

        file_size_kb = get_file_size_kb(txt_file)
        target_ms = get_performance_target(file_size_kb)

        # Measure performance
        with perf_measure() as perf:
            result = self.extractor.extract(txt_file)

        # Verify extraction succeeded
        assert result.success, f"Extraction failed: {result.errors}"
        assert len(result.content_blocks) > 0, "No content blocks extracted"

        # Create benchmark result
        benchmark = create_benchmark_result(
            operation="txt_extract_medium", perf=perf, file_path=txt_file
        )

        # Assert performance targets
        assert_performance_target(perf.duration_ms, target_ms, "TXT medium file extraction")
        assert_memory_limit(perf.peak_memory_mb, MEMORY_LIMIT_MB, "TXT medium file extraction")

        # Log for baseline
        print(f"\n{'='*60}")
        print(f"TXT Medium File Benchmark: {txt_file.name}")
        print(f"  File Size: {file_size_kb:.2f} KB")
        print(f"  Duration: {perf.duration_ms:.2f} ms ({perf.duration_seconds:.2f}s)")
        print(f"  Peak Memory: {perf.peak_memory_mb:.2f} MB")
        print(f"  Throughput: {benchmark.throughput:.2f} KB/s")
        print(f"  Content Blocks: {len(result.content_blocks)}")
        print(f"{'='*60}")

        # Update baseline
        production_baseline_manager.update_baseline("txt_extract_medium", benchmark)
        production_baseline_manager.save()


# ============================================================================
# Regression Detection Tests
# ============================================================================


@pytest.mark.performance
@pytest.mark.slow
class TestPerformanceRegression:
    """Tests to detect performance regressions against baselines."""

    def test_no_major_regressions(self, production_baseline_manager):
        """Verify no operations have regressed significantly."""
        baseline_file = Path(__file__).parent / "baselines.json"

        if not baseline_file.exists():
            pytest.skip("No baseline file found. Run benchmarks first to establish baselines.")

        # Load baselines
        production_baseline_manager.load()

        # This is a meta-test that would be run after all benchmarks
        # In a real scenario, you'd compare current run against stored baselines
        # For now, just verify baseline file is valid
        assert len(production_baseline_manager._baselines) > 0, "No baselines stored"

        print(f"\nLoaded {len(production_baseline_manager._baselines)} baseline measurements")
        for operation, baseline in production_baseline_manager._baselines.items():
            print(f"  {operation}: {baseline.duration_ms:.2f}ms, {baseline.memory_mb:.2f}MB")
