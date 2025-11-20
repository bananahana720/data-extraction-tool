# Story: 4-2 Document and Chunk Similarity Analysis

## Story
**ID:** 4-2-document-and-chunk-similarity-analysis
**Epic:** 4 - Knowledge Curation via Classical NLP
**Title:** Implement Document and Chunk Similarity Analysis Engine
**Priority:** P0
**Estimate:** 13 hours

As an audit analyst processing large document collections, I want to compute pairwise similarity between documents and chunks to identify duplicates and related content, so that I can reduce redundant processing by 30-40% and build relationship graphs for navigation.

## Acceptance Criteria

- [ ] **AC-4.2-1:** SimilarityAnalysisStage implements PipelineStage protocol accepting ProcessingResult from TF-IDF and returning enriched ProcessingResult
- [ ] **AC-4.2-2:** Compute pairwise cosine similarity for all document pairs using sparse matrix operations
- [ ] **AC-4.2-3:** Duplicate detection identifies near-duplicates with configurable threshold (default 0.95) achieving ≥85% precision
- [ ] **AC-4.2-4:** Build similarity graph with edges for relationships above threshold (default 0.7) for document navigation
- [ ] **AC-4.2-5:** Memory-efficient block-wise computation for matrices >1000 documents using configurable block size
- [ ] **AC-4.2-6:** Similarity matrix is symmetric (similarity(A,B) == similarity(B,A)) and deterministic
- [ ] **AC-4.2-7:** Performance meets NFR: <200ms for 100x100 matrix, <5s for 1000x1000 matrix, <500MB memory
- [ ] **AC-4.2-8:** Output includes similarity_matrix, similar_pairs list, and statistics (mean, std, max, count above threshold)
- [ ] **AC-4.2-9:** Cache similarity matrices using content-based keys with compression for space efficiency
- [ ] **AC-4.2-10:** All code passes mypy with zero errors and black/ruff with zero violations

## Tasks/Subtasks

### Core Implementation
- [ ] Create src/data_extract/semantic/similarity.py module
- [ ] Implement SimilarityAnalysisStage class with PipelineStage protocol
- [ ] Add cosine_similarity computation using sklearn.metrics.pairwise
- [ ] Implement sparse matrix handling for memory efficiency
- [ ] Create similarity statistics calculator (mean, std, max)

### Duplicate Detection
- [ ] Implement find_similar_pairs() method with threshold parameter
- [ ] Create duplicate groups identifier for transitive relationships
- [ ] Add configurable similarity thresholds (duplicate: 0.95, related: 0.7)
- [ ] Generate duplicate report with pair counts and savings estimate
- [ ] Validate precision/recall against golden dataset

### Memory Optimization
- [ ] Implement block-wise similarity computation for large matrices
- [ ] Add streaming mode for documents exceeding memory limits
- [ ] Use scipy.sparse operations throughout
- [ ] Implement matrix compression for cache storage
- [ ] Profile memory usage with 10k document corpus

### Graph Construction
- [ ] Build similarity graph using networkx or simple adjacency list
- [ ] Add edge weights for similarity scores
- [ ] Implement connected components for cluster identification
- [ ] Create graph traversal utilities for navigation
- [ ] Export graph in standard formats (GraphML, JSON)

### Integration
- [ ] Integrate with TF-IDF output (ProcessingResult chaining)
- [ ] Add similarity caching with joblib
- [ ] Implement cache key generation from TF-IDF matrix hash
- [ ] Create similarity report generator
- [ ] Add CLI command: data-extract semantic similarity

### Testing and Quality
- [ ] Create unit tests for SimilarityAnalysisStage (90% coverage)
- [ ] Implement behavioral test for duplicate detection accuracy
- [ ] Add performance benchmarks for various matrix sizes
- [ ] Test symmetry property of similarity matrix
- [ ] Validate memory usage stays within limits

### Review Follow-ups (AI)
*To be added after code review*

## Dev Notes

### Algorithm Selection
- Use scikit-learn's cosine_similarity for proven implementation
- Consider approximate methods (LSH) for very large corpora
- Sparse matrix operations essential for memory efficiency
- Block-wise computation prevents memory overflow

### Performance Optimization
- Similarity matrix is O(n²) space and time - must optimize
- Use symmetric property to compute only upper triangle
- Consider threshold-based sparsification (only store > 0.1)
- Parallel processing can speed up block computation

### Memory Management
- 10k documents = 100M element matrix = 400MB if float32
- Sparse storage only keeps values above threshold
- Block size tuning critical (100-500 documents per block)
- Memory-mapped arrays for very large matrices

### Integration Considerations
- Input: ProcessingResult with tfidf_matrix from Story 4.1
- Must preserve all input data while adding similarity fields
- Side effects: Cached similarity matrices
- Dependencies: scikit-learn, scipy, numpy

## Dev Agent Record

### Debug Log
*To be updated during implementation*

### Completion Notes
*To be updated after implementation*

### Context Reference
- docs/stories/4-2-document-and-chunk-similarity-analysis.context.xml (this file)

## File List
*To be updated with created/modified files*

## Change Log
- 2025-11-20: Story created for similarity analysis implementation

## Status
ready-for-dev