"""Unit tests for EntityPreserver component (Story 3.2 - RED PHASE).

Tests entity-aware boundary detection, relationship extraction, and entity reference
management. All tests WILL FAIL until EntityPreserver is implemented (GREEN phase).

Test Coverage:
    - AC-3.2-1: Entity preservation within chunks
    - AC-3.2-4: Entity definition boundary detection
    - AC-3.2-5: Entity ID cross-references
    - AC-3.2-6: Entity metadata tags
    - AC-3.2-8: Deterministic entity analysis
"""

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.chunk.entity_preserver import EntityPreserver, EntityReference
    from data_extract.core.models import Entity, EntityType
except ImportError:
    EntityPreserver = None
    EntityReference = None
    Entity = None
    EntityType = None

pytestmark = [pytest.mark.unit, pytest.mark.chunking, pytest.mark.entity_aware]


class TestEntityReferenceModel:
    """Test EntityReference dataclass creation and serialization (AC-3.2-6)."""

    def test_entity_reference_creation(self):
        """Should create EntityReference with all required fields."""
        # GIVEN: Entity data
        entity_type = "RISK"
        entity_id = "RISK-2024-001"
        start_pos = 100
        end_pos = 150
        is_partial = False
        context_snippet = "...Data breach risk involving..."

        # WHEN: EntityReference instantiated
        entity_ref = EntityReference(
            entity_type=entity_type,
            entity_id=entity_id,
            start_pos=start_pos,
            end_pos=end_pos,
            is_partial=is_partial,
            context_snippet=context_snippet,
        )

        # THEN: All fields populated correctly
        assert entity_ref.entity_type == entity_type
        assert entity_ref.entity_id == entity_id
        assert entity_ref.start_pos == start_pos
        assert entity_ref.end_pos == end_pos
        assert entity_ref.is_partial == is_partial
        assert entity_ref.context_snippet == context_snippet

    def test_entity_reference_frozen(self):
        """Should enforce immutability with frozen=True."""
        # GIVEN: EntityReference
        entity_ref = EntityReference(
            entity_type="CONTROL",
            entity_id="CTRL-001",
            start_pos=200,
            end_pos=220,
            is_partial=False,
            context_snippet="...Encryption control...",
        )

        # WHEN/THEN: Attempting to modify raises error
        with pytest.raises(AttributeError):
            entity_ref.entity_id = "CTRL-002"

    def test_entity_reference_to_dict(self):
        """Should serialize to JSON-compatible dict (AC-3.2-6)."""
        # GIVEN: EntityReference with all fields
        entity_ref = EntityReference(
            entity_type="POLICY",
            entity_id="POL-001",
            start_pos=500,
            end_pos=550,
            is_partial=True,
            context_snippet="...Data protection policy...",
        )

        # WHEN: to_dict() called
        result = entity_ref.to_dict()

        # THEN: Returns dict with all fields
        assert isinstance(result, dict)
        assert result["entity_type"] == "POLICY"
        assert result["entity_id"] == "POL-001"
        assert result["start_pos"] == 500
        assert result["end_pos"] == 550
        assert result["is_partial"] is True
        assert result["context_snippet"] == "...Data protection policy..."

        # AND: Dict is JSON serializable
        import json

        json_str = json.dumps(result)
        assert json_str is not None


