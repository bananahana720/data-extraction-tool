#!/bin/bash
# Create Enhanced Development Package
# This creates a comprehensive dev package with tests, docs, and extras

set -e

echo "Creating enhanced development package..."

# Create temp directory
DEV_DIR="dev-package-temp"
mkdir -p "$DEV_DIR/ai_data_extractor-1.0.0-dev"
cd "$DEV_DIR/ai_data_extractor-1.0.0-dev"

# Copy source distribution contents
echo "Extracting source distribution..."
tar -xzf ../../dist/ai_data_extractor-1.0.0.tar.gz --strip-components=1

# Add tests
echo "Adding test suite..."
cp -r ../../tests ./

# Add pytest configuration
cp ../../pytest.ini ./

# Add additional documentation
echo "Adding development documentation..."
mkdir -p docs/development
cp ../../docs/architecture/FOUNDATION.md ./docs/development/ 2>/dev/null || true
cp ../../docs/guides/INFRASTRUCTURE_GUIDE.md ./docs/development/ 2>/dev/null || true
cp ../../docs/USER_GUIDE.md ./docs/ 2>/dev/null || true

# Add examples
echo "Adding examples..."
mkdir -p examples
cp -r ../../examples/* ./examples/ 2>/dev/null || true

# Create DEV_README.md
echo "Creating development README..."
cat > DEV_README.md << 'EOFREADME'
# AI Data Extractor - Development Package v1.0.0

This is the comprehensive development package for AI Data Extractor, including source code, tests, documentation, and examples.

## Package Contents

- **src/** - Complete source code for all modules
- **tests/** - Full test suite (525+ tests, 92%+ coverage)
- **docs/** - User guide and development documentation
- **examples/** - Example scripts and workflows
- **pytest.ini** - Test configuration
- **config.yaml.example** - Configuration template

## Quick Start

### 1. Extract Package
```bash
tar -xzf ai_data_extractor-1.0.0-dev.tar.gz
cd ai_data_extractor-1.0.0-dev
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install in Editable Mode with Dev Dependencies
```bash
pip install -e ".[dev]"
```

### 4. Run Tests
```bash
pytest tests/ -v
```

### 5. Run the Tool
```bash
# Using the installed command
data-extract --help
data-extract version

# Or direct Python execution
python -m cli.main --help
```

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_extractors/test_pdf_extractor.py -v

# Run tests by marker
pytest tests/ -v -m "not slow"
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

### Building Package
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution
python -m build
```

## Project Structure

```
src/
├── cli/                # Command-line interface
│   ├── main.py        # Entry point
│   ├── commands.py    # CLI commands
│   └── progress_display.py
├── core/              # Core data models
│   ├── models.py      # Data structures
│   └── interfaces.py  # Base classes
├── extractors/        # File extractors
│   ├── docx_extractor.py
│   ├── pdf_extractor.py
│   ├── pptx_extractor.py
│   └── excel_extractor.py
├── formatters/        # Output formatters
│   ├── json_formatter.py
│   ├── markdown_formatter.py
│   └── chunked_text_formatter.py
├── infrastructure/    # Infrastructure components
│   ├── config_manager.py
│   ├── logging_framework.py
│   ├── error_handler.py
│   └── progress_tracker.py
├── pipeline/          # Processing pipeline
│   ├── extraction_pipeline.py
│   └── batch_processor.py
└── processors/        # Content processors
    ├── context_linker.py
    ├── metadata_aggregator.py
    └── quality_validator.py

tests/
├── test_cli/          # CLI tests
├── test_extractors/   # Extractor tests
├── test_formatters/   # Formatter tests
├── test_infrastructure/  # Infrastructure tests
├── test_pipeline/     # Pipeline tests
├── test_processors/   # Processor tests
└── integration/       # Integration tests
```

## Configuration

The tool uses `config.yaml` for configuration. Copy the example:

```bash
cp config.yaml.example config.yaml
# Edit config.yaml as needed
```

## Features

- **Multi-Format Support**: DOCX, PDF, PPTX, XLSX, TXT
- **AI-Ready Output**: JSON, Markdown, Chunked Text
- **Batch Processing**: Parallel file processing
- **Quality Validation**: Content quality scoring
- **Progress Tracking**: Rich progress displays
- **Extensible**: Plugin-based architecture

## Requirements

- Python 3.11 or higher
- Dependencies managed via pip (see pyproject.toml)

## Troubleshooting

### Module Import Errors
If you see "No module named 'cli'" or similar:
- Ensure you're in the package root directory
- Ensure virtual environment is activated
- Try: `pip install -e .` (editable install)

### Test Failures
- Check Python version: `python --version` (3.11+ required)
- Install dev dependencies: `pip install -e ".[dev]"`
- Check test file paths are correct

### Package Build Issues
- Clean artifacts: `rm -rf dist/ build/ *.egg-info src/*.egg-info`
- Reinstall build tools: `pip install --upgrade build setuptools wheel`
- Try building again: `python -m build`

## Documentation

- **USER_GUIDE.md** - End-user documentation
- **QUICKSTART.md** - Quick start guide
- **docs/development/** - Developer documentation
- **examples/** - Usage examples

## Known Issues

- **error_codes.yaml Warning**: The package may show a warning about missing error_codes.yaml. This is non-fatal; the tool still works correctly. To include this file, add it to package data in setup.py or pyproject.toml.

## Support

For questions or issues, refer to the project documentation or contact the development team.

## License

Proprietary - See LICENSE file
EOFREADME

# Create package
echo "Creating tar.gz archive..."
cd ..
tar -czf ai_data_extractor-1.0.0-dev.tar.gz ai_data_extractor-1.0.0-dev/

# Move to dist
echo "Moving to dist/ directory..."
mv ai_data_extractor-1.0.0-dev.tar.gz ../../dist/

# Cleanup
cd ../..
rm -rf "$DEV_DIR"

echo ""
echo "✓ Development package created: dist/ai_data_extractor-1.0.0-dev.tar.gz"
echo ""
echo "Contents:"
echo "- Source code (all modules)"
echo "- Test suite (525+ tests)"
echo "- Documentation (user + dev guides)"
echo "- Examples and configuration templates"
echo "- DEV_README.md with setup instructions"
