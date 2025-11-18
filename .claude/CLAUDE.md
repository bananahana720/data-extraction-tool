# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- MODULE: CORE-OVERVIEW -->
## Project Overview

**Data Extraction Tool** - Enterprise document processing pipeline for RAG workflows. Transforms messy corporate audit documents into AI-optimized outputs using a five-stage modular pipeline architecture.

**Status**: Epic 3 - Chunk & Output (COMPLETE - all 7 stories done)
**Python**: 3.12+ (mandatory enterprise requirement)
**Architecture**: `Extract → Normalize → Chunk → Semantic → Output`
<!-- END MODULE: CORE-OVERVIEW -->

<!-- MODULE: CRITICAL-RULES -->
## Critical Rules

**[CRITICAL]** Fill AC evidence table BEFORE marking review status - prevents review cycles
**[CRITICAL]** Run Black → Ruff → Mypy → Tests BEFORE marking task complete - quality gate enforcement
**[CRITICAL]** Fix violations immediately when discovered - don't accumulate tech debt
**[CRITICAL]** Mirror test structure to src/ exactly - prevents test organization issues
**[CRITICAL]** Never break brownfield code during greenfield migration - both systems must coexist

For complete lessons learned, see `docs/retrospective-lessons.md`.
<!-- END MODULE: CRITICAL-RULES -->

<!-- MODULE: ARCHITECTURE -->
## Core Architecture

### Five-Stage Pipeline Pattern

Each stage is a composable, testable component using frozen dataclasses and ABC interfaces:

1. **Extract** (`src/data_extract/extract/`) - Document format-specific extraction (PDF, DOCX, XLSX, PPTX, CSV, images+OCR)
2. **Normalize** (`src/data_extract/normalize/`) - Text cleaning, entity standardization
3. **Chunk** (`src/data_extract/chunk/`) - Semantic-aware chunking (spaCy-based)
4. **Semantic** (`src/data_extract/semantic/`) - Classical NLP analysis (TF-IDF, LSA - no transformers per enterprise constraints)
5. **Output** (`src/data_extract/output/`) - Multiple formats (JSON, TXT, CSV)

### Design Principles

**[REQUIRED]** Modularity - Each stage independent, testable, replaceable
**[REQUIRED]** Immutability - Frozen dataclasses prevent pipeline state mutations
**[REQUIRED]** Type Safety - Full type hints + Pydantic v2 validation enforced by mypy
**[REQUIRED]** Interface-Based - All modules implement ABCs (BaseExtractor, BaseProcessor, BaseFormatter)
**[REQUIRED]** Determinism - Same input always produces same output

### Dual Codebase Structure

**Greenfield** (`src/data_extract/`) - Modern pipeline implementation
**Brownfield** (`src/{cli,core,extractors,processors,formatters,infrastructure,pipeline}/`) - Legacy code

**[CRITICAL]** Both systems coexist during migration. Don't break existing brownfield code.
<!-- END MODULE: ARCHITECTURE -->

<!-- MODULE: COMMANDS -->
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
```bash
python -m spacy download en_core_web_md
python -m spacy validate
```

### Semantic Dependencies Setup (Required for Epic 4)
```bash
# Dependencies are installed via pip install -e ".[dev]"
# Verify installation with smoke test:
python scripts/smoke-test-semantic.py
```

**Semantic Stack:**
- **scikit-learn** (≥1.3.0) - TF-IDF vectorization, LSA, cosine similarity
- **joblib** (≥1.3.0) - Model serialization and caching
- **textstat** (≥0.7.3) - Readability metrics (Flesch, SMOG, etc.)

**Performance Baselines:**
- TF-IDF fit/transform: <100ms for 1k-word document
- Full pipeline: <500ms for 10 documents
- CI validation: Smoke test runs automatically after dependency installation

