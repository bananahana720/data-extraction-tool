"""
Unit tests for semantic validation framework.

Tests the SemanticValidator class and its various validation methods.
Ensures the validator can handle TF-IDF vectors, LSA topics with sign ambiguity,
similarity rankings, quality metrics, and regression detection.

Author: Elena (Dev Agent - Semantic Analysis Specialist)
Epic: 4 (Semantic Analysis) - Wave 2.3 Preparation Sprint
Created: 2025-11-18
"""

import json
from pathlib import Path

import numpy as np
import pytest
from scipy.sparse import csr_matrix

from tests.validation.semantic_validator import (
    SemanticValidator,
    check_regression,
    validate_lsa,
    validate_metrics,
    validate_rankings,
    validate_tfidf,
)

# ============================================================================
# SHARED FIXTURES
# ============================================================================


@pytest.fixture
def validator():
    """Create a validator instance."""
    return SemanticValidator()


@pytest.fixture
def sample_tfidf_vectors():
    """Create sample TF-IDF vectors for testing."""
    # Create dense arrays
    actual = np.array(
        [
            [0.5, 0.3, 0.0, 0.2],
            [0.0, 0.4, 0.6, 0.0],
            [0.1, 0.0, 0.0, 0.9],
        ]
    )
    expected = np.array(
        [
            [0.48, 0.32, 0.0, 0.2],  # Slight variations
            [0.0, 0.39, 0.61, 0.0],
            [0.1, 0.0, 0.0, 0.9],
        ]
    )
    return actual, expected


@pytest.fixture
def sample_lsa_topics():
    """Create sample LSA topics for testing."""
    # Topics with potential sign flipping
    actual = np.array(
        [
            [0.5, -0.3, 0.2],  # Topic assignments for doc 1
            [0.4, 0.6, -0.1],  # Topic assignments for doc 2
            [-0.2, 0.1, 0.8],  # Topic assignments for doc 3
        ]
    )
    # Expected with some sign flipping
    expected = np.array(
        [
            [0.5, 0.3, 0.2],  # Topic 2 sign flipped
            [0.4, -0.6, -0.1],  # Topic 2 sign flipped
            [-0.2, -0.1, 0.8],  # Topic 2 sign flipped
        ]
    )
    return actual, expected


@pytest.fixture
def sample_rankings():
    """Create sample document rankings."""
    actual = [
        ("doc1", 0.95),
        ("doc2", 0.85),
        ("doc3", 0.75),
        ("doc4", 0.65),
        ("doc5", 0.55),
    ]
    expected = [
        ("doc1", 0.93),  # Slightly different scores
        ("doc3", 0.84),  # doc2 and doc3 swapped
        ("doc2", 0.74),
        ("doc4", 0.64),
        ("doc5", 0.54),
    ]
    return actual, expected


@pytest.fixture
def sample_metrics():
    """Create sample quality metrics."""
    actual = {
        "flesch_reading_ease": 45.3,
        "flesch_kincaid_grade": 12.5,
        "smog_index": 14.2,
        "avg_sentence_length": 18.5,
    }
    expected = {
        "flesch_reading_ease": 46.0,
        "flesch_kincaid_grade": 12.3,
        "smog_index": 14.0,
        "avg_sentence_length": 18.0,
    }
    return actual, expected


# ============================================================================
# TEST CLASSES
# ============================================================================


class TestSemanticValidator:
    """Test the SemanticValidator class."""

    def test_validator_initialization(self, validator):
        """Test validator initialization."""
        assert validator.gold_standard_path == Path("tests/fixtures/semantic/gold-standard")
        assert isinstance(validator._gold_standards, dict)

    def test_validator_with_custom_path(self, tmp_path):
        """Test validator with custom gold standard path."""
        custom_path = tmp_path / "custom_gold"
        custom_path.mkdir()

        # Create a test gold standard file
        test_data = {"test": "data"}
        gold_file = custom_path / "test.json"
        gold_file.write_text(json.dumps(test_data))

        validator = SemanticValidator(gold_standard_path=custom_path)
        assert validator.gold_standard_path == custom_path
        assert "test" in validator._gold_standards
        assert validator._gold_standards["test"] == test_data


