# Testing Infrastructure

This directory contains the test suite for the data extraction tool. The testing infrastructure is designed to support modular development with clear patterns for testing extractors, processors, and formatters.

## Quick Start

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_extractors/test_docx_extractor.py

# Run specific test
pytest tests/test_extractors/test_docx_extractor.py::test_docx_extractor_basic

# Run tests matching pattern
pytest -k "docx"

# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Running with Coverage

```bash
# Install coverage tool first
pip install pytest-cov

# Run tests with coverage report
pytest --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## Directory Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── README.md                # This file
│
├── fixtures/                # Test data files
│   ├── sample.txt           # Basic text file
│   ├── sample.docx          # (TODO) Sample Word document
│   ├── sample.pdf           # (TODO) Sample PDF
│   └── ...                  # More test files as needed
│
├── test_extractors/         # Extractor tests
│   ├── __init__.py
│   ├── test_docx_extractor.py
│   ├── test_pdf_extractor.py   # (TODO)
│   └── ...
│
├── test_processors/         # Processor tests
│   ├── __init__.py
│   ├── test_context_linker.py  # (TODO)
│   └── ...
│
└── test_formatters/         # Formatter tests
    ├── __init__.py
    ├── test_json_formatter.py  # (TODO)
    └── ...
```

## Testing Patterns

### Pattern 1: Testing Extractors

Every extractor test should follow this structure:

```python
import pytest
from pathlib import Path
from src.extractors.my_extractor import MyExtractor
from src.core import ExtractionResult, ContentType

@pytest.mark.unit
@pytest.mark.extraction
def test_my_extractor_basic(validate_extraction_result):
    """Test basic extraction with valid file."""
    # Arrange
    extractor = MyExtractor()
    test_file = Path("tests/fixtures/sample.ext")

    # Act
    result = extractor.extract(test_file)

    # Assert
    validate_extraction_result(result)
    assert result.success is True
    assert len(result.content_blocks) > 0
```

**Key principles:**
- Use `validate_extraction_result` fixture to check structure
- Test success path first, then error cases
- Mark with `@pytest.mark.unit` and `@pytest.mark.extraction`
- Follow Arrange-Act-Assert pattern

### Pattern 2: Testing Processors

Every processor test should follow this structure:

```python
import pytest
from src.processors.my_processor import MyProcessor
from src.core import ProcessingResult

@pytest.mark.unit
@pytest.mark.processing
def test_my_processor(sample_extraction_result, validate_processing_result):
    """Test processor enriches content correctly."""
    # Arrange
    processor = MyProcessor()

    # Act
    result = processor.process(sample_extraction_result)

    # Assert
    validate_processing_result(result)
    assert result.success is True
    # Check specific enrichments
    assert result.content_blocks[0].metadata.get("enriched") is True
```

**Key principles:**
- Use `sample_extraction_result` fixture for input
- Use `validate_processing_result` fixture to check structure
- Verify enrichments were applied
- Test with both successful and failed extraction inputs

### Pattern 3: Testing Formatters

Every formatter test should follow this structure:

```python
import pytest
from src.formatters.my_formatter import MyFormatter
from src.core import FormattedOutput

@pytest.mark.unit
@pytest.mark.formatting
def test_my_formatter(sample_processing_result):
    """Test formatter produces correct output."""
    # Arrange
    formatter = MyFormatter()

    # Act
    result = formatter.format(sample_processing_result)

    # Assert
    assert isinstance(result, FormattedOutput)
    assert result.success is True
    assert len(result.content) > 0
    assert result.format_type == "my_format"
```

**Key principles:**
- Use `sample_processing_result` fixture for input
- Verify output format structure
- Test format-specific features
- Check additional files if applicable

### Pattern 4: Testing Error Handling

All modules should gracefully handle errors:

```python
@pytest.mark.unit
def test_extractor_missing_file():
    """Test extractor handles missing file gracefully."""
    extractor = MyExtractor()
    missing_file = Path("nonexistent.ext")

    result = extractor.extract(missing_file)

    # Should return result with success=False, not raise exception
    assert result.success is False
    assert len(result.errors) > 0
    assert "not found" in result.errors[0].lower()
```

**Key principles:**
- Never raise exceptions for expected errors (missing files, corrupt data)
- Return result objects with `success=False` and populated `errors`
- Only raise exceptions for programming errors (bugs, invalid arguments)

## Available Fixtures

The `conftest.py` file provides shared fixtures for all tests. Key fixtures:

### Content Block Fixtures

- `sample_content_block` - Basic paragraph block
- `sample_heading_block` - Heading block
- `sample_table_block` - Table block with metadata
- `sample_image_block` - Image block
- `sample_content_blocks` - List of mixed blocks

### Result Fixtures

- `sample_document_metadata` - DocumentMetadata with sample data
- `sample_extraction_result` - Successful ExtractionResult
- `failed_extraction_result` - Failed ExtractionResult with errors
- `sample_processing_result` - Successful ProcessingResult

### File Fixtures

- `temp_test_file(tmp_path)` - Creates temporary test file
- `empty_test_file(tmp_path)` - Empty file for edge case testing
- `large_test_file(tmp_path)` - Large file for performance testing
- `fixture_dir` - Path to fixtures directory

### Validation Fixtures

- `validate_extraction_result` - Validates ExtractionResult structure
- `validate_processing_result` - Validates ProcessingResult structure

### Usage Example

```python
def test_with_fixtures(sample_content_block, temp_test_file):
    """Example using multiple fixtures."""
    # sample_content_block is automatically created
    assert sample_content_block.block_type == ContentType.PARAGRAPH

    # temp_test_file is created in temporary directory
    assert temp_test_file.exists()
```

