"""
Tests for JsonFormatter.

Tests organized by requirement:
- Hierarchical JSON structure
- Metadata inclusion
- Pretty-print configuration
- Schema validity
- Content type preservation
- Position information
- Error handling
- Unicode support
"""

import json
from pathlib import Path

from core.models import ContentType, ProcessingResult
from formatters.json_formatter import JsonFormatter


class TestJsonFormatterBasicStructure:
    """Tests for basic JSON structure and validity."""

    def test_format_returns_formatted_output(self, minimal_processing_result):
        """Format should return FormattedOutput with JSON content."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        assert result.success is True
        assert result.format_type == "json"
        assert result.content != ""
        assert isinstance(result.content, str)

    def test_format_produces_valid_json(self, minimal_processing_result):
        """Output should be valid, parseable JSON."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        # Should parse without errors
        parsed = json.loads(result.content)
        assert isinstance(parsed, dict)

    def test_format_includes_content_blocks(self, minimal_processing_result):
        """JSON should include all content blocks."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        parsed = json.loads(result.content)
        assert "content_blocks" in parsed
        assert len(parsed["content_blocks"]) == 2  # heading + paragraph

    def test_format_includes_document_metadata(self, minimal_processing_result):
        """JSON should include document metadata."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        parsed = json.loads(result.content)
        assert "document_metadata" in parsed
        assert parsed["document_metadata"]["title"] == "Test Document"
        assert parsed["document_metadata"]["author"] == "Test Author"


class TestJsonFormatterHierarchy:
    """Tests for hierarchical structure in JSON output."""

    def test_hierarchical_structure_with_parent_child(self, rich_processing_result):
        """Blocks with parent_id should be nested under parent."""
        formatter = JsonFormatter(config={"hierarchical": True})
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)

        # Should have hierarchical structure
        assert "content_blocks" in parsed
        # Root level should have main heading
        root_blocks = [b for b in parsed["content_blocks"] if b.get("parent_id") is None]
        assert len(root_blocks) > 0

    def test_flat_structure_when_not_hierarchical(self, rich_processing_result):
        """When hierarchical=False, all blocks should be in flat list."""
        formatter = JsonFormatter(config={"hierarchical": False})
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)
        assert "content_blocks" in parsed
        assert isinstance(parsed["content_blocks"], list)
        # All blocks in flat list
        assert len(parsed["content_blocks"]) == len(rich_processing_result.content_blocks)


class TestJsonFormatterMetadata:
    """Tests for metadata inclusion."""

    def test_includes_block_metadata(self, rich_processing_result):
        """Block-level metadata should be preserved."""
        formatter = JsonFormatter()
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)
        blocks = parsed["content_blocks"]

        # Find code block
        code_blocks = [b for b in blocks if b["block_type"] == "code"]
        assert len(code_blocks) > 0
        code_block = code_blocks[0]
        assert "metadata" in code_block
        assert code_block["metadata"]["language"] == "python"

    def test_includes_position_information(self, rich_processing_result):
        """Position data should be included for each block."""
        formatter = JsonFormatter()
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)
        blocks = parsed["content_blocks"]

        # Check first block has position
        assert "position" in blocks[0]
        position = blocks[0]["position"]
        assert "page" in position or "sequence_index" in position

    def test_includes_style_information(self):
        """Style information in blocks should be preserved."""
        # This will be tested with blocks that have style data
        pass  # Implementation will add style to blocks


class TestJsonFormatterConfiguration:
    """Tests for configuration options."""

    def test_pretty_print_enabled(self, minimal_processing_result):
        """With pretty_print=True, JSON should be indented."""
        formatter = JsonFormatter(config={"pretty_print": True})
        result = formatter.format(minimal_processing_result)

        # Pretty-printed JSON has newlines and indentation
        assert "\n" in result.content
        assert "  " in result.content or "\t" in result.content

    def test_pretty_print_disabled(self, minimal_processing_result):
        """With pretty_print=False, JSON should be compact."""
        formatter = JsonFormatter(config={"pretty_print": False})
        result = formatter.format(minimal_processing_result)

        # Compact JSON has minimal whitespace
        # Note: may have some whitespace after separators
        lines = result.content.split("\n")
        # Should be mostly on one line (or very few lines)
        assert len(lines) < 5

    def test_indent_configuration(self, minimal_processing_result):
        """Indent size should be configurable."""
        formatter = JsonFormatter(config={"pretty_print": True, "indent": 4})
        result = formatter.format(minimal_processing_result)

        # Should have 4-space indentation
        assert "    " in result.content


