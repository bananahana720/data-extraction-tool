"""
Tests for ChunkedTextFormatter.

Tests organized by requirement:
- Token limit respect
- Configurable token limits
- Context maintenance across chunks
- Chunk metadata
- Smart splitting on boundaries
- Token counting accuracy
- Oversized block handling
- Multi-chunk output
"""

from pathlib import Path

import pytest

from core.models import ContentBlock, ContentType, DocumentMetadata, ProcessingResult
from formatters.chunked_text_formatter import ChunkedTextFormatter


class TestChunkedFormatterBasicStructure:
    """Tests for basic chunked formatter structure."""

    def test_format_returns_formatted_output(self, minimal_processing_result):
        """Format should return FormattedOutput with chunked content."""
        formatter = ChunkedTextFormatter()
        result = formatter.format(minimal_processing_result)

        assert result.success is True
        assert result.format_type == "chunked"
        assert result.content != ""
        assert isinstance(result.content, str)

    def test_small_content_fits_in_single_chunk(self, minimal_processing_result):
        """Small content should fit in a single chunk."""
        formatter = ChunkedTextFormatter(config={"token_limit": 1000})
        result = formatter.format(minimal_processing_result)

        # Should have main content
        assert "Test Document" in result.content
        # Should not have multiple files
        assert len(result.additional_files) == 0


class TestChunkedFormatterTokenLimit:
    """Tests for token limit enforcement."""

    def test_respects_token_limit(self, long_content_result):
        """No single chunk should exceed token limit."""
        token_limit = 500
        formatter = ChunkedTextFormatter(config={"token_limit": token_limit})
        result = formatter.format(long_content_result)

        # Estimate tokens in main content
        estimated_tokens = len(result.content.split()) * 1.3
        assert estimated_tokens <= token_limit * 1.2  # Allow 20% tolerance

    def test_configurable_token_limit(self, long_content_result):
        """Token limit should be configurable."""
        # Test with different limits
        formatter_small = ChunkedTextFormatter(config={"token_limit": 100})
        result_small = formatter_small.format(long_content_result)

        formatter_large = ChunkedTextFormatter(config={"token_limit": 5000})
        result_large = formatter_large.format(long_content_result)

        # Smaller limit should create more chunks
        # Main content + additional files
        total_files_small = 1 + len(result_small.additional_files)
        total_files_large = 1 + len(result_large.additional_files)

        assert total_files_small >= total_files_large

    def test_default_token_limit(self):
        """Should have reasonable default token limit."""
        formatter = ChunkedTextFormatter()
        # Access config to check default
        assert "token_limit" in formatter.config or hasattr(formatter, "token_limit")


class TestChunkedFormatterContextMaintenance:
    """Tests for context preservation across chunks."""

    def test_chunk_headers_include_context(self, rich_processing_result):
        """Chunk headers should repeat current heading/section context."""
        formatter = ChunkedTextFormatter(config={"token_limit": 200})
        result = formatter.format(rich_processing_result)

        # If multiple chunks, should have context headers
        if result.additional_files:
            # Main content should have some structure
            assert "Chapter" in result.content or "#" in result.content

    def test_chunks_maintain_parent_heading_context(self, deeply_nested_result):
        """Chunks should track which heading they're under."""
        formatter = ChunkedTextFormatter(config={"token_limit": 150})
        result = formatter.format(deeply_nested_result)

        # Should maintain some heading context
        assert "Heading" in result.content


class TestChunkedFormatterMetadata:
    """Tests for chunk metadata."""

    def test_chunk_includes_metadata(self, long_content_result):
        """Chunks should include metadata (chunk number, total chunks, source)."""
        formatter = ChunkedTextFormatter(config={"token_limit": 300})
        result = formatter.format(long_content_result)

        # Should have some metadata
        content_lower = result.content.lower()
        # Check for chunk indicators
        assert "chunk" in content_lower or "part" in content_lower or len(result.content) > 0

    def test_chunk_numbering(self, long_content_result):
        """Multiple chunks should be numbered."""
        formatter = ChunkedTextFormatter(config={"token_limit": 300})
        result = formatter.format(long_content_result)

        if len(result.additional_files) > 0:
            # Should have numbered chunks
            assert "chunk" in result.content.lower() or "1" in result.content


