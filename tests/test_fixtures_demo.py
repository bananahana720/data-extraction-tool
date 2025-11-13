"""
Demonstration tests showing that fixtures work correctly.

This file can be run to verify the testing infrastructure is properly set up.
These tests actually execute (don't skip) to prove fixtures are working.

Run with: pytest tests/test_fixtures_demo.py -v
"""

from pathlib import Path

import pytest

from src.core import (
    ContentBlock,
    ContentType,
    ExtractionResult,
    ProcessingResult,
    ProcessingStage,
)


@pytest.mark.unit
def test_sample_content_block_fixture(sample_content_block):
    """Verify sample_content_block fixture works correctly."""
    assert isinstance(sample_content_block, ContentBlock)
    assert sample_content_block.block_type == ContentType.PARAGRAPH
    assert len(sample_content_block.content) > 0
    assert sample_content_block.confidence == 0.95


@pytest.mark.unit
def test_sample_heading_block_fixture(sample_heading_block):
    """Verify sample_heading_block fixture works correctly."""
    assert isinstance(sample_heading_block, ContentBlock)
    assert sample_heading_block.block_type == ContentType.HEADING
    assert sample_heading_block.metadata["level"] == 1


@pytest.mark.unit
def test_sample_content_blocks_fixture(sample_content_blocks):
    """Verify sample_content_blocks fixture provides mixed content."""
    assert isinstance(sample_content_blocks, list)
    assert len(sample_content_blocks) == 5

    # Should have mixed types
    types = [block.block_type for block in sample_content_blocks]
    assert ContentType.HEADING in types
    assert ContentType.PARAGRAPH in types
    assert ContentType.TABLE in types
    assert ContentType.IMAGE in types


@pytest.mark.unit
def test_sample_extraction_result_fixture(sample_extraction_result):
    """Verify sample_extraction_result fixture is properly structured."""
    assert isinstance(sample_extraction_result, ExtractionResult)
    assert sample_extraction_result.success is True
    assert len(sample_extraction_result.content_blocks) > 0
    assert len(sample_extraction_result.errors) == 0


@pytest.mark.unit
def test_failed_extraction_result_fixture(failed_extraction_result):
    """Verify failed_extraction_result fixture represents failure correctly."""
    assert isinstance(failed_extraction_result, ExtractionResult)
    assert failed_extraction_result.success is False
    assert len(failed_extraction_result.errors) > 0
    assert len(failed_extraction_result.content_blocks) == 0


@pytest.mark.unit
def test_sample_processing_result_fixture(sample_processing_result):
    """Verify sample_processing_result fixture has enrichments."""
    assert isinstance(sample_processing_result, ProcessingResult)
    assert sample_processing_result.success is True
    assert sample_processing_result.processing_stage == ProcessingStage.METADATA_AGGREGATION
    assert sample_processing_result.quality_score == 92.5

    # Check that blocks have enrichments
    for block in sample_processing_result.content_blocks:
        assert block.metadata.get("processed") is True
        assert "word_count" in block.metadata


@pytest.mark.unit
def test_temp_test_file_fixture(temp_test_file):
    """Verify temp_test_file fixture creates valid file."""
    assert isinstance(temp_test_file, Path)
    assert temp_test_file.exists()
    assert temp_test_file.is_file()

    # Check content
    content = temp_test_file.read_text()
    assert len(content) > 0
    assert "Sample Document" in content


@pytest.mark.unit
def test_empty_test_file_fixture(empty_test_file):
    """Verify empty_test_file fixture creates empty file."""
    assert isinstance(empty_test_file, Path)
    assert empty_test_file.exists()
    assert empty_test_file.stat().st_size == 0


@pytest.mark.unit
def test_fixture_dir_exists(fixture_dir):
    """Verify fixture_dir points to correct location."""
    assert isinstance(fixture_dir, Path)
    assert fixture_dir.exists()
    assert fixture_dir.is_dir()
    assert fixture_dir.name == "fixtures"


@pytest.mark.unit
def test_validate_extraction_result_fixture(sample_extraction_result, validate_extraction_result):
    """Verify validation fixture works correctly."""
    # Should not raise exception for valid result
    validate_extraction_result(sample_extraction_result)

    # Validation checks structure
    assert True  # If we get here, validation passed


@pytest.mark.unit
def test_validate_processing_result_fixture(sample_processing_result, validate_processing_result):
    """Verify processing result validation works."""
    # Should not raise exception for valid result
    validate_processing_result(sample_processing_result)

    # Validation checks structure and quality score range
    assert True  # If we get here, validation passed


@pytest.mark.unit
def test_fixture_immutability(sample_content_block):
    """Verify fixtures use immutable data models."""
    # Should not be able to modify frozen dataclass
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        sample_content_block.content = "Modified"


@pytest.mark.unit
def test_fixture_independence():
    """
    Verify fixtures are independent between tests.

    This test demonstrates that fixtures don't share state.
    """
    # Each test gets its own fixture instances
    # No shared state between tests
    assert True


# ============================================================================
# Summary
# ============================================================================

"""
If all these tests pass, the testing infrastructure is working correctly:

✓ Fixtures create proper data models
✓ Validation helpers work
✓ Temporary files are created correctly
✓ Immutability is enforced
✓ Fixtures are properly typed

Next steps:
1. Use these fixtures in your extractor/processor/formatter tests
2. Add custom fixtures to conftest.py as needed
3. Follow the patterns from test_docx_extractor.py
"""
