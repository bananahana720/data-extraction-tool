"""
MarkdownFormatter - Convert ProcessingResult to human-readable Markdown.

This formatter produces clean, readable Markdown output with:
- YAML frontmatter for document metadata
- Preserved heading hierarchy
- Proper formatting for lists, quotes, code blocks
- Markdown tables for structured data
- Image references with alt text

Design:
- Human-readable output (no UUIDs or technical details)
- Preserves document structure through heading hierarchy
- Configurable frontmatter and heading levels
- Clean, idiomatic markdown
"""

from pathlib import Path
from typing import Any

from core.interfaces import BaseFormatter
from core.models import (
    ContentBlock,
    ContentType,
    DocumentMetadata,
    FormattedOutput,
    ProcessingResult,
)


class MarkdownFormatter(BaseFormatter):
    """
    Format ProcessingResult as human-readable Markdown.

    Configuration Options:
        include_frontmatter (bool): Include YAML frontmatter (default: True)
        heading_offset (int): Offset for heading levels, 0-based (default: 0)
        include_metadata (bool): Include technical metadata comments (default: False)
        include_position_info (bool): Include page/position comments (default: False)

    Example:
        >>> formatter = MarkdownFormatter(config={"heading_offset": 1})
        >>> result = formatter.format(processing_result)
        >>> print(result.content)  # Clean markdown output
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize Markdown formatter.

        Args:
            config: Configuration options
        """
        super().__init__(config)

        # Extract configuration with defaults
        self.include_frontmatter = self.config.get("include_frontmatter", True)
        self.heading_offset = self.config.get("heading_offset", 0)
        self.include_metadata = self.config.get("include_metadata", False)
        self.include_position_info = self.config.get("include_position_info", False)

    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """
        Convert ProcessingResult to Markdown format.

        Args:
            processing_result: Result from processing stage

        Returns:
            FormattedOutput with Markdown content
        """
        try:
            # Build markdown sections
            sections = []

            # Add frontmatter if enabled
            if self.include_frontmatter:
                frontmatter = self._build_frontmatter(processing_result.document_metadata)
                if frontmatter:
                    sections.append(frontmatter)

            # Convert content blocks
            content = self._convert_blocks_to_markdown(processing_result.content_blocks)
            if content:
                sections.append(content)

            # Combine sections
            markdown_content = "\n\n".join(sections)

            return FormattedOutput(
                content=markdown_content,
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                success=True,
            )

        except Exception as e:
            return FormattedOutput(
                content="",
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                success=False,
                errors=(f"Markdown formatting failed: {str(e)}",),
            )

    def get_format_type(self) -> str:
        """
        Return format type identifier.

        Returns:
            "markdown"
        """
        return "markdown"

    def get_file_extension(self) -> str:
        """
        Return file extension for markdown.

        Returns:
            ".markdown"
        """
        return ".markdown"

    def _build_frontmatter(self, metadata: DocumentMetadata) -> str:
        """
        Build YAML frontmatter from document metadata.

        Args:
            metadata: Document metadata

        Returns:
            YAML frontmatter string or empty if no useful metadata
        """
        frontmatter_data = {}

        # Add key metadata fields
        if metadata.title:
            frontmatter_data["title"] = metadata.title

        if metadata.author:
            frontmatter_data["author"] = metadata.author

        if metadata.created_date:
            frontmatter_data["date"] = metadata.created_date.isoformat()

        if metadata.subject:
            frontmatter_data["subject"] = metadata.subject

        if metadata.keywords:
            frontmatter_data["keywords"] = list(metadata.keywords)

        if metadata.language:
            frontmatter_data["language"] = metadata.language

        # Add source info
        frontmatter_data["source"] = str(metadata.source_file.name)
        frontmatter_data["format"] = metadata.file_format

        # Build YAML frontmatter
        if frontmatter_data:
            lines = ["---"]
            for key, value in frontmatter_data.items():
                if isinstance(value, list):
                    lines.append(f"{key}:")
                    for item in value:
                        lines.append(f"  - {item}")
                else:
                    # Escape value if it contains special characters
                    if isinstance(value, str) and (":" in value or "#" in value):
                        value = f'"{value}"'
                    lines.append(f"{key}: {value}")
            lines.append("---")
            return "\n".join(lines)

        return ""

    def _convert_blocks_to_markdown(self, blocks: tuple[ContentBlock, ...]) -> str:
        """
        Convert content blocks to markdown.

        Args:
            blocks: Content blocks to convert

        Returns:
            Markdown string
        """
        if not blocks:
            return ""

        markdown_lines = []

        for block in blocks:
            # Add position comment if enabled
            if self.include_position_info and block.position:
                if block.position.page is not None:
                    markdown_lines.append(f"<!-- Page {block.position.page} -->")

            # Convert block based on type
            markdown = self._convert_block(block)
            if markdown:
                markdown_lines.append(markdown)

        return "\n\n".join(markdown_lines)

    def _convert_block(self, block: ContentBlock) -> str:
        """
        Convert a single content block to markdown.

        Args:
            block: Block to convert

        Returns:
            Markdown string
        """
        if block.block_type == ContentType.HEADING:
            return self._convert_heading(block)
        elif block.block_type == ContentType.PARAGRAPH:
            return self._convert_paragraph(block)
        elif block.block_type == ContentType.LIST_ITEM:
            return self._convert_list_item(block)
        elif block.block_type == ContentType.QUOTE:
            return self._convert_quote(block)
        elif block.block_type == ContentType.CODE:
            return self._convert_code(block)
        elif block.block_type == ContentType.TABLE:
            return self._convert_table(block)
        elif block.block_type == ContentType.IMAGE:
            return self._convert_image(block)
        else:
            # Default: plain text
            return block.content

    def _convert_heading(self, block: ContentBlock) -> str:
        """
        Convert heading block to markdown heading.

        Args:
            block: Heading block

        Returns:
            Markdown heading
        """
        # Determine heading level
        level = block.metadata.get("level", 1) if block.metadata else 1
        level = min(max(level + self.heading_offset, 1), 6)  # Clamp to 1-6

        # Build heading
        hashes = "#" * level
        return f"{hashes} {block.content}"

    def _convert_paragraph(self, block: ContentBlock) -> str:
        """
        Convert paragraph block to markdown.

        Args:
            block: Paragraph block

        Returns:
            Paragraph text
        """
        return block.content

    def _convert_list_item(self, block: ContentBlock) -> str:
        """
        Convert list item to markdown list.

        Args:
            block: List item block

        Returns:
            Markdown list item
        """
        # Use metadata to determine list type if available
        list_type = block.metadata.get("list_type", "bullet") if block.metadata else "bullet"

        if list_type == "numbered":
            return f"1. {block.content}"
        else:
            return f"- {block.content}"

    def _convert_quote(self, block: ContentBlock) -> str:
        """
        Convert quote block to markdown blockquote.

        Args:
            block: Quote block

        Returns:
            Markdown blockquote
        """
        # Handle multi-line quotes
        lines = block.content.split("\n")
        return "\n".join(f"> {line}" for line in lines)

    def _convert_code(self, block: ContentBlock) -> str:
        """
        Convert code block to fenced code block.

        Args:
            block: Code block

        Returns:
            Markdown fenced code block
        """
        # Extract language from metadata if available
        language = block.metadata.get("language", "") if block.metadata else ""

        # Build fenced code block
        return f"```{language}\n{block.content}\n```"

    def _convert_table(self, block: ContentBlock) -> str:
        """
        Convert table block to markdown table.

        Args:
            block: Table block

        Returns:
            Markdown table or reference
        """
        # For now, just reference the table
        # Full table rendering would require table metadata
        return f"**Table:** {block.content}"

    def _convert_image(self, block: ContentBlock) -> str:
        """
        Convert image block to markdown image reference.

        Args:
            block: Image block

        Returns:
            Markdown image syntax
        """
        # Extract alt text and path from metadata
        alt_text = block.metadata.get("alt_text", "") if block.metadata else ""
        image_path = block.metadata.get("image_path", "") if block.metadata else ""

        if not alt_text:
            # Use content as fallback
            alt_text = block.content

        if image_path:
            return f"![{alt_text}]({image_path})"
        else:
            # Just reference the image
            return f"**{block.content}**"
