"""
Test suite for TextFileExtractor - Plain Text Document Extraction

This test suite follows TDD methodology (Red-Green-Refactor) to validate
text file extraction functionality.

Test Coverage:
- Basic functionality (UTF-8, line endings, paragraphs)
- Edge cases (empty, binary, corrupted, permission errors)
- ContentBlock generation (IDs, positions, metadata)
- BaseExtractor integration (validation, format support)
- Heading detection heuristics
- Error handling and recovery

Coverage Target: 85%+ (20+ tests)
"""

import sys
from pathlib import Path
from uuid import UUID

import pytest

# Import the extractor under test
from extractors.txt_extractor import TextFileExtractor

# Import core models
from src.core import (
    ContentType,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def extractor():
    """Create a TextFileExtractor instance for testing."""
    return TextFileExtractor()


@pytest.fixture
def simple_txt_file(tmp_path):
    """
    Create a simple text file with paragraphs.

    Returns:
        Path to test file with 3 paragraphs
    """
    file_path = tmp_path / "simple.txt"
    content = """First paragraph with some content.

Second paragraph with more content.

Third paragraph for testing."""
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def empty_txt_file(tmp_path):
    """Create an empty text file."""
    file_path = tmp_path / "empty.txt"
    file_path.touch()
    return file_path


@pytest.fixture
def file_with_headings(tmp_path):
    """
    Create a text file with headings and paragraphs.

    Headings are detected by being short and not ending with punctuation.
    """
    file_path = tmp_path / "with_headings.txt"
    content = """Introduction

This is a paragraph under the introduction heading.
It has multiple sentences. This makes it clearly a paragraph.

Key Features

This section describes key features.
It also has multiple sentences."""
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def large_txt_file(tmp_path):
    """Create a large text file for performance testing."""
    file_path = tmp_path / "large.txt"
    paragraphs = []
    for i in range(100):
        paragraphs.append(f"Paragraph {i}: This is test content for performance validation.")
    content = "\n\n".join(paragraphs)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def special_chars_file(tmp_path):
    """Create a text file with special characters and unicode."""
    file_path = tmp_path / "special_chars.txt"
    content = """Unicode Test: émojis 🎉 中文 ñ

Special characters: @#$%^&*()

Tab\tcharacters\there.

Line with "quotes" and 'apostrophes'."""
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def mixed_line_endings_file(tmp_path):
    """Create a file with mixed line endings (CRLF and LF)."""
    file_path = tmp_path / "mixed_endings.txt"
    # Manually write with different line endings
    with open(file_path, "wb") as f:
        f.write(b"First paragraph\r\n\r\n")  # CRLF
        f.write(b"Second paragraph\n\n")  # LF
        f.write(b"Third paragraph")  # No ending
    return file_path


@pytest.fixture
def long_lines_file(tmp_path):
    """Create a file with very long lines."""
    file_path = tmp_path / "long_lines.txt"
    long_line = "A" * 1000 + " word " + "B" * 1000
    content = f"{long_line}\n\nSecond paragraph with normal length."
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture
def binary_file(tmp_path):
    """Create a binary file (not valid UTF-8 text)."""
    file_path = tmp_path / "binary.bin"
    file_path.write_bytes(b"\x00\x01\x02\xff\xfe\xfd")
    return file_path


@pytest.fixture
def whitespace_only_file(tmp_path):
    """Create a file with only whitespace."""
    file_path = tmp_path / "whitespace.txt"
    content = "   \n\n   \t\t\n\n   "
    file_path.write_text(content, encoding="utf-8")
    return file_path


# ============================================================================
# Category 1: Basic Functionality Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.extraction
def test_001_extract_simple_text_file(extractor, simple_txt_file):
    """
    Test basic text extraction from a simple file.

    RED: Write failing test that expects successful extraction
    GREEN: Verify test passes with existing implementation
    REFACTOR: N/A - implementation already exists
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True
    assert len(result.errors) == 0
    assert len(result.content_blocks) == 3  # Three paragraphs

    # Verify content is extracted
    all_content = " ".join(block.content for block in result.content_blocks)
    assert "First paragraph" in all_content
    assert "Second paragraph" in all_content
    assert "Third paragraph" in all_content


@pytest.mark.unit
@pytest.mark.extraction
def test_002_utf8_encoding_support(extractor, special_chars_file):
    """
    Test UTF-8 encoding support with special characters.

    Validates that unicode characters are properly extracted.
    """
    # Act
    result = extractor.extract(special_chars_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) > 0

    # Verify unicode characters are preserved
    all_content = " ".join(block.content for block in result.content_blocks)
    assert "émojis" in all_content
    assert "🎉" in all_content
    assert "中文" in all_content
    assert "ñ" in all_content


@pytest.mark.unit
@pytest.mark.extraction
def test_003_different_line_endings(extractor, mixed_line_endings_file):
    """
    Test handling of different line endings (CRLF, LF).

    Text files from Windows (CRLF) and Unix (LF) should both work.
    """
    # Act
    result = extractor.extract(mixed_line_endings_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 3  # Three paragraphs

    # Verify all paragraphs extracted
    contents = [block.content for block in result.content_blocks]
    assert any("First paragraph" in c for c in contents)
    assert any("Second paragraph" in c for c in contents)
    assert any("Third paragraph" in c for c in contents)


@pytest.mark.unit
@pytest.mark.extraction
def test_004_empty_file_handling(extractor, empty_txt_file):
    """
    Test extraction of empty file.

    Empty files fail validation (from BaseExtractor), returning success=False.
    This is expected behavior - empty files are invalid.
    """
    # Act
    result = extractor.extract(empty_txt_file)

    # Assert
    assert result.success is False
    assert len(result.content_blocks) == 0
    assert len(result.errors) > 0

    # Verify error mentions empty file
    error_text = " ".join(result.errors).lower()
    assert "empty" in error_text


@pytest.mark.unit
@pytest.mark.extraction
def test_005_very_large_file_performance(extractor, large_txt_file):
    """
    Test extraction performance on large files.

    Large files should extract reasonably quickly.
    """
    import time

    # Act
    start_time = time.time()
    result = extractor.extract(large_txt_file)
    duration = time.time() - start_time

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 100  # 100 paragraphs

    # Performance check: should complete in < 1 second for 100 paragraphs
    assert duration < 1.0, f"Extraction took {duration:.2f}s (target: <1s)"


@pytest.mark.unit
@pytest.mark.extraction
def test_006_special_characters_preserved(extractor, special_chars_file):
    """
    Test that special characters are preserved.

    Characters like @#$%^&*() should not be stripped or escaped.
    """
    # Act
    result = extractor.extract(special_chars_file)

    # Assert
    assert result.success is True

    # Verify special characters preserved
    all_content = " ".join(block.content for block in result.content_blocks)
    assert "@#$%^&*()" in all_content
    assert '"quotes"' in all_content
    assert "'apostrophes'" in all_content


@pytest.mark.unit
@pytest.mark.extraction
def test_007_multiple_paragraphs_separated(extractor, simple_txt_file):
    """
    Test that paragraphs are properly separated.

    Double newlines should create separate ContentBlocks.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 3

    # Each block should be a different paragraph
    block_contents = [b.content for b in result.content_blocks]
    assert "First paragraph" in block_contents[0]
    assert "Second paragraph" in block_contents[1]
    assert "Third paragraph" in block_contents[2]


@pytest.mark.unit
@pytest.mark.extraction
def test_008_whitespace_only_file_handling(extractor, whitespace_only_file):
    """
    Test file with only whitespace characters.

    Should handle gracefully without creating empty blocks.
    """
    # Act
    result = extractor.extract(whitespace_only_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 0  # No real content
    assert len(result.warnings) > 0  # Should warn about no content


# ============================================================================
# Category 2: Edge Cases Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.extraction
def test_101_nonexistent_file(extractor, tmp_path):
    """
    Test extraction of non-existent file.

    Should return failure with appropriate error message.
    """
    # Arrange
    missing_file = tmp_path / "does_not_exist.txt"

    # Act
    result = extractor.extract(missing_file)

    # Assert
    assert result.success is False
    assert len(result.errors) > 0

    # Verify error message mentions file not found
    error_text = " ".join(result.errors).lower()
    assert "not found" in error_text or "does not exist" in error_text


@pytest.mark.unit
@pytest.mark.extraction
def test_102_binary_file_fails_gracefully(extractor, binary_file):
    """
    Test extraction of binary file (not valid UTF-8).

    Should fail gracefully with UnicodeDecodeError handling.
    """
    # Act
    result = extractor.extract(binary_file)

    # Assert
    assert result.success is False
    assert len(result.errors) > 0

    # Verify error mentions UTF-8 or encoding issue
    error_text = " ".join(result.errors).lower()
    assert "utf-8" in error_text or "encoding" in error_text or "text" in error_text


@pytest.mark.unit
@pytest.mark.extraction
def test_103_corrupted_file_with_null_bytes(extractor, tmp_path):
    """
    Test file with null bytes (corrupted text).

    Should handle without crashing. Python can actually handle null bytes
    in UTF-8 text, so this may succeed.
    """
    # Arrange
    file_path = tmp_path / "null_bytes.txt"
    file_path.write_bytes(b"Text with\x00null\x00bytes")

    # Act
    result = extractor.extract(file_path)

    # Assert
    # Python handles null bytes in text, so this succeeds
    # Either way, should not crash and return proper result
    assert result is not None
    assert hasattr(result, "success")
    assert isinstance(result.success, bool)


@pytest.mark.unit
@pytest.mark.extraction
def test_104_extremely_long_single_line(extractor, long_lines_file):
    """
    Test file with extremely long lines (>1000 characters).

    Should handle without memory issues.
    """
    # Act
    result = extractor.extract(long_lines_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) >= 1

    # Verify long line was extracted
    first_block = result.content_blocks[0]
    assert len(first_block.content) > 1000


@pytest.mark.unit
@pytest.mark.extraction
def test_105_mixed_encoding_file(extractor, tmp_path):
    """
    Test file with non-UTF-8 encoding.

    Should fail with encoding error.
    """
    # Arrange
    file_path = tmp_path / "latin1.txt"
    # Write with Latin-1 encoding (not UTF-8)
    with open(file_path, "w", encoding="latin-1") as f:
        f.write("Text with Latin-1 character: \xe9")  # é in Latin-1

    # Act
    result = extractor.extract(file_path)

    # Assert
    # Depending on character, may succeed or fail
    # If fails, should have encoding error
    if not result.success:
        error_text = " ".join(result.errors).lower()
        assert "utf-8" in error_text or "encoding" in error_text


@pytest.mark.unit
@pytest.mark.extraction
@pytest.mark.skipif(sys.platform == "win32", reason="Permission tests unreliable on Windows")
def test_106_read_permission_denied(extractor, simple_txt_file):
    """
    Test extraction when file has no read permissions.

    Should fail with permission error.
    """
    import os
    import stat

    try:
        # Remove read permissions
        os.chmod(simple_txt_file, 0o000)

        # Act
        result = extractor.extract(simple_txt_file)

        # Assert
        assert result.success is False
        assert len(result.errors) > 0

    finally:
        # Restore permissions for cleanup
        os.chmod(simple_txt_file, stat.S_IRUSR | stat.S_IWUSR)


@pytest.mark.unit
@pytest.mark.extraction
def test_107_directory_instead_of_file(extractor, tmp_path):
    """
    Test extraction when path is a directory, not a file.

    Should fail validation.
    """
    # Arrange
    directory = tmp_path / "subdir"
    directory.mkdir()

    # Act
    result = extractor.extract(directory)

    # Assert
    assert result.success is False
    assert len(result.errors) > 0

    # Verify error mentions not a file
    error_text = " ".join(result.errors).lower()
    assert "not a file" in error_text or "directory" in error_text


@pytest.mark.unit
@pytest.mark.extraction
def test_108_file_with_bom(extractor, tmp_path):
    """
    Test file with UTF-8 BOM (Byte Order Mark).

    Python's UTF-8 decoder reads BOM but includes it as U+FEFF character.
    We test that the file is handled correctly.
    """
    # Arrange
    file_path = tmp_path / "with_bom.txt"
    # Write with UTF-8 BOM
    content = "Text with BOM"
    file_path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))

    # Act
    result = extractor.extract(file_path)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) > 0

    # Python includes BOM as \ufeff character in the text
    first_content = result.content_blocks[0].content
    # Verify BOM is present or content is readable
    assert "Text with BOM" in first_content


