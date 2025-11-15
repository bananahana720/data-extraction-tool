# Story 3.4: JSON Output Format with Full Metadata

Status: ready-for-dev

## Story

As a **RAG engineer integrating document processing with vector databases**,
I want **chunks output in valid JSON format with complete metadata**,
so that **I can programmatically ingest, query, and filter chunks for downstream LLM retrieval workflows**.

## Context Summary

**Epic Context:** Story 3.4 implements the first of three output formats (JSON, TXT, CSV) in Epic 3. This story creates the JSON formatter that serializes enriched chunks with complete metadata, enabling programmatic consumption by vector databases, RAG systems, and analysis tools.

**Business Value:**
- Enables automated ingestion into vector databases (Pinecone, Weaviate, Chroma, FAISS)
- Provides queryable metadata for chunk filtering and prioritization (quality scores, entity tags, source traceability)
- Supports schema-driven validation (JSON Schema ensures output correctness)
- Enables programmatic analysis (jq queries, Python json.load(), pandas integration)
- Establishes foundation for by_document/by_entity/flat organization strategies (Story 3.7)

**Dependencies:**
- **Story 3.3 Complete (Chunk Metadata and Quality Scoring)** - Enriched chunks with QualityScore, ChunkMetadata operational
- **Story 3.2 Complete (Entity-Aware Chunking)** - Entity tags populated in chunks
- **Story 3.1 Complete (Semantic Chunking Engine)** - ChunkingEngine generates well-formed chunks
- **Epic 2 Complete (Extract & Normalize)** - Source metadata available for traceability

**Technical Foundation:**
- **Chunk Model (Stories 3.1-3.3):** Frozen dataclass with text, metadata, entities, quality fields
- **ChunkMetadata Model (Story 3.3):** Source traceability, section context, quality scores, word/token counts
- **QualityScore Model (Story 3.3):** Readability metrics, composite quality, flags
- **EntityReference Model (Story 3.2):** Entity type, ID, position, partial flag, context snippet

**Key Requirements:**
1. **Valid JSON Output:** Parsable by standard JSON libraries (not JSON Lines) (AC-3.4-2)
2. **Complete Metadata:** All ChunkMetadata fields serialized to JSON (AC-3.4-3)
3. **Pretty-Printed:** Human-readable formatting with indentation (AC-3.4-4)
4. **Queryable Structure:** Array of chunks enables jq filtering and pandas DataFrame conversion (AC-3.4-5)
5. **Schema Validation:** Output validates against JSON Schema (AC-3.4-7)
6. **Document Header:** Configuration and version information for reproducibility (AC-3.4-6)

## Acceptance Criteria

**AC-3.4-1: JSON Structure Includes Chunk Text and Metadata (P0 - Critical)**
- JSON root object contains:
  - `metadata` object: Document-level configuration and version info
  - `chunks` array: List of chunk objects with text and metadata
- Each chunk object includes:
  - `chunk_id`: Unique identifier (string)
  - `text`: Chunk content (string)
  - `metadata`: Nested ChunkMetadata object (all fields from Story 3.3)
  - `entities`: Array of EntityReference objects (from Story 3.2)
  - `quality`: Nested QualityScore object (from Story 3.3)
- **Validation:** Unit tests verify structure matches schema, integration tests verify completeness
- **UAT Required:** Yes - Schema validation against real chunk data

**AC-3.4-2: Output is Valid, Parsable JSON (Not JSON Lines) (P0 - Critical)**
- Single JSON file per output (not newline-delimited JSON Lines format)
- Valid according to JSON specification (RFC 8259)
- Parsable by: Python json.load(), jq, Node.js JSON.parse(), pandas.read_json()
- UTF-8 encoding with BOM for Windows compatibility
- **Validation:** Unit tests parse output with multiple libraries, integration tests verify no corruption
- **UAT Required:** Yes - Critical for downstream tool compatibility

**AC-3.4-3: Metadata Includes All Fields from ChunkMetadata (P1)**
- Each chunk's metadata object includes all fields:
  - `chunk_id`, `source_file`, `source_hash`, `document_type`
  - `section_context`, `position_index`, `entity_tags`
  - `quality` (nested QualityScore with all subfields)
  - `word_count`, `token_count`, `created_at`, `processing_version`
