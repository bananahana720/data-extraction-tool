# Test Fixtures

This directory contains test data files for the data extraction tool test suite.

## Directory Structure

```
fixtures/
├── pdfs/           # PDF test files
├── docx/           # Word document test files
├── xlsx/           # Excel spreadsheet test files
├── images/         # Image files for OCR testing
├── archer/         # Archer-specific audit domain test files
├── excel/          # Legacy Excel fixtures (to be migrated)
└── real-world-files/  # Real-world audit framework documents (COBIT, NIST, OWASP)
```

## Test Fixtures

### PDFs (`pdfs/`)
- **sample.pdf** (629 bytes) - Minimal PDF with basic text content for unit testing

### Word Documents (`docx/`)
- **sample.docx** (36KB) - Word document with tables for extraction testing

### Excel Files (`xlsx/`)
- **sample.xlsx** (4.8KB) - Simple Excel spreadsheet for tabular data extraction

### Images (`images/`)
- **sample.png** (3.1KB) - Simple image with text for OCR testing

### Archer Domain Files (`archer/`)
- Reserved for Archer-specific audit domain test files

## Real-World Files (`real-world-files/`)

Large reference documents for integration and performance testing:
- COBIT 2019 framework documents (PDFs, 0.8MB - 11.9MB)
- NIST cybersecurity framework documents (Excel/PDF, various sizes)
- OWASP security guides (PDFs)
- COSO ERM compliance documents (PDFs)

**Note:** Real-world files are used for integration tests and benchmarking, not unit tests.

## Size Guidelines

All test fixtures in `pdfs/`, `docx/`, `xlsx/`, `images/`, and `archer/` directories should be:
- **<100KB each** (requirement from AC-1.3.2)
- **Sanitized** - no sensitive data or PII
- **Representative** - reflect real-world audit document characteristics where possible

## Usage in Tests

Test fixtures are accessible via pytest fixtures defined in:
- `tests/conftest.py` - Global fixtures
- `tests/test_extractors/conftest.py` - Extractor-specific fixtures
- `tests/test_cli/conftest.py` - CLI testing fixtures

Example usage:
```python
def test_pdf_extraction(tmp_path):
    """Test PDF extraction with sample fixture."""
    fixture_path = Path("tests/fixtures/pdfs/sample.pdf")
    result = extract_pdf(fixture_path)
    assert result.success
```

## Adding New Fixtures

When adding new test fixtures:
1. Ensure file size is <100KB
2. Remove any sensitive data
3. Place in appropriate subdirectory
4. Update this README
5. Consider adding a pytest fixture in relevant conftest.py

## Maintenance

Created: 2025-11-10
Last Updated: 2025-11-10
Maintained by: Dev team
