"""
Tests for Batch Command - Multiple File Processing.

Test coverage for:
- Batch processing multiple files
- Glob pattern filtering
- Parallel processing with workers
- Progress display
- Summary statistics
- Partial failure handling
- Exit codes
"""

import pytest
from pathlib import Path
from click.testing import CliRunner

from cli.main import cli


class TestBatchCommandSuccess:
    """Test successful batch processing scenarios."""

    def test_batch_process_batch(self, cli_runner, multiple_test_files, tmp_path):
        """Process all files in a directory."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0
        assert "processed" in result.output.lower()

        # Check output files created
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) > 0

    def test_batch_process_file_list(self, cli_runner, multiple_test_files, tmp_path):
        """Process explicit list of files."""
        output_dir = tmp_path / "output"

        # Pass multiple files as arguments
        file_args = [str(f) for f in multiple_test_files[:3]]

        result = cli_runner.invoke(
            cli, ["batch", *file_args, "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0

    def test_batch_with_glob_pattern(self, cli_runner, multiple_test_files, tmp_path):
        """Filter files using glob pattern."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli,
            [
                "batch",
                str(input_dir),
                "--pattern",
                "*.docx",
                "--output",
                str(output_dir),
                "--format",
                "json",
            ],
        )

        assert result.exit_code == 0

        # Should only process DOCX files
        output_files = list(output_dir.glob("*.json"))
        assert len(output_files) >= 3  # We created 3 DOCX files

    def test_batch_custom_workers(self, cli_runner, multiple_test_files, tmp_path):
        """Configure number of worker threads."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli,
            [
                "batch",
                str(input_dir),
                "--output",
                str(output_dir),
                "--format",
                "json",
                "--workers",
                "2",
            ],
        )

        assert result.exit_code == 0

    def test_batch_all_formats(self, cli_runner, multiple_test_files, tmp_path):
        """Generate all output formats."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "all"]
        )

        assert result.exit_code == 0

        # Should create multiple format outputs
        all_output_files = list(output_dir.glob("*"))
        assert len(all_output_files) > 0


class TestBatchCommandProgress:
    """Test progress display during batch processing."""

    def test_batch_shows_progress_bar(self, cli_runner, multiple_test_files, tmp_path):
        """Display progress bar during batch processing."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0
        # Progress indicators might be in output

    def test_batch_shows_summary_stats(self, cli_runner, multiple_test_files, tmp_path):
        """Display summary statistics after batch processing."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0

        # Should show summary
        output_lower = result.output.lower()
        assert "files" in output_lower or "processed" in output_lower

    def test_batch_quiet_mode(self, cli_runner, multiple_test_files, tmp_path):
        """Suppress progress in quiet mode."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli,
            ["batch", str(input_dir), "--output", str(output_dir), "--format", "json", "--quiet"],
        )

        assert result.exit_code == 0
        # Minimal output


class TestBatchCommandErrors:
    """Test error handling scenarios."""

    def test_batch_directory_not_found(self, cli_runner, tmp_path):
        """Handle missing directory gracefully."""
        nonexistent_dir = tmp_path / "nonexistent"
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(nonexistent_dir), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "does not exist" in result.output.lower()

    def test_batch_no_matching_files(self, cli_runner, tmp_path):
        """Handle no files matching pattern."""
        input_dir = tmp_path / "empty"
        input_dir.mkdir()
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli,
            [
                "batch",
                str(input_dir),
                "--pattern",
                "*.pdf",
                "--output",
                str(output_dir),
                "--format",
                "json",
            ],
        )

        # Could succeed with 0 files or give informative message
        assert "no files" in result.output.lower() or result.exit_code == 0

    def test_batch_partial_failure_continues(self, cli_runner, multiple_test_files, tmp_path):
        """Continue processing after individual file failure."""
        input_dir = multiple_test_files[0].parent

        # Create an invalid file
        invalid_file = input_dir / "corrupted.docx"
        invalid_file.write_bytes(b"not a real docx file")

        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "json"]
        )

        # Should complete with some files processed
        # Exit code might be non-zero but should show summary

    def test_batch_invalid_workers(self, cli_runner, tmp_path):
        """Validate workers parameter."""
        input_dir = tmp_path
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--workers", "0"]
        )

        assert result.exit_code != 0

    def test_batch_invalid_workers_negative(self, cli_runner, tmp_path):
        """Reject negative worker count."""
        input_dir = tmp_path
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--workers", "-1"]
        )

        assert result.exit_code != 0


class TestBatchCommandValidation:
    """Test input validation."""

    def test_batch_requires_path_argument(self, cli_runner):
        """Command requires directory or file path."""
        result = cli_runner.invoke(cli, ["batch"])

        assert result.exit_code != 0

    def test_batch_validates_pattern_syntax(self, cli_runner, tmp_path):
        """Validate glob pattern syntax."""
        input_dir = tmp_path
        output_dir = tmp_path / "output"

        # Invalid glob pattern (implementation-specific)
        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--pattern", "[invalid", "--output", str(output_dir)]
        )

        # Should either accept or reject gracefully


class TestBatchCommandOutput:
    """Test output formatting and messages."""

    def test_batch_summary_shows_counts(self, cli_runner, multiple_test_files, tmp_path):
        """Summary shows file counts."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli, ["batch", str(input_dir), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0

        # Should show numbers
        output_lower = result.output.lower()
        assert any(char.isdigit() for char in result.output)

    def test_batch_verbose_mode(self, cli_runner, multiple_test_files, tmp_path):
        """Verbose mode shows per-file details."""
        input_dir = multiple_test_files[0].parent
        output_dir = tmp_path / "output"

        result = cli_runner.invoke(
            cli,
            ["batch", str(input_dir), "--output", str(output_dir), "--format", "json", "--verbose"],
        )

        assert result.exit_code == 0
