"""Regenerate gold standard corpus with spaCy-generated boundaries."""

import json
from pathlib import Path

import spacy

# Load model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_md")

# Load current corpus
corpus_path = Path("tests/fixtures/spacy_gold_standard.json")
with open(corpus_path, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# Regenerate expected boundaries using spaCy
print("Regenerating expected boundaries with spaCy...")
for test_case in corpus["test_cases"]:
    text = test_case["text"]
    doc = nlp(text)
    actual_boundaries = [sent.end_char for sent in doc.sents]

    # Update expected boundaries
    old_expected = test_case["expected_boundaries"]
    test_case["expected_boundaries"] = actual_boundaries

    if old_expected != actual_boundaries:
        print(f'  Case {test_case["id"]}: {old_expected} -> {actual_boundaries}')

# Save updated corpus
with open(corpus_path, "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=2)

print(f'\nUpdated {len(corpus["test_cases"])} test cases')
print("Expected boundaries now match spaCy output exactly")
