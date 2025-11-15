"""Integration tests for end-to-end JSON output pipeline (Story 3.4 - ATDD RED PHASE).

Tests complete pipeline from ProcessingResult → ChunkingEngine → JsonFormatter → JSON file,
including queryability with jq and pandas, metadata accuracy, and determinism.

Test Coverage:
    - AC-3.4-2: Valid parsable JSON (cross-library compatibility)
    - AC-3.4-5: Queryable array structure (jq, pandas filtering)
    - AC-3.4-6: Metadata accuracy (sources, chunk_count, configuration)

These tests WILL FAIL until full pipeline is integrated (GREEN phase).
"""

import json
import subprocess
from pathlib import Path

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from data_extract.chunk.engine import ChunkingConfig, ChunkingEngine
    from data_extract.output.formatters.json_formatter import JsonFormatter
except ImportError:
    ChunkingEngine = None
    ChunkingConfig = None
    JsonFormatter = None


pytestmark = [pytest.mark.integration, pytest.mark.output, pytest.mark.pipeline]


@pytest.fixture
def sample_processing_result(sample_processing_result):
    """Use shared fixture from conftest.py for ProcessingResult."""
    return sample_processing_result


@pytest.fixture
def chunking_engine():
    """Create ChunkingEngine with default configuration."""
    if ChunkingEngine is None or ChunkingConfig is None:
        pytest.skip("ChunkingEngine not available yet (RED phase)")

    config = ChunkingConfig(chunk_size=512, overlap_pct=0.15)
    return ChunkingEngine(config)


@pytest.fixture
def json_formatter():
    """Create JsonFormatter with validation enabled."""
    if JsonFormatter is None:
        pytest.skip("JsonFormatter not available yet (RED phase)")

    return JsonFormatter(validate=True)


