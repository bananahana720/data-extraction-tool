# Data Extraction Tool - Master Documentation Index

**Generated**: 2025-11-13
**Project**: Data Extraction Tool v0.1.0
**Type**: Monolith CLI Tool (Python 3.12+)
**Architecture**: 5-Stage Pipeline with Dual Codebase

---

## 🚀 Quick Start

**New to this project?** Start here:
1. [README.md](../README.md) - Project overview
2. [QUICKSTART.md](./QUICKSTART.md) - 5-minute quick start
3. [CLAUDE.md](../CLAUDE.md) - Development with Claude Code
4. [Development & Operations Guide](./development-operations-guide-2025-11-13.md) - Complete setup guide

---

## 📊 Project Overview

- **Type**: Monolith CLI Tool
- **Language**: Python 3.12-3.13
- **Architecture**: 5-stage modular pipeline (Extract → Normalize → Chunk → Semantic → Output)
- **Status**: Epic 2.5 complete, Epic 3 in progress
- **Codebase**: Dual structure (greenfield modernization + brownfield compatibility)
- **Total Documentation**: 93 files | 70,000+ lines

---

## 📂 Documentation Categories

### 🏗️ Architecture & Design

- [Architecture Overview](./architecture.md) - Complete technical architecture (4,847 lines)
- [Source Tree Analysis](./reviews/source-tree-analysis-annotated-2025-11-13.md) - Annotated directory structure with 50+ modules *(NEW)*
- [Brownfield Assessment](./brownfield-assessment.md) - Legacy codebase analysis and consolidation plan
- **Architecture Reference** (deep dives):
  - [Foundation](./architecture/FOUNDATION.md) - Core abstractions and interfaces
  - [Getting Started](./architecture/GETTING_STARTED.md) - Quick reference guide
  - [Quick Reference](./architecture/QUICK_REFERENCE.md) - Architecture cheat sheet
  - [Infrastructure Needs](./architecture/INFRASTRUCTURE_NEEDS.md) - Tooling and dependencies
  - [Testing Infrastructure](./architecture/TESTING_INFRASTRUCTURE.md) - Test architecture patterns

### 🔧 Development Guides

- [Development & Operations Guide](./development-operations-guide-2025-11-13.md) - Complete dev/ops reference with setup, testing, quality gates *(NEW)*
- [Configuration Management](./config-management-analysis.md) - Configuration cascade (4-tier), parser architecture, patterns *(NEW)*
- [Test Infrastructure](./test-infrastructure-analysis.md) - Organization, markers, fixtures, patterns, coverage *(NEW)*
- [CLI Entry Points](./cli-entry-points-analysis.md) - CLI commands, entry points, scripts *(NEW)*
- [Shared Utilities](./reviews/shared-utilities-analysis.md) - Core abstractions, helpers, validators *(NEW)*
- [CI/CD Infrastructure](./ci-cd-infrastructure-analysis.md) - Pipeline architecture, quality gates, workflows *(NEW)*
- [Configuration Guide](./CONFIG_GUIDE.md) - Configuration reference and examples
- [Logging Guide](./LOGGING_GUIDE.md) - Structured logging setup and patterns
- [Error Handling Guide](./ERROR_HANDLING_GUIDE.md) - Exception handling and recovery patterns
- [spaCy Troubleshooting](./troubleshooting-spacy.md) - spaCy model setup and common issues

### 📋 Planning & Requirements

- [Product Requirements Document (PRD)](./PRD.md) - Vision, requirements, and acceptance criteria (3,147 lines)
- [Epic Breakdown](./epics.md) - Story decomposition and roadmap (2,645 lines)
- **Technical Specifications**:
  - [Epic 1: Foundation](./tech-spec-epic-1.md) - Infrastructure and core patterns
  - [Epic 2: Extract & Normalize](./tech-spec-epic-2.md) - Extraction and normalization stages
  - [Epic 2.5: Refinement](./tech-spec-epic-2.5.md) - Quality and performance enhancements
- **Traceability & Mapping**:
  - [Epic 1 Traceability](./traceability-epic-1-foundation.md) - Requirements to stories
  - [Epic 2 Traceability](./traceability-epic-2-extract-normalize.md) - Extract/normalize mapping
  - [Epic 2.5 Traceability](./traceability-epic-2.5-refinement-quality.md) - Refinement mapping
  - [Master Traceability](./traceability-master-epic-1-2-consolidated.md) - Consolidated mapping (Epics 1-2)

