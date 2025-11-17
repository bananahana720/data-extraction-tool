"""Unit tests for CsvFormatter (Story 3.6 - ATDD RED PHASE).

Validates canonical CSV schema, RFC 4180 escaping, truncation indicators,
entity serialization, FormattingResult metadata, and parser validation hooks.

Test Coverage:
    - AC-3.6-1: Canonical column schema with stable ordering
    - AC-3.6-2: RFC 4180 escaping (commas, quotes, multiline text)
    - AC-3.6-3: Header row emitted once with human-readable labels
    - AC-3.6-5: Optional truncation indicator with ellipsis suffix
    - AC-3.6-6: Entity list serialization as semicolon-delimited values
    - AC-3.6-7: Parser sanity check invocation (Python csv, pandas, CLI)

These tests WILL FAIL until CsvFormatter exists and satisfies Story 3.6 requirements.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.output.formatters.base import FormattingResult
    from data_extract.output.formatters.csv_formatter import CsvFormatter
except ImportError:  # pragma: no cover - CsvFormatter not implemented yet
    CsvFormatter = None  # type: ignore[assignment]
    FormattingResult = None  # type: ignore[assignment]

from data_extract.chunk.entity_preserver import EntityReference
from data_extract.chunk.models import Chunk, ChunkMetadata
from data_extract.chunk.quality import QualityScore

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.formatting]

EXPECTED_COLUMNS: List[str] = [
    "chunk_id",
    "source_file",
    "section_context",
    "chunk_text",
    "entity_tags",
    "quality_score",
    "word_count",
    "token_count",
    "processing_version",
    "warnings",
]


class DummyParserValidator:
    """Spy validator used to assert parser validation hook invocation."""

    def __init__(self) -> None:
        self.called_with: Path | None = None

    def validate(self, csv_path: Path) -> None:
        """Record invocation path."""
        self.called_with = csv_path


@pytest.fixture
def enriched_chunk(tmp_path: Path) -> Chunk:
    """Create enriched chunk with metadata, entities, and warnings."""
    source_file = tmp_path / "audit-plan.pdf"
    source_file.write_text("dummy content", encoding="utf-8")

    entity_1 = EntityReference(
        entity_type="risk",
        entity_id="RISK-001",
        start_pos=10,
        end_pos=30,
        is_partial=False,
        context_snippet="Risk reference snippet",
    )
    entity_2 = EntityReference(
        entity_type="control",
        entity_id="CTRL-003",
        start_pos=45,
        end_pos=70,
        is_partial=False,
        context_snippet="Control reference snippet",
    )

    metadata = ChunkMetadata(
        entity_tags=[entity_1, entity_2],
        section_context="Audit > Controls > User Access",
        entity_relationships=[("RISK-001", "mitigated_by", "CTRL-003")],
        quality=QualityScore(
            readability_flesch_kincaid=8.7,
            readability_gunning_fog=10.1,
            ocr_confidence=0.97,
            completeness=0.94,
            coherence=0.9,
            overall=0.92,
            flags=["OCR_LOW", "MANUAL_REVIEW"],
        ),
        source_hash="3d833a3b41054595a9b9fb4ef85a",
        document_type="audit_plan",
        word_count=142,
        token_count=195,
        created_at=datetime(2025, 11, 20, 9, 15, 0),
        processing_version="1.0.0-epic3",
        source_file=source_file,
        config_snapshot={"chunk_size": 512, "overlap_pct": 0.15},
    )

    return Chunk(
        id="chunk_csv_001",
        text='Control summary with comma, quote "marker", and newline.\nSecond line continues context.',
        document_id="doc_csv_001",
        position_index=0,
        token_count=195,
        word_count=142,
        entities=[],
        section_context="Audit > Controls > User Access",
        quality_score=0.92,
        readability_scores={"flesch_kincaid": 8.7, "gunning_fog": 10.1},
        metadata=metadata,
    )


@pytest.fixture
def chunk_with_long_text(enriched_chunk: Chunk) -> Chunk:
    """Clone chunk with long text to test truncation indicator."""
    long_text = "Paragraph " + ("with verbose narrative, " * 20) + "end of chunk."
    return Chunk(
        id="chunk_csv_002",
        text=long_text,
        document_id=enriched_chunk.document_id,
        position_index=1,
        token_count=enriched_chunk.token_count + 50,
        word_count=enriched_chunk.word_count + 30,
        entities=[],
        section_context=enriched_chunk.section_context,
        quality_score=enriched_chunk.quality_score,
        readability_scores=enriched_chunk.readability_scores,
        metadata=enriched_chunk.metadata,
    )


@pytest.fixture
def csv_formatter() -> CsvFormatter:
    """Create CsvFormatter instance with default validation enabled."""
    if CsvFormatter is None:
        pytest.skip("CsvFormatter not implemented yet (RED phase)")
    return CsvFormatter()


@pytest.fixture
def csv_formatter_with_truncation() -> CsvFormatter:
    """Create CsvFormatter configured with max_text_length to test truncation indicator."""
    if CsvFormatter is None:
        pytest.skip("CsvFormatter not implemented yet (RED phase)")
    return CsvFormatter(max_text_length=120, validate=False)


@pytest.fixture
def sample_chunks(enriched_chunk: Chunk, chunk_with_long_text: Chunk) -> Iterable[Chunk]:
    """Provide iterator with two enriched chunks."""
    return iter([enriched_chunk, chunk_with_long_text])


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    """Helper to read CSV rows into list of dictionaries."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


