"""
Generate scanned PDF fixture for OCR integration testing.

Creates an image-based PDF that requires OCR to extract text.
Uses PIL to render text to images, then combines into PDF.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_scanned_page_image(page_num: int, output_dir: Path) -> Path:
    """Create a single page as an image with rendered text."""
    # Create white background image (letter size at 150 DPI)
    width, height = 1275, 1650  # 8.5" x 11" at 150 DPI
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Try to use a standard font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        heading_font = ImageFont.truetype("arial.ttf", 36)
        body_font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        # Fallback to default font
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw content based on page number
    y_position = 100

    if page_num == 1:
        # Title page
        draw.text(
            (width // 2, y_position),
            "CONFIDENTIAL AUDIT REPORT",
            fill="black",
            font=title_font,
            anchor="mt",
        )
        y_position += 150

        draw.text(
            (width // 2, y_position),
            "Internal Controls Assessment",
            fill="black",
            font=heading_font,
            anchor="mt",
        )
        y_position += 100

        draw.text(
            (width // 2, y_position),
            "Fiscal Year 2024",
            fill="black",
            font=body_font,
            anchor="mt",
        )
        y_position += 200

        draw.text(
            (150, y_position),
            "This document contains sensitive information regarding",
            fill="black",
            font=body_font,
        )
        y_position += 50
        draw.text(
            (150, y_position),
            "the organization's internal controls and audit findings.",
            fill="black",
            font=body_font,
        )
        y_position += 50
        draw.text(
            (150, y_position),
            "Distribution is restricted to authorized personnel only.",
            fill="black",
            font=body_font,
        )

    elif page_num == 2:
        # Executive summary
        draw.text(
            (150, y_position), "Executive Summary", fill="black", font=heading_font
        )
        y_position += 100

        summary_lines = [
            "The annual internal audit was conducted over a three-month period",
            "covering all major business processes and control frameworks. The",
            "assessment included evaluation of 247 key controls across financial",
            "reporting, IT general controls, and operational processes.",
            "",
            "Key Findings:",
            "- 85% of tested controls were found to be operating effectively",
            "- 23 control deficiencies identified requiring management action",
            "- 5 high-priority findings requiring immediate remediation",
            "- Overall control environment rated as 'Satisfactory'",
            "",
            "Management has committed to addressing all identified deficiencies",
            "within 90 days and has allocated appropriate resources for",
            "remediation activities. Follow-up testing is scheduled for Q2 2024.",
        ]

        for line in summary_lines:
            draw.text((150, y_position), line, fill="black", font=body_font)
            y_position += 45

    elif page_num == 3:
        # Risk assessment table
        draw.text(
            (150, y_position), "Risk Assessment Results", fill="black", font=heading_font
        )
        y_position += 100

        # Simple table header
        draw.rectangle([(150, y_position), (1100, y_position + 40)], fill="lightgray")
        draw.text((170, y_position + 10), "Risk Area", fill="black", font=body_font)
        draw.text((450, y_position + 10), "Rating", fill="black", font=body_font)
        draw.text((650, y_position + 10), "Status", fill="black", font=body_font)
        y_position += 50

        # Table rows
        risk_data = [
            ("Financial Reporting", "Medium", "Acceptable"),
            ("IT Security", "High", "Action Required"),
            ("Operations", "Low", "Acceptable"),
            ("Compliance", "Medium", "Monitoring"),
            ("Third-Party Risk", "High", "Action Required"),
        ]

        for risk_area, rating, status in risk_data:
            draw.rectangle(
                [(150, y_position), (1100, y_position + 40)], outline="black"
            )
            draw.text((170, y_position + 10), risk_area, fill="black", font=body_font)
            draw.text((450, y_position + 10), rating, fill="black", font=body_font)
            draw.text((650, y_position + 10), status, fill="black", font=body_font)
            y_position += 50

        y_position += 50
        conclusion_lines = [
            "The risk assessment identified areas requiring enhanced controls",
            "and monitoring. Management action plans are in place for all",
            "high-priority risks with quarterly progress reviews scheduled.",
        ]

        for line in conclusion_lines:
            draw.text((150, y_position), line, fill="black", font=body_font)
            y_position += 45

    else:
        # Generic page
        draw.text(
            (150, y_position),
            f"Page {page_num} - Additional Details",
            fill="black",
            font=heading_font,
        )
        y_position += 100

        generic_lines = [
            f"This page contains supplementary information related to the audit",
            f"findings and recommendations. Detailed control testing procedures,",
            f"evidence documentation, and management responses are included in",
            f"the appendices. All findings have been discussed with responsible",
            f"management and action plans have been agreed upon.",
        ]

        for line in generic_lines:
            draw.text((150, y_position), line, fill="black", font=body_font)
            y_position += 45

    # Add page number footer
    draw.text(
        (width // 2, height - 100),
        f"Page {page_num}",
        fill="gray",
        font=body_font,
        anchor="mt",
    )

    # Save image
    img_path = output_dir / f"page_{page_num}.png"
    img.save(img_path, "PNG", dpi=(150, 150))
    return img_path


def generate_scanned_pdf(output_path: Path, num_pages: int = 5) -> None:
    """Generate a scanned PDF by combining rendered image pages."""
    temp_dir = output_path.parent / "temp_images"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Create image pages
        print(f"Generating {num_pages} scanned pages...")
        image_paths = []
        for page_num in range(1, num_pages + 1):
            img_path = create_scanned_page_image(page_num, temp_dir)
            image_paths.append(img_path)
            print(f"  Created page {page_num}")

        # Combine images into PDF
        print("Combining images into PDF...")
        c = canvas.Canvas(str(output_path), pagesize=letter)
        page_width, page_height = letter

        for img_path in image_paths:
            # Draw image on PDF page
            c.drawImage(
                str(img_path),
                0,
                0,
                width=page_width,
                height=page_height,
                preserveAspectRatio=True,
            )
            c.showPage()

        c.save()

        print(f"Generated scanned PDF: {output_path}")
        print(f"File size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")

    finally:
        # Clean up temporary images
        for img_path in temp_dir.glob("*.png"):
            img_path.unlink()
        temp_dir.rmdir()


if __name__ == "__main__":
    output_dir = (
        Path(__file__).parent.parent / "tests" / "fixtures" / "pdfs" / "scanned"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "audit-scan.pdf"
    generate_scanned_pdf(output_file, num_pages=5)
