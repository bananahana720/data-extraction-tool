# Foundation: Core Data Models & Interface Contracts

This document explains the foundational architecture that all modules build upon.

## Philosophy: Get the Foundation Right

The foundation consists of two critical pieces:

1. **Data Models** - The universal language all modules speak
2. **Interface Contracts** - The rules for how modules interact

**Get these right, and everything else becomes modular and composable.**
Get these wrong, and you'll be refactoring everything.

## Core Principles

### Immutability
All data models are **immutable** (frozen dataclasses). This prevents accidental mutations during processing and makes data flow traceable.

```python
# ✓ CORRECT: Create new block with modifications
enriched_block = ContentBlock(
    block_id=original_block.block_id,
    content=original_block.content,
    metadata={**original_block.metadata, "new_field": "value"}
)

# ✗ WRONG: Can't mutate (will raise error)
original_block.metadata["new_field"] = "value"  # FrozenInstanceError!
```

### Type Safety
Everything uses **full type hints**. This catches errors at development time, not runtime.

```python
def extract(self, file_path: Path) -> ExtractionResult:
    # Type checker knows file_path is Path, not str
    # Type checker knows return value is ExtractionResult
```

### Clear Contracts
Interfaces define **exactly what each module must do**. No guessing.

```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        """Extract content. Must implement."""
        pass

    def supports_streaming(self) -> bool:
        """Optional: Override if you support streaming."""
        return False
```

## The Data Models

### ContentBlock - The Atomic Unit

Everything is composed of `ContentBlock` objects. A document is just a collection of blocks.

```python
@dataclass(frozen=True)
class ContentBlock:
    block_id: UUID              # Unique identifier
    block_type: ContentType     # paragraph, heading, table, image, etc.
    content: str                # Primary text content
    position: Optional[Position]  # Where in document
    metadata: dict[str, Any]    # Extensible metadata
    confidence: Optional[float] # Extraction confidence (0.0-1.0)
```

**Key Features:**
- **Immutable**: Can't be modified after creation
- **Self-contained**: All information in one place
- **Extensible**: `metadata` dict for format-specific data
- **Traceable**: `block_id` for tracking through pipeline

### Pipeline Data Flow

```
Path → ExtractionResult → ProcessingResult → FormattedOutput → PipelineResult
```

Each stage has its own result type:

1. **ExtractionResult** - Raw content from file
2. **ProcessingResult** - Enriched content after processing
3. **FormattedOutput** - Final formatted output
4. **PipelineResult** - Complete pipeline run

### Why Separate Result Types?

Each stage has different concerns:

- **ExtractionResult**: "What did I find in the file?"
  - Content blocks, images, tables
  - File metadata
  - Extraction errors

- **ProcessingResult**: "How did I enrich the content?"
  - Modified content blocks
  - Quality score
  - Processing-specific metadata

- **FormattedOutput**: "What's the final output?"
  - Formatted string (JSON, Markdown, etc.)
  - Additional files (images, sidecars)
  - Format-specific metadata

## The Interface Contracts

### BaseExtractor - Reading Files

```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        """Core extraction logic. Must implement."""
        pass

    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """Can this extractor handle this file?"""
        pass
```

**Contract:**
- Input: File path
- Output: `ExtractionResult` with `success` flag
- Never raise exceptions for file-level failures
- Return partial results when possible

### BaseProcessor - Enriching Content

```python
class BaseProcessor(ABC):
    @abstractmethod
    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """Enrich extracted content."""
        pass

    def get_dependencies(self) -> list[str]:
        """What processors must run first?"""
        return []
```

**Contract:**
- Input: `ExtractionResult` (or previous `ProcessingResult`)
- Output: `ProcessingResult` with enriched data
- Declare dependencies for ordering
- Mark as optional if non-critical

### BaseFormatter - Creating Output

```python
class BaseFormatter(ABC):
    @abstractmethod
    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """Convert to target format."""
        pass

    @abstractmethod
    def get_format_type(self) -> str:
        """Format identifier (json, markdown, etc.)."""
        pass
```

**Contract:**
- Input: `ProcessingResult`
- Output: `FormattedOutput` with formatted string
- Independent (can run in parallel with other formatters)

## Working with the Foundation

### Example 1: Simple Extractor

See `examples/minimal_extractor.py` for a complete working example.

```python
from core import BaseExtractor, ContentBlock, ExtractionResult

class MyExtractor(BaseExtractor):
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix == ".txt"

    def extract(self, file_path: Path) -> ExtractionResult:
        # Validate
        is_valid, errors = self.validate_file(file_path)
        if not is_valid:
            return ExtractionResult(success=False, errors=tuple(errors))

        # Extract
        text = file_path.read_text()
        blocks = [
            ContentBlock(
                block_type=ContentType.PARAGRAPH,
                content=paragraph,
                position=Position(sequence_index=idx)
            )
            for idx, paragraph in enumerate(text.split("\n\n"))
        ]

        # Return
        return ExtractionResult(
            content_blocks=tuple(blocks),
            success=True
        )
```

### Example 2: Simple Processor

See `examples/minimal_processor.py` for a complete working example.

