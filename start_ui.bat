@echo off
set VENV_DIR=%~dp0venv
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
)
streamlit run "%~dp0\ui\app.py"