# ============================================================================
# Category 3: ContentBlock Generation Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.extraction
def test_201_block_id_generation_is_unique(extractor, simple_txt_file):
    """
    Test that each ContentBlock has a unique block_id.

    block_id should be a valid UUID.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) > 0

    # Collect all block IDs
    block_ids = [block.block_id for block in result.content_blocks]

    # Verify all are UUIDs
    for block_id in block_ids:
        assert isinstance(block_id, UUID)

    # Verify all are unique
    assert len(block_ids) == len(set(block_ids))


@pytest.mark.unit
@pytest.mark.extraction
def test_202_position_information_is_correct(extractor, simple_txt_file):
    """
    Test that position information is correctly set.

    sequence_index should increment for each block.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 3

    # Verify sequence indices
    for idx, block in enumerate(result.content_blocks):
        assert block.position is not None
        assert block.position.sequence_index == idx


@pytest.mark.unit
@pytest.mark.extraction
def test_203_metadata_includes_character_count(extractor, simple_txt_file):
    """
    Test that metadata includes char_count.

    Each block should have character and word counts.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True

    # Verify metadata
    for block in result.content_blocks:
        assert "char_count" in block.metadata
        assert "word_count" in block.metadata

        # Verify counts are accurate
        assert block.metadata["char_count"] == len(block.content)
        assert block.metadata["word_count"] == len(block.content.split())


@pytest.mark.unit
@pytest.mark.extraction
def test_204_heading_detection_short_lines(extractor, file_with_headings):
    """
    Test heading detection for short lines without punctuation.

    Lines < 80 chars without ending punctuation should be HEADING.
    """
    # Act
    result = extractor.extract(file_with_headings)

    # Assert
    assert result.success is True

    # Find heading blocks
    heading_blocks = [b for b in result.content_blocks if b.block_type == ContentType.HEADING]
    paragraph_blocks = [b for b in result.content_blocks if b.block_type == ContentType.PARAGRAPH]

    # Should have at least 2 headings
    assert len(heading_blocks) >= 2

    # Should also have paragraphs
    assert len(paragraph_blocks) >= 2

    # Verify headings are short
    for heading in heading_blocks:
        assert len(heading.content) < 80


@pytest.mark.unit
@pytest.mark.extraction
def test_205_paragraph_detection_long_lines(extractor):
    """
    Test that long lines are detected as paragraphs.

    Lines > 80 chars should be PARAGRAPH regardless of punctuation.
    """
    # Arrange
    file_path = Path("test_long_para.txt")
    long_paragraph = "A" * 100  # 100 chars, no punctuation

    # Create temporary file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(long_paragraph)
        temp_path = Path(f.name)

    try:
        # Act
        result = extractor.extract(temp_path)

        # Assert
        assert result.success is True
        assert len(result.content_blocks) == 1

        block = result.content_blocks[0]
        assert block.block_type == ContentType.PARAGRAPH

    finally:
        # Cleanup
        temp_path.unlink(missing_ok=True)


@pytest.mark.unit
@pytest.mark.extraction
def test_206_confidence_score_is_high(extractor, simple_txt_file):
    """
    Test that confidence score is high for plain text.

    Plain text extraction should have confidence = 1.0.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True

    # Verify high confidence
    for block in result.content_blocks:
        assert block.confidence == 1.0


