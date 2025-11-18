# CLAUDE.md

**[TMUX-CLI and TMUX Use Instructions - GAMECHANGER IN AI AGENTIC CODING](tmux-cli-instructions.md)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Data Extraction Tool** - Enterprise document processing pipeline for RAG workflows. Transforms messy corporate audit documents into AI-optimized outputs using a five-stage modular pipeline architecture.

**Status**: Epic 3 - Chunk & Output (COMPLETE - all 7 stories done)
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
- ✅ Story 3.3: Chunk metadata and quality scoring (complete)
- ✅ Story 3.4: JSON output format with full metadata (complete)
- ✅ Story 3.5: Plain text output format for LLM upload (complete)
- ✅ Story 3.6: CSV output format for analysis and tracking (complete)
- ✅ Story 3.7: Configurable output organization strategies (complete)

### Upcoming
- **Epic 4**: Semantic analysis stage
- **Epic 5**: CLI, batch processing, configuration cascade

See `docs/sprint-status.yaml` and `docs/stories/` for detailed specifications.

## Lessons & Reminders (Epics 1-3)

Consolidated critical lessons from retrospectives to prevent repeating past mistakes.

### Story Development

- **Fill AC evidence table BEFORE marking review status** - AC matrices with test locations and perf numbers
- **Include BOM/logging/CLI wiring sections** - Never omit provenance, metadata, or integration points
- **Document Debug Log during implementation** - Write brief plan, capture approaches and decisions
- **Update File List immediately** - Track every changed file as you work, not retrospectively
- **Verify all tasks/subtasks checked [x]** - Story isn't complete if any checkbox remains [ ]

### Code Quality

- **Run Black → Ruff → Mypy BEFORE marking task complete** - Never defer quality gate fixes
- **Fix violations immediately when discovered** - Don't accumulate tech debt
- **mypy must run from project root** - Use `mypy src/data_extract/` not relative paths
- **Zero violations required for greenfield** - `src/data_extract/` must be clean
- **Brownfield violations tracked separately** - Don't mix legacy issues with new code

### Testing

- **Mirror src/ structure exactly** - `tests/unit/test_extract/` mirrors `src/data_extract/extract/`
- **Write integration tests for NFR validation** - Memory, throughput, latency must be measured
- **Coverage targets: 80% greenfield, 60% overall** - Enforce in CI, measure before claiming done
- **Use Path(__file__).parent for fixtures** - Never hardcode relative paths like `tests/fixtures/`
- **Test edge cases comprehensively** - Boundary values, error conditions, missing data

### Documentation

- **ADRs need owners and deadlines** - Documentation is a deliverable, not "nice to have"
- **Performance baselines required for optimization claims** - Measure first, optimize second
- **CLAUDE.md is for essential guidance only** - Keep under 100 lines per section, link to detailed docs
- **Retrospectives capture action items** - Track completion in sprint-status.yaml
- **README files only when explicitly requested** - Don't create documentation proactively

### Architecture

- **Protocol-based design > ABC inheritance** - PipelineStage pattern scales without friction
- **Continue-on-error for batch processing** - ProcessingError (recoverable) vs CriticalError (halt)
- **Adapter pattern for brownfield integration** - Wrap legacy code, don't modify it
- **Profile-driven optimization** - cProfile data beats assumptions every time
- **Validate architecture BEFORE implementation** - Confirm brownfield vs greenfield usage upfront

### Process

- **Automation > Memory** - Encode guidelines in scripts so they can't be skipped
- **Code review cycles are teaching moments** - First 2-3 stories have more findings, that's expected
- **Bridge epics prevent downstream blockers** - 1-2 day infrastructure investment saves week of debugging
- **UAT framework for systematic validation** - Use create-test-cases → execute-tests → review workflows
- **Sprint status is authoritative** - Update immediately when story status changes

## Development Automation Tools (Epic 3.5)

Production-ready automation scripts that enforce quality and accelerate development.

### P0 Scripts (Priority Zero - Essential)

#### 1. Story Template Generator
**Location:** `scripts/generate_story_template.py`
**Purpose:** Generate complete story markdown with all required sections
**Benefits:** 60% token reduction, 75% faster story creation, prevents omitted sections