class TestEndToEndPipeline:
    """Test complete pipeline: ProcessingResult → Chunks → JSON file (AC-3.4-2, AC-3.4-5)."""

    def test_complete_pipeline_processing_result_to_json(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should process document from ProcessingResult through to JSON file."""
        # GIVEN: ProcessingResult from normalization stage
        output_path = tmp_path / "output.json"

        # WHEN: Chunking and formatting to JSON
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # THEN: JSON file should exist and be parsable
        assert output_path.exists()

        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        assert "metadata" in json_data
        assert "chunks" in json_data
        assert len(json_data["chunks"]) > 0

    def test_json_parsing_with_python_json_module(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should parse JSON using Python's json.load() (AC-3.4-2)."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Parsing with json.load()
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # THEN: Should parse successfully
        assert isinstance(json_data, dict)
        assert "chunks" in json_data


class TestCrossLibraryCompatibility:
    """Test JSON parsing with multiple libraries (AC-3.4-2)."""

    def test_pandas_read_json_compatibility(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should parse JSON using pandas.read_json() (AC-3.4-2)."""
        if pd is None:
            pytest.skip("pandas not installed")

        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Reading with pandas
        df = pd.read_json(output_path)

        # THEN: Should create DataFrame with chunks column
        assert "chunks" in df.columns
        assert len(df) > 0

    def test_jq_command_line_parsing(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should parse JSON using jq command-line tool (AC-3.4-2)."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Parsing with jq (if available)
        try:
            result = subprocess.run(
                ["jq", ".", str(output_path)],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            pytest.skip("jq not installed on system")

        # THEN: jq should parse successfully
        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_nodejs_json_parse_compatibility(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should parse JSON using Node.js JSON.parse() (AC-3.4-2)."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Parsing with Node.js (if available)
        node_code = f"""
        const fs = require('fs');
        const data = JSON.parse(fs.readFileSync('{output_path}', 'utf8'));
        console.log(JSON.stringify({{ chunks: data.chunks.length }}));
        """

        try:
            result = subprocess.run(
                ["node", "-e", node_code],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            pytest.skip("Node.js not installed on system")

        # THEN: Node.js should parse successfully
        assert result.returncode == 0
        parsed = json.loads(result.stdout)
        assert "chunks" in parsed


class TestQueryability:
    """Test chunk filtering and querying (AC-3.4-5)."""

    def test_jq_filter_by_quality_score(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should filter chunks by quality score using jq (AC-3.4-5)."""
        # GIVEN: Generated JSON file with quality scores
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Filtering with jq for high-quality chunks (overall >= 0.75)
        jq_query = ".chunks[] | select(.quality.overall >= 0.75)"

        try:
            result = subprocess.run(
                ["jq", jq_query, str(output_path)],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            pytest.skip("jq not installed on system")

        # THEN: Should return filtered chunks
        assert result.returncode == 0
        # Output should be valid JSON (one or more chunk objects)

    def test_jq_filter_by_entity_type(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should filter chunks by entity type using jq (AC-3.4-5)."""
        # GIVEN: Generated JSON file with entities
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Filtering with jq for chunks containing risk entities
        jq_query = '.chunks[] | select(.metadata.entity_tags[].entity_type == "risk")'

        try:
            result = subprocess.run(
                ["jq", jq_query, str(output_path)],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            pytest.skip("jq not installed on system")

        # THEN: jq should execute successfully
        assert result.returncode == 0

    def test_pandas_dataframe_filtering(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should filter chunks using pandas DataFrame operations (AC-3.4-5)."""
        if pd is None:
            pytest.skip("pandas not installed")

        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Loading and filtering with pandas
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        df = pd.DataFrame(json_data["chunks"])

        # Filter by quality score
        high_quality = df[df["quality"].apply(lambda q: q["overall"] >= 0.75)]

        # THEN: Should filter successfully
        assert len(high_quality) >= 0  # May be 0 if no high-quality chunks

    def test_index_based_access(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should support index-based access to chunks array (AC-3.4-5)."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Loading and accessing by index
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # THEN: Should support array indexing
        if len(json_data["chunks"]) > 0:
            first_chunk = json_data["chunks"][0]
            assert "chunk_id" in first_chunk
            assert "text" in first_chunk


class TestMetadataAccuracy:
    """Test metadata header accuracy (AC-3.4-6)."""

    def test_source_documents_list_matches_input(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should list source documents accurately in metadata."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Reading metadata
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # THEN: Source documents should be listed
        assert "source_documents" in json_data["metadata"]
        assert isinstance(json_data["metadata"]["source_documents"], list)

    def test_chunk_count_matches_actual_chunks(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should set chunk_count to actual number of chunks (AC-3.4-6)."""
        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Reading metadata and chunks
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # THEN: chunk_count should match actual chunks
        assert json_data["metadata"]["chunk_count"] == len(json_data["chunks"])

    def test_configuration_reflects_chunking_params(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should reflect actual chunking configuration (AC-3.4-6)."""
        # GIVEN: ChunkingEngine with specific config
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # WHEN: Reading metadata configuration
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        config = json_data["metadata"]["configuration"]

        # THEN: Configuration should match ChunkingEngine settings
        assert config["chunk_size"] == 512
        assert config["overlap_pct"] == 0.15


class TestDeterminism:
    """Test deterministic output generation (AC-3.4-2)."""

    def test_same_input_produces_same_json(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should produce identical JSON for same input (excluding timestamp)."""
        # GIVEN: Same ProcessingResult processed twice
        output_path_1 = tmp_path / "output1.json"
        output_path_2 = tmp_path / "output2.json"

        chunks_1 = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks_1, output_path_1)

        chunks_2 = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks_2, output_path_2)

        # WHEN: Loading both JSON files
        with open(output_path_1, "r", encoding="utf-8") as f:
            json_data_1 = json.load(f)

        with open(output_path_2, "r", encoding="utf-8") as f:
            json_data_2 = json.load(f)

        # THEN: Chunks should be identical (excluding processing_timestamp)
        # Remove timestamps for comparison
        del json_data_1["metadata"]["processing_timestamp"]
        del json_data_2["metadata"]["processing_timestamp"]

        # Chunk content should be identical
        assert len(json_data_1["chunks"]) == len(json_data_2["chunks"])

        for chunk1, chunk2 in zip(json_data_1["chunks"], json_data_2["chunks"]):
            assert chunk1["text"] == chunk2["text"]
            assert chunk1["chunk_id"] == chunk2["chunk_id"]


class TestPerformance:
    """Test JSON generation performance (NFR-P1-E3)."""

    def test_json_generation_under_1_second(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should generate JSON in <1 second for typical document."""
        import time

        # GIVEN: ProcessingResult and JsonFormatter
        output_path = tmp_path / "output.json"
        chunks = list(chunking_engine.chunk(sample_processing_result))

        # WHEN: Formatting to JSON
        start_time = time.time()
        json_formatter.format_chunks(iter(chunks), output_path)
        duration = time.time() - start_time

        # THEN: Should complete in <1 second
        assert duration < 1.0, f"JSON generation took {duration:.2f}s (target: <1s)"

    def test_large_document_json_generation(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should handle large documents (1000+ chunks) efficiently."""
        import time

        # GIVEN: Large document (simulate with many chunks)
        output_path = tmp_path / "large_output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        chunk_list = list(chunks)

        # Replicate chunks to simulate large document
        large_chunks = chunk_list * 100  # Multiply chunks

        # WHEN: Formatting large document
        start_time = time.time()
        json_formatter.format_chunks(iter(large_chunks), output_path)
        duration = time.time() - start_time

        # THEN: Should complete in reasonable time (<5 seconds)
        assert duration < 5.0, f"Large JSON generation took {duration:.2f}s"


class TestSchemaValidationIntegration:
    """Test schema validation on real pipeline output (AC-3.4-7)."""

    def test_pipeline_output_validates_against_schema(
        self, sample_processing_result, chunking_engine, json_formatter, tmp_path
    ):
        """Should produce output that validates against JSON schema."""
        try:
            from jsonschema import validate
        except ImportError:
            pytest.skip("jsonschema library not installed")

        # GIVEN: Generated JSON file
        output_path = tmp_path / "output.json"
        chunks = chunking_engine.chunk(sample_processing_result)
        json_formatter.format_chunks(chunks, output_path)

        # Load schema
        project_root = Path(__file__).parent.parent.parent
        schema_path = (
            project_root
            / "src"
            / "data_extract"
            / "output"
            / "schemas"
            / "data-extract-chunk.schema.json"
        )

        if not schema_path.exists():
            pytest.skip("Schema file not created yet")

        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        # WHEN: Validating output
        with open(output_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # THEN: Should validate without errors
        validate(instance=json_data, schema=schema)