# ============================================================================
# Category 4: Integration with BaseExtractor Tests
# ============================================================================


@pytest.mark.unit
def test_301_validate_file_implementation(extractor, simple_txt_file):
    """
    Test validate_file method implementation.

    Should return (True, []) for valid files.
    """
    # Act
    is_valid, errors = extractor.validate_file(simple_txt_file)

    # Assert
    assert is_valid is True
    assert len(errors) == 0


@pytest.mark.unit
def test_302_validate_file_missing_file(extractor, tmp_path):
    """
    Test validate_file with missing file.

    Should return (False, [error_message]).
    """
    # Arrange
    missing_file = tmp_path / "missing.txt"

    # Act
    is_valid, errors = extractor.validate_file(missing_file)

    # Assert
    assert is_valid is False
    assert len(errors) > 0
    assert "not found" in errors[0].lower()


@pytest.mark.unit
def test_303_validate_file_empty_file(extractor, empty_txt_file):
    """
    Test validate_file with empty file.

    Should return (False, [error_message]) since empty files are invalid.
    """
    # Act
    is_valid, errors = extractor.validate_file(empty_txt_file)

    # Assert
    assert is_valid is False
    assert len(errors) > 0
    assert "empty" in errors[0].lower()


@pytest.mark.unit
def test_304_get_supported_extensions(extractor):
    """
    Test get_supported_extensions returns correct extensions.

    Should return ['.txt', '.md', '.log'].
    """
    # Act
    extensions = extractor.get_supported_extensions()

    # Assert
    assert isinstance(extensions, list)
    assert ".txt" in extensions
    assert ".md" in extensions
    assert ".log" in extensions


