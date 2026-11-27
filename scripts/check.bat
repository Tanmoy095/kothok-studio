@echo off
setlocal
cd /d "%~dp0.."
set "PYTHON=.venv\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"
"%PYTHON%" -m ruff check .
if errorlevel 1 exit /b %errorlevel%
"%PYTHON%" -m pytest
exit /b %errorlevel%
