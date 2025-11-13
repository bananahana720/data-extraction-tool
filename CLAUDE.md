# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Data Extraction Tool** - Enterprise document processing pipeline for RAG workflows. Transforms messy corporate audit documents into AI-optimized outputs using a five-stage modular pipeline architecture.

**Status**: Brownfield modernization (Epic 1 - Foundation in progress)
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
`src/{cli,core,extractors,processors,formatters,infrastructure,pipeline}/` - Legacy code being assessed and consolidated (Story 1.2-1.4)

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

**Test Markers**: `unit`, `integration`, `extraction`, `processing`, `formatting`, `pipeline`, `cli`, `slow`, `performance`

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

**Note**: Pre-commit hooks run automatically on `git commit`. If blocked, fix the issues or ask user to check hook configuration.

### CLI Entry Point
```bash
data-extract    # Typer-based CLI (Epic 5 - placeholder in Epic 1)
```

## Testing Strategy

### Organization
Tests mirror `src/` structure exactly:
- `tests/unit/` - Fast, isolated tests
- `tests/integration/` - Multi-component, end-to-end
- `tests/performance/` - Benchmarks and stress tests
- `tests/fixtures/` - Shared test data

### Coverage Requirements
- Epic 1: >60% baseline
- Epic 2-4: >80% overall
- Epic 5: >90% critical paths

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

### Current: Epic 1 - Foundation
- ✅ Story 1.1: Project Infrastructure (complete)
- 🔄 Story 1.2: Brownfield Codebase Assessment (in progress)
- 📋 Story 1.3: Testing Framework & CI Pipeline
- 📋 Story 1.4: Core Pipeline Architecture Consolidation

### Upcoming
- **Epic 2**: Extract & Normalize stages
- **Epic 3**: Chunk & Output stages
- **Epic 4**: Semantic analysis stage
- **Epic 5**: CLI, batch processing, configuration cascade

See `docs/epics.md` and `docs/stories/` for detailed story specifications.

## Configuration (Epic 5)

Four-tier precedence cascade:
1. CLI flags (highest)
2. Environment variables (`DATA_EXTRACT_*` prefix)
3. YAML config file (`~/.data-extract/config.yaml` or project-local)
4. Hardcoded defaults (lowest)

Epic 1 sets up infrastructure; Epic 5 implements full cascade.

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

## Lessons from Epic 2

Epic 2 (Extract & Normalize) established critical patterns from 6 stories with multiple code review cycles.

### Quality Gates Workflow

**Run BEFORE committing** (shift-left approach):
1. Write code
2. `black src/ tests/` → Fix formatting
3. `ruff check src/ tests/` → Fix linting
4. `mypy src/data_extract/` → Fix type violations (**must run from project root**)
5. Run tests → Fix failures
6. Commit clean code

**Quality Bar**: 0 violations required. No exceptions.

### Key Anti-Patterns (DO NOT REPEAT)

1. **Deferred Validation Fixes**: Fix mypy/ruff violations immediately, not in later stories. Accumulating tech debt slows velocity.
2. **Skipping Integration Tests**: Unit tests alone miss memory leaks, resource issues, and NFR violations. Always test multi-component workflows.
3. **Premature Optimization**: Profile first (establish baseline), measure actual behavior, then optimize. Don't guess at bottlenecks.
4. **Missing Context Docs**: Document architectural decisions and patterns as you go. Future stories depend on this context.

### Architecture Patterns

**PipelineStage Protocol**: All processing stages implement `process(ProcessingResult) -> ProcessingResult` interface. Enables easy testing, flexible composition, gradual refactoring.

**Memory Monitoring**: Reuse `get_total_memory()` from `scripts/profile_pipeline.py:151-167` (aggregates main + worker processes, 9.6ms overhead).

**Test Fixtures**: Keep total <100MB, use synthetic/sanitized data, document in `tests/fixtures/README.md`, provide regeneration scripts.

**spaCy Integration**: Download models via setup (not runtime), lazy-load on first use, cache globally. See `docs/troubleshooting-spacy.md`.

### NFR Validation Approach

Validate continuously against baselines (established in Story 2.5.1):
- **NFR-P1**: <10 min for 100 PDFs (achieved: 6.86 min, 148% improvement)
- **NFR-P2**: <2GB memory (individual files: 167MB ✅, batch: 4.15GB ⚠️ trade-off documented)
- **NFR-R2**: Graceful degradation via continue-on-error pattern
- **NFR-O3**: Test reporting via pytest coverage + performance baselines

Document trade-offs transparently when targets conflict with complexity.

### Detailed References

- **Quality gates**: See `## Code Quality` section above for command details
- **spaCy setup**: `docs/troubleshooting-spacy.md`
- **Memory monitoring**: `docs/stories/2.5-2.1-pipeline-throughput-optimization.md`
- **Test fixtures**: `tests/fixtures/README.md`
- **Performance baselines**: `docs/performance-baselines-story-2.5.1.md`
- **Story details**: `docs/stories/2.5-*.md` for implementation patterns

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

### Running UAT Workflows

The UAT (User Acceptance Testing) workflow framework provides systematic validation of acceptance criteria through a 4-stage pipeline.

