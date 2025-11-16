# Infrastructure Needs Document

**Last Updated**: 2025-10-29 (Wave 1 - Agent 2: DocxExtractor Spike)

This document tracks infrastructure components discovered during module development that are needed for a production-ready system.

---

## Priority: CRITICAL

### INFRA-001: Configuration Management System
**Discovered During**: DocxExtractor implementation
**Need**: Centralized configuration for all extractors, processors, and formatters

**Current Situation**:
- Each module accepts `config: dict` in `__init__`
- No validation of config values
- No default config file
- No environment variable support
- Config is passed ad-hoc

**Requirements**:
```python
# Desired usage:
from config import ConfigManager

config = ConfigManager.load()  # Loads from file + env vars
extractor = DocxExtractor(config.get_extractor_config("docx"))

# Configuration should support:
# - Default values
# - Per-extractor overrides
# - Environment variable overrides
# - Validation (type checking, ranges)
# - Documentation (what each setting does)
```

**Config Settings Needed for DocxExtractor**:
- `max_paragraph_length` (int, optional) - Truncate long paragraphs
- `skip_empty` (bool, default: True) - Skip empty paragraphs
- `extract_styles` (bool, default: True) - Include style metadata
- `extract_tables` (bool, default: False) - Extract tables (future)
- `extract_images` (bool, default: False) - Extract images (future)

**Implementation Priority**: HIGH (needed before adding more extractors)

---

### INFRA-002: Logging Framework
**Discovered During**: DocxExtractor implementation
**Need**: Structured logging for debugging and monitoring

**Current Situation**:
- No logging in extractors
- Errors only captured in result objects
- No way to trace execution flow
- No performance metrics

**Requirements**:
```python
# Desired usage:
from logging_framework import get_logger

logger = get_logger(__name__)

def extract(self, file_path: Path):
    logger.info("Starting extraction", file=file_path, format="docx")
    # ... extraction logic ...
    logger.debug("Extracted paragraph", index=idx, length=len(text))
    # ... more logic ...
    logger.info("Extraction complete", blocks=len(content_blocks), duration=elapsed)
```

**Logging Levels Needed**:
- **DEBUG**: Per-block extraction details
- **INFO**: Start/end of extraction, summary stats
- **WARNING**: Recoverable issues (truncated paragraphs, missing metadata)
- **ERROR**: Extraction failures

**Features Needed**:
- Structured logging (JSON output for log aggregation)
- Configurable log levels per module
- Performance timing (automatic duration tracking)
- Context propagation (trace ID through pipeline)

**Implementation Priority**: HIGH (needed for production debugging)

---

### INFRA-003: Error Handling Patterns
**Discovered During**: DocxExtractor implementation
**Need**: Standardized error types and handling patterns

**Current Situation**:
- Generic error messages in tuple
- No error categorization
- No error codes
- No recovery guidance

**Requirements**:
```python
# Desired pattern:
from errors import ExtractionError, FileAccessError, CorruptedFileError

class DocxExtractor:
    def extract(self, file_path: Path):
        try:
            doc = Document(file_path)
        except FileNotFoundError:
            raise FileAccessError(
                file_path=file_path,
                error_code="DOCX-001",
                message="File not found",
                recoverable=False
            )
        except PermissionError:
            raise FileAccessError(
                file_path=file_path,
                error_code="DOCX-002",
                message="Permission denied",
                recoverable=False
            )
        except InvalidXmlError as e:
            raise CorruptedFileError(
                file_path=file_path,
                error_code="DOCX-003",
                message="Invalid DOCX structure",
                recoverable=False,
                details=str(e)
            )
```

**Error Categories Needed**:
1. **File Access Errors** - File not found, permission denied, file locked
2. **Corrupted File Errors** - Invalid format, corrupted structure
3. **Configuration Errors** - Invalid config values
4. **Processing Errors** - Unexpected content that breaks extraction
5. **Resource Errors** - Memory limits, disk space

**Error Attributes**:
- Error code (for documentation/troubleshooting)
- Message (human-readable)
- Recoverable flag (can retry?)
- Suggested action (what user should do)
- Original exception (for debugging)

**Implementation Priority**: MEDIUM (improves error messages)

---

### INFRA-004: Progress Tracking
**Discovered During**: DocxExtractor implementation
**Need**: Progress reporting for long-running operations

**Current Situation**:
- No progress indication
- No way to estimate completion time
- User doesn't know if process is stuck or working

**Requirements**:
```python
# Desired usage:
from progress import ProgressTracker

tracker = ProgressTracker(total_items=len(paragraphs))

for idx, paragraph in enumerate(doc.paragraphs):
    # ... process paragraph ...
    tracker.update(
        items_processed=idx + 1,
        current_item=f"Paragraph {idx}"
    )
    # Tracker automatically computes: ETA, items/sec, % complete
```

**Features Needed**:
- Progress percentage
- Items processed / total items
- Estimated time remaining
- Current item being processed
- Items per second (throughput)

**Use Cases**:
- Large DOCX files (100+ pages)
- Batch processing (multiple files)
- OCR operations (slow, per-page tracking)
- Image extraction (many images)

**Implementation Priority**: LOW (nice-to-have for UX)

---

## Priority: MEDIUM

### INFRA-005: Performance Monitoring
**Discovered During**: DocxExtractor testing
**Need**: Track extraction performance metrics