- Fields never null (empty string or empty array for missing data)
- Datetime fields formatted as ISO 8601 strings (e.g., "2025-11-14T20:37:23Z")
- **Validation:** Schema validation tests, completeness tests
- **UAT Required:** No - Covered by unit/schema tests

**AC-3.4-4: JSON is Pretty-Printed (Human Readable) (P2)**
- Output formatted with 2-space indentation (standard JSON convention)
- Fields ordered logically: text first, then metadata, then entities, then quality
- No trailing commas (strict JSON compliance)
- Line length reasonable for diff tools (<120 chars per line preferred)
- **Validation:** Visual inspection during development, linting tests
- **UAT Required:** No - Development-time validation sufficient

**AC-3.4-5: Array of Chunks Filterable/Queryable (P0 - Critical)**
- Chunks stored as JSON array (not object with chunk IDs as keys)
- Supports jq filtering: `.chunks[] | select(.quality.overall >= 0.75)`
- Supports pandas: `df = pd.read_json(path).explode('chunks')`
- Supports JavaScript: `chunks.filter(c => c.quality.overall >= 0.75)`
- Index-based access: `chunks[0]` returns first chunk
- **Validation:** Integration tests with jq queries, pandas DataFrame conversion
- **UAT Required:** Yes - Critical for programmatic filtering

**AC-3.4-6: Configuration and Version in JSON Header (P1)**
- Root `metadata` object includes:
  - `processing_version`: Tool version (e.g., "1.0.0-epic3")
  - `processing_timestamp`: ISO 8601 timestamp of processing
  - `configuration`: Nested object with chunking parameters
    - `chunk_size`: Target chunk size (tokens)
    - `overlap_pct`: Overlap percentage (0.0-0.5)
    - `entity_aware`: Boolean flag
    - `quality_enrichment`: Boolean flag
  - `source_documents`: Array of source file paths processed
  - `chunk_count`: Total number of chunks in file
- Configuration enables reproducibility (rerun with same settings)
- **Validation:** Unit tests verify header structure, integration tests verify accuracy
- **UAT Required:** No - Covered by unit tests

**AC-3.4-7: JSON Validates Against Schema (P0 - Critical)**
- JSON output validates against `data-extract-chunk.schema.json` (JSON Schema Draft 7)
- Schema defines:
  - Required fields and types for all nested objects
  - Enum values for document_type, entity_type, quality flags
  - Numeric ranges for quality scores (0.0-1.0), readability scores (0.0-30.0)
  - String patterns for chunk_id, source_hash (SHA-256 hex)
- Schema validation integrated into unit tests (every test validates against schema)
- Schema file versioned alongside code (schema changes tracked in git)
- **Validation:** Unit tests use jsonschema library, integration tests validate 100-chunk samples
- **UAT Required:** Yes - Critical for downstream tool integration

## Acceptance Criteria Trade-offs and Deferrals

**AC-3.4-2 Format Choice (JSON vs JSON Lines):**
- **Issue:** JSON Lines more streaming-friendly for large outputs
- **Resolution:** Single JSON file chosen for human readability and tooling compatibility
- **Rationale:** Most downstream tools (jq, pandas, vector DBs) prefer single JSON
- **Future:** Add JSON Lines format in Epic 5 if streaming use cases emerge
- **Documented In:** Dev Notes, JsonFormatter docstring

**AC-3.4-4 Field Ordering:**
- **Issue:** JSON spec doesn't guarantee field order (object keys unordered)
- **Resolution:** Python 3.7+ dicts maintain insertion order, use OrderedDict if needed
- **Rationale:** Consistent order improves human readability and diff stability
- **Documented In:** JsonFormatter implementation comments

**AC-3.4-6 Configuration Scope:**
- **Issue:** Full configuration cascade not available until Epic 5
- **Resolution:** Include only chunking-specific configuration (chunk_size, overlap_pct, flags)
- **Rationale:** Epic 5 will add CLI-level config; for now, include what's available
- **Documented In:** Dev Notes, Epic 5 backlog

**No Deferrals:** All ACs critical for MVP JSON output format.

## Tasks / Subtasks

