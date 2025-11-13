"""
QualityValidator Processor - Score Extraction Quality

This processor validates extraction quality by scoring:
- Completeness: Expected content types present (headings, paragraphs, etc.)
- Consistency: Proper block structure, confidence scores, metadata
- Readability: Text is readable and not corrupted
- Overall quality: Combined score from all dimensions (0-100)

Example Quality Assessment:
    Quality Score: 85.2/100
    Issues: ["2 empty blocks found", "1 block without confidence"]
    Needs Review: False

Design:
- Informational: Provides quality metrics, doesn't modify content
- Comprehensive: Checks multiple quality dimensions
- Actionable: Provides specific issues and recommendations
- Configurable: Thresholds and penalties can be adjusted
"""


from core import (
    BaseProcessor,
    ContentBlock,
    ContentType,
    ExtractionResult,
    ProcessingResult,
    ProcessingStage,
)


class QualityValidator(BaseProcessor):
    """
    Validate extraction quality and compute quality scores.

    This processor:
    - Computes quality score (0-100) based on multiple dimensions
    - Identifies specific quality issues
    - Sets needs_review flag for low-quality extractions
    - Provides detailed quality metrics in stage_metadata

    Quality Dimensions:
    1. Completeness (0-100):
       - Presence of headings
       - Content type diversity
       - Document structure

    2. Consistency (0-100):
       - Confidence scores present
       - Metadata completeness
       - Block structure validity

    3. Readability (0-100):
       - Text appears readable
       - Not corrupted or garbled
       - Reasonable character distributions

    Overall Score:
        Average of all dimension scores

    Configuration:
    - needs_review_threshold (float): Score below which needs_review=True (default: 60.0)
    - empty_block_penalty (float): Penalty per empty block (default: 5.0)
    - low_confidence_threshold (float): Threshold for low confidence warning (default: 0.5)
    """

    def get_processor_name(self) -> str:
        """Return processor name."""
        return "QualityValidator"

    def is_optional(self) -> bool:
        """QualityValidator is optional - informational only."""
        return True

    def get_dependencies(self) -> list[str]:
        """Can benefit from MetadataAggregator but not required."""
        return []  # No strict dependencies

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """
        Process extracted content to validate quality.

        Args:
            extraction_result: Raw extraction result

        Returns:
            ProcessingResult with quality score and issues

        Processing Steps:
        1. Check for empty input (low score)
        2. Compute completeness score
        3. Compute consistency score
        4. Compute readability score
        5. Calculate overall quality score
        6. Identify specific issues
        7. Determine if review needed
        """
        # Handle empty input
        if not extraction_result.content_blocks:
            return ProcessingResult(
                content_blocks=tuple(),
                document_metadata=extraction_result.document_metadata,
                images=extraction_result.images,
                tables=extraction_result.tables,
                processing_stage=ProcessingStage.QUALITY_VALIDATION,
                stage_metadata={
                    "completeness_score": 0.0,
                    "consistency_score": 0.0,
                    "readability_score": 0.0,
                    "empty_blocks": 0,
                    "blocks_without_confidence": 0,
                    "readability_issues": 0,
                },
                quality_score=0.0,
                quality_issues=("Empty document - no content blocks found",),
                needs_review=True,
                success=True,
            )

        # Analyze content blocks
        blocks = extraction_result.content_blocks

        # Completeness analysis
        completeness_score, completeness_data = self._compute_completeness(blocks)

        # Consistency analysis
        consistency_score, consistency_data = self._compute_consistency(blocks)

        # Readability analysis
        readability_score, readability_data = self._compute_readability(blocks)

        # Calculate overall quality score (average of dimensions)
        quality_score = (completeness_score + consistency_score + readability_score) / 3.0

        # Collect quality issues
        issues = []

        if completeness_data["empty_blocks"] > 0:
            issues.append(f"{completeness_data['empty_blocks']} empty blocks found")

        if consistency_data["blocks_without_confidence"] > 0:
            issues.append(
                f"{consistency_data['blocks_without_confidence']} blocks without confidence scores"
            )

        if consistency_data["low_confidence_blocks"] > 0:
            issues.append(f"{consistency_data['low_confidence_blocks']} blocks with low confidence")

        if readability_data["suspicious_blocks"] > 0:
            issues.append(f"{readability_data['suspicious_blocks']} blocks with readability issues")

        # Determine if review needed
        review_threshold = self.config.get("needs_review_threshold", 60.0)
        needs_review = quality_score < review_threshold

        # Create enriched blocks (preserving all original data)
        enriched_blocks = []
        for block in blocks:
            # Add quality flag to metadata
            enriched_metadata = {
                **block.metadata,
                "quality_checked": True,
            }

            enriched_block = ContentBlock(
                block_id=block.block_id,
                block_type=block.block_type,
                content=block.content,
                raw_content=block.raw_content,
                position=block.position,
                parent_id=block.parent_id,
                related_ids=block.related_ids,
                metadata=enriched_metadata,
                confidence=block.confidence,
                style=block.style,
            )
            enriched_blocks.append(enriched_block)

        # Combine all metadata
        stage_metadata = {
            "completeness_score": completeness_score,
            "consistency_score": consistency_score,
            "readability_score": readability_score,
            **completeness_data,
            **consistency_data,
            **readability_data,
        }

        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            document_metadata=extraction_result.document_metadata,
            images=extraction_result.images,
            tables=extraction_result.tables,
            processing_stage=ProcessingStage.QUALITY_VALIDATION,
            stage_metadata=stage_metadata,
            quality_score=quality_score,
            quality_issues=tuple(issues),
            needs_review=needs_review,
            success=True,
        )

    def _compute_completeness(self, blocks: tuple[ContentBlock, ...]) -> tuple[float, dict]:
        """
        Compute completeness score.

        Checks for:
        - Presence of headings (structure)
        - Content type diversity
        - Empty blocks (penalty)

        Args:
            blocks: Content blocks to analyze

        Returns:
            Tuple of (score, analysis_data)
        """
        score = 100.0

        # Count content types
        has_headings = any(b.block_type == ContentType.HEADING for b in blocks)
        empty_blocks = sum(1 for b in blocks if not b.content.strip())

        # Unique content types
        content_types = set(b.block_type for b in blocks)
        type_diversity = len(content_types)

        # Penalties
        if not has_headings:
            score -= 20.0  # No structure

        empty_penalty = self.config.get("empty_block_penalty", 5.0)
        score -= empty_blocks * empty_penalty

        # Bonus for diversity
        if type_diversity >= 3:
            score += 10.0

        # Clamp score
        score = max(0.0, min(100.0, score))

        return score, {
            "has_headings": has_headings,
            "empty_blocks": empty_blocks,
            "content_type_diversity": type_diversity,
        }

    def _compute_consistency(self, blocks: tuple[ContentBlock, ...]) -> tuple[float, dict]:
        """
        Compute consistency score.

        Checks for:
        - Confidence scores present
        - Confidence scores reasonable
        - Metadata completeness

        Args:
            blocks: Content blocks to analyze

        Returns:
            Tuple of (score, analysis_data)
        """
        score = 100.0

        blocks_without_confidence = 0
        low_confidence_blocks = 0
        low_conf_threshold = self.config.get("low_confidence_threshold", 0.5)

        for block in blocks:
            if block.confidence is None:
                blocks_without_confidence += 1
                score -= 5.0  # Penalty for missing confidence
            elif block.confidence < low_conf_threshold:
                low_confidence_blocks += 1
                score -= 3.0  # Smaller penalty for low confidence

        # Clamp score
        score = max(0.0, min(100.0, score))

        return score, {
            "blocks_without_confidence": blocks_without_confidence,
            "low_confidence_blocks": low_confidence_blocks,
        }

    def _compute_readability(self, blocks: tuple[ContentBlock, ...]) -> tuple[float, dict]:
        """
        Compute readability score.

        Checks for:
        - Excessive special characters (corruption)
        - Very long words (potential gibberish)
        - Readable character distribution

        Args:
            blocks: Content blocks to analyze

        Returns:
            Tuple of (score, analysis_data)
        """
        score = 100.0
        suspicious_blocks = 0

        for block in blocks:
            if not block.content.strip():
                continue  # Skip empty blocks (handled in completeness)

            # Check for excessive special characters
            special_char_ratio = self._special_char_ratio(block.content)
            if special_char_ratio > 0.5:  # More than 50% special chars
                suspicious_blocks += 1
                score -= 10.0

            # Check for very long words (potential corruption)
            if self._has_abnormal_words(block.content):
                suspicious_blocks += 1
                score -= 5.0

        # Clamp score
        score = max(0.0, min(100.0, score))

        return score, {
            "suspicious_blocks": suspicious_blocks,
            "readability_issues": suspicious_blocks,
        }

    def _special_char_ratio(self, text: str) -> float:
        """
        Calculate ratio of special characters to total characters.

        Args:
            text: Text to analyze

        Returns:
            Ratio (0.0 to 1.0)
        """
        if not text:
            return 0.0

        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        return special_chars / len(text)

    def _has_abnormal_words(self, text: str) -> bool:
        """
        Check for abnormally long words (potential corruption).

        Args:
            text: Text to analyze

        Returns:
            True if abnormal words found
        """
        words = text.split()

        # Check for words longer than 30 characters (likely corrupted)
        for word in words:
            if len(word) > 30:
                return True

        return False
