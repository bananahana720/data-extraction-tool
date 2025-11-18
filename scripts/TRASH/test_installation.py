#!/usr/bin/env python3
"""Comprehensive installation test for the wheel package."""

import sys
import os
from pathlib import Path

def test_yaml_files():
    """Test that all YAML files are accessible."""
    print("\n" + "=" * 80)
    print("TEST 1: YAML File Access")
    print("=" * 80)

    try:
        import infrastructure.error_handler as eh

        # Get module directory
        module_dir = Path(eh.__file__).parent
        print(f"Module directory: {module_dir}")

        # Check for each YAML file
        yaml_files = {
            'error_codes.yaml': 'Error code definitions',
            'config_schema.yaml': 'Configuration schema',
            'log_config.yaml': 'Logging configuration',
        }

        all_found = True
        for filename, description in yaml_files.items():
            filepath = module_dir / filename
            if filepath.exists():
                print(f"[OK] {filename} - {description}")
                # Try to read and parse
                try:
                    import yaml
                    with open(filepath, 'r') as f:
                        data = yaml.safe_load(f)
                    print(f"     -> Loaded successfully ({len(str(data))} chars)")
                except Exception as e:
                    print(f"     -> ERROR loading: {e}")
                    all_found = False
            else:
                print(f"[FAIL] {filename} - NOT FOUND at {filepath}")
                all_found = False

        return all_found

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handler():
    """Test ErrorHandler can load error codes."""
    print("\n" + "=" * 80)
    print("TEST 2: ErrorHandler Initialization")
    print("=" * 80)

    try:
        from infrastructure.error_handler import ErrorHandler

        handler = ErrorHandler()
        print("[OK] ErrorHandler created successfully")

        # Try to get a known error code
        error = handler.get_error('E001')
        if error:
            print(f"[OK] Retrieved error code E001")
            print(f"     Category: {error.get('category', 'N/A')}")
            print(f"     Message: {error.get('message', 'N/A')[:50]}...")
        else:
            print("[FAIL] Could not retrieve error code E001")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_manager():
    """Test ConfigManager can access config schema."""
    print("\n" + "=" * 80)
    print("TEST 3: ConfigManager Schema Access")
    print("=" * 80)

    try:
        from infrastructure.config_manager import ConfigManager

        # Create a minimal config for testing
        test_config = {
            'extraction': {'max_file_size_mb': 100},
            'processing': {'enable_quality_validation': True},
            'output': {'default_format': 'json'}
        }

        config = ConfigManager(test_config)
        print("[OK] ConfigManager created successfully")

        # Check schema was loaded
        if hasattr(config, '_schema') or hasattr(config, 'schema'):
            print("[OK] Schema appears to be loaded")

        # Try to get a config value
        max_size = config.get('extraction.max_file_size_mb', 50)
        print(f"[OK] Retrieved config value: max_file_size_mb = {max_size}")

        return True

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logging_framework():
    """Test LoggingFramework can access log config."""
    print("\n" + "=" * 80)
    print("TEST 4: LoggingFramework Configuration")
    print("=" * 80)

    try:
        from infrastructure.logging_framework import LoggingFramework

        logger = LoggingFramework.setup_logger('test_logger')
        print("[OK] Logger created successfully")

        # Try logging
        logger.info("Test log message")
        print("[OK] Logging works")

        return True

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_import():
    """Test CLI can be imported."""
    print("\n" + "=" * 80)
    print("TEST 5: CLI Import")
    print("=" * 80)

    try:
        from cli.main import cli
        print("[OK] CLI imported successfully")
        return True

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_extractors_import():
    """Test extractors can be imported."""
    print("\n" + "=" * 80)
    print("TEST 6: Extractors Import")
    print("=" * 80)

    try:
        from extractors import DocxExtractor, PdfExtractor, PptxExtractor, ExcelExtractor
        print("[OK] All extractors imported successfully")
        return True

    except Exception as e:
        print(f"[FAIL] Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE INSTALLATION TEST")
    print("=" * 80)

    tests = [
        test_yaml_files,
        test_error_handler,
        test_config_manager,
        test_logging_framework,
        test_cli_import,
        test_extractors_import,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n[FAIL] Test crashed: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
