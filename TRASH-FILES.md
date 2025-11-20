test_utils/ - moved to TRASH/ - migrated to tests/unit/data_extract/utils/
test_extract/ - moved to TRASH/ - migrated to tests/unit/data_extract/extract/
test_normalize/ - moved to TRASH/ - migrated to tests/unit/data_extract/normalize/
test_chunk/ - moved to TRASH/ - migrated to tests/unit/data_extract/chunk/
test_output/ - moved to TRASH/ - migrated to tests/unit/data_extract/output/
test_semantic/ - moved to TRASH/ - migrated to tests/unit/data_extract/semantic/

## Wave 3 Phase 3: Test Deletion Execution
**Date:** 2025-11-20
**Approved by:** Murat (Master Test Architect)

### Wave 1: Demo/Template Files (Priority 1)
tests/support/ - moved to TRASH/ - support utilities directory (zero execution value)
tests/test_fixtures_demo.py - moved to TRASH/ - demo code, never executed
tests/fixtures/test_fixtures.py - moved to TRASH/ - template fixture tests
tests/fixtures/test_story_fixtures.py - moved to TRASH/ - story template tests
tests/fixtures/semantic_corpus.py - moved to TRASH/ - corpus template only
tests/fixtures/semantic/generate_corpus.py - moved to TRASH/ - generator template
tests/fixtures/semantic/generate_enhanced_corpus.py - moved to TRASH/ - template code
tests/fixtures/semantic/generate_full_corpus.py - moved to TRASH/ - unused generator
tests/fixtures/semantic/generate_gold_standard.py - moved to TRASH/ - template generator
tests/validation/semantic_validator.py - moved to TRASH/ - validation utility
tests/fixtures/semantic/harness/compare-entities.py - moved to TRASH/ - comparison utility
tests/fixtures/semantic/harness/compare-lsa.py - moved to TRASH/ - comparison utility
tests/fixtures/semantic/harness/compare-tfidf.py - moved to TRASH/ - comparison utility
tests/fixtures/semantic/validate_pii.py - moved to TRASH/ - one-time validation

### Wave 2: Getter/Setter Tests (Priority 2)
tests/test_infrastructure/test_config_manager.py - moved to TRASH/ - getter/setter tests only
tests/test_infrastructure/test_error_handler.py - moved to TRASH/ - property access tests
tests/test_infrastructure/test_logging_framework.py - moved to TRASH/ - log level getters/setters
tests/test_infrastructure/test_progress_tracker.py - moved to TRASH/ - progress property access

### Wave 3: Structure-Only Tests (Priority 3)
tests/test_cli/test_threading.py - moved to TRASH/ - only checks thread structure
tests/test_cli/test_encoding.py - moved to TRASH/ - only validates encoding types
tests/test_cli/test_signal_handling.py - moved to TRASH/ - structure checks only
tests/test_pipeline/test_pipeline_edge_cases.py - moved to TRASH/ - unrealistic edge cases
tests/test_processors/test_processor_edge_cases.py - moved to TRASH/ - structure validation only

### Wave 4: Trivial Edge Cases (Priority 4)
tests/test_edge_cases/ - moved to TRASH/ - entire directory of unrealistic edge cases
tests/test_poppler_config.py - moved to TRASH/ - config test only
tests/test_docx_extractor.py - moved to TRASH/ - root level duplicate of unit test
tests/uat/execute_story_3_3_uat.py - moved to TRASH/ - one-time UAT script
