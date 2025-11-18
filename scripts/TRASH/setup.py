"""
Setup script for AI Data Extractor package.

This is a fallback setup.py for compatibility with older build systems.
The primary packaging configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="ai-data-extractor",
    version="1.0.5",
    description="AI-ready file extraction tool for enterprise documents (DOCX, PDF, PPTX, XLSX)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrew",
    author_email="andrew@example.com",
    url="https://github.com/yourusername/ai-data-extractor",
    license="Proprietary",

    # Package discovery - find all packages in src directory
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # Python version requirement
    python_requires=">=3.11",

    # Dependencies
    install_requires=[
        "python-docx>=0.8.11",
        "pypdf>=3.0.0",
        "python-pptx>=0.6.21",
        "openpyxl>=3.0.10",
        "click>=8.1.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "PyYAML>=6.0.0",
        "pdfplumber>=0.10.0",
        "Pillow>=10.0.0",
    ],

    # Optional dependencies
    extras_require={
        "ocr": [
            "pytesseract>=0.3.10",
            "pdf2image>=1.16.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
    },

    # CLI entry points
    entry_points={
        "console_scripts": [
            "data-extract=cli.main:main",
        ],
    },

    # Include package data
    include_package_data=True,
    package_data={
        '*': ['*.yaml', '*.yml', '*.json', '*.txt'],
        'infrastructure': ['*.yaml', '*.yml', '*.json'],
        'cli': ['*.yaml', '*.yml', '*.json'],
        'formatters': ['*.yaml', '*.yml'],
        'extractors': ['*.yaml', '*.yml'],
        'processors': ['*.yaml', '*.yml'],
    },

    # Classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],

    # Keywords
    keywords="document-extraction ai-ready enterprise data-extraction pdf docx excel powerpoint",
)
