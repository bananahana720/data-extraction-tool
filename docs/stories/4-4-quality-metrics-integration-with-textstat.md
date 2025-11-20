# Story: 4-4 Quality Metrics Integration with Textstat

## Story
**ID:** 4-4-quality-metrics-integration-with-textstat
**Epic:** 4 - Knowledge Curation via Classical NLP
**Title:** Integrate Quality Metrics using Textstat for Content Assessment
**Priority:** P1
**Estimate:** 8 hours

As a content quality analyst, I want to assess the readability and quality of document chunks using comprehensive metrics from textstat, so that I can filter out low-quality content (OCR gibberish, malformed text) and reduce LLM hallucinations by 20% while prioritizing high-quality chunks for processing.

## Acceptance Criteria

- [ ] **AC-4.4-1:** QualityMetricsStage implements PipelineStage protocol accepting List[Chunk] and returning enriched List[Chunk]
- [ ] **AC-4.4-2:** Compute Flesch-Kincaid Grade Level, Gunning Fog, SMOG Index, and Coleman-Liau Index for each chunk
- [ ] **AC-4.4-3:** Calculate lexical diversity (unique words/total words) and syllable complexity metrics
- [ ] **AC-4.4-4:** Generate composite quality score (0.0-1.0 scale) combining readability and diversity metrics
- [ ] **AC-4.4-5:** Flag low-quality chunks (score < 0.3) for review or exclusion from semantic processing
- [ ] **AC-4.4-6:** Performance meets NFR: <10ms per chunk, <10s for 1000 chunks, minimal memory overhead
- [ ] **AC-4.4-7:** Enrich chunk.quality_score field and add readability_scores dictionary to metadata
- [ ] **AC-4.4-8:** Support configurable metric weights for domain-specific quality assessment
- [ ] **AC-4.4-9:** Generate quality distribution report showing score histogram and flagged chunks
- [ ] **AC-4.4-10:** All code passes mypy with zero errors and black/ruff with zero violations

## Tasks/Subtasks

### Core Implementation
- [ ] Create src/data_extract/semantic/quality.py module
- [ ] Implement QualityMetricsStage class with PipelineStage protocol
- [ ] Integrate textstat library for readability calculations
- [ ] Add comprehensive metric computation methods
- [ ] Create composite scoring algorithm

### Readability Metrics
- [ ] Implement Flesch Reading Ease calculator
- [ ] Add Flesch-Kincaid Grade Level metric
- [ ] Implement Gunning Fog Index
- [ ] Add SMOG (Simple Measure of Gobbledygook) Index
- [ ] Implement Coleman-Liau and Dale-Chall readability scores

### Quality Assessment
- [ ] Calculate lexical diversity (type-token ratio)
- [ ] Add syllable count and complexity metrics
- [ ] Implement sentence length and structure analysis
- [ ] Create OCR gibberish detection heuristics
- [ ] Add special character and formatting anomaly detection

### Scoring and Flagging
- [ ] Design weighted composite scoring formula
- [ ] Implement quality threshold configuration
- [ ] Create quality flag enum (HIGH, MEDIUM, LOW, REVIEW)
- [ ] Add filtering logic for quality-based selection
- [ ] Generate quality improvement suggestions

### Integration and Reporting
- [ ] Chain with existing chunk processing pipeline
- [ ] Update chunk.quality_score with computed value
- [ ] Add readability_scores to chunk metadata
- [ ] Create quality distribution visualizer
- [ ] Generate quality audit report

### Testing and Validation
- [ ] Create unit tests for QualityMetricsStage (95% coverage)
- [ ] Test edge cases (empty text, single words, special chars)
- [ ] Validate scoring consistency across document types
- [ ] Benchmark performance with various chunk sizes
- [ ] Test quality filtering effectiveness

### Review Follow-ups (AI)
*To be added after code review*

## Dev Notes

### Metric Selection
- Flesch-Kincaid: Standard for government documents
- Gunning Fog: Good for business/technical content
- SMOG: Better for health/medical documents
- Coleman-Liau: Character-based, handles OCR errors better
- Combine multiple metrics for robustness

### Quality Scoring Formula
```python
composite_score = (
    flesch_ease * 0.3 +      # Readability (normalized)
    (12 - grade_level)/12 * 0.3 +  # Grade level (inverted)
    lexical_diversity * 0.2 +  # Vocabulary richness
    1 - anomaly_score * 0.2    # Absence of gibberish
)
```

### OCR Gibberish Detection
- High ratio of special characters
- Very low lexical diversity (<0.1)
- Extremely high/low syllable counts
- No sentence structure detected
- Grade level > 20 or < 0

### Performance Optimization
- Cache syllable counts for repeated words
- Batch process chunks for efficiency
- Use numpy for statistical calculations
- Minimal regex for better performance

## Dev Agent Record

### Debug Log
*To be updated during implementation*

### Completion Notes
*To be updated after implementation*

### Context Reference
- docs/stories/4-4-quality-metrics-integration-with-textstat.context.xml (this file)

## File List
*To be updated with created/modified files*

## Change Log
- 2025-11-20: Story created for quality metrics integration

## Status
ready-for-dev