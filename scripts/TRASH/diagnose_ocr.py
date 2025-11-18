#!/usr/bin/env python3
"""
OCR Diagnostic Script for Data Extractor Tool
Run this on your test computer to identify the exact OCR failure cause.
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("OCR DIAGNOSTIC TOOL - Data Extractor")
print("=" * 70)

# Test 1: Check Python environment
print("\n[1] Python Environment")
print(f"    Python version: {sys.version}")
print(f"    Working directory: {Path.cwd()}")

# Test 2: Check environment variable
print("\n[2] Tesseract Environment Variable")
env_var_name = "DATA_EXTRACTOR_EXTRACTORS_PDF_TESSERACT_CMD"
env_var = os.environ.get(env_var_name)
if env_var:
    print(f"    ✓ {env_var_name} is SET")
    print(f"    Value: {env_var}")
    tesseract_path = Path(env_var)
    print(f"    File exists: {tesseract_path.exists()}")
    if tesseract_path.exists():
        print(f"    Is file: {tesseract_path.is_file()}")
    else:
        print(f"    ✗ ERROR: File does not exist at this path!")
else:
    print(f"    ✗ {env_var_name} is NOT SET")
    print("    Will use system PATH or config.yaml")

# Test 3: Check config.yaml
print("\n[3] Configuration File")
config_path = Path("config.yaml")
if config_path.exists():
    print(f"    ✓ config.yaml found at: {config_path.absolute()}")
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            tesseract_cmd = config.get('extractors', {}).get('pdf', {}).get('tesseract_cmd')
            if tesseract_cmd:
                print(f"    ✓ tesseract_cmd configured: {tesseract_cmd}")
                cmd_path = Path(tesseract_cmd)
                print(f"    File exists: {cmd_path.exists()}")
            else:
                print("    - tesseract_cmd not set in config (will use PATH)")
    except ImportError:
        print("    - Cannot check config (pyyaml not installed)")
    except Exception as e:
        print(f"    ✗ Error reading config: {e}")
else:
    print("    - config.yaml not found (will use defaults)")

# Test 4: Import dependencies
print("\n[4] Python Dependencies")

# pytesseract
try:
    import pytesseract
    print("    ✓ pytesseract installed")
except ImportError as e:
    print(f"    ✗ pytesseract NOT installed: {e}")
    print("      Install with: pip install pytesseract")
    pytesseract = None

# pdf2image
try:
    import pdf2image
    print("    ✓ pdf2image installed")
except ImportError as e:
    print(f"    ✗ pdf2image NOT installed: {e}")
    print("      Install with: pip install pdf2image")
    pdf2image = None

# PIL
try:
    from PIL import Image
    print("    ✓ PIL (Pillow) installed")
except ImportError as e:
    print(f"    ✗ PIL NOT installed: {e}")
    print("      Install with: pip install Pillow")

# Test 5: Tesseract executable test
print("\n[5] Tesseract Executable Test")
if pytesseract:
    # Try with environment variable path
    if env_var:
        print(f"    Testing with env var path: {env_var}")
        pytesseract.pytesseract.tesseract_cmd = env_var

    try:
        version = pytesseract.get_tesseract_version()
        print(f"    ✓ SUCCESS: Tesseract found")
        print(f"    Version: {version}")
    except pytesseract.TesseractNotFoundError as e:
        print(f"    ✗ TESSERACT NOT FOUND")
        print(f"    Error: {e}")
        print(f"\n    Troubleshooting:")
        print(f"    1. Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print(f"    2. Add to PATH or set tesseract_cmd in config.yaml")
        print(f"    3. If installed, verify path is correct")
    except Exception as e:
        print(f"    ✗ UNEXPECTED ERROR: {type(e).__name__}")
        print(f"    Message: {e}")
else:
    print("    - Skipped (pytesseract not installed)")

# Test 6: PDF to Image conversion (requires poppler)
print("\n[6] PDF to Image Conversion Test (Poppler)")
if pdf2image:
    # Create a minimal test - we can't actually convert without a PDF
    # but we can check if poppler binaries are accessible
    print("    Checking poppler availability...")
    try:
        # Try to get poppler version info
        # This will fail if poppler is not in PATH
        import subprocess
        result = subprocess.run(['pdftoppm', '-v'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0 or 'poppler' in result.stderr.lower():
            print(f"    ✓ Poppler tools found in PATH")
        else:
            print(f"    ✗ Poppler tools not found")
            print(f"      Download from: https://github.com/oschwartz10612/poppler-windows/releases")
            print(f"      Add to PATH or specify in pdf2image.convert_from_path()")
    except FileNotFoundError:
        print(f"    ✗ pdftoppm not found - Poppler NOT installed or not in PATH")
        print(f"      Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases")
        print(f"      Add poppler/bin to your PATH environment variable")
    except subprocess.TimeoutExpired:
        print(f"    - Timeout checking poppler (might still work)")
    except Exception as e:
        print(f"    - Could not check poppler: {e}")
        print(f"      If you get pdf2image errors, install poppler")
else:
    print("    - Skipped (pdf2image not installed)")

# Test 7: Simulate the actual OCR path
print("\n[7] Full OCR Pipeline Simulation")
if pytesseract and pdf2image:
    print("    Creating test image for OCR...")
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create a simple test image with text
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "TEST OCR", fill='black')

        print("    Running OCR on test image...")

        # Configure tesseract if env var is set
        if env_var:
            pytesseract.pytesseract.tesseract_cmd = env_var

        # Try OCR
        text = pytesseract.image_to_string(img)
        print(f"    ✓ OCR SUCCESS!")
        print(f"    Extracted text: '{text.strip()}'")

    except pytesseract.TesseractNotFoundError as e:
        print(f"    ✗ TESSERACT NOT FOUND during OCR")
        print(f"    Error: {e}")
        print(f"    This is the same error you're seeing in the CLI!")
    except Exception as e:
        print(f"    ✗ OCR FAILED: {type(e).__name__}")
        print(f"    Error: {e}")
        print(f"    This is the actual error causing 'OCR conversion failed'!")
else:
    print("    - Skipped (dependencies not installed)")

# Summary
print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)

issues = []

if not env_var and not config_path.exists():
    issues.append("⚠ No Tesseract path configured (env var or config.yaml)")

if env_var and not Path(env_var).exists():
    issues.append("✗ Tesseract path in env var does not exist")

if not pytesseract:
    issues.append("✗ pytesseract not installed - run: pip install pytesseract")

if not pdf2image:
    issues.append("✗ pdf2image not installed - run: pip install pdf2image")

if pytesseract:
    try:
        if env_var:
            pytesseract.pytesseract.tesseract_cmd = env_var
        pytesseract.get_tesseract_version()
    except:
        issues.append("✗ Tesseract executable not accessible")

if issues:
    print("\nISSUES FOUND:")
    for issue in issues:
        print(f"  {issue}")
    print("\nFIX THESE ISSUES TO ENABLE OCR")
else:
    print("\n✓ ALL CHECKS PASSED - OCR should work!")

print("\n" + "=" * 70)
print("Run this script on your test computer to see actual errors")
print("=" * 70)