### Task 1: Create JSON Schema Definition (AC: #3.4-7)
- [ ] Create `src/data_extract/output/schemas/` directory
- [ ] Create `data-extract-chunk.schema.json` (JSON Schema Draft 7)
  - [ ] Define root object schema (metadata + chunks array)
  - [ ] Define metadata object schema (version, timestamp, configuration, sources)
  - [ ] Define chunk object schema (chunk_id, text, metadata, entities, quality)
  - [ ] Define ChunkMetadata schema (all fields from Story 3.3)
  - [ ] Define QualityScore schema (readability, ocr, completeness, coherence, overall, flags)
  - [ ] Define EntityReference schema (entity_type, entity_id, positions, is_partial)
  - [ ] Add enum definitions for document_type, entity_type, quality flags
  - [ ] Add validation rules: score ranges, string patterns, required fields
- [ ] Add JSON Schema to package manifest (include in distribution)
- [ ] Add type hints for schema validation function

### Task 2: Implement JsonFormatter Component (AC: #3.4-1, #3.4-2, #3.4-3, #3.4-4, #3.4-5, #3.4-6)
- [ ] Create `src/data_extract/output/formatters/` directory
- [ ] Create `src/data_extract/output/formatters/base.py`
  - [ ] Define `BaseFormatter` Protocol
    - [ ] Method: `format_chunks(chunks: Iterator[Chunk], output_path: Path) -> FormatResult`
  - [ ] Define `FormatResult` dataclass (frozen=True)
    - [ ] Fields: format_type, output_path, chunk_count, file_size_bytes, duration_seconds, errors
- [ ] Create `src/data_extract/output/formatters/json_formatter.py`
  - [ ] Implement `JsonFormatter` class
    - [ ] Constructor: `__init__(self, schema_path: Optional[Path] = None, validate: bool = True)`
    - [ ] Method: `format_chunks(chunks: Iterator[Chunk], output_path: Path) -> FormatResult`
      - [ ] Build root metadata object (version, timestamp, configuration)
      - [ ] Collect chunks into array (materialize iterator - required for JSON)
      - [ ] Serialize each chunk using Chunk.to_dict()
      - [ ] Create final JSON structure {metadata: {...}, chunks: [...]}
      - [ ] Write JSON with indent=2 (pretty-print)
      - [ ] Validate against schema if validate=True
      - [ ] Return FormatResult with stats
    - [ ] Method: `_build_metadata_header(chunks: List[Chunk]) -> dict`
      - [ ] Extract processing version from package metadata
      - [ ] Generate ISO 8601 timestamp
      - [ ] Build configuration dict (chunk_size, overlap_pct from first chunk metadata)
      - [ ] Extract unique source files from chunks
      - [ ] Return metadata dict
    - [ ] Method: `_validate_against_schema(json_data: dict) -> List[str]`
      - [ ] Load JSON Schema from schema_path
      - [ ] Validate json_data using jsonschema library
      - [ ] Return list of validation errors (empty if valid)
  - [ ] Add comprehensive docstrings (Google style)
  - [ ] Add type hints (mypy strict mode compliant)
- [ ] Update `src/data_extract/output/__init__.py`
  - [ ] Export JsonFormatter, BaseFormatter, FormatResult

### Task 3: Extend Chunk Model Serialization (AC: #3.4-1, #3.4-3)
- [ ] Update `Chunk.to_dict()` in `src/data_extract/chunk/models.py`
  - [ ] Serialize chunk_id, text
  - [ ] Serialize metadata using ChunkMetadata.to_dict()
  - [ ] Serialize entities using [e.to_dict() for e in entities]
  - [ ] Serialize quality using QualityScore.to_dict()
  - [ ] Ensure datetime fields formatted as ISO 8601 strings
  - [ ] Ensure Path fields converted to strings
  - [ ] Return OrderedDict with consistent field order (text, metadata, entities, quality)
- [ ] Update `ChunkMetadata.to_dict()` (if not already implemented in Story 3.3)
  - [ ] Serialize all fields
  - [ ] Convert source_file Path to string
  - [ ] Format created_at as ISO 8601
  - [ ] Serialize quality as nested dict
- [ ] Update `QualityScore.to_dict()` (already implemented in Story 3.3, verify)
  - [ ] Ensure all numeric fields included
  - [ ] Ensure flags array serialized correctly
