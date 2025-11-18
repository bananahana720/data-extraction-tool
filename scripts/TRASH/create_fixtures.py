#!/usr/bin/env python3
"""Create minimal test fixtures for testing framework."""
import sys
from pathlib import Path

# Create a minimal PDF using reportlab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf_path = Path("tests/fixtures/pdfs/sample.pdf")
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Sample PDF for Testing")
    c.drawString(100, 730, "This is a minimal test document.")
    c.drawString(100, 710, "Content: Lorem ipsum dolor sit amet.")
    c.save()
    print(f"Created: {pdf_path} ({pdf_path.stat().st_size} bytes)")
except ImportError:
    print("Warning: reportlab not installed, skipping PDF creation")

# Create a minimal test image using PIL
try:
    from PIL import Image, ImageDraw, ImageFont

    img_path = Path("tests/fixtures/images/sample.png")
    img = Image.new('RGB', (400, 200), color='white')
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Sample Image for OCR Testing\nTest Document 123", fill='black')
    img.save(str(img_path))
    print(f"Created: {img_path} ({img_path.stat().st_size} bytes)")
except ImportError:
    print("Warning: PIL not installed, skipping image creation")

print("Fixture creation completed")
