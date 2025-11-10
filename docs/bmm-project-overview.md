# Project Overview - AI Data Extractor for RAG-Optimized Knowledge Curation

**Generated**: 2025-11-07
**Project Type**: CLI Tool / Data Processing Pipeline
**Status**: Production (v1.0.6) + Enhancement Planning
**Primary Language**: Python 3.11/3.12

---

## Executive Summary

This project is an **enterprise-grade document extraction and processing pipeline** designed for RAG (Retrieval-Augmented Generation) optimization and AI-ready knowledge curation. Currently in production with v1.0.6, the tool extracts structured content from enterprise documents (DOCX, PDF, PPTX, XLSX, CSV, TXT) with comprehensive table and image preservation.

**Key Capabilities (Current)**:
- Multi-format document extraction (6 extractors)
- Hierarchical content processing (3 processors)
- Multiple output formats (JSON, Markdown, Chunked Text)
- Production-ready CLI with batch processing
- 92%+ test coverage, 82.7% test pass rate
- 100% success rate on real-world enterprise documents

**Strategic Enhancement Goals**:
The project is positioned for two major enhancement journeys:

**Journey A - RAG Optimization**: Handle RAG pipeline issues with images, document objects, comments, annotations, and scanned PDFs. Enable toggleable pre-processing for semantic standardization, context chunking, file consolidation, schema standardization, and quality indicators.

**Journey B - Semantic Analysis Integration**: Add NLP optimization capabilities for knowledge base curation using semantic analysis libraries (automated or interactive via CLI). Target domain: Cybersecurity internal audit with highly structured entities (processes, risks, controls, regulations, policies, GRC platform integration).

---

## Project Classification

### Repository Structure
- **Type**: Monolith (single cohesive codebase)
- **Architecture Pattern**: Layered Pipeline Architecture with Strategy Pattern
- **Modularity**: Plugin-based extractors, processors, and formatters

### Technology Stack Summary

| Category | Technologies | Purpose |
|----------|-------------|----------|
| **Runtime** | Python 3.11/3.12 | Core execution environment |
| **CLI** | Click 8.1.0+, Rich 13.0.0+ | Command-line interface and terminal UI |
| **Document Processing** | python-docx, pypdf, pdfplumber, python-pptx, openpyxl | Format-specific extraction |
| **Configuration** | Pydantic 2.0+, PyYAML 6.0+ | Config validation and parsing |
| **OCR** | pytesseract, pdf2image, Pillow | Optical character recognition (optional) |
| **Testing** | pytest 7.4.0+, pytest-cov, pytest-mock | Test framework and coverage |
| **Quality** | black 23.0+, ruff 0.1.0+, mypy 1.5+ | Code formatting, linting, type checking |

### Project Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Production Version** | v1.0.6 | ✅ Deployed |
| **Modules** | 26/24 (108% MVP) | ✅ Complete |
| **Extractors** | 6 formats | ✅ DOCX, PDF, PPTX, XLSX, CSV, TXT |
| **Processors** | 3 (ContextLinker, MetadataAggregator, QualityValidator) | ✅ Complete |
| **Formatters** | 3 (JSON, Markdown, ChunkedText) | ✅ Complete |
| **Test Suite** | 1,016 tests | ⚠️ 82.7% passing |
| **Test Coverage** | 92%+ overall | ✅ Exceeds target |
| **Documentation** | 115+ markdown files | ✅ Comprehensive |
| **ADR Compliance** | 94-95/100 | ✅ Excellent |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Layer (Click + Rich)                 │
│  - Commands: extract, batch, version, config                │
│  - Progress display with ETA                                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Pipeline Orchestration Layer                   │
│  - ExtractionPipeline: Coordinates end-to-end flow          │
│  - BatchProcessor: Parallel multi-file processing           │
│  - Format detection and routing                             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 Extraction Layer                            │
│  6 Format-Specific Extractors (BaseExtractor interface):   │
│  - DocxExtractor: Word documents (tables + images)          │
│  - PdfExtractor: PDFs with OCR fallback                     │
│  - PptxExtractor: PowerPoint (images + speaker notes)       │
│  - ExcelExtractor: Excel multi-sheet workbooks              │
│  - CsvExtractor: CSV/TSV with auto-detection                │
│  - TxtExtractor: Plain text files                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ExtractionResult
                  (ContentBlocks + Media)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Processing Chain Layer                     │
