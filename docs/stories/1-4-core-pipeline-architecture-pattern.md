# Story 1.4: Core Pipeline Architecture Pattern

Status: review

## Story

As a developer,
I want a well-defined pipeline architecture pattern for modular processing,
so that I can build composable components (extract → normalize → chunk → analyze) with clear contracts and deterministic data flow.

## Acceptance Criteria

1. **AC-1.4.1:** Pipeline interface defined with clear contracts
   - PipelineStage protocol in core/pipeline.py
   - Generic type parameters (Input, Output)
   - process() method signature documented

2. **AC-1.4.2:** Pipeline stages have standalone module structure
   - src/data_extract/extract/ exists with __init__.py
   - src/data_extract/normalize/ exists with __init__.py
   - src/data_extract/chunk/ exists with __init__.py
   - src/data_extract/semantic/ exists with __init__.py
   - src/data_extract/output/ exists with __init__.py

3. **AC-1.4.3:** Data models defined with Pydantic
   - Document model with validation
   - Chunk model with validation
   - Metadata model with validation
   - Entity model with validation
   - ProcessingContext model

4. **AC-1.4.4:** Pipeline configuration centralized
   - ProcessingContext carries config, logger, metrics
   - Config passed through all pipeline stages
   - Type-safe configuration structure

5. **AC-1.4.5:** Architecture supports pipeline and single-command execution
   - Pipeline class orchestrates multiple stages
   - Individual stages can be executed standalone
   - Demonstrated in example test

6. **AC-1.4.6:** Error handling strategy consistent
   - Exception hierarchy defined in core/exceptions.py
   - ProcessingError for recoverable errors
   - CriticalError for unrecoverable errors
   - All exceptions documented

7. **AC-1.4.7:** Architecture documented in docs/architecture.md
   - Pipeline pattern explained
   - Data models documented
   - Error handling strategy described
   - Examples provided

## Tasks / Subtasks

- [x] **Task 1: Define core data models** (AC: 1.4.3)
  - [x] Create `src/data_extract/core/models.py`
  - [x] Implement Entity model with type, id, text, confidence fields
  - [x] Implement Metadata model with source_file, file_hash, processing_timestamp, tool_version, config_version, document_type, quality_scores, quality_flags
  - [x] Implement Document model with id, text, entities, metadata, structure
  - [x] Implement Chunk model with id, text, document_id, position_index, token_count, word_count, entities, section_context, quality_score, readability_scores, metadata
  - [x] Implement ProcessingContext model with config, logger, metrics
  - [x] Add Pydantic v2 field validation constraints (confidence: 0.0-1.0, quality_score: 0.0-1.0)
  - [x] Write unit tests for all models (valid/invalid data, field validation)

- [x] **Task 2: Define pipeline architecture protocol** (AC: 1.4.1, 1.4.5)
  - [x] Create `src/data_extract/core/pipeline.py`
  - [x] Define PipelineStage Protocol with Generic[Input, Output]
  - [x] Implement process() method signature with input_data, context parameters
  - [x] Document protocol contract in docstrings
  - [x] Implement Pipeline orchestrator class
  - [x] Add __init__(stages: List[PipelineStage]) constructor
  - [x] Implement process() method that chains stage outputs to inputs
  - [x] Write unit tests for Pipeline class with mock stages

- [x] **Task 3: Define exception hierarchy** (AC: 1.4.6)
  - [x] Create `src/data_extract/core/exceptions.py`
  - [x] Implement DataExtractError base exception
  - [x] Implement ProcessingError (recoverable) extending DataExtractError
  - [x] Implement CriticalError (unrecoverable) extending DataExtractError
  - [x] Implement ConfigurationError extending CriticalError
  - [x] Implement ExtractionError extending ProcessingError
  - [x] Implement ValidationError extending ProcessingError
  - [x] Add docstrings explaining when to use each exception type
  - [x] Write unit tests for exception hierarchy (raise and catch each type)

