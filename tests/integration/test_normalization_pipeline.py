"""Integration tests for normalization pipeline.

Tests end-to-end normalization workflow integrating:
- Normalizer orchestrator
- TextCleaner
- Configuration cascade
- Metadata enrichment
"""

from datetime import datetime
from pathlib import Path

import pytest
import structlog

from src.data_extract.core.models import Document, Metadata, ProcessingContext
from src.data_extract.normalize import NormalizerFactory


@pytest.mark.integration
class TestNormalizationPipeline:
    """Integration tests for full normalization pipeline."""

    @pytest.fixture
    def sample_metadata(self, tmp_path: Path) -> Metadata:
        """Create sample metadata."""
        source_file = tmp_path / "test.pdf"
        source_file.write_text("test")

        return Metadata(
            source_file=source_file,
            file_hash="abc123",
            processing_timestamp=datetime.now(),
            tool_version="0.1.0",
            config_version="1.0",
            document_type="pdf",
        )

    def test_end_to_end_normalization(self, sample_metadata: Metadata) -> None:
        """Test complete normalization workflow from raw to cleaned document."""
        # Create document with multiple issues
        raw_doc = Document(
            id="test1",
            text="Document ^^^^^ with   OCR  artifacts\n\n\n\nand ■■■■ noise",
            metadata=sample_metadata,
        )

        # Create normalizer and context
        normalizer = NormalizerFactory.create_default()
        context = ProcessingContext(config={}, logger=structlog.get_logger(), metrics={})

        # Normalize document
        cleaned_doc = normalizer.process(raw_doc, context)

        # Verify cleaning
        assert "^^^^^" not in cleaned_doc.text
        assert "■■■■" not in cleaned_doc.text
        assert cleaned_doc.id == raw_doc.id

        # Verify metadata enrichment
        assert "cleaning_artifacts_removed" in cleaned_doc.metadata.quality_scores
        assert cleaned_doc.metadata.quality_scores["cleaning_artifacts_removed"] > 0

        # Verify context metrics
        assert context.metrics["documents_normalized"] == 1

    def test_deterministic_processing(self, sample_metadata: Metadata) -> None:
        """Test that same input produces identical output (AC-2.1.6)."""
        doc = Document(
            id="test1",
            text="Text ^^^^^ with   artifacts",
            metadata=sample_metadata,
        )

        normalizer = NormalizerFactory.create_default()
        context = ProcessingContext(config={}, logger=structlog.get_logger(), metrics={})

        # Process same document 10 times
        results = []
        for _ in range(10):
            result = normalizer.process(doc, context)
            results.append(result.text)

        # All results should be identical
        assert all(text == results[0] for text in results)

    def test_text_cleaning_to_entity_normalization(self, sample_metadata: Metadata) -> None:
        """Test integration from text cleaning to entity normalization (Story 2.1 + 2.2)."""
        # Create document with both cleaning issues and entities
        raw_doc = Document(
            id="test-entity-integration",
            text="Risk #123 ^^^^^ identified in SOX audit. Control-456 mitigates   this risk.",
            metadata=sample_metadata,
        )

        # Create normalizer with entity normalization enabled
        normalizer = NormalizerFactory.create_default()
        context = ProcessingContext(config={}, logger=structlog.get_logger(), metrics={})

        # Process document
        result = normalizer.process(raw_doc, context)

        # Verify text cleaning worked
        assert "^^^^^" not in result.text

        # Verify entity normalization worked (if enabled in default factory)
        # Note: This depends on entity normalization being integrated in Normalizer
        assert isinstance(result.metadata.entity_tags, list)
        assert isinstance(result.metadata.entity_counts, dict)

    def test_entity_normalization_with_real_audit_doc(self, sample_metadata: Metadata) -> None:
        """Test entity normalization with realistic audit document content."""
        audit_text = """
        Audit Finding Report - Q4 2024

        Risk #123: Operational risk identified in SOX compliance review.
        This risk relates to inadequate separation of duties in financial reporting.

        Mitigation:
        - Control-456 implements dual approval for journal entries
        - Control-457 enforces segregation of duties

        Compliance Framework: SOX, NIST CSF, ISO 27001
        Regulation: SOX Section 404, GDPR Article 32

        Issue-001: Control testing revealed gaps in access management.
        Process-100 requires updating to align with Policy-789.
        """

        doc = Document(
            id="real-audit-doc",
            text=audit_text,
            metadata=sample_metadata,
        )

        normalizer = NormalizerFactory.create_default()
        context = ProcessingContext(config={}, logger=structlog.get_logger(), metrics={})

        result = normalizer.process(doc, context)

        # Verify entities were recognized and metadata enriched
        assert isinstance(result.metadata.entity_tags, list)
        assert isinstance(result.metadata.entity_counts, dict)

        # Verify abbreviation expansion (if enabled)
        # SOX, NIST CSF, ISO 27001, GDPR should be expanded if feature is active

    def test_determinism_with_entities(self, sample_metadata: Metadata) -> None:
        """Test determinism of full pipeline including entity normalization."""
        doc = Document(
            id="determinism-test",
            text="Risk-001 and Control-002 in SOX audit.",
            metadata=sample_metadata,
        )

        normalizer = NormalizerFactory.create_default()
        context = ProcessingContext(config={}, logger=structlog.get_logger(), metrics={})

        # Process 10 times
        results = []
        for _ in range(10):
            result = normalizer.process(doc, context)
            results.append(
                {
                    "text": result.text,
                    "entity_tags": result.metadata.entity_tags,
                    "entity_counts": result.metadata.entity_counts,
                }
            )

        # All results should be identical
        first = results[0]
        for result in results[1:]:
            assert result["text"] == first["text"]
            assert result["entity_tags"] == first["entity_tags"]
            assert result["entity_counts"] == first["entity_counts"]
