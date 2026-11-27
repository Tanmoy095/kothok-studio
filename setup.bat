@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul || (echo Python 3.10 or newer is required. Install Python and enable Add to PATH.& exit /b 1)
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" || (echo Install Python 3.10 or newer.& exit /b 1)
if not exist ".venv\Scripts\python.exe" python -m venv .venv
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements\app.txt -r requirements\dev.txt
if errorlevel 1 exit /b %errorlevel%
echo Setup complete. Start Kothok with run.bat.
