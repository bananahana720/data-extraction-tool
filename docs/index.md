# Data Extraction Tool - Documentation Index

**Updated**: 2025-11-15
**Status**: Epic 3 in progress (Stories 3.1-3.5 complete, 3.6 in review)
**Architecture**: 5-Stage Pipeline (Extract → Normalize → Chunk → Semantic → Output)

---

## 🚀 Quick Start

**New to this project?** Start here:
1. [QUICKSTART.md](./QUICKSTART.md) - Five-minute setup guide for first document extraction
2. [USER_GUIDE.md](./USER_GUIDE.md) - Non-technical user guide for document extraction usage
3. [PILOT_DISTRIBUTION_README.md](./PILOT_DISTRIBUTION_README.md) - Installation and quickstart for pilot distribution

---

## 📋 Configuration & Operations

- **[CONFIG_GUIDE.md](./CONFIG_GUIDE.md)** - Configuration management guide with cascade precedence and API reference
- **[LOGGING_GUIDE.md](./LOGGING_GUIDE.md)** - Structured JSON logging with performance timing and correlation tracking
- **[ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md)** - Error handling infrastructure with error codes and recovery patterns
- **[INFRASTRUCTURE_INTEGRATION_GUIDE.md](./INFRASTRUCTURE_INTEGRATION_GUIDE.md)** - Integration patterns for ConfigManager and LoggingFramework

---

## 🧪 Testing & Development

- **[TESTING-README.md](./TESTING-README.md)** - Comprehensive test execution guide with markers and coverage commands
- **[development-operations-guide.md](./development-operations-guide.md)** - Developer and DevOps setup guide with prerequisites and workflow
- **[automation-summary.md](./automation-summary.md)** - Test automation expansion summary with 52 new greenfield CLI tests
- **[tmux-cli-instructions.md](./tmux-cli-instructions.md)** - Command-line tool documentation for tmux pane control and auto-detection

### ATDD Acceptance Criteria Checklists

- **[atdd-checklist-3.4.md](./atdd-checklist-3.4.md)** - JSON output format with complete metadata acceptance criteria tests
- **[atdd-checklist-3.5.md](./atdd-checklist-3.5.md)** - Plain text output format for LLM upload acceptance criteria checklist
- **[atdd-checklist-3.6.md](./atdd-checklist-3.6.md)** - CSV output format for analysis and tracking acceptance criteria validation

---

## 📐 Technical Specifications (Sharded)

Complete technical specifications now organized into navigable sections:

### Epic Specifications

- **[tech-spec-epic-1.md](./tech-spec-epic-1.md)** - Epic 1 technical specification establishing foundation and pipeline architecture
- **[tech-spec-epic-2/](./tech-spec-epic-2/)** - Epic 2 Extract & Normalize (10 sections + index.md)
- **[tech-spec-epic-2.5/](./tech-spec-epic-2.5/)** - Epic 2.5 Refinement (10 sections + index.md)
- **[tech-spec-epic-3/](./tech-spec-epic-3/)** - Epic 3 Chunk & Output (8 sections + index.md)

### Planning Documents

- **[PRD/](./PRD/)** - Product Requirements Document (11 sections + index.md)
- **[architecture/](./architecture/)** - Technical architecture and ADRs (14 sections + index.md)
- **[epics.md](./epics.md)** - Complete epic breakdown transforming brownfield to production-ready RAG pipeline

---

## 🔍 Analysis & Architecture (Sharded)

Deep-dive analyses organized into sections for easier navigation:

- **[brownfield-assessment/](./brownfield-assessment/)** - Legacy codebase analysis and consolidation plan (11 sections + index.md)
- **[bmm-pipeline-integration-guide/](./bmm-pipeline-integration-guide/)** - Pipeline integration patterns (13 sections + index.md)
- **[bmm-processor-chain-analysis/](./bmm-processor-chain-analysis/)** - Processor chain architecture (10 sections + index.md)
- **[implementation-readiness-report-2025-11-10/](./implementation-readiness-report-2025-11-10/)** - Epic 3 readiness assessment (12 sections + index.md)
- **[development-operations-guide-2025-11-13/](./development-operations-guide-2025-11-13/)** - Complete dev/ops reference (11 sections + index.md)

### Single-File Analysis Documents

- **[bmm-project-overview.md](./bmm-project-overview.md)** - Comprehensive project overview with strategic context and enhancement journeys
- **[bmm-source-tree-analysis.md](./bmm-source-tree-analysis.md)** - Source code organization reference with directory structure mapping
- **[ci-cd-infrastructure-analysis.md](./ci-cd-infrastructure-analysis.md)** - CI/CD infrastructure analysis with quality gate pipeline and caching
- **[cli-entry-points-analysis.md](./cli-entry-points-analysis.md)** - CLI entry points analysis showing placeholder and 15 utility scripts
- **[config-management-analysis.md](./config-management-analysis.md)** - Configuration architecture analysis with four-tier cascade and 285 settings
- **[technology-stack-analysis.md](./technology-stack-analysis.md)** - Technology stack analysis with runtime, libraries and Python 3.12 requirements
- **[test-infrastructure-analysis.md](./test-infrastructure-analysis.md)** - Test infrastructure analysis covering 83 test files and pytest markers

---

## 📈 Performance & Optimization

- **[performance-baselines-epic-3.md](./performance-baselines-epic-3.md)** - Epic 3 performance baselines with chunking and JSON formatting metrics
- **[performance-baselines-story-2.5.1.md](./performance-baselines-story-2.5.1.md)** - Greenfield architecture performance baselines from 100-file production run
- **[performance-bottlenecks-story-2.5.1.md](./performance-bottlenecks-story-2.5.1.md)** - cProfile analysis identifying I/O dominance and process pool overhead