- [x] **Task 4: Create module structure for pipeline stages** (AC: 1.4.2)
  - [x] Create directory `src/data_extract/extract/` with `__init__.py`
  - [x] Create directory `src/data_extract/normalize/` with `__init__.py`
  - [x] Create directory `src/data_extract/chunk/` with `__init__.py`
  - [x] Create directory `src/data_extract/semantic/` with `__init__.py`
  - [x] Create directory `src/data_extract/output/` with `__init__.py`
  - [x] Add placeholder docstrings in each __init__.py describing module purpose
  - [x] Write test to verify all module directories exist and contain __init__.py
  - [x] Test that each module is importable (import succeeds without errors)

- [x] **Task 5: Document architecture patterns** (AC: 1.4.7)
  - [x] Update `docs/architecture.md` with Pipeline Stage Pattern section
  - [x] Document PipelineStage protocol contract and generic typing
  - [x] Document data models (Entity, Metadata, Document, Chunk, ProcessingContext)
  - [x] Document exception hierarchy with usage guidance
  - [x] Add example code demonstrating pipeline orchestration
  - [x] Document type contracts between stages (Extract→Normalize→Chunk→Semantic→Output)
  - [x] Document configuration cascade pattern with ProcessingContext

- [x] **Task 6: Create integration tests** (AC: 1.4.5)
  - [x] Create `tests/integration/test_pipeline_architecture.py`
  - [x] Write test demonstrating end-to-end pipeline flow with mock stages
  - [x] Test Pipeline orchestrator chains stages correctly
  - [x] Test ProcessingContext passed through all stages
  - [x] Test ProcessingError handling (continue batch processing)
  - [x] Test CriticalError handling (halt processing)
  - [x] Test individual stage can execute standalone

- [x] **Task 7: Configuration integration** (AC: 1.4.4)
  - [x] Verify ProcessingContext accepts config dict
  - [x] Test logger integration with ProcessingContext
  - [x] Test metrics tracking in ProcessingContext
  - [x] Document configuration structure expected in ProcessingContext.config

- [x] **Task 8: Code quality and testing** (Quality gate)
  - [x] Run pytest with coverage (target: >90% for core modules)
  - [x] Verify mypy type checking passes for all new code
  - [x] Run black formatter on all new files
  - [x] Run ruff linter and fix any issues
  - [x] Verify all pre-commit hooks pass

## Dev Notes

### Architecture Patterns to Implement

**Pipeline Stage Pattern:**
- Protocol-based interface ensures all stages follow consistent contracts
- Generic typing (Input, Output) provides type safety at compile time
- PipelineStage[Input, Output] protocol enables mock implementations for testing

**Error Handling Strategy:**
- Exception hierarchy supports continue-on-error batch processing
- ProcessingError: Log error, skip file, continue with remaining batch
- CriticalError: Halt processing immediately (e.g., invalid config)
- ConfigurationError, ExtractionError, ValidationError extend base hierarchy

**Configuration Cascade:**
- ProcessingContext carries shared state through all stages
- Three-tier precedence: CLI flags > env vars > YAML config > defaults
- Type-safe config structure enables validation at pipeline entry point

### Core Data Models

**Pydantic v2 Models** (must implement runtime validation):

1. **Entity** - Domain entities (risk, control, policy, process, regulation, issue)
   - Fields: type, id, text, confidence (0.0-1.0)
   - Used by: Document, Chunk

2. **Metadata** - Provenance and quality tracking
   - Fields: source_file, file_hash (SHA-256), processing_timestamp, tool_version, config_version, document_type, quality_scores, quality_flags
   - Used by: Document, Chunk

3. **Document** - Represents processed document
   - Fields: id, text, entities, metadata, structure
   - Type contract: Extract → Normalize

4. **Chunk** - Semantic chunk for RAG
   - Fields: id (format: {source}_{index:03d}), text, document_id, position_index, token_count, word_count, entities, section_context, quality_score, readability_scores, metadata
   - Type contract: Chunk → Semantic

