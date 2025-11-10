"""
CLI entry point for python -m cli execution.

This module enables the CLI to be run as:
    python -m cli extract <file>
    python -m cli batch <directory>
    python -m cli --version
"""

from .main import cli

if __name__ == "__main__":
    cli()
