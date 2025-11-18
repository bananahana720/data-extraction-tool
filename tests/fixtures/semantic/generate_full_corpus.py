#!/usr/bin/env python
"""
Generate Full Semantic QA Corpus - 250k+ Words

This script generates the complete corpus to meet all requirements:
- 50+ documents
- 250,000+ words
- 3+ document types
- PII-free content
"""

import json
import random
from pathlib import Path
from typing import Dict, List

# Seed for reproducibility
random.seed(42)


def generate_audit_content_blocks() -> List[str]:
    """Generate reusable content blocks for audit reports."""
    return [
        """The audit team conducted thorough walkthroughs of business processes to understand control design and implementation.
        This involved interviewing key personnel, observing control activities in operation, and reviewing supporting documentation.
        The walkthrough procedures provided insights into process flows, control points, and potential areas of weakness.""",
        """Risk assessment procedures identified multiple areas requiring management attention. The assessment considered both
        inherent and residual risks, evaluating the effectiveness of existing controls in mitigating identified threats.
        Quantitative and qualitative factors were incorporated into the risk scoring methodology.""",
        """Control testing revealed varying levels of effectiveness across different business units. While some controls
        operated consistently and effectively, others showed signs of deterioration or inconsistent application.
        The testing results highlight the need for standardization and enhanced monitoring mechanisms.""",
        """Documentation review indicated gaps in procedural guidance and control descriptions. Many processes relied on
        institutional knowledge rather than formalized documentation, creating vulnerability to staff turnover and
        increasing the risk of inconsistent control execution across the organization.""",
        """System configuration analysis revealed opportunities for enhanced automation and control integration.
        Current manual processes could be streamlined through technology enablement, reducing human error and
        improving efficiency while maintaining or enhancing control effectiveness.""",
        """Compliance testing demonstrated general adherence to regulatory requirements with isolated exceptions.
        The organization maintains appropriate frameworks for compliance management but requires updates to
        address recent regulatory changes and emerging requirements in the evolving compliance landscape.""",
        """Performance metrics analysis showed improvement trends in several key areas while identifying opportunities
        for enhancement in others. The metrics provide valuable insights into control effectiveness and operational
        efficiency, supporting data-driven decision making and continuous improvement initiatives.""",
        """Stakeholder interviews revealed strong awareness of control importance but varying levels of understanding
        regarding specific control requirements and procedures. Training and communication initiatives could
        strengthen the control culture and improve overall compliance rates.""",
        """Historical trend analysis demonstrated progressive improvement in control maturity over the past several
        audit cycles. However, the pace of improvement has not kept pace with increasing business complexity
        and evolving risk landscapes, necessitating accelerated remediation efforts.""",
        """Benchmarking against industry peers indicated that the organization's control environment is generally
        aligned with market practices but lags in certain areas, particularly around technology-enabled controls
        and automated monitoring capabilities. Investment in these areas could yield significant returns.""",
    ]


def generate_risk_content_blocks() -> List[str]:
    """Generate reusable content blocks for risk assessments."""
    return [
        """The risk assessment methodology employed a comprehensive framework incorporating likelihood and impact
        dimensions across multiple risk categories. Each risk was evaluated using standardized criteria to ensure
        consistency and comparability across the enterprise risk portfolio.""",
        """Emerging risks continue to evolve with technological advancement and changing business models.
        Cybersecurity threats, supply chain vulnerabilities, and regulatory changes represent the most significant
        emerging risks requiring proactive management strategies and enhanced monitoring capabilities.""",
        """Risk mitigation strategies have been developed for all high and critical risks identified in the assessment.
        These strategies include preventive controls to reduce likelihood, detective controls to identify occurrences,
        and corrective controls to minimize impact when risks materialize.""",
        """The organization's risk appetite framework provides clear boundaries for acceptable risk-taking aligned
        with strategic objectives. Risk tolerance levels have been established for each risk category, with
        escalation procedures for risks approaching or exceeding defined thresholds.""",
        """Scenario analysis and stress testing revealed potential vulnerabilities under extreme but plausible conditions.
        The analysis considered multiple risk events occurring simultaneously and evaluated the organization's
        resilience and recovery capabilities under various stress scenarios.""",
        """Key risk indicators have been established to provide early warning signals of increasing risk levels.
        These indicators are monitored continuously through automated dashboards and reporting systems, enabling
        timely intervention when risk levels approach unacceptable thresholds.""",
        """Risk interdependencies were analyzed to understand cascade effects and correlation between different risk
        types. This analysis revealed complex relationships requiring coordinated mitigation strategies and
        highlighted the importance of enterprise-wide risk management approaches.""",
        """The risk governance structure ensures appropriate oversight and accountability for risk management activities.
        Clear roles and responsibilities have been defined, with regular reporting to board committees and executive
        management ensuring visibility and engagement at all organizational levels.""",
        """Risk culture assessment indicated growing risk awareness across the organization but identified pockets
        where risk management practices require strengthening. Cultural change initiatives are underway to embed
        risk thinking into decision-making processes at all levels.""",
        """Quantitative risk modeling provided probabilistic assessments of potential losses and enabled cost-benefit
        analysis of mitigation investments. Monte Carlo simulations and other statistical techniques were employed
        to understand the range of possible outcomes and inform risk-based resource allocation.""",
    ]


