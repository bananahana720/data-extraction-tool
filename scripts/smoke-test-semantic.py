#!/usr/bin/env python3
"""
Smoke test script for semantic analysis dependencies.

Validates scikit-learn, joblib, and textstat are properly installed and performant.
All tests must pass for Epic 4 readiness.

Exit codes:
    0: All tests pass
    1: Any test fails
"""

import sys
import time
from typing import List, Tuple

# Test dependency imports
try:
    import joblib  # type: ignore[import-untyped]
    import numpy as np  # type: ignore[import-untyped]
    import textstat  # type: ignore[import-untyped]
    from sklearn.decomposition import TruncatedSVD  # type: ignore[import-untyped]
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore[import-untyped]
    from sklearn.metrics.pairwise import cosine_similarity  # type: ignore[import-untyped]
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Please run: pip install -e '.[dev]'")
    sys.exit(1)


def generate_test_corpus() -> List[str]:
    """Generate a test corpus of 10 documents, each ~1000 words."""
    # Realistic enterprise document text samples
    base_text = """
    The quarterly audit report presents a comprehensive analysis of financial
    statements and internal control systems. Our examination included reviewing
    supporting documentation, assessing accounting principles used, and evaluating
    overall financial statement presentation. Management is responsible for
    maintaining effective internal control over financial reporting. We conducted
    our audit in accordance with generally accepted auditing standards. These
    standards require that we plan and perform the audit to obtain reasonable
    assurance about whether the financial statements are free of material
    misstatement. The company's internal control framework includes policies
    and procedures that pertain to maintenance of records, provide reasonable
    assurance that transactions are recorded as necessary, and that receipts
    and expenditures are being made only in accordance with authorizations
    of management and directors. Our audit procedures included tests of
    documentary evidence supporting the transactions recorded in the accounts,
    tests of physical existence of inventories, and direct confirmation of
    receivables and certain other assets and liabilities by correspondence
    with selected customers, creditors, and financial institutions.
    """

    # Create 10 variations to simulate different documents
    variations = [
        "risk assessment and mitigation strategies for operational efficiency",
        "compliance validation and regulatory framework adherence monitoring",
        "data governance protocols and information security measures",
        "performance metrics evaluation and key indicator analysis",
        "stakeholder engagement processes and communication protocols",
        "quality assurance methodologies and continuous improvement",
        "technology infrastructure assessment and system integration",
        "business continuity planning and disaster recovery procedures",
        "vendor management oversight and third-party risk evaluation",
        "strategic planning alignment and organizational objectives",
    ]

    corpus = []
    for i, variation in enumerate(variations):
        # Expand base text to ~1000 words per document
        doc = f"{base_text} " * 6  # ~150 words * 6 = ~900 words
        doc += f" This document specifically addresses {variation}. "
        doc += f"Document ID: DOC-{i+1:03d}. " * 20  # Add some padding
        corpus.append(doc)

    return corpus


