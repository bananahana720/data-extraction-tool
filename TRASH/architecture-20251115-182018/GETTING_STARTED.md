# Getting Started: Building on the Foundation

The foundation is complete. This guide shows you how to build on top of it.

## What's Done

### ✓ Core Data Models (`src/core/models.py`)
- **ContentBlock** - Atomic unit of content
- **ExtractionResult** - Output from extractors
- **ProcessingResult** - Output from processors
- **FormattedOutput** - Output from formatters
- **PipelineResult** - Complete pipeline output

All models are:
- Immutable (frozen dataclasses)
- Type-safe (full type hints)
- Serializable (for debugging and persistence)

### ✓ Interface Contracts (`src/core/interfaces.py`)
- **BaseExtractor** - Contract for format extractors
- **BaseProcessor** - Contract for content processors
- **BaseFormatter** - Contract for output formatters
- **BasePipeline** - Contract for pipeline orchestrators

All interfaces:
- Define clear contracts
- Support optional methods for advanced features
- Enable modular, independent development

### ✓ Working Examples
- **minimal_extractor.py** - Simple text file extractor
- **minimal_processor.py** - Simple word count processor

Both examples are tested and working.

## What This Enables

### 1. Independent Module Development

**Extractors** can be developed in parallel:
```python
# Developer A: DocxExtractor
class DocxExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        # DOCX-specific logic
        pass

# Developer B: PdfExtractor
class PdfExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        # PDF-specific logic
        pass
```

Both produce `ExtractionResult` → compatible with same pipeline.

### 2. Pluggable Architecture

Add new formats without modifying existing code:
```python
# Pipeline doesn't care about format details
pipeline.register_extractor("docx", DocxExtractor())
pipeline.register_extractor("pdf", PdfExtractor())
pipeline.register_extractor("custom", CustomExtractor())  # Add anytime!
```

### 3. Composable Processors

Processors declare dependencies, pipeline handles ordering:
```python
class MetadataAggregator(BaseProcessor):
    def get_dependencies(self) -> list[str]:
        return ["ContextLinker"]  # Must run after ContextLinker

# Pipeline automatically orders: ContextLinker → MetadataAggregator
```

### 4. Parallel Formatters

Formatters are independent, can run in parallel:
```python
# All produce output simultaneously
pipeline.add_formatter(JsonFormatter())
pipeline.add_formatter(MarkdownFormatter())
pipeline.add_formatter(ChunkedTextFormatter())
```

## Building Blocks Available Now

### ContentType Enum
Pre-defined content types for common cases:
```python
ContentType.PARAGRAPH
ContentType.HEADING
ContentType.TABLE
ContentType.IMAGE
ContentType.CODE
ContentType.FOOTNOTE
# ... and more
```

### Position Tracking
Track where content came from:
```python
Position(
    page=1,
    slide=None,
    sheet="Sheet1",
    sequence_index=5
)
```

### Metadata Extensibility
Store format-specific data:
```python
ContentBlock(
    content="Hello world",
    metadata={
        "font_size": 12,
        "is_bold": True,
        "custom_field": "value"
    }
)
```

## Next Steps: What to Build

### Priority 1: Core Extractors (Week 1-4)

Build format-specific extractors using the foundation:

1. **DocxExtractor** - `src/extractors/docx_extractor.py`
   - Use `python-docx` library
   - Extract paragraphs, headings, tables, images
   - Preserve styles and formatting
   - Return `ExtractionResult`

2. **PdfExtractor** - `src/extractors/pdf_extractor.py`
   - Use `pypdf` library
   - Extract text with position info
   - Detect image-based PDFs for OCR
   - Return `ExtractionResult`

3. **PptxExtractor** - `src/extractors/pptx_extractor.py`
   - Use `python-pptx` library
   - Extract slides, text, images
   - Include speaker notes
   - Return `ExtractionResult`

4. **ExcelExtractor** - `src/extractors/excel_extractor.py`
   - Use `openpyxl` library
   - Extract tables, formulas, charts
   - Handle multiple sheets
   - Return `ExtractionResult`

**Key Point:** All extractors implement the same `BaseExtractor` interface.
No coordination needed - just implement `extract()` and `supports_format()`.

### Priority 2: Core Processors (Week 3-6)

Build content processors that enrich extraction results:

1. **ContextLinker** - `src/processors/context_linker.py`
   - Link headings to paragraphs
   - Link captions to images
   - Build document tree
   - Return `ProcessingResult`

2. **MetadataAggregator** - `src/processors/metadata_aggregator.py`
   - Compute statistics (word count, page count)
   - Extract document properties
   - Generate content summary
   - Return `ProcessingResult`

3. **QualityValidator** - `src/processors/quality_validator.py`
   - Score extraction quality (0-100)
   - Detect incomplete extraction
   - Flag low-confidence results
   - Return `ProcessingResult`

**Key Point:** Declare dependencies with `get_dependencies()`.
Pipeline handles ordering automatically.

### Priority 3: Output Formatters (Week 5-8)

Build output formatters for AI consumption:

1. **JsonFormatter** - `src/formatters/json_formatter.py`
   - Serialize to structured JSON
   - Include all metadata
   - Validate against schema
   - Return `FormattedOutput`

2. **MarkdownFormatter** - `src/formatters/markdown_formatter.py`
   - Convert to readable Markdown
   - Preserve headings, lists, tables
   - Include frontmatter metadata
   - Return `FormattedOutput`

3. **ChunkedTextFormatter** - `src/formatters/chunked_formatter.py`
   - Split by token count
   - Maintain context with overlap
   - Generate chunk metadata
   - Return `FormattedOutput`

**Key Point:** Formatters are independent. Can add new formats anytime.

### Priority 4: Pipeline Implementation (Week 7-10)