@pytest.mark.unit
def test_305_supports_format_txt_files(extractor, tmp_path):
    """
    Test supports_format returns True for .txt files.
    """
    # Arrange
    txt_file = tmp_path / "test.txt"
    txt_file.touch()

    # Act
    result = extractor.supports_format(txt_file)

    # Assert
    assert result is True


@pytest.mark.unit
def test_306_supports_format_md_files(extractor, tmp_path):
    """
    Test supports_format returns True for .md files.
    """
    # Arrange
    md_file = tmp_path / "test.md"
    md_file.touch()

    # Act
    result = extractor.supports_format(md_file)

    # Assert
    assert result is True


@pytest.mark.unit
def test_307_supports_format_log_files(extractor, tmp_path):
    """
    Test supports_format returns True for .log files.
    """
    # Arrange
    log_file = tmp_path / "test.log"
    log_file.touch()

    # Act
    result = extractor.supports_format(log_file)

    # Assert
    assert result is True


@pytest.mark.unit
def test_308_supports_format_rejects_other_formats(extractor, tmp_path):
    """
    Test supports_format returns False for non-text files.
    """
    # Arrange
    pdf_file = tmp_path / "test.pdf"
    pdf_file.touch()

    # Act
    result = extractor.supports_format(pdf_file)

    # Assert
    assert result is False


