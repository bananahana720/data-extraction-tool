"""
ContextLinker Processor - Build Hierarchical Document Structure

This processor creates a tree structure from flat content blocks by:
- Detecting heading hierarchy (H1 > H2 > H3...)
- Linking paragraphs and other content to their parent headings
- Computing depth information for each block
- Generating document paths (breadcrumb trails)

Example Structure:
    Chapter 1 (H1, depth=0)
    ├─ Section 1.1 (H2, depth=1, parent=Chapter 1)
    │  ├─ Paragraph (depth=2, parent=Section 1.1)
    │  └─ Table (depth=2, parent=Section 1.1)
    └─ Section 1.2 (H2, depth=1, parent=Chapter 1)
       └─ Paragraph (depth=2, parent=Section 1.2)

Design:
- Immutable: Creates new ContentBlocks instead of modifying
- Incremental: Single pass through content blocks
- Robust: Handles missing metadata, malformed hierarchies
"""

from typing import Optional

from core import (
    BaseProcessor,
    ContentBlock,
    ContentType,
    ExtractionResult,
    ProcessingResult,
    ProcessingStage,
)


class ContextLinker(BaseProcessor):
    """
    Build hierarchical document structure from flat content blocks.

    This processor enriches content blocks with:
    - parent_id: Links to parent heading (if any)
    - depth: Nesting depth in document hierarchy
    - document_path: List of heading titles from root to this block

    Algorithm:
    1. Maintain heading stack (tracks current heading at each level)
    2. For each block:
       - If heading: Update stack at that level, clear deeper levels
       - If content: Link to most recent heading
    3. Compute depth based on hierarchy position
    4. Generate document path by walking up parent chain

    Configuration:
    - max_depth (int): Maximum nesting depth to track (default: 10)
    - include_path (bool): Include document_path in metadata (default: True)
    """

    def get_processor_name(self) -> str:
        """Return processor name."""
        return "ContextLinker"

    def is_optional(self) -> bool:
        """ContextLinker is required for downstream processors."""
        return False

    def get_dependencies(self) -> list[str]:
        """ContextLinker has no dependencies - runs first."""
        return []

    def process(self, extraction_result: ExtractionResult) -> ProcessingResult:
        """
        Process extracted content to build document hierarchy.

        Args:
            extraction_result: Raw extraction result

        Returns:
            ProcessingResult with enriched content blocks

        Processing Steps:
        1. Handle empty input gracefully
        2. Build heading stack while processing blocks
        3. Enrich each block with hierarchy metadata
        4. Compute statistics for stage_metadata
        """
        # Handle empty input
        if not extraction_result.content_blocks:
            return ProcessingResult(
                content_blocks=tuple(),
                document_metadata=extraction_result.document_metadata,
                images=extraction_result.images,
                tables=extraction_result.tables,
                processing_stage=ProcessingStage.CONTEXT_LINKING,
                stage_metadata={
                    "blocks_processed": 0,
                    "heading_count": 0,
                    "max_depth": 0,
                },
                success=True,
            )

        # Build hierarchy
        enriched_blocks = []
        heading_stack = {}  # Maps level -> (block_id, title)
        max_depth = 0
        heading_count = 0

        for block in extraction_result.content_blocks:
            # Determine if this is a heading
            is_heading = block.block_type == ContentType.HEADING
            heading_level = block.metadata.get("level", 1) if is_heading else None

            # Process based on block type
            if is_heading:
                heading_count += 1

                # Update heading stack
                heading_stack[heading_level] = (block.block_id, block.content)

                # Clear deeper levels
                levels_to_remove = [l for l in heading_stack.keys() if l > heading_level]
                for level in levels_to_remove:
                    del heading_stack[level]

                # Find parent (closest higher-level heading)
                parent_id = self._find_parent_heading(heading_stack, heading_level)

                # Compute depth
                depth = heading_level - 1 if heading_level else 0

                # Build document path
                document_path = self._build_document_path(heading_stack, heading_level)

            else:
                # Content block - link to most recent heading
                parent_id = self._find_current_parent(heading_stack)

                # Compute depth (one level deeper than parent)
                depth = self._compute_depth(heading_stack)

                # Build document path
                document_path = self._build_full_document_path(heading_stack)

            # Track max depth
            max_depth = max(max_depth, depth)

            # Create enriched block
            enriched_metadata = {
                **block.metadata,
                "depth": depth,
            }

            # Add document path if configured
            if self.config.get("include_path", True):
                enriched_metadata["document_path"] = document_path

            enriched_block = ContentBlock(
                block_id=block.block_id,  # Preserve original ID
                block_type=block.block_type,
                content=block.content,
                raw_content=block.raw_content,
                position=block.position,
                parent_id=parent_id,
                related_ids=block.related_ids,
                metadata=enriched_metadata,
                confidence=block.confidence,
                style=block.style,
            )

            enriched_blocks.append(enriched_block)

        # Create result
        return ProcessingResult(
            content_blocks=tuple(enriched_blocks),
            document_metadata=extraction_result.document_metadata,
            images=extraction_result.images,
            tables=extraction_result.tables,
            processing_stage=ProcessingStage.CONTEXT_LINKING,
            stage_metadata={
                "blocks_processed": len(enriched_blocks),
                "heading_count": heading_count,
                "max_depth": max_depth,
            },
            success=True,
        )

    def _find_parent_heading(self, heading_stack: dict, current_level: int) -> Optional:
        """
        Find parent heading for a heading block.

        Parent is the most recent heading at a higher level.
        If no higher-level heading exists, returns None (root-level).

        Args:
            heading_stack: Current heading stack
            current_level: Level of current heading

        Returns:
            Block ID of parent heading, or None if root
        """
        # Find closest higher-level heading
        parent_levels = [l for l in heading_stack.keys() if l < current_level]

        if not parent_levels:
            return None

        parent_level = max(parent_levels)
        parent_id, _ = heading_stack[parent_level]
        return parent_id

    def _find_current_parent(self, heading_stack: dict) -> Optional:
        """
        Find parent heading for a content block.

        Parent is the most recent heading at any level.

        Args:
            heading_stack: Current heading stack

        Returns:
            Block ID of parent heading, or None if no headings
        """
        if not heading_stack:
            return None

        # Get most recent heading (highest level number in stack)
        deepest_level = max(heading_stack.keys())
        parent_id, _ = heading_stack[deepest_level]
        return parent_id

    def _compute_depth(self, heading_stack: dict) -> int:
        """
        Compute depth for a content block.

        Depth is one level deeper than the current heading level.

        Args:
            heading_stack: Current heading stack

        Returns:
            Depth value (0 if no headings, else level of deepest heading + 1)
        """
        if not heading_stack:
            return 0

        deepest_level = max(heading_stack.keys())
        # Content is one level deeper than its parent heading
        # For H1 (level 1), depth = 1; for H2 (level 2), depth = 2, etc.
        return deepest_level

    def _build_document_path(self, heading_stack: dict, current_level: int) -> list[str]:
        """
        Build document path for a heading block.

        Path includes all ancestor headings but not the current heading itself.

        Args:
            heading_stack: Current heading stack
            current_level: Level of current heading

        Returns:
            List of heading titles from root to parent
        """
        path = []

        # Include all headings at higher levels
        for level in sorted(heading_stack.keys()):
            if level < current_level:
                _, title = heading_stack[level]
                path.append(title)

        return path

    def _build_full_document_path(self, heading_stack: dict) -> list[str]:
        """
        Build complete document path for a content block.

        Path includes all ancestor headings.

        Args:
            heading_stack: Current heading stack

        Returns:
            List of heading titles from root to current parent
        """
        path = []

        # Include all headings in order
        for level in sorted(heading_stack.keys()):
            _, title = heading_stack[level]
            path.append(title)

        return path
