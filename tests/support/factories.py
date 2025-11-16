"""
Test data factories using Faker for deterministic, randomized test data.

Epic 3/4/5 test infrastructure - generates realistic test data with overrides support.
Follows pytest best practices: pure functions, no global state, deterministic seeding.

Usage:
    from tests.support.factories import chunk_factory, processing_result_factory

    def test_my_feature():
        chunk = chunk_factory(chunk_id="test-001", quality_score=0.95)
        assert chunk.chunk_id == "test-001"
"""

import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.data_extract.chunk.models import (
    Chunk,
    ChunkMetadata,
    EntityReference,
    QualityScore,
)

# Note: Using brownfield imports for now - will migrate to greenfield when available
try:
    from src.core import (
        ContentBlock,
        ContentType,
        ExtractionResult,
        Position,
        ProcessingResult,
        ProcessingStage,
    )
except ImportError:
    # Fallback for greenfield-only environments
    ContentBlock = None
    ContentType = None
    ExtractionResult = None
    Position = None
    ProcessingResult = None
    ProcessingStage = None

# Use stdlib random with fixed seed for deterministic tests
random.seed(42)


# Simple fake data generators (stdlib only - no faker dependency)
def _fake_paragraph(sentences=3):
    """Generate fake paragraph text."""
    sample_sentences = [
        "The risk assessment identified several critical control gaps.",
        "Remediation plans have been developed and approved.",
        "Implementation timeline is scheduled for next quarter.",
        "Control effectiveness will be monitored continuously.",
        "Audit findings have been documented in detail.",
    ]
    return " ".join(random.sample(sample_sentences, min(sentences, len(sample_sentences))))


def _fake_sentence(words=4):
    """Generate fake sentence."""
    sample_words = [
        "Risk",
        "Control",
        "Assessment",
        "Audit",
        "Compliance",
        "Mitigation",
        "Framework",
        "Procedure",
    ]
    return " ".join(random.sample(sample_words, min(words, len(sample_words))))


def _fake_filename(extension="pdf"):
    """Generate fake filename."""
    return f"audit-2024-{random.randint(1, 999):03d}.{extension}"


def _fake_random_int(low, high):
    """Generate random integer."""
    return random.randint(low, high)


# ============================================================================
# Core Model Factories (Epic 2 - Extract & Normalize)
# ============================================================================


def content_block_factory(
    block_type: ContentType = ContentType.PARAGRAPH,
    content: Optional[str] = None,
    page: int = 1,
    sequence_index: int = 0,
    metadata: Optional[Dict[str, Any]] = None,
    confidence: float = 0.95,
    **overrides,
) -> ContentBlock:
    """
    Create a ContentBlock with realistic fake data.

    Args:
        block_type: Type of content block (default: PARAGRAPH)
        content: Block content (default: random paragraph)
        page: Page number (default: 1)
        sequence_index: Position in sequence (default: 0)
        metadata: Block metadata (default: empty dict)
        confidence: Confidence score (default: 0.95)
        **overrides: Additional fields to override

    Returns:
        ContentBlock with fake data
    """
    if content is None:
        if block_type == ContentType.PARAGRAPH:
            content = _fake_paragraph(sentences=3)
        elif block_type == ContentType.HEADING:
            content = _fake_sentence(words=4)
        elif block_type == ContentType.TABLE:
            content = "[Table: 3x3]"
        else:
            content = _fake_paragraph(sentences=2)

    return ContentBlock(
        block_type=block_type,
        content=content,
        position=Position(page=page, sequence_index=sequence_index),
        metadata=metadata or {},
        confidence=confidence,
        **overrides,
    )


def extraction_result_factory(
    source_file: Optional[Path] = None,
    content_blocks: Optional[List[ContentBlock]] = None,
    num_blocks: int = 5,
    **overrides,
) -> ExtractionResult:
    """
    Create an ExtractionResult with realistic fake data.

    Args:
        source_file: Source file path (default: random PDF path)
        content_blocks: List of content blocks (default: auto-generated)
        num_blocks: Number of blocks to generate if content_blocks is None
        **overrides: Additional fields to override

    Returns:
        ExtractionResult with fake data
    """
    if source_file is None:
        source_file = Path(f"/data/{_fake_filename(extension='pdf')}")

    if content_blocks is None:
        content_blocks = [content_block_factory(sequence_index=i) for i in range(num_blocks)]

    return ExtractionResult(
        source_file=source_file,
        content_blocks=content_blocks,
        **overrides,
    )


