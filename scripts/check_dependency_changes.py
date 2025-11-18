#!/usr/bin/env python3
"""
Pre-commit hook to detect dependency changes in pyproject.toml.

Reminds developers to follow the test-dependency audit process when
dependencies are added or modified.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_git_diff(file_path: str) -> str:
    """Get git diff for a specific file."""
    try:
        # Get staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def check_dependency_changes(file_path: str) -> bool:
    """
    Check if dependency sections were modified in pyproject.toml.

    Returns:
        True if dependency changes detected, False otherwise
    """
    diff = get_git_diff(file_path)
    if not diff:
        return False

    # Check if diff contains changes in dependency sections
    in_dependency_section = False
    has_dependency_changes = False

    for line in diff.split("\n"):
        # Check if we're entering a dependency section
        if "[project]" in line or "[project.optional-dependencies]" in line:
            in_dependency_section = True
        elif line.startswith("[") and "]" in line:
            # Entering a different section
            in_dependency_section = False

        # Check for actual dependency changes
        if in_dependency_section and (line.startswith("+") or line.startswith("-")):
            # Skip diff metadata lines
            if not (line.startswith("+++") or line.startswith("---")):
                # Check if line contains a dependency (has = sign or is in list format)
                if "=" in line or (
                    '"' in line and "#" not in line[: line.find('"') if '"' in line else len(line)]
                ):
                    has_dependency_changes = True
                    break

    return has_dependency_changes


def print_reminder() -> None:
    """Print the dependency audit reminder message."""
    message = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📦 DEPENDENCY CHANGE DETECTED 📦                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  You've modified dependencies in pyproject.toml.                            ║
║                                                                              ║
║  Please ensure you've followed the Test Dependency Audit Process:           ║
║                                                                              ║
║  📋 Review the checklist at:                                                ║
║     docs/processes/test-dependency-audit.md                                 ║
║                                                                              ║
║  Key steps:                                                                 ║
║  ✓ Security assessment (CVE check)                                         ║
║  ✓ Version constraints with story reference                                ║
║  ✓ Installation validation                                                 ║
║  ✓ Smoke test script (if new library)                                      ║
║  ✓ Performance baseline measurement                                        ║
║  ✓ CI/CD integration & caching                                            ║
║  ✓ Documentation updates (CLAUDE.md, README.md)                            ║
║  ✓ Integration tests                                                       ║
║                                                                              ║
║  Reference: Story 2.5.2 (spaCy integration) shows a complete example        ║
║                                                                              ║
║  💡 Tip: Run the smoke test before committing:                             ║
║     python scripts/smoke-test-[package].py                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(message)


def main() -> int:
    """Main entry point for the pre-commit hook."""
    parser = argparse.ArgumentParser(description="Check for dependency changes")
    parser.add_argument("files", nargs="*", help="Files to check")
    args = parser.parse_args()

    # Check if pyproject.toml is in the changed files
    for file_path in args.files:
        if Path(file_path).name == "pyproject.toml":
            if check_dependency_changes(file_path):
                print_reminder()
                # Don't fail the commit, just remind
                return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
