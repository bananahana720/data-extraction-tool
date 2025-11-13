"""
File System Edge Case Tests for CLI.

Tests file system boundary conditions including:
- Non-existent input paths
- Read-only output directories
- Output file already exists (with/without --force)
- Very long file paths (near OS limit)
- Special characters in paths
- Permission issues
- Disk space constraints (if testable)

Design: Equivalency partitioning methodology
Status: v1.0.2 edge case validation
"""

import os
import stat
import sys
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from cli.main import cli


class TestFilesystemEdgeCases:
    """Test filesystem-related edge cases."""

    @pytest.fixture
    def runner(self):
        """Create CLI runner."""
        return CliRunner()

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    # Category: Negative - Non-existent Paths
    def test_nonexistent_input_file(self, runner, temp_output_dir):
        """1. FAIL-EXPECTED: Input file does not exist."""
        nonexistent = temp_output_dir / "does_not_exist.txt"
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(nonexistent), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code != 0, "Should fail for non-existent input"
        assert "not found" in result.output.lower() or "does not exist" in result.output.lower()

    def test_nonexistent_batch_directory(self, runner, temp_output_dir):
        """2. FAIL-EXPECTED: Batch directory does not exist."""
        nonexistent_dir = temp_output_dir / "missing_directory"
        output_dir = temp_output_dir / "output"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            ["batch", str(nonexistent_dir), "--output", str(output_dir), "--format", "json"],
        )

        assert result.exit_code != 0, "Should fail for non-existent directory"
        assert "not found" in result.output.lower() or "does not exist" in result.output.lower()

    # Category: Negative - Permission Issues
    @pytest.mark.skipif(sys.platform == "win32", reason="Permission tests unreliable on Windows")
    def test_readonly_output_directory(self, runner, temp_output_dir):
        """3. FAIL-EXPECTED: Output directory is read-only."""
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")

        # Create read-only output directory
        readonly_dir = temp_output_dir / "readonly_output"
        readonly_dir.mkdir()
        os.chmod(readonly_dir, stat.S_IRUSR | stat.S_IXUSR)  # Read + execute only

        try:
            output_file = readonly_dir / "output.json"

            result = runner.invoke(
                cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
            )

            assert result.exit_code != 0, "Should fail for read-only directory"
            assert "permission" in result.output.lower() or "denied" in result.output.lower()

        finally:
            # Restore permissions for cleanup
            os.chmod(readonly_dir, stat.S_IRWXU)

    @pytest.mark.skipif(sys.platform == "win32", reason="Permission tests unreliable on Windows")
    def test_readonly_input_file_should_work(self, runner, temp_output_dir):
        """4. PASS: Read-only input file should still be readable."""
        test_file = temp_output_dir / "readonly_input.txt"
        test_file.write_text("Test content for readonly file")

        # Make file read-only
        os.chmod(test_file, stat.S_IRUSR)  # Read only

        try:
            output_file = temp_output_dir / "output.json"

            result = runner.invoke(
                cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
            )

            # Should succeed - we only need read access
            assert result.exit_code == 0, f"Should read readonly file: {result.output}"

        finally:
            # Restore permissions
            os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)

    # Category: Negative - Output File Already Exists
    def test_output_file_exists_without_force(self, runner, temp_output_dir):
        """5. FAIL/PASS: Output file already exists, no --force flag."""
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")

        output_file = temp_output_dir / "output.json"
        output_file.write_text('{"existing": "data"}')  # Pre-existing file

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # Behavior depends on CLI implementation
        # Either fails with error or overwrites by default
        # Document current behavior
        if result.exit_code != 0:
            assert "exists" in result.output.lower() or "overwrite" in result.output.lower()
        else:
            # Overwrites by default - that's okay too
            assert output_file.exists()

    def test_output_file_exists_with_force(self, runner, temp_output_dir):
        """6. PASS: Output file exists but --force flag provided."""
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")

        output_file = temp_output_dir / "output.json"
        output_file.write_text('{"existing": "data"}')

        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_file),
                "--output",
                str(output_file),
                "--format",
                "json",
                "--force",  # If this flag exists
            ],
        )

        # Should succeed and overwrite
        # If --force doesn't exist, test will fail indicating feature not implemented
        assert result.exit_code == 0 or "--force" not in result.output

    # Category: Negative - Special Characters in Paths
    def test_path_with_spaces(self, runner, temp_output_dir):
        """7. PASS: File path with spaces."""
        dir_with_spaces = temp_output_dir / "dir with spaces"
        dir_with_spaces.mkdir()

        test_file = dir_with_spaces / "file with spaces.txt"
        test_file.write_text("Test content")

        output_file = dir_with_spaces / "output with spaces.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with spaces in path: {result.output}"
        assert output_file.exists()

    def test_path_with_special_chars(self, runner, temp_output_dir):
        """8. PASS: Path with special characters (parentheses, brackets)."""
        special_dir = temp_output_dir / "dir[with]special(chars)"
        special_dir.mkdir()

        test_file = special_dir / "file(1)[test].txt"
        test_file.write_text("Test content")

        output_file = special_dir / "output[result].json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with special chars: {result.output}"
        assert output_file.exists()

    def test_path_with_dots(self, runner, temp_output_dir):
        """9. PASS: Path with multiple dots."""
        test_file = temp_output_dir / "file.with.many.dots.txt"
        test_file.write_text("Test content")

        output_file = temp_output_dir / "output.with.dots.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with dots: {result.output}"
        assert output_file.exists()

    # Category: Performance - Long Paths
    def test_moderately_long_path(self, runner, temp_output_dir):
        """10. PASS: Moderately long file path (still reasonable)."""
        # Create nested directory structure
        deep_path = temp_output_dir
        for i in range(10):
            deep_path = deep_path / f"level_{i}_directory"
            deep_path.mkdir()

        test_file = deep_path / "deeply_nested_file.txt"
        test_file.write_text("Test content in deep directory")

        output_file = deep_path / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with deep path: {result.output}"
        assert output_file.exists()

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows path length limits")
    def test_path_near_windows_limit(self, runner, temp_output_dir):
        """11. FAIL/PASS: Path approaching Windows 260 character limit."""
        # Windows has 260 char limit (can be 32767 with long path support)
        # Create path close to limit
        long_dir_name = "a" * 200
        long_path = temp_output_dir / long_dir_name

        try:
            long_path.mkdir()
            test_file = long_path / "test.txt"
            test_file.write_text("Test content")

            output_file = long_path / "output.json"

            result = runner.invoke(
                cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
            )

            # May succeed with long path support or fail gracefully
            if result.exit_code != 0:
                assert "path" in result.output.lower() or "too long" in result.output.lower()
            else:
                assert output_file.exists()

        except OSError as e:
            # Expected on systems without long path support
            pytest.skip(f"Long path not supported: {e}")

    # Category: Negative - File vs Directory Confusion
    def test_input_is_directory_not_file(self, runner, temp_output_dir):
        """12. FAIL-EXPECTED: Trying to extract a directory as a file."""
        test_dir = temp_output_dir / "is_a_directory"
        test_dir.mkdir()

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_dir), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code != 0, "Should fail when input is directory"
        assert "directory" in result.output.lower() or "not a file" in result.output.lower()

    def test_output_is_directory_not_file(self, runner, temp_output_dir):
        """13. FAIL-EXPECTED: Output path is existing directory, not file."""
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")

        output_dir = temp_output_dir / "output_is_dir"
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "extract",
                str(test_file),
                "--output",
                str(output_dir),  # Directory, not file
                "--format",
                "json",
            ],
        )

        # Should fail or handle gracefully
        assert result.exit_code != 0 or (output_dir / "output.json").exists()

    # Category: Negative - Relative vs Absolute Paths
    def test_relative_path_input(self, runner, temp_output_dir):
        """14. PASS: Relative path for input file."""
        # Create file and change to its directory
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")
        output_file = temp_output_dir / "output.json"

        # Use relative path
        with runner.isolated_filesystem(temp=temp_output_dir):
            result = runner.invoke(
                cli,
                [
                    "extract",
                    "./test.txt",  # Relative path
                    "--output",
                    "./output.json",
                    "--format",
                    "json",
                ],
            )

            # Should work with relative paths
            assert result.exit_code == 0 or result.exit_code is None

    # Category: Negative - Symlinks (if supported)
    @pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require admin on Windows")
    def test_symlink_input_file(self, runner, temp_output_dir):
        """15. PASS: Input file is a symlink."""
        real_file = temp_output_dir / "real_file.txt"
        real_file.write_text("Test content from real file")

        symlink = temp_output_dir / "symlink.txt"
        symlink.symlink_to(real_file)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(symlink), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with symlink: {result.output}"
        assert output_file.exists()

    @pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require admin on Windows")
    def test_circular_symlink(self, runner, temp_output_dir):
        """16. FAIL-EXPECTED: Circular symlink should be handled."""
        symlink1 = temp_output_dir / "symlink1.txt"
        symlink2 = temp_output_dir / "symlink2.txt"

        # Create circular symlinks
        symlink1.symlink_to(symlink2)
        symlink2.symlink_to(symlink1)

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(symlink1), "--output", str(output_file), "--format", "json"]
        )

        # Should fail gracefully
        assert result.exit_code != 0
        assert (
            "error" in result.output.lower()
            or "circular" in result.output.lower()
            or "too many levels" in result.output.lower()
        )

    # Category: Integration - Hidden Files
    def test_hidden_file_unix(self, runner, temp_output_dir):
        """17. PASS: Hidden file (starts with dot on Unix)."""
        test_file = temp_output_dir / ".hidden_file.txt"
        test_file.write_text("Hidden file content")

        output_file = temp_output_dir / ".hidden_output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with hidden file: {result.output}"
        assert output_file.exists()

    # Category: Negative - No Extension
    def test_file_without_extension(self, runner, temp_output_dir):
        """18. PASS/FAIL: Input file with no extension."""
        test_file = temp_output_dir / "no_extension"
        test_file.write_text("Test content without extension")

        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # May succeed (treat as text) or fail (unsupported format)
        # Both behaviors are acceptable
        assert (
            result.exit_code == 0
            or "unsupported" in result.output.lower()
            or "format" in result.output.lower()
        )

    def test_output_without_extension(self, runner, temp_output_dir):
        """19. PASS: Output file without extension."""
        test_file = temp_output_dir / "test.txt"
        test_file.write_text("Test content")

        output_file = temp_output_dir / "output_no_ext"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # Should work - extension not strictly required
        assert result.exit_code == 0, f"Failed without output extension: {result.output}"
        assert output_file.exists()

    # Category: Negative - Case Sensitivity
    @pytest.mark.skipif(sys.platform == "win32", reason="Windows is case-insensitive")
    def test_case_sensitive_paths_unix(self, runner, temp_output_dir):
        """20. PASS: Case-sensitive file names on Unix."""
        file_lower = temp_output_dir / "test.txt"
        file_upper = temp_output_dir / "TEST.txt"

        file_lower.write_text("lowercase content")
        file_upper.write_text("UPPERCASE content")

        output_lower = temp_output_dir / "output_lower.json"
        output_upper = temp_output_dir / "output_upper.json"

        # Extract both
        result1 = runner.invoke(
            cli, ["extract", str(file_lower), "--output", str(output_lower), "--format", "json"]
        )

        result2 = runner.invoke(
            cli, ["extract", str(file_upper), "--output", str(output_upper), "--format", "json"]
        )

        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert output_lower.exists()
        assert output_upper.exists()