5. **ProcessingContext** - Shared pipeline state
   - Fields: config (Dict), logger (structlog), metrics (Dict)
   - Passed through all pipeline stages

### Module Structure

Create placeholder modules for future pipeline stages:

```
src/data_extract/
├── extract/       # Document extraction (Epic 2-3)
├── normalize/     # Text normalization (Epic 2)
├── chunk/         # Semantic chunking (Epic 3)
├── semantic/      # Similarity analysis (Epic 4)
└── output/        # Output formatting (Epic 3)
```

Each module gets `__init__.py` with docstring describing future responsibility.

### Type Contracts Between Stages

- **Extract → Normalize:** Document (with raw text)
- **Normalize → Chunk:** Document (with cleaned text, normalized entities)
- **Chunk → Semantic:** List[Chunk] (with metadata)
- **Semantic → Output:** ProcessingResult (with analysis results)

### Testing Strategy

**Unit Tests (>90% coverage target):**
- Test Pydantic model instantiation (valid/invalid data)
- Test field validation constraints (confidence: 0.0-1.0, etc.)
- Test PipelineStage protocol implementation with mock stages
- Test exception hierarchy (raise and catch each type)
- Test ProcessingContext creation and immutability

**Integration Tests:**
- End-to-end pipeline flow with mock stages
- Verify Pipeline orchestrator chains outputs to inputs correctly
- Test error handling (ProcessingError vs CriticalError behavior)
- Test individual stages can execute standalone

**Edge Cases:**
- Empty pipeline (no stages)
- Invalid Pydantic model inputs
- Missing config keys in ProcessingContext
- Malformed file paths in Metadata

**Testing Conventions from Story 1-3 (MUST FOLLOW):**
- **Path Resolution:** Use `Path(__file__).parent.parent / "fixtures"` for robust fixture paths (NOT hardcoded relative paths)
- **Error Handling:** Wrap all pipeline stage calls in try-except blocks with descriptive error messages
- **Type Hints:** All callbacks and fixtures must have type hints: `def callback(status: dict) -> None:`
- **Cleanup Pattern:** Use yield...finally pattern for temp file cleanup in fixtures
- **Import Errors:** Provide helpful installation messages when optional dependencies missing

### Learnings from Previous Story (1.3: Testing Framework)

**From Story 1-3-testing-framework-and-ci-pipeline (Status: DONE)**

**Test Infrastructure to Reuse:**
- `tests/conftest.py` - Shared pytest fixtures with status callback, temp file cleanup (yield...finally pattern), ImportError handling
- `pytest.ini` - Coverage configuration (60% baseline for Epic 1), 13 test markers configured
- Path resolution pattern: `Path(__file__).parent.parent / "fixtures"` (CRITICAL - use everywhere)

**New Files Created in 1.3:**
- Test infrastructure: tests/unit/, tests/integration/, tests/fixtures/
- CI pipeline: .github/workflows/test.yml (Python 3.12, 3.13 matrix)
- Pre-commit hooks: .pre-commit-config.yaml (black, ruff, mypy)
- Coverage baseline: tests/COVERAGE_BASELINE.md (55% actual vs 60% target)

**Architectural Decisions:**
- Coverage threshold: 60% for Epic 1 brownfield (single source of truth in pytest.ini)
- Test markers: unit, integration, performance, slow, extraction, processing, formatting, pipeline, cli, edge_case, stress, infrastructure, cross_format
- Pre-commit strategy: black, ruff, mypy run locally before commit

**Technical Debt to Address:**
- 229 failing brownfield tests need categorization (import errors, API changes, deprecated functionality)
- Extractor coverage critically low: PDF 19%, CSV 24%, Excel 26%, PPTX 24% (target: 60%+)
- Coverage baseline at 55% (5% below 60% target) - acceptable for Epic 1 brownfield

