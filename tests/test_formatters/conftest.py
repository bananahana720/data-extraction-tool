"""
Shared test fixtures for formatter tests.

Provides reusable ProcessingResult objects with various characteristics:
- Minimal results (basic structure)
- Rich results (multiple content types)
- Edge cases (empty, deeply nested, unicode)
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from core.models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    ImageMetadata,
    Position,
    ProcessingResult,
    ProcessingStage,
    TableMetadata,
)


@pytest.fixture
def minimal_processing_result():
    """Minimal ProcessingResult with basic heading and paragraph."""
    return ProcessingResult(
        content_blocks=(
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.HEADING,
                content="Test Document",
                position=Position(sequence_index=0),
            ),
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content="This is a test paragraph.",
                position=Position(sequence_index=1),
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=Path("test.docx"),
            file_format="docx",
            file_size_bytes=1024,
            title="Test Document",
            author="Test Author",
            word_count=5,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=True,
    )


@pytest.fixture
def rich_processing_result():
    """Rich ProcessingResult with multiple content types and relationships."""
    heading_id = uuid4()
    subheading_id = uuid4()

    blocks = [
        # Main heading
        ContentBlock(
            block_id=heading_id,
            block_type=ContentType.HEADING,
            content="Chapter 1: Introduction",
            position=Position(page=1, sequence_index=0),
            metadata={"level": 1},
        ),
        # Paragraph under heading
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.PARAGRAPH,
            content="This chapter introduces key concepts.",
            position=Position(page=1, sequence_index=1),
            parent_id=heading_id,
        ),
        # Subheading
        ContentBlock(
            block_id=subheading_id,
            block_type=ContentType.HEADING,
            content="1.1 Background",
            position=Position(page=1, sequence_index=2),
            parent_id=heading_id,
            metadata={"level": 2},
        ),
        # List items
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.LIST_ITEM,
            content="First item",
            position=Position(page=1, sequence_index=3),
            parent_id=subheading_id,
            metadata={"list_type": "bullet"},
        ),
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.LIST_ITEM,
            content="Second item",
            position=Position(page=1, sequence_index=4),
            parent_id=subheading_id,
            metadata={"list_type": "bullet"},
        ),
        # Quote
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.QUOTE,
            content="This is a quoted text.",
            position=Position(page=2, sequence_index=5),
        ),
        # Code block
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.CODE,
            content="def hello():\n    print('world')",
            position=Position(page=2, sequence_index=6),
            metadata={"language": "python"},
        ),
        # Table reference
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.TABLE,
            content="[Table: Sales Data]",
            position=Position(page=3, sequence_index=7),
            metadata={"table_id": str(uuid4())},
        ),
        # Image reference
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.IMAGE,
            content="[Figure 1: Architecture Diagram]",
            position=Position(page=3, sequence_index=8),
            metadata={
                "image_id": str(uuid4()),
                "alt_text": "Architecture diagram showing system components",
            },
        ),
    ]

    return ProcessingResult(
        content_blocks=tuple(blocks),
        document_metadata=DocumentMetadata(
            source_file=Path("rich_document.docx"),
            file_format="docx",
            file_size_bytes=50000,
            title="Rich Test Document",
            author="Jane Doe",
            created_date=datetime(2025, 1, 1),
            page_count=3,
            word_count=150,
            image_count=1,
            table_count=1,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        quality_score=95.0,
        success=True,
    )


@pytest.fixture
def empty_processing_result():
    """Empty ProcessingResult with no content blocks."""
    return ProcessingResult(
        content_blocks=tuple(),
        document_metadata=DocumentMetadata(
            source_file=Path("empty.docx"),
            file_format="docx",
            file_size_bytes=0,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=True,
    )


@pytest.fixture
def unicode_processing_result():
    """ProcessingResult with unicode content (emojis, Chinese, RTL)."""
    return ProcessingResult(
        content_blocks=(
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.HEADING,
                content="Unicode Test: 你好世界 مرحبا بالعالم",
            ),
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content="Emojis: 🎉 🚀 💻 and special chars: é ñ ü",
            ),
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content="Math symbols: ∑ ∫ √ ∞",
            ),
        ),
        document_metadata=DocumentMetadata(
            source_file=Path("unicode.docx"),
            file_format="docx",
            file_size_bytes=2048,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=True,
    )


@pytest.fixture
def deeply_nested_result():
    """ProcessingResult with deeply nested structure (heading hierarchy)."""
    blocks = []
    parent_id = None

    # Create 5 levels of headings
    for level in range(1, 6):
        heading_id = uuid4()
        blocks.append(
            ContentBlock(
                block_id=heading_id,
                block_type=ContentType.HEADING,
                content=f"Heading Level {level}",
                parent_id=parent_id,
                metadata={"level": level},
                position=Position(sequence_index=len(blocks)),
            )
        )
        # Add a paragraph under each heading
        blocks.append(
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content=f"Content under level {level} heading.",
                parent_id=heading_id,
                position=Position(sequence_index=len(blocks)),
            )
        )
        parent_id = heading_id

    return ProcessingResult(
        content_blocks=tuple(blocks),
        document_metadata=DocumentMetadata(
            source_file=Path("nested.docx"),
            file_format="docx",
            file_size_bytes=4096,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=True,
    )


@pytest.fixture
def long_content_result():
    """ProcessingResult with very long content (for chunking tests)."""
    blocks = []

    # Create main heading
    blocks.append(
        ContentBlock(
            block_id=uuid4(),
            block_type=ContentType.HEADING,
            content="Long Document",
            position=Position(sequence_index=0),
        )
    )

    # Add 50 paragraphs of substantial content
    lorem_text = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris. "
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum. "
    )

    for i in range(50):
        blocks.append(
            ContentBlock(
                block_id=uuid4(),
                block_type=ContentType.PARAGRAPH,
                content=f"Paragraph {i+1}: {lorem_text}",
                position=Position(sequence_index=i + 1),
            )
        )

    return ProcessingResult(
        content_blocks=tuple(blocks),
        document_metadata=DocumentMetadata(
            source_file=Path("long.docx"),
            file_format="docx",
            file_size_bytes=100000,
            word_count=5000,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=True,
    )


@pytest.fixture
def failed_processing_result():
    """ProcessingResult that indicates processing failure."""
    return ProcessingResult(
        content_blocks=tuple(),
        document_metadata=DocumentMetadata(
            source_file=Path("failed.docx"),
            file_format="docx",
            file_size_bytes=1024,
        ),
        processing_stage=ProcessingStage.FORMATTING,
        success=False,
        errors=("Processing failed due to test error",),
        warnings=("Warning: partial extraction",),
    )


@pytest.fixture
def table_metadata_sample():
    """Sample TableMetadata for testing table formatting."""
    return TableMetadata(
        table_id=uuid4(),
        num_rows=3,
        num_columns=3,
        has_header=True,
        header_row=("Name", "Age", "City"),
        cells=(
            ("Alice", "30", "New York"),
            ("Bob", "25", "San Francisco"),
            ("Charlie", "35", "Seattle"),
        ),
    )


@pytest.fixture
def image_metadata_sample():
    """Sample ImageMetadata for testing image formatting."""
    return ImageMetadata(
        image_id=uuid4(),
        file_path=Path("test_image.png"),
        format="PNG",
        width=800,
        height=600,
        alt_text="Test image description",
        caption="Figure 1: Test Image",
        image_type="diagram",
    )