### 📝 Story Documentation

**Epic 1: Foundation** (4 stories):
- [Story 1.1: Project Infrastructure](./stories/1-1-project-infrastructure-initialization.md) - Setup and tooling
- [Story 1.2: Brownfield Assessment](./stories/1-2-brownfield-codebase-assessment.md) - Legacy code analysis
- [Story 1.3: Testing Framework](./stories/1-3-testing-framework-and-ci-pipeline.md) - Test infrastructure
- [Story 1.4: Core Pipeline](./stories/1-4-core-pipeline-architecture-pattern.md) - Pipeline interfaces

**Epic 2: Extract & Normalize** (6 stories):
- [Story 2.1: Text Cleaning](./stories/2-1-text-cleaning-and-artifact-removal.md) - OCR and formatting cleanup
- [Story 2.2: Entity Normalization](./stories/2-2-entity-normalization-for-audit-domain.md) - Domain entity standardization
- [Story 2.3: Schema Standardization](./stories/2-3-schema-standardization-across-document-types.md) - Format harmonization
- [Story 2.4: OCR Validation](./stories/2-4-ocr-confidence-scoring-and-validation.md) - Confidence scoring
- [Story 2.5: Completeness Validation](./stories/2-5-completeness-validation-and-gap-detection.md) - Quality checks
- [Story 2.6: Metadata Enrichment](./stories/2-6-metadata-enrichment-framework.md) - Metadata extraction

**Epic 2.5: Refinement & Quality** (8 stories):
- [Story 2.5.1: Performance](./stories/2.5-1-large-document-validation-and-performance.md) - Throughput and memory
- [Story 2.5.1.1: Extractor Migration](./stories/2.5-1.1-greenfield-extractor-migration.md) - Greenfield extraction
- [Story 2.5.2: spaCy Integration](./stories/2.5-2-spacy-integration-and-end-to-end-testing.md) - Sentence boundary detection
- [Story 2.5.2.1: Pipeline Optimization](./stories/2.5-2.1-pipeline-throughput-optimization.md) - Optimization techniques
- [Story 2.5.3: Quality Automation](./stories/2.5-3-quality-gate-automation-and-documentation.md) - CI/CD gates
- [Story 2.5.3.1: UAT Framework](./stories/2.5-3.1-uat-workflow-framework.md) - UAT workflow implementation
- [Story 2.5.3.1: Completion Summary](./stories/2.5-3.1-completion-summary.md) - Story completion details
- [Story 2.5.4: CI/CD Enhancement](./stories/2.5-4-ci-cd-enhancement-for-epic-3-readiness.md) - Pipeline improvements

### 🧪 Testing & Validation

- [Test Infrastructure Analysis](./test-infrastructure-analysis.md) - Test organization and patterns *(NEW)*
- [Testing README](./TESTING-README.md) - Testing overview and command reference
- **Test Plans** (story-specific):
  - [PPTX Test Plan](./test-plans/PPTX_TEST_PLAN.md) - PowerPoint extraction testing
  - [Excel Extractor Test Plan](./test-plans/EXCEL_EXTRACTOR_TEST_PLAN.md) - XLSX testing
  - [TDD CLI Test Plan](./test-plans/TDD_TEST_PLAN_CLI.md) - CLI testing approach
  - [TDD Integration Test Plan](./test-plans/TDD_TEST_PLAN_INTEGRATION.md) - Integration testing
  - [TDD DOCX Coverage](./test-plans/TDD_TEST_PLAN_DOCX_COVERAGE.md) - DOCX coverage expansion
  - [Test Skip Policy](./test-plans/TEST_SKIP_POLICY.md) - Guidelines for skipping tests
  - [Skip Cleanup Reference](./test-plans/SKIP_CLEANUP_QUICK_REF.md) - Quick reference