class TestJsonFormatterContentTypes:
    """Tests for content type preservation."""

    def test_preserves_all_content_types(self, rich_processing_result):
        """All ContentType enum values should be correctly serialized."""
        formatter = JsonFormatter()
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)
        blocks = parsed["content_blocks"]

        # Extract all block types
        block_types = {b["block_type"] for b in blocks}

        # Should have various types
        assert "heading" in block_types
        assert "paragraph" in block_types
        assert "list_item" in block_types
        assert "code" in block_types

    def test_content_type_as_string(self, minimal_processing_result):
        """ContentType should be serialized as string, not enum object."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        parsed = json.loads(result.content)
        blocks = parsed["content_blocks"]

        # Should be string
        assert isinstance(blocks[0]["block_type"], str)


class TestJsonFormatterErrorHandling:
    """Tests for error handling and edge cases."""

    def test_handles_empty_input(self, empty_processing_result):
        """Should handle ProcessingResult with no blocks."""
        formatter = JsonFormatter()
        result = formatter.format(empty_processing_result)

        assert result.success is True
        parsed = json.loads(result.content)
        assert parsed["content_blocks"] == []

    def test_handles_failed_processing_result(self, failed_processing_result):
        """Should handle ProcessingResult with success=False."""
        formatter = JsonFormatter()
        result = formatter.format(failed_processing_result)

        # Formatter should still succeed, but include error info
        assert result.success is True
        parsed = json.loads(result.content)
        assert "errors" in parsed or "processing_errors" in parsed


class TestJsonFormatterUnicode:
    """Tests for Unicode support."""

    def test_handles_unicode_content(self, unicode_processing_result):
        """Should properly handle Unicode characters."""
        formatter = JsonFormatter()
        result = formatter.format(unicode_processing_result)

        parsed = json.loads(result.content)
        blocks = parsed["content_blocks"]

        # Find block with unicode
        assert any("你好世界" in b["content"] for b in blocks)
        assert any("🎉" in b["content"] for b in blocks)

    def test_unicode_properly_encoded(self, unicode_processing_result):
        """Unicode should be properly encoded in JSON."""
        formatter = JsonFormatter()
        result = formatter.format(unicode_processing_result)

        # Should be valid UTF-8
        assert isinstance(result.content, str)
        # Re-encoding should work
        result.content.encode("utf-8")


class TestJsonFormatterInterface:
    """Tests for BaseFormatter interface compliance."""

    def test_implements_get_format_type(self):
        """Should implement get_format_type method."""
        formatter = JsonFormatter()
        assert formatter.get_format_type() == "json"

    def test_implements_get_file_extension(self):
        """Should return correct file extension."""
        formatter = JsonFormatter()
        assert formatter.get_file_extension() == ".json"

    def test_returns_formatted_output_type(self, minimal_processing_result):
        """format() should return FormattedOutput instance."""
        from core.models import FormattedOutput

        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        assert isinstance(result, FormattedOutput)


class TestJsonFormatterSchema:
    """Tests for JSON schema structure."""

    def test_output_has_expected_top_level_keys(self, rich_processing_result):
        """Top-level JSON should have expected structure."""
        formatter = JsonFormatter()
        result = formatter.format(rich_processing_result)

        parsed = json.loads(result.content)

        # Expected top-level keys
        assert "content_blocks" in parsed
        assert "document_metadata" in parsed

    def test_block_has_required_fields(self, minimal_processing_result):
        """Each block should have required fields."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_processing_result)

        parsed = json.loads(result.content)
        block = parsed["content_blocks"][0]

        # Required fields
        assert "block_id" in block
        assert "block_type" in block
        assert "content" in block


