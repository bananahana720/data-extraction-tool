#!/usr/bin/env python3
"""Check that the wheel package contains all necessary files."""

import zipfile
import sys
from pathlib import Path

REQUIRED_FILES = [
    'infrastructure/error_codes.yaml',
    'infrastructure/config_schema.yaml',
    'infrastructure/log_config.yaml',
    'infrastructure/error_handler.py',
    'infrastructure/config_manager.py',
    'infrastructure/logging_framework.py',
    'infrastructure/progress_tracker.py',
]

def check_wheel(wheel_path: str) -> bool:
    """Check wheel contents."""
    print(f"Checking wheel: {wheel_path}")
    print("=" * 80)

    with zipfile.ZipFile(wheel_path, 'r') as zf:
        contents = zf.namelist()

        print(f"\nTotal files in wheel: {len(contents)}")

        # Check for required files
        missing = []
        found = []

        print("\n### Required Files Check ###")
        for req_file in REQUIRED_FILES:
            # Wheel files have paths like: package_name/path/to/file
            matching = [f for f in contents if req_file in f and not f.endswith('.pyc')]

            if matching:
                found.append(req_file)
                print(f"[OK] {req_file}")
                for match in matching:
                    print(f"   -> {match}")
            else:
                missing.append(req_file)
                print(f"[MISS] {req_file} -> NOT FOUND")

        # Show all YAML files in package
        yaml_files = [f for f in contents if (f.endswith('.yaml') or f.endswith('.yml')) and not '__pycache__' in f]
        print(f"\n### All YAML Files in Package ({len(yaml_files)}) ###")
        if yaml_files:
            for yf in sorted(yaml_files):
                print(f"  [+] {yf}")
        else:
            print("  [MISS] NO YAML FILES FOUND!")

        # Show all data files (non-Python)
        data_files = [f for f in contents
                      if not f.endswith('.py')
                      and not f.endswith('.pyc')
                      and not '__pycache__' in f
                      and not f.endswith('/')]
        print(f"\n### All Data Files in Package ({len(data_files)}) ###")
        for df in sorted(data_files):
            print(f"  • {df}")

        # Summary
        print("\n" + "=" * 80)
        if missing:
            print(f"[FAIL] MISSING {len(missing)} required files:")
            for m in missing:
                print(f"   - {m}")
            print(f"[OK] Found {len(found)}/{len(REQUIRED_FILES)} required files")
            return False
        else:
            print(f"[SUCCESS] All {len(REQUIRED_FILES)} required files present!")
            return True

if __name__ == '__main__':
    wheel = Path('dist/ai_data_extractor-1.0.0-py3-none-any.whl')
    if not wheel.exists():
        print(f"[FAIL] Wheel not found: {wheel}")
        sys.exit(1)

    success = check_wheel(str(wheel))
    sys.exit(0 if success else 1)