- **UAT Framework** (user acceptance testing):
  - [Test Cases: Story 2.5.3.1](./uat/test-cases/2.5-3.1-test-cases.md) - Comprehensive test scenarios
  - [Test Results: Story 2.5.3.1](./uat/test-results/2.5-3.1-test-results.md) - Execution results
  - [UAT Review: Story 2.5.3.1](./uat/reviews/2.5-3.1-uat-review.md) - QA approval and findings
  - [tmux-cli Windows Setup](./uat/tmux-cli-windows-setup.md) - Windows CLI testing guidance
  - [tmux-cli Documentation](./uat/tmux-cli-documentation-updates-2025-11-13.md) - Complete tmux-cli reference

### 📈 Analysis & Reports

- [Technology Stack Analysis](./technology-stack-analysis.md) - Libraries, versions, and rationale
- [Housekeeping Findings](./reviews/housekeeping-findings-2025-11-13.md) - Documentation and code cleanup results
- [Implementation Readiness](./implementation-readiness-report-2025-11-10.md) - Epic 3 readiness assessment
- **Performance Analysis**:
  - [Performance Baselines](./performance-baselines-story-2.5.1.md) - NFR targets and measurements
  - [Performance Bottlenecks](./performance-bottlenecks-story-2.5.1.md) - Optimization opportunities
- **BMM Documentation** (BMAD Method):
  - [BMM Project Overview](./bmm-project-overview.md) - BMM methodology application
  - [BMM Pipeline Integration](./bmm-pipeline-integration-guide.md) - Integration patterns
  - [BMM Processor Chain Analysis](./bmm-processor-chain-analysis.md) - Processor architecture
  - [BMM Source Tree Analysis](./bmm-source-tree-analysis.md) - BMM-specific structure
  - [BMM Index](./bmm-index.md) - BMM documentation index
- **Brainstorming & Research**:
  - [Brainstorming Results](./brainstorming-session-results-2025-11-07.md) - Initial ideation
  - [Technical Research](./reviews/research-technical-2025-11-08.md) - Deep technical analysis

### 🔄 Retrospectives & Reviews

- [Epic 1 Retrospective](./retrospectives/epic-1-retro-20251110.md) - Foundation lessons learned
- [Epic 2 Retrospective](./retrospectives/epic-2-retro-20250111.md) - Extract/Normalize retrospective
- [Epic 2.5 Retrospective](./epic-2.5-retro-2025-11-13.md) - Refinement retrospective
- [Story 2.2 Code Review](./reviews/2-2-entity-normalization-review.md) - Detailed code review

### 🚀 CI/CD & Infrastructure

- [CI/CD Pipeline Documentation](./ci-cd-pipeline.md) - Full pipeline reference (4,000+ lines)
- [CI/CD Infrastructure Analysis](./ci-cd-infrastructure-analysis.md) - Architecture and quality gates *(NEW)*
- [Infrastructure Integration Guide](./INFRASTRUCTURE_INTEGRATION_GUIDE.md) - Integration patterns
- **GitHub Actions**:
  - test.yml - Unit and integration tests
  - performance.yml - Performance benchmarking
  - performance-regression.yml - Regression detection
  - (See .github/workflows/ directory for workflow files)

### 📊 Status & Tracking

- [Sprint Status](./sprint-status.yaml) - Real-time implementation tracking
- [BMM Workflow Status](./bmm-workflow-status.yaml) - BMM methodology tracking
- **Audit Reports** (from UAT workflows):
  - [Create Test Cases Audit](./reviews/audit-report-create-test-cases-2025-11-13.md) - Test case generation audit
  - [Build Test Context Audit](./reviews/audit-report-build-test-context-2025-11-13.md) - Context assembly audit
  - [Execute Tests Audit](./reviews/audit-report-execute-tests-2025-11-13.md) - Execution audit
  - [Review UAT Results Audit](./reviews/audit-report-review-uat-results-2025-11-13.md) - Results review audit

### 👥 User Documentation

- [User Guide](./USER_GUIDE.md) - Non-technical user guide (1,039 lines)
- [Quick Start](./QUICKSTART.md) - 5-minute extraction guide
- [Pilot Distribution README](./PILOT_DISTRIBUTION_README.md) - Distribution instructions
- [Complete Parameter Reference](./COMPLETE_PARAMETER_REFERENCE.md) - All CLI parameters documented

---

## 🎯 Finding What You Need

### By Task

**I want to...**

