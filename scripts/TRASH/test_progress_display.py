"""
Test script for CLI progress display integration.

Tests both single-file and batch progress displays with simulated
progress updates to verify visual output and performance.

Usage:
    python scripts/test_progress_display.py --mode single
    python scripts/test_progress_display.py --mode batch
    python scripts/test_progress_display.py --mode both
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli.progress_display import SingleFileProgress, BatchProgress
from rich.console import Console


def test_single_file_progress(verbose: bool = False):
    """Test single file progress display."""
    console = Console()
    console.print("\n[bold]Testing Single File Progress[/bold]\n")

    file_path = Path("test_document.docx")

    with SingleFileProgress(
        file_path=file_path,
        console=console,
        verbose=verbose,
        quiet=False
    ) as progress:
        # Simulate extraction stage (0-40%)
        for i in range(5):
            progress.update({
                'stage': 'extraction',
                'percentage': i * 8,
                'message': f'Extracting block {i+1}/5'
            })
            time.sleep(0.2)

        # Simulate processing stage (40-70%)
        for i in range(4):
            progress.update({
                'stage': 'processing',
                'percentage': 40 + i * 7.5,
                'message': f'Running processor {i+1}/4'
            })
            time.sleep(0.2)

        # Simulate formatting stage (70-100%)
        for i in range(3):
            progress.update({
                'stage': 'formatting',
                'percentage': 70 + i * 10,
                'message': f'Generating format {i+1}/3'
            })
            time.sleep(0.2)

        # Complete
        progress.update({
            'stage': 'complete',
            'percentage': 100,
            'message': 'Processing complete'
        })

    console.print("\n[green]SUCCESS: Single file progress test complete[/green]\n")


def test_batch_progress(verbose: bool = False):
    """Test batch progress display."""
    console = Console()
    console.print("\n[bold]Testing Batch Progress[/bold]\n")

    # Create test file list
    files = [
        Path(f"document{i}.docx") for i in range(1, 6)
    ]

    with BatchProgress(
        file_paths=files,
        console=console,
        verbose=verbose,
        quiet=False
    ) as progress:
        # Simulate processing each file
        for idx, file_path in enumerate(files):
            # Start file
            progress.update({
                'current_file': file_path.name,
                'stage': 'extraction',
                'percentage': 0,
                'items_processed': idx
            })
            time.sleep(0.1)

            # Process stages for file
            for stage_pct in [25, 50, 75, 100]:
                stage_name = (
                    'extraction' if stage_pct <= 40 else
                    'processing' if stage_pct <= 70 else
                    'formatting'
                )
                progress.update({
                    'current_file': file_path.name,
                    'stage': stage_name,
                    'percentage': stage_pct,
                    'items_processed': idx if stage_pct < 100 else idx + 1
                })
                time.sleep(0.1)

            # Mark complete
            if idx == 2:
                # Simulate one failure
                progress.mark_file_failed(file_path, "Simulated error for testing")
            else:
                progress.mark_file_complete(file_path, success=True)

        # Show summary table
        table = progress.get_summary_table()
        console.print("\n")
        console.print(table)

    console.print("\n[green]SUCCESS: Batch progress test complete[/green]\n")


def main():
    """Main test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Test CLI progress displays")
    parser.add_argument(
        '--mode',
        choices=['single', 'batch', 'both'],
        default='both',
        help='Which progress mode to test'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    try:
        if args.mode in ('single', 'both'):
            test_single_file_progress(verbose=args.verbose)

        if args.mode in ('batch', 'both'):
            test_batch_progress(verbose=args.verbose)

        print("\nSUCCESS: All progress display tests passed!\n")
        return 0

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        return 130

    except Exception as e:
        print(f"\nERROR: Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
