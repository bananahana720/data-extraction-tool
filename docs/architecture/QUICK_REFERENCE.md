# Quick Reference: Foundation API

One-page reference for building on the foundation.

## Core Imports

```python
from core import (
    # Models
    ContentBlock, ContentType, Position,
    ExtractionResult, ProcessingResult, FormattedOutput,
    DocumentMetadata, ImageMetadata, TableMetadata,

    # Interfaces
    BaseExtractor, BaseProcessor, BaseFormatter, BasePipeline
)
```

## Creating Content Blocks

```python
from uuid import uuid4

block = ContentBlock(
    block_id=uuid4(),                      # Unique ID
    block_type=ContentType.PARAGRAPH,      # Type from enum
    content="Text content",                # Primary content
    raw_content="Original text",           # Optional: before processing
    position=Position(page=1, sequence_index=0),  # Location info
    parent_id=None,                        # Optional: parent block ID
    related_ids=(),                        # Optional: related block IDs
    metadata={"word_count": 2},            # Extensible metadata
    confidence=0.95,                       # Optional: extraction confidence
    style={"bold": True}                   # Optional: formatting
)
```

## Content Types

```python
ContentType.PARAGRAPH   # Body text
ContentType.HEADING     # H1-H6 headings
ContentType.LIST_ITEM   # List items
ContentType.TABLE       # Tables
ContentType.IMAGE       # Images
ContentType.CODE        # Code blocks
ContentType.QUOTE       # Block quotes
ContentType.FOOTNOTE    # Footnotes
ContentType.COMMENT     # Comments/annotations
ContentType.HYPERLINK   # Links
ContentType.METADATA    # Document metadata
ContentType.UNKNOWN     # Fallback
```

## Building an Extractor

```python
from pathlib import Path
from core import BaseExtractor, ExtractionResult, ContentBlock, DocumentMetadata

class MyExtractor(BaseExtractor):
    def supports_format(self, file_path: Path) -> bool:
        """Check if this extractor handles this file."""
        return file_path.suffix.lower() in [".txt", ".md"]

    def extract(self, file_path: Path) -> ExtractionResult:
        """Extract content from file."""
        # Validate
        is_valid, errors = self.validate_file(file_path)
        if not is_valid:
            return ExtractionResult(
                success=False,
                errors=tuple(errors),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="text"
                )
            )

        # Extract
        try:
            text = file_path.read_text()
            blocks = [
                ContentBlock(
                    block_type=ContentType.PARAGRAPH,
                    content=para
                )
                for para in text.split("\n\n") if para.strip()
            ]

            return ExtractionResult(
                content_blocks=tuple(blocks),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="text",
                    word_count=len(text.split())
                ),
                success=True
            )
        except Exception as e:
            return ExtractionResult(
                success=False,
                errors=(str(e),),
                document_metadata=DocumentMetadata(
                    source_file=file_path,
                    file_format="text"
                )
            )
```

## Building a Processor

```python
from core import BaseProcessor, ProcessingResult, ExtractionResult, ContentBlock

class MyProcessor(BaseProcessor):
    def get_dependencies(self) -> list[str]:
        """Processors that must run first."""
        return []  # No dependencies

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """Process/enrich extracted content."""
        enriched_blocks = []

        for block in extraction_result.content_blocks:
            # Enrich metadata (blocks are immutable!)
            new_block = ContentBlock(
                block_id=block.block_id,
                block_type=block.block_type,
                content=block.content,
                raw_content=block.raw_content,
                position=block.position,
                parent_id=block.parent_id,
                related_ids=block.related_ids,
                metadata={
                    **block.metadata,
                    "processed": True,
                    "word_count": len(block.content.split())
                },
                confidence=block.confidence,
                style=block.style
            )
            enriched_blocks.append(new_block)

        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            document_metadata=extraction_result.document_metadata,
            success=True
        )
```

## Building a Formatter

```python
from core import BaseFormatter, FormattedOutput, ProcessingResult

class MyFormatter(BaseFormatter):
    def get_format_type(self) -> str:
        """Format identifier."""
        return "json"  # or "markdown", "chunked", etc.

    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """Convert to target format."""
        import json

        output = {
            "blocks": [
                {
                    "type": block.block_type.value,
                    "content": block.content,
                    "metadata": block.metadata
                }
                for block in processing_result.content_blocks
            ]
        }

        return FormattedOutput(
            content=json.dumps(output, indent=2),
            format_type=self.get_format_type(),
            source_document=processing_result.document_metadata.source_file,
            success=True
        )
```

## Result Types Summary

| Result Type | Used By | Contains |
|-------------|---------|----------|
| `ExtractionResult` | Extractors | Raw content blocks, images, tables |
| `ProcessingResult` | Processors | Enriched content blocks, quality score |
| `FormattedOutput` | Formatters | Formatted string, output files |
| `PipelineResult` | Pipeline | All results from complete run |

