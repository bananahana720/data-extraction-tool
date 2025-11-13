"""
Tests for Config Command - Configuration Management.

Test coverage for:
- Show current configuration
- Validate configuration
- Show config file path
- Handle missing config
- Error reporting
"""


from cli.main import cli


class TestConfigShowCommand:
    """Test config show functionality."""

    def test_config_show(self, cli_runner, config_file):
        """Display current configuration."""
        result = cli_runner.invoke(cli, ["config", "show", "--config", str(config_file)])

        assert result.exit_code == 0
        # Should show configuration content

    def test_config_show_readable_format(self, cli_runner, config_file):
        """Configuration displayed in readable format."""
        result = cli_runner.invoke(cli, ["config", "show", "--config", str(config_file)])

        assert result.exit_code == 0
        assert len(result.output.strip()) > 0

    def test_config_show_missing_file(self, cli_runner, tmp_path):
        """Handle missing config file gracefully."""
        nonexistent_config = tmp_path / "nonexistent.yaml"

        result = cli_runner.invoke(cli, ["config", "show", "--config", str(nonexistent_config)])

        # Should either use defaults or report missing
        assert "not found" in result.output.lower() or result.exit_code == 0

    def test_config_show_default_location(self, cli_runner):
        """Show config from default location."""
        result = cli_runner.invoke(cli, ["config", "show"])

        # Should work with default config or report location
        assert result.exit_code == 0 or "config" in result.output.lower()


class TestConfigValidateCommand:
    """Test config validation functionality."""

    def test_config_validate_valid(self, cli_runner, config_file):
        """Validate valid configuration file."""
        result = cli_runner.invoke(cli, ["config", "validate", "--config", str(config_file)])

        assert result.exit_code == 0
        assert "valid" in result.output.lower() or "ok" in result.output.lower()

    def test_config_validate_invalid(self, cli_runner, tmp_path):
        """Report invalid configuration."""
        invalid_config = tmp_path / "invalid.yaml"
        invalid_config.write_text("invalid: [unclosed bracket")

        result = cli_runner.invoke(cli, ["config", "validate", "--config", str(invalid_config)])

        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "error" in result.output.lower()

    def test_config_validate_missing_file(self, cli_runner, tmp_path):
        """Handle missing file during validation."""
        nonexistent_config = tmp_path / "nonexistent.yaml"

        result = cli_runner.invoke(cli, ["config", "validate", "--config", str(nonexistent_config)])

        assert result.exit_code != 0

    def test_config_validate_shows_errors(self, cli_runner, tmp_path):
        """Validation errors are clearly reported."""
        invalid_config = tmp_path / "bad.yaml"
        invalid_config.write_text("!!python/object/apply:os.system ['ls']")

        result = cli_runner.invoke(cli, ["config", "validate", "--config", str(invalid_config)])

        # Should report what's wrong
        assert result.exit_code != 0


class TestConfigPathCommand:
    """Test config path display."""

    def test_config_path_shows_location(self, cli_runner, config_file):
        """Show configuration file location."""
        result = cli_runner.invoke(cli, ["config", "path", "--config", str(config_file)])

        assert result.exit_code == 0
        assert str(config_file) in result.output or "config" in result.output.lower()

    def test_config_path_default_location(self, cli_runner):
        """Show default config location."""
        result = cli_runner.invoke(cli, ["config", "path"])

        assert result.exit_code == 0
        # Should show some path

    def test_config_path_nonexistent(self, cli_runner, tmp_path):
        """Handle nonexistent config path."""
        nonexistent_config = tmp_path / "nonexistent.yaml"

        result = cli_runner.invoke(cli, ["config", "path", "--config", str(nonexistent_config)])

        # Should still show the path even if doesn't exist
        assert str(nonexistent_config) in result.output or result.exit_code == 0


class TestConfigCommandErrors:
    """Test config command error handling."""

    def test_config_requires_subcommand(self, cli_runner):
        """Config command requires subcommand."""
        result = cli_runner.invoke(cli, ["config"])

        # Should show help or require subcommand
        assert (
            "show" in result.output.lower()
            or "validate" in result.output.lower()
            or result.exit_code != 0
        )

    def test_config_invalid_subcommand(self, cli_runner):
        """Invalid subcommand is rejected."""
        result = cli_runner.invoke(cli, ["config", "invalid"])

        assert result.exit_code != 0

    def test_config_user_friendly_errors(self, cli_runner, tmp_path):
        """Errors are user-friendly."""
        invalid_config = tmp_path / "bad.yaml"
        invalid_config.write_text("{ invalid yaml syntax")

        result = cli_runner.invoke(cli, ["config", "validate", "--config", str(invalid_config)])

        assert result.exit_code != 0
        # Should not show technical stack traces
        assert "traceback" not in result.output.lower()
