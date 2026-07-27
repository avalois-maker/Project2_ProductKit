@echo off
REM Double-click this file to set up (first run only) and launch the app.
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

if not exist ".venv" (
    echo First run: setting up the app (this only happens once)...
    python -m venv .venv
    call ".venv\Scripts\activate.bat"
    pip install -q -r requirements.txt
) else (
    call ".venv\Scripts\activate.bat"
)

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo NOTE: .env was created from .env.example. Add your API keys to it, then re-run this.
    pause
    exit /b 1
)

echo Starting Feature Launch Kit... a browser tab will open automatically.
echo Close this window to stop the app.
cd src
python app_ui.py

pause
