#!/usr/bin/env python
"""
Generate Synthetic Audit-Domain Corpus for Semantic QA Testing

This script generates a corpus of 50+ synthetic audit-domain documents
covering audit reports, risk matrices, and compliance documentation.
All documents are PII-free and designed to reflect production characteristics.

Story: 3.5-6-semantic-qa-fixtures
"""

import json
import random
from pathlib import Path
from typing import Dict

# Seed for reproducibility
random.seed(42)


def generate_audit_report(doc_id: int) -> Dict[str, str]:
    """Generate a synthetic audit report document."""

    # Audit report templates with realistic content
    sections = []

    # Executive Summary
    sections.append(
        f"""
INTERNAL AUDIT REPORT {doc_id:04d}
Audit Period: FY2024 Q{(doc_id % 4) + 1}
Audit Type: {"Operational" if doc_id % 3 == 0 else "Compliance" if doc_id % 3 == 1 else "Financial"}

EXECUTIVE SUMMARY

This internal audit was conducted to evaluate the effectiveness of {"operational controls" if doc_id % 3 == 0 else "compliance frameworks" if doc_id % 3 == 1 else "financial reporting processes"}
within the organization. The audit encompassed a comprehensive review of {"process efficiency and resource utilization" if doc_id % 3 == 0 else "regulatory adherence and policy compliance" if doc_id % 3 == 1 else "accounting practices and internal controls"}.
Our assessment identified {"several opportunities for process improvement" if doc_id % 2 == 0 else "strong control environments with minor enhancement areas"}.

The audit team performed {"detailed walkthroughs" if doc_id % 2 == 0 else "extensive testing"} of key control activities,
examining {"operational workflows" if doc_id % 3 == 0 else "compliance documentation" if doc_id % 3 == 1 else "financial transactions"} across multiple business units.
Risk assessment procedures were applied to identify areas of {"high operational risk" if doc_id % 3 == 0 else "compliance exposure" if doc_id % 3 == 1 else "financial vulnerability"}.
"""
    )

    # Scope and Objectives
    sections.append(
        f"""
AUDIT SCOPE AND OBJECTIVES

The primary objectives of this audit engagement included:

1. Evaluate the design and operating effectiveness of {"business processes" if doc_id % 3 == 0 else "compliance controls" if doc_id % 3 == 1 else "financial controls"}
2. Assess compliance with {"operational policies and procedures" if doc_id % 3 == 0 else "regulatory requirements and standards" if doc_id % 3 == 1 else "accounting principles and guidelines"}
3. Identify opportunities for {"process optimization" if doc_id % 3 == 0 else "compliance enhancement" if doc_id % 3 == 1 else "financial reporting improvement"}
4. Review the adequacy of {"resource allocation" if doc_id % 3 == 0 else "compliance monitoring" if doc_id % 3 == 1 else "financial oversight mechanisms"}

The audit scope encompassed the period from {"January 2024" if doc_id % 2 == 0 else "July 2023"} through {"June 2024" if doc_id % 2 == 0 else "December 2023"},
focusing on {"core operational activities" if doc_id % 3 == 0 else "regulatory compliance areas" if doc_id % 3 == 1 else "material financial transactions"}.
"""
    )

    # Risk Assessment
    risk_levels = ["HIGH", "MEDIUM", "LOW"]
    risk_areas = [
        "Data integrity and accuracy",
        "Process documentation completeness",
        "Control design effectiveness",
        "Monitoring and oversight activities",
        "Change management procedures",
        "Access control mechanisms",
        "Segregation of duties",
        "Exception handling processes",
    ]

    sections.append(
        f"""
RISK ASSESSMENT

Our risk assessment identified the following key risk areas:

RISK-{doc_id:03d}-001: {random.choice(risk_areas)}
Risk Level: {random.choice(risk_levels)}
Impact: {"Potential for operational disruption" if doc_id % 3 == 0 else "Regulatory non-compliance exposure" if doc_id % 3 == 1 else "Financial misstatement risk"}

RISK-{doc_id:03d}-002: {random.choice(risk_areas)}
Risk Level: {random.choice(risk_levels)}
Impact: {"Process inefficiency and resource waste" if doc_id % 3 == 0 else "Policy violation potential" if doc_id % 3 == 1 else "Internal control weakness"}

The risk assessment methodology incorporated both quantitative and qualitative factors,
including {"process complexity analysis" if doc_id % 3 == 0 else "regulatory requirement mapping" if doc_id % 3 == 1 else "transaction volume analysis"}
and {"stakeholder impact assessment" if doc_id % 2 == 0 else "historical incident review"}.
"""
    )

    # Control Testing Results
    sections.append(
        f"""
CONTROL TESTING RESULTS

Control testing was performed on {"key operational controls" if doc_id % 3 == 0 else "compliance controls" if doc_id % 3 == 1 else "financial controls"}
using a combination of inquiry, observation, inspection, and reperformance procedures.

CTRL-{doc_id:03d}-001: {"Automated Process Control" if doc_id % 2 == 0 else "Manual Review Control"}
Test Result: {"Operating Effectively" if doc_id % 4 < 3 else "Requires Improvement"}
Sample Size: {random.randint(25, 50)} transactions
Exception Rate: {random.randint(0, 5)}%

CTRL-{doc_id:03d}-002: {"Approval Authority Matrix" if doc_id % 2 == 0 else "Reconciliation Process"}
Test Result: {"Operating Effectively" if doc_id % 3 < 2 else "Design Enhancement Needed"}
Sample Size: {random.randint(30, 60)} transactions
Exception Rate: {random.randint(0, 8)}%

CTRL-{doc_id:03d}-003: {"System Access Controls" if doc_id % 2 == 0 else "Documentation Standards"}
Test Result: {"Operating Effectively" if doc_id % 5 < 4 else "Implementation Gaps Noted"}
Sample Size: {random.randint(20, 40)} samples
Exception Rate: {random.randint(0, 10)}%
"""
    )

    # Findings and Recommendations
    sections.append(
        f"""
FINDINGS AND RECOMMENDATIONS

Based on our audit procedures, we identified the following findings requiring management attention:

Finding 1: {"Process Documentation Gaps" if doc_id % 3 == 0 else "Compliance Monitoring Weaknesses" if doc_id % 3 == 1 else "Reconciliation Delays"}
Severity: {random.choice(["HIGH", "MEDIUM", "LOW"])}
Recommendation: Implement {"comprehensive process documentation standards" if doc_id % 3 == 0 else "enhanced compliance monitoring procedures" if doc_id % 3 == 1 else "timely reconciliation protocols"}
Management Response: Agreed. Implementation target: Q{((doc_id % 4) + 2) % 4 + 1} 2024

Finding 2: {"Control Design Inefficiencies" if doc_id % 3 == 0 else "Policy Update Requirements" if doc_id % 3 == 1 else "Approval Threshold Reviews"}
Severity: {random.choice(["MEDIUM", "LOW"])}
Recommendation: {"Redesign control activities for efficiency" if doc_id % 3 == 0 else "Update policies to reflect current regulations" if doc_id % 3 == 1 else "Review and update approval thresholds"}
Management Response: Agreed. Review scheduled for next quarter

Finding 3: {"Training and Awareness Gaps" if doc_id % 2 == 0 else "Monitoring Coverage Limitations"}
Severity: LOW
Recommendation: {"Develop targeted training programs" if doc_id % 2 == 0 else "Expand monitoring coverage scope"}
Management Response: Under consideration
"""
    )

    # Conclusion
    sections.append(
        f"""
CONCLUSION

The audit engagement successfully evaluated {"operational control effectiveness" if doc_id % 3 == 0 else "compliance framework adequacy" if doc_id % 3 == 1 else "financial control reliability"}.
While the overall control environment is {"generally effective" if doc_id % 2 == 0 else "adequate with improvement opportunities"},
the findings identified provide opportunities for {"process enhancement" if doc_id % 3 == 0 else "compliance strengthening" if doc_id % 3 == 1 else "control optimization"}.

Management has demonstrated commitment to addressing the identified findings through {"action plan development" if doc_id % 2 == 0 else "resource allocation"}
and {"timeline establishment" if doc_id % 2 == 0 else "accountability assignment"}. Follow-up procedures will be conducted in {"six months" if doc_id % 2 == 0 else "the next audit cycle"}
to verify implementation effectiveness.

The audit team acknowledges the cooperation and support provided by {"operational management" if doc_id % 3 == 0 else "compliance officers" if doc_id % 3 == 1 else "finance personnel"}
throughout the engagement. Their participation was instrumental in achieving audit objectives and identifying improvement opportunities.
"""
    )

    return {
        "id": f"audit-report-{doc_id:04d}",
        "type": "audit-report",
        "content": "\n".join(sections),
    }