- [ ] Update `EntityReference.to_dict()` (from Story 3.2, verify)
  - [ ] Ensure all position fields included
  - [ ] Ensure is_partial boolean serialized

### Task 4: Unit Testing - JsonFormatter and Schema (AC: #3.4-1, #3.4-2, #3.4-3, #3.4-4, #3.4-5, #3.4-6, #3.4-7)
- [ ] Create `tests/unit/test_output/test_json_formatter.py`
  - [ ] Test JSON structure creation (metadata + chunks array)
  - [ ] Test metadata header generation (version, timestamp, configuration, sources)
  - [ ] Test chunk serialization (all fields present)
  - [ ] Test pretty-printing (indentation, no trailing commas)
  - [ ] Test UTF-8 encoding (non-ASCII text handling)
  - [ ] Test schema validation (valid output passes, invalid output caught)
  - [ ] Test empty chunks list (valid JSON, zero chunks)
  - [ ] Test single chunk (minimal valid output)
  - [ ] Test 100+ chunks (large output handling)
  - [ ] Test error handling (invalid chunks, missing fields)
- [ ] Create `tests/unit/test_output/test_json_schema.py`
  - [ ] Test schema loads correctly (valid JSON Schema Draft 7)
  - [ ] Test schema validates valid chunk JSON
  - [ ] Test schema rejects invalid JSON (missing required fields)
  - [ ] Test schema rejects out-of-range values (scores <0 or >1)
  - [ ] Test schema validates enum fields (document_type, quality flags)
  - [ ] Test schema validates string patterns (chunk_id, source_hash)
- [ ] Use fixtures from `tests/fixtures/chunks/` (sample enriched chunks from Story 3.3)
- [ ] Achieve >90% coverage for json_formatter.py

### Task 5: Integration Testing - End-to-End JSON Generation (AC: all)
- [ ] Create `tests/integration/test_output/test_json_output_pipeline.py`
  - [ ] Test complete pipeline: ProcessingResult → ChunkingEngine → JsonFormatter → JSON file
  - [ ] Test JSON parsing with multiple libraries:
    - [ ] Python json.load()
    - [ ] pandas.read_json()
    - [ ] jq command-line (via subprocess)
  - [ ] Test chunk queryability:
    - [ ] jq filter by quality: `.chunks[] | select(.quality.overall >= 0.75)`
    - [ ] jq filter by entity: `.chunks[] | select(.entities[].entity_type == "risk")`
    - [ ] pandas DataFrame conversion and filtering
  - [ ] Test metadata accuracy:
    - [ ] Verify source_documents list matches input files
    - [ ] Verify chunk_count matches actual chunks
    - [ ] Verify configuration reflects actual chunking params
  - [ ] Test schema validation on real output
  - [ ] Test file size and chunk count correctness
  - [ ] Test determinism (same input → same JSON output byte-for-byte)
- [ ] Create `tests/integration/test_output/test_json_compatibility.py`
  - [ ] Test UTF-8 encoding with special characters (emoji, accents, CJK)
  - [ ] Test large chunk text (>10KB per chunk)
  - [ ] Test deeply nested entity structures
  - [ ] Test Windows/Linux path compatibility (source_file paths)
- [ ] Use real document samples from `tests/fixtures/normalized_results/`
- [ ] Measure JSON generation performance (<1 second per document)

### Task 6: Performance Testing - JSON Generation Overhead (AC: NFR-P1-E3)
- [ ] Create `tests/performance/test_json_performance.py`
  - [ ] Benchmark JSON generation for 100-chunk document
  - [ ] Benchmark JSON generation for 1000-chunk document
  - [ ] Measure memory usage during JSON serialization (should not double memory)
  - [ ] Measure file I/O time (write latency)
  - [ ] Compare performance: validation enabled vs disabled
- [ ] Update `docs/performance-baselines-epic-3.md`
  - [ ] Add JSON generation baseline (<1 second per document target)
  - [ ] Document memory overhead (materialization cost)
  - [ ] Track against NFR-P1-E3 (<10 min total pipeline)
- [ ] Validate performance acceptable for MVP (<1 second per document)

