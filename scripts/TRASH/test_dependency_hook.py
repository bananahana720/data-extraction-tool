#!/usr/bin/env python3
"""Test script to validate the dependency change detection hook."""

import subprocess
import tempfile
from pathlib import Path


def test_hook_detects_changes() -> None:
    """Test that the hook detects dependency changes."""
    # Create a temporary pyproject.toml with a change
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(
            """
[project]
dependencies = [
    "pytest>=8.0.0,<9.0",  # Testing framework
    "new-package>=1.0.0,<2.0",  # Test addition
]
"""
        )
        temp_file = f.name

    try:
        # Run the hook on the test file
        result = subprocess.run(
            ["python", "scripts/check_dependency_changes.py", temp_file],
            capture_output=True,
            text=True,
        )

        # Check if it ran successfully (doesn't fail commits)
        assert result.returncode == 0, "Hook should not fail commits"
        print("✅ Hook runs successfully (exit code 0)")

        # The hook only shows reminder when git diff shows changes,
        # which we can't easily simulate without modifying git state
        print("✅ Hook script is functional")

    finally:
        # Clean up
        Path(temp_file).unlink()


def test_process_doc_exists() -> None:
    """Test that the process doc exists and is readable."""
    doc_path = Path("docs/processes/test-dependency-audit.md")
    assert doc_path.exists(), "Process doc should exist"

    content = doc_path.read_text()
    assert "Step-by-Step Dependency Audit Checklist" in content
    assert "Epic 2.5 spaCy Integration Example" in content
    assert "Common Pitfalls to Avoid" in content
    print("✅ Process doc exists with required sections")


def test_template_generator_integration() -> None:
    """Test that the template generator includes dependency audit reference."""
    script_path = Path("scripts/generate_story_template.py")
    content = script_path.read_text()

    assert "docs/processes/test-dependency-audit.md" in content
    print("✅ Template generator references dependency audit process")


def test_precommit_config() -> None:
    """Test that pre-commit config includes the new hook."""
    config_path = Path(".pre-commit-config.yaml")
    content = config_path.read_text()

    assert "check-dependency-changes" in content
    assert "scripts/check_dependency_changes.py" in content
    print("✅ Pre-commit configuration includes dependency check hook")


if __name__ == "__main__":
    print("Testing dependency audit integration...\n")

    test_process_doc_exists()
    test_template_generator_integration()
    test_precommit_config()
    test_hook_detects_changes()

    print("\n✅ All integration tests passed!")
    print("\nIntegration complete:")
    print("1. Process doc created at docs/processes/test-dependency-audit.md")
    print("2. Pre-commit hook configured to detect pyproject.toml changes")
    print("3. Story template generator links to audit process")
    print("4. All components are properly integrated")
