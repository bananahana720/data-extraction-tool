"""
Threading Edge Case Tests for CLI Batch Processing.

Tests thread pool edge conditions including:
- Batch with 1 file (minimal threading)
- Batch with 100+ files (heavy threading)
- Batch with simulated slow files
- Batch where some files fail
- Batch where all files fail
- Worker count variations
- Thread safety under stress

Design: Equivalency partitioning methodology
Status: v1.0.2 edge case validation
"""

import tempfile
import time
from pathlib import Path
import pytest

from cli.main import cli
from click.testing import CliRunner


class TestThreadingEdgeCases:
    """Test threading-related edge cases in batch processing."""

    @pytest.fixture
    def runner(self):
        """Create CLI runner."""
        return CliRunner()

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def create_test_files(self, count: int, temp_dir: Path, file_prefix="test") -> list[Path]:
        """Helper to create multiple test files."""
        files = []
        for i in range(count):
            file_path = temp_dir / f"{file_prefix}_{i:04d}.txt"
            file_path.write_text(f"Test content for file {i}\nLine 2\nLine 3\n")
            files.append(file_path)
        return files

    # Category: Happy Path - Minimal Threading
    def test_batch_single_file(self, runner, temp_output_dir):
        """1. PASS: Batch processing with only 1 file (edge of threading)."""
        files = self.create_test_files(1, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        assert result.exit_code == 0, f"Single file batch failed: {result.output}"
        # Should still work with thread pool
        assert (output_dir / "test_0000.json").exists()

    def test_batch_two_files(self, runner, temp_output_dir):
        """2. PASS: Batch with 2 files (minimal parallel execution)."""
        files = self.create_test_files(2, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "2",
            ],
        )

        assert result.exit_code == 0, f"Two file batch failed: {result.output}"
        assert (output_dir / "test_0000.json").exists()
        assert (output_dir / "test_0001.json").exists()

    # Category: Performance - Heavy Threading
    def test_batch_many_files_low_workers(self, runner, temp_output_dir):
        """3. PASS: 50 files with only 1 worker (serial processing)."""
        files = self.create_test_files(50, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "1",
            ],
        )

        assert result.exit_code == 0, f"Many files/low workers failed: {result.output}"

        # Verify all files processed
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 50, f"Expected 50 outputs, got {len(output_files)}"

    def test_batch_many_files_high_workers(self, runner, temp_output_dir):
        """4. PASS: 50 files with 16 workers (heavy parallelism)."""
        files = self.create_test_files(50, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "16",
            ],
        )

        assert result.exit_code == 0, f"Many files/high workers failed: {result.output}"

        # Verify all files processed
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 50, f"Expected 50 outputs, got {len(output_files)}"

    def test_batch_100_plus_files(self, runner, temp_output_dir):
        """5. PASS: 100+ files to stress thread pool."""
        # Create 120 files
        files = self.create_test_files(120, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "8",
            ],
        )

        assert result.exit_code == 0, f"100+ files batch failed: {result.output}"

        # Verify all files processed
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 120, f"Expected 120 outputs, got {len(output_files)}"

    # Category: Negative - Worker Count Edge Cases
    def test_batch_workers_greater_than_files(self, runner, temp_output_dir):
        """6. PASS: More workers than files (worker count > file count)."""
        files = self.create_test_files(3, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "10",  # More workers than files
            ],
        )

        assert result.exit_code == 0, f"Workers > files failed: {result.output}"

        # Should still work, just with idle workers
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 3

    def test_batch_zero_workers_rejected(self, runner, temp_output_dir):
        """7. FAIL-EXPECTED: Zero workers should be rejected."""
        files = self.create_test_files(5, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "0",
            ],
        )

        # Should fail gracefully
        assert result.exit_code != 0, "Zero workers should be rejected"
        assert "error" in result.output.lower() or "invalid" in result.output.lower()

    def test_batch_negative_workers_rejected(self, runner, temp_output_dir):
        """8. FAIL-EXPECTED: Negative workers should be rejected."""
        files = self.create_test_files(5, temp_output_dir)
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "-1",
            ],
        )

        # Should fail gracefully
        assert result.exit_code != 0, "Negative workers should be rejected"

    # Category: Negative - Mixed Success/Failure
    def test_batch_with_some_corrupted_files(self, runner, temp_output_dir):
        """9. PASS: Batch where some files are corrupted but others succeed."""
        # Create mix of good and bad files
        good_files = self.create_test_files(5, temp_output_dir, "good")

        # Create corrupted files (empty or invalid)
        for i in range(5):
            bad_file = temp_output_dir / f"bad_{i:04d}.docx"
            bad_file.write_bytes(b"\x00" * 100)  # Invalid DOCX

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        # Should complete with partial success
        # The tool should continue processing despite failures
        assert result.exit_code == 0 or "processed" in result.output.lower()

        # At least the good files should be processed
        output_files = list(output_dir.glob("good_*.json"))
        assert len(output_files) >= 3, "Should process at least some good files"

    def test_batch_all_files_fail(self, runner, temp_output_dir):
        """10. PASS/FAIL: Batch where ALL files fail to process."""
        # Create only corrupted files
        for i in range(10):
            bad_file = temp_output_dir / f"corrupted_{i:04d}.docx"
            bad_file.write_bytes(b"\xFF\xFE" * 50)  # Invalid content

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        # Should complete but indicate failures
        # Exit code might be 0 (batch completed) or non-zero (all failed)
        assert (
            "error" in result.output.lower()
            or "failed" in result.output.lower()
            or result.exit_code != 0
        )

    # Category: Performance - Large Individual Files
    def test_batch_with_large_files(self, runner, temp_output_dir):
        """11. PASS: Batch with several large text files."""
        # Create large files (5MB each)
        large_content = "Line of text\n" * 100000  # ~5MB

        for i in range(5):
            large_file = temp_output_dir / f"large_{i:04d}.txt"
            large_file.write_text(large_content)

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "2",  # Limited workers for memory
            ],
        )

        assert result.exit_code == 0, f"Large files batch failed: {result.output}"

        output_files = list(output_dir.glob("large_*.json"))
        assert len(output_files) == 5, f"Expected 5 outputs, got {len(output_files)}"

    # Category: Integration - Mixed File Sizes
    def test_batch_mixed_file_sizes(self, runner, temp_output_dir):
        """12. PASS: Batch with mix of tiny, small, medium, large files."""
        # Tiny files
        for i in range(10):
            (temp_output_dir / f"tiny_{i:04d}.txt").write_text("a")

        # Small files
        for i in range(10):
            (temp_output_dir / f"small_{i:04d}.txt").write_text("test\n" * 100)

        # Medium files
        for i in range(5):
            (temp_output_dir / f"medium_{i:04d}.txt").write_text("test\n" * 10000)

        # Large files
        for i in range(2):
            (temp_output_dir / f"large_{i:04d}.txt").write_text("test\n" * 100000)

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "batch",
                str(temp_output_dir),
                "--output-dir",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        assert result.exit_code == 0, f"Mixed sizes batch failed: {result.output}"

        # Should process all files
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 27, f"Expected 27 outputs, got {len(output_files)}"

    # Category: Performance - Stress Test
    def test_batch_rapid_succession(self, runner, temp_output_dir):
        """13. PASS: Multiple batch operations in rapid succession."""
        # Create files for multiple batches
        batch1_dir = temp_output_dir / "batch1"
        batch2_dir = temp_output_dir / "batch2"
        batch1_dir.mkdir()
        batch2_dir.mkdir()

        self.create_test_files(20, batch1_dir, "batch1")
        self.create_test_files(20, batch2_dir, "batch2")

        output1_dir = temp_output_dir / "output1"
        output2_dir = temp_output_dir / "output2"
        output1_dir.mkdir()
        output2_dir.mkdir()

        # Run first batch
        result1 = runner.invoke(
            cli,
            [
                "batch",
                str(batch1_dir),
                "--output-dir",
                str(output1_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        # Immediately run second batch
        result2 = runner.invoke(
            cli,
            [
                "batch",
                str(batch2_dir),
                "--output-dir",
                str(output2_dir),
                "--format",
                "json",
                "--workers",
                "4",
            ],
        )

        assert result1.exit_code == 0, "First batch failed"
        assert result2.exit_code == 0, "Second batch failed"

        assert len(list(output1_dir.glob("*.json"))) == 20
        assert len(list(output2_dir.glob("*.json"))) == 20

    # Category: Negative - Empty Batch
    def test_batch_empty_directory(self, runner, temp_output_dir):
        """14. FAIL/PASS: Batch processing empty directory."""
        empty_dir = temp_output_dir / "empty"
        empty_dir.mkdir()

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli, ["batch", str(empty_dir), "--output-dir", str(output_dir), "--format", "json"]
        )

        # Should handle gracefully - either success with warning or specific error
        assert "no files" in result.output.lower() or result.exit_code == 0

    def test_batch_directory_with_only_subdirs(self, runner, temp_output_dir):
        """15. PASS: Directory with subdirectories but no files at root."""
        # Create subdirectories with files
        (temp_output_dir / "subdir1").mkdir()
        (temp_output_dir / "subdir2").mkdir()

        (temp_output_dir / "subdir1" / "file1.txt").write_text("test 1")
        (temp_output_dir / "subdir2" / "file2.txt").write_text("test 2")

        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            ["batch", str(temp_output_dir), "--output-dir", str(output_dir), "--format", "json"],
        )

        # Behavior depends on whether batch command recursively processes
        # Either way should not crash
        assert result.exit_code == 0 or "no files" in result.output.lower()