## Test Markers

Tests can be marked for selective execution:

```python
@pytest.mark.unit          # Fast unit tests
@pytest.mark.integration   # Integration tests (slower)
@pytest.mark.slow          # Tests taking >1 second
@pytest.mark.extraction    # Extractor tests
@pytest.mark.processing    # Processor tests
@pytest.mark.formatting    # Formatter tests
```

Run specific marker groups:

```bash
pytest -m unit              # Only unit tests
pytest -m "unit and extraction"  # Unit tests for extractors
pytest -m "not slow"        # Skip slow tests
```

## Coverage Requirements

**Enterprise target: >85% code coverage**

### Measuring Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html  # or browse to file
```

### Coverage Goals

- **Core models**: 100% (should be simple data classes)
- **Interfaces**: 100% (base implementations)
- **Extractors**: >85% (including error paths)
- **Processors**: >85%
- **Formatters**: >85%
- **Pipeline**: >90% (critical orchestration logic)

### What to Test

Every module should have tests for:

1. **Success path** - Normal operation with valid input
2. **Error paths** - Invalid input, failures, edge cases
3. **Interface contract** - Implements required methods correctly
4. **Type contracts** - Returns correct types
5. **Edge cases** - Empty input, large input, boundary conditions

## Adding New Tests

### Step 1: Create Test File

Create test file following naming convention:

```bash
tests/test_extractors/test_new_extractor.py
tests/test_processors/test_new_processor.py
tests/test_formatters/test_new_formatter.py
```

### Step 2: Use Template

Start with the template from `test_docx_extractor.py`:

```python
"""
Test module for NewExtractor.

Description of what's being tested.
"""

import pytest
from pathlib import Path
from src.extractors.new_extractor import NewExtractor

@pytest.mark.unit
@pytest.mark.extraction
def test_new_extractor_basic(validate_extraction_result):
    """Test basic extraction."""
    extractor = NewExtractor()
    test_file = Path("tests/fixtures/sample.ext")

    result = extractor.extract(test_file)

    validate_extraction_result(result)
    assert result.success is True
```

### Step 3: Add Fixtures

If you need custom test data, add fixtures to `conftest.py` or create
a local `conftest.py` in the subdirectory.

### Step 4: Add Test Files

Add sample files to `tests/fixtures/`:

```bash
tests/fixtures/sample_new_format.ext
tests/fixtures/empty.ext
tests/fixtures/corrupt.ext
```

### Step 5: Run Tests

```bash
# Run your new tests
pytest tests/test_extractors/test_new_extractor.py -v

# Run with coverage
pytest tests/test_extractors/test_new_extractor.py --cov=src.extractors.new_extractor
```

## Best Practices

### Do's

✓ **Test one thing per test** - Each test should verify one behavior
✓ **Use descriptive names** - `test_extractor_handles_corrupt_file` not `test_error`
✓ **Arrange-Act-Assert** - Clear separation of setup, execution, verification
✓ **Use fixtures** - Share common setup via fixtures in conftest.py
✓ **Mark tests appropriately** - Use markers for selective execution
✓ **Test error paths** - Don't just test happy path
✓ **Document test purpose** - Docstring explaining what and why

### Don'ts

✗ **Don't test implementation details** - Test behavior, not internals
✗ **Don't share state between tests** - Each test should be independent
✗ **Don't use real external resources** - Mock APIs, file systems when appropriate
✗ **Don't skip error testing** - Error paths are critical
✗ **Don't hardcode paths** - Use fixtures and Path objects
✗ **Don't test without markers** - Always mark test type

## Debugging Tests

### Running Single Test

```bash
# Run specific test with output
pytest tests/test_extractors/test_docx_extractor.py::test_name -v -s

# -v = verbose
# -s = show print statements
```

### Using Debugger

```python
def test_something():
    import pdb; pdb.set_trace()  # Breakpoint
    # Test code here
```

Or use pytest's built-in debugger:

```bash
pytest --pdb  # Drop into debugger on failure
pytest --trace  # Drop into debugger at start of test
```

### Showing Output

```bash
# See print statements
pytest -s

# See logging output
pytest --log-cli-level=DEBUG
```

## CI/CD Integration

For continuous integration, tests should:

1. **Run on every commit** - Catch issues early
2. **Block merges on failure** - Enforce quality
3. **Generate coverage reports** - Track coverage trends
4. **Run in isolation** - No external dependencies

Example GitHub Actions workflow:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting

### Tests Not Found

```bash
# Check test discovery
pytest --collect-only

# Ensure files match pattern test_*.py
# Ensure functions match pattern test_*
```

### Import Errors

```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install package in development mode
pip install -e .
```

### Fixture Not Found

```bash
# Check conftest.py is in correct location
# Check fixture name is spelled correctly
# Check fixture is not shadowed by local fixture
```

### Slow Tests

```bash
# Profile test execution
pytest --durations=10

# Run only fast tests
pytest -m "not slow"
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Markers](https://docs.pytest.org/en/stable/mark.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- Project Foundation: `../FOUNDATION.md`
- Development Guide: `../GETTING_STARTED.md`

## Next Steps

1. **Implement extractors** - Use test template from `test_docx_extractor.py`
2. **Add test fixtures** - Create sample files in `fixtures/`
3. **Write tests first** - TDD approach recommended
4. **Run tests frequently** - Fast feedback loop
5. **Monitor coverage** - Aim for >85% coverage

---

**Status**: Test infrastructure complete and ready for use.

**Last Updated**: 2025-10-29

For questions or issues with testing, refer to this guide or check the foundation documentation.
