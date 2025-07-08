@echo off
REM =============================================================================
REM ==                   Project Setup Script                                 ==
REM ==     Solves variable expansion issue with "Delayed Expansion"           ==
REM =============================================================================

REM Enables Delayed Expansion. Essential for reading variables inside blocks.
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set TOOLS_REQ_FILE=%SCRIPT_DIR%tools-requirements.txt
set TEMP_DEPS_FILE=%SCRIPT_DIR%temp_deps.txt

echo.
echo [STEP 1 of 5] Checking Python installation...
python --version >nul 2>&1 || (echo [ERROR] Python not found. & pause & exit /b 1)
echo Python found.

echo.
echo [STEP 2 of 5] Cleaning and creating new virtual environment 'venv'...
if exist venv ( rmdir /s /q venv )
python -m venv venv || (echo [ERROR] Failed to create virtual environment. & pause & exit /b 1)

echo.
echo [STEP 3 of 5] Activating environment and installing dependencies...
call venv\Scripts\activate.bat

echo Environment activated.
if exist "%TOOLS_REQ_FILE%" (
    echo Installing development tools...
    pip install -r "%TOOLS_REQ_FILE%" --quiet || (echo [ERROR] Failed to install tools. & pause & exit /b 1)
)

echo Discovering project dependencies...
python modules/generate_requirements.py --discover

if not exist "%TEMP_DEPS_FILE%" (
    echo [INFO] No project dependencies discovered for installation.
) else (
    REM Read the file content into the variable
    FOR /F "usebackq tokens=*" %%i IN ("%TEMP_DEPS_FILE%") DO SET "PACKAGES_TO_INSTALL=%%i"
    
    echo Installing project dependencies...
    REM Use !VARIABLES! instead of %VARIABLES% due to delayed expansion
    pip install !PACKAGES_TO_INSTALL! || (echo [ERROR] Failed to install project dependencies. & pause & exit /b 1)
    
    del "%TEMP_DEPS_FILE%"
)

echo.
echo [STEP 4 of 5] Generating final 'requirements.txt' file...
python modules/generate_requirements.py || (echo [ERROR] Failed to generate final 'requirements.txt'. & pause & exit /b 1)

echo.
echo [STEP 5 of 5] Process completed.
echo ----------------------------------------------------------------
echo.
echo  PROJECT READY AND CONFIGURED
echo.
echo   - Virtual environment created in 'venv'.
echo   - Dependencies installed.
echo   - 'requirements.txt' generated with versions.
echo.
echo   To get started, activate the environment: .\venv\Scripts\activate
echo.
echo ----------------------------------------------------------------

pause
endlocal
