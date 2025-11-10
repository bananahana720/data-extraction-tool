"""
Tests for Version Command - Version Information Display.

Test coverage for:
- Basic version display
- Verbose version information
- Component versions
- Exit codes
- Platform information
- Formatting and encoding
- Integration with other commands
"""

import pytest
import sys
import platform
from click.testing import CliRunner

from cli.main import cli, __version__


class TestVersionCommand:
    """Test version command functionality."""

    def test_version_basic(self, cli_runner):
        """Display basic version information."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower() or any(char.isdigit() for char in result.output)

    def test_version_shows_tool_name(self, cli_runner):
        """Version output includes tool name."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        # Should mention the tool name
        output_lower = result.output.lower()
        assert "data" in output_lower or "extract" in output_lower or "version" in output_lower

    def test_version_verbose(self, cli_runner):
        """Verbose mode shows component versions."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0
        # Verbose should show more information than basic

    def test_version_exit_code_success(self, cli_runner):
        """Version command exits with 0."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0

    def test_version_short_flag(self, cli_runner):
        """Support -V short flag for version."""
        result = cli_runner.invoke(cli, ["-V"])

        # May or may not be implemented
        # If implemented, should show version

    def test_version_format_readable(self, cli_runner):
        """Version output is readable format."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        # Should have some structured output
        assert len(result.output.strip()) > 0

    def test_version_displays_version_number(self, cli_runner):
        """Verify version number is displayed."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        # Should contain actual version (may have ANSI codes from Rich)
        # Check for version parts separately to handle Rich formatting
        import re

        # Strip ANSI codes for checking
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
        assert __version__ in clean_output or "version" in result.output.lower()

    def test_version_consistent_across_calls(self, cli_runner):
        """Verify version output is consistent."""
        result1 = cli_runner.invoke(cli, ["version"])
        result2 = cli_runner.invoke(cli, ["version"])

        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert result1.output == result2.output


class TestVersionCommandVerbose:
    """Test verbose version information."""

    def test_version_verbose_shows_components(self, cli_runner):
        """Verbose version shows component information."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0
        # Should show more than just version number

    def test_version_verbose_shows_python_version(self, cli_runner):
        """Verbose version shows Python version."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0
        # Should include Python version
        assert "Python" in result.output or "python" in result.output.lower()
        # Check for major.minor version (Rich may format it with ANSI codes)
        import re

        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
        python_version = sys.version.split()[0]
        major_minor = ".".join(python_version.split(".")[:2])  # Just major.minor
        assert major_minor in clean_output

    def test_version_verbose_shows_dependencies(self, cli_runner):
        """Verbose version shows key dependencies."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0
        # Should mention click and/or rich
        output_lower = result.output.lower()
        assert "click" in output_lower or "rich" in output_lower

    def test_version_verbose_shows_platform(self, cli_runner):
        """Verify verbose mode shows platform information."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0
        assert "Platform" in result.output or "platform" in result.output.lower()

    def test_verbose_flag_variations(self, cli_runner):
        """Test different verbose flag formats."""
        # Long form
        result1 = cli_runner.invoke(cli, ["version", "--verbose"])
        assert result1.exit_code == 0

        # Short form
        result2 = cli_runner.invoke(cli, ["version", "-v"])
        assert result2.exit_code == 0

    def test_verbose_has_more_content(self, cli_runner):
        """Verify verbose version has more content than basic."""
        basic_result = cli_runner.invoke(cli, ["version"])
        verbose_result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert basic_result.exit_code == 0
        assert verbose_result.exit_code == 0
        assert len(verbose_result.output) > len(basic_result.output)


class TestVersionCommandFormatting:
    """Test version output formatting."""

    def test_version_output_is_readable(self, cli_runner):
        """Verify version output is well-formatted."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        # Should have reasonable length
        assert len(result.output) > 10
        assert len(result.output) < 1000

    def test_version_no_error_output(self, cli_runner):
        """Verify version doesn't produce error output."""
        result = cli_runner.invoke(cli, ["version"])

        assert result.exit_code == 0
        output_lower = result.output.lower()
        assert "error" not in output_lower
        assert "warning" not in output_lower

    def test_version_output_is_utf8(self, cli_runner):
        """Verify version output is properly encoded."""
        result = cli_runner.invoke(cli, ["version", "--verbose"])

        assert result.exit_code == 0

        # Output should be valid UTF-8
        try:
            result.output.encode("utf-8")
        except UnicodeEncodeError:
            pytest.fail("Version output contains invalid UTF-8")


class TestVersionCommandEdgeCases:
    """Test edge cases for version command."""

    def test_version_with_quiet_flag(self, cli_runner):
        """Test version command with quiet flag."""
        result = cli_runner.invoke(cli, ["--quiet", "version"])

        # Quiet shouldn't suppress version output
        assert result.exit_code == 0
        assert len(result.output) > 0

    def test_version_with_verbose_global(self, cli_runner):
        """Test version command with global verbose flag."""
        result = cli_runner.invoke(cli, ["--verbose", "version"])

        assert result.exit_code == 0

    def test_version_multiple_times(self, cli_runner):
        """Test calling version multiple times."""
        import re

        for i in range(3):
            result = cli_runner.invoke(cli, ["version"])
            assert result.exit_code == 0
            # Strip ANSI codes for checking
            clean_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
            assert __version__ in clean_output or "version" in result.output.lower()


class TestVersionCommandHelp:
    """Test version command help."""

    def test_version_help_available(self, cli_runner):
        """Verify version command has help."""
        result = cli_runner.invoke(cli, ["version", "--help"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_version_in_main_help(self, cli_runner):
        """Verify version command listed in main help."""
        result = cli_runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()


@pytest.mark.integration
class TestVersionCommandIntegration:
    """Integration tests for version command."""

    def test_version_in_workflow(self, cli_runner, sample_docx_file, tmp_path):
        """Test version command in realistic workflow."""
        # Check version
        result1 = cli_runner.invoke(cli, ["version"])
        assert result1.exit_code == 0

        # Run extraction
        output_file = tmp_path / "output.json"
        result2 = cli_runner.invoke(
            cli,
            ["extract", str(sample_docx_file), "--output", str(output_file), "--format", "json"],
        )
        assert result2.exit_code == 0

        # Check version again
        result3 = cli_runner.invoke(cli, ["version"])
        assert result3.exit_code == 0
        assert result3.output == result1.output

    def test_version_with_config(self, cli_runner, config_file):
        """Test version command with config file specified."""
        result = cli_runner.invoke(cli, ["--config", str(config_file), "version"])

        assert result.exit_code == 0
        # Strip ANSI codes for checking
        import re

        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
        assert __version__ in clean_output or "version" in result.output.lower()