### Task 7: Documentation and Validation (AC: all)
- [ ] Update `CLAUDE.md`
  - [ ] Document JsonFormatter usage patterns
  - [ ] Document JSON schema location and validation
  - [ ] Add jq query examples for common filtering
  - [ ] Document pandas integration examples
  - [ ] Update Epic 3 section with JSON output configuration
- [ ] Update `docs/architecture.md`
  - [ ] Document JSON output format decision (single JSON vs JSON Lines)
  - [ ] Document schema validation approach
  - [ ] Update Epic 3 component diagram (add JsonFormatter)
- [ ] Create `docs/json-schema-reference.md`
  - [ ] Document complete JSON schema structure
  - [ ] Provide example valid JSON output
  - [ ] List all enum values and their meanings
  - [ ] Explain validation rules and constraints
- [ ] Run all quality gates:
  - [ ] `black src/ tests/` → 0 violations
  - [ ] `ruff check src/ tests/` → 0 violations
  - [ ] `mypy src/data_extract/` → 0 violations (run from project root)
  - [ ] `pytest -m unit tests/unit/test_output/` → All pass
  - [ ] `pytest -m integration tests/integration/test_output/` → All pass
  - [ ] `pytest -m performance tests/performance/test_json_performance.py` → Performance acceptable
- [ ] Validate all 7 ACs end-to-end:
  - [ ] AC-3.4-1: JSON structure (integration tests)
  - [ ] AC-3.4-2: Valid JSON (parser tests, UAT)
  - [ ] AC-3.4-3: Complete metadata (schema tests)
  - [ ] AC-3.4-4: Pretty-printed (visual inspection)
  - [ ] AC-3.4-5: Queryable (jq tests, UAT)
  - [ ] AC-3.4-6: Configuration header (unit tests)
  - [ ] AC-3.4-7: Schema validation (schema tests, UAT)
- [ ] Mark story ready for review

## Dev Notes

### Architecture Patterns and Constraints

**JSON Format Choice (Single JSON vs JSON Lines):**
- **Context:** Two common JSON formats for array data - single JSON file vs newline-delimited JSON Lines
- **Decision:** Single JSON file with array of chunks
- **Rationale:**
  - Human readability: JSON arrays easier to inspect manually
  - Tool compatibility: jq, pandas, most vector DBs expect single JSON
  - Schema validation: JSON Schema works naturally with single documents
  - File size manageable: Typical document produces <10MB JSON (100-500 chunks)
- **Trade-off:** JSON Lines better for streaming and very large outputs (100K+ chunks)
- **Future Enhancement:** Add JSON Lines formatter in Epic 5 if streaming use cases emerge
- **Documented In:** ADR-012 (to be created)

**Chunk Materialization Requirement:**
- **Context:** JsonFormatter must materialize full chunk iterator (no streaming possible)
- **Decision:** Collect all chunks into list before JSON serialization
- **Rationale:** JSON array format requires complete collection before writing
- **Memory Impact:** ~2x memory during JSON generation (chunk objects + serialized JSON)
- **Mitigation:** Memory pooling from Story 3.3 reduces per-chunk overhead, Python garbage collection releases chunk objects after serialization
- **Acceptable Because:** Typical documents produce <500 chunks (~50MB materialized), well within NFR-P2-E3 memory budget

**Schema Validation Strategy:**
- **Context:** Schema validation adds overhead (~10-50ms per document)
- **Decision:** Validation enabled by default, optional via constructor parameter `validate=False`
- **Rationale:**
  - Development/testing: Always validate (catch bugs early)
  - Production: Disable for performance if validation confidence high
  - CI/UAT: Always validate (quality gate)
- **Implementation:** `JsonFormatter(validate=True)` constructor parameter

**Field Ordering for Diff Stability:**
- **Context:** JSON spec doesn't guarantee object key order, but Python 3.7+ dicts maintain insertion order
- **Decision:** Use consistent field order in serialization (text, metadata, entities, quality)
- **Rationale:** Stable field order improves git diff readability, aids manual inspection
- **Implementation:** OrderedDict or careful dict construction to control order

**UTF-8 Encoding with BOM:**
- **Context:** Windows tools sometimes require BOM for UTF-8 detection
- **Decision:** Write JSON with UTF-8 encoding, include BOM for Windows compatibility
- **Rationale:** Ensures Excel, Notepad, PowerShell correctly detect encoding
- **Implementation:** `open(file, 'w', encoding='utf-8-sig')` (sig = BOM)