def generate_risk_matrix(doc_id: int) -> Dict[str, str]:
    """Generate a synthetic risk assessment matrix document."""

    sections = []

    # Header
    sections.append(
        f"""
ENTERPRISE RISK ASSESSMENT MATRIX
Document ID: RISK-MATRIX-{doc_id:04d}
Assessment Period: {"H1" if doc_id % 2 == 0 else "H2"} 2024
Department: {"Operations" if doc_id % 4 == 0 else "Finance" if doc_id % 4 == 1 else "Compliance" if doc_id % 4 == 2 else "Technology"}

RISK ASSESSMENT FRAMEWORK

This risk assessment matrix evaluates potential threats to organizational objectives using a structured methodology
incorporating likelihood and impact measurements. Risk ratings are calculated using a {"5x5 matrix" if doc_id % 2 == 0 else "3x3 matrix"}
with {"quantitative scoring" if doc_id % 2 == 0 else "qualitative assessment"} criteria.
"""
    )

    # Risk Categories
    risk_categories = [
        "Strategic Risk",
        "Operational Risk",
        "Financial Risk",
        "Compliance Risk",
        "Technology Risk",
        "Reputational Risk",
        "Market Risk",
        "Credit Risk",
    ]

    for i, category in enumerate(risk_categories[: 5 + (doc_id % 3)]):
        likelihood = random.choice(["Very Low", "Low", "Medium", "High", "Very High"])
        impact = random.choice(["Negligible", "Minor", "Moderate", "Major", "Severe"])

        sections.append(
            f"""
RISK CATEGORY: {category}

RISK-{doc_id:03d}-{i+1:02d}: {category} - {"Process Failure" if i % 3 == 0 else "Control Weakness" if i % 3 == 1 else "External Threat"}
Description: Potential for {"operational disruption" if i % 3 == 0 else "control bypass" if i % 3 == 1 else "external impact"}
affecting {"business continuity" if i % 2 == 0 else "organizational objectives"}

Likelihood Assessment: {likelihood}
Impact Assessment: {impact}
Inherent Risk Score: {random.randint(1, 25)}
Residual Risk Score: {random.randint(1, 15)}

Current Controls:
- CTRL-{doc_id:03d}-{i+1:02d}A: {"Preventive control" if i % 2 == 0 else "Detective control"} - {"automated monitoring" if i % 2 == 0 else "manual review"}
- CTRL-{doc_id:03d}-{i+1:02d}B: {"Compensating control" if i % 2 == 0 else "Corrective control"} - {"alternative procedure" if i % 2 == 0 else "remediation process"}

Mitigation Strategy:
{"Implement additional preventive controls" if likelihood in ["High", "Very High"] else "Enhance monitoring procedures" if likelihood == "Medium" else "Accept risk with periodic review"}

Risk Owner: {"Chief Operating Officer" if i % 4 == 0 else "Chief Financial Officer" if i % 4 == 1 else "Chief Compliance Officer" if i % 4 == 2 else "Chief Information Officer"}
Review Frequency: {"Quarterly" if likelihood in ["High", "Very High"] else "Semi-annually" if likelihood == "Medium" else "Annually"}
"""
        )

    # Risk Heat Map Summary
    sections.append(
        f"""
RISK HEAT MAP SUMMARY

Critical Risks (Immediate Action Required): {random.randint(0, 3)}
High Risks (Management Attention): {random.randint(2, 5)}
Medium Risks (Monitor and Review): {random.randint(3, 7)}
Low Risks (Routine Monitoring): {random.randint(5, 10)}

TREND ANALYSIS

Compared to previous assessment period:
- Increasing Risk Trends: {"Cybersecurity threats" if doc_id % 3 == 0 else "Regulatory changes" if doc_id % 3 == 1 else "Market volatility"}
- Decreasing Risk Trends: {"Operational inefficiencies" if doc_id % 3 == 0 else "Compliance gaps" if doc_id % 3 == 1 else "Technology obsolescence"}
- Stable Risk Areas: {"Financial reporting" if doc_id % 2 == 0 else "Internal controls"}

KEY RISK INDICATORS (KRIs)

KRI-001: {"System downtime hours" if doc_id % 4 == 0 else "Policy violations count" if doc_id % 4 == 1 else "Audit findings count" if doc_id % 4 == 2 else "Security incidents"}
Current Value: {random.randint(1, 50)}
Threshold: {random.randint(20, 75)}
Status: {"Within tolerance" if random.random() > 0.3 else "Exceeds threshold"}

KRI-002: {"Process exception rate" if doc_id % 4 == 0 else "Financial variance percentage" if doc_id % 4 == 1 else "Compliance score" if doc_id % 4 == 2 else "Patch compliance rate"}
Current Value: {random.randint(1, 100)}%
Threshold: {random.randint(5, 15)}%
Status: {"Acceptable" if random.random() > 0.4 else "Requires attention"}
"""
    )

    return {
        "id": f"risk-matrix-{doc_id:04d}",
        "type": "risk-matrix",
        "content": "\n".join(sections),
    }


