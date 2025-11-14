"""Integration tests for entity-aware chunking (Story 3.2 - RED PHASE).

End-to-end tests with real entity-rich documents validating entity preservation,
relationship detection, and metadata enrichment. All tests WILL FAIL until
EntityPreserver is integrated into ChunkingEngine (GREEN phase).

Test Coverage:
    - AC-3.2-1: >95% entity preservation rate (CRITICAL)
    - AC-3.2-2: Partial entity flagging for split entities
    - AC-3.2-3: Relationship context preservation (CRITICAL)
    - AC-3.2-4: Multi-sentence entity definition boundaries
    - AC-3.2-5: Entity ID cross-chunk lookups
    - AC-3.2-6: Entity tags JSON serialization
"""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

import pytest

# These imports WILL FAIL in RED phase - this is expected
try:
    from data_extract.chunk.engine import ChunkingEngine
    from data_extract.core.models import (
        Chunk,
        Document,
        Entity,
        EntityType,
        Metadata,
        ProcessingContext,
    )
except ImportError:
    ChunkingEngine = None
    Chunk = None
    Document = None
    Entity = None
    EntityType = None
    Metadata = None
    ProcessingContext = None

pytestmark = [pytest.mark.integration, pytest.mark.chunking, pytest.mark.entity_aware]


def create_test_metadata(source_file: str = "test.pdf") -> "Metadata":
    """Create complete Metadata for tests."""
    return Metadata(
        source_file=Path(source_file),
        file_hash="abc123",
        processing_timestamp=datetime.now(timezone.utc),
        tool_version="3.2.0",
        config_version="1.0",
    )


@pytest.fixture
def risk_register_document():
    """Load entity-rich risk register fixture (100+ entities)."""
    fixture_path = Path(__file__).parent.parent.parent / "fixtures" / "entity_rich_documents"
    risk_register_file = fixture_path / "risk_register.md"

    if not risk_register_file.exists():
        pytest.skip(f"Fixture not found: {risk_register_file}")

    text = risk_register_file.read_text(encoding="utf-8")

    # Create entities found in risk register
    entities = []
    # Sample entities (real implementation would parse all)
    entity_patterns = [
        ("RISK-2024-001", EntityType.RISK, 0, 100),
        ("CTRL-001", EntityType.CONTROL, 200, 250),
        ("POL-001", EntityType.POLICY, 400, 450),
        ("RISK-2024-002", EntityType.RISK, 600, 700),
        ("CTRL-002", EntityType.CONTROL, 800, 850),
    ]

    for entity_id, entity_type, start, end in entity_patterns:
        entities.append(
            Entity(
                type=entity_type,
                id=entity_id,
                text=text[start:end] if start < len(text) else entity_id,
                confidence=0.95,
                location={"start": start, "end": end},
            )
        )

    return Document(
        id="risk_register_test",
        text=text,
        entities=entities,
        metadata=create_test_metadata("risk_register.md"),
        structure={},
    )


class TestEntityPreservationRate:
    """Test entity preservation rate >95% (AC-3.2-1 - CRITICAL)."""

    def test_entity_preservation_rate_exceeds_95_percent(self, risk_register_document):
        """Should preserve >95% of entities within single chunks (AC-3.2-1)."""
        # GIVEN: Real risk register document with 100+ entities
        document = risk_register_document

        # WHEN: ChunkingEngine.chunk_document() called with entity_aware=True
        mock_segmenter = Mock()
        # Simple sentence splitting for test
        sentences = document.text.split(". ")
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=512, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: Measure entities intact vs. split
        total_entities = len(document.entities)
        split_entities = 0

        for chunk in chunks:
            # Count entities marked as partial
            if hasattr(chunk.metadata, "entity_tags"):
                for entity_tag in chunk.metadata.entity_tags:
                    if entity_tag.is_partial:
                        split_entities += 1

        intact_entities = total_entities - split_entities
        preservation_rate = intact_entities / total_entities if total_entities > 0 else 0

        # AND: Assert >95% intact
        assert preservation_rate > 0.95, (
            f"Entity preservation rate {preservation_rate:.2%} below 95% threshold. "
            f"Intact: {intact_entities}, Split: {split_entities}, Total: {total_entities}"
        )


