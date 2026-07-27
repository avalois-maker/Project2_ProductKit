@echo off
set "PROJECT_DIR=C:\Users\anura\Desktop\Ironhack\Week-3\Project2_ProductKit"

call "%PROJECT_DIR%\.venv\Scripts\activate.bat"
cd /d "%PROJECT_DIR%\src"

echo Starting Feature Launch Kit... a browser tab will open automatically.
echo Close this window to stop the app.
python app_ui.py

pause