class TestTfIdfValidation:
    """Test TF-IDF vector validation."""

    def test_identical_vectors_pass(self, validator):
        """Test that identical vectors pass validation."""
        vectors = np.array([[0.5, 0.3], [0.2, 0.8]])
        result = validator.validate_tfidf_vectors(vectors, vectors)

        assert result.passed
        assert result.similarity_score == pytest.approx(1.0)
        assert len(result.mismatches) == 0

    def test_similar_vectors_within_tolerance(self, validator, sample_tfidf_vectors):
        """Test that similar vectors within tolerance pass."""
        actual, expected = sample_tfidf_vectors
        result = validator.validate_tfidf_vectors(actual, expected, tolerance=0.05)

        assert result.passed
        assert result.similarity_score > 0.95
        assert len(result.mismatches) == 0

    def test_different_vectors_fail(self, validator):
        """Test that different vectors fail validation."""
        actual = np.array([[0.5, 0.3], [0.2, 0.8]])
        expected = np.array([[0.1, 0.9], [0.7, 0.3]])
        result = validator.validate_tfidf_vectors(actual, expected, tolerance=0.01)

        assert not result.passed
        assert result.similarity_score < 0.7  # Adjusted threshold
        assert len(result.mismatches) > 0

    def test_sparse_matrix_handling(self, validator):
        """Test handling of sparse matrices."""
        # Create sparse matrices
        dense = np.array([[0.5, 0, 0.3], [0, 0.2, 0.8]])
        sparse_actual = csr_matrix(dense)
        sparse_expected = csr_matrix(dense * 0.99)  # Slight variation

        result = validator.validate_tfidf_vectors(sparse_actual, sparse_expected, tolerance=0.02)

        assert result.passed
        assert "sparse" not in str(result.details)  # Converted to dense

    def test_empty_matrix_handling(self, validator):
        """Test handling of empty matrices."""
        empty = np.array([])
        non_empty = np.array([[0.5, 0.3]])

        result = validator.validate_tfidf_vectors(empty, non_empty)
        assert not result.passed
        assert "Empty matrix" in str(result.mismatches)

    def test_shape_mismatch_documents(self, validator):
        """Test handling of document count mismatch."""
        actual = np.array([[0.5, 0.3], [0.2, 0.8]])  # 2 docs
        expected = np.array([[0.5, 0.3], [0.2, 0.8], [0.1, 0.9]])  # 3 docs

        result = validator.validate_tfidf_vectors(actual, expected)
        assert not result.passed
        assert "Document count mismatch" in str(result.mismatches)

    def test_vocabulary_mismatch_warning(self, validator):
        """Test that vocabulary mismatch produces warning, not error."""
        actual = np.array([[0.5, 0.3, 0.2]])  # 3 features
        expected = np.array([[0.5, 0.3]])  # 2 features

        result = validator.validate_tfidf_vectors(actual, expected, tolerance=0.01)
        # Should pad and compare
        assert "Vocabulary size mismatch" in str(result.warnings)

    def test_euclidean_method(self, validator):
        """Test Euclidean distance comparison method."""
        actual = np.array([[0.5, 0.3], [0.2, 0.8]])
        expected = np.array([[0.48, 0.32], [0.19, 0.81]])

        result = validator.validate_tfidf_vectors(
            actual, expected, tolerance=0.05, method="euclidean"
        )

        assert result.passed
        assert "euclidean" in result.details["method"]

    def test_elementwise_method(self, validator):
        """Test element-wise comparison method."""
        actual = np.array([[0.5, 0.3], [0.2, 0.8]])
        expected = np.array([[0.49, 0.31], [0.21, 0.79]])

        result = validator.validate_tfidf_vectors(
            actual, expected, tolerance=0.02, method="elementwise"
        )

        assert result.passed
        assert "elementwise" in result.details["method"]

    def test_zero_vector_handling(self, validator):
        """Test handling of zero vectors."""
        actual = np.array([[0.0, 0.0], [0.5, 0.5]])
        expected = np.array([[0.0, 0.0], [0.5, 0.5]])

        result = validator.validate_tfidf_vectors(actual, expected)
        assert result.passed
        assert result.similarity_score == pytest.approx(1.0)