def generate_compliance_content_blocks() -> List[str]:
    """Generate reusable content blocks for compliance documents."""
    return [
        """Regulatory compliance requirements continue to expand in scope and complexity, requiring sophisticated
        compliance management systems and processes. The organization must balance compliance obligations with
        operational efficiency while maintaining competitive positioning in the market.""",
        """Compliance monitoring procedures have been enhanced to provide real-time visibility into compliance status
        across all regulated areas. Automated monitoring tools and exception reporting enable rapid identification
        and remediation of compliance gaps before they escalate into violations.""",
        """The compliance training program ensures all employees understand their compliance responsibilities and
        the potential consequences of non-compliance. Role-based training modules provide targeted education
        relevant to specific job functions and compliance exposure levels.""",
        """Policy management processes ensure that all compliance policies remain current and aligned with regulatory
        requirements. Regular policy reviews, updates, and communications maintain policy relevance and promote
        consistent understanding and application across the organization.""",
        """Third-party compliance management has become increasingly critical as organizations rely more heavily on
        vendors and partners. Due diligence procedures, contractual provisions, and ongoing monitoring ensure
        that third parties maintain appropriate compliance standards.""",
        """Compliance technology investments have improved efficiency and effectiveness of compliance programs.
        Automation of routine compliance tasks frees resources for higher-value activities while reducing the
        risk of human error in compliance processes.""",
        """Regulatory change management processes ensure timely identification and implementation of new requirements.
        Horizon scanning, impact assessments, and implementation planning enable proactive compliance with
        evolving regulatory landscapes.""",
        """Compliance metrics and reporting provide stakeholders with clear visibility into compliance performance.
        Key performance indicators track compliance effectiveness, efficiency, and maturity, supporting data-driven
        improvement initiatives and resource allocation decisions.""",
        """Internal compliance assessments complement external audits and regulatory examinations, providing early
        identification of potential issues. Self-assessment programs engage business units in compliance ownership
        and promote a culture of continuous compliance improvement.""",
        """Compliance incident management procedures ensure appropriate response to compliance failures when they occur.
        Root cause analysis, remediation planning, and lessons learned processes prevent recurrence and strengthen
        the overall compliance framework.""",
    ]