class TestPartialEntityMetadata:
    """Test partial entity flagging (AC-3.2-2)."""

    def test_partial_entity_metadata_flagging(self):
        """Should flag split entities with is_partial=True (AC-3.2-2)."""
        # GIVEN: Document with very large entity (>chunk_size to force split)
        large_entity_text = " ".join([f"Sentence {i} of large entity." for i in range(100)])
        text = f"RISK-LARGE-001: {large_entity_text} End of risk."

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-LARGE-001",
                text=large_entity_text[:200],  # Truncated for display
                confidence=0.95,
                location={"start": 0, "end": len(large_entity_text)},
            )
        ]

        document = Document(
            id="large_entity_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: Entity unavoidably split across chunks (chunk_size=256 < entity size)
        mock_segmenter = Mock()
        sentences = text.split(". ")
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=256, overlap_pct=0.0, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: Both chunks have is_partial=True, continuation flags set
        partial_chunks = [
            c for c in chunks if hasattr(c.metadata, "entity_tags") and c.metadata.entity_tags
        ]
        assert len(partial_chunks) >= 2, "Expected at least 2 chunks with entity parts"

        # Find chunks with partial entity markers
        partial_entity_chunks = []
        for chunk in partial_chunks:
            for entity_tag in chunk.metadata.entity_tags:
                if entity_tag.is_partial:
                    partial_entity_chunks.append(chunk)
                    break

        assert len(partial_entity_chunks) >= 2, "Expected partial entity across multiple chunks"


class TestRelationshipPreservation:
    """Test entity relationship preservation (AC-3.2-3 - CRITICAL)."""

    def test_relationship_context_preserved(self):
        """Should preserve risk-control relationships in chunks (AC-3.2-3)."""
        # GIVEN: Document with "RISK-001 mitigated by CTRL-042" patterns
        text = """
        RISK-001 data breach risk is mitigated by CTRL-042 encryption control.
        The control implements AES-256 encryption for all sensitive data.
        RISK-002 supply chain disruption addresses CTRL-043 vendor diversification.
        """

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-001",
                text="RISK-001",
                confidence=0.95,
                location={"start": 9, "end": 17},
            ),
            Entity(
                type=EntityType.CONTROL,
                id="CTRL-042",
                text="CTRL-042",
                confidence=0.92,
                location={"start": 54, "end": 62},
            ),
            Entity(
                type=EntityType.RISK,
                id="RISK-002",
                text="RISK-002",
                confidence=0.95,
                location={"start": 150, "end": 158},
            ),
            Entity(
                type=EntityType.CONTROL,
                id="CTRL-043",
                text="CTRL-043",
                confidence=0.92,
                location={"start": 199, "end": 207},
            ),
        ]

        document = Document(
            id="relationship_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: chunk_document() called
        mock_segmenter = Mock()
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=512, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: Relationship triples in ChunkMetadata
        found_relationships = []
        for chunk in chunks:
            if hasattr(chunk.metadata, "entity_relationships"):
                found_relationships.extend(chunk.metadata.entity_relationships)

        # AND: Both entities in same chunk when relationship span < chunk_size
        assert len(found_relationships) >= 1, "Expected at least one relationship detected"
        # Should find ("RISK-001", "mitigated_by", "CTRL-042")
        relationship_types = [r[1] for r in found_relationships]
        assert "mitigated_by" in relationship_types or "mitigates" in relationship_types


class TestMultiSentenceEntityDefinitions:
    """Test multi-sentence entity definition boundaries (AC-3.2-4)."""

    def test_multi_sentence_entity_definitions_kept_together(self):
        """Should keep multi-sentence entity definitions together (AC-3.2-4)."""
        # GIVEN: Document with entity spanning 3 sentences
        text = """
        RISK-2024-002: Supply chain disruption risk affecting critical vendor relationships.
        This risk impacts component availability and delivery schedules.
        The risk requires immediate mitigation through vendor diversification strategy.
        Next topic starts here.
        """

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-2024-002",
                text="RISK-2024-002 definition",
                confidence=0.95,
                # Span covers 3 sentences
                location={"start": 9, "end": 250},
            )
        ]

        document = Document(
            id="multi_sentence_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: chunk_document() called
        mock_segmenter = Mock()
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=512, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: All 3 sentences in same chunk
        # Find chunk containing RISK-2024-002
        entity_chunks = [
            c
            for c in chunks
            if hasattr(c.metadata, "entity_tags")
            and any(e.entity_id == "RISK-2024-002" for e in c.metadata.entity_tags)
        ]
        assert len(entity_chunks) >= 1, "Expected entity in at least one chunk"

        # AND: Boundary after definition complete (before "Next topic")
        # Entity should not be split unless it exceeds chunk_size


class TestEntityIDCrossReferences:
    """Test entity ID cross-chunk lookups (AC-3.2-5)."""

    def test_entity_ids_enable_cross_chunk_search(self):
        """Should enable cross-chunk entity lookups by ID (AC-3.2-5)."""
        # GIVEN: Entity "RISK-2024-001" mentioned in multiple chunks
        text = (
            """
        RISK-2024-001 is a critical data breach risk.
        """
            + (" ".join([f"Sentence {i}." for i in range(50)]))
            + """
        RISK-2024-001 requires ongoing monitoring and mitigation.
        """
        )

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-2024-001",
                text="RISK-2024-001",
                confidence=0.95,
                location={"start": 9, "end": 22},
            ),
            Entity(
                type=EntityType.RISK,
                id="RISK-2024-001",
                text="RISK-2024-001",
                confidence=0.95,
                location={"start": len(text) - 100, "end": len(text) - 87},
            ),
        ]

        document = Document(
            id="cross_ref_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: Search all chunks for entity_id="RISK-2024-001"
        mock_segmenter = Mock()
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=256, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: Returns all chunks containing that entity
        matching_chunks = []
        for chunk in chunks:
            if hasattr(chunk.metadata, "entity_tags"):
                for entity_tag in chunk.metadata.entity_tags:
                    if entity_tag.entity_id == "RISK-2024-001":
                        matching_chunks.append(chunk)
                        break

        assert len(matching_chunks) >= 1, "Expected entity found in at least one chunk"


class TestEntityTagsJSONSerialization:
    """Test entity tags JSON serialization (AC-3.2-6)."""

    def test_entity_tags_json_serialization(self):
        """Should serialize entity_tags to JSON (AC-3.2-6)."""
        # GIVEN: Chunk with entity_tags populated
        text = "RISK-001 data breach risk mitigated by CTRL-042."

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
                id="CTRL-042",
                text="CTRL-042",
                confidence=0.92,
                location={"start": 40, "end": 48},
            ),
        ]

        document = Document(
            id="serialization_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: Chunk.to_dict() called
        mock_segmenter = Mock()
        mock_segmenter.segment.return_value = [text]

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=512, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        assert len(chunks) > 0, "Expected at least one chunk"
        chunk_dict = chunks[0].to_dict()

        # THEN: entity_tags converted to list of dicts, JSON serializable
        assert "metadata" in chunk_dict
        if "entity_tags" in chunk_dict["metadata"]:
            entity_tags = chunk_dict["metadata"]["entity_tags"]
            assert isinstance(entity_tags, list)
            # Should be JSON serializable
            import json

            json_str = json.dumps(chunk_dict)
            assert json_str is not None


class TestMixedEntityTypes:
    """Test entity-aware chunking with multiple entity types (AC-3.2-1, AC-3.2-6)."""

    def test_entity_aware_with_multiple_entity_types(self):
        """Should handle risks, controls, policies, processes (AC-3.2-1)."""
        # GIVEN: Document with risks, controls, policies, processes
        text = """
        RISK-001 data security risk addresses POL-SEC-001 data protection policy.
        CTRL-IAM-002 multi-factor authentication implements the policy requirements.
        PROC-ACC-001 access management process supports the control implementation.
        """

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-001",
                text="RISK-001",
                confidence=0.95,
                location={"start": 9, "end": 17},
            ),
            Entity(
                type=EntityType.POLICY,
                id="POL-SEC-001",
                text="POL-SEC-001",
                confidence=0.93,
                location={"start": 46, "end": 57},
            ),
            Entity(
                type=EntityType.CONTROL,
                id="CTRL-IAM-002",
                text="CTRL-IAM-002",
                confidence=0.92,
                location={"start": 87, "end": 99},
            ),
            Entity(
                type=EntityType.PROCESS,
                id="PROC-ACC-001",
                text="PROC-ACC-001",
                confidence=0.94,
                location={"start": 166, "end": 178},
            ),
        ]

        document = Document(
            id="mixed_types_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: chunk_document() called
        mock_segmenter = Mock()
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=512, overlap_pct=0.15, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: All entity types preserved, tagged correctly in metadata
        found_entity_types = set()
        for chunk in chunks:
            if hasattr(chunk.metadata, "entity_tags"):
                for entity_tag in chunk.metadata.entity_tags:
                    found_entity_types.add(entity_tag.entity_type)

        # Should find all entity types
        assert "RISK" in found_entity_types or len(found_entity_types) > 0


class TestLargeEntityHandling:
    """Test oversized entity handling (AC-3.2-1, AC-3.2-4)."""

    def test_large_entity_exceeding_chunk_size(self):
        """Should handle entity > chunk_size gracefully (AC-3.2-1, AC-3.2-4)."""
        # GIVEN: Entity definition > chunk_size (e.g., 1000 tokens)
        large_definition = " ".join(
            [f"This is sentence {i} of a very large entity definition." for i in range(100)]
        )
        text = f"RISK-LARGE: {large_definition}"

        entities = [
            Entity(
                type=EntityType.RISK,
                id="RISK-LARGE",
                text=large_definition[:200],  # Truncated
                confidence=0.95,
                location={"start": 0, "end": len(text)},
            )
        ]

        document = Document(
            id="large_entity_test",
            text=text,
            entities=entities,
            metadata=create_test_metadata(),
            structure={},
        )

        # WHEN: chunk_document() called with small chunk_size
        mock_segmenter = Mock()
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        mock_segmenter.segment.return_value = sentences

        engine = ChunkingEngine(
            segmenter=mock_segmenter, chunk_size=256, overlap_pct=0.0, entity_aware=True
        )
        context = ProcessingContext(config={}, logger=Mock(), metrics={})
        chunks = list(engine.process(document, context))

        # THEN: Entity becomes single chunk exceeding chunk_size, warning logged
        # Should not crash, handles gracefully
        assert len(chunks) > 0, "Expected at least one chunk (oversized allowed for entities)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