@pytest.mark.unit
@pytest.mark.extraction
def test_309_extraction_result_structure(extractor, simple_txt_file):
    """
    Test that ExtractionResult has proper structure.

    Validates all required fields are populated correctly.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert - ExtractionResult structure
    assert result is not None
    assert hasattr(result, "success")
    assert isinstance(result.success, bool)
    assert hasattr(result, "content_blocks")
    assert isinstance(result.content_blocks, tuple)
    assert hasattr(result, "errors")
    assert isinstance(result.errors, tuple)
    assert hasattr(result, "warnings")
    assert isinstance(result.warnings, tuple)
    assert hasattr(result, "document_metadata")
    assert result.document_metadata is not None

    # Verify metadata fields
    metadata = result.document_metadata
    assert metadata.source_file == simple_txt_file
    assert metadata.file_format == "text"
    assert metadata.file_size_bytes > 0
    assert metadata.word_count > 0
    assert metadata.character_count > 0


@pytest.mark.unit
@pytest.mark.extraction
def test_310_error_handling_returns_extraction_result(extractor, tmp_path):
    """
    Test that errors return proper ExtractionResult structure.

    Failed extractions should still return ExtractionResult, not raise.
    """
    # Arrange
    missing_file = tmp_path / "missing.txt"

    # Act
    result = extractor.extract(missing_file)

    # Assert
    assert result is not None
    assert hasattr(result, "success")
    assert result.success is False
    assert len(result.errors) > 0

    # Metadata should still be populated
    assert hasattr(result, "document_metadata")
    metadata = result.document_metadata
    assert metadata is not None
    assert metadata.source_file == missing_file
    assert metadata.file_format == "text"


# ============================================================================
# Additional Coverage Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.extraction
def test_401_raw_content_matches_content(extractor, simple_txt_file):
    """
    Test that raw_content matches content for plain text.

    For text files, raw and processed content should be identical.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True

    for block in result.content_blocks:
        assert block.raw_content == block.content


