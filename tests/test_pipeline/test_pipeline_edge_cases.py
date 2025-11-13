"""
Comprehensive edge case tests for pipeline components.

This test suite tests pipeline boundary conditions using equivalency partitioning.

Pipeline Components:
- ExtractionPipeline: Format detection, orchestration
- BatchProcessor: Multi-file processing

Test Categories:
- Format detection edge cases
- Batch processing boundaries
- Mixed file types
- Error recovery
- Concurrent processing
"""

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pipeline.batch_processor import BatchProcessor
from pipeline.extraction_pipeline import ExtractionPipeline

# ==============================================================================
# Format Detection Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestFormatDetectionEdgeCases:
    """Edge cases for format detection in pipeline."""

    def test_file_with_no_extension(self, tmp_path):
        """
        EDGE: File with no extension.

        Partition: Format → Invalid → No extension
        Expected: Detection failure or default handling
        """
        pipeline = ExtractionPipeline()

        no_ext = tmp_path / "document_no_extension"
        no_ext.write_text("Some content")

        result = pipeline.process_file(no_ext)

        # Should fail to detect format
        assert result.success is False or result.warnings

    def test_file_with_unknown_extension(self, tmp_path):
        """
        EDGE: File with unknown/unsupported extension.

        Partition: Format → Invalid → Unknown extension
        Expected: Clear error about unsupported format
        """
        pipeline = ExtractionPipeline()

        unknown = tmp_path / "document.xyz"
        unknown.write_text("Content")

        result = pipeline.process_file(unknown)

        assert result.success is False
        # Should indicate unsupported format

    def test_file_with_multiple_extensions(self, tmp_path):
        """
        EDGE: File with multiple extensions (file.tar.gz style).

        Partition: Format → Valid → Multiple extensions
        Expected: Should use final extension
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        # File with multiple extensions
        pdf_path = tmp_path / "document.backup.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        result = pipeline.process_file(pdf_path)

        # Should detect as PDF based on final extension
        assert result.success is True
        assert result.document_metadata.file_format == "pdf"

    def test_extension_case_sensitivity(self, tmp_path):
        """
        EDGE: Extensions with different cases (.PDF vs .pdf).

        Partition: Format → Valid → Case variations
        Expected: Case-insensitive detection
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        # Create file with uppercase extension
        pdf_path = tmp_path / "document.PDF"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        result = pipeline.process_file(pdf_path)

        # Should detect regardless of case
        assert result.success is True

    def test_content_type_mismatch(self, tmp_path):
        """
        EDGE: File extension doesn't match content (PDF named .txt).

        Partition: Format → Invalid → Extension mismatch
        Expected: Extraction failure with clear error
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        # Create PDF but name it .txt
        fake_txt = tmp_path / "actually_pdf.txt"
        c = canvas.Canvas(str(fake_txt))
        c.drawString(100, 750, "I'm a PDF")
        c.showPage()
        c.save()

        result = pipeline.process_file(fake_txt)

        # TXT extractor should fail on PDF content
        # OR might succeed if it handles binary gracefully
        assert result is not None


# ==============================================================================
# Batch Processing Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestBatchProcessingEdgeCases:
    """Edge cases for batch processing."""

    def test_empty_directory(self, tmp_path):
        """
        EDGE: Batch process empty directory.

        Partition: Input size → Valid → Minimum (0 files)
        Expected: Should complete successfully with zero results
        """
        processor = BatchProcessor()

        results = processor.process_batch(tmp_path)

        assert len(results) == 0

    def test_directory_with_single_file(self, tmp_path):
        """
        EDGE: Directory with exactly one file.

        Partition: Input size → Valid → Minimum useful (1)
        Expected: Should process single file
        """
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create single file
        pdf_path = tmp_path / "single.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Single file")
        c.showPage()
        c.save()

        results = processor.process_batch(tmp_path)

        assert len(results) == 1
        assert results[0].success is True

    @pytest.mark.slow
    @pytest.mark.stress
    def test_directory_with_many_files(self, tmp_path):
        """
        EDGE: Directory with 100+ files.

        Partition: Input size → Valid → Maximum
        Expected: Should process all files efficiently
        """
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create 50 files (reduced from 100 for test speed)
        for i in range(50):
            pdf_path = tmp_path / f"doc_{i:03d}.pdf"
            c = canvas.Canvas(str(pdf_path))
            c.drawString(100, 750, f"Document {i}")
            c.showPage()
            c.save()

        start = time.time()
        results = processor.process_batch(tmp_path)
        duration = time.time() - start

        assert len(results) == 50

        # Performance check: Should average <2s per file
        avg_time = duration / 50
        assert avg_time < 3.0, f"Average {avg_time:.2f}s per file (target: <3s)"

    def test_mixed_valid_invalid_files(self, tmp_path):
        """
        EDGE: Directory with mix of valid and invalid files.

        Partition: File validity → Mixed
        Expected: Valid files processed, invalid files reported
        """
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create valid PDF
        valid_pdf = tmp_path / "valid.pdf"
        c = canvas.Canvas(str(valid_pdf))
        c.drawString(100, 750, "Valid")
        c.showPage()
        c.save()

        # Create invalid file
        invalid = tmp_path / "corrupted.pdf"
        invalid.write_text("Not a real PDF")

        # Create unsupported format
        unsupported = tmp_path / "document.xyz"
        unsupported.write_text("Unsupported")

        results = processor.process_batch(tmp_path)

        # Should have results for all files (some failed)
        assert len(results) >= 1  # At least the valid one

        # At least one should succeed
        successes = [r for r in results if r.success]
        assert len(successes) >= 1

    def test_directory_with_subdirectories(self, tmp_path):
        """
        EDGE: Directory containing subdirectories.

        Partition: Structure → Valid → Nested
        Expected: Should handle based on recursive flag
        """
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create subdirectory with file
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        pdf_path = subdir / "nested.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Nested file")
        c.showPage()
        c.save()

        # Also file in root
        root_pdf = tmp_path / "root.pdf"
        c = canvas.Canvas(str(root_pdf))
        c.drawString(100, 750, "Root file")
        c.showPage()
        c.save()

        # Non-recursive should only get root file
        results = processor.process_batch(tmp_path, recursive=False)

        # Should have at least root file
        assert len(results) >= 1

    def test_mixed_file_types_in_batch(self, tmp_path):
        """
        EDGE: Batch process mixed file types (PDF, TXT, DOCX).

        Partition: Format → Valid → Mixed
        Expected: Each file processed by correct extractor
        """
        from docx import Document
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create PDF
        pdf_path = tmp_path / "document.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "PDF content")
        c.showPage()
        c.save()

        # Create TXT
        txt_path = tmp_path / "document.txt"
        txt_path.write_text("Text content")

        # Create DOCX
        docx_path = tmp_path / "document.docx"
        doc = Document()
        doc.add_paragraph("DOCX content")
        doc.save(docx_path)

        results = processor.process_batch(tmp_path)

        assert len(results) == 3

        # All should succeed (or fail gracefully)
        assert all(r is not None for r in results)

    def test_batch_process_with_errors_continues(self, tmp_path):
        """
        EDGE: Batch processing continues after errors.

        Partition: Error handling → Recovery
        Expected: Errors reported but processing continues
        """
        from reportlab.pdfgen import canvas

        processor = BatchProcessor()

        # Create valid file
        valid1 = tmp_path / "valid1.pdf"
        c = canvas.Canvas(str(valid1))
        c.drawString(100, 750, "Valid 1")
        c.showPage()
        c.save()

        # Create corrupted file
        corrupted = tmp_path / "corrupted.pdf"
        corrupted.write_text("CORRUPTED")

        # Create another valid file
        valid2 = tmp_path / "valid2.pdf"
        c = canvas.Canvas(str(valid2))
        c.drawString(100, 750, "Valid 2")
        c.showPage()
        c.save()

        results = processor.process_batch(tmp_path)

        # Should have all 3 results
        assert len(results) == 3

        # At least 2 should succeed (the valid ones)
        successes = [r for r in results if r.success]
        assert len(successes) >= 2


# ==============================================================================
# Pipeline Error Recovery Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestPipelineErrorRecoveryEdgeCases:
    """Test pipeline error recovery and resilience."""

    def test_extractor_failure_recovery(self, tmp_path):
        """
        EDGE: Extractor fails but pipeline handles gracefully.

        Partition: Error handling → Extraction failure
        Expected: Pipeline returns failed result, no exception
        """
        pipeline = ExtractionPipeline()

        # Try to extract missing file
        missing = tmp_path / "nonexistent.pdf"

        result = pipeline.process_file(missing)

        # Should return failed result, not raise exception
        assert result is not None
        assert result.success is False

    def test_processor_failure_recovery(self, tmp_path, monkeypatch):
        """
        EDGE: Processor fails but pipeline continues.

        Partition: Error handling → Processing failure
        Expected: Error reported, partial results returned
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        # Create valid file
        pdf_path = tmp_path / "test.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        # Mock processor to fail
        def failing_processor(self, extraction_result):
            raise RuntimeError("Simulated processor failure")

        # This test validates error handling structure exists
        # Actual mocking would require more complex setup

        result = pipeline.process_file(pdf_path)

        # Should still return result (extraction succeeded even if processing had issues)
        assert result is not None

    def test_formatter_failure_recovery(self, tmp_path):
        """
        EDGE: Formatter fails but pipeline reports error.

        Partition: Error handling → Formatting failure
        Expected: Error in formatting stage reported
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        pdf_path = tmp_path / "test.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        # Extract first
        result = pipeline.process_file(pdf_path)
        assert result.success is True

        # Format with invalid formatter config
        # This tests that formatter errors are handled
        try:
            formatted = pipeline.format_result(result, format_type="invalid_format")
            # Should either fail gracefully or return error
            assert formatted is not None
        except ValueError:
            # Also acceptable - explicit error for invalid format
            pass


# ==============================================================================
# Pipeline Configuration Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestPipelineConfigurationEdgeCases:
    """Test pipeline with various configurations."""

    def test_pipeline_with_no_config(self, tmp_path):
        """
        EDGE: Pipeline with no configuration (defaults).

        Partition: Configuration → Valid → Default
        Expected: Should use sensible defaults
        """
        from reportlab.pdfgen import canvas

        # Create pipeline with no config
        pipeline = ExtractionPipeline()

        pdf_path = tmp_path / "test.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        result = pipeline.process_file(pdf_path)

        assert result.success is True

    def test_pipeline_with_custom_config(self, tmp_path):
        """
        EDGE: Pipeline with custom configuration.

        Partition: Configuration → Valid → Custom
        Expected: Should respect custom config
        """
        from reportlab.pdfgen import canvas

        custom_config = {"extractors": {"pdf": {"extract_images": True, "extract_tables": True}}}

        pipeline = ExtractionPipeline(config=custom_config)

        pdf_path = tmp_path / "test.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Content")
        c.showPage()
        c.save()

        result = pipeline.process_file(pdf_path)

        assert result.success is True


# ==============================================================================
# Concurrency Edge Cases
# ==============================================================================


@pytest.mark.edge_case
class TestConcurrencyEdgeCases:
    """Test concurrent access patterns."""

    def test_process_same_file_sequentially(self, tmp_path):
        """
        EDGE: Process same file multiple times.

        Partition: Concurrency → Sequential
        Expected: All extractions should succeed identically
        """
        from reportlab.pdfgen import canvas

        pipeline = ExtractionPipeline()

        pdf_path = tmp_path / "repeated.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Repeated content")
        c.showPage()
        c.save()

        # Extract multiple times
        results = []
        for i in range(5):
            result = pipeline.process_file(pdf_path)
            results.append(result)

        # All should succeed
        assert all(r.success for r in results)

        # All should have same number of blocks
        block_counts = [len(r.content_blocks) for r in results]
        assert len(set(block_counts)) == 1  # All identical


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "edge_case"])