```bash
# Basic usage
python scripts/generate_story_template.py \
  --story-number 4.1 \
  --epic 4 \
  --title "TF-IDF Vectorization Engine" \
  --owner Charlie \
  --estimate 8

# Advanced with all features
python scripts/generate_story_template.py \
  --story-number 4.2 \
  --epic 4 \
  --title "Document Similarity Analysis" \
  --owner Elena \
  --estimate 12 \
  --output-dir docs/stories \
  --dry-run  # Preview without creating files
```

**Features:**
- Generates story markdown with AC table template
- Creates test file stubs at `tests/unit/test_{module}/`
- Generates fixtures at `tests/fixtures/{story_key}_fixtures.py`
- Updates sprint-status.yaml automatically
- Creates UAT test cases at `docs/uat/test-cases/`
- Validates epic dependencies before creation

#### 2. Quality Gate Runner
**Location:** `scripts/run_quality_gates.py`
**Purpose:** Run all quality checks in correct order with smart detection
**Benefits:** Catches issues before commit, prevents review cycles

```bash
# Run all quality gates
python scripts/run_quality_gates.py

# CI mode with strict failures
python scripts/run_quality_gates.py --ci

# Check specific paths
python scripts/run_quality_gates.py --path src/data_extract/chunk

# Skip slow checks for quick validation
python scripts/run_quality_gates.py --quick
```

**Checks performed:**
1. Black formatting (auto-fixes if not --ci)
2. Ruff linting with autofix
3. Mypy type checking (strict for greenfield)
4. pytest with coverage thresholds
5. spaCy model validation
6. Generates quality report in JSON/markdown

#### 3. Claude Session Initializer
**Location:** `scripts/init_claude_session.py`
**Purpose:** Set up Claude Code environment automatically on session start
**Benefits:** Consistent environment, no manual setup, immediate productivity

```bash
# Initialize for new session
python scripts/init_claude_session.py

# Skip git operations (for uncommitted work)
python scripts/init_claude_session.py --skip-git

# Verbose mode for debugging
python scripts/init_claude_session.py --verbose
```

**Session setup includes:**
- Git pull/merge from main
- pip install -e ".[dev]" with dependency updates
- spaCy model download if missing
- Load CLAUDE.md context sections
- Display sprint status summary
- Set Python path and environment variables

### Test Infrastructure Achievements

#### Greenfield Fixtures Framework
**Location:** `tests/fixtures/greenfield/`
**Coverage:** 94% on template generator, all P0 scripts covered
**Performance:** 60% token reduction in test code, 75% faster test development

Key patterns established:
- Script fixtures with expected outputs
- AI instruction templates for consistency
- Validation schemas for generated files
- Mock data generators for edge cases

#### Semantic Smoke Tests
**Location:** `tests/integration/test_semantic_smoke.py`
**Performance baselines validated:**
- TF-IDF vectorization: <100ms (target: <500ms)
- LSA decomposition: <200ms (target: <1s)
- Full pipeline: <500ms (target: <2s)

#### QA Fixtures Validation Suite
**Location:** `tests/fixtures/qa/`
**Features:**
- PII scanner utility for compliance checking
- 200+ word semantic corpus for NLP testing
- Gold standard annotations for comparison
- Automated fixture maintenance scripts

### Performance Benefits Summary

| Metric | Before Epic 3.5 | After Epic 3.5 | Improvement |
|--------|-----------------|----------------|-------------|
| Story creation time | 20-30 min | 5 min | **75% faster** |
| Review cycles | 2-3 iterations | 1 iteration | **50% reduction** |
| Test development | 2-3 hours | 30-45 min | **75% faster** |
| Quality gate checks | Manual, often skipped | Automated, enforced | **100% compliance** |
| Session setup | 10-15 min manual | 30 sec automated | **95% faster** |

### Integration with BMAD Workflows

All P0 scripts integrate with BMAD development workflows:

1. **dev-story workflow:** References template generator for story creation
2. **code-review workflow:** Uses quality gate runner for pre-review validation
3. **sprint-planning workflow:** Leverages sprint-status.yaml updates from template
4. **UAT workflows:** Consume test cases generated by template script

### Usage in Daily Development

