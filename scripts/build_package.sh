#!/bin/bash
# Build script for AI Data Extractor package (Linux/Mac)
# Creates a distributable wheel package ready for installation

set -e  # Exit on error

echo "======================================"
echo "AI Data Extractor - Package Builder"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

# Check Python version is 3.11+
python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null || {
    echo "ERROR: Python 3.11 or higher is required"
    python3 --version
    exit 1
}

echo "[1/6] Checking Python version..."
python3 --version
echo ""

# Clean previous builds
echo "[2/6] Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info
echo "   - Removed old build artifacts"
echo ""

# Install build dependencies
echo "[3/6] Installing build dependencies..."
python3 -m pip install --upgrade pip >/dev/null 2>&1
python3 -m pip install --upgrade build hatchling >/dev/null 2>&1
echo "   - Build tools installed"
echo ""

# Run tests (optional, comment out to skip)
echo "[4/6] Running tests..."
python3 -m pytest tests/ -q --tb=no || {
    echo "WARNING: Some tests failed. Continue? (Ctrl+C to cancel, Enter to continue)"
    read -r
}
echo "   - Tests completed"
echo ""

# Build package
echo "[5/6] Building package..."
python3 -m build
echo "   - Package built successfully"
echo ""

# Verify package
echo "[6/6] Verifying package contents..."
if [ ! -f dist/*.whl ]; then
    echo "ERROR: No wheel file found in dist/"
    exit 1
fi

for file in dist/*.whl; do
    echo "   - Wheel: $(basename "$file")"
    echo "   - Size: $(du -h "$file" | cut -f1)"
done
echo ""

# Test installation (dry run)
echo "Testing package installation (dry-run)..."
for file in dist/*.whl; do
    python3 -m pip install "$file" --dry-run >/dev/null 2>&1 && {
        echo "   - Installation check passed"
    } || {
        echo "WARNING: Package installation check failed"
    }
done
echo ""

echo "======================================"
echo "SUCCESS! Package built successfully"
echo "======================================"
echo ""
echo "Distribution files:"
ls -lh dist/
echo ""
echo "Next steps:"
echo "1. Test installation: pip install dist/ai_data_extractor-1.0.0-py3-none-any.whl"
echo "2. Distribute to pilot users"
echo "3. Or upload to internal PyPI"
echo ""
echo "For installation instructions, see INSTALL.md"
echo ""