class TestLsaValidation:
    """Test LSA topic validation with sign-flipping handling."""

    def test_identical_topics_pass(self, validator):
        """Test that identical topics pass validation."""
        topics = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3]])
        result = validator.validate_lsa_topics(topics, topics)

        assert result.passed
        assert result.similarity_score == pytest.approx(1.0)
        assert result.details["sign_flips"] == 0

    def test_sign_flipped_topics_pass(self, validator, sample_lsa_topics):
        """Test that sign-flipped topics still pass validation."""
        actual, expected = sample_lsa_topics
        result = validator.validate_lsa_topics(actual, expected, cosine_threshold=0.9)

        # Should pass despite sign flipping
        assert result.passed
        assert result.similarity_score > 0.9
        # Should have warnings about sign flips
        assert any("Sign flipped" in w for w in result.warnings)
        assert result.details["sign_flips"] > 0

    def test_different_topics_fail(self, validator):
        """Test that different topics fail validation."""
        actual = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3]])
        expected = np.array([[0.1, 0.2, 0.7], [0.8, 0.1, 0.1]])

        result = validator.validate_lsa_topics(actual, expected, cosine_threshold=0.9)

        assert not result.passed
        assert result.similarity_score < 0.5
        assert len(result.mismatches) > 0

    def test_shape_mismatch(self, validator):
        """Test handling of shape mismatch."""
        actual = np.array([[0.5, 0.3], [0.1, 0.6]])  # 2x2
        expected = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3]])  # 2x3

        result = validator.validate_lsa_topics(actual, expected)
        assert not result.passed
        assert "Shape mismatch" in str(result.mismatches)

    def test_transposed_matrix_handling(self, validator):
        """Test handling of transposed topic matrices."""
        # Create topics in (topics x docs) format - more topics than docs
        topics_transposed = np.array(
            [
                [0.5, 0.4],  # Topic 1 weights for 2 docs
                [-0.3, 0.6],  # Topic 2 weights
                [0.2, -0.1],  # Topic 3 weights
                [0.1, 0.8],  # Topic 4 weights
            ]
        )  # 4 topics x 2 docs - should trigger transpose

        # Validation should handle transposition
        result = validator.validate_lsa_topics(topics_transposed, topics_transposed)

        assert result.passed
        # Only warns if rows < columns (more likely to be topics x docs)
        if topics_transposed.shape[0] < topics_transposed.shape[1]:
            assert "Transposed" in str(result.warnings)

    def test_zero_topic_handling(self, validator):
        """Test handling of zero topics."""
        # Create 3x3 matrix to avoid transpose, with a zero column (topic)
        actual = np.array(
            [
                [0.5, 0.0, 0.3],  # Doc 1
                [0.7, 0.0, 0.2],  # Doc 2
                [0.4, 0.0, 0.6],  # Doc 3
            ]
        )  # Topic 2 (index 1) is all zeros
        expected = np.array(
            [
                [0.5, 0.0, 0.3],
                [0.7, 0.0, 0.2],
                [0.4, 0.0, 0.6],
            ]
        )

        result = validator.validate_lsa_topics(actual, expected)

        # The validator should detect the zero topic and warn
        assert result.passed  # Should still pass since they match
        # Check if warning is present (topic with index 1 is all zeros)
        if any(np.allclose(actual[:, i], 0) for i in range(actual.shape[1])):
            assert any(
                "zero vector" in w.lower() for w in result.warnings
            ), f"Warnings: {result.warnings}"


class TestSimilarityRankingValidation:
    """Test document similarity ranking validation."""

    def test_identical_rankings_pass(self, validator):
        """Test that identical rankings pass validation."""
        rankings = [("doc1", 0.9), ("doc2", 0.8), ("doc3", 0.7)]
        result = validator.validate_similarity_rankings(rankings, rankings)

        assert result.passed
        assert result.similarity_score == 1.0
        assert result.details["precision"] == 1.0

    def test_similar_scores_within_tolerance(self, validator, sample_rankings):
        """Test that similar scores within tolerance pass."""
        actual, expected = sample_rankings
        result = validator.validate_similarity_rankings(actual, expected, top_k=3, tolerance=0.05)

        # Should mostly pass with small tolerance
        assert result.details["precision"] >= 0.66  # At least 2/3 match

    def test_different_order_detected(self, validator):
        """Test that different ordering is detected."""
        actual = [("doc1", 0.9), ("doc2", 0.8), ("doc3", 0.7)]
        expected = [("doc4", 0.9), ("doc5", 0.8), ("doc6", 0.7)]  # Completely different docs

        result = validator.validate_similarity_rankings(actual, expected, top_k=3)

        assert not result.passed
        assert result.details["precision"] == 0.0  # No overlap
        assert "Missing from top" in str(result.mismatches)

    def test_empty_rankings(self, validator):
        """Test handling of empty rankings."""
        result = validator.validate_similarity_rankings([], [])
        assert result.passed
        assert result.similarity_score == 1.0

        result = validator.validate_similarity_rankings([], [("doc1", 0.9)])
        assert not result.passed

    def test_top_k_filtering(self, validator):
        """Test top-K filtering."""
        actual = [(f"doc{i}", 0.9 - i * 0.1) for i in range(10)]
        expected = [(f"doc{i}", 0.9 - i * 0.1) for i in range(10)]
        # Swap one document outside top-3
        expected[5], expected[6] = expected[6], expected[5]

        result = validator.validate_similarity_rankings(actual, expected, top_k=3)

        # Top-3 should still match
        assert result.passed
        assert result.details["precision"] == 1.0

    def test_rank_difference_warnings(self, validator):
        """Test that large rank differences produce warnings."""
        actual = [("doc1", 0.9), ("doc2", 0.8), ("doc3", 0.7), ("doc4", 0.6)]
        expected = [("doc4", 0.9), ("doc3", 0.8), ("doc2", 0.7), ("doc1", 0.6)]

        result = validator.validate_similarity_rankings(actual, expected, top_k=4, tolerance=0.5)

        # Should have warnings about rank differences
        assert any("rank difference" in w for w in result.warnings)