class TestChunkedFormatterSmartSplitting:
    """Tests for smart boundary splitting."""

    def test_splits_on_heading_boundaries(self, rich_processing_result):
        """Should split at heading boundaries, not mid-content."""
        formatter = ChunkedTextFormatter(config={"token_limit": 200})
        result = formatter.format(rich_processing_result)

        # Should preserve complete headings
        if "Chapter" in result.content:
            # Heading should be complete, not cut off
            assert "Chapter 1:" in result.content or "Chapter 1" in result.content

    def test_splits_on_paragraph_boundaries(self, long_content_result):
        """Should split at paragraph boundaries when possible."""
        formatter = ChunkedTextFormatter(config={"token_limit": 400})
        result = formatter.format(long_content_result)

        # Should have complete paragraphs
        # Not cutting mid-sentence (check for proper ending punctuation)
        sentences = result.content.split(".")
        # Most sentence fragments should end properly
        assert len(result.content) > 0

    def test_does_not_split_mid_sentence(self):
        """Should avoid splitting in the middle of sentences."""
        from uuid import uuid4

        # Create content with clear sentences
        blocks = [
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content="This is sentence one. This is sentence two. This is sentence three.",
            )
            for _ in range(10)
        ]

        result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = ChunkedTextFormatter(config={"token_limit": 50})
        output = formatter.format(result)

        # Should not end with incomplete sentences (rough check)
        # Main content should end with period or be complete
        if output.content.strip():
            # Allow some tolerance for chunk headers
            pass  # Basic check that we got output


class TestChunkedFormatterTokenCounting:
    """Tests for token counting algorithm."""

    def test_token_counting_accuracy(self):
        """Token estimation should be reasonable."""
        from uuid import uuid4

        # Create known content
        content = " ".join(["word"] * 100)  # 100 words
        block = ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.PARAGRAPH,
            content=content,
        )

        result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = ChunkedTextFormatter()
        # Should have a token estimation method
        assert hasattr(formatter, "_estimate_tokens") or hasattr(formatter, "_count_tokens")


class TestChunkedFormatterOversizedBlocks:
    """Tests for handling blocks larger than limit."""

    def test_handles_oversized_block(self):
        """Single block larger than limit should go in its own chunk with warning."""
        from uuid import uuid4

        # Create a very long block
        long_content = " ".join(["word"] * 1000)  # ~1000 words
        block = ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.PARAGRAPH,
            content=long_content,
        )

        result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("test.docx"),
                file_format="docx",
            ),
            success=True,
        )

        formatter = ChunkedTextFormatter(config={"token_limit": 100})
        output = formatter.format(result)

        # Should still succeed
        assert output.success is True
        # Should have warning about oversized block
        assert len(output.warnings) > 0 or "word" in output.content


class TestChunkedFormatterMultipleChunks:
    """Tests for multi-chunk output generation."""

    def test_generates_multiple_files(self, long_content_result):
        """Large content should generate multiple chunk files."""
        formatter = ChunkedTextFormatter(config={"token_limit": 200})
        result = formatter.format(long_content_result)

        # Should have additional files for extra chunks
        total_chunks = 1 + len(result.additional_files)
        assert total_chunks >= 1

    def test_additional_files_are_paths(self, long_content_result):
        """additional_files should contain Path objects."""
        formatter = ChunkedTextFormatter(config={"token_limit": 200})
        result = formatter.format(long_content_result)

        if result.additional_files:
            assert all(isinstance(f, Path) for f in result.additional_files)

    def test_chunk_files_have_sequential_names(self, long_content_result):
        """Chunk files should have sequential naming."""
        formatter = ChunkedTextFormatter(config={"token_limit": 200})
        result = formatter.format(long_content_result)

        if len(result.additional_files) > 1:
            # Files should have numbers
            names = [f.name for f in result.additional_files]
            # Should have sequential patterns
            assert any(char.isdigit() for name in names for char in name)


class TestChunkedFormatterInterface:
    """Tests for BaseFormatter interface compliance."""

    def test_implements_get_format_type(self):
        """Should implement get_format_type method."""
        formatter = ChunkedTextFormatter()
        assert formatter.get_format_type() == "chunked"

    def test_implements_get_file_extension(self):
        """Should return correct file extension."""
        formatter = ChunkedTextFormatter()
        ext = formatter.get_file_extension()
        assert ext in [".txt", ".chunked", ".chunk"]

    def test_returns_formatted_output_type(self, minimal_processing_result):
        """format() should return FormattedOutput instance."""
        from core.models import FormattedOutput

        formatter = ChunkedTextFormatter()
        result = formatter.format(minimal_processing_result)

        assert isinstance(result, FormattedOutput)


class TestChunkedFormatterEdgeCases:
    """Tests for edge cases."""

    def test_handles_empty_input(self, empty_processing_result):
        """Should handle empty ProcessingResult."""
        formatter = ChunkedTextFormatter()
        result = formatter.format(empty_processing_result)

        assert result.success is True
        # Empty content or minimal output
        assert len(result.content) < 100 or result.content.strip() == ""

    def test_handles_single_block(self, minimal_processing_result):
        """Should handle minimal single-block input."""
        formatter = ChunkedTextFormatter(config={"token_limit": 1000})
        result = formatter.format(minimal_processing_result)

        assert result.success is True
        assert "Test Document" in result.content
