# Engineering Backlog

This backlog collects cross-cutting or future action items that emerge from reviews and planning.

Routing guidance:

- Use this file for non-urgent optimizations, refactors, or follow-ups that span multiple stories/epics.
- Must-fix items to ship a story belong in that story’s `Tasks / Subtasks`.
- Same-epic improvements may also be captured under the epic Tech Spec `Post-Review Follow-ups` section.

| Date | Story | Epic | Type | Severity | Owner | Status | Notes |
| ---- | ----- | ---- | ---- | -------- | ----- | ------ | ----- |
| 2025-11-15 | 3.4 | 3 | Bug | High | TBD | Open | Propagate chunk config + source file metadata so JSON headers report real chunk_size/overlap (`src/data_extract/chunk/metadata_enricher.py`, `src/data_extract/output/formatters/json_formatter.py`). |
| 2025-11-15 | 3.4 | 3 | Bug | High | TBD | Open | Normalize `ChunkMetadata.to_dict()` so all required fields serialize without nulls and include source_file provenance (`src/data_extract/chunk/models.py`). |
| 2025-11-15 | 3.4 | 3 | Bug | Medium | TBD | Open | Reinstate UTF-8 BOM support when writing JSON as required by AC-3.4-2 (`src/data_extract/output/formatters/json_formatter.py`). |
| 2025-11-15 | 3.4 | 3 | Bug | Medium | TBD | Open | Surface schema validation failures as hard errors instead of silent `FormatResult` entries (`src/data_extract/output/formatters/json_formatter.py`). |
| 2025-11-15 | 3.4 | 3 | Documentation | Low | TBD | Open | Update Dev Agent File List / docs to enumerate formatter base + unit test changes for traceability (`docs/stories/3-4-json-output-format-with-full-metadata.md`). |
