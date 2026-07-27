#!/bin/bash
# Double-click this file to set up (first run only) and launch the app.
cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
    echo "First run: setting up the app (this only happens once)..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -r requirements.txt
else
    source .venv/bin/activate
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "NOTE: .env was created from .env.example. Add your API keys to it, then re-run this."
    read -p "Press Enter to close..."
    exit 1
fi

echo "Starting Feature Launch Kit... a browser tab will open automatically."
echo "Close this window to stop the app."
cd src
python3 app_ui.py