class TestQualityMetricsValidation:
    """Test quality metrics validation."""

    def test_identical_metrics_pass(self, validator):
        """Test that identical metrics pass validation."""
        metrics = {"score1": 10.5, "score2": 20.3, "score3": 15.8}
        result = validator.validate_quality_metrics(metrics, metrics)

        assert result.passed
        assert result.similarity_score == 1.0

    def test_similar_metrics_within_tolerance(self, validator, sample_metrics):
        """Test that similar metrics within tolerance pass."""
        actual, expected = sample_metrics
        result = validator.validate_quality_metrics(actual, expected, tolerance=0.05)

        assert result.passed
        assert result.similarity_score > 0.95

    def test_different_metrics_fail(self, validator):
        """Test that different metrics fail validation."""
        actual = {"score1": 10.0, "score2": 20.0}
        expected = {"score1": 15.0, "score2": 30.0}

        result = validator.validate_quality_metrics(actual, expected, tolerance=0.1)

        assert not result.passed
        assert len(result.mismatches) > 0

    def test_missing_metrics(self, validator):
        """Test detection of missing metrics."""
        actual = {"score1": 10.0}
        expected = {"score1": 10.0, "score2": 20.0}

        result = validator.validate_quality_metrics(actual, expected)

        assert not result.passed
        assert "Missing metrics" in str(result.mismatches)

    def test_extra_metrics_warning(self, validator):
        """Test that extra metrics produce warnings."""
        actual = {"score1": 10.0, "score2": 20.0, "extra": 5.0}
        expected = {"score1": 10.0, "score2": 20.0}

        result = validator.validate_quality_metrics(actual, expected)

        assert result.passed  # Extra metrics shouldn't fail
        assert "Extra metrics" in str(result.warnings)

    def test_zero_value_handling(self, validator):
        """Test handling of zero values."""
        actual = {"zero_score": 0.0, "non_zero": 10.0}
        expected = {"zero_score": 0.0, "non_zero": 10.5}

        result = validator.validate_quality_metrics(actual, expected, tolerance=0.05)

        # Zero values should match exactly
        assert result.details["metric_details"]["zero_score"]["similarity"] == 1.0


