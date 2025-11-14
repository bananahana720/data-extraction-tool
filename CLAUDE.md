# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Data Extraction Tool** - Enterprise document processing pipeline for RAG workflows. Transforms messy corporate audit documents into AI-optimized outputs using a five-stage modular pipeline architecture.

**Status**: Epic 3 - Chunk & Output (in progress, Stories 3.1-3.2 complete)
**Python**: 3.12+ (mandatory enterprise requirement)
**Architecture**: `Extract → Normalize → Chunk → Semantic → Output`

## Core Architecture

### Five-Stage Pipeline Pattern

Each stage is a composable, testable component using frozen dataclasses and ABC interfaces:

1. **Extract** (`src/data_extract/extract/`) - Document format-specific extraction (PDF, DOCX, XLSX, PPTX, CSV, images+OCR)
2. **Normalize** (`src/data_extract/normalize/`) - Text cleaning, entity standardization
3. **Chunk** (`src/data_extract/chunk/`) - Semantic-aware chunking (spaCy-based)
4. **Semantic** (`src/data_extract/semantic/`) - Classical NLP analysis (TF-IDF, LSA - no transformers per enterprise constraints)
5. **Output** (`src/data_extract/output/`) - Multiple formats (JSON, TXT, CSV)

### Key Data Models (Immutable)

- `ExtractionResult` - Stage 1 output with content blocks
- `ContentBlock` - Individual unit (text/table/image) with type + position + metadata
- `ProcessingResult` - Stages 2-4 output, preserves structure
- `FormattedOutput` - Stage 5 final output

### Design Principles

- **Modularity**: Each stage independent, testable, replaceable
- **Immutability**: Frozen dataclasses prevent pipeline state mutations
- **Type Safety**: Full type hints + Pydantic v2 validation enforced by mypy
- **Interface-Based**: All modules implement ABCs (BaseExtractor, BaseProcessor, BaseFormatter)
- **Determinism**: Same input always produces same output

## Dual Codebase Structure

### Greenfield (New Modular Architecture)
`src/data_extract/` - Modern pipeline implementation following Epic-based development

### Brownfield (Existing Code)
`src/{cli,core,extractors,processors,formatters,infrastructure,pipeline}/` - Legacy code assessed and consolidated during Epic 1.

**Important**: Both systems coexist during migration. Don't break existing brownfield code.

## Development Commands

### Setup
```bash
# Windows (primary target)
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install

# macOS/Linux
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

### spaCy Model Setup (Required for Epic 3)

**Story 2.5.2** integrates spaCy 3.7.2+ for sentence boundary detection used in Epic 3 chunking.

```bash
# Download required language model (43MB, one-time setup)
python -m spacy download en_core_web_md

# Verify installation
python -m spacy validate

# Test in Python
python -c "import spacy; nlp = spacy.load('en_core_web_md'); print(f'Model loaded: {nlp.meta[\"version\"]}')"
```

**Performance**: Model loads in ~1.2 seconds, processes 4000+ words/second.

**CI/CD Caching**: spaCy models are automatically cached in CI (transparent to developers - no manual action needed).

**Troubleshooting**: See `docs/troubleshooting-spacy.md` for common issues.

### Testing (pytest with markers)
```bash
# Run all tests (includes 1000+ brownfield tests)
pytest

# With coverage
pytest --cov=src --cov-report=html

# By category
pytest -m unit              # Fast unit tests only
pytest -m integration       # Integration tests
pytest -m extraction        # Extraction-specific tests
pytest -m "not slow"        # Skip slow tests

# Specific test file/function
pytest tests/unit/test_extract/test_pdf.py
pytest tests/unit/test_extract/test_pdf.py::test_basic_extraction

# Debug mode
pytest --pdb tests/unit/test_name.py        # Drop to debugger on failure
pytest -vv --showlocals tests/unit/test.py  # Verbose with variables
pytest -s tests/unit/test.py                 # Show print statements