│  3 Ordered Processors (BaseProcessor interface):            │
│  1. ContextLinker: Build document hierarchy                 │
│  2. MetadataAggregator: Compute statistics                  │
│  3. QualityValidator: Score extraction quality              │
│  **INTEGRATION POINT**: Semantic analysis would fit here    │
└────────────────────────┬────────────────────────────────────┘
                         │
                   ProcessingResult
                  (Enriched ContentBlocks)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Output Formatting Layer                    │
│  3 Parallel Formatters (BaseFormatter interface):           │
│  - JsonFormatter: Hierarchical JSON                         │
│  - MarkdownFormatter: Human-readable Markdown               │
│  - ChunkedTextFormatter: Token-limited AI chunks            │
└─────────────────────────────────────────────────────────────┘

         ═════════════════════════════════════════════
              Cross-Cutting Infrastructure Layer
         ═════════════════════════════════════════════
         - ConfigManager: YAML/JSON config with Pydantic
         - LoggingFramework: Structured JSON logging
         - ErrorHandler: 50+ error codes with recovery
         - ProgressTracker: Real-time progress tracking
```

---

## Key Design Patterns

### 1. **Strategy Pattern** (Pluggable Components)
- **Extractors**: Each format implements `BaseExtractor` interface
- **Processors**: Each processor implements `BaseProcessor` interface
- **Formatters**: Each formatter implements `BaseFormatter` interface
- **Benefit**: Add new formats/processors/formatters without modifying core pipeline

### 2. **Pipeline Pattern** (Staged Processing)
- **Flow**: File → Extract → Process → Format → Output
- **Immutability**: Each stage creates new data structures (no mutations)
- **Error Handling**: Graceful degradation at each stage

### 3. **Dependency Injection** (Configurability)
- Pipeline accepts registered components
- Configuration via constructor injection
- Infrastructure components injected throughout

### 4. **Topological Sorting** (Processor Ordering)
- Processors declare dependencies via `get_dependencies()`
- Pipeline automatically orders processors using Kahn's algorithm
- Prevents circular dependencies at runtime

---

## Integration Points for Semantic Analysis

### Recommended Integration Location: New Processor

**Why as a Processor?**
1. Processors are designed for content enrichment (perfect for semantic analysis)
2. Automatic dependency ordering (can depend on ContextLinker, MetadataAggregator)
3. Access to both content blocks and document hierarchy
4. Infrastructure support (logging, error handling, progress)
5. Optional/required flexibility via `is_optional()` flag

**Example Semantic Processor Structure**:
```python
class SemanticAnalyzer(BaseProcessor):
    def get_processor_name(self) -> str:
        return "SemanticAnalyzer"

    def get_dependencies(self) -> list[str]:
        # Run after context linking and metadata aggregation
        return ["ContextLinker", "MetadataAggregator"]

    def is_optional(self) -> bool:
        return True  # Don't block pipeline if semantic analysis fails

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        # Semantic analysis logic here:
        # - Entity extraction (processes, risks, controls, regulations)
        # - Relationship mapping (GRC entities)
        # - Semantic standardization
        # - Context enrichment
        # - Quality indicators
        pass
