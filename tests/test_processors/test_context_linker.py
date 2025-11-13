"""
Tests for ContextLinker processor.

ContextLinker builds hierarchical document structure by:
- Detecting heading hierarchy (H1 > H2 > H3)
- Linking paragraphs to their parent headings
- Creating document tree structure
- Preserving relationships in metadata
"""

from pathlib import Path

from processors.context_linker import ContextLinker
from src.core import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ExtractionResult,
    ProcessingStage,
)


class TestContextLinkerBasics:
    """Test basic ContextLinker functionality."""

    def test_processor_name(self):
        """RED: Processor should return correct name."""
        processor = ContextLinker()
        assert processor.get_processor_name() == "ContextLinker"

    def test_is_required_processor(self):
        """RED: ContextLinker is required, not optional."""
        processor = ContextLinker()
        assert processor.is_optional() is False

    def test_no_dependencies(self):
        """RED: ContextLinker runs first, has no dependencies."""
        processor = ContextLinker()
        assert processor.get_dependencies() == []


class TestContextLinkerEmptyInput:
    """Test ContextLinker with empty or minimal input."""

    def test_empty_extraction_result(self):
        """RED: Should handle empty extraction result gracefully."""
        processor = ContextLinker()

        extraction_result = ExtractionResult(
            content_blocks=tuple(),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 0
        assert result.processing_stage == ProcessingStage.CONTEXT_LINKING
        assert "blocks_processed" in result.stage_metadata

    def test_single_paragraph_no_heading(self):
        """RED: Single paragraph without heading should have no parent."""
        processor = ContextLinker()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="This is a paragraph.")

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 1
        processed_block = result.content_blocks[0]
        assert processed_block.parent_id is None
        assert processed_block.metadata.get("depth") == 0


