"""
Generate large PDF fixture for integration testing.

Creates a 50+ page synthetic audit report with realistic structure.
Uses reportlab to generate PDF with headings, paragraphs, and tables.
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def generate_large_audit_pdf(output_path: Path) -> None:
    """Generate a large (50+ page) synthetic audit report PDF."""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#1a1a1a"),
        spaceAfter=30,
        alignment=1,  # Center
    )

    heading1_style = ParagraphStyle(
        "CustomHeading1", parent=styles["Heading1"], fontSize=16, spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        "CustomHeading2", parent=styles["Heading2"], fontSize=14, spaceAfter=10
    )

    # --- Cover Page ---
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Annual Internal Audit Report", title_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Fiscal Year 2024", styles["Heading2"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph(
            "Enterprise Risk Management & Compliance Assessment", styles["Normal"]
        )
    )
    story.append(PageBreak())

    # --- Table of Contents ---
    story.append(Paragraph("Table of Contents", heading1_style))
    toc_items = [
        "1. Executive Summary ............................ 3",
        "2. Risk Assessment Findings ..................... 5",
        "3. Control Framework Evaluation ................. 18",
        "4. Compliance Review Results .................... 32",
        "5. Recommendations .............................. 45",
        "6. Appendix: Audit Policies ..................... 50",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles["Normal"]))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # --- Executive Summary (3 pages) ---
    story.append(Paragraph("1. Executive Summary", heading1_style))
    story.append(
        Paragraph(
            "This report presents the findings of the annual internal audit conducted "
            "for the fiscal year 2024. The audit focused on enterprise risk management, "
            "internal controls, and regulatory compliance across all business units.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    for section_num in range(1, 4):
        story.append(
            Paragraph(f"1.{section_num} Key Findings Overview", heading2_style)
        )
        for para in range(3):
            story.append(
                Paragraph(
                    f"The audit identified {15 + section_num * 3} areas requiring management attention, "
                    f"including {5 + para} high-priority items. Overall control effectiveness was rated "
                    "as satisfactory with opportunities for improvement in operational efficiency and "
                    "compliance monitoring processes. Detailed findings are presented in subsequent sections.",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 12))
    story.append(PageBreak())

    # --- Risk Assessment Findings (15+ pages) ---
    story.append(Paragraph("2. Risk Assessment Findings", heading1_style))
    story.append(
        Paragraph(
            "The risk assessment evaluated inherent and residual risks across strategic, "
            "operational, financial, and compliance categories.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    risk_categories = [
        "Strategic Risks",
        "Operational Risks",
        "Financial Risks",
        "Compliance Risks",
        "Technology Risks",
    ]

    for idx, category in enumerate(risk_categories, start=1):
        story.append(Paragraph(f"2.{idx} {category}", heading2_style))

        # Risk table
        risk_data = [
            ["Risk ID", "Description", "Impact", "Likelihood", "Rating"],
            [
                f"R-{idx}01",
                "Market volatility impact on revenue",
                "High",
                "Medium",
                "High",
            ],
            [
                f"R-{idx}02",
                "Supply chain disruption risk",
                "High",
                "High",
                "Critical",
            ],
            [
                f"R-{idx}03",
                "Talent retention challenges",
                "Medium",
                "Medium",
                "Medium",
            ],
            [
                f"R-{idx}04",
                "Regulatory compliance gaps",
                "High",
                "Low",
                "Medium",
            ],
            [
                f"R-{idx}05",
                "Cybersecurity threat exposure",
                "Critical",
                "Medium",
                "High",
            ],
        ]

        risk_table = Table(risk_data, colWidths=[0.8 * inch, 2.5 * inch, 0.8 * inch, 1 * inch, 0.8 * inch])
        risk_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                ]
            )
        )
        story.append(risk_table)
        story.append(Spacer(1, 12))

        # Analysis paragraphs
        for para_num in range(4):
            story.append(
                Paragraph(
                    f"Analysis of {category.lower()} reveals significant exposure in areas {para_num + 1} through "
                    f"{para_num + 3}. Current mitigation strategies are partially effective but require enhancement. "
                    "Management has committed to implementing recommended controls within the next fiscal quarter. "
                    "Ongoing monitoring will be essential to ensure risk levels remain within acceptable tolerances.",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 12))

        if idx < len(risk_categories):
            story.append(PageBreak())

    # --- Control Framework Evaluation (12+ pages) ---
    story.append(Paragraph("3. Control Framework Evaluation", heading1_style))
    story.append(
        Paragraph(
            "The control framework assessment evaluated design effectiveness and operating effectiveness "
            "of key controls across all business processes.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    control_areas = [
        "Financial Controls",
        "IT General Controls",
        "Operations Controls",
        "Compliance Controls",
    ]

    for idx, area in enumerate(control_areas, start=1):
        story.append(Paragraph(f"3.{idx} {area}", heading2_style))

        # Control testing results table
        control_data = [
            ["Control ID", "Control Description", "Test Result", "Deficiencies"],
            [
                f"C-{idx}001",
                "Segregation of duties verification",
                "Effective",
                "None",
            ],
            [
                f"C-{idx}002",
                "Authorization approval workflows",
                "Partially Effective",
                "2 Minor",
            ],
            [
                f"C-{idx}003",
                "Reconciliation processes",
                "Effective",
                "None",
            ],
            [
                f"C-{idx}004",
                "Access control reviews",
                "Ineffective",
                "1 Major",
            ],
            [
                f"C-{idx}005",
                "Change management controls",
                "Effective",
                "None",
            ],
        ]

        control_table = Table(
            control_data, colWidths=[1 * inch, 2.5 * inch, 1.2 * inch, 1.2 * inch]
        )
        control_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                ]
            )
        )
        story.append(control_table)
        story.append(Spacer(1, 12))

        for para_num in range(5):
            story.append(
                Paragraph(
                    f"Testing of {area.lower()} demonstrated overall satisfactory performance with "
                    f"{para_num + 2} controls operating as designed. However, {para_num + 1} control deficiencies "
                    "were identified requiring management remediation. Action plans have been developed with "
                    "target completion dates within 90 days. Follow-up testing will validate remediation effectiveness.",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 12))

        story.append(PageBreak())

    # --- Compliance Review (10+ pages) ---
    story.append(Paragraph("4. Compliance Review Results", heading1_style))
    story.append(
        Paragraph(
            "The compliance review assessed adherence to applicable laws, regulations, and internal policies "
            "across all operating jurisdictions.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    compliance_domains = [
        "Regulatory Compliance",
        "Data Privacy Compliance",
        "Environmental Compliance",
    ]

    for idx, domain in enumerate(compliance_domains, start=1):
        story.append(Paragraph(f"4.{idx} {domain}", heading2_style))

        # Compliance findings table
        findings_data = [
            ["Finding ID", "Requirement", "Status", "Action Required"],
            [
                f"F-{idx}001",
                "SOX Section 404 controls",
                "Compliant",
                "None",
            ],
            [
                f"F-{idx}002",
                "GDPR data subject rights",
                "Non-Compliant",
                "Remediation Plan",
            ],
            [
                f"F-{idx}003",
                "Industry standard certifications",
                "Compliant",
                "None",
            ],
            [
                f"F-{idx}004",
                "Environmental reporting",
                "Compliant",
                "None",
            ],
        ]

        findings_table = Table(
            findings_data, colWidths=[1 * inch, 2.2 * inch, 1.2 * inch, 1.5 * inch]
        )
        findings_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                ]
            )
        )
        story.append(findings_table)
        story.append(Spacer(1, 12))

        for para_num in range(6):
            story.append(
                Paragraph(
                    f"The {domain.lower()} assessment covered {para_num + 5} regulatory requirements and "
                    f"identified {para_num + 1} areas requiring attention. Management has developed comprehensive "
                    "remediation plans with dedicated resources assigned. Compliance monitoring processes have been "
                    "enhanced to prevent recurrence. Ongoing assessments will track progress against commitments.",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 12))

        story.append(PageBreak())

    # --- Recommendations (5+ pages) ---
    story.append(Paragraph("5. Recommendations", heading1_style))
    story.append(
        Paragraph(
            "Based on audit findings, the following recommendations are provided to strengthen "
            "the control environment and address identified deficiencies.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    for rec_num in range(1, 16):
        story.append(Paragraph(f"5.{rec_num} Recommendation #{rec_num}", heading2_style))
        story.append(
            Paragraph(
                f"Management should implement enhanced controls for risk area #{rec_num} by establishing "
                "clear accountability, defining measurable objectives, and allocating appropriate resources. "
                "This will improve overall risk posture and ensure compliance with applicable requirements. "
                "Implementation timeline: 90-120 days. Expected impact: High.",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 12))

        if rec_num % 3 == 0:
            story.append(PageBreak())

    # --- Appendix (5+ pages) ---
    story.append(Paragraph("6. Appendix: Audit Policies", heading1_style))
    story.append(
        Paragraph(
            "The following audit policies and methodologies were applied during this assessment.",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 12))

    policies = [
        "Risk Assessment Methodology",
        "Control Testing Standards",
        "Sampling Techniques",
        "Documentation Requirements",
        "Quality Assurance Procedures",
    ]

    for idx, policy in enumerate(policies, start=1):
        story.append(Paragraph(f"6.{idx} {policy}", heading2_style))
        for para in range(3):
            story.append(
                Paragraph(
                    f"The {policy.lower()} follows industry best practices and professional standards. "
                    "Audit procedures are designed to provide reasonable assurance regarding the effectiveness "
                    "of controls and the accuracy of reported information. All findings are documented with "
                    "sufficient evidence to support conclusions and recommendations. Independence and objectivity "
                    "are maintained throughout the audit process.",
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 12))

        if idx < len(policies):
            story.append(PageBreak())

    # Build PDF
    doc.build(story)
    print(f"Generated large PDF: {output_path}")
    print(f"File size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "tests" / "fixtures" / "pdfs" / "large"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "audit-report-large.pdf"
    generate_large_audit_pdf(output_file)