**Warnings for This Story:**
1. **Path Resolution Critical:** All new tests MUST use `Path(__file__).parent.parent / "fixtures"` pattern
2. **Type Hints Required:** All callbacks need type hints: `def callback(status: dict) -> None:`
3. **Try-Except Pattern:** Wrap all extractor/processor/formatter calls with descriptive error messages
4. **Cleanup Pattern:** Use yield...finally for temp file cleanup in fixtures
5. **Coverage Target:** Aim for >90% coverage on new core modules (models.py, pipeline.py, exceptions.py)

**Testing Patterns Established:**
- Integration test structure: fixture loading → object creation → pipeline execution → edge cases
- Edge case template: empty files, nonexistent files, minimal content (1 char), corrupted files
- Error handling tests: ProcessingError vs CriticalError behavior differentiation

**Files Modified in 1.3:**
- pytest.ini - Added coverage config, test markers, fail_under=60%
- .pre-commit-config.yaml - Added hooks for black, ruff, mypy
- README.md - Added pre-commit usage documentation

**Key Pattern to Follow:**
```python
# Robust path resolution (use everywhere in tests)
fixtures_dir = Path(__file__).parent.parent / "fixtures"
# NOT: Path("tests/fixtures") - fails in different working directories
```

**Quality Gates (Non-Negotiable):**
- All code must pass: pytest, ruff, mypy, black
- Coverage target: >90% for new core modules, >80% overall
- Pre-commit hooks enforce quality before commit
- CI pipeline blocks PRs if any check fails