class TestContextLinkerHeadingHierarchy:
    """Test heading hierarchy detection and depth calculation."""

    def test_single_heading_with_paragraphs(self):
        """RED: Paragraphs should link to preceding heading."""
        processor = ContextLinker()

        heading = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        para1 = ContentBlock(block_type=ContentType.PARAGRAPH, content="First paragraph.")

        para2 = ContentBlock(block_type=ContentType.PARAGRAPH, content="Second paragraph.")

        extraction_result = ExtractionResult(
            content_blocks=(heading, para1, para2),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        assert len(result.content_blocks) == 3

        # Heading has no parent
        processed_heading = result.content_blocks[0]
        assert processed_heading.parent_id is None
        assert processed_heading.metadata.get("depth") == 0

        # Paragraphs link to heading
        processed_para1 = result.content_blocks[1]
        assert processed_para1.parent_id == heading.block_id
        assert processed_para1.metadata.get("depth") == 1

        processed_para2 = result.content_blocks[2]
        assert processed_para2.parent_id == heading.block_id
        assert processed_para2.metadata.get("depth") == 1

    def test_nested_headings_hierarchy(self):
        """RED: Nested headings should create tree structure."""
        processor = ContextLinker()

        h1 = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        h2 = ContentBlock(
            block_type=ContentType.HEADING, content="Section 1.1", metadata={"level": 2}
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content under section 1.1")

        extraction_result = ExtractionResult(
            content_blocks=(h1, h2, para),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # H1 is root (depth 0)
        processed_h1 = result.content_blocks[0]
        assert processed_h1.parent_id is None
        assert processed_h1.metadata.get("depth") == 0

        # H2 links to H1 (depth 1)
        processed_h2 = result.content_blocks[1]
        assert processed_h2.parent_id == h1.block_id
        assert processed_h2.metadata.get("depth") == 1

        # Paragraph links to H2 (depth 2)
        processed_para = result.content_blocks[2]
        assert processed_para.parent_id == h2.block_id
        assert processed_para.metadata.get("depth") == 2

    def test_multiple_root_headings(self):
        """RED: Multiple H1 headings should all be roots."""
        processor = ContextLinker()

        h1_a = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        para_a = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content for chapter 1")

        h1_b = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 2", metadata={"level": 1}
        )

        para_b = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content for chapter 2")

        extraction_result = ExtractionResult(
            content_blocks=(h1_a, para_a, h1_b, para_b),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # Both H1 headings are roots
        processed_h1_a = result.content_blocks[0]
        assert processed_h1_a.parent_id is None
        assert processed_h1_a.metadata.get("depth") == 0

        processed_h1_b = result.content_blocks[2]
        assert processed_h1_b.parent_id is None
        assert processed_h1_b.metadata.get("depth") == 0

        # Paragraphs link to their respective headings
        processed_para_a = result.content_blocks[1]
        assert processed_para_a.parent_id == h1_a.block_id

        processed_para_b = result.content_blocks[3]
        assert processed_para_b.parent_id == h1_b.block_id


class TestContextLinkerComplexStructures:
    """Test complex document structures."""

    def test_skip_level_hierarchy(self):
        """RED: H1 -> H3 (skipping H2) should work."""
        processor = ContextLinker()

        h1 = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        h3 = ContentBlock(
            block_type=ContentType.HEADING, content="Sub-section", metadata={"level": 3}
        )

        extraction_result = ExtractionResult(
            content_blocks=(h1, h3),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # H3 should link to H1 (closest higher level heading)
        processed_h3 = result.content_blocks[1]
        assert processed_h3.parent_id == h1.block_id

    def test_mixed_content_types(self):
        """RED: Tables, lists, etc. should also link to headings."""
        processor = ContextLinker()

        heading = ContentBlock(
            block_type=ContentType.HEADING, content="Data Section", metadata={"level": 1}
        )

        table = ContentBlock(
            block_type=ContentType.TABLE, content="[table content]", metadata={"rows": 3, "cols": 2}
        )

        list_item = ContentBlock(block_type=ContentType.LIST_ITEM, content="First item")

        extraction_result = ExtractionResult(
            content_blocks=(heading, table, list_item),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True

        # Both table and list item should link to heading
        processed_table = result.content_blocks[1]
        assert processed_table.parent_id == heading.block_id

        processed_list = result.content_blocks[2]
        assert processed_list.parent_id == heading.block_id


class TestContextLinkerMetadata:
    """Test metadata enrichment."""

    def test_stage_metadata_populated(self):
        """RED: Stage metadata should include hierarchy stats."""
        processor = ContextLinker()

        h1 = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content")

        extraction_result = ExtractionResult(
            content_blocks=(h1, para),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert "blocks_processed" in result.stage_metadata
        assert "heading_count" in result.stage_metadata
        assert "max_depth" in result.stage_metadata
        assert result.stage_metadata["heading_count"] == 1
        assert result.stage_metadata["blocks_processed"] == 2

    def test_document_path_in_metadata(self):
        """RED: Each block should have path from root in metadata."""
        processor = ContextLinker()

        h1 = ContentBlock(
            block_type=ContentType.HEADING, content="Chapter 1", metadata={"level": 1}
        )

        h2 = ContentBlock(
            block_type=ContentType.HEADING, content="Section 1.1", metadata={"level": 2}
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content")

        extraction_result = ExtractionResult(
            content_blocks=(h1, h2, para),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        # Paragraph should have document path
        processed_para = result.content_blocks[2]
        assert "document_path" in processed_para.metadata
        # Path should be list of heading titles
        path = processed_para.metadata["document_path"]
        assert "Chapter 1" in path
        assert "Section 1.1" in path


class TestContextLinkerErrorHandling:
    """Test error handling and edge cases."""

    def test_heading_without_level_metadata(self):
        """RED: Heading without level metadata should be treated as level 1."""
        processor = ContextLinker()

        heading = ContentBlock(
            block_type=ContentType.HEADING,
            content="Untitled Section",
            # No level metadata
        )

        para = ContentBlock(block_type=ContentType.PARAGRAPH, content="Content")

        extraction_result = ExtractionResult(
            content_blocks=(heading, para),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        assert result.success is True
        # Paragraph should still link to heading
        processed_para = result.content_blocks[1]
        assert processed_para.parent_id == heading.block_id

    def test_preserves_original_metadata(self):
        """RED: Should not overwrite existing metadata fields."""
        processor = ContextLinker()

        block = ContentBlock(
            block_type=ContentType.PARAGRAPH, content="Test", metadata={"custom_field": "value"}
        )

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        processed_block = result.content_blocks[0]
        # Original metadata should be preserved
        assert processed_block.metadata.get("custom_field") == "value"
        # New metadata should be added
        assert "depth" in processed_block.metadata

    def test_preserves_block_ids(self):
        """RED: Should preserve original block IDs."""
        processor = ContextLinker()

        block = ContentBlock(block_type=ContentType.PARAGRAPH, content="Test")
        original_id = block.block_id

        extraction_result = ExtractionResult(
            content_blocks=(block,),
            document_metadata=DocumentMetadata(source_file=Path("test.txt"), file_format="text"),
            success=True,
        )

        result = processor.process(extraction_result)

        processed_block = result.content_blocks[0]
        assert processed_block.block_id == original_id


class TestContextLinkerConfiguration:
    """Test configuration options."""

    def test_with_custom_config(self):
        """RED: Should accept configuration dict."""
        config = {"max_depth": 5, "include_path": True}
        processor = ContextLinker(config=config)
        assert processor.config == config

    def test_with_no_config(self):
        """RED: Should work with no configuration."""
        processor = ContextLinker()
        assert processor.config == {}