```bash
# Morning session start
python scripts/init_claude_session.py

# Create new story
python scripts/generate_story_template.py --story-number 4.1 --epic 4 --title "TF-IDF Engine"

# Before committing
python scripts/run_quality_gates.py --quick

# Before review
python scripts/run_quality_gates.py --ci
```

For complete documentation see:
- `docs/stories/3.5-1-story-review-template-generator.md`
- `tests/unit/test_scripts/` (test examples)
- Scripts include --help for all options

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

### JsonFormatter & JSON Schema (Story 3.4)

**Location**
- Formatter protocol/dataclasses: `src/data_extract/output/formatters/base.py`
- Implementation: `src/data_extract/output/formatters/json_formatter.py`
- JSON Schema (Draft 7): `src/data_extract/output/schemas/data-extract-chunk.schema.json`
- Reference doc for downstream consumers: `docs/json-schema-reference.md`

**Output Contract**
- Root object: `{"metadata": {...}, "chunks": [...]}` (single JSON document, not JSON Lines)
- `metadata` captures processing version, timestamp, chunking config, source files, and chunk count
- Each `chunk` entry serializes the Chunk/ChunkMetadata/QualityScore/EntityReference models (ISO 8601 timestamps, stringified paths)
- Schema validation is enabled by default; disable with `JsonFormatter(validate=False)` when high-throughput jobs already trust upstream validation

**Dependencies**
- `pip install textstat pandas`
- `python -m spacy download en_core_web_md`
- Install `jq` CLI (e.g., `curl -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -o venv/bin/jq && chmod +x venv/bin/jq`)
- Node.js available on PATH (used to exercise `JSON.parse`)

**Validation Commands**
```bash
# Unit coverage (structure, schema, serialization)
pytest tests/unit/test_output/test_json_formatter.py tests/unit/test_output/test_json_schema.py

# End-to-end pipeline validation (json.load, pandas, jq, Node, queryability, determinism)
pytest tests/integration/test_output/test_json_output_pipeline.py

# UTF-8 + path compatibility
pytest tests/integration/test_output/test_json_compatibility.py

# Performance baselines (<1s/doc target, validation toggle)
pytest tests/performance/test_json_performance.py
```

**Gotchas**
- JsonFormatter materializes the chunk iterator (array output). Large documents should stay under ~500 chunks; JSON Lines support is deferred to Story 3.7/5.x.
- Schema expects `source_hash` to be 12–64 hex characters. Emit `None` when provenance isn't available instead of empty strings.
- pandas compatibility relies on `pd.json_normalize(json_data["chunks"])`; `pd.read_json` on the root object mixes dict + array and raises.
- jq tests require the binary on PATH; install per instructions above.

### TxtFormatter & Plain Text Output (Story 3.5)

**Location**
- Formatter implementation: `src/data_extract/output/formatters/txt_formatter.py`
- Shared utilities: `src/data_extract/output/utils.py`
- Reference documentation: `docs/txt-format-reference.md`

**Output Contract**
- Clean plain text optimized for direct LLM upload (ChatGPT/Claude)
- Configurable chunk delimiters (default: `━━━ CHUNK {{n}} ━━━`)
- Optional compact metadata headers (source, entities, quality)
- UTF-8-sig encoding with BOM (Windows compatibility)
- Zero formatting artifacts (no markdown/HTML/JSON/ANSI codes)

**Usage Patterns**
```python
from data_extract.output.formatters import TxtFormatter
from data_extract.chunk import ChunkingEngine, ChunkingConfig

# Basic usage (clean text only)
formatter = TxtFormatter()
result = formatter.format_chunks(chunks, Path("output.txt"))

# With metadata headers
formatter = TxtFormatter(include_metadata=True)
result = formatter.format_chunks(chunks, Path("output.txt"))

# Custom delimiter
formatter = TxtFormatter(delimiter="--- CHUNK {{n}} ---")
result = formatter.format_chunks(chunks, Path("output.txt"))
```

**Validation Commands**
```bash
# Unit tests (26 tests)
pytest tests/unit/test_output/test_txt_formatter.py -v

# Integration tests (8 tests - end-to-end pipeline)
pytest tests/integration/test_output/test_txt_pipeline.py -v

# Compatibility tests (5 tests - Unicode, paths, artifacts)
pytest tests/integration/test_output/test_txt_compatibility.py -v

# Performance tests (2 tests - latency baselines)
pytest tests/performance/test_txt_performance.py -v
```