## Error Handling Pattern

```python
# In extractors, processors, formatters:
def extract(self, file_path: Path) -> ExtractionResult:
    try:
        # Do work
        return ExtractionResult(success=True, ...)
    except ExpectedError as e:
        # Return failure result
        return ExtractionResult(
            success=False,
            errors=(str(e),)
        )
    # Don't catch unexpected errors - let them propagate
```

## Immutability Pattern

```python
# ✓ CORRECT: Create new object with changes
new_block = ContentBlock(
    block_id=old_block.block_id,
    block_type=old_block.block_type,
    content=old_block.content,
    # ... copy all fields ...
    metadata={**old_block.metadata, "new_field": "value"}  # Extend
)

# ✗ WRONG: Can't modify frozen dataclass
old_block.metadata["new_field"] = "value"  # FrozenInstanceError!
```

## Position Info

```python
# Document with pages
Position(page=1, sequence_index=0)

# Presentation with slides
Position(slide=3, sequence_index=5)

# Spreadsheet with sheets
Position(sheet="Sheet1", sequence_index=10)

# With bounding box
Position(page=1, x=100, y=200, width=300, height=50)
```

## Metadata Patterns

```python
# Document metadata
DocumentMetadata(
    source_file=Path("doc.pdf"),
    file_format="pdf",
    title="My Document",
    author="John Doe",
    page_count=10,
    word_count=5000
)

# Image metadata
ImageMetadata(
    file_path=Path("image.png"),
    format="PNG",
    width=800,
    height=600,
    alt_text="Diagram showing..."
)

# Table metadata
TableMetadata(
    num_rows=5,
    num_columns=3,
    has_header=True,
    header_row=("Name", "Age", "City"),
    cells=(("Alice", "30", "NYC"), ...)
)
```

## Testing Your Module

```python
def test_my_extractor():
    extractor = MyExtractor()

    # Test file support
    assert extractor.supports_format(Path("test.txt"))
    assert not extractor.supports_format(Path("test.pdf"))

    # Test extraction
    result = extractor.extract(Path("test.txt"))
    assert result.success
    assert len(result.content_blocks) > 0
    assert result.content_blocks[0].block_type == ContentType.PARAGRAPH
```

## Common Patterns

### Extract paragraphs from text
```python
text = file.read_text()
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
blocks = [
    ContentBlock(
        block_type=ContentType.PARAGRAPH,
        content=para,
        position=Position(sequence_index=idx)
    )
    for idx, para in enumerate(paragraphs)
]
```

### Link caption to image
```python
image_block = ContentBlock(block_type=ContentType.IMAGE, ...)
caption_block = ContentBlock(
    block_type=ContentType.PARAGRAPH,
    content="Figure 1: Diagram",
    related_ids=(image_block.block_id,)  # Link to image
)
```

### Create heading hierarchy
```python
h1_block = ContentBlock(block_type=ContentType.HEADING, ...)
para_block = ContentBlock(
    block_type=ContentType.PARAGRAPH,
    parent_id=h1_block.block_id  # Paragraph belongs to heading
)
```

### Add quality warning
```python
ProcessingResult(
    content_blocks=blocks,
    quality_score=75.0,
    quality_issues=("Low OCR confidence on page 3",),
    needs_review=True,
    success=True
)
```

## File Structure

```
src/core/              # Foundation (done)
  ├── models.py        # Data models
  ├── interfaces.py    # Base classes
  └── __init__.py      # Public API

src/extractors/        # Format extractors (to build)
  ├── docx_extractor.py
  ├── pdf_extractor.py
  └── ...

src/processors/        # Content processors (to build)
  ├── context_linker.py
  ├── metadata_aggregator.py
  └── ...

src/formatters/        # Output formatters (to build)
  ├── json_formatter.py
  ├── markdown_formatter.py
  └── ...

src/pipeline/          # Orchestration (to build)
  ├── pipeline.py
  └── batch_processor.py
```

## Quick Start

```bash
# Test foundation
python examples/minimal_extractor.py
python examples/minimal_processor.py

# Read documentation
cat FOUNDATION.md        # Complete guide
cat GETTING_STARTED.md   # How to build modules

# Start building
# Pick a module from GETTING_STARTED.md and implement it
```

## Remember

1. **Models are immutable** - Create new, don't modify
2. **Return success/failure** - Don't raise exceptions for expected errors
3. **Use type hints** - Helps catch errors early
4. **Test as you go** - Run examples to validate
5. **Study examples** - See working code in `examples/`

## Help

- Detailed guide: `FOUNDATION.md`
- Getting started: `GETTING_STARTED.md`
- Working examples: `examples/minimal_*.py`
- Source with docstrings: `src/core/*.py`
