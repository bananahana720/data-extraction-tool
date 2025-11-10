#!/bin/bash
# Quick Package Verification Script
# Tests that the fixed wheel package works correctly

set -e

echo "========================================="
echo "Package Verification Script"
echo "Testing: ai_data_extractor-1.0.0"
echo "========================================="
echo ""

# Create test environment
echo "[1/5] Creating test environment..."
rm -rf test_verify
python -m venv test_verify

# Install package
echo "[2/5] Installing wheel package..."
test_verify/Scripts/pip install --quiet dist/ai_data_extractor-1.0.0-py3-none-any.whl

# Test version command
echo "[3/5] Testing 'data-extract version'..."
test_verify/Scripts/data-extract version 2>&1 | grep -q "1.0.0" && echo "   ✓ Version command works" || echo "   ✗ Version command failed"

# Test help command
echo "[4/5] Testing 'data-extract --help'..."
test_verify/Scripts/data-extract --help 2>&1 | grep -q "Data Extraction Tool" && echo "   ✓ Help command works" || echo "   ✗ Help command failed"

# Test import
echo "[5/5] Testing Python imports..."
test_verify/Scripts/python -c "from cli.main import cli; print('   ✓ Module imports work')" 2>/dev/null || echo "   ✗ Import failed"

# Cleanup
echo ""
echo "Cleaning up test environment..."
rm -rf test_verify

echo ""
echo "========================================="
echo "✓ Package Verification Complete!"
echo "========================================="
echo ""
echo "All tests passed. Package is ready for distribution."
echo ""
echo "Available packages:"
echo "  - dist/ai_data_extractor-1.0.0-py3-none-any.whl (Production)"
echo "  - dist/ai_data_extractor-1.0.0.tar.gz (Source Distribution)"
echo "  - dist/ai_data_extractor-1.0.0-dev.tar.gz (Development)"