**Output Format**
- Single concatenated TXT file with all chunks
- UTF-8-sig BOM for Windows compatibility
- Delimiters between chunks with sequential numbering (001, 002, ...)
- Optional metadata headers (1-3 lines when enabled)

**Performance Characteristics**
- Small documents (10 chunks): ~0.01s (100x faster than 1s target)
- Large documents (100 chunks): ~0.03s (33x faster than 3s target)
- Memory: ~5MB peak (constant across batch sizes)

**Key Features**
- Clean text (markdown/HTML artifacts removed automatically)
- Deterministic output (same input → byte-identical files)
- Cross-platform (Windows/Unix paths, Unicode filenames)
- Multilingual support (preserves emoji, Chinese, Arabic, etc.)

**Common Use Cases**
1. **LLM Context Upload**: Copy/paste TXT output directly to ChatGPT/Claude
2. **Audit Documentation**: Generate clean reports from messy corporate documents
3. **Text Analysis**: Prepare corpus for downstream NLP tools
4. **Human Review**: Readable format for manual QA workflows

### CsvFormatter & CSV Output (Story 3.6)

**Location**
- Formatter implementation: `src/data_extract/output/formatters/csv_formatter.py`
- Parser validator: `src/data_extract/output/validation/csv_parser.py`
- Unit tests: `tests/unit/test_output/test_csv_formatter.py`, `tests/unit/test_output/test_csv_parser_validator.py`

**Output Contract**
- Canonical 10-column schema (chunk_id, source_file, section_context, chunk_text, entity_tags, quality_score, word_count, token_count, processing_version, warnings)
- RFC 4180 compliant escaping (commas, quotes, newlines)
- UTF-8-sig encoding with BOM (Windows Excel compatibility)
- Optional text truncation with ellipsis indicator
- Semicolon-delimited entity tags for spreadsheet filtering
- Multi-engine parser validation (Python csv + pandas + csvkit)

**Usage Patterns**
```python
from data_extract.output.formatters import CsvFormatter
from pathlib import Path

# Basic usage
formatter = CsvFormatter()
result = formatter.format_chunks(chunks, Path("output.csv"))

# With truncation and validation disabled
formatter = CsvFormatter(max_text_length=200, validate=False)
result = formatter.format_chunks(chunks, Path("output.csv"))
```

**Validation Commands**
```bash
# Unit tests (13 tests - formatter + parser validator)
pytest tests/unit/test_output/test_csv_formatter.py tests/unit/test_output/test_csv_parser_validator.py -v

# Quality gates (BLUE phase - all pass)
python -m black src/data_extract/output/ --check
python -m ruff check src/data_extract/output/
python -m mypy src/data_extract/output/
```

**Status**: Core formatter production-ready with RED→GREEN→BLUE TDD complete. OutputWriter/Organization/CLI integration completed in Story 3.7 (shared infrastructure across JSON/TXT/CSV formatters).

### Output Organization Strategies (Story 3.7)

**Purpose:** Organize output files (JSON/TXT/CSV) by document, entity, or flat layout with comprehensive manifests.

**Strategies:**
- **BY_DOCUMENT:** One folder per source document (audit_report/, risk_matrix/)
- **BY_ENTITY:** Folders by entity type (risks/, controls/, processes/, unclassified/)
- **FLAT:** Single directory with prefixed filenames + manifest.json

**Manifest Enrichment (AC-3.7-6):**
Each manifest includes:
- `config_snapshot` - Chunking/formatter configuration for reproducibility
- `source_hashes` - SHA-256 hashes for source file integrity verification
- `entity_summary` - Entity statistics (total_entities, entity_types, unique_entity_ids)
- `quality_summary` - Quality score aggregations (avg/min/max, quality_flags)
- `generated_at` - ISO 8601 timestamp

**Structured Logging (AC-3.7-7):**
All organization operations emit structlog events:
- organization_start, folder_created, manifest_generated, organization_complete
- Timestamped entries for audit trail per FR-8.3

