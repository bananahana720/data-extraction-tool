"""
JsonFormatter - Convert ProcessingResult to hierarchical JSON.

This formatter produces structured JSON output with:
- Hierarchical or flat content block structure
- Complete metadata preservation
- Configurable formatting (pretty-print, indentation)
- Type-safe serialization of enums and dataclasses

Design:
- Supports both hierarchical and flat JSON structures
- Preserves all metadata and position information
- Handles Unicode content properly
- Configurable via BaseFormatter config pattern
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from core.interfaces import BaseFormatter
from core.models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    FormattedOutput,
    Position,
    ProcessingResult,
)


class JsonFormatter(BaseFormatter):
    """
    Format ProcessingResult as hierarchical JSON.

    Configuration Options:
        hierarchical (bool): Build nested structure based on parent_id (default: False)
        pretty_print (bool): Pretty-print JSON with indentation (default: True)
        indent (int): Number of spaces for indentation (default: 2)
        ensure_ascii (bool): Escape non-ASCII characters (default: False)

    Example:
        >>> formatter = JsonFormatter(config={"pretty_print": True, "indent": 4})
        >>> result = formatter.format(processing_result)
        >>> print(result.content)  # Pretty JSON output
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize JSON formatter.

        Args:
            config: Configuration options
        """
        super().__init__(config)

        # Extract configuration with defaults
        self.hierarchical = self.config.get("hierarchical", False)
        self.pretty_print = self.config.get("pretty_print", True)
        self.indent = self.config.get("indent", 2)
        self.ensure_ascii = self.config.get("ensure_ascii", False)

    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """
        Convert ProcessingResult to JSON format.

        Args:
            processing_result: Result from processing stage

        Returns:
            FormattedOutput with JSON content
        """
        try:
            # Build JSON structure
            json_data = self._build_json_structure(processing_result)

            # Serialize to JSON string
            if self.pretty_print:
                content = json.dumps(
                    json_data,
                    indent=self.indent,
                    ensure_ascii=self.ensure_ascii,
                    default=self._json_serializer,
                )
            else:
                content = json.dumps(
                    json_data,
                    ensure_ascii=self.ensure_ascii,
                    default=self._json_serializer,
                )

            return FormattedOutput(
                content=content,
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                success=True,
            )

        except Exception as e:
            return FormattedOutput(
                content="{}",
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                success=False,
                errors=(f"JSON formatting failed: {str(e)}",),
            )

    def get_format_type(self) -> str:
        """
        Return format type identifier.

        Returns:
            "json"
        """
        return "json"

    def _build_json_structure(self, processing_result: ProcessingResult) -> dict[str, Any]:
        """
        Build JSON data structure from ProcessingResult.

        Args:
            processing_result: Result to convert

        Returns:
            Dictionary ready for JSON serialization
        """
        # Convert content blocks
        if self.hierarchical:
            content_blocks = self._build_hierarchical_blocks(processing_result.content_blocks)
        else:
            content_blocks = [
                self._serialize_content_block(block) for block in processing_result.content_blocks
            ]

        # Build complete structure
        json_data = {
            "content_blocks": content_blocks,
            "document_metadata": self._serialize_document_metadata(
                processing_result.document_metadata
            ),
        }

        # Add media assets if present
        if processing_result.tables:
            json_data["tables"] = [
                self._serialize_table_metadata(table) for table in processing_result.tables
            ]

        if processing_result.images:
            json_data["images"] = [
                self._serialize_image_metadata(image) for image in processing_result.images
            ]

        # Add processing metadata if available
        if processing_result.processing_stage:
            json_data["processing_stage"] = processing_result.processing_stage.value

        if processing_result.quality_score is not None:
            json_data["quality_score"] = processing_result.quality_score

        # Add errors and warnings if present
        if processing_result.errors:
            json_data["processing_errors"] = list(processing_result.errors)

        if processing_result.warnings:
            json_data["processing_warnings"] = list(processing_result.warnings)

        # Add success status
        json_data["processing_success"] = processing_result.success

        return json_data

    def _build_hierarchical_blocks(self, blocks: tuple[ContentBlock, ...]) -> list[dict[str, Any]]:
        """
        Build hierarchical block structure based on parent_id.

        Args:
            blocks: Flat tuple of content blocks

        Returns:
            List of blocks with children nested
        """
        # Create mapping of block_id to block
        block_map = {block.block_id: block for block in blocks}

        # Create mapping of parent_id to children
        children_map: dict[UUID | None, list[ContentBlock]] = {}
        for block in blocks:
            parent_id = block.parent_id
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(block)

        # Build tree starting from root nodes (parent_id = None)
        root_blocks = children_map.get(None, [])
        return [self._serialize_block_with_children(block, children_map) for block in root_blocks]

    def _serialize_block_with_children(
        self, block: ContentBlock, children_map: dict[UUID | None, list[ContentBlock]]
    ) -> dict[str, Any]:
        """
        Serialize a block with its children nested.

        Args:
            block: Block to serialize
            children_map: Mapping of parent_id to children

        Returns:
            Dictionary with nested children
        """
        block_dict = self._serialize_content_block(block)

        # Add children if any
        children = children_map.get(block.block_id, [])
        if children:
            block_dict["children"] = [
                self._serialize_block_with_children(child, children_map) for child in children
            ]

        return block_dict

    def _serialize_content_block(self, block: ContentBlock) -> dict[str, Any]:
        """
        Serialize a ContentBlock to dictionary.

        Args:
            block: Block to serialize

        Returns:
            Dictionary representation
        """
        block_dict = {
            "block_id": str(block.block_id),
            "block_type": block.block_type.value,
            "content": block.content,
        }

        # Add optional fields if present
        if block.raw_content:
            block_dict["raw_content"] = block.raw_content

        if block.position:
            block_dict["position"] = self._serialize_position(block.position)

        if block.parent_id:
            block_dict["parent_id"] = str(block.parent_id)

        if block.related_ids:
            block_dict["related_ids"] = [str(rid) for rid in block.related_ids]

        if block.metadata:
            block_dict["metadata"] = block.metadata

        if block.confidence is not None:
            block_dict["confidence"] = block.confidence

        if block.style:
            block_dict["style"] = block.style

        return block_dict

    def _serialize_position(self, position: Position) -> dict[str, Any]:
        """
        Serialize Position to dictionary.

        Args:
            position: Position to serialize

        Returns:
            Dictionary representation
        """
        pos_dict = {}

        if position.page is not None:
            pos_dict["page"] = position.page

        if position.slide is not None:
            pos_dict["slide"] = position.slide

        if position.sheet is not None:
            pos_dict["sheet"] = position.sheet

        if position.x is not None:
            pos_dict["x"] = position.x

        if position.y is not None:
            pos_dict["y"] = position.y

        if position.width is not None:
            pos_dict["width"] = position.width

        if position.height is not None:
            pos_dict["height"] = position.height

        if position.sequence_index is not None:
            pos_dict["sequence_index"] = position.sequence_index

        return pos_dict

    def _serialize_document_metadata(self, metadata: DocumentMetadata) -> dict[str, Any]:
        """
        Serialize DocumentMetadata to dictionary.

        Args:
            metadata: Metadata to serialize

        Returns:
            Dictionary representation
        """
        meta_dict = {
            "source_file": str(metadata.source_file),
            "file_format": metadata.file_format,
            "file_size_bytes": metadata.file_size_bytes,
        }

        # Add optional fields if present
        if metadata.file_hash:
            meta_dict["file_hash"] = metadata.file_hash

        if metadata.title:
            meta_dict["title"] = metadata.title

        if metadata.author:
            meta_dict["author"] = metadata.author

        if metadata.created_date:
            meta_dict["created_date"] = metadata.created_date.isoformat()

        if metadata.modified_date:
            meta_dict["modified_date"] = metadata.modified_date.isoformat()

        if metadata.subject:
            meta_dict["subject"] = metadata.subject

        if metadata.keywords:
            meta_dict["keywords"] = list(metadata.keywords)

        if metadata.page_count is not None:
            meta_dict["page_count"] = metadata.page_count

        if metadata.word_count is not None:
            meta_dict["word_count"] = metadata.word_count

        if metadata.character_count is not None:
            meta_dict["character_count"] = metadata.character_count

        if metadata.image_count:
            meta_dict["image_count"] = metadata.image_count

        if metadata.table_count:
            meta_dict["table_count"] = metadata.table_count

        if metadata.language:
            meta_dict["language"] = metadata.language

        if metadata.content_summary:
            meta_dict["content_summary"] = metadata.content_summary

        meta_dict["extracted_at"] = metadata.extracted_at.isoformat()

        if metadata.extractor_version:
            meta_dict["extractor_version"] = metadata.extractor_version

        if metadata.extraction_duration_seconds is not None:
            meta_dict["extraction_duration_seconds"] = metadata.extraction_duration_seconds

        return meta_dict

    def _serialize_table_metadata(self, table: Any) -> dict[str, Any]:
        """
        Serialize TableMetadata to dictionary.

        Args:
            table: TableMetadata to serialize

        Returns:
            Dictionary representation
        """
        table_dict = {
            "table_id": str(table.table_id),
            "num_rows": table.num_rows,
            "num_columns": table.num_columns,
            "has_header": table.has_header,
        }

        if table.header_row:
            table_dict["header_row"] = list(table.header_row)

        if table.cells:
            table_dict["cells"] = [list(row) for row in table.cells]

        return table_dict

    def _serialize_image_metadata(self, image: Any) -> dict[str, Any]:
        """
        Serialize ImageMetadata to dictionary.

        Args:
            image: ImageMetadata to serialize

        Returns:
            Dictionary representation
        """
        image_dict = {
            "image_id": str(image.image_id),
        }

        # Add optional fields if present
        if image.file_path:
            image_dict["file_path"] = str(image.file_path)

        if image.format:
            image_dict["format"] = image.format

        if image.width is not None:
            image_dict["width"] = image.width

        if image.height is not None:
            image_dict["height"] = image.height

        if image.color_mode:
            image_dict["color_mode"] = image.color_mode

        if image.dpi:
            image_dict["dpi"] = image.dpi

        if image.alt_text:
            image_dict["alt_text"] = image.alt_text

        if image.caption:
            image_dict["caption"] = image.caption

        if image.image_type:
            image_dict["image_type"] = image.image_type

        if image.content_hash:
            image_dict["content_hash"] = image.content_hash

        if image.is_low_quality:
            image_dict["is_low_quality"] = image.is_low_quality

        if image.quality_issues:
            image_dict["quality_issues"] = list(image.quality_issues)

        return image_dict

    def _json_serializer(self, obj: Any) -> Any:
        """
        Custom JSON serializer for non-standard types.

        Args:
            obj: Object to serialize

        Returns:
            Serializable representation

        Raises:
            TypeError: If object type is not supported
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, ContentType):
            return obj.value
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
