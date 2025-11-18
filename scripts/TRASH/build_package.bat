@echo off
REM Build script for AI Data Extractor package (Windows)
REM Creates a distributable wheel package ready for installation

echo ======================================
echo AI Data Extractor - Package Builder
echo ======================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.11 or higher
    exit /b 1
)

REM Check Python version is 3.11+
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>nul
if errorlevel 1 (
    echo ERROR: Python 3.11 or higher is required
    python --version
    exit /b 1
)

echo [1/6] Checking Python version...
python --version
echo.

REM Clean previous builds
echo [2/6] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist src\ai_data_extractor.egg-info rmdir /s /q src\ai_data_extractor.egg-info
echo    - Removed old build artifacts
echo.

REM Install build dependencies
echo [3/6] Installing build dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install --upgrade build hatchling >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install build dependencies
    exit /b 1
)
echo    - Build tools installed
echo.

REM Run tests (optional, comment out to skip)
echo [4/6] Running tests...
python -m pytest tests/ -q --tb=no
if errorlevel 1 (
    echo WARNING: Some tests failed. Continue? (Ctrl+C to cancel)
    pause
)
echo    - Tests completed
echo.

REM Build package
echo [5/6] Building package...
python -m build
if errorlevel 1 (
    echo ERROR: Package build failed
    exit /b 1
)
echo    - Package built successfully
echo.

REM Verify package
echo [6/6] Verifying package contents...
if not exist dist\*.whl (
    echo ERROR: No wheel file found in dist/
    exit /b 1
)

for %%f in (dist\*.whl) do (
    echo    - Wheel: %%~nxf
    echo    - Size: %%~zf bytes
)
echo.

REM Test installation (dry run)
echo Testing package installation (dry-run)...
for %%f in (dist\*.whl) do (
    python -m pip install "%%f" --dry-run >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Package installation check failed
    ) else (
        echo    - Installation check passed
    )
)
echo.

echo ======================================
echo SUCCESS! Package built successfully
echo ======================================
echo.
echo Distribution files:
dir /b dist
echo.
echo Next steps:
echo 1. Test installation: pip install dist\ai_data_extractor-1.0.0-py3-none-any.whl
echo 2. Distribute to pilot users
echo 3. Or upload to internal PyPI
echo.
echo For installation instructions, see INSTALL.md
echo.

pause