def test_tfidf_vectorization() -> Tuple[bool, str, float]:
    """Test 1: TF-IDF vectorization with performance baseline."""
    print("\nTest 1: TF-IDF Vectorization")
    print("-" * 40)

    try:
        corpus = generate_test_corpus()

        # Configure TF-IDF with production settings
        vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            lowercase=True,
            stop_words="english",
        )

        # Measure fit/transform time
        start_time = time.time()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        duration_ms = (time.time() - start_time) * 1000

        # Validate output
        n_docs, n_features = tfidf_matrix.shape

        print(f"  Corpus size: {len(corpus)} documents")
        print(f"  Features extracted: {n_features}")
        print(f"  Matrix shape: {tfidf_matrix.shape}")
        print(f"  Matrix density: {tfidf_matrix.nnz / (n_docs * n_features):.2%}")
        print(f"  Fit/transform time: {duration_ms:.1f}ms")

        # Performance baseline: <100ms for 10 docs × 1k words
        if duration_ms >= 100:
            return False, f"Performance failed: {duration_ms:.1f}ms >= 100ms", duration_ms

        if n_docs != len(corpus):
            return False, f"Document count mismatch: {n_docs} != {len(corpus)}", duration_ms

        if n_features == 0:
            return False, "No features extracted", duration_ms

        print(f"✓ TF-IDF vectorization successful ({duration_ms:.1f}ms < 100ms)")
        return True, "Success", duration_ms

    except Exception as e:
        error_msg = f"TF-IDF test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def test_lsa_decomposition() -> Tuple[bool, str, float]:
    """Test 2: LSA (TruncatedSVD) dimensionality reduction."""
    print("\nTest 2: LSA Dimensionality Reduction")
    print("-" * 40)

    try:
        # Generate TF-IDF matrix first
        corpus = generate_test_corpus()
        vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Apply LSA
        n_components = min(100, tfidf_matrix.shape[0] - 1)  # Cannot exceed n_samples - 1
        lsa = TruncatedSVD(n_components=n_components, random_state=42)

        start_time = time.time()
        lsa_matrix = lsa.fit_transform(tfidf_matrix)
        duration_ms = (time.time() - start_time) * 1000

        # Validate output
        explained_variance = lsa.explained_variance_ratio_.sum()

        print(f"  Input shape: {tfidf_matrix.shape}")
        print(f"  Output shape: {lsa_matrix.shape}")
        print(f"  Components: {n_components}")
        print(f"  Explained variance: {explained_variance:.2%}")
        print(f"  LSA transform time: {duration_ms:.1f}ms")

        if lsa_matrix.shape != (len(corpus), n_components):
            return False, f"Shape mismatch: {lsa_matrix.shape}", duration_ms

        if explained_variance < 0.1:  # Should explain at least 10% variance
            return False, f"Low variance: {explained_variance:.2%}", duration_ms

        print("✓ LSA decomposition successful")
        return True, "Success", duration_ms

    except Exception as e:
        error_msg = f"LSA test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def test_textstat_metrics() -> Tuple[bool, str, float]:
    """Test 3: Textstat readability metrics."""
    print("\nTest 3: Textstat Readability Metrics")
    print("-" * 40)

    try:
        # Test document with known characteristics
        test_text = """
        The audit team evaluated the effectiveness of internal controls.
        Management implemented comprehensive risk assessment procedures.
        Financial statements were prepared in accordance with standards.
        The company maintains adequate documentation for all transactions.
        Our review included substantive testing of account balances.
        We obtained sufficient appropriate audit evidence for our opinion.
        """

        start_time = time.time()

        # Calculate various readability scores
        flesch_score = textstat.flesch_reading_ease(test_text)
        flesch_grade = textstat.flesch_kincaid_grade(test_text)
        fog_score = textstat.gunning_fog(test_text)
        smog_score = textstat.smog_index(test_text)
        ari_score = textstat.automated_readability_index(test_text)

        duration_ms = (time.time() - start_time) * 1000

        print(f"  Flesch Reading Ease: {flesch_score:.1f} (0-100, higher=easier)")
        print(f"  Flesch-Kincaid Grade: {flesch_grade:.1f}")
        print(f"  Gunning Fog: {fog_score:.1f}")
        print(f"  SMOG Index: {smog_score:.1f}")
        print(f"  ARI Score: {ari_score:.1f}")
        print(f"  Calculation time: {duration_ms:.1f}ms")

        # Validate scores are in expected ranges
        if not (0 <= flesch_score <= 100):
            return False, f"Flesch score out of range: {flesch_score}", duration_ms

        if not (0 <= flesch_grade <= 20):
            return False, f"Grade level out of range: {flesch_grade}", duration_ms

        print("✓ Textstat metrics calculated successfully")
        return True, "Success", duration_ms

    except Exception as e:
        error_msg = f"Textstat test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def test_cosine_similarity() -> Tuple[bool, str, float]:
    """Test 4: Cosine similarity computation."""
    print("\nTest 4: Cosine Similarity")
    print("-" * 40)

    try:
        # Create small test corpus
        test_docs = [
            "Financial audit report for quarterly review",
            "Quarterly financial audit report review",
            "Technology infrastructure assessment document",
            "Risk management and compliance validation",
        ]

        # Vectorize
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(test_docs)

        # Calculate similarity
        start_time = time.time()
        similarity_matrix = cosine_similarity(tfidf_matrix)
        duration_ms = (time.time() - start_time) * 1000

        print(f"  Documents: {len(test_docs)}")
        print(f"  Similarity matrix shape: {similarity_matrix.shape}")
        print(f"  Doc 0-1 similarity: {similarity_matrix[0, 1]:.3f} (should be high)")
        print(f"  Doc 0-2 similarity: {similarity_matrix[0, 2]:.3f} (should be low)")
        print(f"  Computation time: {duration_ms:.1f}ms")

        # Validate expected similarities
        if similarity_matrix[0, 1] < 0.5:  # Similar docs should have high similarity
            return (
                False,
                f"Low similarity for similar docs: {similarity_matrix[0, 1]:.3f}",
                duration_ms,
            )

        if similarity_matrix[0, 2] > 0.5:  # Different docs should have low similarity
            return (
                False,
                f"High similarity for different docs: {similarity_matrix[0, 2]:.3f}",
                duration_ms,
            )

        # Check matrix properties
        if not np.allclose(similarity_matrix, similarity_matrix.T):
            return False, "Similarity matrix not symmetric", duration_ms

        if not np.allclose(np.diag(similarity_matrix), 1.0):
            return False, "Diagonal elements not 1.0", duration_ms

        print("✓ Cosine similarity computed successfully")
        return True, "Success", duration_ms

    except Exception as e:
        error_msg = f"Cosine similarity test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def test_joblib_serialization() -> Tuple[bool, str, float]:
    """Test 5: Joblib model serialization."""
    print("\nTest 5: Joblib Model Serialization")
    print("-" * 40)

    import os
    import tempfile

    try:
        # Create and train a model
        corpus = ["doc one", "doc two", "doc three"]
        vectorizer = TfidfVectorizer()
        vectorizer.fit(corpus)

        # Test serialization
        with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Save model
            start_time = time.time()
            joblib.dump(vectorizer, tmp_path, compress=3)
            save_time_ms = (time.time() - start_time) * 1000

            file_size_kb = os.path.getsize(tmp_path) / 1024

            # Load model
            start_time = time.time()
            loaded_vectorizer = joblib.load(tmp_path)
            load_time_ms = (time.time() - start_time) * 1000

            # Validate loaded model works
            _ = loaded_vectorizer.transform(["test doc"])

            print(f"  Model type: {type(vectorizer).__name__}")
            print(f"  File size: {file_size_kb:.1f}KB")
            print(f"  Save time: {save_time_ms:.1f}ms")
            print(f"  Load time: {load_time_ms:.1f}ms")
            print("  Compression: level 3")

            # Verify model integrity
            original_vocab = vectorizer.vocabulary_
            loaded_vocab = loaded_vectorizer.vocabulary_

            if original_vocab != loaded_vocab:
                return False, "Vocabulary mismatch after load", save_time_ms + load_time_ms

            print("✓ Joblib serialization successful")
            return True, "Success", save_time_ms + load_time_ms

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        error_msg = f"Joblib test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def test_performance_baseline() -> Tuple[bool, str, float]:
    """Test 6: End-to-end performance baseline."""
    print("\nTest 6: End-to-End Performance Baseline")
    print("-" * 40)

    try:
        # Full pipeline test
        corpus = generate_test_corpus()

        start_time = time.time()

        # Step 1: TF-IDF vectorization
        vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Step 2: LSA reduction
        lsa = TruncatedSVD(n_components=50, random_state=42)
        lsa_matrix = lsa.fit_transform(tfidf_matrix)

        # Step 3: Similarity computation
        similarities = cosine_similarity(lsa_matrix)

        # Step 4: Textstat on first doc
        _ = textstat.flesch_reading_ease(corpus[0])

        total_time_ms = (time.time() - start_time) * 1000

        print(f"  Documents processed: {len(corpus)}")
        print(f"  TF-IDF features: {tfidf_matrix.shape[1]}")
        print(f"  LSA dimensions: {lsa_matrix.shape[1]}")
        print(f"  Similarity pairs: {similarities.shape[0] * (similarities.shape[0] - 1) // 2}")
        print(f"  Total pipeline time: {total_time_ms:.1f}ms")

        # Performance requirement: Full pipeline < 500ms
        if total_time_ms >= 500:
            return False, f"Pipeline too slow: {total_time_ms:.1f}ms >= 500ms", total_time_ms

        print(f"✓ End-to-end pipeline successful ({total_time_ms:.1f}ms < 500ms)")
        return True, "Success", total_time_ms

    except Exception as e:
        error_msg = f"Pipeline test failed: {e}"
        print(f"✗ {error_msg}")
        return False, error_msg, 0.0


