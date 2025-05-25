@echo off
setlocal

rem Directory where this script resides
set BASE_DIR=%~dp0
set VENV_DIR=%BASE_DIR%venv

rem Create virtual environment on first run
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment in %VENV_DIR%
    python -m venv "%VENV_DIR%"
)

rem Activate the environment
call "%VENV_DIR%\Scripts\activate.bat"

rem Install Python dependencies and Turkish spaCy model
pip install -r "%BASE_DIR%requirements.txt"
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl
pip install "%BASE_DIR%"
python -m spacy link tr_core_news_md tr_core_news_md >nul 2>nul

rem Launch the Streamlit UI
streamlit run "%BASE_DIR%ui\app.py"
