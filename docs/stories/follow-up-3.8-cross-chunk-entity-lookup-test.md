# Story: Add P1 Cross-Chunk Entity Lookup Test

**Epic:** Epic 3 - Chunk & Output
**Story ID:** 3.8 (Follow-up to Story 3.2)
**Priority:** P1 (HIGH)
**Effort:** 30 minutes
**Status:** todo

## Overview

Add explicit integration test validating cross-chunk entity lookup functionality. AC-3.2-5 (P1) requires that entity IDs enable cross-chunk queries, but current test coverage only validates EntityReference serialization without demonstrating actual cross-chunk lookup.

## Problem Statement

Entity IDs are included in ChunkMetadata.entity_tags to enable cross-chunk queries for RAG workflows. While EntityReference serialization is tested, there's no explicit test demonstrating that users can query for all chunks containing a specific entity_id. This gap leaves P1 RAG workflow functionality unvalidated.

## User Story

**As a** RAG system developer
**I want** explicit tests validating cross-chunk entity lookup
**So that** I have confidence that entity IDs enable cross-chunk queries as designed

## Acceptance Criteria

### AC-3.8-1 (P1 - Critical): Cross-Chunk Entity Lookup Validated
- **Given:** Document with large entity (>chunk_size) that splits across 2 chunks
- **When:** Entity-aware chunking performed
- **Then:** Entity appears in chunk 0 and chunk 1 with same entity_id
- **And:** Lookup function `find_chunks_by_entity_id(chunks, entity_id)` returns both chunks
- **UAT Required:** No (unit/integration test)

### AC-3.8-2 (P1): Multiple Entity Lookup
- **Given:** 3 entities ("RISK-001", "CTRL-042", "PROC-100") across 5 chunks
- **When:** Lookup performed for "RISK-001"
- **Then:** Only chunks containing "RISK-001" returned (not other entities)
- **UAT Required:** No

### AC-3.8-3 (P1): Entity Not Found Handling
- **Given:** Chunks with entities
- **When:** Lookup performed for non-existent entity_id "RISK-999"
- **Then:** Empty list returned (graceful handling)
- **UAT Required:** No

## Technical Approach

**Test File:** `tests/integration/test_chunk/test_entity_aware_chunking.py`

**Test Function:** `test_cross_chunk_entity_lookup`

**Implementation Steps:**
1. Create ProcessingResult with large entity (1500 tokens) that exceeds chunk_size (512 tokens)
2. Perform entity-aware chunking
3. Assert entity appears in multiple chunks (chunk 0 and chunk 1)
4. Implement helper function:
   ```python
   def find_chunks_by_entity_id(chunks: List[Chunk], entity_id: str) -> List[Chunk]:
       return [
           chunk for chunk in chunks
           if any(entity.entity_id == entity_id for entity in chunk.metadata.entity_tags)
       ]
   ```
5. Assert helper returns both chunks containing the entity
6. Test multiple entities and not-found case

**Test Pattern:**
```python
def test_cross_chunk_entity_lookup():
    # Given: Large entity splitting across chunks
    large_entity_text = "RISK-001: " + "risk description " * 300  # ~1500 tokens
    processing_result = create_processing_result_with_entity(
        entity_id="RISK-001",
        entity_text=large_entity_text
    )

    # When: Entity-aware chunking performed
    engine = ChunkingEngine(ChunkingConfig(chunk_size=512, entity_aware=True))
    chunks = list(engine.chunk(processing_result))

    # Then: Entity appears in multiple chunks
    assert len(chunks) >= 2
    chunk_0_entities = [e.entity_id for e in chunks[0].metadata.entity_tags]
    chunk_1_entities = [e.entity_id for e in chunks[1].metadata.entity_tags]
    assert "RISK-001" in chunk_0_entities
    assert "RISK-001" in chunk_1_entities

    # And: Lookup function returns both chunks
    found_chunks = find_chunks_by_entity_id(chunks, "RISK-001")
    assert len(found_chunks) == 2
    assert found_chunks[0].chunk_id == chunks[0].chunk_id
    assert found_chunks[1].chunk_id == chunks[1].chunk_id
```

## Definition of Done

- [ ] Test added to `tests/integration/test_chunk/test_entity_aware_chunking.py`
- [ ] All 3 acceptance criteria covered (cross-chunk, multiple entities, not found)
- [ ] Test passes in local pytest run
- [ ] Test passes in CI/CD pipeline
- [ ] Helper function `find_chunks_by_entity_id()` implemented and documented
- [ ] Traceability matrix updated (AC-3.2-5 coverage: PARTIAL → FULL)
- [ ] Pre-commit checks pass (black, ruff, mypy)

## Test Execution

```bash
# Run new test
pytest tests/integration/test_chunk/test_entity_aware_chunking.py::test_cross_chunk_entity_lookup -v

# Run all entity-aware tests
pytest tests/integration/test_chunk/test_entity_aware_chunking.py -v

# Coverage check
pytest tests/integration/test_chunk/test_entity_aware_chunking.py --cov=src/data_extract/chunk --cov-report=html
```

## Dependencies

- Epic 3 Story 3.2 (Entity-Aware Chunking) - COMPLETE
- EntityReference model - EXISTS
- ChunkMetadata.entity_tags field - EXISTS

## Risk Mitigation

**Risk:** Feature already implemented but not explicitly tested
**Mitigation:** This story validates existing functionality, no code changes required (test-only)
**Impact:** Reduces Risk Score from 2 → 0 for AC-3.2-5

## Related Artifacts

- Traceability Matrix: `docs/traceability-matrix-epic-3.md` (Gap 1)
- Story 3.2: `docs/stories/3-2-entity-aware-chunking.md`
- Test File: `tests/integration/test_chunk/test_entity_aware_chunking.py`

## Notes

This is a follow-up story to close the P1 gap identified in the Epic 3 traceability assessment. The feature is already implemented and working - this story adds explicit test coverage to validate the cross-chunk lookup use case for RAG workflows.

---

**Created:** 2025-11-17
**Workflow:** testarch-trace Phase 1 follow-up
**Agent:** Murat (TEA)
