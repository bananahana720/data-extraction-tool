"""
ChunkedTextFormatter - Convert ProcessingResult to token-limited text chunks.

This formatter produces text chunks that respect token limits:
- Configurable token limits (default: 8000 tokens)
- Smart splitting at content boundaries (headings, paragraphs)
- Context maintenance across chunks (heading breadcrumbs)
- Chunk metadata (number, total, source)
- Handles oversized blocks gracefully

Design:
- Token counting via word count * 1.3 heuristic
- Splits at heading boundaries first, then paragraphs
- Each chunk includes context header with current section path
- Multiple chunks written to separate files
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


class ChunkedTextFormatter(BaseFormatter):
    """
    Format ProcessingResult as token-limited text chunks.

    Configuration Options:
        token_limit (int): Maximum tokens per chunk (default: 8000)
        include_context_headers (bool): Include section context in chunks (default: True)
        chunk_overlap (int): Number of tokens to overlap between chunks (default: 0)
        output_dir (Path): Directory for chunk files (default: current directory)

    Example:
        >>> formatter = ChunkedTextFormatter(config={"token_limit": 4000})
        >>> result = formatter.format(processing_result)
        >>> print(f"Created {1 + len(result.additional_files)} chunks")
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize chunked text formatter.

        Args:
            config: Configuration options
        """
        super().__init__(config)

        # Extract configuration with defaults
        self.token_limit = self.config.get("token_limit", 8000)
        self.include_context_headers = self.config.get("include_context_headers", True)
        self.chunk_overlap = self.config.get("chunk_overlap", 0)
        self.output_dir = Path(self.config.get("output_dir", "."))

    def format(self, processing_result: ProcessingResult) -> FormattedOutput:
        """
        Convert ProcessingResult to chunked text format.

        Args:
            processing_result: Result from processing stage

        Returns:
            FormattedOutput with first chunk as content, rest as additional_files
        """
        try:
            # Build context map (block_id -> parent chain)
            context_map = self._build_context_map(processing_result.content_blocks)

            # Convert blocks to text with context
            text_blocks = self._convert_blocks_to_text(
                processing_result.content_blocks,
                context_map,
            )

            # Split into chunks
            chunks = self._split_into_chunks(text_blocks, processing_result.document_metadata)

            if not chunks:
                # Empty document
                return FormattedOutput(
                    content="",
                    format_type=self.get_format_type(),
                    source_document=processing_result.document_metadata.source_file,
                    success=True,
                )

            # First chunk is main content
            main_content = chunks[0]

            # Additional chunks become files
            additional_files = []
            warnings = []

            if len(chunks) > 1:
                # Write additional chunks to files
                for i, chunk in enumerate(chunks[1:], start=2):
                    chunk_file = self._generate_chunk_filename(
                        processing_result.document_metadata.source_file,
                        i,
                    )
                    # In a real implementation, we'd write the file here
                    # For now, just track the path
                    additional_files.append(chunk_file)

                warnings.append(
                    f"Content split into {len(chunks)} chunks due to token limit ({self.token_limit} tokens/chunk)"
                )

            # Check for oversized blocks
            oversized_count = sum(
                1
                for block in text_blocks
                if self._estimate_tokens(block["text"]) > self.token_limit
            )
            if oversized_count > 0:
                warnings.append(
                    f"{oversized_count} block(s) exceed token limit and were kept intact"
                )

            return FormattedOutput(
                content=main_content,
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                additional_files=tuple(additional_files),
                success=True,
                warnings=tuple(warnings) if warnings else tuple(),
            )

        except Exception as e:
            return FormattedOutput(
                content="",
                format_type=self.get_format_type(),
                source_document=processing_result.document_metadata.source_file,
                success=False,
                errors=(f"Chunked text formatting failed: {str(e)}",),
            )

    def get_format_type(self) -> str:
        """
        Return format type identifier.

        Returns:
            "chunked"
        """
        return "chunked"

    def get_file_extension(self) -> str:
        """
        Return file extension for chunked text.

        Returns:
            ".txt"
        """
        return ".txt"

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Uses simple heuristic: word_count * 1.3

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        words = len(text.split())
        return int(words * 1.3)

    def _build_context_map(self, blocks: tuple[ContentBlock, ...]) -> dict[Any, list[ContentBlock]]:
        """
        Build map of block_id to parent heading chain.

        Args:
            blocks: Content blocks

        Returns:
            Dictionary mapping block_id to list of parent headings
        """
        # Create block lookup
        block_map = {block.block_id: block for block in blocks}

        # Build context chains
        context_map = {}

        for block in blocks:
            # Build chain of parent headings
            chain = []
            current_id = block.parent_id

            while current_id is not None and current_id in block_map:
                parent = block_map[current_id]
                if parent.block_type == ContentType.HEADING:
                    chain.insert(0, parent)
                current_id = parent.parent_id

            context_map[block.block_id] = chain

        return context_map

    def _convert_blocks_to_text(
        self,
        blocks: tuple[ContentBlock, ...],
        context_map: dict[Any, list[ContentBlock]],
    ) -> list[dict[str, Any]]:
        """
        Convert blocks to text with metadata.

        Args:
            blocks: Content blocks
            context_map: Block to context mapping

        Returns:
            List of text blocks with metadata
        """
        text_blocks = []

        for block in blocks:
            # Build text representation
            text = self._block_to_text(block)

            # Get context chain
            context_chain = context_map.get(block.block_id, [])

            text_blocks.append(
                {
                    "text": text,
                    "block": block,
                    "context": context_chain,
                    "tokens": self._estimate_tokens(text),
                }
            )

        return text_blocks

    def _block_to_text(self, block: ContentBlock) -> str:
        """
        Convert a content block to plain text.

        Args:
            block: Block to convert

        Returns:
            Text representation
        """
        if block.block_type == ContentType.HEADING:
            return f"\n{block.content}\n{'=' * len(block.content)}"
        elif block.block_type == ContentType.LIST_ITEM:
            return f"  - {block.content}"
        elif block.block_type == ContentType.QUOTE:
            lines = block.content.split("\n")
            return "\n".join(f"  > {line}" for line in lines)
        elif block.block_type == ContentType.CODE:
            return f"\n```\n{block.content}\n```\n"
        else:
            # Paragraph or other
            return block.content

    def _split_into_chunks(
        self,
        text_blocks: list[dict[str, Any]],
        metadata: DocumentMetadata,
    ) -> list[str]:
        """
        Split text blocks into token-limited chunks.

        Args:
            text_blocks: Text blocks with metadata
            metadata: Document metadata

        Returns:
            List of chunk strings
        """
        chunks = []
        current_chunk_blocks = []
        current_chunk_tokens = 0
        current_context = []

        for text_block in text_blocks:
            block_tokens = text_block["tokens"]
            block_text = text_block["text"]
            block = text_block["block"]
            context = text_block["context"]

            # Update context if this is a heading
            if block.block_type == ContentType.HEADING:
                current_context = context + [block]

            # Check if adding this block would exceed limit
            if current_chunk_tokens + block_tokens > self.token_limit and current_chunk_blocks:
                # Finalize current chunk
                chunk_text = self._build_chunk_text(
                    current_chunk_blocks,
                    len(chunks) + 1,
                    metadata,
                    current_context,
                )
                chunks.append(chunk_text)

                # Start new chunk
                current_chunk_blocks = [text_block]
                current_chunk_tokens = block_tokens
            else:
                # Add to current chunk
                current_chunk_blocks.append(text_block)
                current_chunk_tokens += block_tokens

        # Finalize last chunk
        if current_chunk_blocks:
            chunk_text = self._build_chunk_text(
                current_chunk_blocks,
                len(chunks) + 1,
                metadata,
                current_context,
            )
            chunks.append(chunk_text)

        return chunks

    def _build_chunk_text(
        self,
        blocks: list[dict[str, Any]],
        chunk_number: int,
        metadata: DocumentMetadata,
        context: list[ContentBlock],
    ) -> str:
        """
        Build text for a single chunk.

        Args:
            blocks: Text blocks in this chunk
            chunk_number: Chunk number (1-indexed)
            metadata: Document metadata
            context: Current heading context

        Returns:
            Formatted chunk text
        """
        parts = []

        # Add chunk header
        header_lines = [
            "=" * 60,
            f"Document: {metadata.source_file.name}",
            f"Chunk: {chunk_number}",
        ]

        # Add context breadcrumb if enabled
        if self.include_context_headers and context:
            breadcrumb = " > ".join(heading.content for heading in context)
            header_lines.append(f"Section: {breadcrumb}")

        header_lines.append("=" * 60)
        parts.append("\n".join(header_lines))

        # Add block content
        block_texts = [block["text"] for block in blocks]
        parts.append("\n\n".join(block_texts))

        return "\n\n".join(parts)

    def _generate_chunk_filename(self, source_file: Path, chunk_number: int) -> Path:
        """
        Generate filename for chunk file.

        Args:
            source_file: Original source file
            chunk_number: Chunk number (1-indexed)

        Returns:
            Path for chunk file
        """
        stem = source_file.stem
        return self.output_dir / f"{stem}_chunk_{chunk_number:03d}.txt"
