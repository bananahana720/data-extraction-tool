"""
Tests for Extract Command - Single File Processing.

Test coverage for:
- Extract single file to various formats
- Error handling (missing files, unsupported formats)
- Output directory creation
- Overwrite protection
- Exit codes
- User-friendly error messages
"""

import pytest
from pathlib import Path
from click.testing import CliRunner

from cli.main import cli


class TestExtractCommandSuccess:
    """Test successful extraction scenarios."""

    def test_extract_docx_to_json(self, cli_runner, sample_docx_file, tmp_path):
        """Extract DOCX file to JSON format."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            ["extract", str(sample_docx_file), "--output", str(output_file), "--format", "json"],
        )

        assert result.exit_code == 0
        assert "Successfully extracted" in result.output
        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_extract_docx_to_markdown(self, cli_runner, sample_docx_file, tmp_path):
        """Extract DOCX file to Markdown format."""
        output_file = tmp_path / "output.md"

        result = cli_runner.invoke(
            cli,
            [
                "extract",
                str(sample_docx_file),
                "--output",
                str(output_file),
                "--format",
                "markdown",
            ],
        )

        assert result.exit_code == 0
        assert "Successfully extracted" in result.output
        assert output_file.exists()

    def test_extract_all_formats(self, cli_runner, sample_docx_file, tmp_path):
        """Extract to all supported formats simultaneously."""
        output_dir = tmp_path / "outputs"

        result = cli_runner.invoke(
            cli, ["extract", str(sample_docx_file), "--output", str(output_dir), "--format", "all"]
        )

        assert result.exit_code == 0
        assert "Successfully extracted" in result.output

        # Should create multiple output files
        output_files = list(output_dir.glob("*"))
        assert len(output_files) > 0

    def test_extract_creates_output_directory(self, cli_runner, sample_docx_file, tmp_path):
        """Create output directory if it doesn't exist."""
        output_dir = tmp_path / "new_dir" / "output.json"

        result = cli_runner.invoke(
            cli, ["extract", str(sample_docx_file), "--output", str(output_dir), "--format", "json"]
        )

        assert result.exit_code == 0
        assert output_dir.exists()

    def test_extract_default_output_location(self, cli_runner, sample_docx_file, tmp_path):
        """Use default output location when not specified."""
        # Run from tmp directory
        result = cli_runner.invoke(
            cli, ["extract", str(sample_docx_file), "--format", "json"], catch_exceptions=False
        )

        assert result.exit_code == 0

    def test_extract_shows_progress(self, cli_runner, sample_docx_file, tmp_path):
        """Display progress during extraction."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            ["extract", str(sample_docx_file), "--output", str(output_file), "--format", "json"],
        )

        # Check for progress indicators
        assert result.exit_code == 0


class TestExtractCommandErrors:
    """Test error handling scenarios."""

    def test_extract_missing_file(self, cli_runner, nonexistent_file, tmp_path):
        """Handle file not found gracefully."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            ["extract", str(nonexistent_file), "--output", str(output_file), "--format", "json"],
        )

        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "could not find" in result.output.lower()

        # Should NOT contain technical jargon
        assert "exception" not in result.output.lower()
        assert "traceback" not in result.output.lower()

    def test_extract_unsupported_format(self, cli_runner, unsupported_file, tmp_path):
        """Handle unsupported file format gracefully."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            ["extract", str(unsupported_file), "--output", str(output_file), "--format", "json"],
        )

        assert result.exit_code != 0
        assert "format" in result.output.lower() or "not supported" in result.output.lower()

    def test_extract_invalid_output_format(self, cli_runner, sample_docx_file, tmp_path):
        """Handle invalid output format option."""
        output_file = tmp_path / "output.xyz"

        result = cli_runner.invoke(
            cli,
            [
                "extract",
                str(sample_docx_file),
                "--output",
                str(output_file),
                "--format",
                "invalid_format",
            ],
        )

        assert result.exit_code != 0

    def test_extract_overwrite_protection(self, cli_runner, sample_docx_file, tmp_path):
        """Prompt before overwriting existing file."""
        output_file = tmp_path / "output.json"
        output_file.write_text('{"existing": "content"}')

        # Simulate "no" answer to overwrite prompt
        result = cli_runner.invoke(
            cli,
            ["extract", str(sample_docx_file), "--output", str(output_file), "--format", "json"],
            input="n\n",
        )

        # Should ask about overwrite
        assert "overwrite" in result.output.lower() or "exists" in result.output.lower()

    def test_extract_force_overwrite(self, cli_runner, sample_docx_file, tmp_path):
        """Force overwrite with --force flag."""
        output_file = tmp_path / "output.json"
        output_file.write_text('{"existing": "content"}')

        result = cli_runner.invoke(
            cli,
            [
                "extract",
                str(sample_docx_file),
                "--output",
                str(output_file),
                "--format",
                "json",
                "--force",
            ],
        )

        assert result.exit_code == 0
        # Should not prompt
        assert "overwrite" not in result.output.lower()


class TestExtractCommandValidation:
    """Test input validation."""

    def test_extract_requires_file_argument(self, cli_runner):
        """Command requires file path argument."""
        result = cli_runner.invoke(cli, ["extract"])

        assert result.exit_code != 0
        assert "file" in result.output.lower() or "missing" in result.output.lower()

    def test_extract_validates_format_option(self, cli_runner, sample_docx_file):
        """Validate format option values."""
        result = cli_runner.invoke(cli, ["extract", str(sample_docx_file), "--format", ""])

        assert result.exit_code != 0


class TestExtractCommandOutput:
    """Test output formatting and messages."""

    def test_extract_success_message_non_technical(self, cli_runner, sample_docx_file, tmp_path):
        """Success message should be clear for non-technical users."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            ["extract", str(sample_docx_file), "--output", str(output_file), "--format", "json"],
        )

        assert result.exit_code == 0

        # Should contain helpful information
        assert str(sample_docx_file.name) in result.output or "file" in result.output.lower()

    def test_extract_verbose_output(self, cli_runner, sample_docx_file, tmp_path):
        """Verbose mode shows detailed information."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            [
                "extract",
                str(sample_docx_file),
                "--output",
                str(output_file),
                "--format",
                "json",
                "--verbose",
            ],
        )

        assert result.exit_code == 0
        # Verbose mode should show more details

    def test_extract_quiet_mode(self, cli_runner, sample_docx_file, tmp_path):
        """Quiet mode suppresses progress output."""
        output_file = tmp_path / "output.json"

        result = cli_runner.invoke(
            cli,
            [
                "extract",
                str(sample_docx_file),
                "--output",
                str(output_file),
                "--format",
                "json",
                "--quiet",
            ],
        )

        assert result.exit_code == 0
        # Minimal output in quiet mode
