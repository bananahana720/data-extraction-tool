#!/usr/bin/env python
"""
LSA Topic Comparison Harness

This script compares LSA topic assignments from the semantic processor
against gold-standard annotations for regression testing.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import numpy as np


def load_gold_standard() -> Dict:
    """Load gold-standard LSA annotations."""
    gold_path = Path(__file__).parent.parent / "gold-standard" / "lsa_annotations.json"

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


def calculate_lsa_similarity(
    doc_content: str, gold_primary_topic: int, gold_top_topics: List[Dict], tolerance: float = 0.7
) -> Tuple[float, Dict]:
    """
    Calculate similarity between generated and gold-standard LSA topics.

    Args:
        doc_content: Document text content
        gold_primary_topic: Gold-standard primary topic ID
        gold_top_topics: Gold-standard top topics with weights
        tolerance: Minimum similarity for success (0.7 = 70%)

    Returns:
        Tuple of (similarity score, comparison details)
    """

    # Load pre-fitted models
    vectorizer_path = Path(__file__).parent.parent / "gold-standard" / "tfidf_vectorizer.joblib"
    lsa_path = Path(__file__).parent.parent / "gold-standard" / "lsa_model.joblib"

    if not vectorizer_path.exists() or not lsa_path.exists():
        raise ValueError("Pre-fitted models not found. Please generate gold-standard first.")

    vectorizer = joblib.load(vectorizer_path)
    lsa = joblib.load(lsa_path)

    # Transform document through TF-IDF and LSA
    try:
        tfidf_vector = vectorizer.transform([doc_content])
        topic_weights = lsa.transform(tfidf_vector)[0]
    except Exception as e:
        return 0.0, {"error": str(e)}

    # Get generated primary topic
    generated_primary = int(topic_weights.argmax())

    # Get generated top topics
    top_topics_idx = topic_weights.argsort()[-3:][::-1]
    generated_top_topics = [
        {"topic_id": int(idx), "weight": float(topic_weights[idx])} for idx in top_topics_idx
    ]

    # Compare primary topics
    primary_match = generated_primary == gold_primary_topic

    # Compare top topics (check if gold primary is in generated top 3)
    generated_top_ids = [t["topic_id"] for t in generated_top_topics]
    gold_top_ids = [t["topic_id"] for t in gold_top_topics]

    primary_in_top3 = gold_primary_topic in generated_top_ids

    # Calculate topic overlap
    common_topics = set(generated_top_ids) & set(gold_top_ids)
    overlap_ratio = len(common_topics) / len(gold_top_ids) if gold_top_ids else 0

    # Calculate weight similarity using cosine similarity
    # Create weight vectors for all topics
    n_topics = len(topic_weights)
    gold_weights = np.zeros(n_topics)
    for topic in gold_top_topics:
        if topic["topic_id"] < n_topics:
            gold_weights[topic["topic_id"]] = topic["weight"]

    # Normalize weights
    if np.linalg.norm(gold_weights) > 0 and np.linalg.norm(topic_weights) > 0:
        gold_norm = gold_weights / np.linalg.norm(gold_weights)
        gen_norm = topic_weights / np.linalg.norm(topic_weights)
        cosine_sim = np.dot(gold_norm, gen_norm)
    else:
        cosine_sim = 0

    # Combined similarity score
    similarity = (
        (1.0 if primary_match else 0.5 if primary_in_top3 else 0.0) * 0.4
        + overlap_ratio * 0.3
        + max(0, cosine_sim) * 0.3
    )

    details = {
        "primary_match": primary_match,
        "primary_in_top3": primary_in_top3,
        "overlap_ratio": round(overlap_ratio, 3),
        "cosine_similarity": round(float(cosine_sim), 3),
        "combined_similarity": round(similarity, 3),
        "gold_primary": gold_primary_topic,
        "generated_primary": generated_primary,
        "common_topics": len(common_topics),
        "passes_tolerance": similarity >= tolerance,
    }

    return similarity, details


def run_comparison(doc_ids: List[str] = None, tolerance: float = 0.7) -> Dict:
    """
    Run LSA comparison for specified documents.

    Args:
        doc_ids: List of document IDs to test (None = all)
        tolerance: Minimum similarity for success

    Returns:
        Comparison results dictionary
    """

    print("LSA Topic Comparison Harness")
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
    }

    print(f"\nTesting {len(doc_ids)} documents with {tolerance:.0%} tolerance...")

    for doc_id in doc_ids:
        if doc_id not in annotations:
            print(f"⚠️  {doc_id}: Not in gold-standard")
            continue

        try:
            # Load document
            doc_content = load_test_document(doc_id)

            # Get gold-standard topics
            gold_annotation = annotations[doc_id]
            gold_primary = gold_annotation["primary_topic"]
            gold_top_topics = gold_annotation["top_topics"]

            # Calculate similarity
            similarity, details = calculate_lsa_similarity(
                doc_content, gold_primary, gold_top_topics, tolerance
            )

            # Record results
            results["documents"][doc_id] = {
                "similarity": similarity,
                "details": details,
                "passed": details["passes_tolerance"],
            }

            if details["passes_tolerance"]:
                results["passed"] += 1
                status = "✅"
            else:
                results["failed"] += 1
                status = "❌"

            primary_status = "✓" if details["primary_match"] else "✗"
            print(f"{status} {doc_id}: {similarity:.1%} similarity, Primary topic {primary_status}")

        except Exception as e:
            print(f"❌ {doc_id}: Error - {e}")
            results["documents"][doc_id] = {"error": str(e), "passed": False}
            results["failed"] += 1

    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Documents tested: {results['total_documents']}")
    print(f"Passed: {results['passed']} ({results['passed']/results['total_documents']:.1%})")
    print(f"Failed: {results['failed']} ({results['failed']/results['total_documents']:.1%})")
    print(f"Tolerance threshold: {tolerance:.0%}")

    # Calculate average metrics
    if results["documents"]:
        avg_similarity = sum(d.get("similarity", 0) for d in results["documents"].values()) / len(
            results["documents"]
        )
        results["average_similarity"] = round(avg_similarity, 3)

        primary_matches = sum(
            1
            for d in results["documents"].values()
            if d.get("details", {}).get("primary_match", False)
        )
        primary_match_rate = primary_matches / len(results["documents"])
        results["primary_match_rate"] = round(primary_match_rate, 3)

        print(f"Average similarity: {avg_similarity:.1%}")
        print(f"Primary topic match rate: {primary_match_rate:.1%}")

    success = results["passed"] / results["total_documents"] >= 0.9  # 90% must pass
    if success:
        print("\n✅ LSA comparison PASSED")
    else:
        print("\n❌ LSA comparison FAILED")

    return results


def main():
    """Main entry point for command-line execution."""

    # Parse command-line arguments
    tolerance = 0.7  # Default 70% similarity
    doc_ids = None  # Test all by default

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python compare-lsa.py [tolerance] [doc_ids...]")
            print("  tolerance: Minimum similarity score (default: 0.7)")
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
    results_path = Path(__file__).parent / "lsa_comparison_results.json"
    results_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to: {results_path}")

    # Exit with appropriate code
    sys.exit(0 if results["passed"] / results["total_documents"] >= 0.9 else 1)


if __name__ == "__main__":
    main()
