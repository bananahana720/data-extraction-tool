# TRASH Files Log

## Pre-BMAD Documentation Cleanup - 2025-11-13

**Reason**: Archiving verbose, low-quality Claude Code session reports generated before BMAD framework adoption (pre-Nov 7, 2025). These files create context bloat and are superseded by BMAD-generated documentation.

**Archive Location**: `docs/.archive/pre-bmad/` (backup copy preserved)

### Directories Moved to TRASH/pre-bmad-docs/

- `docs/reports/` - 105+ verbose Claude Code session reports and completion summaries
- `docs/wave-handoffs/` - Legacy wave handoff documents
- `docs/planning/` - Point-in-time planning documents
- `docs/deployment/` - Version-specific deployment documentation (v1.0.4)
- `docs/assessment/` - ADR assessment reports

### Root-Level Files Moved to TRASH/pre-bmad-docs/

- `DOCUMENTATION_INDEX.md` - Legacy documentation index (to be regenerated with BMAD framework)
- `INSTALL.md` - Installation guide (to be regenerated)
- `PROJECT_STATE.md` - Project state tracking (to be regenerated)
- `docs/backlog.md` - Legacy backlog
- `docs/brownfield-test-failures-tracking.md` - Test failure tracking
- `docs/brownfield-test-triage.md` - Test triage report
- `docs/cli-test-triage-report.md` - CLI test triage
- `docs/p0-fix-results.md` - P0 fix results
- `docs/test-quick-wins.md` - Test quick wins
- `docs/test-triage-analysis.md` - Test triage analysis
- `docs/test-triage-executive-summary.md` - Test triage summary
- `docs/epic-2-transition-brief.md` - Epic 2 transition brief

### Files Kept (BMAD-Aligned)

**Architecture Documentation**:
- `docs/architecture/FOUNDATION.md` - Core architecture reference
- `docs/architecture/GETTING_STARTED.md` - Development getting started
- `docs/architecture/QUICK_REFERENCE.md` - API quick reference
- `docs/architecture/INFRASTRUCTURE_NEEDS.md` - Infrastructure requirements
- `docs/architecture/TESTING_INFRASTRUCTURE.md` - Testing infrastructure

**User & Technical Guides**:
- `docs/USER_GUIDE.md` - End-user documentation
- `docs/QUICKSTART.md` - Quick start guide
- `docs/CONFIG_GUIDE.md` - Configuration guide
- `docs/ERROR_HANDLING_GUIDE.md` - Error handling reference
- `docs/LOGGING_GUIDE.md` - Logging framework guide
- `docs/COMPLETE_PARAMETER_REFERENCE.md` - Complete parameter reference
- `docs/INFRASTRUCTURE_INTEGRATION_GUIDE.md` - Infrastructure integration
- `docs/TESTING-README.md` - Testing guide

**BMAD-Generated Documentation** (all files created Nov 7+):
- `docs/bmm-index.md` - BMAD master index
- `docs/bmm-project-overview.md` - Project overview
- `docs/bmm-pipeline-integration-guide.md` - Pipeline integration guide
- `docs/bmm-processor-chain-analysis.md` - Processor chain analysis
- `docs/bmm-source-tree-analysis.md` - Source tree analysis
- `docs/architecture.md` - Architecture document
- `docs/PRD.md` - Product requirements
- `docs/epics.md` - Epic breakdown
- `docs/tech-spec-epic-*.md` - Technical specifications
- `docs/stories/` - Story documentation
- `docs/retrospectives/` - Epic retrospectives
- `docs/reviews/` - Story reviews
- `docs/uat/` - UAT framework

### Impact

**Before Cleanup**: 230+ markdown files
**After Cleanup**: ~50-60 high-quality, BMAD-aligned documentation files
**Context Bloat Reduction**: ~170 files removed from active docs
**Archive Preservation**: All removed files backed up in `docs/.archive/pre-bmad/`
story-review-append.txt - moved to TRASH/ - temporary review content file
docs/uat/test-context/3-2-test-context.xml - moved to TRASH/ - template placeholder, regenerating with actual content