def processing_result_factory(
    source_file: Optional[Path] = None,
    text: Optional[str] = None,
    entities: Optional[Dict[str, str]] = None,
    num_paragraphs: int = 3,
    **overrides,
) -> ProcessingResult:
    """
    Create a ProcessingResult with realistic fake data.

    Args:
        source_file: Source file path (default: random PDF path)
        text: Normalized text (default: random paragraphs)
        entities: Entity dictionary (default: risk entities)
        num_paragraphs: Number of paragraphs to generate
        **overrides: Additional fields to override

    Returns:
        ProcessingResult with fake data
    """
    if source_file is None:
        source_file = Path(f"/data/{_fake_filename(extension='pdf')}")

    if text is None:
        text = "\n\n".join([_fake_paragraph(sentences=3) for _ in range(num_paragraphs)])

    if entities is None:
        # Generate realistic audit entities
        entities = {
            f"RISK-{_fake_random_int(100, 999):03d}": f"Risk: {_fake_sentence(words=6)}",
            f"CTRL-{_fake_random_int(100, 999):03d}": f"Control: {_fake_sentence(words=6)}",
        }

    return ProcessingResult(
        source_file=source_file,
        text=text,
        entities=entities,
        stage=ProcessingStage.NORMALIZED,
        **overrides,
    )


# ============================================================================
# Chunk Model Factories (Epic 3 - Chunking & Output)
# ============================================================================


def quality_score_factory(
    readability: float = 0.75,
    coherence: float = 0.80,
    completeness: float = 0.85,
    **overrides,
) -> QualityScore:
    """
    Create a QualityScore with realistic values.

    Args:
        readability: Readability score (default: 0.75)
        coherence: Coherence score (default: 0.80)
        completeness: Completeness score (default: 0.85)
        **overrides: Additional fields to override

    Returns:
        QualityScore with realistic values
    """
    return QualityScore(
        readability=readability,
        coherence=coherence,
        completeness=completeness,
        **overrides,
    )


def entity_reference_factory(
    entity_id: Optional[str] = None,
    entity_type: str = "RISK",
    text: Optional[str] = None,
    start_pos: int = 0,
    end_pos: int = 50,
    **overrides,
) -> EntityReference:
    """
    Create an EntityReference with realistic fake data.

    Args:
        entity_id: Entity ID (default: RISK-XXX)
        entity_type: Entity type (default: RISK)
        text: Entity text (default: random sentence)
        start_pos: Start position (default: 0)
        end_pos: End position (default: 50)
        **overrides: Additional fields to override

    Returns:
        EntityReference with fake data
    """
    if entity_id is None:
        entity_id = f"{entity_type}-{_fake_random_int(100, 999):03d}"

    if text is None:
        text = _fake_sentence(words=8)

    return EntityReference(
        entity_id=entity_id,
        entity_type=entity_type,
        text=text,
        start_pos=start_pos,
        end_pos=end_pos,
        **overrides,
    )


def chunk_metadata_factory(
    source_file: Optional[Path] = None,
    section_context: Optional[str] = None,
    entities: Optional[List[EntityReference]] = None,
    quality_score: Optional[QualityScore] = None,
    **overrides,
) -> ChunkMetadata:
    """
    Create ChunkMetadata with realistic fake data.

    Args:
        source_file: Source file path (default: random PDF)
        section_context: Section context (default: random heading)
        entities: Entity references (default: 2 entities)
        quality_score: Quality score (default: high quality)
        **overrides: Additional fields to override

    Returns:
        ChunkMetadata with fake data
    """
    if source_file is None:
        source_file = Path(f"/data/{_fake_filename(extension='pdf')}")

    if section_context is None:
        section_context = _fake_sentence(words=4)

    if entities is None:
        entities = [
            entity_reference_factory(entity_type="RISK"),
            entity_reference_factory(entity_type="CONTROL"),
        ]

    if quality_score is None:
        quality_score = quality_score_factory()

    return ChunkMetadata(
        source_file=source_file,
        section_context=section_context,
        entities=entities,
        quality_score=quality_score,
        processing_version="test-1.0.0",
        **overrides,
    )


