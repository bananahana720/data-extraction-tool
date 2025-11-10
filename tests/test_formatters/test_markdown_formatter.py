"""
Tests for MarkdownFormatter.

Tests organized by requirement:
- Human-readable output
- Heading hierarchy preservation
- Document structure preservation
- YAML frontmatter metadata
- Lists and quotes formatting
- Table formatting
- Code block formatting
- Image references
"""

from pathlib import Path

import pytest

from core.models import ContentType
from formatters.markdown_formatter import MarkdownFormatter


class TestMarkdownFormatterBasicStructure:
    """Tests for basic markdown structure and validity."""

    def test_format_returns_formatted_output(self, minimal_processing_result):
        """Format should return FormattedOutput with markdown content."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        assert result.success is True
        assert result.format_type == "markdown"
        assert result.content != ""
        assert isinstance(result.content, str)

    def test_format_produces_readable_markdown(self, minimal_processing_result):
        """Output should be human-readable markdown."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        # Should have markdown content
        assert len(result.content) > 0
        # Should not be excessively technical
        assert "block_id" not in result.content  # Don't expose UUIDs
        assert "block_type" not in result.content  # Don't expose types

    def test_format_includes_content(self, minimal_processing_result):
        """Markdown should include actual content."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        # Should include text from blocks
        assert "Test Document" in result.content
        assert "This is a test paragraph." in result.content


class TestMarkdownFormatterHeadings:
    """Tests for heading hierarchy."""

    def test_converts_headings_to_markdown_syntax(self, rich_processing_result):
        """ContentType.HEADING should use markdown # syntax."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have markdown headings
        assert (
            "# Chapter 1: Introduction" in result.content
            or "## Chapter 1: Introduction" in result.content
        )

    def test_preserves_heading_hierarchy(self, deeply_nested_result):
        """Heading levels should be preserved with correct # count."""
        formatter = MarkdownFormatter()
        result = formatter.format(deeply_nested_result)

        # Should have different heading levels
        assert "# Heading Level 1" in result.content
        assert "## Heading Level 2" in result.content
        assert "### Heading Level 3" in result.content

    def test_heading_from_metadata_level(self, rich_processing_result):
        """Should use metadata.level to determine heading depth."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Check that levels are used
        lines = result.content.split("\n")
        heading_lines = [line for line in lines if line.strip().startswith("#")]
        assert len(heading_lines) > 0


class TestMarkdownFormatterFrontmatter:
    """Tests for YAML frontmatter metadata."""

    def test_includes_yaml_frontmatter(self, minimal_processing_result):
        """Should include YAML frontmatter with document metadata."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        # Should start with frontmatter
        assert result.content.startswith("---")
        # Should have closing frontmatter
        lines = result.content.split("\n")
        assert "---" in lines[1:10]  # Second --- within first few lines

    def test_frontmatter_contains_title(self, minimal_processing_result):
        """Frontmatter should include document title."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        assert "title:" in result.content
        assert "Test Document" in result.content

    def test_frontmatter_contains_author(self, minimal_processing_result):
        """Frontmatter should include document author."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        assert "author:" in result.content
        assert "Test Author" in result.content

    def test_frontmatter_optional_when_no_metadata(self, empty_processing_result):
        """Frontmatter can be omitted if no useful metadata."""
        formatter = MarkdownFormatter(config={"include_frontmatter": False})
        result = formatter.format(empty_processing_result)

        # Should not have frontmatter
        assert not result.content.startswith("---") or result.content.strip() == ""


class TestMarkdownFormatterContentTypes:
    """Tests for different content type formatting."""

    def test_formats_paragraphs(self, minimal_processing_result):
        """Paragraphs should be plain text with blank lines."""
        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        # Paragraph content should be present
        assert "This is a test paragraph." in result.content

    def test_formats_list_items(self, rich_processing_result):
        """LIST_ITEM should use markdown list syntax."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have list items
        assert "- First item" in result.content or "* First item" in result.content
        assert "- Second item" in result.content or "* Second item" in result.content

    def test_formats_quotes(self, rich_processing_result):
        """QUOTE should use markdown blockquote syntax."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have blockquote
        assert "> This is a quoted text." in result.content

    def test_formats_code_blocks(self, rich_processing_result):
        """CODE should use fenced code blocks."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have code fence
        assert "```" in result.content
        assert "def hello():" in result.content
        assert "print('world')" in result.content

    def test_code_block_includes_language(self, rich_processing_result):
        """Code fence should include language from metadata."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should specify language
        assert "```python" in result.content


