@echo off
setlocal enabledelayedexpansion

rem -----------------------------------------------------------------------------
rem Run Black/Ruff/mypy from Windows (faster than WSL for large trees).
rem Usage: double-click or run `scripts\run_quality_gates_windows.cmd`.
rem -----------------------------------------------------------------------------

set PROJECT_DIR=%~dp0..
pushd "%PROJECT_DIR%" >NUL

rem Detect virtual environment (prefer .venv, fall back to my_venv).
set VENV_DIR=%PROJECT_DIR%\.venv
if not exist "%VENV_DIR%\Scripts\python.exe" (
    set VENV_DIR=%PROJECT_DIR%\my_venv
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [ERROR] Could not find virtual environment. Expected:
    echo         %PROJECT_DIR%\.venv  or  %PROJECT_DIR%\my_venv
    echo Please create/activate the venv from Windows first.
    exit /b 1
)

echo.
echo [INFO] Activating virtual environment at %VENV_DIR%
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

echo.
echo [INFO] Running Black...
black src tests
if errorlevel 1 goto :error

echo.
echo [INFO] Running Ruff...
ruff check src tests
if errorlevel 1 goto :error

echo.
echo [INFO] Running mypy...
mypy src/data_extract
if errorlevel 1 goto :error

echo.
echo [SUCCESS] Quality gates completed.
goto :eof

:error
echo.
echo [FAIL] Quality gates stopped due to the error above.
exit /b 1

