# Story: 4-1 TF-IDF Vectorization Engine

## Story
**ID:** 4-1-tf-idf-vectorization-engine
**Epic:** 4 - Knowledge Curation via Classical NLP
**Title:** Implement TF-IDF Vectorization Engine with Caching
**Priority:** P0
**Estimate:** 13 hours

As a data scientist working with large document corpora, I want to convert chunks of text into TF-IDF vectors with intelligent caching, so that I can perform efficient similarity analysis and duplicate detection while reducing redundant computation by 10-100x.

## Acceptance Criteria

- [ ] **AC-4.1-1:** TfidfVectorizationStage implements PipelineStage protocol with process() method accepting List[Chunk] and returning ProcessingResult
- [ ] **AC-4.1-2:** Vectorizer configurable with max_features (5000 default), min_df (2), max_df (0.95), ngram_range (1,2), sublinear_tf (True)
- [ ] **AC-4.1-3:** Quality filtering removes chunks with quality_score < threshold (0.5 default) before vectorization
- [ ] **AC-4.1-4:** Cache manager with joblib persistence stores/retrieves vectorizers and sparse matrices using SHA256 content hashing
- [ ] **AC-4.1-5:** Performance meets NFR-P1: <100ms for 1000 words, <1s for 10k words, <500MB memory for 10k documents
- [ ] **AC-4.1-6:** Deterministic output: identical input produces identical vectors across runs (fixed random_state=42)
- [ ] **AC-4.1-7:** ProcessingResult includes tfidf_matrix (sparse CSR), vectorizer, vocabulary dict, feature_names array, chunk_ids
- [ ] **AC-4.1-8:** Cache hit ratio >90% after initial run on same corpus, with 10-100x speedup
- [ ] **AC-4.1-9:** All code passes mypy with zero errors and black/ruff with zero violations
- [ ] **AC-4.1-10:** Unit test coverage ≥95% with behavioral test for duplicate detection accuracy ≥85%

## Tasks/Subtasks

### Setup and Infrastructure
- [ ] Create src/data_extract/semantic/ module structure with __init__.py
- [ ] Define base SemanticStage abstract class implementing PipelineStage protocol
- [ ] Create cache manager singleton with joblib serialization support
- [ ] Set up .data-extract-cache/models/ directory structure

### TF-IDF Implementation
- [ ] Implement TfidfVectorizationStage class with configurable TfidfConfig
- [ ] Add quality filtering logic for chunk preprocessing
- [ ] Implement SHA256-based cache key generation from corpus content
- [ ] Add sparse matrix handling with scipy.sparse.csr_matrix
- [ ] Create ProcessingResult builder with all required metadata

### Caching Layer
- [ ] Implement CacheManager.get() and CacheManager.set() with joblib
- [ ] Add cache warming strategy for common configurations
- [ ] Implement cache size management with LRU eviction
- [ ] Add cache hit/miss metrics tracking
- [ ] Create cache corruption detection and recovery

### Performance Optimization
- [ ] Profile memory usage with 10k document corpus
- [ ] Implement batch processing for large corpora
- [ ] Add parallel processing option for multi-core systems
- [ ] Optimize vocabulary size with min/max document frequency

### Testing and Validation
- [ ] Create unit tests for TfidfVectorizationStage (95% coverage)
- [ ] Implement behavioral test for duplicate detection (≥85% precision)
- [ ] Add performance benchmarks validating NFR-P1 requirements
- [ ] Test determinism with multiple runs on same input
- [ ] Validate cache effectiveness metrics

### Integration and Quality
- [ ] Integrate with existing PipelineStage infrastructure
- [ ] Add CLI command: data-extract semantic tfidf
- [ ] Run mypy type checking (0 errors required)
- [ ] Apply black/ruff formatting (0 violations required)
- [ ] Update documentation with API reference

### Review Follow-ups (AI)
*To be added after code review*

## Dev Notes

### Implementation Strategy
- Use scikit-learn's TfidfVectorizer as the core engine (proven, fast, reliable)
- Leverage scipy.sparse for memory-efficient matrix operations
- Cache aggressively to enable team collaboration and reduce redundant computation
- Focus on determinism and reproducibility for scientific validity

### Performance Considerations
- Sparse matrices essential for memory efficiency (10k docs = 100M elements if dense)
- Block-wise processing for similarity computation to avoid memory overflow
- Consider memory-mapped arrays for very large corpora
- Profile with realistic audit document corpus (mix of PDFs, Excel, text)

### Integration Points
- Input: List[Chunk] from ChunkStage (Epic 3 output)
- Output: ProcessingResult with vectors for SimilarityAnalysisStage
- Side effects: Cached models in .data-extract-cache/
- Dependencies: scikit-learn>=1.3.0, joblib>=1.3.0, numpy, scipy

### Cache Strategy (ADR-012)
- Hash-based keys: tfidf_v1_[sha256[:8]].joblib
- Storage: .data-extract-cache/models/
- Max size: 500MB with LRU eviction
- Compression: joblib level 3 for space efficiency
- Invalidation: Content-based, automatic on corpus change

## Dev Agent Record

### Debug Log
*To be updated during implementation*

### Completion Notes
*To be updated after implementation*

### Context Reference
- docs/stories/4-1-tf-idf-vectorization-engine.context.xml (this file)

## File List
*To be updated with created/modified files*

## Change Log
- 2025-11-20: Story created for TF-IDF vectorization engine implementation

## Status
ready-for-dev