# Parallel execution
pytest -n auto
```

**Test Markers**: `unit`, `integration`, `extraction`, `processing`, `formatting`, `chunking`, `pipeline`, `cli`, `slow`, `performance`

### CI/CD Pipeline

See `docs/ci-cd-pipeline.md` for complete CI/CD documentation.

**Quick validation before push**:
```bash
pre-commit run --all-files  # Runs all quality checks
```

**Performance testing**:
```bash
pytest tests/performance/ -v  # Run performance benchmarks locally
```

### Code Quality (Enforced by Pre-commit)
```bash
# Format code (100 char line length)
black src/ tests/

# Lint code (modern, fast replacement for flake8)
ruff check src/ tests/

# Type check (strict mode, excludes brownfield)
mypy src/data_extract/

# Run all pre-commit hooks manually
pre-commit run --all-files
```

**Pre-commit Enforcement**: Pre-commit hooks run automatically on `git commit` AND are validated in CI. This ensures consistency between local development and CI environments. Always run `pre-commit run --all-files` before pushing to catch issues early. CI will fail if pre-commit checks don't pass.

### CLI Entry Point
```bash
data-extract    # Typer-based CLI (full implementation in Epic 5)
```

## Testing Strategy

### Organization
Tests mirror `src/` structure exactly:
- `tests/unit/` - Fast, isolated tests
- `tests/integration/` - Multi-component, end-to-end
- `tests/performance/` - Benchmarks and stress tests
- `tests/fixtures/` - Shared test data

### Coverage Requirements
- Baseline: >60% overall (enforced in CI, includes brownfield code)
- Greenfield (`src/data_extract/`): >80% coverage
- Epic 5 critical paths: >90% coverage

### Key Patterns
- Use pytest fixtures for test data (see `tests/conftest.py`)
- Use markers for selective execution
- Mirror src/ structure exactly (e.g., `tests/unit/test_extract/test_pdf.py` mirrors `src/data_extract/extract/pdf.py`)
- Include integration and performance tests for all stages

## Code Conventions

### Style (Enforced by Tools)
- **Formatting**: Black (100 char lines, target Python 3.12)
- **Linting**: Ruff (replaces flake8 + isort)
- **Type Checking**: Mypy strict mode (excludes brownfield during migration)

### Naming
- Classes: `PascalCase` (e.g., `DocxExtractor`)
- Functions/methods: `snake_case` (e.g., `extract_content`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CHUNK_SIZE`)
- Modules: `snake_case` (e.g., `context_linker.py`)

### Required
- Type hints on all public functions
- Google-style docstrings for public APIs
- Tests for all new functionality
- Pre-commit compliance (black, ruff, mypy must pass)

## Epic-Based Development

### Completed
- **Epic 1**: Foundation (4 stories complete)
- **Epic 2**: Extract & Normalize stages (6 stories complete)
- **Epic 2.5**: Infrastructure & optimization (6 stories complete)

### Current: Epic 3 - Chunk & Output
- ✅ Story 3.1: Semantic boundary-aware chunking engine (complete)
- ✅ Story 3.2: Entity-aware chunking (complete)
- 📋 Stories 3.3-3.7: Metadata, output formats, configuration (backlog)

### Upcoming
- **Epic 4**: Semantic analysis stage
- **Epic 5**: CLI, batch processing, configuration cascade

See `docs/sprint-status.yaml` and `docs/stories/` for detailed specifications.

## Configuration (Epic 5)

Four-tier precedence cascade (planned for Epic 5):
1. CLI flags (highest)
2. Environment variables (`DATA_EXTRACT_*` prefix)
3. YAML config file (`~/.data-extract/config.yaml` or project-local)
4. Hardcoded defaults (lowest)

## Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| CLI | Typer | Type-safe, modern, minimal boilerplate |
| UI | Rich | Industry-standard progress bars |
| Data Models | Pydantic v2 | Runtime validation, schema generation |
| PDF | PyMuPDF | Fast, handles native + OCR fallback |
| Office | python-docx, openpyxl, python-pptx | Mature, standard libraries |
| OCR | pytesseract | Tesseract wrapper with confidence scores |
| Chunking | spaCy | Production-ready sentence boundaries |
| Semantic | scikit-learn | TF-IDF, LSA, cosine similarity |
| Advanced NLP | gensim | Word2Vec, LDA (optional) |
| Quality | textstat | Readability metrics |
| Logging | structlog | Structured JSON for audit trails |
| Testing | pytest | Industry standard with rich ecosystem |
| Type Checking | mypy | Static analysis, gradual typing |
| Linting | ruff | Fast, modern, replaces flake8 |

**Enterprise Constraint**: Classical NLP only - no transformer models allowed.

## Epic 3: Chunking Engine

Epic 3 implements semantic boundary-aware chunking that transforms normalized text into RAG-optimized chunks while preserving document structure and entity context.

### Entity-Aware Chunking (Story 3.2)

Story 3.2 adds entity-aware boundary adjustment to prevent splitting entity definitions across chunks.

**EntityPreserver Integration:**
- `analyze_entities()`: Maps Epic 2 entities to EntityReference objects with positions
- `find_entity_gaps()`: Identifies safe split zones between entity boundaries
- `detect_entity_relationships()`: Finds relationship patterns (e.g., "RISK-001 mitigated by CTRL-042")

**How it works:**
1. ChunkingEngine analyzes entities at document start (when `entity_aware=True`)
2. During chunk generation, when target size reached, engine calls `find_entity_gaps()`
3. Engine searches for nearest gap within ±20% of chunk_size to adjust boundary
4. If suitable gap found, boundary shifts to preserve entity completeness
5. Entities marked as `is_partial=True` if split is unavoidable (e.g., entity > chunk_size)

**Preservation rate:** >95% of entities kept intact within single chunks (AC-3.2-1).

### ChunkingEngine Usage Patterns

**Basic Usage:**
```python
from data_extract.chunk import ChunkingEngine, ChunkingConfig

# Initialize engine with default configuration
config = ChunkingConfig(
    chunk_size=512,      # Target tokens per chunk (128-2048)
    overlap_pct=0.15     # 15% overlap between chunks (0.0-0.5)
)
engine = ChunkingEngine(config)

# Chunk a ProcessingResult
from data_extract.core.models import ProcessingResult
result = ProcessingResult(...)  # From normalize stage
chunks = engine.chunk(result)   # Returns List[Chunk]
```

**Streaming Large Documents:**
```python
# Memory-efficient streaming using generator
for chunk in engine.chunk(result):
    # Process chunk immediately (constant memory)
    output_writer.write_chunk(chunk)
```

**Configuration Options:**
```python
config = ChunkingConfig(
    chunk_size=1024,       # Larger chunks for dense content
    overlap_pct=0.25,      # Higher overlap preserves more context
    respect_sentences=True # Always enabled (semantic boundaries)
)
```

### Chunk Configuration Reference

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `chunk_size` | 128-2048 tokens | 512 | Target chunk size (may exceed for long sentences) |
| `overlap_pct` | 0.0-0.5 | 0.15 | Overlap between chunks (0% = no overlap, 50% = max) |
| `respect_sentences` | N/A | True | Always respects sentence boundaries (spaCy-based) |

**Key Behaviors:**
- **Semantic Boundaries:** Chunks never split mid-sentence (uses spaCy sentence segmentation)
- **Long Sentences:** Sentences >chunk_size become single chunks (preserves context)
- **Metadata Preservation:** Each chunk includes source file, position, entity tags, quality scores
- **Memory Efficiency:** Generator-based streaming (constant memory across batch sizes)

**Performance Characteristics:**
- **Latency:** ~0.19s per 1,000 words (linear scaling)
- **Memory:** 255 MB peak for 10k-word document (51% of 500 MB limit)
- **Throughput:** ~5,000 words/second (including spaCy segmentation)

