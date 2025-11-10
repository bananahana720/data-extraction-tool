# Core Foundation Module

The foundation that everything else builds on.

**Status**: Complete ✓ | Stable | Immutable

## Purpose

This module defines:
1. **Data Models** - Universal data structures all modules use
2. **Interface Contracts** - Rules for how modules interact

**Get these right, and everything else becomes modular and composable.**

## Files

### `models.py` - Data Structures

All data models used throughout the system.

**Key Models**:
- `ContentBlock` - Atomic unit of content (the building block)
- `ExtractionResult` - Output from extractors
- `ProcessingResult` - Output from processors
- `FormattedOutput` - Output from formatters
- `PipelineResult` - Complete pipeline execution result

**Supporting Models**:
- `Position` - Location tracking (page, slide, coordinates)
- `DocumentMetadata` - Document-level information
- `ImageMetadata` - Image asset metadata
- `TableMetadata` - Table structure metadata

**Enums**:
- `ContentType` - Types of content blocks
- `ProcessingStage` - Pipeline stages

**All models are immutable** (frozen dataclasses).

### `interfaces.py` - Base Classes

Abstract base classes that define module contracts.

**Interfaces**:
- `BaseExtractor` - Contract for format extractors
- `BaseProcessor` - Contract for content processors
- `BaseFormatter` - Contract for output formatters
- `BasePipeline` - Contract for pipeline orchestrators

**Each interface defines**:
- Required methods (abstract)
- Optional methods (with default implementations)
- Expected behavior (via docstrings)

### `__init__.py` - Public API

Exports the public API:
```python
from core import (
    ContentBlock, ContentType, ExtractionResult,
    BaseExtractor, BaseProcessor, BaseFormatter
)
```

Everything else is private implementation.

## Design Principles

### Immutability

All models are **frozen dataclasses** - cannot be modified after creation.

```python
# ✓ CORRECT
new_block = ContentBlock(
    block_id=old.block_id,
    metadata={**old.metadata, "new": "value"}
)

# ✗ WRONG
old.metadata["new"] = "value"  # FrozenInstanceError!
```

**Why**: Prevents accidental mutations, makes data flow traceable, catches bugs early.

### Type Safety

Full type hints on all functions and classes.

```python
def extract(self, file_path: Path) -> ExtractionResult:
    # Type checker knows exact types
```

**Why**: Catches errors at development time, not runtime.

### Clear Contracts

Interfaces define exactly what's required vs. optional.

```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> ExtractionResult:
        """Required: must implement"""
        pass

    def supports_streaming(self) -> bool:
        """Optional: override if needed"""
        return False
```

**Why**: No guessing what needs to be implemented.

## Usage Patterns

### Creating Content Blocks

```python
from uuid import uuid4
from core import ContentBlock, ContentType, Position

block = ContentBlock(
    block_id=uuid4(),
    block_type=ContentType.PARAGRAPH,
    content="Text content",
    position=Position(page=1, sequence_index=0),
    metadata={"word_count": 2},
    confidence=0.95
)
```

### Building Extraction Results

```python
from core import ExtractionResult, DocumentMetadata

result = ExtractionResult(
    content_blocks=(block1, block2, block3),
    document_metadata=DocumentMetadata(
        source_file=Path("doc.pdf"),
        file_format="pdf",
        word_count=1000
    ),
    success=True
)
```

### Implementing an Extractor

```python
from core import BaseExtractor, ExtractionResult

class MyExtractor(BaseExtractor):
    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix == ".txt"

    def extract(self, file_path: Path) -> ExtractionResult:
        # Extraction logic
        return ExtractionResult(success=True, ...)
```

## Modification Policy

### ⚠️ Changes to Core Require Discussion

Changes to this module affect **all** other modules:
- Changing `ContentBlock` affects extractors, processors, formatters
- Changing interfaces breaks implementations
- Adding required methods breaks existing modules

**Before modifying**:
1. Discuss with team/user
2. Document rationale
3. Plan migration for existing code
4. Update all documentation

### ✓ Safe Extensions

These changes are safe:
- Adding new `ContentType` enum values
- Adding new optional fields to models (with defaults)
- Adding new optional methods to interfaces
- Extending `metadata` dict usage

### Prefer Extension Over Modification

Use the `metadata` dict to extend without breaking:

```python
# ✓ GOOD: Extend via metadata
block = ContentBlock(
    content="text",
    metadata={
        "custom_field": "value",
        "format_specific": {...}
    }
)

# ✗ BAD: Modify core model
# (Requires changing ContentBlock definition)
```

## Testing

Foundation must always pass tests:

```bash
python examples/minimal_extractor.py  # Must show [SUCCESS]
python examples/minimal_processor.py  # Must show [SUCCESS]
```

If these fail, foundation is broken.

## Documentation

Complete documentation in:
- **`../../FOUNDATION.md`** - Architecture and design decisions
- **`../../QUICK_REFERENCE.md`** - API usage examples
- **Docstrings** - Every class and public method documented

## Version History

### v1.0 (2025-10-29) - Initial Foundation
- Data models defined and frozen
- Interface contracts established
- Examples validated
- Documentation complete

**Status**: Stable, ready for use

---

**Remember**: This is the foundation. Stability here enables velocity everywhere else.
