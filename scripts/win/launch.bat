@echo off

rem Change the current working directory to the directory of the batch script
cd /d %~dp0
cd ..\..

if not exist pyproject.toml (
    echo "Error: pyproject.toml not found in the current directory."
    exit /b 1
) else (
    echo "pyproject.toml found. Continuing with the script."
)

rem Check if Python is installed
uv --version > nul 2>&1
if errorlevel 1 (
    echo UV needs to be installed for this script to work. Refer to Installation instructions here: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

rem Install uv and use uv to run script
#pip install uv
uv run --no-group dev scripts/main.py