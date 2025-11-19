"""
Semantic Validation Framework

Validates TF-IDF vectors, LSA topics, similarity scores, and quality metrics
against gold-standard annotations or expected behaviors.

This framework addresses the critical need for validating semantic analysis correctness,
particularly handling the non-deterministic aspects of LSA (sign-flipping) and providing
flexible tolerance levels for TF-IDF vector comparisons.

Usage:
    validator = SemanticValidator(gold_standard_path)
    result = validator.validate_tfidf_vectors(actual, expected, tolerance=0.01)
    if not result.passed:
        print(result.mismatches)

Author: Elena (Dev Agent - Semantic Analysis Specialist)
Epic: 4 (Semantic Analysis) - Wave 2.3 Preparation Sprint
Created: 2025-11-18
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from scipy.sparse import csr_matrix, issparse
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ValidationResult:
    """
    Results from semantic validation.

    Attributes:
        passed: Whether validation passed all criteria
        similarity_score: Overall similarity metric (0.0-1.0)
        mismatches: List of specific validation failures
        warnings: List of non-critical issues or observations
        details: Additional metrics and debug information
    """

    passed: bool
    similarity_score: float
    mismatches: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegressionReport:
    """
    Report on semantic model regression vs baseline.

    Attributes:
        has_regression: Whether any metrics degraded beyond tolerance
        degraded_metrics: List of metrics that got worse
        improved_metrics: List of metrics that improved
        details: Detailed comparison data for each metric
    """

    has_regression: bool
    degraded_metrics: List[str] = field(default_factory=list)
    improved_metrics: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class SemanticValidator:
    """
    Framework for validating semantic analysis outputs.

    This validator handles the complexities of comparing semantic analysis results:
    - TF-IDF vector validation with multiple comparison methods
    - LSA topic validation with sign-flipping ambiguity handling
    - Similarity score validation with ranking preservation
    - Quality metrics validation with flexible tolerances
    - Regression detection against baseline performance

    ULTRATHINK Design Decisions:
    - Tolerance levels default to 1% for TF-IDF (strict) and 10% for LSA (looser due to SVD)
    - Sign-flipping is handled by taking absolute cosine similarity for LSA topics
    - Vocabulary differences are warnings not errors (corpus can evolve)
    - Top-K precision is more important than exact score matching
    """

    def __init__(self, gold_standard_path: Optional[Path] = None):
        """
        Initialize validator with optional gold standards.

        Args:
            gold_standard_path: Path to gold-standard annotations.
                              If None, uses tests/fixtures/semantic/gold-standard/
        """
        if gold_standard_path is None:
            gold_standard_path = Path("tests/fixtures/semantic/gold-standard")

        self.gold_standard_path = gold_standard_path
        self._gold_standards = {}

        # Load gold standards if they exist
        if gold_standard_path.exists():
            self._load_gold_standards()

    def _load_gold_standards(self):
        """Load all gold-standard JSON files."""
        for json_file in self.gold_standard_path.glob("*.json"):
            key = json_file.stem  # e.g., "tfidf-expected" from "tfidf-expected.json"
            with open(json_file, "r", encoding="utf-8") as f:
                self._gold_standards[key] = json.load(f)

    def validate_tfidf_vectors(
        self,
        actual: Union[np.ndarray, csr_matrix],
        expected: Union[np.ndarray, csr_matrix],
        tolerance: float = 0.01,
        method: str = "cosine",
    ) -> ValidationResult:
        """
        Validate TF-IDF vectors against expected values.

        Args:
            actual: Actual TF-IDF matrix (sparse or dense)
            expected: Expected TF-IDF matrix
            tolerance: Maximum allowed difference (default 0.01 = 1%)
            method: Comparison method ("cosine", "euclidean", "elementwise")

        Returns:
            ValidationResult with pass/fail and details

        ULTRATHINK Considerations:
        - Vocabulary differences are common when corpus changes (warning not error)
        - Sparse matrices need conversion for comparison
        - Cosine similarity is most robust to scaling differences
        - Element-wise comparison is most strict but brittle
        """
        mismatches = []
        warnings = []

        # Convert to dense for comparison
        if issparse(actual):
            actual_dense = actual.toarray()
        else:
            actual_dense = np.asarray(actual)

        if issparse(expected):
            expected_dense = expected.toarray()
        else:
            expected_dense = np.asarray(expected)

        # Handle empty matrices
        if actual_dense.size == 0 or expected_dense.size == 0:
            return ValidationResult(
                passed=False,
                similarity_score=0.0,
                mismatches=["Empty matrix provided"],
                warnings=warnings,
                details={"method": method, "tolerance": tolerance},
            )

        # Check shape compatibility
        if actual_dense.shape != expected_dense.shape:
            # Try to align if only vocabulary differs
            if actual_dense.shape[0] == expected_dense.shape[0]:
                warnings.append(
                    f"Vocabulary size mismatch: {actual_dense.shape[1]} vs {expected_dense.shape[1]}"
                )
                # Pad smaller matrix to match larger for comparison
                if actual_dense.shape[1] < expected_dense.shape[1]:
                    padding = expected_dense.shape[1] - actual_dense.shape[1]
                    actual_dense = np.pad(actual_dense, ((0, 0), (0, padding)))
                else:
                    padding = actual_dense.shape[1] - expected_dense.shape[1]
                    expected_dense = np.pad(expected_dense, ((0, 0), (0, padding)))
            else:
                return ValidationResult(
                    passed=False,
                    similarity_score=0.0,
                    mismatches=[
                        f"Document count mismatch: {actual_dense.shape[0]} vs {expected_dense.shape[0]}"
                    ],
                    warnings=warnings,
                    details={"method": method, "tolerance": tolerance},
                )

        # Compute similarity based on method
        if method == "cosine":
            # Document-wise cosine similarity
            similarities = []
            for i in range(actual_dense.shape[0]):
                # Handle zero vectors
                actual_vec = actual_dense[i : i + 1]
                expected_vec = expected_dense[i : i + 1]

                if np.allclose(actual_vec, 0) and np.allclose(expected_vec, 0):
                    # Both zero vectors - perfect match
                    similarities.append(1.0)
                elif np.allclose(actual_vec, 0) or np.allclose(expected_vec, 0):
                    # One zero vector - no match
                    similarities.append(0.0)
                    mismatches.append(f"Document {i}: one vector is zero")
                else:
                    sim = cosine_similarity(actual_vec, expected_vec)[0, 0]
                    similarities.append(sim)

                    if sim < (1.0 - tolerance):
                        mismatches.append(
                            f"Document {i}: similarity {sim:.4f} < threshold {1.0-tolerance:.4f}"
                        )

            avg_similarity = np.mean(similarities) if similarities else 0.0

        elif method == "euclidean":
            # Euclidean distance per document
            distances = []
            for i in range(actual_dense.shape[0]):
                dist = np.linalg.norm(actual_dense[i] - expected_dense[i])
                distances.append(dist)

                if dist > tolerance:
                    mismatches.append(
                        f"Document {i}: distance {dist:.4f} > tolerance {tolerance:.4f}"
                    )

            # Convert distance to similarity score (0=far, 1=identical)
            avg_distance = np.mean(distances) if distances else float("inf")
            avg_similarity = 1.0 / (1.0 + avg_distance)

        else:  # elementwise
            # Element-wise comparison
            diff = np.abs(actual_dense - expected_dense)
            max_diff = np.max(diff)
            avg_diff = np.mean(diff)

            avg_similarity = max(0.0, 1.0 - avg_diff)

            # Check each document for tolerance violations
            for i in range(actual_dense.shape[0]):
                doc_max_diff = np.max(diff[i])
                if doc_max_diff > tolerance:
                    mismatches.append(
                        f"Document {i}: max difference {doc_max_diff:.4f} > tolerance {tolerance:.4f}"
                    )

        passed = len(mismatches) == 0

        return ValidationResult(
            passed=passed,
            similarity_score=avg_similarity,
            mismatches=mismatches,
            warnings=warnings,
            details={
                "method": method,
                "tolerance": tolerance,
                "shape": actual_dense.shape,
                "num_documents": actual_dense.shape[0],
                "num_features": actual_dense.shape[1],
            },
        )

    def validate_lsa_topics(
        self, actual_topics: np.ndarray, expected_topics: np.ndarray, cosine_threshold: float = 0.9
    ) -> ValidationResult:
        """
        Validate LSA topic extraction handling sign ambiguity.

        Args:
            actual_topics: Actual LSA topic matrix (documents x topics)
            expected_topics: Expected LSA topics
            cosine_threshold: Minimum absolute cosine similarity for match

        Returns:
            ValidationResult

        ULTRATHINK: LSA has inherent sign ambiguity from SVD decomposition.
        Topics [0.5, 0.3] and [-0.5, -0.3] are mathematically equivalent.
        We use absolute value of cosine similarity to handle this.
        """
        mismatches = []
        warnings = []

        # Convert to arrays if needed
        actual_topics = np.asarray(actual_topics)
        expected_topics = np.asarray(expected_topics)

        # Check shape
        if actual_topics.shape != expected_topics.shape:
            return ValidationResult(
                passed=False,
                similarity_score=0.0,
                mismatches=[f"Shape mismatch: {actual_topics.shape} vs {expected_topics.shape}"],
                warnings=warnings,
                details={"cosine_threshold": cosine_threshold},
            )

        # Handle both (docs x topics) and (topics x docs) layouts
        if actual_topics.shape[0] < actual_topics.shape[1]:
            # Likely topics x docs, transpose for consistency
            actual_topics = actual_topics.T
            expected_topics = expected_topics.T
            warnings.append(
                "Transposed topics matrix for validation (topics x docs → docs x topics)"
            )

        # Compute topic-wise similarity (handle sign-flipping)
        similarities = []
        num_topics = actual_topics.shape[1] if len(actual_topics.shape) > 1 else 1

        for i in range(num_topics):  # For each topic
            if len(actual_topics.shape) > 1:
                actual_topic = actual_topics[:, i : i + 1]
                expected_topic = expected_topics[:, i : i + 1]
            else:
                actual_topic = actual_topics.reshape(-1, 1)
                expected_topic = expected_topics.reshape(-1, 1)

            # Check for zero topics
            if np.allclose(actual_topic, 0) or np.allclose(expected_topic, 0):
                warnings.append(f"Topic {i}: Contains zero vector")
                similarities.append(0.0)
                continue

            sim = cosine_similarity(actual_topic.T, expected_topic.T)[0, 0]

            # Take absolute value to handle sign-flipping
            abs_sim = abs(sim)
            similarities.append(abs_sim)

            if abs_sim < cosine_threshold:
                mismatches.append(
                    f"Topic {i}: similarity {abs_sim:.4f} < threshold {cosine_threshold:.4f}"
                )

            # Track sign flips as warnings
            if sim < 0 and abs_sim >= cosine_threshold:
                warnings.append(
                    f"Topic {i}: Sign flipped (similarity={sim:.4f}, using abs={abs_sim:.4f})"
                )

        avg_similarity = np.mean(similarities) if similarities else 0.0
        passed = len(mismatches) == 0

        return ValidationResult(
            passed=passed,
            similarity_score=avg_similarity,
            mismatches=mismatches,
            warnings=warnings,
            details={
                "cosine_threshold": cosine_threshold,
                "num_topics": num_topics,
                "num_documents": actual_topics.shape[0],
                "sign_flips": sum(1 for w in warnings if "Sign flipped" in w),
            },
        )

    def validate_similarity_rankings(
        self,
        actual_rankings: List[Tuple[str, float]],
        expected_rankings: List[Tuple[str, float]],
        top_k: int = 10,
        tolerance: float = 0.05,
    ) -> ValidationResult:
        """
        Validate document similarity rankings focusing on order preservation.

        Args:
            actual_rankings: List of (doc_id, score) tuples
            expected_rankings: Expected rankings
            top_k: Only validate top K results
            tolerance: Score difference tolerance

        Returns:
            ValidationResult

        ULTRATHINK: Exact score matching is brittle and affected by:
        - Vocabulary changes (new terms added/removed)
        - Floating point precision differences
        - TF-IDF normalization variations

        Focus on:
        1. Top-K precision (same documents in top results)
        2. Ranking order (relative positions)
        3. Score differences within tolerance
        """
        mismatches = []
        warnings = []

        # Handle empty rankings
        if not actual_rankings and not expected_rankings:
            return ValidationResult(
                passed=True,
                similarity_score=1.0,
                mismatches=[],
                warnings=[],
                details={"top_k": top_k, "precision": 1.0},
            )

        if not actual_rankings or not expected_rankings:
            return ValidationResult(
                passed=False,
                similarity_score=0.0,
                mismatches=["Empty rankings provided"],
                warnings=[],
                details={"top_k": top_k},
            )

        # Limit to top K
        actual_top_k = actual_rankings[: min(top_k, len(actual_rankings))]
        expected_top_k = expected_rankings[: min(top_k, len(expected_rankings))]

        # Check if same documents in top K
        actual_ids = {doc_id for doc_id, _ in actual_top_k}
        expected_ids = {doc_id for doc_id, _ in expected_top_k}

        missing = expected_ids - actual_ids
        extra = actual_ids - expected_ids

        if missing:
            mismatches.append(f"Missing from top-{top_k}: {sorted(missing)}")
        if extra:
            warnings.append(f"Extra in top-{top_k}: {sorted(extra)}")

        # Check ranking order for common documents
        actual_order = {doc_id: idx for idx, (doc_id, _) in enumerate(actual_top_k)}
        expected_order = {doc_id: idx for idx, (doc_id, _) in enumerate(expected_top_k)}

        common_ids = actual_ids & expected_ids
        rank_differences = []

        for doc_id in common_ids:
            actual_rank = actual_order[doc_id]
            expected_rank = expected_order[doc_id]
            rank_diff = abs(actual_rank - expected_rank)
            rank_differences.append(rank_diff)

            if rank_diff > 2:  # Allow small rank variations
                warnings.append(
                    f"Document {doc_id}: rank difference {rank_diff} "
                    f"(actual: {actual_rank}, expected: {expected_rank})"
                )

        # Check score differences for matching documents
        actual_scores = {doc_id: score for doc_id, score in actual_top_k}
        expected_scores = {doc_id: score for doc_id, score in expected_top_k}

        score_diffs = []
        for doc_id in common_ids:
            actual_score = actual_scores[doc_id]
            expected_score = expected_scores[doc_id]
            diff = abs(actual_score - expected_score)
            score_diffs.append(diff)

            if diff > tolerance:
                mismatches.append(
                    f"Document {doc_id}: score diff {diff:.4f} > tolerance {tolerance:.4f} "
                    f"(actual: {actual_score:.4f}, expected: {expected_score:.4f})"
                )

        # Calculate precision
        overlap = len(common_ids)
        precision = overlap / min(top_k, len(expected_top_k)) if expected_top_k else 0.0

        # Consider it passed if precision is high and no major score differences
        passed = len(mismatches) == 0 and precision >= 0.8

        return ValidationResult(
            passed=passed,
            similarity_score=precision,
            mismatches=mismatches,
            warnings=warnings,
            details={
                "top_k": top_k,
                "precision": precision,
                "avg_score_diff": np.mean(score_diffs) if score_diffs else 0.0,
                "avg_rank_diff": np.mean(rank_differences) if rank_differences else 0.0,
                "common_documents": len(common_ids),
            },
        )

    def validate_quality_metrics(
        self,
        actual_metrics: Dict[str, float],
        expected_metrics: Dict[str, float],
        tolerance: float = 0.1,
    ) -> ValidationResult:
        """
        Validate readability and quality metrics.

        Args:
            actual_metrics: Actual quality metrics dict
            expected_metrics: Expected quality metrics dict
            tolerance: Maximum relative difference (default 0.1 = 10%)

        Returns:
            ValidationResult
        """
        mismatches = []
        warnings = []
        details = {}

        # Check for missing metrics
        missing_metrics = set(expected_metrics.keys()) - set(actual_metrics.keys())
        extra_metrics = set(actual_metrics.keys()) - set(expected_metrics.keys())

        if missing_metrics:
            mismatches.append(f"Missing metrics: {sorted(missing_metrics)}")
        if extra_metrics:
            warnings.append(f"Extra metrics: {sorted(extra_metrics)}")

        # Compare common metrics
        common_metrics = set(actual_metrics.keys()) & set(expected_metrics.keys())
        metric_similarities = []

        for metric_name in common_metrics:
            actual_value = actual_metrics[metric_name]
            expected_value = expected_metrics[metric_name]

            # Handle zero values
            if expected_value == 0:
                if actual_value == 0:
                    similarity = 1.0
                else:
                    similarity = 0.0
                    mismatches.append(f"{metric_name}: expected 0, got {actual_value}")
            else:
                # Calculate relative difference
                rel_diff = abs(actual_value - expected_value) / abs(expected_value)
                similarity = max(0.0, 1.0 - rel_diff)

                if rel_diff > tolerance:
                    mismatches.append(
                        f"{metric_name}: relative diff {rel_diff:.2%} > tolerance {tolerance:.2%} "
                        f"(actual: {actual_value:.2f}, expected: {expected_value:.2f})"
                    )

            metric_similarities.append(similarity)
            details[metric_name] = {
                "actual": actual_value,
                "expected": expected_value,
                "similarity": similarity,
            }

        avg_similarity = np.mean(metric_similarities) if metric_similarities else 0.0
        passed = len(mismatches) == 0

        return ValidationResult(
            passed=passed,
            similarity_score=avg_similarity,
            mismatches=mismatches,
            warnings=warnings,
            details={
                "tolerance": tolerance,
                "metrics_compared": len(common_metrics),
                "metric_details": details,
            },
        )

    def detect_regression(
        self,
        current_results: Dict[str, Any],
        baseline_results: Dict[str, Any],
        tolerance: float = 0.05,
    ) -> RegressionReport:
        """
        Detect semantic model regression vs baseline.

        Args:
            current_results: Current metrics/results
            baseline_results: Baseline metrics/results
            tolerance: Degradation threshold (default 0.05 = 5%)

        Returns:
            RegressionReport

        ULTRATHINK: Regression detection needs to be smart about:
        - Different metric types (higher is better vs lower is better)
        - Missing metrics (new features added/removed)
        - Noise in measurements (small variations are normal)
        """
        degraded = []
        improved = []
        details = {}

        # Define which metrics are "lower is better"
        lower_is_better = {
            "processing_time_ms",
            "memory_usage_mb",
            "error_rate",
            "distance",
            "loss",
            "mse",
            "mae",
            "rmse",
        }

        for metric_name, baseline_value in baseline_results.items():
            if metric_name not in current_results:
                degraded.append(f"{metric_name}: MISSING")
                details[metric_name] = {"status": "missing"}
                continue

            current_value = current_results[metric_name]

            # Skip non-numeric comparisons
            if not isinstance(baseline_value, (int, float)) or not isinstance(
                current_value, (int, float)
            ):
                details[metric_name] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "status": "non-numeric",
                }
                continue

            # Calculate change
            if baseline_value == 0:
                if current_value == 0:
                    change = 0.0
                else:
                    # Infinite change from zero baseline
                    change = float("inf") if current_value > 0 else float("-inf")
            else:
                change = (current_value - baseline_value) / abs(baseline_value)

            details[metric_name] = {
                "baseline": baseline_value,
                "current": current_value,
                "change_pct": change * 100 if not np.isinf(change) else "inf",
            }

            # Determine if metric degraded or improved
            is_lower_better = any(indicator in metric_name.lower() for indicator in lower_is_better)

            if is_lower_better:
                # Lower values are better
                if change > tolerance:
                    degraded.append(f"{metric_name}: +{change*100:.1f}% (worse)")
                elif change < -tolerance:
                    improved.append(f"{metric_name}: {change*100:.1f}% (better)")
            else:
                # Higher values are better (accuracy, f1_score, etc.)
                if change < -tolerance:
                    degraded.append(f"{metric_name}: {change*100:.1f}% (worse)")
                elif change > tolerance:
                    improved.append(f"{metric_name}: +{change*100:.1f}% (better)")
                elif change > 0:  # Small positive change still an improvement
                    improved.append(f"{metric_name}: +{change*100:.1f}% (better)")

        # Check for new metrics (potential improvements)
        new_metrics = set(current_results.keys()) - set(baseline_results.keys())
        if new_metrics:
            details["new_metrics"] = list(new_metrics)

        has_regression = len(degraded) > 0

        return RegressionReport(
            has_regression=has_regression,
            degraded_metrics=degraded,
            improved_metrics=improved,
            details=details,
        )


# Convenience functions for common validations


def validate_tfidf(actual, expected, tolerance=0.01):
    """Quick TF-IDF validation helper."""
    validator = SemanticValidator()
    return validator.validate_tfidf_vectors(actual, expected, tolerance)


def validate_lsa(actual, expected, threshold=0.9):
    """Quick LSA validation helper."""
    validator = SemanticValidator()
    return validator.validate_lsa_topics(actual, expected, threshold)


def validate_rankings(actual, expected, top_k=10, tolerance=0.05):
    """Quick similarity ranking validation helper."""
    validator = SemanticValidator()
    return validator.validate_similarity_rankings(actual, expected, top_k, tolerance)


def validate_metrics(actual, expected, tolerance=0.1):
    """Quick quality metrics validation helper."""
    validator = SemanticValidator()
    return validator.validate_quality_metrics(actual, expected, tolerance)


def check_regression(current, baseline, tolerance=0.05):
    """Quick regression check helper."""
    validator = SemanticValidator()
    return validator.detect_regression(current, baseline, tolerance)