**Pipeline**: `create-test-cases` → `build-test-context` → `execute-tests` → `review-uat-results`

#### 1. Generate Test Cases from Story

```bash
workflow create-test-cases
# Generates: docs/uat/test-cases/{story-key}-test-cases.md

# Options:
workflow create-test-cases story_path=docs/stories/2.5-3.1-uat-workflow-framework.md
workflow create-test-cases test_coverage_level=comprehensive  # minimal|standard|comprehensive
```

**Output**: Test cases with scenarios (happy path, edge cases, error cases), mapped to test types (unit, integration, CLI, manual).

#### 2. Build Test Context

```bash
workflow build-test-context
# Generates: docs/uat/test-context/{story-key}-test-context.xml

# Options:
workflow build-test-context test_cases_file=docs/uat/test-cases/2.5-3.1-test-cases.md
workflow build-test-context include_story_context=false  # Don't reuse story context
```

**Output**: Test context XML with fixtures, helpers, pytest config, code under test.

#### 3. Execute Tests

```bash
workflow execute-tests
# Generates: docs/uat/test-results/{story-key}-test-results.md

# Options:
workflow execute-tests test_execution_mode=automated  # automated|manual|hybrid
workflow execute-tests capture_screenshots=true  # For CLI tests
workflow execute-tests continue_on_failure=false  # Stop on first failure
```

**Execution Types**:
- **Automated**: Runs pytest tests (unit, integration, performance)
- **CLI**: Uses tmux-cli for interactive CLI testing
- **Manual**: Guides user through manual test execution

**Output**: Test results with pass/fail/blocked status, evidence, and recommendations.

#### 4. Review UAT Results

```bash
workflow review-uat-results
# Generates: docs/uat/reviews/{story-key}-uat-review.md

# Options:
workflow review-uat-results quality_gate_level=strict  # minimal|standard|strict
workflow review-uat-results auto_approve_if_all_pass=true  # Auto-approve (not recommended)
```

**Quality Gates**:
- **Minimal**: 80% pass rate, critical ACs 100%
- **Standard**: 90% pass rate, critical ACs 100%, 70% edge case coverage *[default]*
- **Strict**: 95% pass rate, critical ACs 100%, 85% edge case coverage, high evidence quality

**Output**: UAT review with approval decision (APPROVED, CHANGES REQUESTED, BLOCKED), findings, and stakeholder summary.

#### Complete UAT Flow Example

```bash
# 1. Generate test cases
workflow create-test-cases

# 2. Build test context
workflow build-test-context

# 3. Execute tests
workflow execute-tests test_execution_mode=hybrid

# 4. Review and approve
workflow review-uat-results
```

**tmux-cli Integration** (for CLI tests):

**⚠️ Windows Users**: tmux-cli requires tmux, which is Unix/Linux only. On Windows, run workflows with CLI tests from WSL:
```bash
# Enter WSL environment
wsl

# Navigate to project (Windows filesystem mounted at /mnt/c/)
cd /mnt/c/Users/Andrew/projects/data-extraction-tool-1

# Run workflow with CLI tests
workflow execute-tests test_execution_mode=hybrid
```

**Linux/macOS or WSL** - Standard tmux-cli usage:
```bash
# Always launch shell first
tmux-cli launch "zsh"

# Send commands and wait for completion
tmux-cli send "data-extract process test.pdf" --pane=2
tmux-cli wait_idle --pane=2 --idle-time=2.0

# Capture output
tmux-cli capture --pane=2
```

See `docs/tmux-cli-instructions.md` for full tmux-cli reference and `docs/uat/tmux-cli-windows-setup.md` for detailed Windows setup.

**UAT Output Locations**:
```
docs/uat/
├── test-cases/      # Generated test case specifications
├── test-context/    # Test infrastructure context (XML)
├── test-results/    # Test execution results
└── reviews/         # QA review and approval reports
```

## Key Architecture Decisions

- **ADR-001**: Immutable models prevent pipeline state corruption
- **ADR-002**: Pluggable extractors isolate format-specific logic
- **ADR-003**: ContentBlocks preserve document structure over raw text
- **ADR-004**: Classical NLP only (enterprise constraint - no transformers)
- **ADR-005**: Gradual brownfield modernization (don't break production)

See `docs/architecture.md` for full details.

## Documentation References

- `docs/architecture.md` - Technical architecture and ADRs
- `docs/PRD.md` - Product requirements and vision
- `docs/tech-spec-epic-1.md` - Epic 1 technical specification
- `docs/brownfield-assessment.md` - Existing code analysis
- `docs/epics.md` - Epic breakdown and roadmap
- `docs/stories/` - Story-level implementation specs
- `pyproject.toml` - Project configuration and dependencies
- `.pre-commit-config.yaml` - Code quality hooks

## Important Notes

### Search Tools
**Always use ripgrep (rg), never grep**. The tool is configured to use rg for performance.

### Brownfield Code
Existing code in `src/{cli,extractors,processors,formatters,core,pipeline,infrastructure}/` is being assessed and consolidated. During Epic 1, both systems coexist. Don't remove or refactor brownfield code without checking Story 1.2 assessment first.

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