**Data Model Immutability:**
- Consistent with Stories 3.1-3.3: `@dataclass(frozen=True)` for all models
- JsonFormatter does not mutate chunks (read-only serialization)
- FormatResult is frozen (immutable output metadata)

### Learnings from Previous Story

**From Story 3.3 (Chunk Metadata and Quality Scoring) (Status: done)**

**Completion Status:** Story 3.3 completed 2025-11-14. All 8 ACs validated, 109/109 tests passing (97 unit + 12 integration), code review approved, UAT approved, quality gates GREEN (black/ruff/mypy 0 violations), NFR-P3 satisfied (4.6s < 5.0s per 10k words).

**New Services Created:**
- `QualityScore` at `src/data_extract/chunk/quality.py` - Use QualityScore.to_dict() for JSON serialization
- `MetadataEnricher` at `src/data_extract/chunk/metadata_enricher.py` - Quality calculation pipeline
- `ProcessingResult` model extended in `src/data_extract/core/models.py` - Epic 2/3 boundary model

**Architectural Decisions:**
- **Weighted Quality Scoring:** OCR 40%, Completeness 30%, Coherence 20%, Readability 10%
- **Quality Flag Specificity:** Flags identify specific issues (low_ocr, incomplete_extraction, high_complexity, gibberish)
- **Token Count Approximation:** `len(text) / 4` heuristic (±5% accuracy, no tokenizer dependency)
- **Lexical Overlap Coherence:** Simple sentence-to-sentence word intersection (Epic 4 will add TF-IDF)

**Files to EXTEND (not recreate):**
- `src/data_extract/chunk/models.py` - Verify Chunk.to_dict() includes quality serialization (Task 3)
- `src/data_extract/output/__init__.py` - Add JsonFormatter exports (Task 2)

**Files to CREATE:**
- `src/data_extract/output/formatters/base.py` - NEW protocol module (Task 2)
- `src/data_extract/output/formatters/json_formatter.py` - NEW formatter (Task 2)
- `src/data_extract/output/schemas/data-extract-chunk.schema.json` - NEW schema (Task 1)
- `tests/unit/test_output/test_json_formatter.py` - NEW test file (Task 4)
- `tests/unit/test_output/test_json_schema.py` - NEW test file (Task 4)
- `tests/integration/test_output/test_json_output_pipeline.py` - NEW test file (Task 5)
- `tests/integration/test_output/test_json_compatibility.py` - NEW test file (Task 5)
- `tests/performance/test_json_performance.py` - NEW performance test (Task 6)

**Serialization Methods Available (from Story 3.3):**
- `Chunk.to_dict()` - Main serialization entry point
- `ChunkMetadata.to_dict()` - Metadata serialization
- `QualityScore.to_dict()` - Quality metrics serialization
- `EntityReference.to_dict()` - Entity serialization (Story 3.2)
- **Verify All Methods:** Ensure all to_dict() methods format datetimes as ISO 8601, Path objects as strings

**Performance Baselines (from Stories 3.1-3.3):**
- Chunking latency: ~0.19s per 1,000 words (Story 3.1)
- Entity analysis overhead: ~0.3s per 10k words (Story 3.2)
- Quality enrichment overhead: ~0.5s per 10k words (Story 3.3)
- Total current latency: ~4.6s per 10k words
- **Target for Story 3.4:**
  - JSON generation: <1.0s per document (typical 100-500 chunks)
  - Memory overhead: <100MB during serialization (materialization + JSON string)
  - Total latency: ~5.6s per 10k words (still within NFR-P1-E3 budget)

**Testing Patterns:**
- Use `tests/fixtures/chunks/` for enriched chunk fixtures (created in Story 3.3)
- Follow Story 3.3 test organization: unit (>90% coverage), integration (end-to-end), performance (NFR validation)
- JSON validation: Use jsonschema library, test with real downstream tools (jq, pandas)
- Use pytest markers: `-m unit`, `-m integration`, `-m performance`, `-m output`

**Quality Gates (0 violations required):**
1. `black src/ tests/` → 0 violations
2. `ruff check src/ tests/` → 0 violations
3. `mypy src/data_extract/` → 0 violations (MUST run from project root)
4. `pytest -m unit` → All pass
5. Fix violations IMMEDIATELY, do not defer to later stories

