#!/usr/bin/env python3
"""
Installation Validation Script for AI Data Extractor.

Tests all documented CLI commands to ensure they work as expected
after wheel installation.

Usage:
    python scripts/validate_installation.py

Exit Codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(msg: str) -> None:
    """Print colored header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{msg}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(msg: str) -> None:
    """Print success message."""
    print(f"{GREEN}✓ {msg}{RESET}")


def print_error(msg: str) -> None:
    """Print error message."""
    print(f"{RED}✗ {msg}{RESET}")


def print_warning(msg: str) -> None:
    """Print warning message."""
    print(f"{YELLOW}⚠ {msg}{RESET}")


def run_command(cmd: List[str], expect_success: bool = True) -> Tuple[bool, str, str]:
    """
    Run a command and return success status and output.

    Args:
        cmd: Command as list of strings
        expect_success: Whether command should succeed (True) or fail (False)

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        success = (result.returncode == 0) == expect_success
        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_help_command() -> bool:
    """Test: data-extract --help"""
    print("\n📋 Test: data-extract --help")
    success, stdout, stderr = run_command(["data-extract", "--help"])

    if success and "Data Extraction Tool" in stdout:
        print_success("Help command works")
        return True
    else:
        print_error("Help command failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_version_command() -> bool:
    """Test: data-extract version"""
    print("\n📋 Test: data-extract version")
    success, stdout, stderr = run_command(["data-extract", "version"])

    if success and "1.0.0" in stdout:
        print_success("Version command works")
        return True
    else:
        print_error("Version command failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_version_verbose() -> bool:
    """Test: data-extract version --verbose"""
    print("\n📋 Test: data-extract version --verbose")
    success, stdout, stderr = run_command(["data-extract", "version", "--verbose"])

    if success and "Python version" in stdout:
        print_success("Version --verbose works")
        return True
    else:
        print_error("Version --verbose failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_extract_help() -> bool:
    """Test: data-extract extract --help"""
    print("\n📋 Test: data-extract extract --help")
    success, stdout, stderr = run_command(["data-extract", "extract", "--help"])

    if success and "Extract content from a single file" in stdout:
        print_success("Extract --help works")
        return True
    else:
        print_error("Extract --help failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_batch_help() -> bool:
    """Test: data-extract batch --help"""
    print("\n📋 Test: data-extract batch --help")
    success, stdout, stderr = run_command(["data-extract", "batch", "--help"])

    if success and "Process multiple files" in stdout:
        print_success("Batch --help works")
        return True
    else:
        print_error("Batch --help failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_config_help() -> bool:
    """Test: data-extract config --help"""
    print("\n📋 Test: data-extract config --help")
    success, stdout, stderr = run_command(["data-extract", "config", "--help"])

    if success and "Configuration management" in stdout:
        print_success("Config --help works")
        return True
    else:
        print_error("Config --help failed")
        if stderr:
            print(f"  Error: {stderr[:200]}")
        return False


def test_extract_txt_file() -> bool:
    """Test: data-extract extract on a test .txt file"""
    print("\n📋 Test: data-extract extract <test.txt>")

    # Create temporary test file
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        test_file = tmpdir_path / "test.txt"
        output_file = tmpdir_path / "output.json"

        # Write test content
        test_file.write_text("Hello, World!\nThis is a test.\n")

        # Run extraction
        success, stdout, stderr = run_command([
            "data-extract",
            "extract",
            str(test_file),
            "--output", str(output_file),
            "--format", "json"
        ])

        # Check success and output file exists
        if success and output_file.exists():
            content = output_file.read_text()
            if "Hello, World!" in content:
                print_success("Extract command works (TXT → JSON)")
                return True
            else:
                print_error("Output file doesn't contain expected content")
                return False
        else:
            print_error("Extract command failed")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            return False


def test_missing_file_error() -> bool:
    """Test: data-extract extract with missing file (should fail gracefully)"""
    print("\n📋 Test: data-extract extract <nonexistent.txt> (expect error)")

    success, stdout, stderr = run_command(
        ["data-extract", "extract", "nonexistent_file_12345.txt"],
        expect_success=False
    )

    if success:  # Should fail
        print_success("Missing file error handled gracefully")
        return True
    else:
        print_error("Missing file not handled properly")
        return False


def main() -> int:
    """Run all validation tests."""
    print_header("AI Data Extractor - Installation Validation")

    print("This script validates that all documented CLI commands work correctly.")
    print("It should be run AFTER installing the wheel package.")

    # Check if data-extract is available
    print("\n🔍 Checking if 'data-extract' command is available...")
    success, stdout, stderr = run_command(["data-extract", "--help"])

    if not success:
        print_error("Command 'data-extract' not found!")
        print("\nPlease install the wheel first:")
        print("  pip install dist/ai_data_extractor-1.0.0-py3-none-any.whl")
        return 1

    print_success("Command 'data-extract' is available")

    # Run all tests
    tests = [
        test_help_command,
        test_version_command,
        test_version_verbose,
        test_extract_help,
        test_batch_help,
        test_config_help,
        test_extract_txt_file,
        test_missing_file_error,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print_error(f"Test {test.__name__} raised exception: {e}")
            results.append(False)

    # Print summary
    print_header("Validation Summary")

    passed = sum(results)
    total = len(results)

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print_success("ALL TESTS PASSED ✓")
        print("\nThe installation is working correctly!")
        print("\nYou can now use commands like:")
        print("  data-extract extract document.pdf")
        print("  data-extract batch ./documents/ --output ./results/")
        return 0
    else:
        print_error(f"SOME TESTS FAILED ({total - passed} failures)")
        print("\nPlease review the errors above and ensure:")
        print("  1. The wheel was installed correctly")
        print("  2. All dependencies are available")
        print("  3. You're using Python 3.11+")
        return 1


if __name__ == "__main__":
    sys.exit(main())