**Requirements**:
- Extraction duration per file
- Per-block extraction time
- Memory usage tracking
- Throughput metrics (MB/sec, pages/sec)

**Use Cases**:
- Identify performance bottlenecks
- Compare extractor performance
- Optimize slow operations
- Set SLA targets (e.g., <2s/MB)

**Implementation Priority**: MEDIUM (needed for optimization)

---

### INFRA-006: Validation Framework
**Discovered During**: DocxExtractor implementation
**Need**: Validate extraction results quality

**Requirements**:
```python
# Desired usage:
from validation import ResultValidator

validator = ResultValidator()
issues = validator.validate(extraction_result)

# Check for:
# - Empty content blocks
# - Missing position information
# - Invalid confidence scores
# - Truncated content without warning
# - Missing metadata
```

**Validation Rules**:
- Content blocks should have non-empty content (or be flagged)
- Position information should be sequential
- Confidence scores should be 0.0-1.0
- Metadata should include expected keys
- Word count should match actual words
- Character count should match actual length

**Implementation Priority**: MEDIUM (improves quality)

---

### INFRA-007: File Hash Caching
**Discovered During**: DocxExtractor implementation
**Need**: Cache file hashes to avoid recomputing

**Current Situation**:
- File hash computed on every extraction
- SHA256 computation is I/O intensive
- Same file extracted multiple times = redundant hashing

**Requirements**:
- Cache hash by (file_path, mtime, size)
- Invalidate cache when file changes
- Optional: persistent cache (survives restarts)

**Implementation Priority**: LOW (optimization, not critical)

---

### INFRA-008: Metadata Extraction Framework
**Discovered During**: DocxExtractor implementation
**Need**: Standardized metadata extraction across formats

**Current Situation**:
- Each extractor manually extracts metadata
- Inconsistent metadata keys across formats
- Some metadata available but not extracted

**Requirements**:
```python
# Desired pattern:
from metadata import MetadataExtractor

class DocxExtractor:
    def extract(self, file_path: Path):
        # ... extraction logic ...

        metadata_extractor = MetadataExtractor("docx")
        doc_metadata = metadata_extractor.extract(
            file_path=file_path,
            native_object=doc,  # python-docx Document
        )

        # Standardized metadata across all formats:
        # - title, author, created, modified, subject, keywords
        # - page_count, word_count, character_count
        # - language, content_summary
```

**Benefits**:
- Consistent metadata keys
- Single place to handle date parsing
- Format-specific metadata normalization
- Easier testing (mock metadata extractor)

**Implementation Priority**: MEDIUM (reduces duplication)

---

## Priority: LOW

### INFRA-009: Temp File Management
**Discovered During**: Thinking about image extraction
**Need**: Manage temporary files (extracted images, intermediate files)

**Requirements**:
- Create temp directories
- Clean up temp files automatically
- Handle temp file collisions
- Configurable temp directory location

**Implementation Priority**: LOW (needed later for images)

---

### INFRA-010: File Type Detection
**Discovered During**: Thinking about pipeline routing
**Need**: Detect file type beyond extension (magic bytes)

**Requirements**:
- Detect file type by content (magic bytes)
- Don't trust file extension alone
- Handle misnamed files (.doc renamed to .docx)
- Return confidence score

**Implementation Priority**: LOW (robustness, not critical for MVP)

---

## Decision: What to Build Next?

**Recommendation**: Build **INFRA-001 (Configuration Management)** first

**Reasoning**:
1. Needed immediately as we add more extractors
2. Prevents config parameter explosion
3. Establishes pattern for all modules
4. Relatively simple to implement
5. High impact on developer experience

**Alternative**: Continue with more extractors (PDF, PPTX) and defer infrastructure

**Trade-off**:
- **Defer infrastructure**: Faster short-term progress, but accumulates technical debt
- **Build infrastructure first**: Slower short-term, but cleaner long-term architecture

**User Decision Required**: Which approach do you prefer?

---

## Notes from DocxExtractor Implementation

### What Worked Well
✓ Immutable data models prevent bugs
✓ BaseExtractor interface is clean and sufficient
✓ ContentBlock is flexible (metadata dict handles format-specific data)
✓ ExtractionResult structure works well
✓ Error handling pattern (return result with success=False) is clear

### What Could Be Improved
- Configuration management is ad-hoc
- No logging makes debugging harder
- Error messages are generic strings
- No progress indication for large files
- Performance not tracked/optimized

### Future Enhancements for DocxExtractor
See comment tags in code:
- DOCX-TABLE-001: Extract tables
- DOCX-IMAGE-001: Extract images
- DOCX-HEADER-001: Extract headers/footers
- DOCX-STYLE-001: Extract detailed formatting
- DOCX-LIST-001: Detect and extract lists properly
- DOCX-META-001: Extract footnotes/comments

---

## Summary

**Critical Path**:
1. Configuration management (enables scalable extractor development)
2. Logging framework (enables debugging and monitoring)
3. Error handling patterns (improves error messages)

**Can Defer**:
- Progress tracking (UX improvement)
- Performance monitoring (optimization)
- Validation framework (quality improvement)
- File hash caching (optimization)
- Metadata extraction framework (code quality)

**Much Later**:
- Temp file management (needed for images)
- File type detection (robustness)

---

**End of Document**