@pytest.mark.unit
@pytest.mark.extraction
def test_402_paragraph_ending_with_period(extractor, tmp_path):
    """
    Test that paragraphs ending with period are not detected as headings.

    Punctuation should indicate paragraph, not heading.
    """
    # Arrange
    file_path = tmp_path / "with_period.txt"
    content = "This is a short line ending with a period."
    file_path.write_text(content, encoding="utf-8")

    # Act
    result = extractor.extract(file_path)

    # Assert
    assert result.success is True
    assert len(result.content_blocks) == 1

    block = result.content_blocks[0]
    assert block.block_type == ContentType.PARAGRAPH


@pytest.mark.unit
@pytest.mark.extraction
def test_403_case_insensitive_extension_support(extractor, tmp_path):
    """
    Test case-insensitive extension matching.

    .TXT, .Txt, .txt should all be supported.
    """
    # Test uppercase
    file1 = tmp_path / "test.TXT"
    file1.touch()
    assert extractor.supports_format(file1) is True

    # Test mixed case
    file2 = tmp_path / "test.Txt"
    file2.touch()
    assert extractor.supports_format(file2) is True

    # Test lowercase
    file3 = tmp_path / "test.txt"
    file3.touch()
    assert extractor.supports_format(file3) is True


@pytest.mark.unit
@pytest.mark.extraction
def test_404_document_metadata_word_count_accuracy(extractor, simple_txt_file):
    """
    Test that document-level word count is accurate.

    Should count all words across all paragraphs.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True

    # Calculate expected word count
    file_content = simple_txt_file.read_text(encoding="utf-8")
    expected_words = len(file_content.split())

    assert result.document_metadata.word_count == expected_words


@pytest.mark.unit
@pytest.mark.extraction
def test_405_document_metadata_character_count_accuracy(extractor, simple_txt_file):
    """
    Test that document-level character count is accurate.
    """
    # Act
    result = extractor.extract(simple_txt_file)

    # Assert
    assert result.success is True

    # Calculate expected character count
    file_content = simple_txt_file.read_text(encoding="utf-8")
    expected_chars = len(file_content)

    assert result.document_metadata.character_count == expected_chars


@pytest.mark.unit
@pytest.mark.extraction
def test_406_tabs_preserved_in_content(extractor, special_chars_file):
    """
    Test that tab characters are preserved in content.
    """
    # Act
    result = extractor.extract(special_chars_file)

    # Assert
    assert result.success is True

    # Find block with tabs
    all_content = " ".join(block.content for block in result.content_blocks)
    assert "\t" in all_content


@pytest.mark.unit
@pytest.mark.extraction
def test_407_unexpected_exception_handling(extractor, tmp_path, monkeypatch):
    """
    Test that unexpected exceptions are caught and returned as errors.

    Validates the general exception handler at end of extract method.
    """
    # Arrange - Create a valid file
    file_path = tmp_path / "test.txt"
    file_path.write_text("Test content", encoding="utf-8")

    # Mock read_text to raise unexpected exception
    def mock_read_text(*args, **kwargs):
        raise RuntimeError("Unexpected error during read")

    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # Act
    result = extractor.extract(file_path)

    # Assert
    assert result.success is False
    assert len(result.errors) > 0

    # Error should mention the unexpected error
    error_text = " ".join(result.errors).lower()
    assert "unexpected error" in error_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