**Learning Resources:**
- **TF-IDF/LSA Playbook**: `docs/playbooks/semantic-analysis-intro.ipynb` - Interactive Jupyter notebook for junior developers
- **Quick Reference**: `docs/playbooks/semantic-analysis-reference.md` - API reference and troubleshooting guide
- **Test Corpus**: `tests/fixtures/semantic_corpus.py` - Pre-built corpus for examples

### Testing
```bash
pytest                      # Run all tests
pytest --cov=src           # With coverage
pytest -m unit             # Fast unit tests only
pytest -m integration      # Integration tests
pytest -n auto             # Parallel execution
```

**[REQUIRED]** Test Markers: `unit`, `integration`, `extraction`, `processing`, `formatting`, `chunking`, `pipeline`, `cli`, `slow`, `performance`

### Code Quality (Enforced by Pre-commit)
```bash
black src/ tests/          # Format code (100 char line length)
ruff check src/ tests/     # Lint code
mypy src/data_extract/     # Type check (strict mode, excludes brownfield)
pre-commit run --all-files # Run all pre-commit hooks
```

**[CRITICAL]** Pre-commit hooks run on `git commit` AND are validated in CI. Always run `pre-commit run --all-files` before pushing.

### CLI Entry Point
```bash
data-extract    # Typer-based CLI (full implementation in Epic 5)
```
<!-- END MODULE: COMMANDS -->

<!-- MODULE: AUTOMATION -->
## Development Automation (Epic 3.5)

**P0 Scripts** (60% token reduction, 75% faster development):
- `scripts/generate_story_template.py` - Story template generator
- `scripts/run_quality_gates.py` - Quality gate runner (Black/Ruff/Mypy/coverage)
- `scripts/init_claude_session.py` - Session initializer (git sync, deps, spaCy)

**Usage:** See `docs/automation-guide.md` for complete documentation and examples.
<!-- END MODULE: AUTOMATION -->

<!-- MODULE: CONVENTIONS -->
## Code Conventions

### Style (Enforced by Tools)
**[REQUIRED]** Formatting - Black (100 char lines, target Python 3.12)
**[REQUIRED]** Linting - Ruff (replaces flake8 + isort)
**[REQUIRED]** Type Checking - Mypy strict mode (excludes brownfield during migration)

