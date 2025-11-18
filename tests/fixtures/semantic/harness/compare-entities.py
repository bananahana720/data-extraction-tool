#!/usr/bin/env python
"""
Entity Extraction Comparison Harness

This script compares entity extraction output from the semantic processor
against gold-standard annotations for regression testing.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_gold_standard() -> Dict:
    """Load gold-standard entity annotations."""
    gold_path = Path(__file__).parent.parent / "gold-standard" / "entity_annotations.json"

    if not gold_path.exists():
        raise FileNotFoundError(f"Gold-standard annotations not found: {gold_path}")

    with gold_path.open() as f:
        return json.load(f)


def load_test_document(doc_id: str) -> str:
    """Load a test document by ID."""
    corpus_dir = Path(__file__).parent.parent / "corpus"

    # Try different document type directories
    for doc_type in ["audit-reports", "risk-matrices", "compliance-docs"]:
        doc_path = corpus_dir / doc_type / f"{doc_id}.txt"
        if doc_path.exists():
            return doc_path.read_text()

    raise FileNotFoundError(f"Document not found: {doc_id}")


def extract_entities(text: str) -> List[str]:
    """Extract entity patterns from document text."""
    entities = []

    # Entity patterns to extract (same as gold-standard generator)
    patterns = [
        r"RISK-\d{3}-\d{2}",  # Risk identifiers
        r"CTRL-\d{3}-\d{2}",  # Control identifiers
        r"REQ-\d{3}-\d{3}",  # Requirement identifiers
        r"ACTION-\d{3}-\d{3}",  # Action item identifiers
        r"KRI-\d{3}",  # Key Risk Indicator identifiers
        r"COMP-\d{4}",  # Compliance document references
        r"TECH-CTRL-\d{3}-\d{3}",  # Technical control identifiers
        r"ADMIN-CTRL-\d{3}-\d{3}",  # Administrative control identifiers
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        entities.extend(matches)

    # Remove duplicates while preserving order
    seen = set()
    unique_entities = []
    for entity in entities:
        if entity not in seen:
            seen.add(entity)
            unique_entities.append(entity)

    return unique_entities


def calculate_entity_metrics(
    generated_entities: List[str], gold_entities: List[str], tolerance: float = 0.8
) -> Tuple[float, Dict]:
    """
    Calculate precision, recall, and F1 score for entity extraction.

    Args:
        generated_entities: Entities extracted from test
        gold_entities: Gold-standard entities
        tolerance: Minimum F1 score for success

    Returns:
        Tuple of (F1 score, comparison details)
    """

    # Convert to sets for comparison
    generated_set = set(generated_entities)
    gold_set = set(gold_entities)

    # Calculate metrics
    true_positives = len(generated_set & gold_set)
    false_positives = len(generated_set - gold_set)
    false_negatives = len(gold_set - generated_set)

    # Calculate precision
    if true_positives + false_positives > 0:
        precision = true_positives / (true_positives + false_positives)
    else:
        precision = 0

    # Calculate recall
    if true_positives + false_negatives > 0:
        recall = true_positives / (true_positives + false_negatives)
    else:
        recall = 0

    # Calculate F1 score
    if precision + recall > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0

    # Entity type analysis
    def get_entity_type(entity: str) -> str:
        return entity.split("-")[0]

    generated_types = set(get_entity_type(e) for e in generated_entities)
    gold_types = set(get_entity_type(e) for e in gold_entities)
    type_coverage = len(generated_types & gold_types) / len(gold_types) if gold_types else 0

    details = {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1_score, 3),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "generated_count": len(generated_entities),
        "gold_count": len(gold_entities),
        "type_coverage": round(type_coverage, 3),
        "missing_entities": list(gold_set - generated_set)[:10],  # First 10 missing
        "extra_entities": list(generated_set - gold_set)[:10],  # First 10 extra
        "passes_tolerance": f1_score >= tolerance,
    }

    return f1_score, details


def run_comparison(doc_ids: List[str] = None, tolerance: float = 0.8) -> Dict:
    """
    Run entity extraction comparison for specified documents.

    Args:
        doc_ids: List of document IDs to test (None = all)
        tolerance: Minimum F1 score for success

    Returns:
        Comparison results dictionary
    """

    print("Entity Extraction Comparison Harness")
    print("=" * 60)

    # Load gold-standard
    gold_data = load_gold_standard()
    annotations = gold_data["annotations"]

    if doc_ids is None:
        # Use all documents in gold-standard
        doc_ids = list(annotations.keys())[:10]  # Test first 10 for demo

    results = {
        "total_documents": len(doc_ids),
        "passed": 0,
        "failed": 0,
        "tolerance": tolerance,
        "documents": {},
        "aggregate_metrics": {
            "total_true_positives": 0,
            "total_false_positives": 0,
            "total_false_negatives": 0,
        },
    }

    print(f"\nTesting {len(doc_ids)} documents with {tolerance:.0%} F1 score tolerance...")

    for doc_id in doc_ids:
        if doc_id not in annotations:
            print(f"⚠️  {doc_id}: Not in gold-standard")
            continue

        try:
            # Load document
            doc_content = load_test_document(doc_id)

            # Extract entities
            generated_entities = extract_entities(doc_content)

            # Get gold-standard entities
            gold_annotation = annotations[doc_id]
            gold_entities = gold_annotation["entities"]

            # Calculate metrics
            f1_score, details = calculate_entity_metrics(
                generated_entities, gold_entities, tolerance
            )

            # Record results
            results["documents"][doc_id] = {
                "f1_score": f1_score,
                "details": details,
                "passed": details["passes_tolerance"],
            }

            # Update aggregate metrics
            results["aggregate_metrics"]["total_true_positives"] += details["true_positives"]
            results["aggregate_metrics"]["total_false_positives"] += details["false_positives"]
            results["aggregate_metrics"]["total_false_negatives"] += details["false_negatives"]

            if details["passes_tolerance"]:
                results["passed"] += 1
                status = "✅"
            else:
                results["failed"] += 1
                status = "❌"

            print(
                f"{status} {doc_id}: F1={f1_score:.1%}, P={details['precision']:.1%}, R={details['recall']:.1%}"
            )

        except Exception as e:
            print(f"❌ {doc_id}: Error - {e}")
            results["documents"][doc_id] = {"error": str(e), "passed": False}
            results["failed"] += 1

    # Calculate aggregate metrics
    agg = results["aggregate_metrics"]
    if agg["total_true_positives"] + agg["total_false_positives"] > 0:
        agg_precision = agg["total_true_positives"] / (
            agg["total_true_positives"] + agg["total_false_positives"]
        )
    else:
        agg_precision = 0

    if agg["total_true_positives"] + agg["total_false_negatives"] > 0:
        agg_recall = agg["total_true_positives"] / (
            agg["total_true_positives"] + agg["total_false_negatives"]
        )
    else:
        agg_recall = 0

    if agg_precision + agg_recall > 0:
        agg_f1 = 2 * (agg_precision * agg_recall) / (agg_precision + agg_recall)
    else:
        agg_f1 = 0

    results["aggregate_metrics"]["precision"] = round(agg_precision, 3)
    results["aggregate_metrics"]["recall"] = round(agg_recall, 3)
    results["aggregate_metrics"]["f1_score"] = round(agg_f1, 3)

    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Documents tested: {results['total_documents']}")
    print(f"Passed: {results['passed']} ({results['passed']/results['total_documents']:.1%})")
    print(f"Failed: {results['failed']} ({results['failed']/results['total_documents']:.1%})")
    print(f"Tolerance threshold: F1 ≥ {tolerance:.0%}")
    print("\nAggregate Metrics:")
    print(f"  Overall Precision: {agg_precision:.1%}")
    print(f"  Overall Recall: {agg_recall:.1%}")
    print(f"  Overall F1 Score: {agg_f1:.1%}")

    # Calculate average F1
    if results["documents"]:
        avg_f1 = sum(d.get("f1_score", 0) for d in results["documents"].values()) / len(
            results["documents"]
        )
        results["average_f1_score"] = round(avg_f1, 3)
        print(f"  Average F1 Score: {avg_f1:.1%}")

    success = results["passed"] / results["total_documents"] >= 0.9  # 90% must pass
    if success:
        print("\n✅ Entity extraction comparison PASSED")
    else:
        print("\n❌ Entity extraction comparison FAILED")

    return results


def main():
    """Main entry point for command-line execution."""

    # Parse command-line arguments
    tolerance = 0.8  # Default 80% F1 score
    doc_ids = None  # Test all by default

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python compare-entities.py [tolerance] [doc_ids...]")
            print("  tolerance: Minimum F1 score for success (default: 0.8)")
            print("  doc_ids: Specific document IDs to test (default: all)")
            sys.exit(0)

        try:
            tolerance = float(sys.argv[1])
        except ValueError:
            doc_ids = sys.argv[1:]
        else:
            if len(sys.argv) > 2:
                doc_ids = sys.argv[2:]

    # Run comparison
    results = run_comparison(doc_ids, tolerance)

    # Save results
    results_path = Path(__file__).parent / "entity_comparison_results.json"
    results_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to: {results_path}")

    # Exit with appropriate code
    sys.exit(0 if results["passed"] / results["total_documents"] >= 0.9 else 1)


if __name__ == "__main__":
    main()