```python
from core import BaseProcessor, ProcessingResult

class MyProcessor(BaseProcessor):
    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        # Enrich blocks (remember: immutable!)
        enriched_blocks = []
        for block in extraction_result.content_blocks:
            # Create new block with enriched metadata
            new_block = ContentBlock(
                block_id=block.block_id,  # Keep same ID
                block_type=block.block_type,
                content=block.content,
                # ... copy other fields ...
                metadata={
                    **block.metadata,
                    "word_count": len(block.content.split())
                }
            )
            enriched_blocks.append(new_block)

        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            success=True
        )
```

### Example 3: Building a Pipeline

```python
from core import BasePipeline, PipelineResult

# Create pipeline
pipeline = Pipeline()

# Register extractors
pipeline.register_extractor("docx", DocxExtractor())
pipeline.register_extractor("pdf", PdfExtractor())

# Add processors (auto-ordered by dependencies)
pipeline.add_processor(ContextLinker())
pipeline.add_processor(MetadataAggregator())

# Add formatters (run in parallel)
pipeline.add_formatter(JsonFormatter())
pipeline.add_formatter(MarkdownFormatter())

# Process file
result = pipeline.process_file(Path("document.docx"))

if result.success:
    print(f"✓ Processed {result.source_file}")
    for output in result.formatted_outputs:
        print(f"  - {output.format_type}: {output.content[:100]}...")
```

## Design Decisions

### Why Frozen Dataclasses?

**Immutability prevents bugs.** When data can't change, you can reason about it locally without worrying about side effects.

```python
# With mutable data:
def process(block):
    block.metadata["processed"] = True  # Mutates original!
    return block

# With immutable data:
def process(block):
    return ContentBlock(
        **dataclasses.asdict(block),
        metadata={**block.metadata, "processed": True}
    )  # Returns new block, original unchanged
```

### Why Abstract Base Classes?

**Clear contracts prevent integration issues.** If your extractor doesn't implement `extract()`, it won't even run.

```python
# Type checker catches missing methods
class BadExtractor(BaseExtractor):
    def supports_format(self, file_path: Path) -> bool:
        return True
    # Missing extract()! Type checker error.

# Can't instantiate incomplete implementations
extractor = BadExtractor()  # Error: Can't instantiate abstract class
```

### Why Separate Result Types?

**Each stage has different concerns.** Mixing them creates confusion.

```python
# ✗ BAD: Single result type for everything
class Result:
    content_blocks: list
    quality_score: float  # Only relevant after processing
    formatted_output: str  # Only relevant after formatting
    # What fields are valid when?

# ✓ GOOD: Stage-specific result types
ExtractionResult   # Has content_blocks, no quality_score
ProcessingResult   # Has content_blocks AND quality_score
FormattedOutput    # Has formatted_output, not content_blocks
```

## Testing the Foundation

Run the examples to validate the design:

```bash
# Test minimal extractor
python examples/minimal_extractor.py

# Test minimal processor
python examples/minimal_processor.py
```

Expected output:
```
✓ Extraction successful!
  Blocks: 5
  Words: 47
  Characters: 289

Content blocks:
  - [heading] Introduction...
  - [paragraph] This is a sample document to demonstrate the extraction...
  ...
```

## Next Steps

Now that the foundation exists, you can build modules independently:

1. **Extractors**: `DocxExtractor`, `PdfExtractor`, `PptxExtractor`, etc.
   - Each implements `BaseExtractor`
   - Each produces `ExtractionResult`
   - Independent development

2. **Processors**: `ContextLinker`, `MetadataAggregator`, etc.
   - Each implements `BaseProcessor`
   - Each transforms `ExtractionResult` → `ProcessingResult`
   - Declare dependencies, pipeline orders them

3. **Formatters**: `JsonFormatter`, `MarkdownFormatter`, etc.
   - Each implements `BaseFormatter`
   - Each transforms `ProcessingResult` → `FormattedOutput`
   - Run in parallel

4. **Pipeline**: Orchestrates everything
   - Implements `BasePipeline`
   - Manages extractors, processors, formatters
   - Handles errors, progress, metrics

## Key Takeaways

1. **Everything is a ContentBlock** - Universal building block
2. **Immutable by design** - Prevents bugs, enables reasoning
3. **Type-safe contracts** - Catch errors early
4. **Stage-specific results** - Clear separation of concerns
5. **Pluggable architecture** - Add modules without modifying core

**The foundation is complete. Everything else builds on top of these models and interfaces.**

---

## File Structure

```
src/core/
├── __init__.py       # Public API exports
├── models.py         # Data models (ContentBlock, etc.)
└── interfaces.py     # Interface contracts (BaseExtractor, etc.)

examples/
├── minimal_extractor.py   # Example extractor
└── minimal_processor.py   # Example processor
```

## Public API

```python
from core import (
    # Data models
    ContentBlock,
    ContentType,
    ExtractionResult,
    ProcessingResult,
    FormattedOutput,
    PipelineResult,

    # Interfaces
    BaseExtractor,
    BaseProcessor,
    BaseFormatter,
    BasePipeline,
)
```

Everything you need is in `core`. Import and build.