class TestEntityPreserverAnalysis:
    """Test EntityPreserver.analyze_entities() method (AC-3.2-1, AC-3.2-6, AC-3.2-8)."""

    def test_analyze_entities_sorting(self):
        """Should sort entities by start_pos for determinism (AC-3.2-8)."""
        # GIVEN: Entities in random order
        text = "Risk RISK-003 affects system. Control CTRL-001 mitigates. Risk RISK-001 identified."
        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-003",
                text="RISK-003",
                confidence=0.95,
                location={"start": 5, "end": 14},
            ),
            Entity(
                type=EntityType.CONTROL,
                id="CTRL-001",
                text="CTRL-001",
                confidence=0.92,
                location={"start": 37, "end": 45},
            ),
            Entity(
                type=EntityType.RISK,
                id="RISK-001",
                text="RISK-001",
                confidence=0.93,
                location={"start": 63, "end": 71},
            ),
        ]

        # WHEN: analyze_entities() called
        preserver = EntityPreserver()
        entity_refs = preserver.analyze_entities(text, entities)

        # THEN: Returns EntityReferences sorted by start_pos
        assert len(entity_refs) == 3
        assert entity_refs[0].start_pos == 5  # RISK-003
        assert entity_refs[1].start_pos == 37  # CTRL-001
        assert entity_refs[2].start_pos == 63  # RISK-001
        assert entity_refs[0].entity_id == "RISK-003"
        assert entity_refs[1].entity_id == "CTRL-001"
        assert entity_refs[2].entity_id == "RISK-001"

    def test_analyze_entities_context_snippets(self):
        """Should extract context snippets around entities (AC-3.2-6)."""
        # GIVEN: Entity at various positions in text
        text = "The RISK-2024-001 data breach risk requires immediate attention and mitigation."
        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-2024-001",
                text="RISK-2024-001",
                confidence=0.95,
                location={"start": 4, "end": 17},
            )
        ]

        # WHEN: analyze_entities() called
        preserver = EntityPreserver()
        entity_refs = preserver.analyze_entities(text, entities)

        # THEN: context_snippet contains ±20 chars around entity
        snippet = entity_refs[0].context_snippet
        assert "RISK-2024-001" in snippet
        # Should include some surrounding text
        assert len(snippet) > len("RISK-2024-001")

    def test_analyze_entities_empty_list(self):
        """Should handle empty entity list gracefully (AC-3.2-1)."""
        # GIVEN: Text with no entities
        text = "This is plain text with no entity markers."
        entities = []

        # WHEN: analyze_entities() called
        preserver = EntityPreserver()
        entity_refs = preserver.analyze_entities(text, entities)

        # THEN: Returns empty list
        assert entity_refs == []

    def test_entities_at_document_boundaries(self):
        """Should handle entities at start/end of document (AC-3.2-1 edge case)."""
        # GIVEN: Entity at position 0 and end of text
        text = "RISK-001 is critical. CTRL-999"
        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-001",
                text="RISK-001",
                confidence=0.95,
                location={"start": 0, "end": 8},
            ),
            Entity(
                type=EntityType.CONTROL,
                id="CTRL-999",
                text="CTRL-999",
                confidence=0.92,
                location={"start": 22, "end": 30},
            ),
        ]

        # WHEN: analyze_entities() called
        preserver = EntityPreserver()
        entity_refs = preserver.analyze_entities(text, entities)

        # THEN: Context snippets truncated appropriately (no negative indices)
        assert len(entity_refs) == 2
        # First entity context should not cause negative index
        assert entity_refs[0].context_snippet is not None
        # Last entity context should not exceed text length
        assert entity_refs[1].context_snippet is not None


class TestEntityPreserverGaps:
    """Test EntityPreserver.find_entity_gaps() method (AC-3.2-1)."""

    def test_find_entity_gaps(self):
        """Should identify character offsets between entities (AC-3.2-1)."""
        # GIVEN: Text with multiple entities
        text = "RISK-001 description. CTRL-002 mitigates. POLICY-003 governs."
        entity_refs = [
            EntityReference(
                entity_type="RISK",
                entity_id="RISK-001",
                start_pos=0,
                end_pos=8,
                is_partial=False,
                context_snippet="RISK-001 description",
            ),
            EntityReference(
                entity_type="CONTROL",
                entity_id="CTRL-002",
                start_pos=22,
                end_pos=30,
                is_partial=False,
                context_snippet="CTRL-002 mitigates",
            ),
            EntityReference(
                entity_type="POLICY",
                entity_id="POLICY-003",
                start_pos=43,
                end_pos=53,
                is_partial=False,
                context_snippet="POLICY-003 governs",
            ),
        ]

        # WHEN: find_entity_gaps() called
        preserver = EntityPreserver()
        gaps = preserver.find_entity_gaps(entity_refs, text)

        # THEN: Returns character offsets between entities (safe split zones)
        assert isinstance(gaps, list)
        assert len(gaps) >= 2  # At least gaps between the 3 entities
        # Gaps should be in positions between entities
        for gap in gaps:
            # Gap should not be within any entity span
            for ref in entity_refs:
                assert not (ref.start_pos <= gap <= ref.end_pos)

    def test_find_entity_gaps_no_entities(self):
        """Should return empty list when no entities (AC-3.2-1 edge case)."""
        # GIVEN: Text with no entities
        text = "Plain text with no entity markers."
        entity_refs = []

        # WHEN: find_entity_gaps() called
        preserver = EntityPreserver()
        gaps = preserver.find_entity_gaps(entity_refs, text)

        # THEN: Returns empty list (no gaps to find)
        assert gaps == []

    def test_overlapping_entities_handling(self):
        """Should handle overlapping entity spans gracefully (AC-3.2-1 edge case)."""
        # GIVEN: Entities with overlapping start/end positions
        text = "RISK-CTRL-001 combined entity reference"
        entity_refs = [
            EntityReference(
                entity_type="RISK",
                entity_id="RISK-001",
                start_pos=0,
                end_pos=9,
                is_partial=False,
                context_snippet="RISK-CTRL-001",
            ),
            EntityReference(
                entity_type="CONTROL",
                entity_id="CTRL-001",
                start_pos=5,
                end_pos=13,
                is_partial=False,
                context_snippet="CTRL-001 combined",
            ),
        ]

        # WHEN: find_entity_gaps() called
        preserver = EntityPreserver()
        gaps = preserver.find_entity_gaps(entity_refs, text)

        # THEN: Handles gracefully (prefer earlier entity or flag both)
        # Should not crash, returns valid gap list (may be empty for overlaps)
        assert isinstance(gaps, list)