[Source: stories/1-3-testing-framework-and-ci-pipeline.md#Dev-Agent-Record]

### Project Structure Notes

**Alignment with Project:**
- Core modules location: `src/data_extract/core/` (models.py, pipeline.py, exceptions.py)
- Pipeline stage modules: `src/data_extract/{extract,normalize,chunk,semantic,output}/`
- Test structure: `tests/unit/core/` for unit tests, `tests/integration/` for pipeline tests
- Documentation: `docs/architecture.md` for architecture patterns

**Dependencies from pyproject.toml:**
- Python 3.12.x (mandatory, ADR-004)
- pydantic >= 2.0.0, < 3.0 - Data models with runtime validation
- structlog >= 24.0.0, < 25.0 - Structured logging
- PyYAML >= 6.0.0, < 7.0 - YAML configuration parsing
- pytest >= 8.0.0, < 9.0 - Testing framework
- pytest-cov >= 5.0.0, < 6.0 - Coverage reporting

**Existing Patterns to Follow:**
- Use `Path(__file__).parent.parent` for relative path resolution in tests
- All callbacks need type hints: `def callback(status: dict) -> None:`
- Pydantic models use `model_config = ConfigDict(frozen=False)` for mutability

### References

- [Source: docs/tech-spec-epic-1.md#Story-1.4] - Acceptance criteria, technical requirements, data model specifications
- [Source: docs/epics.md#Epic-1-Story-1.4] - User story statement, success criteria
- [Source: docs/architecture.md] - Architectural patterns and constraints (ADR-002: Pydantic v2, ADR-003: File-based storage, ADR-005: Streaming pipeline)
- [Source: docs/PRD.md#Pipeline-Architecture] - Business context for modular pipeline design
- [Source: stories/1-3-testing-framework-and-ci-pipeline.md] - Testing infrastructure and patterns established

## Dev Agent Record

### Context Reference

- docs/stories/1-4-core-pipeline-architecture-pattern.context.xml

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

**Story 1.4 Implementation Completed Successfully**

**Summary:**
Successfully implemented the core pipeline architecture pattern with comprehensive data models, exception handling, and testing infrastructure. All acceptance criteria met with 100% test coverage on core modules.

**Key Accomplishments:**
1. **Data Models (AC-1.4.3):** Implemented all 5 Pydantic v2 models with field validation constraints
   - Entity, Metadata, Document, Chunk models with proper validation (confidence: 0.0-1.0, quality_score: 0.0-1.0)
   - ProcessingContext model for shared pipeline state (config, logger, metrics)

2. **Pipeline Architecture (AC-1.4.1, AC-1.4.5):** Defined Protocol-based pipeline interface with Generic typing
   - PipelineStage[Input, Output] Protocol ensures type-safe pipeline composition
   - Pipeline orchestrator class chains stages with automatic data flow
   - Supports both pipeline and single-command execution patterns

3. **Exception Hierarchy (AC-1.4.6):** Comprehensive error handling strategy
   - ProcessingError (recoverable) for continue-on-error batch processing
   - CriticalError (unrecoverable) for halt-immediately scenarios
   - ConfigurationError, ExtractionError, ValidationError with usage guidance

4. **Module Structure (AC-1.4.2):** Created placeholder modules for future pipeline stages
   - extract/, normalize/, chunk/, semantic/, output/ with descriptive docstrings
   - All modules importable and tested

5. **Documentation (AC-1.4.7):** Updated architecture.md with implementation patterns
   - Pipeline Stage Pattern with example code
   - Error Handling Pattern with batch processing examples
   - Core Data Models with type contracts documented

6. **Testing (AC-1.4.4, AC-1.4.5):** Comprehensive test coverage achieved
   - 93 total tests (77 unit, 16 integration)
   - 100% coverage on all core modules (models.py, pipeline.py, exceptions.py)
   - All tests pass mypy, black, ruff quality gates

**Quality Metrics:**
- Test Coverage: 100% (72/72 statements in core modules)
- Test Suite: 93 tests, 0 failures
- Type Checking: mypy passes with --explicit-package-bases
- Code Formatting: black compliant (line length 100)
- Linting: ruff passes all checks

**Technical Decisions:**
- Used `arbitrary_types_allowed=True` for ProcessingContext to support structlog logger types
- Used `frozen=False` for all models to support mutability (required for metrics accumulation)
- Protocol-based design (not ABC) for PipelineStage to enable duck typing and flexibility
- Contravariant/Covariant type variables for proper Generic type safety

**Next Steps (Future Epics):**
- Epic 2: Implement extraction and normalization stages
- Epic 3: Implement chunking and output formatting stages
- Epic 4: Implement semantic analysis stages
- All future stages will implement PipelineStage[Input, Output] protocol established in this story

### File List

**New Files Created:**
- `src/data_extract/core/models.py` - Pydantic v2 data models (Entity, Metadata, Document, Chunk, ProcessingContext)
- `src/data_extract/core/pipeline.py` - Pipeline architecture (PipelineStage Protocol, Pipeline orchestrator)
- `src/data_extract/core/exceptions.py` - Exception hierarchy (DataExtractError, ProcessingError, CriticalError, etc.)
- `src/data_extract/extract/__init__.py` - Extract module placeholder with docstring
- `src/data_extract/normalize/__init__.py` - Normalize module placeholder with docstring
- `src/data_extract/chunk/__init__.py` - Chunk module placeholder with docstring
- `src/data_extract/semantic/__init__.py` - Semantic module placeholder with docstring
- `src/data_extract/output/__init__.py` - Output module placeholder with docstring
- `tests/unit/core/test_models.py` - Unit tests for data models (24 tests, 100% coverage)
- `tests/unit/core/test_pipeline.py` - Unit tests for pipeline architecture (13 tests, 100% coverage)
- `tests/unit/core/test_exceptions.py` - Unit tests for exception hierarchy (31 tests, 100% coverage)
- `tests/unit/core/test_module_structure.py` - Unit tests for module structure (9 tests, 100% coverage)
- `tests/integration/test_pipeline_architecture.py` - Integration tests for end-to-end pipeline (16 tests)

**Modified Files:**
- `docs/architecture.md` - Updated Pipeline Stage Pattern, Error Handling Pattern, and Core Data Models sections with implementation references