def generate_compliance_doc(doc_id: int) -> Dict[str, str]:
    """Generate a synthetic compliance document."""

    sections = []

    # Header
    regulations = ["SOX", "GDPR", "HIPAA", "PCI-DSS", "ISO-27001", "SOC-2", "NIST", "COBIT"]
    primary_reg = regulations[doc_id % len(regulations)]

    sections.append(
        f"""
COMPLIANCE ASSESSMENT DOCUMENT
Reference: COMP-{doc_id:04d}
Regulatory Framework: {primary_reg}
Assessment Date: {"Q1" if doc_id % 4 == 0 else "Q2" if doc_id % 4 == 1 else "Q3" if doc_id % 4 == 2 else "Q4"} 2024
Compliance Officer: Compliance Team Lead

REGULATORY COMPLIANCE OVERVIEW

This compliance assessment evaluates organizational adherence to {primary_reg} requirements and related regulatory obligations.
The assessment encompasses {"technical controls" if doc_id % 3 == 0 else "administrative safeguards" if doc_id % 3 == 1 else "physical security measures"}
implemented to ensure regulatory compliance and {"data protection" if primary_reg in ["GDPR", "HIPAA"] else "financial integrity" if primary_reg == "SOX" else "security standards"}.
"""
    )

    # Compliance Requirements
    sections.append(
        f"""
COMPLIANCE REQUIREMENTS ASSESSMENT

Requirement Category: {"Data Privacy" if primary_reg in ["GDPR", "HIPAA"] else "Financial Controls" if primary_reg == "SOX" else "Security Controls"}

REQ-{doc_id:03d}-001: {"Access Control Management" if doc_id % 3 == 0 else "Data Classification" if doc_id % 3 == 1 else "Incident Response"}
Compliance Status: {"Fully Compliant" if doc_id % 4 < 3 else "Partially Compliant" if doc_id % 4 == 3 else "Non-Compliant"}
Evidence: {"Policy documentation reviewed" if doc_id % 2 == 0 else "Control testing completed"}
Gap Analysis: {"No gaps identified" if doc_id % 4 < 3 else "Minor gaps in documentation" if doc_id % 4 == 3 else "Implementation gaps noted"}

REQ-{doc_id:03d}-002: {"Encryption Standards" if doc_id % 3 == 0 else "Retention Policies" if doc_id % 3 == 1 else "Audit Logging"}
Compliance Status: {"Fully Compliant" if doc_id % 3 < 2 else "Partially Compliant"}
Evidence: {"Technical implementation verified" if doc_id % 2 == 0 else "Process documentation confirmed"}
Gap Analysis: {"Standards exceeded" if doc_id % 3 == 0 else "Meets minimum requirements" if doc_id % 3 == 1 else "Enhancement opportunities identified"}

REQ-{doc_id:03d}-003: {"Privacy Notice Requirements" if primary_reg == "GDPR" else "Internal Control Testing" if primary_reg == "SOX" else "Security Assessment"}
Compliance Status: {"Fully Compliant" if doc_id % 5 < 4 else "Requires Update"}
Evidence: {"Documentation review completed" if doc_id % 2 == 0 else "Testing procedures executed"}
Gap Analysis: {"Current and complete" if doc_id % 5 < 4 else "Updates required for new regulations"}
"""
    )

    # Control Implementation
    sections.append(
        f"""
CONTROL IMPLEMENTATION STATUS

Technical Controls:
- TECH-CTRL-{doc_id:03d}-001: {"Firewall Configuration" if doc_id % 4 == 0 else "Encryption Protocols" if doc_id % 4 == 1 else "Access Management System" if doc_id % 4 == 2 else "Monitoring Tools"}
  Status: {"Implemented and Operating" if doc_id % 3 < 2 else "Implementation in Progress"}
  Effectiveness: {random.randint(75, 100)}%

- TECH-CTRL-{doc_id:03d}-002: {"Intrusion Detection System" if doc_id % 4 == 0 else "Data Loss Prevention" if doc_id % 4 == 1 else "Identity Management" if doc_id % 4 == 2 else "Vulnerability Scanning"}
  Status: {"Fully Operational" if doc_id % 2 == 0 else "Partially Deployed"}
  Effectiveness: {random.randint(70, 95)}%

Administrative Controls:
- ADMIN-CTRL-{doc_id:03d}-001: {"Security Awareness Training" if doc_id % 3 == 0 else "Policy Management" if doc_id % 3 == 1 else "Risk Assessment Process"}
  Status: {"Current" if doc_id % 2 == 0 else "Requires Update"}
  Completion Rate: {random.randint(80, 100)}%

- ADMIN-CTRL-{doc_id:03d}-002: {"Incident Response Plan" if doc_id % 3 == 0 else "Business Continuity Plan" if doc_id % 3 == 1 else "Vendor Management"}
  Status: {"Documented and Tested" if doc_id % 4 < 3 else "Documentation Only"}
  Last Review: {"Within 6 months" if doc_id % 2 == 0 else "Within 12 months"}
"""
    )

    # Compliance Metrics
    sections.append(
        f"""
COMPLIANCE METRICS AND INDICATORS

Overall Compliance Score: {random.randint(75, 98)}%
Critical Requirements Met: {random.randint(90, 100)}%
Non-Critical Requirements Met: {random.randint(70, 95)}%

Key Performance Indicators:
- Policy Compliance Rate: {random.randint(85, 100)}%
- Training Completion Rate: {random.randint(80, 100)}%
- Audit Finding Resolution Rate: {random.randint(75, 95)}%
- Control Testing Pass Rate: {random.randint(80, 98)}%

Compliance Trends:
- {"Improving trend over last 4 quarters" if doc_id % 3 < 2 else "Stable compliance levels maintained" if doc_id % 3 == 2 else "Minor decline requiring attention"}
- {"No critical violations identified" if doc_id % 4 < 3 else "Critical violations remediated"}
- {"Regular updates to control framework" if doc_id % 2 == 0 else "Periodic control reviews conducted"}
"""
    )

    # Action Items
    sections.append(
        f"""
COMPLIANCE ACTION PLAN

Priority 1 (Critical):
- ACTION-{doc_id:03d}-001: {"Implement missing critical controls" if doc_id % 5 == 4 else "Update critical documentation" if doc_id % 5 == 3 else "No critical actions required"}
  Due Date: {"Within 30 days" if doc_id % 5 >= 3 else "N/A"}
  Responsible: {"Compliance Officer" if doc_id % 2 == 0 else "Security Team"}

Priority 2 (High):
- ACTION-{doc_id:03d}-002: {"Enhance monitoring capabilities" if doc_id % 3 == 0 else "Update training materials" if doc_id % 3 == 1 else "Review access controls"}
  Due Date: {"Within 60 days" if doc_id % 2 == 0 else "Within 90 days"}
  Responsible: {"IT Security" if doc_id % 3 == 0 else "HR Department" if doc_id % 3 == 1 else "Operations"}

Priority 3 (Medium):
- ACTION-{doc_id:03d}-003: {"Document process improvements" if doc_id % 2 == 0 else "Conduct additional testing"}
  Due Date: {"Next quarter" if doc_id % 2 == 0 else "Within 6 months"}
  Responsible: {"Process Owners" if doc_id % 2 == 0 else "Internal Audit"}

COMPLIANCE CERTIFICATION

Based on the assessment conducted, the organization {"maintains substantial compliance" if doc_id % 4 < 3 else "is working toward full compliance"}
with {primary_reg} requirements. {"All critical requirements are satisfied" if doc_id % 4 < 2 else "Action plans are in place for identified gaps"}.

Next Assessment Schedule: {"3 months" if doc_id % 4 >= 3 else "6 months" if doc_id % 3 == 2 else "12 months"}
Continuous Monitoring: {"Enabled" if doc_id % 2 == 0 else "Scheduled"}
"""
    )

    return {
        "id": f"compliance-doc-{doc_id:04d}",
        "type": "compliance-doc",
        "content": "\n".join(sections),
    }


