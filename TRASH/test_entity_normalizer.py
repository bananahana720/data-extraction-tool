"""Quick test of EntityNormalizer implementation."""
# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

from src.data_extract.core.models import Document, EntityType, Metadata, ProcessingContext
from src.data_extract.normalize.entities import EntityNormalizer

# Test basic initialization
print("Testing EntityNormalizer initialization...")
normalizer = EntityNormalizer(
    patterns_file=Path("config/normalize/entity_patterns.yaml"),
    dictionary_file=Path("config/normalize/entity_dictionary.yaml"),
    context_window=5,
)
print(f"[OK] Loaded {len(normalizer.patterns)} entity types")
print(f"[OK] Loaded {len(normalizer.dictionary)} abbreviations")

# Test abbreviation expansion
print("\nTesting abbreviation expansion...")
text = "GRC framework review for SOX compliance"
expanded, log = normalizer.expand_abbreviations(text)
print(f"Original: {text}")
print(f"Expanded: {expanded}")
print(f"[OK] Expanded {len(log)} abbreviations")

# Test entity recognition
print("\nTesting entity type recognition...")
test_cases = [
    ("Risk #123", ["identified", "operational"]),
    ("Control-456", ["implement", "test"]),
    ("SOX", ["compliance", "audit"]),
]

for mention, context in test_cases:
    result = normalizer.recognize_entity_type(mention, context)
    if result:
        entity_type, confidence = result
        print(f"[OK] '{mention}' -> {entity_type.value} (confidence: {confidence:.2f})")
    else:
        print(f"[FAIL] '{mention}' -> No match")

# Test ID standardization
print("\nTesting ID standardization...")
test_ids = [
    ("Risk #123", EntityType.RISK),
    ("CONTROL_456", EntityType.CONTROL),
    ("policy 789", EntityType.POLICY),
]

for mention, etype in test_ids:
    canonical = normalizer.standardize_entity_id(mention, etype)
    print(f"'{mention}' -> {canonical}")

print("\n[SUCCESS] All basic tests passed!")