### Naming
**[REQUIRED]** Classes: `PascalCase` (e.g., `DocxExtractor`)
**[REQUIRED]** Functions/methods: `snake_case` (e.g., `extract_content`)
**[REQUIRED]** Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_CHUNK_SIZE`)
**[REQUIRED]** Modules: `snake_case` (e.g., `context_linker.py`)

### Required Standards
**[REQUIRED]** Type hints on all public functions
**[REQUIRED]** Google-style docstrings for public APIs
**[REQUIRED]** Tests for all new functionality
**[CRITICAL]** Pre-commit compliance (black, ruff, mypy must pass)
<!-- END MODULE: CONVENTIONS -->

<!-- MODULE: TESTING -->
## Testing Strategy

### Organization
**[CRITICAL]** Tests mirror `src/` structure exactly
**[REQUIRED]** Use pytest fixtures for test data
**[REQUIRED]** Use markers for selective execution
**[RECOMMENDED]** Include integration and performance tests

### Coverage Requirements
**[REQUIRED]** Baseline: >60% overall (includes brownfield)
**[REQUIRED]** Greenfield (`src/data_extract/`): >80% coverage
**[RECOMMENDED]** Epic 5 critical paths: >90% coverage
<!-- END MODULE: TESTING -->

<!-- MODULE: CURRENT-STATE -->
## Epic Status

### Completed
- **Epic 1**: Foundation (4 stories)
- **Epic 2**: Extract & Normalize (6 stories)
- **Epic 2.5**: Infrastructure (6 stories)
- **Epic 3**: Chunk & Output (7 stories COMPLETE)

### Current Focus
Epic 3 implementations complete. For detailed implementation reference, see `docs/epic-3-reference.md`.

**Key Achievements:**
- Semantic-aware chunking with entity preservation
- JSON/TXT/CSV output formatters
- Configurable output organization strategies
- Performance: ~0.19s per 1,000 words, 255 MB peak memory

### Upcoming
- **Epic 4**: Semantic analysis stage
- **Epic 5**: CLI, batch processing, configuration cascade

See `docs/sprint-status.yaml` and `docs/stories/` for specifications.
<!-- END MODULE: CURRENT-STATE -->

<!-- MODULE: QUALITY-GATES -->
## Quality Gates

**[CRITICAL]** Pre-commit workflow (0 violations required):
1. `black src/ tests/` → Fix formatting
2. `ruff check src/ tests/` → Fix linting
3. `mypy src/data_extract/` → Fix type violations (run from project root)
4. Run tests → Fix failures
5. Commit clean code

**[REQUIRED]** Fix validation issues immediately (don't defer tech debt)
**[REQUIRED]** Always include integration tests (catch memory/NFR issues)
**[RECOMMENDED]** Profile before optimizing (establish baselines first)
<!-- END MODULE: QUALITY-GATES -->

<!-- MODULE: TECHNOLOGY -->
## Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| CLI | Typer | Type-safe, modern |
| Data Models | Pydantic v2 | Runtime validation |
| PDF | PyMuPDF | Fast, OCR fallback |
| Office | python-docx, openpyxl | Standard libraries |
| Chunking | spaCy | Sentence boundaries |
| Semantic | scikit-learn | TF-IDF, LSA |
| Testing | pytest | Industry standard |
| Quality | black, ruff, mypy | Modern toolchain |

**[CRITICAL]** Enterprise Constraint: Classical NLP only - no transformer models allowed.
<!-- END MODULE: TECHNOLOGY -->

<!-- MODULE: KEY-DECISIONS -->
## Key Architecture Decisions

**[REQUIRED]** ADR-001: Immutable models prevent pipeline state corruption
**[REQUIRED]** ADR-002: Pluggable extractors isolate format-specific logic
**[REQUIRED]** ADR-003: ContentBlocks preserve document structure
**[CRITICAL]** ADR-004: Classical NLP only (enterprise constraint)
**[CRITICAL]** ADR-005: Gradual brownfield modernization

See `docs/architecture.md` for full details.
<!-- END MODULE: KEY-DECISIONS -->

<!-- MODULE: REFERENCES -->
## Documentation References

### Core Documentation
- `docs/epic-3-reference.md` - Complete Epic 3 implementation guide
- `docs/automation-guide.md` - P0 scripts and automation tools
- `docs/retrospective-lessons.md` - Comprehensive lessons from Epics 1-3
- `docs/architecture.md` - Technical architecture and ADRs
- `docs/sprint-status.yaml` - Current development status (authoritative)

### Epic Documentation
- `docs/tech-spec-epic-*.md` - Epic technical specifications
- `docs/stories/` - Story-level implementation specs
- `docs/performance-baselines-epic-*.md` - Performance benchmarks

### Playbooks and Guides
- `docs/playbooks/semantic-analysis-intro.ipynb` - TF-IDF/LSA interactive tutorial (Epic 4 prep)
- `docs/playbooks/semantic-analysis-reference.md` - Quick API reference for semantic analysis

### Configuration
- `pyproject.toml` - Project configuration and dependencies
- `.pre-commit-config.yaml` - Code quality hooks
<!-- END MODULE: REFERENCES -->

<!-- MODULE: IMPORTANT-NOTES -->
## Important Notes

### Search Tools
**[CRITICAL]** Always use ripgrep (rg), never grep. The tool is configured to use rg for performance.

### Type Checking
**[REQUIRED]** Mypy excludes brownfield packages during migration. New code in `src/data_extract/` must pass strict type checking.

### Error Handling
**[RECOMMENDED]** Pipeline uses "continue-on-error" pattern - graceful degradation per file. Don't fail entire batch on single document error.

### Documentation
**[REQUIRED]** README files only when explicitly requested - don't create documentation proactively.
<!-- END MODULE: IMPORTANT-NOTES -->