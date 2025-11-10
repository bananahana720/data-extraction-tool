"""
Test fixtures for extractor tests.

Provides sample files and data structures for testing extractors.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_pdf_file(tmp_path: Path) -> Path:
    """
    Create a sample PDF file for testing.

    Generates a simple PDF with text content including heading-like patterns.

    Args:
        tmp_path: Pytest built-in temporary directory

    Returns:
        Path to generated PDF file
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed")

    file_path = tmp_path / "test_document.pdf"

    # Create PDF
    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter

    # Add content with heading-like patterns
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Test PDF Document")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This is a test PDF for integration testing.")
    c.drawString(100, height - 170, "It contains multiple lines of text.")

    c.drawString(100, height - 220, "Section 1: Introduction")
    c.drawString(100, height - 240, "This is the introduction section.")

    c.drawString(100, height - 290, "Section 2: Content")
    c.drawString(100, height - 310, "This section contains the main content.")
    c.drawString(100, height - 330, "Multiple paragraphs are included.")

    # Add second page
    c.showPage()
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, "Page 2")
    c.drawString(100, height - 120, "This is the second page of the document.")

    c.save()
    return file_path
