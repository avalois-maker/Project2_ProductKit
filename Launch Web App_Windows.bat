@echo off
setlocal
REM Double-click this file to set up (first run only) and launch the app.
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "VENV_PY=%PROJECT_DIR%.venv\Scripts\python.exe"

if exist "%VENV_PY%" goto env_ready

echo First run: setting up the app (this only happens once)...
py -3 -m venv .venv
if errorlevel 1 goto venv_failed

"%VENV_PY%" -m pip install -q -r requirements.txt
if errorlevel 1 goto install_failed

:env_ready

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo NOTE: .env was created from .env.example. Add your API keys to it, then re-run this.
    pause
    exit /b 1
)

echo Starting Feature Launch Kit... a browser tab will open automatically.
echo Close this window to stop the app.
"%VENV_PY%" src\app_ui.py

pause
exit /b 0

:venv_failed
echo.
echo ERROR: Could not create the virtual environment.
echo Install Python 3 for Windows, or ensure the Python launcher is available.
pause
exit /b 1

:install_failed
echo.
echo ERROR: Could not install dependencies from requirements.txt.
pause
exit /b 1
