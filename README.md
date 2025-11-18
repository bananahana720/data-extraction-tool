# Data Extraction Tool

**Version**: 0.1.0 (Epic 1 - Foundation)
**Python**: 3.12+ (Required)
**Status**: In Development - Foundation Phase

Enterprise data extraction tool with modular pipeline architecture for document processing, optimized for RAG workflows.

## Architecture

The tool implements a modular pipeline pattern:

```
extract → normalize → chunk → semantic → output
```

Each stage is a composable, testable component that processes documents through well-defined interfaces using Pydantic v2 models.

## Prerequisites

- **Python 3.12 or higher** (mandatory - enterprise requirement)
- **Git** for version control
- **Windows, macOS, or Linux** (primary target: Windows)

## Quick Start

### 1. Verify Python Version

```bash
python --version
# Should show Python 3.12.x or 3.13.x
```

If you don't have Python 3.12+, install it from [python.org](https://www.python.org/downloads/).

### 2. Clone Repository

```bash
git clone [repository-url]
cd data-extraction-tool
```

### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- Core dependencies (pydantic, PyYAML, structlog, python-dotenv, **spacy**)
- Development tools (pytest, black, mypy, ruff, pre-commit)
- Brownfield compatibility packages (existing extractors)

### 5. Download spaCy Language Model

**Required for Epic 3 chunking** (Story 2.5.2 integration):

```bash
python -m spacy download en_core_web_md
```

This downloads the English language model (~33MB) for sentence boundary detection. Model loads in ~1.2 seconds and processes 4000+ words/second.

**Troubleshooting**: If the model download fails, see `docs/troubleshooting-spacy.md` for solutions.

### 6. Install Pre-commit Hooks

```bash
pre-commit install
```

Pre-commit hooks run automatically on `git commit` to enforce:
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

### 7. Verify Installation

```bash
# Verify spaCy model
python -m spacy validate
# Expected output: "✔ Loaded compatibility table"

# Run tests
pytest
# Expected output: "collected 1007+ items" (includes brownfield + new tests)

# Check formatting
black --check src/
# Expected output: "All done! ✨ 🍰 ✨" or reformatting messages

# Run linter
ruff check src/
# Expected output: No output if no issues found, or list of linting errors

# Run type checker
mypy src/data_extract/
# Expected output: "Success: no issues found in X source files"

# Verify CLI entry point
data-extract
# Expected output: Placeholder message confirming CLI is functional (Epic 5 implementation)
```

All tools should execute without errors. The test suite collects 1007 existing brownfield tests.

## Project Structure

```
data-extraction-tool/
├── pyproject.toml              # PEP 621 project configuration
├── README.md                   # This file
├── .gitignore                  # Python project excludes
├── .pre-commit-config.yaml     # Code quality hooks
├── src/
│   └── data_extract/           # New modular architecture (Epic 1+)
│       ├── __init__.py         # Package version and exports
│       ├── core/               # Core data models (Story 1.4)
│       ├── extract/            # Stage 1 (Epic 2)
│       ├── normalize/          # Stage 2 (Epic 2)
│       ├── chunk/              # Stage 3 (Epic 3)
│       ├── semantic/           # Stage 4 (Epic 4)
│       ├── output/             # Stage 5 (Epic 3)
│       ├── config/             # Configuration (Epic 5)
│       ├── utils/              # Shared utilities
│       └── cli.py              # CLI entry point (Epic 5)
├── tests/                      # Test suite
│   ├── conftest.py             # Shared fixtures
│   ├── fixtures/               # Test data
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── performance/            # Performance benchmarks
├── docs/                       # Project documentation
│   ├── architecture.md         # System architecture
│   ├── PRD.md                  # Product requirements
│   ├── tech-spec-epic-1.md     # Epic 1 technical spec
│   └── epics.md                # Epic breakdown
├── config/                     # Configuration templates
└── scripts/                    # Utility scripts
```

**Note:** The `src/` directory also contains existing brownfield packages (`cli/`, `extractors/`, `processors/`, etc.). Story 1.2 will assess this code, and Story 1.4 will integrate it into the new architecture.

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest -m "not slow"  # Skip slow tests

# Run tests in parallel
pytest -n auto
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/data_extract/

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### Coverage Requirements

- **Epic 1**: >60% baseline coverage
- **Epic 2-4**: >80% overall coverage
- **Epic 5**: >90% for critical paths

## Configuration

Configuration follows a three-tier precedence (Epic 5):

1. **CLI flags** (highest precedence)
2. **Environment variables** (DATA_EXTRACT_* prefix)
3. **YAML config file** (~/.data-extract/config.yaml or project-local)
4. **Hardcoded defaults** (lowest precedence)

Epic 1 sets up the infrastructure; Epic 5 implements the full cascade.

## Current Status

### ✅ Epic 1: Foundation & Project Setup (In Progress)

- **Story 1.1**: Project Infrastructure Initialization (In Progress)
  - ✅ Python 3.12+ virtual environment
  - ✅ pyproject.toml with dependency management
  - ✅ Development toolchain (pytest, black, mypy, ruff, pre-commit)
  - ✅ Project structure following modern Python conventions
  - ✅ README with setup instructions

- **Story 1.2**: Brownfield Codebase Assessment (Backlog)
- **Story 1.3**: Testing Framework and CI Pipeline (Backlog)
- **Story 1.4**: Core Pipeline Architecture Pattern (Backlog)

### 📋 Epic 2-5: Processing, Output, Analysis, CLI (Planned)

See `docs/epics.md` for full epic breakdown.

## Technology Stack

- **Python 3.12+**: Mandatory enterprise requirement
- **Pydantic v2**: Runtime validation and data models
- **PyYAML**: Configuration management
- **structlog**: Structured logging
- **pytest**: Testing framework with coverage and parallel execution
- **black**: Opinionated code formatting
- **ruff**: Fast Python linter (replaces flake8 + isort)
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality

## Contributing

This is an internal enterprise F100 cybersecurity tool. Development follows the BMad Method with story-based implementation.

### Code Standards

- **Type hints**: Required for all functions (enforced by mypy)
- **Docstrings**: Required for all public APIs
- **Tests**: Required for all new functionality (see coverage requirements)
- **Formatting**: Enforced by black (100 char line length)
- **Linting**: Enforced by ruff
- **Commits**: Pre-commit hooks must pass

### Branch Strategy

- **main**: Production-ready code
- **story/X-Y-name**: Story implementation branches
- Epic-level integration on completion

## License

Proprietary - Internal enterprise use only

## Support

For questions or issues:
1. Check documentation in `docs/`
2. Review story files in `docs/stories/`
3. Consult architecture decisions in `docs/architecture.md`

---

**Next Steps:**
- Complete Story 1.1 verification
- Run Story 1.2 (Brownfield Assessment)
- Implement Story 1.3 (Testing Framework)
- Build Story 1.4 (Core Pipeline Architecture)
#   b m m - d a t a - e x t r a c t i o n - t o o l 
 
 #   d a t a - e x t r a c t i o n - t o o l 
 
 
## API Documentation

The Data Extraction Tool provides 1 modules with 1 classes and 0 functions.

### Key Modules:

- `test_module`

See [API Documentation](docs/api/) for complete reference.

## Test Coverage

Coverage data not available. No coverage data found. Run tests with coverage first.
