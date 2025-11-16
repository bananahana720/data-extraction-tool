# Epic 3.5: Bridge Epic - Tooling & Semantic Prep

**Status:** TODO - Ready for implementation
**Epic Type:** Bridge Epic (Preparation for Epic 4)
**Duration Estimate:** 2.5 days (~20 hours)
**Sprint:** Pre-Epic 4 Preparation Sprint
**Team:** Charlie (Dev Lead), Elena (Dev), Dana (QA), Winston (Architect), Bob (SM)

---

## Epic Overview

Epic 3.5 is a **bridge epic** between Epic 3 (Chunk & Output) and Epic 4 (Foundational Semantic Analysis). It addresses action items and preparation tasks identified in the Epic 3 retrospective (2025-11-16), ensuring Epic 4 can start without blockers or mid-sprint delays.

**Epic Goal:** Prepare tooling, documentation, and infrastructure for Epic 4 semantic analysis implementation, addressing Epic 3 retrospective learnings and preventing repeating past mistakes.

**Epic Value:**
- Eliminates Epic 4 first-story blockers (dependencies installed, process documented)
- Prevents repeating Epic 3 mistakes (AC evidence backfilling, missing templates)
- Accelerates Epic 4 development (playbooks, fixtures, ADRs ready upfront)
- Creates institutional memory (lessons learned, gotchas, best practices)

---

## Epic 3 Retrospective Context

This bridge epic directly addresses findings from the **Epic 3 Retrospective (2025-11-16)**:

### Challenges Identified:
- "Story templates lacked reminders for provenance/logging/wiring"
- "AC evidence often backfilled post-review, causing rework"
- "Dependency audit process still undocumented"

### Key Insights:
- "Invest in scriptable scaffolding to embed development guidelines"
- "Enforce completion via tooling so humans focus on complex work"

### Action Items (Now Epic 3.5 Stories):
- Story/Review Template Generator (Elena + DevOps) → **Story 3.5.1**
- CLAUDE.md Lessons section (Bob) → **Story 3.5.2**
- Test-dependency audit doc (Winston) → **Story 3.5.3**

### Preparation Tasks (Now Epic 3.5 Stories):
- Add semantic dependencies + smoke test (Charlie, 4h) → **Story 3.5.4**
- Model/Cache ADR (Winston, 4h) → **Story 3.5.5**
- Semantic QA fixtures (Dana, 6h) → **Story 3.5.6**
- TF-IDF/LSA playbook (Charlie + Elena, 4h) → **Story 3.5.7**

---

## Epic 3.5 Stories

### Story 3.5.1: Story/Review Template Generator
**Owner:** Elena + DevOps | **Estimate:** 4h | **Priority:** P0

**Goal:** Create automated story and review templates that embed development guidelines (provenance tracking, structured logging, AC evidence collection) to prevent Epic 3 challenges from recurring.

**Deliverables:**
- `bmad/bmm/templates/story-template.md.j2` - Jinja2 story template
- `bmad/bmm/templates/review-template.md.j2` - Jinja2 review checklist template
- `bmad/bmm/tools/scaffold-story.py` - CLI scaffolding tool
- `bmad/bmm/templates/README.md` - Usage documentation

**Success Criteria:**
- Templates include inline reminders for provenance, logging, wiring, AC evidence
- CLI tool generates story/review files from YAML config
- Epic 4+ stories can use templates to avoid Epic 3 mistakes

---

### Story 3.5.2: CLAUDE.md Lessons Section
**Owner:** Bob (SM) | **Estimate:** 4h | **Priority:** P0

**Goal:** Add "Lessons Learned" section to CLAUDE.md documenting retrospective insights from Epics 1-3, creating institutional memory accessible to developers and Claude Code.

**Deliverables:**
- `.claude/CLAUDE.md` updated with "## Lessons Learned" section
- Epic 1, 2, 2.5, 3 lessons documented in Do/Avoid/Consider format
- Cross-references to stories, ADRs, retrospectives

**Success Criteria:**
- Epic 3 lessons documented (AC evidence, unified infrastructure, bridge epics)
- Claude Code can extract relevant lessons (tested via queries)
- Team validates lessons are actionable and clear

---

