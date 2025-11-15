# Repository Guidelines

## Project Structure & Module Organization
Source lives under `src/data_extract/` using a staged pipeline (`extract → normalize → chunk → semantic → output`). Brownfield legacy packages (e.g., `src/extractors/`, `src/processors/`) stay in place until migration stories land. Tests are split between `tests/` for new coverage and historical suites such as `testsunitcore/` and `testsunitpipeline/`; add new files alongside the module you touch. Docs and planning artifacts are in `docs/`, helper utilities in `scripts/`, and runtime artifacts land in `logs/`, `output/`, and `htmlcov/` (keep these out of commits).

## Build, Test, and Development Commands
Use `pip install -e ".[dev]"` inside the repo to pull core and dev dependencies. Download NLP assets with `python -m spacy download en_core_web_md`. Run the CLI with `data-extract --help` to ensure entry points resolve. Quality commands: `black src tests` (format), `ruff check src tests` (lint), `mypy src/data_extract` (types), and `pre-commit run --all-files` before every commit. Execute `pytest -v --cov=src --cov-report=term-missing` for full validation; narrow to categories via `pytest tests/unit -m "not slow"` when iterating.

## Coding Style & Naming Conventions
Code follows Black’s 100-character limit with 4-space indentation. Keep modules and functions snake_case, classes PascalCase, and constants ALL_CAPS. Public functions must carry type hints and docstrings; prefer dataclasses or Pydantic models for structured data. Configuration keys and environment variables use the `DATA_EXTRACT_*` prefix, and YAML configs belong in `config/` or `~/.data-extract/`. Run Ruff (E,F,I,N,W rules) and let Black own formatting conflicts—never hand-edit for 100+ char lines.

## Testing Guidelines
Pytest is configured via `pytest.ini` to collect `test_*.py`; mirror that pattern plus descriptive suffixes (e.g., `test_chunk_metadata.py`). Maintain current coverage targets: >60% baseline, >80% through Epics 2-4, and >90% on critical Epic 5 paths. Generate HTML coverage when touching pipeline-critical code (`pytest --cov=src --cov-report=html`) and inspect `htmlcov/index.html`. Mark slow or performance runs with `@pytest.mark.slow` / `@pytest.mark.performance` to keep CI lean.

## Commit & Pull Request Guidelines
Recent history favors imperative, scoped subjects (`docs: reorganize epics`, `Fix: remove invalid dependency`, `Story 3.3: chunk metadata`). Follow that format: prefix with area or story, keep to ~72 characters, and describe what/why in the body. Every PR should link the driving story/issue, summarize pipeline impacts, note new configs, and attach CLI/log output or screenshots when behavior changes. Confirm CI (tests + pre-commit) locally before requesting review.

## Security & Configuration Tips
Never commit `.env`, raw documents, or customer data—use `.gitignore` entries already provided. Secrets should flow through environment variables or the YAML config cascade (CLI flags > env > config > defaults). When adding processors that touch external services, guard them behind feature flags in `config.yaml` and document required credentials under `docs/`.