def main() -> None:
    """Run all smoke tests and report results."""
    print("=" * 60)
    print("SEMANTIC DEPENDENCIES SMOKE TEST")
    print("=" * 60)
    print("\nValidating scikit-learn, joblib, and textstat installation")
    print("Performance baseline: TF-IDF < 100ms, Pipeline < 500ms")

    # Run all tests
    tests = [
        ("TF-IDF Vectorization", test_tfidf_vectorization),
        ("LSA Decomposition", test_lsa_decomposition),
        ("Textstat Metrics", test_textstat_metrics),
        ("Cosine Similarity", test_cosine_similarity),
        ("Joblib Serialization", test_joblib_serialization),
        ("Performance Baseline", test_performance_baseline),
    ]

    results = []
    total_time_ms = 0.0

    for test_name, test_func in tests:
        success, message, duration_ms = test_func()
        results.append((test_name, success, message, duration_ms))
        total_time_ms += duration_ms

    # Summary report
    print("\n" + "=" * 60)
    print("SMOKE TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success, _, _ in results if success)
    failed = len(results) - passed

    for test_name, success, message, duration_ms in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} : {test_name:25} ({duration_ms:6.1f}ms)")
        if not success and message != "Success":
            print(f"       {message}")

    print("-" * 60)
    print(f"Tests passed: {passed}/{len(results)}")
    print(f"Total time: {total_time_ms:.1f}ms")

    # Performance analysis
    if results[0][1]:  # If TF-IDF test passed
        tfidf_time = results[0][3]
        print("\nPerformance vs baseline:")
        print(f"  TF-IDF: {tfidf_time:.1f}ms / 100ms = {tfidf_time/100:.1%} of limit")

    if results[5][1]:  # If pipeline test passed
        pipeline_time = results[5][3]
        print(f"  Pipeline: {pipeline_time:.1f}ms / 500ms = {pipeline_time/500:.1%} of limit")

    # Exit code
    if failed > 0:
        print(f"\n{failed} test(s) failed. Epic 4 readiness: NOT MET")
        sys.exit(1)
    else:
        print("\n✓ All tests passed! Epic 4 dependencies ready.")
        sys.exit(0)


if __name__ == "__main__":
    main()
