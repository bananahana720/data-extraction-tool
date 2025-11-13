"""
Pipeline Package - Orchestrates Extraction Workflow.

This package provides the main pipeline orchestrator and batch processing
capabilities for the data extraction tool.

Public API:
    ExtractionPipeline - Main pipeline orchestrator
    BatchProcessor - Parallel batch file processing
"""

from .batch_processor import BatchProcessor
from .extraction_pipeline import ExtractionPipeline

__all__ = [
    "ExtractionPipeline",
    "BatchProcessor",
]