---

## 🔄 CI/CD & Pipeline

- **[ci-cd-pipeline.md](./ci-cd-pipeline.md)** - GitHub Actions workflows documentation with test and performance regression
- **[test-design-epic-3.md](./test-design-epic-3.md)** - Test design document with risk assessment and 68.5-hour test effort estimates

---

## 📊 Traceability & Quality

Requirements-to-implementation traceability across all epics:

- **[traceability-epic-1-foundation.md](./traceability-epic-1-foundation.md)** - Requirements-to-tests traceability report for Epic 1 with coverage analysis
- **[traceability-epic-2-extract-normalize.md](./traceability-epic-2-extract-normalize.md)** - Epic 2 traceability report showing 100% test coverage across 6 stories
- **[traceability-epic-2.5-refinement-quality.md](./traceability-epic-2.5-refinement-quality.md)** - Epic 2.5 traceability report documenting NFR trade-off and production readiness
- **[traceability-master-epic-1-2-consolidated.md](./traceability-master-epic-1-2-consolidated.md)** - Master traceability report consolidating Epics 1, 2, and 2.5 quality metrics

---

## 📖 Reference Documentation

- **[json-schema-reference.md](./json-schema-reference.md)** - JSON schema reference documenting canonical chunk output structure
- **[txt-format-reference.md](./txt-format-reference.md)** - Plain text output format reference with structure and configuration options
- **[troubleshooting-spacy.md](./troubleshooting-spacy.md)** - spaCy 3.7.2+ troubleshooting guide with common errors and solutions

---

## 📅 Project Management

- **[sprint-status.yaml](./sprint-status.yaml)** - YAML file tracking development status across all epics and stories
- **[backlog.md](./backlog.md)** - Engineering backlog of non-urgent optimizations and cross-cutting improvements
- **[bmm-index.md](./bmm-index.md)** - BMad Method documentation index with navigation for brownfield enhancement

---

## 📝 Reports & Metadata

- **[project-maintenance-report-2025-11-14.md](./project-maintenance-report-2025-11-14.md)** - Comprehensive maintenance analysis of documentation and technical debt status
- **[brainstorming-session-results-2025-11-07.md](./brainstorming-session-results-2025-11-07.md)** - Brainstorming session exploring self-explanatory CLI design with layered communication
- **[guide-generation-summary-2025-11-13.json](./guide-generation-summary-2025-11-13.json)** - JSON summary of development and operations guide generation with sections
- **[project-scan-report.json](./project-scan-report.json)** - Project scan metadata with findings on docs, models, and CI/CD maturity

---

## 📁 Subdirectories

### Story Documentation
- **[stories/](./stories/)** - Individual story specifications and context files for all epics

### Test Plans & UAT
- **[test-plans/](./test-plans/)** - Test specifications for various formats and integration scenarios
- **[uat/](./uat/)** - User acceptance testing framework, test cases, results, and reviews

### Retrospectives & Reviews
- **[retrospectives/](./retrospectives/)** - Epic retrospectives capturing lessons learned
- **[reviews/](./reviews/)** - Code reviews, audit reports, and analysis findings

### Examples & Archive
- **[examples/](./examples/)** - Sample documents and usage examples
- **[archive/](./archive/)** - Archived original monolithic documents (10 files moved after sharding)

---

## 🎯 Quick Navigation by Task

| I want to... | Start here |
|--------------|------------|
| **Set up the project** | [QUICKSTART.md](./QUICKSTART.md) |
| **Understand the architecture** | [architecture/](./architecture/) → [architecture/index.md](./architecture/index.md) |
| **Run tests** | [TESTING-README.md](./TESTING-README.md) |
| **Configure the tool** | [CONFIG_GUIDE.md](./CONFIG_GUIDE.md) |
| **Troubleshoot issues** | [troubleshooting-spacy.md](./troubleshooting-spacy.md) → [ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md) |
| **Check project status** | [sprint-status.yaml](./sprint-status.yaml) |
| **Review performance** | [performance-baselines-epic-3.md](./performance-baselines-epic-3.md) |
| **Understand BMad Method** | [bmm-index.md](./bmm-index.md) → [bmm-project-overview.md](./bmm-project-overview.md) |
| **Find a specific epic spec** | [PRD/](./PRD/), [tech-spec-epic-2/](./tech-spec-epic-2/), [tech-spec-epic-2.5/](./tech-spec-epic-2.5/), [tech-spec-epic-3/](./tech-spec-epic-3/) |
| **Learn about CI/CD** | [ci-cd-pipeline.md](./ci-cd-pipeline.md) → [ci-cd-infrastructure-analysis.md](./ci-cd-infrastructure-analysis.md) |

---

## 📊 Documentation Statistics

- **Root-level files**: 44 markdown/YAML/JSON files
- **Sharded documentation**: 10 large documents split into 110+ section files
- **Subdirectories**: 18 (stories, test-plans, uat, retrospectives, reviews, examples, archive, + 10 sharded docs)
- **Total documentation**: 150+ files
- **Archive**: 10 original monolithic documents safely archived

---

**Last Updated**: 2025-11-15
**Major Changes**:
- Sharded 10 large documents (>1000 lines each) into organized section-based folders
- Added index.md navigation files to all sharded directories
- Archived original monolithic documents to docs/archive/
- Updated descriptions based on actual file content