### Story 3.5.3: Test-Dependency Audit Documentation
**Owner:** Winston | **Estimate:** 4h | **Priority:** P0

**Goal:** Document comprehensive process for auditing test dependencies and their impacts (performance, compatibility, security), addressing "dependency audit process still undocumented" finding.

**Deliverables:**
- `docs/dependency-audit-process.md` - Step-by-step audit process
- Test impact categories (unit, integration, performance, fixtures)
- Performance baseline process (pytest-benchmark)
- Troubleshooting guide with Epic 3 examples (spaCy, pandas, jq)
- CI/CD integration documentation

**Success Criteria:**
- Process tested by auditing scikit-learn for Epic 4
- Examples from Epic 3 dependencies (spaCy caching, jq binary, pandas)
- Team can follow process for future dependency additions

---

### Story 3.5.4: Semantic Dependencies + Smoke Test
**Owner:** Charlie | **Estimate:** 4h | **Priority:** P0

**Goal:** Install and validate semantic analysis dependencies (scikit-learn, joblib, gensim) with smoke tests, eliminating Epic 4 first-story dependency blockers.

**Deliverables:**
- `pyproject.toml` updated with scikit-learn, joblib, gensim
- `tests/smoke/test_semantic_*.py` - Import, TF-IDF, LSA, similarity, caching smoke tests
- pip-audit security scan passed
- CI/CD pipeline updated with smoke tests

**Success Criteria:**
- All semantic dependencies installed and validated
- No critical/high security vulnerabilities
- TF-IDF, LSA, cosine similarity smoke tests pass
- Epic 4 can start implementation immediately (no dependency delays)

---

### Story 3.5.5: Model/Cache ADR (Architecture Decision Record)
**Owner:** Winston | **Estimate:** 4h | **Priority:** P0

**Goal:** Create ADR-012 documenting model storage, caching, and versioning strategies for Epic 4 semantic analysis (TF-IDF vectorizers, LSA models), preventing mid-Epic 4 architecture debates.

**Deliverables:**
- `docs/architecture-decisions/ADR-012-model-caching-strategy.md`
- Cache location decision (user home ~/.data-extract/models/ with fallback)
- Serialization format decision (joblib with compress=3)
- Versioning strategy (corpus hash + semantic version)
- Cache invalidation strategy (automatic + manual)
- Performance targets (<100ms load, <5s train, <500MB total)

**Success Criteria:**
- ADR follows standard template (Context, Decision, Consequences, Alternatives)
- Team approves caching strategy (Winston + Charlie architecture review)
- Versioning supports reproducibility (provenance requirement)
- Epic 4 stories can implement consistent caching per ADR-012

---

### Story 3.5.6: Semantic QA Fixtures
**Owner:** Dana (QA) | **Estimate:** 6h | **Priority:** P0

**Goal:** Create comprehensive test fixtures with known semantic relationships (similar/dissimilar document pairs, topic clusters) for Epic 4 semantic analysis validation.

**Deliverables:**
- `tests/fixtures/semantic_corpus.py` - 20-30 audit document snippets
- Similarity ground truth labels (30+ pairs with expected scores)
- Topic cluster labels (5-8 clusters for topic modeling validation)
- Edge case documents (very similar, very dissimilar, short, long, jargon)
- `tests/fixtures/semantic_README.md` - Fixture documentation

**Success Criteria:**
- Corpus covers diverse audit topics (risks, controls, compliance, processes)
- Similarity labels annotated by human experts (Dana + domain expert, >80% agreement)
- pytest fixtures provide structured data for Epic 4 tests
- Epic 4 can validate TF-IDF/LSA correctness against ground truth

---

### Story 3.5.7: TF-IDF/LSA Implementation Playbook
**Owner:** Charlie + Elena | **Estimate:** 4h | **Priority:** P0

**Goal:** Create comprehensive playbook with TF-IDF/LSA code examples, best practices, and gotchas, enabling Epic 4 developers to implement semantic features without trial-and-error learning.

