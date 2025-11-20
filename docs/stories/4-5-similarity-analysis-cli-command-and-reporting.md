# Story: 4-5 Similarity Analysis CLI Command and Reporting

## Story
**ID:** 4-5-similarity-analysis-cli-command-and-reporting
**Epic:** 4 - Knowledge Curation via Classical NLP
**Title:** Implement CLI Integration and Reporting for Semantic Analysis
**Priority:** P1
**Estimate:** 8 hours

As a data engineer using the extraction tool, I want to execute semantic analysis operations via CLI commands and generate comprehensive reports, so that I can integrate knowledge curation into my data pipelines and share insights with stakeholders through actionable reports.

## Acceptance Criteria

- [ ] **AC-4.5-1:** Add `data-extract semantic analyze` command accepting input path, output path, and configuration options
- [ ] **AC-4.5-2:** Implement `data-extract semantic deduplicate` command with threshold parameter and savings report
- [ ] **AC-4.5-3:** Add `data-extract semantic cluster` command with configurable K and output format options
- [ ] **AC-4.5-4:** Create `data-extract cache` subcommands for status, clear, warm operations
- [ ] **AC-4.5-5:** Generate HTML/JSON reports with similarity matrices, cluster visualizations, quality distributions
- [ ] **AC-4.5-6:** Progress indicators show real-time status for long-running operations (>1000 documents)
- [ ] **AC-4.5-7:** Configuration via CLI flags or .data-extract.yaml for all semantic parameters
- [ ] **AC-4.5-8:** Export results in multiple formats (JSON, CSV, HTML report, similarity graph)
- [ ] **AC-4.5-9:** Validate all inputs and provide helpful error messages for invalid configurations
- [ ] **AC-4.5-10:** All code passes mypy with zero errors and black/ruff with zero violations

## Tasks/Subtasks

### CLI Command Structure
- [ ] Design semantic command group structure in Click
- [ ] Add analyze subcommand with full pipeline execution
- [ ] Implement deduplicate subcommand for duplicate removal
- [ ] Create cluster subcommand for document grouping
- [ ] Add topics subcommand for LSA topic extraction

### Configuration Management
- [ ] Parse semantic section from .data-extract.yaml
- [ ] Add CLI flags for all configurable parameters
- [ ] Implement flag precedence (CLI > config file > defaults)
- [ ] Validate parameter ranges and combinations
- [ ] Create configuration export command

### Report Generation
- [ ] Design HTML report template with CSS styling
- [ ] Create similarity matrix heatmap visualizer
- [ ] Implement cluster membership tables
- [ ] Add quality score distribution charts
- [ ] Generate duplicate savings summary

### Progress and Feedback
- [ ] Implement progress bars with tqdm or rich
- [ ] Add verbose logging with structlog
- [ ] Create summary statistics output
- [ ] Show memory usage and performance metrics
- [ ] Add dry-run mode for configuration validation

### Cache Management
- [ ] Implement cache status command showing size/hits/misses
- [ ] Add cache clear with pattern matching
- [ ] Create cache warm command for precomputation
- [ ] Show cache effectiveness metrics
- [ ] Add cache export/import functionality

### Integration and Testing
- [ ] Wire all semantic stages into CLI pipeline
- [ ] Create end-to-end integration tests
- [ ] Add CLI command unit tests
- [ ] Test report generation with various inputs
- [ ] Validate configuration parsing

### Review Follow-ups (AI)
*To be added after code review*

## Dev Notes

### CLI Design Principles
- Commands should be intuitive and discoverable
- Provide sensible defaults for all parameters
- Show helpful examples in --help text
- Validate early and fail with clear messages
- Support both interactive and batch modes

### Report Structure
```
Semantic Analysis Report
========================
1. Summary Statistics
   - Documents processed: X
   - Duplicates found: Y (Z% reduction)
   - Clusters identified: N
   - Average quality score: Q

2. Duplicate Analysis
   - Near-duplicates table with similarity scores
   - Potential savings calculation
   - Recommended actions

3. Cluster Analysis
   - Cluster sizes and representatives
   - Topic keywords per cluster
   - Silhouette scores

4. Quality Distribution
   - Histogram of quality scores
   - Low-quality chunks flagged
   - Improvement recommendations
```

### Configuration Schema
```yaml
semantic:
  tfidf:
    max_features: 5000
    ngram_range: [1, 2]
  similarity:
    duplicate_threshold: 0.95
    related_threshold: 0.7
  lsa:
    n_components: 100
    n_clusters: auto
  quality:
    min_score: 0.3
  cache:
    enabled: true
    max_size_mb: 500
```

### Performance Considerations
- Stream processing for large corpora
- Batch operations to reduce overhead
- Memory monitoring to prevent OOM
- Cache warming for repeated analyses

## Dev Agent Record

### Debug Log
*To be updated during implementation*

### Completion Notes
*To be updated after implementation*

### Context Reference
- docs/stories/4-5-similarity-analysis-cli-command-and-reporting.context.xml (this file)

## File List
*To be updated with created/modified files*

## Change Log
- 2025-11-20: Story created for CLI integration and reporting

## Status
ready-for-dev