#!/usr/bin/env python
"""
Generate Gold-Standard Annotations for Semantic QA Corpus

This script generates gold-standard semantic annotations including:
- TF-IDF top terms
- LSA primary topics
- Entity annotations
- Readability scores

Uses validated semantic libraries from Story 3.5-4.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import numpy as np
import textstat
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_entities(text: str) -> List[str]:
    """Extract entity patterns from document text."""
    entities = []

    # Entity patterns to extract
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


def calculate_readability_scores(text: str) -> Dict[str, float]:
    """Calculate multiple readability metrics for a document."""
    scores = {}

    try:
        # Flesch Reading Ease (0-100, higher = easier)
        scores["flesch_reading_ease"] = round(textstat.flesch_reading_ease(text), 2)

        # Flesch-Kincaid Grade Level
        scores["flesch_kincaid_grade"] = round(textstat.flesch_kincaid_grade(text), 2)

        # Gunning Fog Index
        scores["gunning_fog"] = round(textstat.gunning_fog(text), 2)

        # SMOG Index
        scores["smog_index"] = round(textstat.smog_index(text), 2)

        # Coleman-Liau Index
        scores["coleman_liau_index"] = round(textstat.coleman_liau_index(text), 2)

        # Automated Readability Index
        scores["automated_readability_index"] = round(textstat.automated_readability_index(text), 2)

        # Overall text standard (grade level)
        scores["text_standard"] = textstat.text_standard(text)

        # Additional metrics
        scores["syllable_count"] = textstat.syllable_count(text)
        scores["lexicon_count"] = textstat.lexicon_count(text)
        scores["sentence_count"] = textstat.sentence_count(text)

    except Exception as e:
        print(f"Warning: Error calculating readability scores: {e}")
        scores["error"] = str(e)

    return scores


def generate_tfidf_annotations(documents: List[Dict], n_top_terms: int = 10) -> Tuple[Dict, object]:
    """
    Generate TF-IDF annotations for all documents.

    Returns:
        Tuple of (annotations dict, fitted vectorizer)
    """
    print("Generating TF-IDF annotations...")

    # Prepare corpus
    corpus = [doc["content"] for doc in documents]
    doc_ids = [doc["id"] for doc in documents]

    # Create and fit TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=1000,
        min_df=2,
        max_df=0.95,
        stop_words="english",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True,
        ngram_range=(1, 2),  # Include unigrams and bigrams
    )

    start_time = time.perf_counter()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    fit_time = (time.perf_counter() - start_time) * 1000

    print(f"  TF-IDF fitting completed in {fit_time:.2f}ms")
    print(f"  Matrix shape: {tfidf_matrix.shape}")

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Generate top terms for each document
    annotations = {}

    for idx, doc_id in enumerate(doc_ids):
        # Get TF-IDF scores for this document
        doc_tfidf = tfidf_matrix[idx].toarray()[0]

        # Get top N terms
        top_indices = doc_tfidf.argsort()[-n_top_terms:][::-1]
        top_terms = []

        for term_idx in top_indices:
            if doc_tfidf[term_idx] > 0:
                top_terms.append(
                    {"term": feature_names[term_idx], "score": round(float(doc_tfidf[term_idx]), 4)}
                )

        annotations[doc_id] = {
            "top_terms": top_terms,
            "num_unique_terms": int((doc_tfidf > 0).sum()),
            "max_tfidf_score": round(float(doc_tfidf.max()), 4),
        }

    return annotations, vectorizer


def generate_lsa_annotations(
    documents: List[Dict], vectorizer: object, n_topics: int = 10
) -> Tuple[Dict, object]:
    """
    Generate LSA topic annotations for all documents.

    Returns:
        Tuple of (annotations dict, fitted LSA model)
    """
    print("Generating LSA topic annotations...")

    # Prepare corpus and transform with existing vectorizer
    corpus = [doc["content"] for doc in documents]
    doc_ids = [doc["id"] for doc in documents]

    tfidf_matrix = vectorizer.transform(corpus)

    # Apply LSA
    lsa = TruncatedSVD(n_components=n_topics, random_state=42)

    start_time = time.perf_counter()
    doc_topics = lsa.fit_transform(tfidf_matrix)
    fit_time = (time.perf_counter() - start_time) * 1000

    print(f"  LSA fitting completed in {fit_time:.2f}ms")
    print(f"  Explained variance ratio: {lsa.explained_variance_ratio_.sum():.2%}")

    # Generate topic annotations for each document
    annotations = {}

    for idx, doc_id in enumerate(doc_ids):
        # Get topic distribution for this document
        topic_weights = doc_topics[idx]

        # Get primary topic (highest weight)
        primary_topic = int(topic_weights.argmax())

        # Get top 3 topics
        top_topics_idx = topic_weights.argsort()[-3:][::-1]
        top_topics = []

        for topic_idx in top_topics_idx:
            top_topics.append(
                {"topic_id": int(topic_idx), "weight": round(float(topic_weights[topic_idx]), 4)}
            )

        annotations[doc_id] = {
            "primary_topic": primary_topic,
            "top_topics": top_topics,
            "topic_diversity": round(float(np.std(topic_weights)), 4),
        }

    return annotations, lsa


def main():
    """Generate complete gold-standard annotations for the corpus."""

    print("Generating Gold-Standard Annotations")
    print("=" * 60)

    corpus_dir = Path(__file__).parent / "corpus"
    gold_dir = Path(__file__).parent / "gold-standard"
    gold_dir.mkdir(exist_ok=True)

    # Load all documents
    documents = []
    print("\nLoading corpus documents...")

    for doc_type in ["audit-reports", "risk-matrices", "compliance-docs"]:
        type_dir = corpus_dir / doc_type
        if not type_dir.exists():
            continue

        for doc_file in sorted(type_dir.glob("*.txt")):
            content = doc_file.read_text()
            documents.append(
                {
                    "id": doc_file.stem,
                    "type": doc_type.rstrip("s"),  # Remove trailing 's'
                    "content": content,
                    "file": str(doc_file.relative_to(corpus_dir)),
                }
            )

    print(f"  Loaded {len(documents)} documents")

    # Select subset for gold-standard (40+ documents as per requirement)
    # We'll annotate the first 45 documents to exceed the requirement
    annotated_docs = documents[:45]
    print(f"  Selected {len(annotated_docs)} documents for annotation")

    # Generate TF-IDF annotations
    tfidf_annotations, vectorizer = generate_tfidf_annotations(annotated_docs)

    # Generate LSA annotations
    lsa_annotations, lsa_model = generate_lsa_annotations(annotated_docs, vectorizer, n_topics=10)

    # Generate entity and readability annotations
    print("\nGenerating entity and readability annotations...")
    entity_annotations = {}
    readability_annotations = {}

    for doc in annotated_docs:
        doc_id = doc["id"]

        # Extract entities
        entities = extract_entities(doc["content"])
        entity_annotations[doc_id] = {
            "entities": entities,
            "entity_count": len(entities),
            "unique_entity_types": len(set(e.split("-")[0] for e in entities)),
        }

        # Calculate readability
        readability_annotations[doc_id] = calculate_readability_scores(doc["content"])

    # Combine all annotations
    print("\nCombining annotations...")
    gold_standard = {
        "metadata": {
            "generated_date": "2025-11-18",
            "story": "3.5-6-semantic-qa-fixtures",
            "num_documents": len(annotated_docs),
            "annotation_types": ["tfidf", "lsa", "entities", "readability"],
            "tfidf_config": {
                "max_features": 1000,
                "min_df": 2,
                "max_df": 0.95,
                "ngram_range": [1, 2],
            },
            "lsa_config": {"n_components": 10, "random_state": 42},
        },
        "documents": {},
    }

    for doc in annotated_docs:
        doc_id = doc["id"]
        gold_standard["documents"][doc_id] = {
            "document_id": doc_id,
            "document_type": doc["type"],
            "file_path": doc["file"],
            "tfidf": tfidf_annotations[doc_id],
            "lsa": lsa_annotations[doc_id],
            "entities": entity_annotations[doc_id],
            "readability": readability_annotations[doc_id],
        }

    # Save gold-standard annotations
    gold_standard_path = gold_dir / "gold_standard_annotations.json"
    gold_standard_path.write_text(json.dumps(gold_standard, indent=2))
    print(f"\nSaved gold-standard annotations to: {gold_standard_path}")

    # Save individual annotation files for easier access
    print("\nSaving individual annotation files...")

    # TF-IDF annotations
    tfidf_path = gold_dir / "tfidf_annotations.json"
    tfidf_path.write_text(
        json.dumps(
            {"metadata": gold_standard["metadata"], "annotations": tfidf_annotations}, indent=2
        )
    )
    print(f"  Saved TF-IDF annotations to: {tfidf_path}")

    # LSA annotations
    lsa_path = gold_dir / "lsa_annotations.json"
    lsa_path.write_text(
        json.dumps(
            {"metadata": gold_standard["metadata"], "annotations": lsa_annotations}, indent=2
        )
    )
    print(f"  Saved LSA annotations to: {lsa_path}")

    # Entity annotations
    entities_path = gold_dir / "entity_annotations.json"
    entities_path.write_text(
        json.dumps(
            {"metadata": gold_standard["metadata"], "annotations": entity_annotations}, indent=2
        )
    )
    print(f"  Saved entity annotations to: {entities_path}")

    # Readability annotations
    readability_path = gold_dir / "readability_annotations.json"
    readability_path.write_text(
        json.dumps(
            {"metadata": gold_standard["metadata"], "annotations": readability_annotations},
            indent=2,
        )
    )
    print(f"  Saved readability annotations to: {readability_path}")

    # Save models for reuse
    print("\nSaving trained models...")
    vectorizer_path = gold_dir / "tfidf_vectorizer.joblib"
    joblib.dump(vectorizer, vectorizer_path)
    print(f"  Saved TF-IDF vectorizer to: {vectorizer_path}")

    lsa_path = gold_dir / "lsa_model.joblib"
    joblib.dump(lsa_model, lsa_path)
    print(f"  Saved LSA model to: {lsa_path}")

    # Summary
    print("\n" + "=" * 60)
    print("GOLD-STANDARD GENERATION COMPLETE")
    print("=" * 60)
    print(f"✅ Annotated documents: {len(annotated_docs)}")
    print("✅ Annotation types generated:")
    print("   • TF-IDF top terms (10 per document)")
    print("   • LSA topic assignments (10 topics)")
    print("   • Entity extraction (RISK/CTRL/REQ patterns)")
    print("   • Readability scores (7 metrics)")
    print(f"\n📁 Output location: {gold_dir}")
    print("\n✅ All gold-standard annotations generated successfully!")


if __name__ == "__main__":
    main()