[Source: docs/stories/3-3-chunk-metadata-and-quality-scoring.md#Dev-Agent-Record, #Completion-Notes]

### Source Tree Components to Touch

**Files to MODIFY (Documentation):**
- `CLAUDE.md` - Add JSON output documentation
- `docs/architecture.md` - Document JSON format decision
- `docs/performance-baselines-epic-3.md` - Add JSON generation baselines
- `src/data_extract/output/__init__.py` - Export new formatters

**Files to CREATE (Greenfield - src/data_extract/output/):**
- `src/data_extract/output/formatters/base.py` - BaseFormatter protocol, FormatResult model (PRIMARY)
- `src/data_extract/output/formatters/json_formatter.py` - JsonFormatter implementation (PRIMARY)
- `src/data_extract/output/schemas/data-extract-chunk.schema.json` - JSON Schema definition (PRIMARY)

**Files to VERIFY/EXTEND (Chunk Serialization):**
- `src/data_extract/chunk/models.py` - Verify Chunk.to_dict(), ChunkMetadata.to_dict() complete (Task 3)

**Files to CREATE (Testing):**
- `tests/unit/test_output/test_json_formatter.py` - JsonFormatter unit tests
- `tests/unit/test_output/test_json_schema.py` - Schema validation tests
- `tests/integration/test_output/test_json_output_pipeline.py` - End-to-end JSON generation
- `tests/integration/test_output/test_json_compatibility.py` - Cross-platform compatibility
- `tests/performance/test_json_performance.py` - JSON generation performance baselines

**Files to CREATE (Documentation):**
- `docs/json-schema-reference.md` - Complete schema documentation with examples

**No Changes to Brownfield Code:**
- Epic 3 remains pure greenfield development
- All new components in `src/data_extract/output/`

### Key Patterns and Anti-Patterns

**Pattern: Protocol-Based Formatters (ADOPT)**
- Define BaseFormatter Protocol for all output formats (JSON, TXT, CSV)
- Enables polymorphic format selection: `formatter.format_chunks(chunks, path)`
- Simplifies testing (protocol-compliant mocks)
- Future extensibility (add new formats without modifying existing code)
- Example: `def format_chunks(chunks: Iterator[Chunk], output_path: Path) -> FormatResult`

**Pattern: Schema-Driven Validation (ADOPT)**
- JSON Schema as source of truth for output structure
- Schema versioned alongside code (git tracking)
- Validation integrated into unit tests (every test validates against schema)
- Enables downstream tool integration (vector DBs can consume schema)
- Example: `jsonschema.validate(json_data, schema)` in every test

**Pattern: Metadata Header Consistency (ADOPT)**
- All output formats include metadata header (version, timestamp, configuration)
- Enables reproducibility (track which tool version generated output)
- Supports debugging (timestamps, source files, configuration)
- Example: `{"metadata": {"processing_version": "1.0.0", ...}, "chunks": [...]}`

**Pattern: Deterministic Serialization (ADOPT)**
- Consistent field ordering (text, metadata, entities, quality)
- Sorted arrays where order not semantically meaningful (e.g., entity_tags by position)
- Deterministic chunk_id generation (source file + position, no timestamps)
- Enables diff-based change detection and testing
- Example: Same input → byte-identical JSON output (excluding metadata.processing_timestamp)

**Anti-Pattern: Hardcoded Schema in Code (AVOID)**
- **Problem:** Schema embedded as Python dict/class limits reusability
- **Solution:** External JSON Schema file, loaded at runtime
- **Benefit:** Schema shareable with downstream tools, version-controlled, language-agnostic

**Anti-Pattern: Silent Validation Failures (AVOID)**
- **Problem:** Schema validation errors swallowed without visibility
- **Solution:** Raise descriptive exceptions with specific validation errors
- **Example:** `jsonschema.ValidationError: 'quality.overall' 1.5 exceeds maximum of 1.0`
- **Benefit:** Debugging transparency, early error detection

**Anti-Pattern: Ignoring Encoding Issues (AVOID)**
- **Problem:** Non-ASCII text causes UnicodeEncodeError or mojibake
- **Solution:** Always use UTF-8 encoding with explicit declaration
- **Implementation:** `open(file, 'w', encoding='utf-8-sig')` + JSON ensure_ascii=False
- **Benefit:** Global compatibility (emoji, accents, CJK characters work correctly)

**Anti-Pattern: Unbounded Memory Growth (AVOID)**
- **Problem:** Large outputs (1000+ chunks) consume excessive memory during serialization
- **Solution:** While JSON requires materialization, release chunk objects immediately after to_dict()
- **Mitigation:** Python garbage collection, memory pooling from Story 3.3
- **Future:** JSON Lines format in Epic 5 for streaming large outputs

### Testing Strategy

**Test Organization (Mirror src/ Structure):**
```
tests/
├── unit/test_output/                  # Fast, isolated tests
│   ├── test_json_formatter.py         # JsonFormatter logic (NEW)
│   └── test_json_schema.py            # Schema validation (NEW)
├── integration/test_output/           # Multi-component tests
│   ├── test_json_output_pipeline.py   # End-to-end JSON generation (NEW)
│   └── test_json_compatibility.py     # Cross-tool compatibility (NEW)
├── performance/                       # Performance baselines
│   └── test_json_performance.py       # JSON generation overhead (NEW)
└── fixtures/
    └── chunks/                        # Enriched chunk samples (from Story 3.3)
```

**Unit Test Coverage (>90% Target):**
- JsonFormatter class: 100% coverage
  - format_chunks() method: all code paths
  - _build_metadata_header(): various chunk configurations
  - _validate_against_schema(): valid and invalid cases
- JSON Schema: comprehensive validation
  - Valid chunk JSON passes
  - Invalid JSON rejected with specific errors
  - Edge cases: empty arrays, null vs missing fields, out-of-range values

**Integration Test Coverage:**
- End-to-end pipeline: ProcessingResult → Chunks → JSON file
- Cross-library compatibility: json.load(), pandas.read_json(), jq
- Real document samples: varied complexity, entity counts, quality distributions
- Performance validation: <1 second per document

**Performance Test Coverage:**
- JSON generation latency (100-chunk, 1000-chunk documents)
- Memory usage during serialization (peak RSS, garbage collection effectiveness)
- File I/O overhead (write latency)
- Validation overhead (enabled vs disabled)

**UAT Test Coverage (Manual + Automated):**
- **AC-3.4-2 (Valid JSON):** Parse output with Python, Node.js, jq, pandas (CRITICAL)
- **AC-3.4-5 (Queryability):** jq filter tests, pandas DataFrame operations (CRITICAL)
- **AC-3.4-7 (Schema Validation):** Validate real output against schema (CRITICAL)
- Manual inspection: Pretty-printing quality, field ordering, encoding correctness

**Test Fixtures Required:**
- Sample enriched chunks (from Story 3.3 fixtures)
- Multi-document processing results (varied source files)
- Edge case chunks (very long text, many entities, low quality scores)
- Invalid chunk data (for schema validation negative tests)

### References

**Source Documents:**
- [PRD](C:\Users\Andrew\projects\data-extraction-tool-1\docs\PRD.md) - Business requirements, RAG optimization goals
- [Tech Spec Epic 3](C:\Users\Andrew\projects\data-extraction-tool-1\docs\tech-spec-epic-3.md#Story-3.4) - Story 3.4 acceptance criteria, JSON formatter design
- [Architecture](C:\Users\Andrew\projects\data-extraction-tool-1\docs\architecture.md) - Immutable models, protocol-based design
- [Story 3.3](C:\Users\Andrew\projects\data-extraction-tool-1\docs\stories\3-3-chunk-metadata-and-quality-scoring.md) - ChunkMetadata, QualityScore, serialization methods

**Technical References:**
- [JSON Specification (RFC 8259)](https://datatracker.ietf.org/doc/html/rfc8259) - JSON format standard
- [JSON Schema Draft 7](https://json-schema.org/draft-07/json-schema-release-notes.html) - Schema specification
- [Python jsonschema Library](https://python-jsonschema.readthedocs.io/) - Validation implementation

## Dev Agent Record

### Context Reference

- `docs/stories/3-4-json-output-format-with-full-metadata.context.xml` - Story context generated 2025-11-14

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
