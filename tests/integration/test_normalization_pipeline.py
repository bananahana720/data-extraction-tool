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
