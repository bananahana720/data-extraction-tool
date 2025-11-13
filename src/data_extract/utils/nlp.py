"""NLP utilities for text processing using spaCy.

This module provides sentence boundary detection and other NLP utilities
for the data extraction pipeline. Used by Epic 3 chunking stage.
"""

from typing import List, Optional

import structlog
from spacy.language import Language

# Module-level cache for lazy loading (load once, reuse pattern from Story 2.5.1.1)
_nlp_model: Optional[Language] = None

logger = structlog.get_logger(__name__)


def get_sentence_boundaries(text: str, nlp: Optional[Language] = None) -> List[int]:
    """Extract sentence boundary positions from text using spaCy.

    Returns character offsets (zero-indexed) where each sentence ends.
    Lazy loads en_core_web_md model if nlp parameter is None.

    Args:
        text: Input text to segment into sentences. Must be non-empty.
        nlp: Optional pre-loaded spaCy Language model. If None, lazy loads
            en_core_web_md and caches for subsequent calls.

    Returns:
        List of character positions (zero-indexed) where sentences end.
        For example, "Hello. World." returns [6, 13].

    Raises:
        ValueError: If text is empty or whitespace-only.
        OSError: If en_core_web_md model is not installed.

    Example:
        >>> boundaries = get_sentence_boundaries("Dr. Smith visited. This is sentence two.")
        >>> print(boundaries)
        [18, 42]

        >>> # With pre-loaded model
        >>> import spacy
        >>> nlp = spacy.load("en_core_web_md")
        >>> boundaries = get_sentence_boundaries("Hello. World.", nlp=nlp)
        >>> print(boundaries)
        [6, 13]

    NFR Compliance:
        - NFR-P3: Model load <5s, segmentation <100ms per 1000 words
        - NFR-O4: Logs model version on first load
        - NFR-R3: Clear error messages for missing model or invalid input
    """
    global _nlp_model

    # Input validation (NFR-R3)
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty or whitespace-only")

    # Lazy load model if not provided
    if nlp is None:
        if _nlp_model is None:
            try:
                import spacy

                _nlp_model = spacy.load("en_core_web_md")

                # Log model metadata on first load (NFR-O4)
                logger.info(
                    "spaCy model loaded",
                    model_name="en_core_web_md",
                    version=_nlp_model.meta["version"],
                    language=_nlp_model.meta["lang"],
                    vocab_size=len(_nlp_model.vocab),
                )
            except OSError as e:
                # Clear error message with actionable resolution (NFR-R3)
                error_msg = (
                    "spaCy model 'en_core_web_md' not found. "
                    "Install with: python -m spacy download en_core_web_md"
                )
                logger.error("spaCy model load failed", error=str(e), resolution=error_msg)
                raise OSError(error_msg) from e

        nlp = _nlp_model

    # Process text and extract sentence boundaries
    doc = nlp(text)
    boundaries = [sent.end_char for sent in doc.sents]

    return boundaries
