"""Unit tests for CsvParserValidator (Story 3.6 - ATDD RED PHASE).

Verifies parser sanity checks using Python's csv module, pandas.read_csv, and
csvkit CLI tooling hooks execute before surfacing CSV output.

Test Coverage:
    - AC-3.6-4: pandas import validation (dataframe friendly)
    - AC-3.6-7: Parser sanity checks (python csv, pandas, csvkit CLI)

These tests WILL FAIL until CsvParserValidator is implemented.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List

import pytest

try:
    from data_extract.output.validation.csv_parser import (
        CsvParserError,
        CsvParserValidationReport,
        CsvParserValidator,
    )
except ImportError:  # pragma: no cover - CsvParserValidator not implemented yet
    CsvParserValidator = None  # type: ignore[assignment]
    CsvParserValidationReport = None  # type: ignore[assignment]
    CsvParserError = RuntimeError  # type: ignore[assignment]

pytestmark = [pytest.mark.unit, pytest.mark.output]


@pytest.fixture
def valid_csv_path(tmp_path: Path) -> Path:
    """Create valid CSV file for parser validation."""
    csv_path = tmp_path / "valid.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["chunk_id", "chunk_text"])
        writer.writerow(["chunk_001", 'Hello, "World"'])
    return csv_path


@pytest.fixture
def invalid_csv_path(tmp_path: Path) -> Path:
    """Create malformed CSV file with unmatched quote to trigger parser error."""
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text('chunk_id,chunk_text\nchunk_001,"unterminated row\n', encoding="utf-8")
    return csv_path


def _require_validator() -> type:
    """Ensure CsvParserValidator is available, otherwise skip."""
    if CsvParserValidator is None:
        pytest.skip("CsvParserValidator not implemented yet (RED phase)")
    return CsvParserValidator


class TestCsvParserValidatorSuccess:
    """Validate success path hits python csv, pandas, and CLI engines."""

    def test_validate_returns_report_for_valid_csv(self, valid_csv_path: Path) -> None:
        """Should return CsvParserValidationReport with all engines passing."""
        validator_class = _require_validator()
        validator = validator_class()

        report = validator.validate(valid_csv_path)

        assert isinstance(report, CsvParserValidationReport)
        assert report.python_passed is True
        assert report.pandas_passed is True
        assert report.cli_passed is True
        assert report.cli_tool in {"csvformat", "csvclean", "csvlint"}

    def test_validator_invokes_cli_runner(self, valid_csv_path: Path) -> None:
        """Should invoke csvkit CLI command with provided runner."""
        validator_class = _require_validator()
        invoked_commands: List[List[str]] = []

        def fake_run(command: List[str], **_: object) -> object:
            invoked_commands.append(command)
            return type("Result", (), {"stdout": "ok", "stderr": ""})

        validator = validator_class(cli_command=["csvformat", "--out", "csv"], run_command=fake_run)

        validator.validate(valid_csv_path)

        assert invoked_commands, "CLI runner should be invoked"
        assert invoked_commands[0][0].startswith("csvformat")


class TestCsvParserValidatorFailures:
    """Ensure validator raises descriptive errors for malformed CSV."""

    def test_invalid_csv_raises_error(self, invalid_csv_path: Path) -> None:
        """Should raise CsvParserError when python csv parsing fails."""
        validator_class = _require_validator()
        validator = validator_class()

        with pytest.raises(CsvParserError) as excinfo:
            validator.validate(invalid_csv_path)

        assert "python csv" in str(excinfo.value).lower()

    def test_cli_failure_surfaces_in_error_message(self, valid_csv_path: Path) -> None:
        """Should raise CsvParserError when CLI runner reports failure."""
        validator_class = _require_validator()

        def failing_runner(command: List[str], **_: object) -> object:
            raise RuntimeError(f"CLI failure for {' '.join(command)}")

        validator = validator_class(
            cli_command=["csvclean", "--dry-run"], run_command=failing_runner
        )

        with pytest.raises(CsvParserError) as excinfo:
            validator.validate(valid_csv_path)

        assert "csvclean" in str(excinfo.value)