**Deliverables:**
- `docs/tfidf-lsa-playbook.md` - Comprehensive developer guide (400-600 lines)
- TF-IDF deep dive (configuration, preprocessing, audit domain examples)
- LSA deep dive (n_components selection, interpretation, examples)
- Cosine similarity patterns (pairwise, top-K, thresholds)
- Caching patterns (joblib, reference ADR-012)
- Testing patterns (use Story 3.5.6 fixtures)
- Best practices (configuration recommendations, performance tips)
- Common gotchas (empty docs, vocabulary mismatch, n_components bugs)

**Success Criteria:**
- All code examples execute without errors (runnable Python)
- Examples use Story 3.5.6 fixtures for audit domain realism
- Team validates playbook is helpful for Epic 4 implementation
- Developers can adapt examples to Epic 4 specific requirements

---

## Epic 3.5 Dependencies

### Prerequisites:
- **Epic 3 Complete (Chunk & Output)** - All 7 stories done, retrospective complete
- **Epic 3 Retrospective (2025-11-16)** - Action items and prep tasks identified
- **Quality Gate Automation (Story 2.5.3)** - Pre-commit hooks for templates
- **spaCy Caching Precedent (Story 2.5.2)** - Pattern for model caching

### Enables:
- **Epic 4 (Foundational Semantic Analysis)** - All Epic 4 stories
- **Future Semantic Epics** - Patterns and tooling reusable

---

## Epic 3.5 Success Criteria

### Completion Criteria:
- [ ] All 7 stories complete (DoD met, UAT passed)
- [ ] Templates tested with Epic 4 first story
- [ ] CLAUDE.md lessons section reviewed by team
- [ ] Dependency audit process validated (scikit-learn audit)
- [ ] Semantic dependencies smoke tests passing in CI/CD
- [ ] ADR-012 approved by architecture review (Winston + Charlie)
- [ ] Semantic fixtures validated by domain expert (Dana + expert)
- [ ] TF-IDF/LSA playbook validated by Epic 4 developers (Charlie + Elena)

### Epic 4 Readiness Gates:
- [ ] No dependency blockers (scikit-learn, joblib, gensim installed)
- [ ] Model caching strategy documented (ADR-012)
- [ ] Test fixtures ready (semantic_corpus.py with ground truth)
- [ ] Implementation guidance ready (tfidf-lsa-playbook.md)
- [ ] Lessons learned documented (avoid Epic 3 mistakes)

### Quality Gates:
- [ ] All code passes pre-commit hooks (black, ruff, mypy)
- [ ] All tests pass (smoke tests, unit tests, integration tests)
- [ ] All documentation reviewed (templates, playbook, ADR, audit doc)
- [ ] Security scan passed (pip-audit with no critical vulnerabilities)

---

## Epic 3.5 Timeline

**Sprint Structure:** 2.5-day preparation sprint before Epic 4 planning

### Day 1 (Stories 3.5.1-3.5.3):
- Story 3.5.1: Story/Review Template Generator (Elena, 4h)
- Story 3.5.2: CLAUDE.md Lessons Section (Bob, 4h)
- Story 3.5.3: Test-Dependency Audit Doc (Winston, 4h)
- **Checkpoint:** Templates and documentation complete

### Day 2 (Stories 3.5.4-3.5.5):
- Story 3.5.4: Semantic Dependencies + Smoke Test (Charlie, 4h)
- Story 3.5.5: Model/Cache ADR (Winston, 4h)
- **Checkpoint:** Dependencies installed, architecture documented

### Day 2.5 (Stories 3.5.6-3.5.7):
- Story 3.5.6: Semantic QA Fixtures (Dana, 6h)
- Story 3.5.7: TF-IDF/LSA Playbook (Charlie + Elena, 4h)
- **Checkpoint:** Test fixtures and implementation guidance complete

### Day 3 (Epic Review):
- Team retrospective: What worked well? Any gaps?
- Epic 4 planning review: Are we ready to start?
- Green light to Epic 4 sprint planning

---

## Epic 3.5 Risks & Mitigation

### Risk: Inter-annotator agreement <80% for semantic fixtures (Story 3.5.6)
- **Impact:** Ground truth labels unreliable for Epic 4 validation
- **Probability:** Low (Dana + domain expert both have audit background)
- **Mitigation:** If <80%, discuss disagreements until consensus
- **Contingency:** Accept 70-80% agreement with documented ambiguous cases