See `docs/performance-baselines-epic-3.md` for detailed performance baselines.

### Quality Gates

**Pre-commit workflow** (0 violations required):
1. `black src/ tests/` → Fix formatting
2. `ruff check src/ tests/` → Fix linting
3. `mypy src/data_extract/` → Fix type violations (run from project root)
4. Run tests → Fix failures
5. Commit clean code

**Key Patterns**:
- Fix validation issues immediately (don't defer tech debt)
- Always include integration tests (catch memory/NFR issues)
- Profile before optimizing (establish baselines first)
- Document architectural decisions as you go

## Common Tasks

### Adding a New Extractor
1. Create `src/data_extract/extract/{format}.py`
2. Implement `BaseExtractor` ABC
3. Add tests in `tests/unit/test_extract/test_{format}.py`
4. Register in pipeline's `FORMAT_EXTENSIONS` mapping
5. Update documentation

### Adding a New Processing Stage
1. Define stage interface in `src/data_extract/core/`
2. Implement processor in appropriate module
3. Add unit tests with fixtures
4. Add integration tests with sample documents
5. Wire into pipeline configuration

### Running Specific Test Suites
```bash
# All extraction tests
pytest -m extraction

# PDF extraction only
pytest tests/unit/test_extract/test_pdf.py

# Integration tests for entire pipeline
pytest -m integration tests/integration/test_pipeline.py
```

### UAT Workflows (Story Validation)

4-stage pipeline for systematic acceptance criteria validation:

```bash
workflow create-test-cases      # Generate test specs from story ACs
workflow build-test-context     # Assemble test infrastructure context
workflow execute-tests          # Run automated/CLI/manual tests
workflow review-uat-results     # QA review with approval decision
```

**Output locations**: `docs/uat/{test-cases,test-context,test-results,reviews}/`

**Full documentation**: See `docs/tech-spec-epic-2.5.md` (UAT Framework section) and workflow-specific docs in `bmad/bmm/workflows/`.

**Windows users**: CLI tests require tmux (WSL only). See `docs/uat/tmux-cli-windows-setup.md`.

## Key Architecture Decisions

- **ADR-001**: Immutable models prevent pipeline state corruption
- **ADR-002**: Pluggable extractors isolate format-specific logic
- **ADR-003**: ContentBlocks preserve document structure over raw text
- **ADR-004**: Classical NLP only (enterprise constraint - no transformers)
- **ADR-005**: Gradual brownfield modernization (don't break production)
- **ADR-011**: Semantic boundary-aware chunking (respects sentence boundaries via spaCy)

See `docs/architecture.md` for full details.

## Documentation References

- `docs/architecture.md` - Technical architecture and ADRs
- `docs/PRD.md` - Product requirements and vision
- `docs/sprint-status.yaml` - Current development status (authoritative source)
- `docs/tech-spec-epic-*.md` - Epic technical specifications
- `docs/stories/` - Story-level implementation specs
- `docs/performance-baselines-epic-*.md` - Performance benchmarks
- `pyproject.toml` - Project configuration and dependencies
- `.pre-commit-config.yaml` - Code quality hooks

## Important Notes

### Search Tools
**Always use ripgrep (rg), never grep**. The tool is configured to use rg for performance.

### Brownfield Code
Existing code in `src/{cli,extractors,processors,formatters,core,pipeline,infrastructure}/` has been assessed (Epic 1). Both brownfield and greenfield systems coexist. Don't break existing brownfield code during migration.

### Type Checking Exclusions
Mypy excludes brownfield packages during migration (see `pyproject.toml` `[tool.mypy]` section). New code in `src/data_extract/` must pass strict type checking.

### Testing Philosophy
- Tests mirror source structure exactly
- Use markers for selective execution
- Coverage requirements increase by epic
- Integration tests validate end-to-end workflows
- Performance tests catch regressions early

### Error Handling
Pipeline uses "continue-on-error" pattern - graceful degradation per file. Don't fail entire batch on single document error.
