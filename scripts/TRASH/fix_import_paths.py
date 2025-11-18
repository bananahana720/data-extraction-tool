"""
Fix import paths in test files to match source code convention.

Changes all imports from 'from src.X' to 'from X' to ensure Python
treats them as the same modules (avoiding isinstance() failures).
"""
import re
from pathlib import Path
import sys


def fix_imports_in_file(file_path):
    """Fix import paths in a single test file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace patterns - order matters (most specific first)
    patterns = [
        (r'from src\.core\.', 'from core.'),
        (r'from src\.pipeline\.', 'from pipeline.'),
        (r'from src\.infrastructure\.', 'from infrastructure.'),
        (r'from src\.formatters\.', 'from formatters.'),
        (r'from src\.extractors\.', 'from extractors.'),
        (r'from src\.processors\.', 'from processors.'),
        (r'from src\.cli\.', 'from cli.'),
        (r'import src\.core\.', 'import core.'),
        (r'import src\.pipeline\.', 'import pipeline.'),
        (r'import src\.infrastructure\.', 'import infrastructure.'),
        (r'import src\.formatters\.', 'import formatters.'),
        (r'import src\.extractors\.', 'import extractors.'),
        (r'import src\.processors\.', 'import processors.'),
        (r'import src\.cli\.', 'import cli.'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Only write if changes made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_imports_in_directory(directory):
    """Fix imports in all .py files in directory."""
    directory = Path(directory)
    modified_files = []

    for py_file in directory.rglob('*.py'):
        # Skip __pycache__ and other non-test files
        if '__pycache__' in str(py_file):
            continue
        if fix_imports_in_file(py_file):
            modified_files.append(py_file)

    return modified_files


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_import_paths.py <directory>")
        print("Example: python fix_import_paths.py tests/integration")
        sys.exit(1)

    directory = sys.argv[1]
    modified = fix_imports_in_directory(directory)

    print(f"Modified {len(modified)} files in {directory}")
    for f in modified:
        print(f"  - {f}")

    return len(modified)


if __name__ == '__main__':
    main()
