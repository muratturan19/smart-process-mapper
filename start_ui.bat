@echo off
setlocal

rem Directory where this script resides
set BASE_DIR=%~dp0
set VENV_DIR=%BASE_DIR%venv
set FLAG_FILE=%VENV_DIR%\installed.flag
set CACHE_DIR=%BASE_DIR%hf_cache
if exist "%CACHE_DIR%\hub\models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1" (
    set HF_HOME=%CACHE_DIR%
    set TRANSFORMERS_CACHE=%CACHE_DIR%
) else (
    if not defined HF_HOME set HF_HOME=%CACHE_DIR%
    if not defined TRANSFORMERS_CACHE set TRANSFORMERS_CACHE=%HF_HOME%
)

echo BASE_DIR=%BASE_DIR%
echo VENV_DIR=%VENV_DIR%
echo HF_HOME=%HF_HOME%
echo TRANSFORMERS_CACHE=%TRANSFORMERS_CACHE%

rem Skip venv creation if marker exists but still verify dependencies
echo Checking for installation flag at %FLAG_FILE%...
if exist "%FLAG_FILE%" (
    echo Installation flag found - verifying dependencies.
    set SKIP_VENV_CREATION=1
) else (
    echo No installation flag found. Starting installation.
)


rem Create virtual environment and install packages on first run
if not defined SKIP_VENV_CREATION (
    if not exist "%VENV_DIR%\Scripts\python.exe" (
        echo Creating virtual environment in %VENV_DIR%...
        python -m venv "%VENV_DIR%"
        if %ERRORLEVEL% neq 0 (
            echo Failed to create virtual environment (%ERRORLEVEL%)
            goto install_fail
        ) else (
            echo Virtual environment created.
        )
    ) else (
        echo Virtual environment already exists.
    )

    echo Activating the environment...
    call "%VENV_DIR%\Scripts\activate.bat"
    if %ERRORLEVEL% neq 0 (
        echo Failed to activate virtual environment (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Environment activated.
    )

    echo Installing Python dependencies...
    pip install -r "%BASE_DIR%requirements.txt" >> "%BASE_DIR%install.log" 2>&1
    if %ERRORLEVEL% neq 0 (
        echo pip install requirements failed (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Requirements installed successfully.
    )

    echo Installing Turkish spaCy model...
    pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl >> "%BASE_DIR%install.log" 2>&1
    if %ERRORLEVEL% neq 0 (
        echo spaCy model install failed (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo spaCy model installed.
    )

    rem Append a dot so the path does not end with a bare backslash
    echo Installing local package...
    pip install "%BASE_DIR%." >> "%BASE_DIR%install.log" 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Local package install failed (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Local package installed.
    )



    echo Recording installed packages...
    pip list > "%BASE_DIR%installed_packages.log"
    if %ERRORLEVEL% neq 0 (
        echo Failed to record installed packages (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Installed packages recorded.
    )

    echo Creating installation marker...
    type nul > "%FLAG_FILE%"
    if %ERRORLEVEL% neq 0 (
        echo Failed to create installation marker (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Installation marker created.
    )
)

goto run_env

:run_env
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo Failed to activate environment (%ERRORLEVEL%)
    goto install_fail
) else (
    echo Environment activated.
)

rem Download the Kocdigital LLM weights if missing
python "%BASE_DIR%download_model.py" >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 (
    echo LLM weight download failed (%ERRORLEVEL%)
    goto install_fail
)

echo Verifying Python dependencies...
pip install --upgrade -r "%BASE_DIR%requirements.txt" >> "%BASE_DIR%install.log" 2>&1
if %ERRORLEVEL% neq 0 goto install_fail
echo Dependencies verified.

echo Checking Turkish spaCy model...
python -m spacy info tr_core_news_md >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing Turkish spaCy model...
    pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl >> "%BASE_DIR%install.log" 2>&1
    if %ERRORLEVEL% neq 0 goto install_fail
    echo spaCy model installed.
) else (
    echo Turkish spaCy model already installed.
)

echo Launching Streamlit UI...
start "" streamlit run "%BASE_DIR%ui\app.py"
pause
goto :eof

:install_fail
echo Installation failed with error code %ERRORLEVEL%. See log below.
type "%BASE_DIR%install.log"
pause