def chunk_factory(
    chunk_id: Optional[str] = None,
    text: Optional[str] = None,
    metadata: Optional[ChunkMetadata] = None,
    word_count: Optional[int] = None,
    token_count: Optional[int] = None,
    **overrides,
) -> Chunk:
    """
    Create a Chunk with realistic fake data.

    Args:
        chunk_id: Chunk identifier (default: chunk-XXX)
        text: Chunk text (default: random paragraph)
        metadata: Chunk metadata (default: auto-generated)
        word_count: Word count (default: calculated)
        token_count: Token count (default: ~word_count * 1.3)
        **overrides: Additional fields to override

    Returns:
        Chunk with fake data
    """
    if chunk_id is None:
        chunk_id = f"chunk-{_fake_random_int(1, 999):03d}"

    if text is None:
        text = _fake_paragraph(sentences=5)

    if metadata is None:
        metadata = chunk_metadata_factory()

    if word_count is None:
        word_count = len(text.split())

    if token_count is None:
        token_count = int(word_count * 1.3)  # Approximate BPE tokenization

    return Chunk(
        chunk_id=chunk_id,
        text=text,
        metadata=metadata,
        word_count=word_count,
        token_count=token_count,
        **overrides,
    )


# ============================================================================
# Bulk Factories (Generate Multiple Objects)
# ============================================================================


def chunks_factory(count: int = 5, **kwargs) -> List[Chunk]:
    """
    Generate multiple chunks with sequential IDs.

    Args:
        count: Number of chunks to generate
        **kwargs: Passed to chunk_factory for each chunk

    Returns:
        List of chunks with sequential IDs
    """
    return [chunk_factory(chunk_id=f"chunk-{i+1:03d}", **kwargs) for i in range(count)]


def content_blocks_factory(count: int = 5, **kwargs) -> List[ContentBlock]:
    """
    Generate multiple content blocks with sequential positions.

    Args:
        count: Number of blocks to generate
        **kwargs: Passed to content_block_factory for each block

    Returns:
        List of content blocks with sequential positions
    """
    return [content_block_factory(sequence_index=i, **kwargs) for i in range(count)]


# ============================================================================
# Semantic Analysis Factories (Epic 4 Prep)
# ============================================================================


def document_vector_factory(
    doc_id: Optional[str] = None, dimension: int = 100, **overrides
) -> Dict[str, Any]:
    """
    Create a document vector representation for semantic analysis tests.

    Args:
        doc_id: Document identifier (default: doc-XXX)
        dimension: Vector dimension (default: 100 for TF-IDF)
        **overrides: Additional fields

    Returns:
        Dict with doc_id and sparse vector representation
    """
    if doc_id is None:
        doc_id = f"doc-{_fake_random_int(1, 999):03d}"

    # Simulate sparse TF-IDF vector (only 10% non-zero)
    non_zero_indices = random.sample(range(dimension), k=dimension // 10)
    vector = {idx: random.random() for idx in non_zero_indices}

    return {"doc_id": doc_id, "vector": vector, "dimension": dimension, **overrides}


def similarity_matrix_factory(num_docs: int = 5) -> List[List[float]]:
    """
    Create a similarity matrix for document comparison tests.

    Args:
        num_docs: Number of documents (matrix dimension)

    Returns:
        num_docs x num_docs similarity matrix (symmetric, diagonal=1.0)
    """
    matrix = [[0.0] * num_docs for _ in range(num_docs)]

    for i in range(num_docs):
        for j in range(i, num_docs):
            if i == j:
                sim = 1.0
            else:
                sim = random.random() * 0.8  # Max similarity 0.8
            matrix[i][j] = sim
            matrix[j][i] = sim  # Symmetric

    return matrix
