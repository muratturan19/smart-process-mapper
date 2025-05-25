#!/usr/bin/env bash
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$HERE/venv/bin/activate" ]; then
    . "$HERE/venv/bin/activate"
fi
streamlit run "$HERE/ui/app.py"

