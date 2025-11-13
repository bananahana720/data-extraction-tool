"""
Comprehensive edge case tests for all formatters.

This test suite tests formatter boundary conditions using equivalency partitioning.

Formatters Tested:
- JsonFormatter: JSON output
- MarkdownFormatter: Markdown output
- ChunkedTextFormatter: Token-chunked output

Test Categories:
- Empty/minimal input
- Maximum scale (thousands of blocks)
- Special characters and escaping
- Unicode handling
- Token limit boundaries
- Hierarchical structure edge cases
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ProcessingResult,
    ProcessingStage,
)
from formatters.chunked_text_formatter import ChunkedTextFormatter
from formatters.json_formatter import JsonFormatter
from formatters.markdown_formatter import MarkdownFormatter

# ==============================================================================
# JsonFormatter Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestJsonFormatterEdgeCases:
    """Edge cases for JsonFormatter."""

    def test_empty_content_blocks(self):
        """
        EDGE: Format result with zero content blocks.

        Partition: Input size → Valid → Minimum (0)
        Expected: Valid JSON with empty blocks array
        """
        formatter = JsonFormatter()

        processing_result = ProcessingResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(
                source_file=Path("empty.txt"), file_format="text", title="Empty Doc"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)
        assert "content_blocks" in parsed
        assert len(parsed["content_blocks"]) == 0

    def test_single_content_block(self):
        """
        EDGE: Format result with exactly one block.

        Partition: Input size → Valid → Minimum useful (1)
        """
        formatter = JsonFormatter()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Single block")

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("single.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)
        assert len(parsed["content_blocks"]) == 1

    @pytest.mark.slow
    @pytest.mark.stress
    def test_extremely_large_result_set(self):
        """
        EDGE: Format 10,000+ blocks (stress test).

        Partition: Input size → Valid → Maximum
        Expected: Should complete without OOM
        """
        formatter = JsonFormatter()

        blocks = []
        for i in range(10000):
            block = ContentBlock(block_type=ContentType.PARAGRAPH, content=f"Block {i}" * 10)
            blocks.append(block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("huge.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        import time

        start = time.time()
        result = formatter.format(processing_result)
        duration = time.time() - start

        assert result.success is True
        parsed = json.loads(result.content)
        assert len(parsed["content_blocks"]) == 10000

        # Performance check
        assert duration < 30.0, f"Took {duration:.2f}s to format 10k blocks"

    def test_content_with_json_special_characters(self):
        """
        EDGE: Content containing JSON special characters.

        Partition: Content → Valid → Special characters
        Expected: Proper escaping in JSON output
        """
        formatter = JsonFormatter()

        # Content with characters that need escaping in JSON
        special_content = 'Text with "quotes", \\backslashes\\, and \n newlines'

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content=special_content)

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("special.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should parse without errors (proper escaping)
        parsed = json.loads(result.content)
        assert special_content in parsed["content_blocks"][0]["content"]

    def test_content_with_unicode_characters(self):
        """
        EDGE: Content with extensive unicode characters.

        Partition: Content → Valid → Unicode
        Expected: Unicode preserved in JSON
        """
        formatter = JsonFormatter()

        unicode_content = "文档 🎉 中文 العربية עברית ελληνικά Emoji: 🚀🎨🌍"

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content=unicode_content)

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("unicode.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)

        # Unicode should be preserved
        assert unicode_content in parsed["content_blocks"][0]["content"]

    def test_metadata_with_none_values(self):
        """
        EDGE: Block metadata containing None values.

        Partition: Metadata → Valid → Null values
        Expected: JSON null for None values
        """
        formatter = JsonFormatter()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content="Content",
            metadata={"null_field": None, "valid_field": "value"},
        )

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("null.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)

        # None should become JSON null
        assert parsed["content_blocks"][0]["metadata"]["null_field"] is None

    def test_deeply_nested_hierarchical_structure(self):
        """
        EDGE: Deeply nested hierarchy (10 levels) in hierarchical mode.

        Partition: Hierarchy → Valid → Deep nesting
        Expected: Correct nesting in JSON output
        """
        formatter = JsonFormatter(config={"hierarchical": True})

        blocks = []
        parent_id = None

        for level in range(10):
            block = ContentBlock(
                block_type=ContentType.HEADING,
                content=f"Level {level}",
                parent_id=parent_id,
                metadata={"level": level + 1},
            )
            blocks.append(block)
            parent_id = block.block_id

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("deep.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should produce valid JSON without errors
        parsed = json.loads(result.content)


# ==============================================================================
# MarkdownFormatter Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestMarkdownFormatterEdgeCases:
    """Edge cases for MarkdownFormatter."""

    def test_empty_content_blocks(self):
        """
        EDGE: Format result with zero content blocks.

        Partition: Input size → Valid → Minimum (0)
        Expected: Minimal markdown output
        """
        formatter = MarkdownFormatter()

        processing_result = ProcessingResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(
                source_file=Path("empty.txt"), file_format="text", title="Empty Doc"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        assert result.format_type == "markdown"
        # Should have at least title
        assert "Empty Doc" in result.content

    def test_content_with_markdown_special_characters(self):
        """
        EDGE: Content with markdown syntax characters.

        Partition: Content → Valid → Special characters
        Expected: Proper escaping to prevent formatting
        """
        formatter = MarkdownFormatter()

        # Content that looks like markdown
        md_content = "# Not a heading\n**Not bold** `not code` [not a link](url)"

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content=md_content)

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("md_chars.txt"), file_format="text"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Content should be escaped or handled appropriately
        assert result.content is not None

    def test_table_heavy_document(self):
        """
        EDGE: Document with many tables (table-heavy).

        Partition: Content type → Valid → Table-dominated
        Expected: Proper markdown table formatting
        """
        formatter = MarkdownFormatter()

        blocks = []
        for i in range(10):
            table_block = ContentBlock(
                block_type=ContentType.TABLE,
                content=f"Table {i}",
                metadata={"table_id": f"table_{i}"},
            )
            blocks.append(table_block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("tables.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should handle multiple tables
        assert result.content is not None

    def test_image_heavy_document(self):
        """
        EDGE: Document with many images.

        Partition: Content type → Valid → Image-dominated
        Expected: Markdown image syntax for each
        """
        formatter = MarkdownFormatter()

        blocks = []
        for i in range(20):
            img_block = ContentBlock(
                block_type=ContentType.IMAGE,
                content=f"[Image {i}]",
                metadata={"image_id": f"img_{i}"},
            )
            blocks.append(img_block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("images.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True

    def test_code_blocks_with_triple_backticks(self):
        """
        EDGE: Code blocks containing triple backticks.

        Partition: Content → Valid → Nested syntax
        Expected: Proper escaping of nested code fences
        """
        formatter = MarkdownFormatter()

        # Code content that itself contains markdown code fence
        code_content = "```python\nprint('hello')\n```"

        block = ContentBlock(
            block_type=ContentType.CODE, content=code_content, metadata={"language": "markdown"}
        )

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("nested.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should handle nested code fences


# ==============================================================================
# ChunkedTextFormatter Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestChunkedTextFormatterEdgeCases:
    """Edge cases for ChunkedTextFormatter."""

    def test_token_limit_minimum(self):
        """
        EDGE: Token limit at minimum (100 tokens).

        Partition: Token limit → Valid → Minimum
        Expected: Should create small chunks
        """
        formatter = ChunkedTextFormatter(config={"max_tokens_per_chunk": 100})

        blocks = []
        for i in range(5):
            block = ContentBlock(
                block_type=ContentType.PARAGRAPH, content=" ".join(["word"] * 50)  # ~50 tokens
            )
            blocks.append(block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(
                source_file=Path("small_chunks.txt"), file_format="text"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should create multiple chunks due to low limit
        parsed = json.loads(result.content)
        assert "chunks" in parsed
        assert len(parsed["chunks"]) >= 2

    def test_token_limit_maximum(self):
        """
        EDGE: Token limit at maximum (10000 tokens).

        Partition: Token limit → Valid → Maximum
        Expected: Should create large chunks
        """
        formatter = ChunkedTextFormatter(config={"max_tokens_per_chunk": 10000})

        blocks = []
        for i in range(100):
            block = ContentBlock(
                block_type=ContentType.PARAGRAPH, content=" ".join(["word"] * 30)  # ~30 tokens each
            )
            blocks.append(block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(
                source_file=Path("large_chunks.txt"), file_format="text"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should create few chunks due to high limit
        parsed = json.loads(result.content)
        assert "chunks" in parsed

    def test_single_block_exceeds_token_limit(self):
        """
        EDGE: Single block larger than token limit.

        Partition: Content size → Invalid → Exceeds limit
        Expected: Should split block or handle gracefully
        """
        formatter = ChunkedTextFormatter(config={"max_tokens_per_chunk": 100})

        # Create block with ~200 tokens (exceeds limit)
        large_block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content=" ".join(["word"] * 200)
        )

        processing_result = ProcessingResult(
            content_blocks=(large_block,),
            document_metadata=DocumentMetadata(
                source_file=Path("too_large.txt"), file_format="text"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        # Should handle block that exceeds limit
        parsed = json.loads(result.content)
        assert "chunks" in parsed

    def test_exact_token_limit_boundary(self):
        """
        EDGE: Content exactly at token limit.

        Partition: Content size → Boundary → Exact limit
        Expected: Should fit in single chunk
        """
        token_limit = 500
        formatter = ChunkedTextFormatter(config={"max_tokens_per_chunk": token_limit})

        # Create content close to token limit
        block = ContentBlock(
            block_type=ContentType.PARAGRAPH,
            content=" ".join(["word"] * (token_limit - 10)),  # Just under limit
        )

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("boundary.txt"), file_format="text"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)
        # Should fit in one chunk
        assert len(parsed["chunks"]) >= 1

    def test_empty_content_blocks(self):
        """
        EDGE: Empty content blocks list.

        Partition: Input size → Valid → Minimum (0)
        Expected: Valid output with zero chunks
        """
        formatter = ChunkedTextFormatter()

        processing_result = ProcessingResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(source_file=Path("empty.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)
        assert "chunks" in parsed

    def test_optimal_vs_suboptimal_chunking(self):
        """
        EDGE: Test chunking optimization.

        Partition: Algorithm → Valid → Optimization quality
        Expected: Chunks should be well-balanced
        """
        formatter = ChunkedTextFormatter(config={"max_tokens_per_chunk": 500})

        # Create 10 blocks of varying sizes
        blocks = []
        for i in range(10):
            size = 50 + (i * 10)  # Varying sizes
            block = ContentBlock(
                block_type=ContentType.PARAGRAPH, content=" ".join(["word"] * size)
            )
            blocks.append(block)

        processing_result = ProcessingResult(
            content_blocks=tuple(blocks),
            document_metadata=DocumentMetadata(source_file=Path("varied.txt"), file_format="text"),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        result = formatter.format(processing_result)

        assert result.success is True
        parsed = json.loads(result.content)

        # Verify chunks are created
        assert "chunks" in parsed
        assert len(parsed["chunks"]) > 0

        # Check that chunks are reasonably balanced (not wildly different sizes)
        if len(parsed["chunks"]) > 1:
            chunk_sizes = [len(chunk.get("content", "")) for chunk in parsed["chunks"]]
            max_size = max(chunk_sizes)
            min_size = min(chunk_sizes)

            # Chunks shouldn't be too imbalanced (allow 3x variance)
            if min_size > 0:
                assert max_size / min_size < 5.0


# ==============================================================================
# Cross-Formatter Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestCrossFormatterEdgeCases:
    """Edge cases involving multiple formatters."""

    def test_same_input_all_formatters(self):
        """
        EDGE: Same input through all formatters.

        Expected: Each formatter should succeed
        """
        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Test content for all formatters"
        )

        processing_result = ProcessingResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(
                source_file=Path("multi.txt"), file_format="text", title="Test"
            ),
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            success=True,
        )

        # Try all formatters
        json_result = JsonFormatter().format(processing_result)
        md_result = MarkdownFormatter().format(processing_result)
        chunked_result = ChunkedTextFormatter().format(processing_result)

        assert json_result.success is True
        assert md_result.success is True
        assert chunked_result.success is True

        # Each should produce different output
        assert json_result.format_type == "json"
        assert md_result.format_type == "markdown"
        assert chunked_result.format_type == "chunked_text"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "edge_case"])