class TestEntityPreserverRelationships:
    """Test EntityPreserver.detect_entity_relationships() method (AC-3.2-3)."""

    def test_detect_entity_relationships_mitigated_by(self):
        """Should detect 'mitigated by' relationship pattern (AC-3.2-3)."""
        # GIVEN: Text with "RISK-001 mitigated by CTRL-042" pattern
        text = "RISK-001 is mitigated by CTRL-042 encryption control."
        entity_refs = [
            EntityReference(
                entity_type="RISK",
                entity_id="RISK-001",
                start_pos=0,
                end_pos=8,
                is_partial=False,
                context_snippet="RISK-001 is mitigated",
            ),
            EntityReference(
                entity_type="CONTROL",
                entity_id="CTRL-042",
                start_pos=25,
                end_pos=33,
                is_partial=False,
                context_snippet="by CTRL-042 encryption",
            ),
        ]

        # WHEN: detect_entity_relationships() called
        preserver = EntityPreserver()
        relationships = preserver.detect_entity_relationships(text, entity_refs)

        # THEN: Returns triple ("RISK-001", "mitigated_by", "CTRL-042")
        assert len(relationships) >= 1
        assert isinstance(relationships, list)
        # Find the mitigated_by relationship
        mitigated_rel = [r for r in relationships if r[1] == "mitigated_by"]
        assert len(mitigated_rel) >= 1
        assert mitigated_rel[0] == ("RISK-001", "mitigated_by", "CTRL-042")

    def test_detect_entity_relationships_multiple_patterns(self):
        """Should detect various relationship keywords (AC-3.2-3)."""
        # GIVEN: Text with "maps to", "implements", "addresses" patterns
        text = (
            "CTRL-001 maps to REQ-001. "
            "PROC-002 implements CTRL-001. "
            "POLICY-003 addresses RISK-005."
        )
        entity_refs = [
            EntityReference(
                entity_type="CONTROL",
                entity_id="CTRL-001",
                start_pos=0,
                end_pos=8,
                is_partial=False,
                context_snippet="CTRL-001 maps",
            ),
            EntityReference(
                entity_type="REQUIREMENT",
                entity_id="REQ-001",
                start_pos=17,
                end_pos=24,
                is_partial=False,
                context_snippet="to REQ-001",
            ),
            EntityReference(
                entity_type="PROCESS",
                entity_id="PROC-002",
                start_pos=26,
                end_pos=34,
                is_partial=False,
                context_snippet="PROC-002 implements",
            ),
            EntityReference(
                entity_type="POLICY",
                entity_id="POLICY-003",
                start_pos=57,
                end_pos=67,
                is_partial=False,
                context_snippet="POLICY-003 addresses",
            ),
            EntityReference(
                entity_type="RISK",
                entity_id="RISK-005",
                start_pos=78,
                end_pos=86,
                is_partial=False,
                context_snippet="addresses RISK-005",
            ),
        ]

        # WHEN: detect_entity_relationships() called
        preserver = EntityPreserver()
        relationships = preserver.detect_entity_relationships(text, entity_refs)

        # THEN: Returns triples for all detected relationships
        assert len(relationships) >= 3
        # Should find maps_to, implements, addresses relationships
        relationship_types = [r[1] for r in relationships]
        assert "maps_to" in relationship_types or "maps to" in relationship_types
        assert "implements" in relationship_types
        assert "addresses" in relationship_types

    def test_detect_entity_relationships_no_relationships(self):
        """Should return empty list when no relationships detected."""
        # GIVEN: Text with entities but no relationship keywords
        text = "RISK-001 exists. CTRL-002 exists separately."
        entity_refs = [
            EntityReference(
                entity_type="RISK",
                entity_id="RISK-001",
                start_pos=0,
                end_pos=8,
                is_partial=False,
                context_snippet="RISK-001 exists",
            ),
            EntityReference(
                entity_type="CONTROL",
                entity_id="CTRL-002",
                start_pos=17,
                end_pos=25,
                is_partial=False,
                context_snippet="CTRL-002 exists",
            ),
        ]

        # WHEN: detect_entity_relationships() called
        preserver = EntityPreserver()
        relationships = preserver.detect_entity_relationships(text, entity_refs)

        # THEN: Returns empty list
        assert relationships == []


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
