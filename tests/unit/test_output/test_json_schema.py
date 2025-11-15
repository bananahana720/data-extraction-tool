"""Unit tests for JSON Schema validation (Story 3.4 - ATDD RED PHASE).

Tests JSON Schema loading, validation of valid chunk JSON, rejection of invalid JSON,
and enforcement of constraints (score ranges, enums, patterns).

Test Coverage:
    - AC-3.4-7: JSON validates against schema (JSON Schema Draft 7)

These tests WILL FAIL until schema file is created (GREEN phase).
"""

import json
from pathlib import Path

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from jsonschema import ValidationError, validate
except ImportError:
    validate = None
    ValidationError = None

pytestmark = [pytest.mark.unit, pytest.mark.output, pytest.mark.schema]


@pytest.fixture
def schema_path() -> Path:
    """Get path to JSON Schema file."""
    project_root = Path(__file__).parent.parent.parent.parent
    return (
        project_root
        / "src"
        / "data_extract"
        / "output"
        / "schemas"
        / "data-extract-chunk.schema.json"
    )


@pytest.fixture
def schema(schema_path):
    """Load JSON Schema from file."""
    if not schema_path.exists():
        pytest.skip("Schema file not created yet (RED phase)")

    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def valid_chunk_json():
    """Create valid chunk JSON that should pass schema validation."""
    return {
        "metadata": {
            "processing_version": "1.0.0-epic3",
            "processing_timestamp": "2025-11-14T20:30:00Z",
            "configuration": {
                "chunk_size": 512,
                "overlap_pct": 0.15,
                "entity_aware": True,
                "quality_enrichment": True,
            },
            "source_documents": ["test_doc.pdf"],
            "chunk_count": 1,
        },
        "chunks": [
            {
                "chunk_id": "test_doc_001",
                "text": "This is a test chunk with valid content.",
                "metadata": {
                    "entity_tags": [],
                    "section_context": "Introduction",
                    "entity_relationships": [],
                    "source_metadata": None,
                    "quality": {
                        "readability_flesch_kincaid": 8.5,
                        "readability_gunning_fog": 10.2,
                        "ocr_confidence": 0.99,
                        "completeness": 0.95,
                        "coherence": 0.88,
                        "overall": 0.93,
                        "flags": [],
                    },
                    "source_hash": "a3b2c1d4e5f6",
                    "document_type": "report",
                    "word_count": 8,
                    "token_count": 10,
                    "created_at": "2025-11-14T20:30:00Z",
                    "processing_version": "1.0.0-epic3",
                },
                "entities": [],
                "quality": {
                    "readability_flesch_kincaid": 8.5,
                    "readability_gunning_fog": 10.2,
                    "ocr_confidence": 0.99,
                    "completeness": 0.95,
                    "coherence": 0.88,
                    "overall": 0.93,
                    "flags": [],
                },
            }
        ],
    }


class TestSchemaLoading:
    """Test JSON Schema file loading and structure (AC-3.4-7)."""

    def test_schema_file_exists(self, schema_path):
        """Should have schema file at expected location."""
        # GIVEN/WHEN: Schema path constructed
        # THEN: Schema file should exist
        assert schema_path.exists(), f"Schema file not found at {schema_path}"

    def test_schema_is_valid_json(self, schema_path):
        """Should load as valid JSON."""
        # GIVEN: Schema file exists
        # WHEN: Loading schema file
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_data = json.load(f)

        # THEN: Should parse without errors
        assert schema_data is not None
        assert isinstance(schema_data, dict)

    def test_schema_is_json_schema_draft_7(self, schema):
        """Should declare JSON Schema Draft 7 compliance (AC-3.4-7)."""
        # GIVEN: Schema loaded
        # WHEN/THEN: Schema should have Draft 7 $schema declaration
        assert "$schema" in schema
        assert "draft-07" in schema["$schema"] or "draft/2019-09" in schema["$schema"]

    def test_schema_has_required_definitions(self, schema):
        """Should define root object schema with metadata and chunks."""
        # GIVEN: Schema loaded
        # WHEN/THEN: Schema should define required structure
        assert "type" in schema
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "metadata" in schema["properties"]
        assert "chunks" in schema["properties"]


class TestValidJsonValidation:
    """Test schema validation of valid chunk JSON (AC-3.4-7)."""

    def test_valid_chunk_json_passes_validation(self, schema, valid_chunk_json):
        """Should validate valid chunk JSON without errors."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: Valid chunk JSON
        # WHEN: Validating against schema
        # THEN: Should not raise ValidationError
        validate(instance=valid_chunk_json, schema=schema)

    def test_empty_chunks_array_valid(self, schema):
        """Should accept empty chunks array as valid."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with empty chunks array
        json_data = {
            "metadata": {
                "processing_version": "1.0.0",
                "processing_timestamp": "2025-11-14T20:30:00Z",
                "configuration": {
                    "chunk_size": 512,
                    "overlap_pct": 0.15,
                    "entity_aware": False,
                    "quality_enrichment": False,
                },
                "source_documents": [],
                "chunk_count": 0,
            },
            "chunks": [],
        }

        # WHEN: Validating against schema
        # THEN: Should not raise ValidationError
        validate(instance=json_data, schema=schema)