def calculate_word_count(text: str) -> int:
    """Calculate word count for a document."""
    return len(text.split())


def main():
    """Generate the complete semantic QA corpus."""

    print("Generating Semantic QA Fixtures Corpus...")
    print("=" * 60)

    corpus_dir = Path(__file__).parent

    # Generate documents
    all_documents = []
    corpus_stats = {
        "audit-reports": {"count": 0, "words": 0},
        "risk-matrices": {"count": 0, "words": 0},
        "compliance-docs": {"count": 0, "words": 0},
        "total_words": 0,
    }

    # Generate 20 audit reports
    print("\nGenerating Audit Reports...")
    for i in range(20):
        doc = generate_audit_report(i + 1)
        doc["word_count"] = calculate_word_count(doc["content"])

        # Save document
        doc_path = corpus_dir / "corpus" / "audit-reports" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["audit-reports"]["count"] += 1
        corpus_stats["audit-reports"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        print(f"  Created {doc['id']}: {doc['word_count']} words")

    # Generate 17 risk matrices
    print("\nGenerating Risk Matrices...")
    for i in range(17):
        doc = generate_risk_matrix(i + 1)
        doc["word_count"] = calculate_word_count(doc["content"])

        # Save document
        doc_path = corpus_dir / "corpus" / "risk-matrices" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["risk-matrices"]["count"] += 1
        corpus_stats["risk-matrices"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        print(f"  Created {doc['id']}: {doc['word_count']} words")

    # Generate 18 compliance documents
    print("\nGenerating Compliance Documents...")
    for i in range(18):
        doc = generate_compliance_doc(i + 1)
        doc["word_count"] = calculate_word_count(doc["content"])

        # Save document
        doc_path = corpus_dir / "corpus" / "compliance-docs" / f"{doc['id']}.txt"
        doc_path.write_text(doc["content"])

        all_documents.append(doc)
        corpus_stats["compliance-docs"]["count"] += 1
        corpus_stats["compliance-docs"]["words"] += doc["word_count"]
        corpus_stats["total_words"] += doc["word_count"]

        print(f"  Created {doc['id']}: {doc['word_count']} words")

    # Create metadata file
    metadata = {
        "corpus_name": "semantic-qa-fixtures",
        "created_date": "2025-11-18",
        "story": "3.5-6-semantic-qa-fixtures",
        "document_count": len(all_documents),
        "total_words": corpus_stats["total_words"],
        "document_types": {
            "audit-reports": corpus_stats["audit-reports"],
            "risk-matrices": corpus_stats["risk-matrices"],
            "compliance-docs": corpus_stats["compliance-docs"],
        },
        "documents": [
            {"id": doc["id"], "type": doc["type"], "word_count": doc["word_count"]}
            for doc in all_documents
        ],
    }

    # Save metadata
    metadata_path = corpus_dir / "corpus" / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))

    # Print summary
    print("\n" + "=" * 60)
    print("CORPUS GENERATION COMPLETE")
    print("=" * 60)
    print(f"Total Documents: {len(all_documents)}")
    print(f"Total Words: {corpus_stats['total_words']:,}")
    print("\nDocument Types:")
    print(
        f"  - Audit Reports: {corpus_stats['audit-reports']['count']} docs, {corpus_stats['audit-reports']['words']:,} words"
    )
    print(
        f"  - Risk Matrices: {corpus_stats['risk-matrices']['count']} docs, {corpus_stats['risk-matrices']['words']:,} words"
    )
    print(
        f"  - Compliance Docs: {corpus_stats['compliance-docs']['count']} docs, {corpus_stats['compliance-docs']['words']:,} words"
    )
    print(f"\nMetadata saved to: {metadata_path}")

    return corpus_stats


if __name__ == "__main__":
    main()
