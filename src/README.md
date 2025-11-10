# Source Code Directory

This directory contains all implementation code for the extraction tool.

## Structure

```
src/
├── core/           # ✓ Foundation (complete, frozen) - Data models and interfaces
├── extractors/     # ✓ DocxExtractor (Wave 1) - DOCX extraction production-ready
│                   # TODO: PDF, PPTX, XLSX extractors
├── processors/     # TODO - Content enrichment (context linking, metadata)
├── formatters/     # TODO - Output generation (JSON, Markdown, etc.)
├── infrastructure/ # TODO (Wave 2) - Config, logging, error handling, progress
├── pipeline/       # TODO - Orchestration and batch processing
└── cli/            # TODO - Command-line interface
```

## What Goes Where

### `core/` - Foundation ✓
**Status**: Complete and stable

Data models and interface contracts that all other modules use.

**Files**:
- `models.py` - All data structures (ContentBlock, ExtractionResult, etc.)
- `interfaces.py` - All base classes (BaseExtractor, BaseProcessor, etc.)
- `__init__.py` - Public API exports

**Do NOT modify** without discussion - changes affect all modules.

### `extractors/` - Format Handlers
**Status**: ✓ DocxExtractor complete (Wave 1)

One extractor per file format. Each implements `BaseExtractor`.

**Pattern**:
```python
# src/extractors/docx_extractor.py
from core import BaseExtractor, ExtractionResult

class DocxExtractor(BaseExtractor):
    def extract(self, file_path: Path) -> ExtractionResult:
        # DOCX-specific extraction logic
        pass
```

**Complete**: ✓ DocxExtractor (367 lines, production-ready)
**TODO**: PdfExtractor, PptxExtractor, ExcelExtractor

**Files**:
- `docx_extractor.py` - Word document extraction
- `__init__.py` - Package exports

**Test**: `python test_docx_extractor.py` (root level)

### `processors/` - Content Enrichment
**Status**: Not yet created

Processors that enrich extracted content. Each implements `BaseProcessor`.

**Pattern**:
```python
# src/processors/context_linker.py
from core import BaseProcessor, ProcessingResult

class ContextLinker(BaseProcessor):
    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        # Build document structure tree
        pass
```

**Examples**: ContextLinker, MetadataAggregator, QualityValidator

### `formatters/` - Output Generation
**Status**: Not yet created

Formatters that convert to AI-ready formats. Each implements `BaseFormatter`.

**Pattern**:
```python
# src/formatters/json_formatter.py
from core import BaseFormatter, FormattedOutput

class JsonFormatter(BaseFormatter):
    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        # Convert to JSON
        pass
```

**Examples**: JsonFormatter, MarkdownFormatter, ChunkedTextFormatter

### `infrastructure/` - Shared Infrastructure
**Status**: TODO (Wave 2 priority)

Shared configuration, logging, error handling, and progress tracking.

**Files** (planned):
- `config_manager.py` - Centralized configuration (YAML/JSON)
- `logging_framework.py` - Structured logging with performance timing
- `error_handler.py` - Standard error codes and categories
- `progress_tracker.py` - Progress reporting for long operations

**Need**: Identified in Wave 1 spike (see `INFRASTRUCTURE_NEEDS.md`)

### `pipeline/` - Orchestration
**Status**: Simple demo ✓, Full pipeline TODO

Pipeline coordination and batch processing.

**Files**:
- `../examples/simple_pipeline.py` - Simple demo (Wave 1) ✓
- `pipeline.py` - Main extraction pipeline (implements `BasePipeline`) TODO
- `batch_processor.py` - Parallel file processing TODO
- `resource_manager.py` - Memory and resource management TODO

### `cli/` - User Interface
**Status**: Not yet created

Command-line interface for end users.

**Files**:
- `main.py` - CLI entry point
- `commands.py` - Command implementations (extract, batch, config)
- `progress.py` - Progress display and reporting

## Guidelines

### Adding New Modules

1. **Choose correct directory** based on module type
2. **Import from core**: `from core import BaseExtractor, ...`
3. **Implement required interface** (BaseExtractor, BaseProcessor, or BaseFormatter)
4. **Follow naming convention**: `{format}_extractor.py`, `{name}_processor.py`, `{format}_formatter.py`
5. **Add docstrings** to all classes and public methods
6. **Use type hints** for all function signatures

### Module Independence

Modules within a directory should be **independent**:
- `docx_extractor.py` doesn't import from `pdf_extractor.py`
- All shared code goes in `core/` or a new `utils/` directory
- Extractors only depend on `core/`

### Testing

Each module should have corresponding tests in `tests/`:
```
tests/
├── test_extractors/
│   ├── test_docx_extractor.py
│   └── test_pdf_extractor.py
├── test_processors/
└── test_formatters/
```

## Quick Reference

**See**: `../QUICK_REFERENCE.md` for API syntax
**See**: `../GETTING_STARTED.md` for development workflow
**See**: `../FOUNDATION.md` for architecture details