| Task | Start Here |
|------|-----------|
| **Understand the project** | [README.md](../README.md) → [architecture.md](./architecture.md) → [PRD.md](./PRD.md) |
| **Set up development** | [development-operations-guide-2025-11-13.md](./development-operations-guide-2025-11-13.md) |
| **Navigate the codebase** | [source-tree-analysis-annotated-2025-11-13.md](./reviews/source-tree-analysis-annotated-2025-11-13.md) |
| **Understand testing** | [test-infrastructure-analysis.md](./test-infrastructure-analysis.md) → [TESTING-README.md](./TESTING-README.md) |
| **Learn about configuration** | [config-management-analysis.md](./config-management-analysis.md) → [CONFIG_GUIDE.md](./CONFIG_GUIDE.md) |
| **Troubleshoot issues** | [troubleshooting-spacy.md](./troubleshooting-spacy.md) → [ERROR_HANDLING_GUIDE.md](./ERROR_HANDLING_GUIDE.md) |
| **Review epic progress** | [sprint-status.yaml](./sprint-status.yaml) → retrospectives/ folder |
| **Find CLI commands** | [cli-entry-points-analysis.md](./cli-entry-points-analysis.md) → [CLAUDE.md](../CLAUDE.md) |
| **Understand CI/CD** | [ci-cd-infrastructure-analysis.md](./ci-cd-infrastructure-analysis.md) → [ci-cd-pipeline.md](./ci-cd-pipeline.md) |
| **Run tests locally** | [TESTING-README.md](./TESTING-README.md) → [test-infrastructure-analysis.md](./test-infrastructure-analysis.md) |
| **Execute UAT workflows** | [stories/2.5-3.1-uat-workflow-framework.md](./stories/2.5-3.1-uat-workflow-framework.md) |
| **Set up spaCy** | [troubleshooting-spacy.md](./troubleshooting-spacy.md) (in CLAUDE.md) |
| **Optimize performance** | [performance-baselines-story-2.5.1.md](./performance-baselines-story-2.5.1.md) → [performance-bottlenecks-story-2.5.1.md](./performance-bottlenecks-story-2.5.1.md) |

### By Role

**Developer**
1. [development-operations-guide-2025-11-13.md](./development-operations-guide-2025-11-13.md) - Setup
2. [source-tree-analysis-annotated-2025-11-13.md](./reviews/source-tree-analysis-annotated-2025-11-13.md) - Navigation
3. [test-infrastructure-analysis.md](./test-infrastructure-analysis.md) - Testing patterns
4. [CLAUDE.md](../CLAUDE.md) - Development workflow

**QA/Tester**
1. [test-infrastructure-analysis.md](./test-infrastructure-analysis.md)
2. [TESTING-README.md](./TESTING-README.md)
3. [uat/](./uat/) - UAT framework
4. [test-plans/](./test-plans/) - Test scenarios

**Product Manager**
1. [PRD.md](./PRD.md) - Requirements
2. [epics.md](./epics.md) - Epic breakdown
3. [sprint-status.yaml](./sprint-status.yaml) - Progress tracking
4. retrospectives/ - Lessons learned

**DevOps/Architect**
1. [architecture.md](./architecture.md)
2. [ci-cd-infrastructure-analysis.md](./ci-cd-infrastructure-analysis.md)
3. [ci-cd-pipeline.md](./ci-cd-pipeline.md)
4. [INFRASTRUCTURE_INTEGRATION_GUIDE.md](./INFRASTRUCTURE_INTEGRATION_GUIDE.md)

**End User**
1. [QUICKSTART.md](./QUICKSTART.md)
2. [USER_GUIDE.md](./USER_GUIDE.md)
3. [COMPLETE_PARAMETER_REFERENCE.md](./COMPLETE_PARAMETER_REFERENCE.md)

---

## 📚 Documentation Organization

### File Structure

