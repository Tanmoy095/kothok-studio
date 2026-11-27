@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo Run setup.bat first.& exit /b 1)
set "GRADIO_ANALYTICS_ENABLED=False"
".venv\Scripts\python.exe" app.py
if errorlevel 1 pause