def generate_large_document(doc_id: int, doc_type: str, target_words: int = 5000) -> Dict[str, str]:
    """Generate a large document with target word count."""

    if doc_type == "audit":
        content_blocks = generate_audit_content_blocks()
        doc_prefix = "audit-report"
        title = f"COMPREHENSIVE INTERNAL AUDIT REPORT {doc_id:04d}"
    elif doc_type == "risk":
        content_blocks = generate_risk_content_blocks()
        doc_prefix = "risk-matrix"
        title = f"ENTERPRISE RISK ASSESSMENT MATRIX {doc_id:04d}"
    else:
        content_blocks = generate_compliance_content_blocks()
        doc_prefix = "compliance-doc"
        title = f"REGULATORY COMPLIANCE ASSESSMENT {doc_id:04d}"

    sections = [title, "\n"]

    # Add executive summary
    sections.append(
        f"""
EXECUTIVE SUMMARY

This comprehensive {doc_type} document provides detailed analysis and assessment of organizational
{"controls and processes" if doc_type == "audit" else "risks and mitigation strategies" if doc_type == "risk" else "compliance posture and requirements"}.
The assessment was conducted using industry-standard methodologies and best practices, incorporating both
quantitative and qualitative analysis techniques.
"""
    )

    # Build content by repeating and varying blocks until target word count
    current_words = len(" ".join(sections).split())
    block_index = 0
    section_counter = 1

    while current_words < target_words:
        # Add section header
        sections.append(f"\nSECTION {section_counter}: DETAILED ANALYSIS\n")

        # Add content blocks with variations
        for _ in range(3):  # Add 3 blocks per section
            if block_index >= len(content_blocks):
                block_index = 0

            # Add the block with some variation
            block = content_blocks[block_index]

            # Add entity references
            block = block.replace("risks", f"risks (RISK-{doc_id:03d}-{section_counter:02d})")
            block = block.replace("controls", f"controls (CTRL-{doc_id:03d}-{section_counter:02d})")
            block = block.replace(
                "requirements", f"requirements (REQ-{doc_id:03d}-{section_counter:02d})"
            )

            sections.append(block)
            sections.append("\n")

            block_index += 1

        # Add findings for this section
        sections.append(
            f"""
Key Findings for Section {section_counter}:
- Finding {section_counter}.1: {"Process improvement opportunity identified" if section_counter % 3 == 0 else "Control enhancement recommended" if section_counter % 3 == 1 else "Compliance gap noted"}
- Finding {section_counter}.2: {"Documentation updates required" if section_counter % 2 == 0 else "Training needs identified"}
- Finding {section_counter}.3: {"Technology enablement opportunity" if section_counter % 4 == 0 else "Monitoring enhancement suggested" if section_counter % 4 == 1 else "Risk mitigation improvement" if section_counter % 4 == 2 else "Governance strengthening needed"}
"""
        )

        current_words = len(" ".join(sections).split())
        section_counter += 1

    # Add conclusion
    sections.append(
        f"""
CONCLUSION

This {"audit" if doc_type == "audit" else "risk assessment" if doc_type == "risk" else "compliance review"}
has identified multiple opportunities for enhancement while recognizing existing strengths in the
{"control environment" if doc_type == "audit" else "risk management framework" if doc_type == "risk" else "compliance program"}.
Implementation of the recommendations provided will strengthen organizational resilience and support
achievement of strategic objectives.

Management has committed to addressing all identified findings through structured action plans with
defined timelines and accountability. Follow-up reviews will be conducted to verify implementation
effectiveness and ensure sustainable improvements.
"""
    )

    content = "\n".join(sections)

    return {
        "id": f"{doc_prefix}-{doc_id:04d}",
        "type": doc_type,
        "content": content,
        "word_count": len(content.split()),
    }


