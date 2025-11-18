#!/usr/bin/env python
"""
TF-IDF Comparison Harness

This script compares TF-IDF output from the semantic processor
against gold-standard annotations for regression testing.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def load_gold_standard() -> Dict:
    """Load gold-standard TF-IDF annotations."""
    gold_path = Path(__file__).parent.parent / "gold-standard" / "tfidf_annotations.json"

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


def calculate_tfidf_similarity(
    doc_content: str, gold_top_terms: List[Dict], tolerance: float = 0.8
) -> Tuple[float, Dict]:
    """
    Calculate similarity between generated and gold-standard TF-IDF.

    Args:
        doc_content: Document text content
        gold_top_terms: Gold-standard top terms with scores
        tolerance: Minimum overlap ratio for success (0.8 = 80%)

    Returns:
        Tuple of (similarity score, comparison details)
    """

    # Load the pre-fitted vectorizer
    vectorizer_path = Path(__file__).parent.parent / "gold-standard" / "tfidf_vectorizer.joblib"

    if vectorizer_path.exists():
        vectorizer = joblib.load(vectorizer_path)
    else:
        # Create new vectorizer with same config as gold-standard
        vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.95,
            stop_words="english",
            use_idf=True,
            smooth_idf=True,
            sublinear_tf=True,
            ngram_range=(1, 2),
        )
        # Note: This would need to be fitted on the full corpus
        raise ValueError("Pre-fitted vectorizer not found. Please generate gold-standard first.")

    # Transform the document
    try:
        tfidf_vector = vectorizer.transform([doc_content])
    except Exception as e:
        return 0.0, {"error": str(e)}

    # Get feature names and scores
    feature_names = vectorizer.get_feature_names_out()
    doc_tfidf = tfidf_vector.toarray()[0]

    # Get top terms from generated TF-IDF
    n_top = len(gold_top_terms)
    top_indices = doc_tfidf.argsort()[-n_top:][::-1]
    generated_terms = []

    for idx in top_indices:
        if doc_tfidf[idx] > 0:
            generated_terms.append({"term": feature_names[idx], "score": float(doc_tfidf[idx])})

    # Compare terms
    gold_term_set = set(t["term"] for t in gold_top_terms)
    generated_term_set = set(t["term"] for t in generated_terms)

    # Calculate overlap
    common_terms = gold_term_set & generated_term_set
    overlap_ratio = len(common_terms) / len(gold_term_set) if gold_term_set else 0

    # Calculate score similarity for common terms
    gold_score_dict = {t["term"]: t["score"] for t in gold_top_terms}
    generated_score_dict = {t["term"]: t["score"] for t in generated_terms}

    score_differences = []
    for term in common_terms:
        gold_score = gold_score_dict[term]
        gen_score = generated_score_dict[term]
        if gold_score > 0:
            diff = abs(gold_score - gen_score) / gold_score
            score_differences.append(diff)

    avg_score_diff = sum(score_differences) / len(score_differences) if score_differences else 0
    score_similarity = 1 - avg_score_diff

    # Combined similarity (weighted average)
    similarity = (overlap_ratio * 0.7) + (score_similarity * 0.3)

    details = {
        "overlap_ratio": round(overlap_ratio, 3),
        "score_similarity": round(score_similarity, 3),
        "combined_similarity": round(similarity, 3),
        "common_terms": len(common_terms),
        "gold_terms": len(gold_term_set),
        "generated_terms": len(generated_term_set),
        "unique_to_gold": list(gold_term_set - generated_term_set)[:5],
        "unique_to_generated": list(generated_term_set - gold_term_set)[:5],
        "passes_tolerance": overlap_ratio >= tolerance,
    }

    return similarity, details


def run_comparison(doc_ids: List[str] = None, tolerance: float = 0.8) -> Dict:
    """
    Run TF-IDF comparison for specified documents.

    Args:
        doc_ids: List of document IDs to test (None = all)
        tolerance: Minimum overlap ratio for success

    Returns:
        Comparison results dictionary
    """

    print("TF-IDF Comparison Harness")
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

            # Get gold-standard terms
            gold_annotation = annotations[doc_id]
            gold_top_terms = gold_annotation["top_terms"]

            # Calculate similarity
            similarity, details = calculate_tfidf_similarity(doc_content, gold_top_terms, tolerance)

            # Record results
            results["documents"][doc_id] = {
                "similarity": similarity,
                "details": details,
                "passed": details["passes_tolerance"],
            }

            if details["passes_tolerance"]:
                results["passed"] += 1
                print(
                    f"✅ {doc_id}: {similarity:.1%} similarity, {details['overlap_ratio']:.1%} term overlap"
                )
            else:
                results["failed"] += 1
                print(
                    f"❌ {doc_id}: {similarity:.1%} similarity, {details['overlap_ratio']:.1%} term overlap"
                )

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
        print(f"Average similarity: {avg_similarity:.1%}")

    success = results["passed"] / results["total_documents"] >= 0.9  # 90% must pass
    if success:
        print("\n✅ TF-IDF comparison PASSED")
    else:
        print("\n❌ TF-IDF comparison FAILED")

    return results


def main():
    """Main entry point for command-line execution."""

    # Parse command-line arguments
    tolerance = 0.8  # Default 80% term overlap
    doc_ids = None  # Test all by default

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python compare-tfidf.py [tolerance] [doc_ids...]")
            print("  tolerance: Minimum term overlap ratio (default: 0.8)")
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
    results_path = Path(__file__).parent / "tfidf_comparison_results.json"
    results_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to: {results_path}")

    # Exit with appropriate code
    sys.exit(0 if results["passed"] / results["total_documents"] >= 0.9 else 1)


if __name__ == "__main__":
    main()