class TestCsvSchemaAndHeader:
    """Validate canonical header and schema ordering (AC-3.6-1, AC-3.6-3)."""

    def test_formatter_writes_canonical_header_once(
        self, csv_formatter: CsvFormatter, sample_chunks: Iterable[Chunk], tmp_path: Path
    ) -> None:
        """Should emit canonical header row exactly once."""
        output_path = tmp_path / "chunks.csv"

        csv_formatter.format_chunks(sample_chunks, output_path)

        with output_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            assert header == EXPECTED_COLUMNS
            row_count = sum(1 for _ in reader)
        assert row_count == 2

    def test_formatter_populates_required_columns(
        self, csv_formatter: CsvFormatter, enriched_chunk: Chunk, tmp_path: Path
    ) -> None:
        """Should populate schema columns with provenance metadata."""
        output_path = tmp_path / "chunks.csv"

        csv_formatter.format_chunks(iter([enriched_chunk]), output_path)

        rows = read_rows(output_path)
        assert len(rows) == 1
        row = rows[0]
        assert row["chunk_id"] == enriched_chunk.id
        assert Path(row["source_file"]).name == enriched_chunk.metadata.source_file.name
        assert row["section_context"] == enriched_chunk.metadata.section_context
        assert row["quality_score"] == f"{enriched_chunk.quality_score:.2f}"
        assert row["word_count"] == str(enriched_chunk.metadata.word_count)
        assert row["token_count"] == str(enriched_chunk.metadata.token_count)
        assert row["processing_version"] == enriched_chunk.metadata.processing_version


class TestCsvEscapingAndSerialization:
    """Verify RFC 4180 escaping, entity serialization, and warnings (AC-3.6-2, AC-3.6-5, AC-3.6-6)."""

    def test_formatter_escapes_commas_quotes_and_newlines(
        self, csv_formatter: CsvFormatter, enriched_chunk: Chunk, tmp_path: Path
    ) -> None:
        """Should preserve chunk text with commas, quotes, and newlines using RFC 4180 quoting."""
        output_path = tmp_path / "escaped.csv"

        csv_formatter.format_chunks(iter([enriched_chunk]), output_path)

        rows = read_rows(output_path)
        stored_text = rows[0]["chunk_text"]
        assert "quote" in stored_text
        assert "Second line continues context." in stored_text
        assert '"marker"' in enriched_chunk.text

    def test_formatter_serializes_entities_as_semicolon_list(
        self, csv_formatter: CsvFormatter, enriched_chunk: Chunk, tmp_path: Path
    ) -> None:
        """Should serialize entity tags as semicolon-delimited values (AC-3.6-6)."""
        output_path = tmp_path / "entities.csv"

        csv_formatter.format_chunks(iter([enriched_chunk]), output_path)

        rows = read_rows(output_path)
        assert rows[0]["entity_tags"] == "RISK-001;CTRL-003"

    def test_formatter_combines_quality_flags_into_warnings_column(
        self, csv_formatter: CsvFormatter, enriched_chunk: Chunk, tmp_path: Path
    ) -> None:
        """Should surface quality flags (and future formatter warnings) in warnings column."""
        output_path = tmp_path / "warnings.csv"

        csv_formatter.format_chunks(iter([enriched_chunk]), output_path)

        rows = read_rows(output_path)
        assert rows[0]["warnings"] == "OCR_LOW;MANUAL_REVIEW"

    def test_formatter_truncates_text_with_ellipsis_indicator(
        self,
        csv_formatter_with_truncation: CsvFormatter,
        chunk_with_long_text: Chunk,
        tmp_path: Path,
    ) -> None:
        """Should truncate long text and append ellipsis marker when max_text_length configured."""
        output_path = tmp_path / "truncated.csv"

        csv_formatter_with_truncation.format_chunks(iter([chunk_with_long_text]), output_path)

        rows = read_rows(output_path)
        assert rows[0]["chunk_text"].endswith("…")
        assert "TRUNCATED" in rows[0]["warnings"]


class TestCsvFormatterResults:
    """Validate FormattingResult metadata and parser validation hook (AC-3.6-1, AC-3.6-7)."""

    def test_format_chunks_returns_format_result(
        self, csv_formatter: CsvFormatter, sample_chunks: Iterable[Chunk], tmp_path: Path
    ) -> None:
        """Should return FormattingResult populated with CSV metadata."""
        output_path = tmp_path / "chunks.csv"

        result = csv_formatter.format_chunks(sample_chunks, output_path)

        assert isinstance(result, FormattingResult)
        assert result.format_type == "csv"
        assert result.output_path == output_path
        assert result.chunk_count == 2
        assert result.file_size_bytes > 0
        assert result.errors == []

    def test_formatter_invokes_parser_validator_when_enabled(
        self, sample_chunks: Iterable[Chunk], tmp_path: Path
    ) -> None:
        """Should run parser validator after writing file when validate=True (AC-3.6-7)."""
        if CsvFormatter is None:
            pytest.skip("CsvFormatter not implemented yet (RED phase)")

        validator = DummyParserValidator()
        formatter = CsvFormatter(validate=True, parser_validator=validator)
        output_path = tmp_path / "validated.csv"

        formatter.format_chunks(sample_chunks, output_path)

        assert validator.called_with == output_path

    def test_formatter_allows_disabling_validation(
        self, sample_chunks: Iterable[Chunk], tmp_path: Path
    ) -> None:
        """Should skip parser validation when validate=False."""
        if CsvFormatter is None:
            pytest.skip("CsvFormatter not implemented yet (RED phase)")

        validator = DummyParserValidator()
        formatter = CsvFormatter(validate=False, parser_validator=validator)
        output_path = tmp_path / "no-validation.csv"

        formatter.format_chunks(sample_chunks, output_path)

        assert validator.called_with is None