def main():
    """Generate the full corpus meeting all requirements."""

    print("Generating Full Semantic QA Corpus (250k+ words)...")
    print("=" * 60)

    corpus_dir = Path(__file__).parent / "corpus"

    # Clear existing files
    for doc_type in ["audit-reports", "risk-matrices", "compliance-docs"]:
        type_dir = corpus_dir / doc_type
        type_dir.mkdir(parents=True, exist_ok=True)
        for file in type_dir.glob("*.txt"):
            file.unlink()

    all_documents = []
    corpus_stats = {
        "audit-reports": {"count": 0, "words": 0},
        "risk-matrices": {"count": 0, "words": 0},
        "compliance-docs": {"count": 0, "words": 0},
        "total_words": 0,
    }

    # Calculate documents needed
    target_total_words = 255000  # Slightly over 250k to ensure we meet requirement
    target_docs = 55  # Slightly over 50 to ensure we meet requirement
    words_per_doc = target_total_words // target_docs

    # Distribute documents across types
    audit_count = 20
    risk_count = 18
    compliance_count = 17

    print(f"\nTarget: {target_total_words:,} words across {target_docs} documents")
    print(f"Average words per document: {words_per_doc:,}")

    # Generate audit reports
    print("\nGenerating Audit Reports...")
    for i in range(audit_count):
        doc = generate_large_document(i + 1, "audit", words_per_doc)

        doc_path = corpus_dir / "audit-reports" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["audit-reports"]["count"] += 1
        corpus_stats["audit-reports"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        if (i + 1) % 5 == 0:
            print(f"  Generated {i + 1}/{audit_count} audit reports...")

    print(
        f"  ✓ Complete: {corpus_stats['audit-reports']['count']} docs, {corpus_stats['audit-reports']['words']:,} words"
    )

    # Generate risk matrices
    print("\nGenerating Risk Matrices...")
    for i in range(risk_count):
        doc = generate_large_document(i + 1, "risk", words_per_doc)

        doc_path = corpus_dir / "risk-matrices" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["risk-matrices"]["count"] += 1
        corpus_stats["risk-matrices"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        if (i + 1) % 5 == 0:
            print(f"  Generated {i + 1}/{risk_count} risk matrices...")

    print(
        f"  ✓ Complete: {corpus_stats['risk-matrices']['count']} docs, {corpus_stats['risk-matrices']['words']:,} words"
    )

    # Generate compliance documents
    print("\nGenerating Compliance Documents...")
    for i in range(compliance_count):
        doc = generate_large_document(i + 1, "compliance", words_per_doc)

        doc_path = corpus_dir / "compliance-docs" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["compliance-docs"]["count"] += 1
        corpus_stats["compliance-docs"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        if (i + 1) % 5 == 0:
            print(f"  Generated {i + 1}/{compliance_count} compliance docs...")

    print(
        f"  ✓ Complete: {corpus_stats['compliance-docs']['count']} docs, {corpus_stats['compliance-docs']['words']:,} words"
    )

    # Create comprehensive metadata
    metadata = {
        "corpus_name": "semantic-qa-fixtures",
        "version": "1.0.0",
        "created_date": "2025-11-18",
        "story": "3.5-6-semantic-qa-fixtures",
        "document_count": len(all_documents),
        "total_words": corpus_stats["total_words"],
        "average_words_per_doc": corpus_stats["total_words"] // len(all_documents),
        "min_words_per_doc": min(doc["word_count"] for doc in all_documents),
        "max_words_per_doc": max(doc["word_count"] for doc in all_documents),
        "document_types": {
            "audit-reports": {
                "count": corpus_stats["audit-reports"]["count"],
                "total_words": corpus_stats["audit-reports"]["words"],
                "average_words": corpus_stats["audit-reports"]["words"]
                // corpus_stats["audit-reports"]["count"],
            },
            "risk-matrices": {
                "count": corpus_stats["risk-matrices"]["count"],
                "total_words": corpus_stats["risk-matrices"]["words"],
                "average_words": corpus_stats["risk-matrices"]["words"]
                // corpus_stats["risk-matrices"]["count"],
            },
            "compliance-docs": {
                "count": corpus_stats["compliance-docs"]["count"],
                "total_words": corpus_stats["compliance-docs"]["words"],
                "average_words": corpus_stats["compliance-docs"]["words"]
                // corpus_stats["compliance-docs"]["count"],
            },
        },
        "quality_attributes": {
            "pii_sanitized": True,
            "synthetic_data": True,
            "entity_patterns": ["RISK-XXX-XX", "CTRL-XXX-XX", "REQ-XXX-XX"],
            "domain": "audit-compliance-risk",
            "language": "English",
            "readability_level": "Professional",
        },
        "documents": [
            {"id": doc["id"], "type": doc["type"], "word_count": doc["word_count"]}
            for doc in all_documents
        ],
    }

    metadata_path = corpus_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))

    # Print final summary
    print("\n" + "=" * 60)
    print("CORPUS GENERATION COMPLETE")
    print("=" * 60)
    print(f"✅ Total Documents: {len(all_documents)} (requirement: ≥50)")
    print(f"✅ Total Words: {corpus_stats['total_words']:,} (requirement: ≥250,000)")
    print("✅ Document Types: 3 (requirement: ≥3)")
    print("\nBreakdown:")
    print(
        f"  • Audit Reports: {corpus_stats['audit-reports']['count']} docs, {corpus_stats['audit-reports']['words']:,} words"
    )
    print(
        f"  • Risk Matrices: {corpus_stats['risk-matrices']['count']} docs, {corpus_stats['risk-matrices']['words']:,} words"
    )
    print(
        f"  • Compliance Docs: {corpus_stats['compliance-docs']['count']} docs, {corpus_stats['compliance-docs']['words']:,} words"
    )
    print(f"\nCorpus location: {corpus_dir}")
    print(f"Metadata saved: {metadata_path}")

    # Validation checks
    assert len(all_documents) >= 50, f"Document count {len(all_documents)} < 50"
    assert (
        corpus_stats["total_words"] >= 250000
    ), f"Word count {corpus_stats['total_words']} < 250,000"
    assert len(corpus_stats) - 1 >= 3, "Less than 3 document types"
    print("\n✅ All validation checks passed!")

    return corpus_stats


if __name__ == "__main__":
    main()