**References:**
- Format docs: `docs/csv-format-reference.md`, `docs/organizer-reference.md`
- Samples: `docs/examples/csv-output-samples/`, `docs/examples/manifest-samples/`
- Performance: `docs/performance-baselines-epic-3.md` (Organization overhead <50ms)

**Usage:**
```bash
# BY_DOCUMENT organization
data-extract process input.pdf --format csv --output output/ \
  --organize --strategy by_document

# BY_ENTITY organization
data-extract process input.pdf --format json --output output/ \
  --organize --strategy by_entity

# FLAT organization
data-extract process input.pdf --format txt --output output/ \
  --organize --strategy flat
```

### OutputWriter & Production Integration (Story 3.5 - Bucket 2)

**Location**
- Writer implementation: `src/data_extract/output/writer.py`
- CLI implementation: `src/data_extract/cli.py`
- Integration tests: `tests/integration/test_output/test_writer_integration.py`

**OutputWriter API**

OutputWriter is the main entry point for generating formatted output from chunks. It coordinates formatters (JSON, TXT, CSV) with organization strategies.

**Programmatic Usage:**
```python
from data_extract.output.writer import OutputWriter
from data_extract.output.organization import OrganizationStrategy
from pathlib import Path

writer = OutputWriter()

# Concatenated TXT output (default)
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output.txt"),
    format_type="txt"
)

# Per-chunk TXT files
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output/"),
    format_type="txt",
    per_chunk=True
)

# With metadata headers
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output.txt"),
    format_type="txt",
    include_metadata=True
)

# Custom delimiter
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output.txt"),
    format_type="txt",
    delimiter="--- CHUNK {{n}} ---"
)

# Organized output with BY_DOCUMENT strategy
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output/"),
    format_type="txt",
    per_chunk=True,
    organize=True,
    strategy=OrganizationStrategy.BY_DOCUMENT
)

# JSON output (validation optional)
result = writer.write(
    chunks=my_chunks,
    output_path=Path("output.json"),
    format_type="json",
    validate=False  # Disable schema validation for performance
)
```

**CLI Usage (Minimal Implementation for Story 3.5):**

```bash
# Basic TXT output (concatenated)
data-extract process input.pdf --format txt --output chunks.txt

# Per-chunk TXT files
data-extract process input.pdf --format txt --output output/ --per-chunk

# With metadata headers
data-extract process input.pdf --format txt --output chunks.txt --include-metadata

# Custom delimiter
data-extract process input.pdf --format txt --output chunks.txt --delimiter "--- CHUNK {{n}} ---"

# Organized output with BY_DOCUMENT strategy
data-extract process input.pdf --format txt --output output/ --per-chunk --organize --strategy by_document

# Organized output with FLAT strategy
data-extract process input.pdf --format txt --output output/ --per-chunk --organize --strategy flat

# JSON output
data-extract process input.pdf --format json --output output.json

# Display version information
data-extract version
```

**Available CLI Options:**
- `--format {json,txt}`: Output format (default: txt)
- `--output PATH`: Output file or directory path (required)
- `--per-chunk`: Write each chunk to separate file (TXT only)
- `--include-metadata`: Include metadata headers (TXT only)
- `--organize`: Enable output organization (requires --strategy)
- `--strategy {by_document,by_entity,flat}`: Organization strategy
- `--delimiter TEXT`: Custom chunk delimiter (TXT only, use {{n}} for chunk number)

**Organization Strategies:**
- `by_document`: One folder per source document
- `by_entity`: One folder per entity type (risks/, controls/, etc.)
- `flat`: Single directory with prefixed filenames

**Note:** This is a minimal implementation for Story 3.5 UAT validation. Epic 5 will implement full Typer-based CLI with:
- Complete extraction pipeline integration
- Configuration cascade (CLI → env vars → YAML → defaults)
- Batch processing and progress indicators
- Advanced error handling and recovery

**Validation Commands:**
```bash
# Integration tests (17 test cases)
pytest tests/integration/test_output/test_writer_integration.py -v

# Run all output tests
pytest tests/integration/test_output/ -v

# CLI smoke tests
pytest tests/integration/test_output/test_writer_integration.py::TestCLIIntegration -v
```

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
