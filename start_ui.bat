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
pip install -r "%BASE_DIR%requirements.txt" >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 goto install_fail
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 goto install_fail
pip install "%BASE_DIR%" >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 goto install_fail
python -m spacy link tr_core_news_md tr_core_news_md >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 goto install_fail

rem Record installed packages
pip list > "%BASE_DIR%installed_packages.log"

rem Launch the Streamlit UI in a new window
start "" streamlit run "%BASE_DIR%ui\app.py"
pause
goto :eof

:install_fail
echo Installation failed. See log below.
type "%BASE_DIR%install.log"
pause