class TestJsonFormatterEdgeCases:
    """Tests for edge cases and full metadata coverage."""

    def test_serializes_all_optional_position_fields(self):
        """Should handle Position with all fields populated."""
        from core.models import (
            ContentBlock,
            DocumentMetadata,
            Position,
        )

        result = ProcessingResult(
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content="Test",
                    position=Position(
                        page=1,
                        slide=2,
                        sheet="Sheet1",
                        x=10.5,
                        y=20.3,
                        width=100.0,
                        height=50.0,
                        sequence_index=5,
                    ),
                ),
            ),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = JsonFormatter()
        output = formatter.format(result)
        parsed = json.loads(output.content)

        pos = parsed["content_blocks"][0]["position"]
        assert pos["page"] == 1
        assert pos["slide"] == 2
        assert pos["sheet"] == "Sheet1"
        assert pos["x"] == 10.5
        assert pos["y"] == 20.3
        assert pos["width"] == 100.0
        assert pos["height"] == 50.0
        assert pos["sequence_index"] == 5

    def test_serializes_all_optional_metadata_fields(self):
        """Should handle DocumentMetadata with all fields populated."""
        from datetime import datetime

        from core.models import DocumentMetadata

        result = ProcessingResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
                file_size_bytes=1024,
                file_hash="abc123",
                title="Test Title",
                author="Test Author",
                created_date=datetime(2025, 1, 1, 10, 30),
                modified_date=datetime(2025, 1, 2, 15, 45),
                subject="Test Subject",
                keywords=("keyword1", "keyword2"),
                page_count=10,
                word_count=500,
                character_count=2500,
                image_count=3,
                table_count=2,
                language="en",
                content_summary="Test summary",
                extractor_version="1.0.0",
                extraction_duration_seconds=2.5,
            ),
            success=True,
        )

        formatter = JsonFormatter()
        output = formatter.format(result)
        parsed = json.loads(output.content)

        meta = parsed["document_metadata"]
        assert meta["file_hash"] == "abc123"
        assert meta["title"] == "Test Title"
        assert meta["author"] == "Test Author"
        assert "created_date" in meta
        assert "modified_date" in meta
        assert meta["subject"] == "Test Subject"
        assert meta["keywords"] == ["keyword1", "keyword2"]
        assert meta["page_count"] == 10
        assert meta["word_count"] == 500
        assert meta["character_count"] == 2500
        assert meta["image_count"] == 3
        assert meta["table_count"] == 2
        assert meta["language"] == "en"
        assert meta["content_summary"] == "Test summary"
        assert meta["extractor_version"] == "1.0.0"
        assert meta["extraction_duration_seconds"] == 2.5

    def test_serializes_content_block_optional_fields(self):
        """Should handle ContentBlock with all optional fields."""
        from uuid import uuid4

        from core.models import ContentBlock, DocumentMetadata

        block_id = uuid4()
        related_id = uuid4()

        result = ProcessingResult(
            content_blocks=(
                ContentBlock(
                    block_id=block_id,
                    block_type=ContentType.PARAGRAPH,
                    content="Test content",
                    raw_content="Raw test content",
                    related_ids=(related_id,),
                    confidence=0.95,
                    style={"font": "Arial", "size": 12},
                ),
            ),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = JsonFormatter()
        output = formatter.format(result)
        parsed = json.loads(output.content)

        block = parsed["content_blocks"][0]
        assert block["raw_content"] == "Raw test content"
        assert block["related_ids"] == [str(related_id)]
        assert block["confidence"] == 0.95
        assert block["style"]["font"] == "Arial"
        assert block["style"]["size"] == 12

    def test_error_handling_during_serialization(self):
        """Should handle serialization errors gracefully."""
        from core.models import DocumentMetadata

        # Create a result that might cause issues
        result = ProcessingResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = JsonFormatter()
        # Should not raise, even with potential issues
        output = formatter.format(result)
        assert output.success is True