```
docs/
├── index.md                              # THIS FILE - Master index
├── architecture/                         # Deep architecture dives
│   ├── FOUNDATION.md
│   ├── GETTING_STARTED.md
│   ├── QUICK_REFERENCE.md
│   ├── INFRASTRUCTURE_NEEDS.md
│   └── TESTING_INFRASTRUCTURE.md
├── stories/                              # Epic story specifications
│   ├── 1-1-*.md
│   ├── 1-2-*.md
│   ├── 1-3-*.md
│   ├── 1-4-*.md
│   ├── 2-1-*.md to 2-6-*.md
│   └── 2.5-*.md (8 stories)
├── test-plans/                           # Test specifications
│   ├── PPTX_TEST_PLAN.md
│   ├── EXCEL_EXTRACTOR_TEST_PLAN.md
│   ├── TDD_TEST_PLAN_*.md (3 files)
│   ├── TEST_SKIP_POLICY.md
│   └── SKIP_CLEANUP_QUICK_REF.md
├── uat/                                  # User acceptance testing
│   ├── test-cases/
│   ├── test-results/
│   ├── reviews/
│   └── tmux-cli-*.md
├── retrospectives/                       # Epic/milestone retrospectives
│   ├── epic-1-retro-*.md
│   ├── epic-2-retro-*.md
│   └── epic-2.5-retro-*.md
├── reviews/                              # Code reviews and analysis reports
│   ├── 2-2-entity-normalization-review.md
│   ├── audit-report-create-test-cases-2025-11-13.md
│   ├── audit-report-build-test-context-2025-11-13.md
│   ├── audit-report-execute-tests-2025-11-13.md
│   ├── audit-report-review-uat-results-2025-11-13.md
│   ├── housekeeping-findings-2025-11-13.md
│   ├── research-technical-2025-11-08.md
│   ├── shared-utilities-analysis.md
│   └── source-tree-analysis-annotated-2025-11-13.md
├── architecture.md                       # Main architecture document
├── PRD.md                                # Product requirements (3,147 lines)
├── epics.md                              # Epic breakdown (2,645 lines)
├── tech-spec-epic-*.md (3 files)        # Technical specifications
├── traceability-*.md (4 files)          # Requirements traceability
├── brownfield-assessment.md              # Legacy code analysis
├── CONFIG_GUIDE.md                       # Configuration reference
├── LOGGING_GUIDE.md                      # Logging setup
├── ERROR_HANDLING_GUIDE.md               # Error handling patterns
├── TESTING-README.md                     # Testing overview
├── QUICKSTART.md                         # 5-minute quick start
├── USER_GUIDE.md                         # End user guide
├── PILOT_DISTRIBUTION_README.md          # Distribution instructions
├── COMPLETE_PARAMETER_REFERENCE.md       # CLI parameters
├── INFRASTRUCTURE_INTEGRATION_GUIDE.md   # Integration patterns
├── ci-cd-pipeline.md                     # CI/CD documentation
├── troubleshooting-spacy.md              # spaCy troubleshooting
├── tmux-cli-instructions.md              # tmux-cli reference
├── technology-stack-analysis.md          # Stack breakdown
├── implementation-readiness-report-2025-11-10.md
├── performance-baselines-story-2.5.1.md  # Performance targets
├── performance-bottlenecks-story-2.5.1.md
├── brainstorming-session-results-2025-11-07.md
├── NEW ANALYSIS DOCUMENTS (2025-11-13):
│   ├── config-management-analysis.md
│   ├── test-infrastructure-analysis.md
│   ├── cli-entry-points-analysis.md
│   ├── ci-cd-infrastructure-analysis.md
│   └── development-operations-guide-2025-11-13.md
├── BMM DOCUMENTATION:
│   ├── bmm-project-overview.md
│   ├── bmm-pipeline-integration-guide.md
│   ├── bmm-processor-chain-analysis.md
│   ├── bmm-source-tree-analysis.md
│   └── bmm-index.md
├── sprint-status.yaml                    # Implementation tracking
├── bmm-workflow-status.yaml              # BMM tracking
└── .archive/                             # Historical documentation (165+ files)
    └── pre-bmad/
        ├── assessment/
        ├── backlog.md
        ├── deployment/
        ├── planning/
        ├── reports/
        └── (165+ historical files)
```