```

### Available Data at Processing Stage

When a semantic processor runs, it has access to:

**Content Blocks** (via `ExtractionResult.content_blocks`):
- `block_type`: ContentType enum (HEADING, PARAGRAPH, TABLE, LIST, etc.)
- `content`: Extracted text content
- `raw_content`: Original unprocessed content
- `position`: Page number and sequence index
- `metadata`: Dictionary with:
  - `depth`: Hierarchical depth (from ContextLinker)
  - `document_path`: List of parent headings (breadcrumb trail)
  - `word_count`: Words in block (from MetadataAggregator)
  - `char_count`: Character count
  - `level`: Heading level (for HEADING blocks)
  - Custom metadata per block type

**Document Metadata** (via `ExtractionResult.document_metadata`):
- `source_file`: Original file path
- `file_size_bytes`: File size
- `title`, `author`, `created_date`, `modified_date`: Document properties
- `page_count`: Number of pages
- `extraction_metadata`: Extractor-specific metadata

**Media Assets**:
- `images`: List of ImageMetadata (format, dimensions, binary data)
- `tables`: List of TableMetadata (rows, columns, headers)

**Stage Metadata** (from previous processors):
```python
{
    # From ContextLinker
    "blocks_processed": 245,
    "heading_count": 28,
    "max_depth": 4,

    # From MetadataAggregator
    "total_words": 5234,
    "total_characters": 32456,
    "average_words_per_block": 21.3,
    "content_type_distribution": {"heading": 28, "paragraph": 180, ...},
    "summary": {"headings": ["Chapter 1", "Section 1.1", ...]}
}
```

### Alternative Integration: Custom Formatter

**For RAG-specific output formats**:
- Create `RagOptimizedFormatter(BaseFormatter)`
- Implements semantic chunking with overlap
- Adds embeddings metadata
- Preserves context boundaries
- Outputs RAG-ready JSON schema

---

## Development Workflow for New Features

### Adding a New Processor (e.g., Semantic Analyzer)

**Step 1: Create Processor Module**
```bash
# File: src/processors/semantic_analyzer.py
from core import BaseProcessor, ExtractionResult, ProcessingResult
```

**Step 2: Implement Base Interface**
```python
class SemanticAnalyzer(BaseProcessor):
    def get_processor_name(self) -> str:
        return "SemanticAnalyzer"

    def get_dependencies(self) -> list[str]:
        return ["ContextLinker", "MetadataAggregator"]  # Run after these

    def is_optional(self) -> bool:
        return True  # Don't block pipeline on failure

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        # Implement semantic analysis logic
        enriched_blocks = []
        for block in extraction_result.content_blocks:
            # Analyze block content
            entities = self._extract_entities(block.content)
            semantic_tags = self._classify_content(block.content)

            # Enrich metadata
            enriched_metadata = {
                **block.metadata,
                "entities": entities,
                "semantic_tags": semantic_tags,
                "domain_classification": "cybersecurity_audit"
            }

            # Create enriched block
            enriched_block = ContentBlock(..., metadata=enriched_metadata)
            enriched_blocks.append(enriched_block)

        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            document_metadata=extraction_result.document_metadata,
            images=extraction_result.images,
            tables=extraction_result.tables,
            processing_stage=ProcessingStage.SEMANTIC_ANALYSIS,  # New stage
            stage_metadata={"entities_found": len(entities), ...},
            success=True
        )
```

**Step 3: Register with Pipeline**
```python
# In src/pipeline/__init__.py or CLI setup
from processors import ContextLinker, MetadataAggregator, QualityValidator, SemanticAnalyzer

pipeline = ExtractionPipeline()
pipeline.add_processor(ContextLinker())
pipeline.add_processor(MetadataAggregator())
pipeline.add_processor(SemanticAnalyzer())  # Automatically ordered after dependencies
pipeline.add_processor(QualityValidator())
```

**Step 4: Configure via YAML**
```yaml
# config.yaml
processors:
  semantic_analyzer:
    enabled: true
    entity_extraction: true
    domain_model: "cybersecurity_audit"
    grc_entities:
      - processes
      - risks
      - controls
      - regulations
      - policies
    confidence_threshold: 0.7
```

**Step 5: Test**
```python
# tests/test_processors/test_semantic_analyzer.py
def test_semantic_analyzer_extracts_entities():
    analyzer = SemanticAnalyzer(config={"entity_extraction": True})
    result = analyzer.process(extraction_result)

    assert result.success
    assert "entities" in result.content_blocks[0].metadata
```

### Configuration Integration

**Infrastructure Support Available**:
- `ConfigManager`: Thread-safe config access with Pydantic validation
- `LoggingFramework`: Structured logging with correlation IDs
- `ErrorHandler`: Standardized error handling with recovery patterns
- `ProgressTracker`: Real-time progress updates

**Example Configuration Schema**:
```python
from pydantic import BaseModel

class SemanticAnalyzerConfig(BaseModel):
    enabled: bool = True
    entity_extraction: bool = True
    semantic_standardization: bool = True
    context_chunking: bool = False
    chunk_size: int = 512
    chunk_overlap: int = 50
    domain_model: str = "general"
    confidence_threshold: float = 0.7