class TestInvalidJsonRejection:
    """Test schema rejection of invalid JSON (AC-3.4-7)."""

    def test_missing_required_field_metadata(self, schema, valid_chunk_json):
        """Should reject JSON missing required 'metadata' field."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON missing metadata field
        invalid_json = valid_chunk_json.copy()
        del invalid_json["metadata"]

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_missing_required_field_chunks(self, schema, valid_chunk_json):
        """Should reject JSON missing required 'chunks' field."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON missing chunks field
        invalid_json = valid_chunk_json.copy()
        del invalid_json["chunks"]

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_chunks_not_array_rejected(self, schema, valid_chunk_json):
        """Should reject chunks field that is not an array."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with chunks as object instead of array
        invalid_json = valid_chunk_json.copy()
        invalid_json["chunks"] = {"chunk_001": "test"}

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)


class TestScoreRangeValidation:
    """Test schema enforcement of score ranges (AC-3.4-7)."""

    def test_quality_score_above_1_rejected(self, schema, valid_chunk_json):
        """Should reject quality scores > 1.0."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with overall score > 1.0
        invalid_json = valid_chunk_json.copy()
        invalid_json["chunks"][0]["quality"]["overall"] = 1.5

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_quality_score_below_0_rejected(self, schema, valid_chunk_json):
        """Should reject quality scores < 0.0."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with overall score < 0.0
        invalid_json = valid_chunk_json.copy()
        invalid_json["chunks"][0]["quality"]["overall"] = -0.1

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_readability_score_above_30_rejected(self, schema, valid_chunk_json):
        """Should reject readability scores > 30.0."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with Flesch-Kincaid > 30.0
        invalid_json = valid_chunk_json.copy()
        invalid_json["chunks"][0]["quality"]["readability_flesch_kincaid"] = 35.0

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)


class TestEnumValidation:
    """Test schema enforcement of enum values (AC-3.4-7)."""

    def test_invalid_document_type_rejected(self, schema, valid_chunk_json):
        """Should reject invalid document_type values."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with invalid document_type
        invalid_json = valid_chunk_json.copy()
        invalid_json["chunks"][0]["metadata"]["document_type"] = "invalid_type"

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_valid_document_types_accepted(self, schema, valid_chunk_json):
        """Should accept valid document_type enum values: report, matrix, export, image."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: Valid document types
        valid_types = ["report", "matrix", "export", "image"]

        # WHEN/THEN: Each valid type should pass validation
        for doc_type in valid_types:
            test_json = valid_chunk_json.copy()
            test_json["chunks"][0]["metadata"]["document_type"] = doc_type
            validate(instance=test_json, schema=schema)


class TestStringPatternValidation:
    """Test schema enforcement of string patterns (AC-3.4-7)."""

    def test_chunk_id_pattern_validation(self, schema, valid_chunk_json):
        """Should validate chunk_id format (alphanumeric with underscores/hyphens)."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: Valid chunk_id patterns
        valid_ids = ["doc_001", "test-chunk-01", "file123_chunk456"]

        # WHEN/THEN: Valid IDs should pass validation
        for chunk_id in valid_ids:
            test_json = valid_chunk_json.copy()
            test_json["chunks"][0]["chunk_id"] = chunk_id
            validate(instance=test_json, schema=schema)

    def test_source_hash_pattern_validation(self, schema, valid_chunk_json):
        """Should validate source_hash as hexadecimal string."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: Valid SHA-256 hash (64 hex characters)
        valid_hash = "a" * 64  # 64 hex chars

        # WHEN: Validating with valid hash
        test_json = valid_chunk_json.copy()
        test_json["chunks"][0]["metadata"]["source_hash"] = valid_hash

        # THEN: Should pass validation
        validate(instance=test_json, schema=schema)


class TestNestedObjectValidation:
    """Test schema validation of nested objects (AC-3.4-7)."""

    def test_quality_score_nested_validation(self, schema, valid_chunk_json):
        """Should validate nested QualityScore object structure."""
        if validate is None or ValidationError is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with incomplete quality object (missing required field)
        invalid_json = valid_chunk_json.copy()
        del invalid_json["chunks"][0]["quality"]["overall"]

        # WHEN/THEN: Validation should raise ValidationError
        with pytest.raises(ValidationError):
            validate(instance=invalid_json, schema=schema)

    def test_entity_reference_nested_validation(self, schema, valid_chunk_json):
        """Should validate nested EntityReference object structure."""
        if validate is None:
            pytest.skip("jsonschema library not installed")

        # GIVEN: JSON with valid entity reference
        test_json = valid_chunk_json.copy()
        test_json["chunks"][0]["metadata"]["entity_tags"] = [
            {
                "entity_type": "risk",
                "entity_id": "RISK-001",
                "start_pos": 50,
                "end_pos": 70,
                "is_partial": False,
                "context_snippet": "test",
            }
        ]

        # WHEN: Validating with entity
        # THEN: Should pass validation
        validate(instance=test_json, schema=schema)