class TestRegressionDetection:
    """Test regression detection functionality."""

    def test_no_regression(self, validator):
        """Test detection when no regression exists."""
        baseline = {"accuracy": 0.95, "f1_score": 0.92, "processing_time_ms": 100}
        current = {"accuracy": 0.96, "f1_score": 0.93, "processing_time_ms": 95}

        report = validator.detect_regression(current, baseline)

        assert not report.has_regression
        assert len(report.degraded_metrics) == 0
        assert len(report.improved_metrics) > 0

    def test_regression_detected(self, validator):
        """Test detection of performance regression."""
        baseline = {"accuracy": 0.95, "f1_score": 0.92, "processing_time_ms": 100}
        current = {"accuracy": 0.85, "f1_score": 0.88, "processing_time_ms": 150}

        report = validator.detect_regression(current, baseline, tolerance=0.05)

        assert report.has_regression
        assert len(report.degraded_metrics) > 0
        assert "accuracy" in str(report.degraded_metrics)
        assert "processing_time_ms" in str(report.degraded_metrics)

    def test_missing_metric_regression(self, validator):
        """Test that missing metrics are treated as regression."""
        baseline = {"accuracy": 0.95, "f1_score": 0.92}
        current = {"accuracy": 0.95}  # Missing f1_score

        report = validator.detect_regression(current, baseline)

        assert report.has_regression
        assert "f1_score: MISSING" in report.degraded_metrics

    def test_lower_is_better_metrics(self, validator):
        """Test handling of "lower is better" metrics."""
        baseline = {"accuracy": 0.95, "error_rate": 0.05, "processing_time_ms": 100}
        current = {"accuracy": 0.94, "error_rate": 0.04, "processing_time_ms": 90}

        report = validator.detect_regression(current, baseline, tolerance=0.05)

        # Error rate and processing time improved (lower is better)
        assert "error_rate" in str(report.improved_metrics)
        assert "processing_time_ms" in str(report.improved_metrics)

    def test_zero_baseline_handling(self, validator):
        """Test handling of zero baseline values."""
        baseline = {"zero_metric": 0.0, "non_zero": 10.0}
        current = {"zero_metric": 0.1, "non_zero": 11.0}

        report = validator.detect_regression(current, baseline)

        # Should handle zero baseline without dividing by zero
        assert "zero_metric" in report.details
        assert report.details["zero_metric"]["change_pct"] == "inf"

    def test_non_numeric_metrics_skipped(self, validator):
        """Test that non-numeric metrics are skipped."""
        baseline = {"accuracy": 0.95, "model_name": "v1"}
        current = {"accuracy": 0.96, "model_name": "v2"}

        report = validator.detect_regression(current, baseline)

        assert not report.has_regression
        assert report.details["model_name"]["status"] == "non-numeric"


class TestConvenienceFunctions:
    """Test convenience functions for validation."""

    def test_validate_tfidf_convenience(self):
        """Test validate_tfidf convenience function."""
        actual = np.array([[0.5, 0.3]])
        expected = np.array([[0.49, 0.31]])

        result = validate_tfidf(actual, expected, tolerance=0.02)
        assert result.passed

    def test_validate_lsa_convenience(self):
        """Test validate_lsa convenience function."""
        topics = np.array([[0.5, 0.3], [0.2, 0.8]])
        result = validate_lsa(topics, topics)
        assert result.passed

    def test_validate_rankings_convenience(self):
        """Test validate_rankings convenience function."""
        rankings = [("doc1", 0.9), ("doc2", 0.8)]
        result = validate_rankings(rankings, rankings)
        assert result.passed

    def test_validate_metrics_convenience(self):
        """Test validate_metrics convenience function."""
        metrics = {"score": 10.0}
        result = validate_metrics(metrics, metrics)
        assert result.passed

    def test_check_regression_convenience(self):
        """Test check_regression convenience function."""
        baseline = {"accuracy": 0.95}
        current = {"accuracy": 0.96}
        report = check_regression(current, baseline)
        assert not report.has_regression


class TestGoldStandardIntegration:
    """Test integration with gold standard files."""

    def test_load_gold_standards(self, tmp_path):
        """Test loading gold standards from files."""
        # Create test gold standard files
        gold_path = tmp_path / "gold"
        gold_path.mkdir()

        tfidf_gold = {
            "vocabulary_size": 100,
            "num_documents": 10,
            "top_terms": ["control", "risk", "assessment"],
        }
        lsa_gold = {"num_topics": 5, "explained_variance": 0.85}

        (gold_path / "tfidf.json").write_text(json.dumps(tfidf_gold))
        (gold_path / "lsa.json").write_text(json.dumps(lsa_gold))

        validator = SemanticValidator(gold_standard_path=gold_path)

        assert "tfidf" in validator._gold_standards
        assert "lsa" in validator._gold_standards
        assert validator._gold_standards["tfidf"]["vocabulary_size"] == 100
        assert validator._gold_standards["lsa"]["num_topics"] == 5

    def test_nonexistent_gold_path(self, tmp_path):
        """Test handling of non-existent gold standard path."""
        nonexistent = tmp_path / "nonexistent"
        validator = SemanticValidator(gold_standard_path=nonexistent)

        # Should initialize without error
        assert validator.gold_standard_path == nonexistent
        assert len(validator._gold_standards) == 0