### Risk: Dependency conflicts (scikit-learn incompatible with existing packages)
- **Impact:** Epic 4 blocked on dependency resolution
- **Probability:** Low (scikit-learn widely compatible)
- **Mitigation:** Test installation early (Story 3.5.4), follow audit process (Story 3.5.3)
- **Contingency:** Use pip-tools or poetry for dependency resolution

### Risk: Team bandwidth (2.5 days may be tight)
- **Impact:** Epic 3.5 incomplete, Epic 4 starts with gaps
- **Probability:** Medium (realistic estimate from retro, but dependencies exist)
- **Mitigation:** Prioritize P0 stories first, defer P1 if needed
- **Contingency:** Extend to 3-4 days if critical path stories need more time

---

## Epic 3.5 Key Learnings (To Be Updated Post-Epic)

**Placeholder for retrospective insights from Epic 3.5 execution:**

- What worked well?
- What challenges did we face?
- What would we do differently next time?
- What patterns should we reuse for future bridge epics?

**Note:** This section will be populated after Epic 3.5 retrospective, then added to CLAUDE.md Lessons Learned section (Story 3.5.2 pattern).

---

## Epic 3.5 References

### Retrospectives:
- `docs/retrospectives/epic-3-retro-2025-11-16.md` - Source for Epic 3.5 action items

### Stories:
- `docs/stories/3.5-1-story-review-template-generator.md`
- `docs/stories/3.5-2-claude-md-lessons-section.md`
- `docs/stories/3.5-3-test-dependency-audit-doc.md`
- `docs/stories/3.5-4-semantic-dependencies-smoke-test.md`
- `docs/stories/3.5-5-model-cache-adr.md`
- `docs/stories/3.5-6-semantic-qa-fixtures.md`
- `docs/stories/3.5-7-tfidf-lsa-playbook.md`

### Related Documentation:
- `.claude/CLAUDE.md` - Updated with Lessons Learned (Story 3.5.2)
- `docs/dependency-audit-process.md` - Created in Story 3.5.3
- `docs/architecture-decisions/ADR-012-model-caching-strategy.md` - Created in Story 3.5.5
- `docs/tfidf-lsa-playbook.md` - Created in Story 3.5.7

### Related Epics:
- Epic 3: Chunk & Output (Complete - prerequisite)
- Epic 4: Foundational Semantic Analysis (Next - enabled by Epic 3.5)

---

## Appendix: Bridge Epic Pattern

Epic 3.5 follows the **bridge epic pattern** established in Epic 2.5:

### Bridge Epic Characteristics:
1. **Preparation Focus:** Addresses infrastructure, tooling, documentation gaps
2. **Retrospective-Driven:** Action items from previous epic retrospective
3. **Short Duration:** 2-4 days typical (vs 2-4 weeks for feature epics)
4. **Enables Next Epic:** Removes blockers, provides guidance for upcoming work
5. **Cross-Functional:** Involves multiple roles (Dev, QA, Arch, SM)

### When to Create Bridge Epics:
- Previous epic retrospective identifies significant preparation needs
- Next epic requires new dependencies, tooling, or architecture decisions
- Team identifies patterns/lessons that need documentation
- Risk of mid-sprint blockers if preparation deferred

### Bridge Epic Success Patterns (Epic 2.5):
- **Quality Gate Automation (Story 2.5.3):** Pre-commit hooks prevent quality issues
- **UAT Framework (Story 2.5.3.1):** Systematic validation reduces rework
- **Performance Profiling (Story 2.5.2.1):** Baselines catch regressions early
- **CI/CD Enhancement (Story 2.5.4):** Caching and monitoring improve developer experience

### Epic 3.5 Applies These Patterns:
- Story templates (3.5.1) = Quality gate automation for story structure
- Lessons learned (3.5.2) = Institutional memory like UAT framework docs
- Dependency audit (3.5.3) = Process like performance profiling
- Smoke tests (3.5.4) = Quick validation like CI/CD caching

---

**Epic 3.5 Status:** TODO - Ready for team kickoff
**Next Milestone:** Epic 4 Planning Review (after Epic 3.5 complete)
**Epic Owner:** Charlie (Dev Lead) + Bob (SM)
