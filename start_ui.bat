@echo off
setlocal

rem Directory where this script resides
set BASE_DIR=%~dp0
set VENV_DIR=%BASE_DIR%venv
set FLAG_FILE=%VENV_DIR%\installed.flag
set HF_HOME=%BASE_DIR%hf_cache

echo BASE_DIR=%BASE_DIR%
echo VENV_DIR=%VENV_DIR%
echo HF_HOME=%HF_HOME%

rem Skip installation if marker exists
echo Checking for installation flag at %FLAG_FILE%...
if exist "%FLAG_FILE%" (
    echo Installation flag found - skipping setup.
    goto run_env
) else (
    echo No installation flag found. Starting installation.
)


rem Create virtual environment and install packages on first run
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo Virtual environment created.
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

    echo Linking spaCy model...
    python -m spacy link tr_core_news_md tr_core_news_md >> "%BASE_DIR%install.log" 2>&1
    if %ERRORLEVEL% neq 0 (
        echo spaCy model link failed (%ERRORLEVEL%)
        goto install_fail
    ) else (
        echo spaCy model linked.
    )

    echo Checking for Kocdigital LLM weights...
    if not exist "%HF_HOME%\hub\models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1" (
        echo Downloading Kocdigital LLM weights...
        "%VENV_DIR%\Scripts\huggingface-cli.exe" download KOCDIGITAL/Kocdigital-LLM-8b-v0.1 >> "%BASE_DIR%install.log" 2>&1
        if %ERRORLEVEL% neq 0 (
            echo LLM weight download failed (%ERRORLEVEL%)
            goto install_fail
        ) else (
            echo LLM weights downloaded.
        )
    ) else (
        echo Kocdigital LLM weights already downloaded.
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

echo Launching Streamlit UI...
start "" streamlit run "%BASE_DIR%ui\app.py"
pause
goto :eof

:install_fail
echo Installation failed with error code %ERRORLEVEL%. See log below.
type "%BASE_DIR%install.log"
pause