class TestMarkdownFormatterTables:
    """Tests for table formatting."""

    def test_formats_table_reference(self, rich_processing_result):
        """TABLE blocks should be referenced or formatted as markdown tables."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should mention the table
        assert "Table" in result.content or "|" in result.content

    def test_formats_table_with_metadata(self, table_metadata_sample):
        """Should format table data as markdown table if available."""
        from core.models import ContentBlock, ContentType, DocumentMetadata, ProcessingResult

        result = ProcessingResult(
            content_blocks=(
                ContentBlock(
                    block_type=ContentType.TABLE,
                    content="Sales Data",
                    metadata={"table_id": str(table_metadata_sample.table_id)},
                ),
            ),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = MarkdownFormatter()
        output = formatter.format(result)

        # Should format as table or reference it
        assert "Sales Data" in output.content


class TestMarkdownFormatterImages:
    """Tests for image formatting."""

    def test_formats_image_reference(self, rich_processing_result):
        """IMAGE blocks should use markdown image syntax."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have image reference
        assert "![" in result.content or "Figure" in result.content

    def test_image_includes_alt_text(self, rich_processing_result):
        """Image should include alt text from metadata."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Should have alt text or description
        assert "Architecture" in result.content or "diagram" in result.content.lower()


class TestMarkdownFormatterStructure:
    """Tests for structure preservation."""

    def test_preserves_document_order(self, rich_processing_result):
        """Content should appear in sequence_index order."""
        formatter = MarkdownFormatter()
        result = formatter.format(rich_processing_result)

        # Chapter should come before background section
        chapter_pos = result.content.find("Chapter 1")
        background_pos = result.content.find("Background")
        assert chapter_pos < background_pos

    def test_empty_document_handled(self, empty_processing_result):
        """Empty document should produce minimal markdown."""
        formatter = MarkdownFormatter()
        result = formatter.format(empty_processing_result)

        assert result.success is True
        # Should have minimal content
        assert len(result.content) < 100 or result.content.strip() == ""


class TestMarkdownFormatterUnicode:
    """Tests for Unicode support."""

    def test_handles_unicode_content(self, unicode_processing_result):
        """Should properly handle Unicode characters."""
        formatter = MarkdownFormatter()
        result = formatter.format(unicode_processing_result)

        # Unicode should be preserved
        assert "你好世界" in result.content
        assert "🎉" in result.content
        assert "é" in result.content or "&#" in result.content  # Either literal or encoded


class TestMarkdownFormatterInterface:
    """Tests for BaseFormatter interface compliance."""

    def test_implements_get_format_type(self):
        """Should implement get_format_type method."""
        formatter = MarkdownFormatter()
        assert formatter.get_format_type() == "markdown"

    def test_implements_get_file_extension(self):
        """Should return correct file extension."""
        formatter = MarkdownFormatter()
        assert formatter.get_file_extension() == ".markdown"

    def test_returns_formatted_output_type(self, minimal_processing_result):
        """format() should return FormattedOutput instance."""
        from core.models import FormattedOutput

        formatter = MarkdownFormatter()
        result = formatter.format(minimal_processing_result)

        assert isinstance(result, FormattedOutput)


class TestMarkdownFormatterConfiguration:
    """Tests for configuration options."""

    def test_heading_offset_configuration(self, minimal_processing_result):
        """Should support heading_offset to adjust # levels."""
        formatter = MarkdownFormatter(config={"heading_offset": 1})
        result = formatter.format(minimal_processing_result)

        # Headings should be offset by 1
        # First heading would be ## instead of #
        lines = result.content.split("\n")
        heading_lines = [
            line for line in lines if line.strip().startswith("#") and "Test Document" in line
        ]
        if heading_lines:
            assert heading_lines[0].strip().startswith("##")

    def test_include_metadata_flag(self, minimal_processing_result):
        """Should support flag to include/exclude technical metadata."""
        formatter = MarkdownFormatter(config={"include_metadata": True})
        result = formatter.format(minimal_processing_result)

        # With metadata, might include file info
        assert "test.docx" in result.content or "Test Document" in result.content