```

---

## Current Limitations & Enhancement Opportunities

### For Journey A (RAG Optimization)

**Current State**:
- ✅ Tables and images extracted and preserved
- ✅ Multi-format support (6 extractors)
- ✅ Hierarchical context available
- ⚠️ No semantic standardization
- ⚠️ No context chunking with overlap
- ⚠️ No schema standardization
- ⚠️ No RAG-specific quality indicators

**Enhancement Path**:
1. Create `RagOptimizationProcessor` or `RagOptimizedFormatter`
2. Add semantic standardization rules
3. Implement context-aware chunking
4. Add RAG quality metrics
5. Create RAG-optimized output schema

### For Journey B (Semantic Analysis)

**Current State**:
- ✅ Pipeline architecture supports new processors
- ✅ Dependency-ordered processing
- ✅ Hierarchical document structure available
- ✅ Metadata aggregation framework
- ⚠️ No NLP library integration
- ⚠️ No entity extraction (placeholder in MetadataAggregator)
- ⚠️ No domain-specific classification
- ⚠️ No GRC entity recognition

**Enhancement Path**:
1. Add semantic analysis library dependencies (spaCy, NLTK, scikit-learn)
2. Create `SemanticAnalyzer` processor
3. Implement domain-specific entity extraction
4. Add GRC entity classification
5. Build relationship mapping
6. Create interactive CLI for configuration

### Constraints to Consider

**Hard Constraints**:
- Python 3.12 environment (enterprise restriction)
- No transformer-based LLMs (enterprise restriction on Gen AI)
- Must work without admin privileges

**Soft Constraints**:
- User is AI power user but lacks NLP background
- Automation + explanations preferred
- Future GUI consideration (currently CLI)

---

## Next Steps for Enhancement

### Immediate Actions

1. **Review Architecture Docs** (Priority 1):
   - Read `docs/bmm-pipeline-integration-guide.md` (this doc's companion)
   - Review `docs/architecture/FOUNDATION.md` for core interfaces
   - Study `docs/architecture/GETTING_STARTED.md` for development workflow

2. **Design Semantic Processor** (Priority 2):
   - Define entities for cybersecurity audit domain
   - Choose semantic analysis libraries (compatible with Python 3.12, no LLMs)
   - Design processor interface and configuration schema
   - Plan integration with existing processors

3. **Prototype & Test** (Priority 3):
   - Create proof-of-concept semantic analyzer
   - Test with real audit documents
   - Measure performance and quality
   - Iterate on entity extraction accuracy

### Strategic Planning

**BMad Method Workflow**:
- Current Status: `document-project` workflow ✅ COMPLETE
- Next Workflow: `brainstorm-project` (optional, recommended)
- Following: `research` → `prd` → `architecture` → `sprint-planning`

**Recommended Approach**:
1. Run brainstorming workflow to explore semantic analysis approaches
2. Research NLP libraries compatible with constraints
3. Create PRD defining Journey A and Journey B features
4. Design architecture for semantic analysis integration
5. Implement using TDD methodology (project standard)

---

## References

**Primary Documentation**:
- `docs/architecture/FOUNDATION.md` - Core data models and interfaces
- `docs/architecture/GETTING_STARTED.md` - Development workflow
- `docs/architecture/QUICK_REFERENCE.md` - API reference
- `docs/bmm-pipeline-integration-guide.md` - Pipeline deep dive (generated)
- `docs/bmm-processor-chain-analysis.md` - Processor analysis (generated)

**Project State**:
- `PROJECT_STATE.md` - Current status and metrics
- `README.md` - Project overview and quick start
- `DOCUMENTATION_INDEX.md` - Complete documentation navigation

**User Guide**:
- `docs/USER_GUIDE.md` - End-user documentation (1,400+ lines)
- `docs/QUICKSTART.md` - Quick start guide
- `INSTALL.md` - Installation instructions

**Infrastructure**:
- `docs/INFRASTRUCTURE_GUIDE.md` - Comprehensive developer guide
- `docs/CONFIG_GUIDE.md` - Configuration patterns
- `docs/LOGGING_GUIDE.md` - Logging framework usage
- `docs/ERROR_HANDLING_GUIDE.md` - Error handling patterns

---

**Document Status**: ✅ Complete | **Generated**: 2025-11-07 | **For**: BMM document-project workflow