### Documentation Categories by Line Count

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| Architecture | 6 | 8,000+ | Technical design and patterns |
| Planning | 10 | 12,000+ | Requirements and specifications |
| Stories | 18 | 25,000+ | Epic implementation details |
| Testing | 15 | 8,000+ | Test specs and UAT framework |
| Guides | 8 | 6,000+ | Setup, configuration, troubleshooting |
| Analysis | 11 | 7,000+ | Deep system analysis (NEW 2025-11-13) |
| Status | 4 | 2,000+ | Progress tracking and reporting |
| User Docs | 4 | 3,000+ | End-user guides |
| **TOTAL** | **93** | **70,000+** | Complete documentation suite |

---

## 🔗 Key References

### Standards & Conventions
- See [CLAUDE.md](../CLAUDE.md) for:
  - Code quality gates and pre-commit hooks
  - Testing strategy and markers
  - Epic-based development workflow
  - Development commands and CI/CD overview

### Architecture Decisions
- [architecture.md](./architecture.md) - Complete ADRs (Architecture Decision Records)
- Key decisions: ADR-001 through ADR-005 documented

### External Resources
- GitHub: [yourusername/ai-data-extractor](https://github.com/yourusername/ai-data-extractor)
- Issues: [GitHub Issues](https://github.com/yourusername/ai-data-extractor/issues)

---

## 📅 Documentation Timeline

| Date | Event | Output |
|------|-------|--------|
| 2025-11-07 | Initial documentation generation | document-project workflow results |
| 2025-11-08 | Product research and technical analysis | PRD + research documents |
| 2025-11-10 | Architecture and solutioning gate | architecture.md + tech specs |
| 2025-11-13 | Exhaustive rescan with analysis | 7 NEW analysis documents |

### Latest Updates (2025-11-13)

Seven comprehensive new analysis documents generated:
1. **config-management-analysis.md** - Configuration cascade, parsers, patterns
2. **test-infrastructure-analysis.md** - Test organization, fixtures, CI integration
3. **cli-entry-points-analysis.md** - CLI commands, entry points, scripts
4. **reviews/shared-utilities-analysis.md** - Core abstractions and helpers
5. **ci-cd-infrastructure-analysis.md** - Pipeline architecture and gates
6. **reviews/source-tree-analysis-annotated-2025-11-13.md** - Complete annotated source tree
7. **development-operations-guide-2025-11-13.md** - Comprehensive dev/ops manual

Plus 4 UAT audit reports documenting test generation workflows (in reviews/).

---

## ✨ Documentation Highlights

### Comprehensive Coverage
- **Architecture**: 8,000+ lines covering all stages of the pipeline
- **Testing**: Complete infrastructure with 18 story specs and UAT framework
- **User Guides**: From 5-minute quick start to comprehensive parameter reference
- **Analysis**: 7 new deep-dive analyses of key systems (2025-11-13)

### AI-Optimized Structure
- All documents designed for Claude Code AI retrieval
- Cross-referenced with relative paths (./file.md format)
- Markdown formatting with consistent heading hierarchy
- Source tree maps with annotations for code navigation

### Developer-Friendly
- Quick navigation by role and task
- Troubleshooting guides for common issues
- Performance baselines and optimization guides
- Clear separation of greenfield vs. brownfield code

---

## 🎯 Next Steps

**For New Developers**:
1. Start with [QUICKSTART.md](./QUICKSTART.md)
2. Clone repository
3. Run [development-operations-guide-2025-11-13.md](./development-operations-guide-2025-11-13.md) setup steps
4. Review [source-tree-analysis-annotated-2025-11-13.md](./reviews/source-tree-analysis-annotated-2025-11-13.md)
5. Pick a story from [sprint-status.yaml](./sprint-status.yaml)

**For Continuing Development**:
1. Check [sprint-status.yaml](./sprint-status.yaml) for current story
2. Review relevant story spec in [stories/](./stories/)
3. Consult [test-infrastructure-analysis.md](./test-infrastructure-analysis.md) for test patterns
4. Run quality gates: `pre-commit run --all-files`

**For Integration/Deployment**:
1. Review [ci-cd-infrastructure-analysis.md](./ci-cd-infrastructure-analysis.md)
2. Check [ci-cd-pipeline.md](./ci-cd-pipeline.md) for workflow details
3. Verify performance against [performance-baselines-story-2.5.1.md](./performance-baselines-story-2.5.1.md)

---

**Master Documentation Index**
Generated: 2025-11-13 | Updated: 2025-11-13
93 total files | 70,000+ lines | Complete coverage