Build the orchestrator that ties everything together:

1. **ExtractionPipeline** - `src/pipeline/pipeline.py`
   - Implements `BasePipeline`
   - Registers extractors, processors, formatters
   - Handles error propagation
   - Tracks progress and metrics
   - Returns `PipelineResult`

2. **BatchProcessor** - `src/pipeline/batch_processor.py`
   - Parallel file processing
   - Progress tracking
   - Resource management
   - Summary reporting

### Priority 5: CLI Interface (Week 9-12)

Build user-facing interface:

1. **CLI Framework** - `src/cli/main.py`
   - Use Click for CLI
   - Commands: `extract`, `batch`, `config`
   - Rich progress bars
   - User-friendly error messages

## Development Workflow

### 1. Pick a Module

Choose a module to implement (extractor, processor, formatter).

### 2. Study the Interface

Read the base class documentation:
```python
# For extractors
from core import BaseExtractor

# Read the docstrings
help(BaseExtractor)
help(BaseExtractor.extract)
```

### 3. Study the Example

Look at the working example:
```python
# For extractors
cat examples/minimal_extractor.py

# For processors
cat examples/minimal_processor.py
```

### 4. Implement the Interface

Create your module:
```python
from core import BaseExtractor, ExtractionResult

class MyExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        # Your logic here
        pass

    def supports_format(self, file_path: Path) -> bool:
        # Your logic here
        pass
```

### 5. Test Your Module

Create a test file:
```python
# test_my_extractor.py
from my_extractor import MyExtractor

def test_extraction():
    extractor = MyExtractor()
    result = extractor.extract(Path("sample.txt"))
    assert result.success
    assert len(result.content_blocks) > 0
```

### 6. Integrate with Pipeline

Once working, register with pipeline:
```python
pipeline.register_extractor("myformat", MyExtractor())
```

## Testing Your Work

### Run Examples
```bash
# Test extractor example
python examples/minimal_extractor.py

# Test processor example
python examples/minimal_processor.py
```

### Create Your Own Tests
```python
from core import ContentBlock, ContentType, ExtractionResult

# Create test data
block = ContentBlock(
    block_type=ContentType.PARAGRAPH,
    content="Test content"
)

result = ExtractionResult(
    content_blocks=(block,),
    success=True
)

# Verify properties
assert len(result) == 1
assert result.success
assert result.content_blocks[0].content == "Test content"
```

## Design Guidelines

### 1. Follow Immutability

Never modify objects in place:
```python
# ✗ WRONG
block.metadata["new_field"] = "value"  # Error: frozen!

# ✓ CORRECT
new_block = ContentBlock(
    block_id=block.block_id,
    block_type=block.block_type,
    content=block.content,
    # ... copy other fields ...
    metadata={**block.metadata, "new_field": "value"}
)
```

### 2. Use Type Hints

Always specify types:
```python
# ✓ CORRECT
def process(self, result: ExtractionResult) -> ProcessingResult:
    pass

# ✗ WRONG
def process(self, result):  # What type?
    pass
```

### 3. Return Success/Failure

Don't raise exceptions for expected failures:
```python
# ✓ CORRECT
def extract(self, file_path: Path) -> ExtractionResult:
    try:
        content = self._read_file(file_path)
        return ExtractionResult(success=True, ...)
    except FileNotFoundError:
        return ExtractionResult(
            success=False,
            errors=("File not found",)
        )

# ✗ WRONG
def extract(self, file_path: Path) -> ExtractionResult:
    content = self._read_file(file_path)  # Raises exception!
```

### 4. Preserve Data

When processing, keep original data:
```python
# ✓ CORRECT
new_block = ContentBlock(
    block_id=block.block_id,  # Keep same ID
    content=block.content,     # Keep content
    raw_content=block.raw_content,  # Keep raw
    metadata={**block.metadata, "new_field": "value"}  # Extend metadata
)

# ✗ WRONG
new_block = ContentBlock(
    content=block.content.upper(),  # Lost original!
    metadata={"new_field": "value"}  # Lost original metadata!
)
```

## Resources

### Documentation
- **FOUNDATION.md** - Complete foundation guide
- **src/core/models.py** - Data model source + docstrings
- **src/core/interfaces.py** - Interface source + docstrings

### Examples
- **examples/minimal_extractor.py** - Working extractor example
- **examples/minimal_processor.py** - Working processor example

### Reference Implementation
- **reference-only-draft-scripts/** - Original prototype (for reference only)

## Questions?

### How do I add a new content type?

Add to `ContentType` enum in `models.py`:
```python
class ContentType(str, Enum):
    # ... existing types ...
    MY_NEW_TYPE = "my_new_type"
```

### How do I pass config to modules?

Use the config dict in constructors:
```python
extractor = MyExtractor(config={
    "enable_ocr": True,
    "language": "en"
})
```

### How do I handle format-specific metadata?

Use the `metadata` dict in `ContentBlock`:
```python
block = ContentBlock(
    content="Hello",
    metadata={
        "docx_style": "Heading1",
        "pdf_font": "Arial",
        "custom_data": {...}
    }
)
```

### How do I track relationships between blocks?

Use `parent_id` and `related_ids`:
```python
# Paragraph belongs to heading
paragraph = ContentBlock(
    content="Body text",
    parent_id=heading.block_id
)

# Caption linked to image
caption = ContentBlock(
    content="Figure 1: Diagram",
    related_ids=(image.block_id,)
)
```

## Ready to Build

The foundation is solid. Pick a module and start building.

**Remember:** If the foundation needs changes, that's OK. Better to discover
issues now than after building 50 modules. The examples are working, so the
core design is sound. But be open to refinements as you build real modules.

**Next:** Build `DocxExtractor` or start with configuration system (INFRA-001).
