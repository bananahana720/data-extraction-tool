"""
Resource Edge Case Tests for CLI.

Tests resource-related boundary conditions including:
- Very large files (100MB+)
- Very small files (empty, 1 byte)
- Many small files in batch
- Few large files in batch
- Files causing high memory usage
- Empty files
- Single character files
- Malformed but parseable files

Design: Equivalency partitioning methodology
Status: v1.0.2 edge case validation
"""

import tempfile
from pathlib import Path
import pytest

from cli.main import cli
from click.testing import CliRunner


class TestResourceEdgeCases:
    """Test resource-related edge cases."""

    @pytest.fixture
    def runner(self):
        """Create CLI runner."""
        return CliRunner()

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    # Category: Negative - Very Small Files
    def test_empty_file(self, runner, temp_output_dir):
        """1. PASS: Completely empty file (0 bytes)."""
        test_file = temp_output_dir / "empty.txt"
        test_file.write_text("")  # 0 bytes

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # Should handle gracefully
        assert result.exit_code == 0, f"Failed with empty file: {result.output}"
        assert output_file.exists()

    def test_single_byte_file(self, runner, temp_output_dir):
        """2. PASS: File with single byte."""
        test_file = temp_output_dir / "single_byte.txt"
        test_file.write_text("a")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with single byte: {result.output}"

    def test_single_line_file(self, runner, temp_output_dir):
        """3. PASS: File with single line, no newline."""
        test_file = temp_output_dir / "single_line.txt"
        test_file.write_text("Single line without newline")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with single line: {result.output}"

    def test_only_newlines_file(self, runner, temp_output_dir):
        """4. PASS: File containing only newlines."""
        test_file = temp_output_dir / "only_newlines.txt"
        test_file.write_text("\n\n\n\n\n")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with only newlines: {result.output}"

    def test_only_whitespace_file(self, runner, temp_output_dir):
        """5. PASS: File containing only whitespace."""
        test_file = temp_output_dir / "only_whitespace.txt"
        test_file.write_text("     \t\t\t     \n     \t     ")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with only whitespace: {result.output}"

    # Category: Performance - Large Files
    def test_large_text_file_5mb(self, runner, temp_output_dir):
        """6. PASS: Large text file (5MB)."""
        # Generate 5MB of text
        line = "This is a line of test content for the large file.\n"
        num_lines = (5 * 1024 * 1024) // len(line)  # 5MB worth of lines

        test_file = temp_output_dir / "large_5mb.txt"
        with open(test_file, "w") as f:
            for _ in range(num_lines):
                f.write(line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with 5MB file: {result.output}"
        assert output_file.exists()

    def test_large_text_file_10mb(self, runner, temp_output_dir):
        """7. PASS: Large text file (10MB)."""
        # Generate 10MB of text
        line = "This is a line of test content for the large file.\n"
        num_lines = (10 * 1024 * 1024) // len(line)  # 10MB

        test_file = temp_output_dir / "large_10mb.txt"
        with open(test_file, "w") as f:
            for _ in range(num_lines):
                f.write(line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with 10MB file: {result.output}"

    @pytest.mark.slow
    def test_very_large_text_file_50mb(self, runner, temp_output_dir):
        """8. PASS: Very large text file (50MB)."""
        # Generate 50MB of text
        line = "This is a line of test content for the very large file.\n"
        num_lines = (50 * 1024 * 1024) // len(line)  # 50MB

        test_file = temp_output_dir / "large_50mb.txt"
        with open(test_file, "w") as f:
            for _ in range(num_lines):
                f.write(line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # Should handle or fail gracefully with clear error
        if result.exit_code != 0:
            assert (
                "memory" in result.output.lower()
                or "too large" in result.output.lower()
                or "size" in result.output.lower()
            )
        else:
            assert output_file.exists()

    @pytest.mark.slow
    @pytest.mark.skipif(True, reason="100MB test only run manually due to size")
    def test_extremely_large_file_100mb(self, runner, temp_output_dir):
        """9. PASS/FAIL: Extremely large text file (100MB) - Manual test only."""
        # Generate 100MB of text
        line = "This is a line of test content for the extremely large file.\n"
        num_lines = (100 * 1024 * 1024) // len(line)  # 100MB

        test_file = temp_output_dir / "large_100mb.txt"
        with open(test_file, "w") as f:
            for _ in range(num_lines):
                f.write(line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # Should handle or fail gracefully
        if result.exit_code != 0:
            assert "memory" in result.output.lower() or "too large" in result.output.lower()
        else:
            assert output_file.exists()

    # Category: Integration - Many Small Files
    def test_batch_many_tiny_files(self, runner, temp_output_dir):
        """10. PASS: Batch of 100 tiny files (minimal content)."""
        for i in range(100):
            tiny_file = temp_output_dir / f"tiny_{i:04d}.txt"
            tiny_file.write_text(f"File {i}")

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

        assert result.exit_code == 0, f"Failed with many tiny files: {result.output}"

        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 100, f"Expected 100 outputs, got {len(output_files)}"

    def test_batch_many_empty_files(self, runner, temp_output_dir):
        """11. PASS: Batch of 50 empty files."""
        for i in range(50):
            empty_file = temp_output_dir / f"empty_{i:04d}.txt"
            empty_file.write_text("")

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

        assert result.exit_code == 0, f"Failed with many empty files: {result.output}"

    # Category: Integration - Few Large Files
    def test_batch_few_large_files(self, runner, temp_output_dir):
        """12. PASS: Batch of 3 large files (10MB each)."""
        line = "This is a line of test content.\n"
        num_lines = (10 * 1024 * 1024) // len(line)

        for i in range(3):
            large_file = temp_output_dir / f"large_{i:04d}.txt"
            with open(large_file, "w") as f:
                for _ in range(num_lines):
                    f.write(line)

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

        assert result.exit_code == 0, f"Failed with few large files: {result.output}"

        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 3, f"Expected 3 outputs, got {len(output_files)}"

    # Category: Negative - Very Long Lines
    def test_file_with_very_long_line(self, runner, temp_output_dir):
        """13. PASS: File with extremely long line (1MB single line)."""
        # Single line of 1MB
        long_line = "a" * (1024 * 1024)

        test_file = temp_output_dir / "long_line.txt"
        test_file.write_text(long_line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with very long line: {result.output}"

    def test_file_with_many_short_lines(self, runner, temp_output_dir):
        """14. PASS: File with very many short lines (100k lines)."""
        test_file = temp_output_dir / "many_lines.txt"
        with open(test_file, "w") as f:
            for i in range(100000):
                f.write(f"Line {i}\n")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with many lines: {result.output}"

    # Category: Negative - Repeated Content
    def test_file_with_highly_repetitive_content(self, runner, temp_output_dir):
        """15. PASS: File with highly repetitive content (compression test)."""
        # 10MB of same character
        repetitive = "a" * (10 * 1024 * 1024)

        test_file = temp_output_dir / "repetitive.txt"
        test_file.write_text(repetitive)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with repetitive content: {result.output}"

    # Category: Negative - Binary-like Text
    def test_file_with_binary_characters(self, runner, temp_output_dir):
        """16. PASS/FAIL: Text file with binary-like characters."""
        # Mix of printable and non-printable ASCII
        binary_text = "".join(chr(i) for i in range(32, 127))  # Printable ASCII
        binary_text += "".join(chr(i) for i in [0, 1, 2, 3, 127])  # Some control chars

        test_file = temp_output_dir / "binary_text.txt"
        test_file.write_bytes(binary_text.encode("latin-1"))

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # May succeed or fail depending on encoding detection
        if result.exit_code != 0:
            assert "encoding" in result.output.lower() or "decode" in result.output.lower()
        else:
            assert output_file.exists()

    # Category: Integration - Extreme Aspect Ratios
    def test_file_single_line_very_wide(self, runner, temp_output_dir):
        """17. PASS: Single very long line (extreme aspect ratio)."""
        # 100k character single line
        wide_line = "word " * 20000

        test_file = temp_output_dir / "wide.txt"
        test_file.write_text(wide_line)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with wide line: {result.output}"

    def test_file_many_lines_very_narrow(self, runner, temp_output_dir):
        """18. PASS: Many lines, each very short (extreme aspect ratio)."""
        test_file = temp_output_dir / "narrow.txt"
        with open(test_file, "w") as f:
            for i in range(50000):
                f.write("a\n")  # Single character per line

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with narrow lines: {result.output}"

    # Category: Security - Null Bytes
    def test_file_with_null_bytes(self, runner, temp_output_dir):
        """19. PASS/FAIL: File containing null bytes."""
        content = b"Text before null\x00Text after null\x00More text"

        test_file = temp_output_dir / "null_bytes.txt"
        test_file.write_bytes(content)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # May handle or reject null bytes
        if result.exit_code != 0:
            assert (
                "null" in result.output.lower()
                or "binary" in result.output.lower()
                or "invalid" in result.output.lower()
            )
        else:
            assert output_file.exists()

    # Category: Performance - Batch Memory Stress
    def test_batch_memory_stress_mixed_sizes(self, runner, temp_output_dir):
        """20. PASS: Batch designed to stress memory with mixed file sizes."""
        # 5 small files
        for i in range(5):
            (temp_output_dir / f"small_{i:04d}.txt").write_text("small")

        # 5 medium files (1MB each)
        medium_content = "x" * (1024 * 1024)
        for i in range(5):
            (temp_output_dir / f"medium_{i:04d}.txt").write_text(medium_content)

        # 2 large files (5MB each)
        large_content = "y" * (5 * 1024 * 1024)
        for i in range(2):
            (temp_output_dir / f"large_{i:04d}.txt").write_text(large_content)

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

        assert result.exit_code == 0, f"Failed with memory stress: {result.output}"

        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) == 12, f"Expected 12 outputs, got {len(output_files)}"
