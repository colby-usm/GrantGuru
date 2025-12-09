@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo GrantGuru Full Installation (Windows)
echo ========================================
echo.

REM -----------------------------------------------------------------
REM 1. Setup Directories
REM -----------------------------------------------------------------
REM Get the directory of this script, move up one level for Project Root
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"
popd

cd /d "%PROJECT_ROOT%"
echo Project Root: %PROJECT_ROOT%
echo.

REM -----------------------------------------------------------------
REM 2. Verify Prerequisites
REM -----------------------------------------------------------------
echo Checking prerequisites...

REM Check Python 3.12
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.12 not found. Please install it and try again.
    pause
    exit /b 1
) else (
    echo [OK] Python 3.12 found.
)

REM Check Node/npm
call npm -v >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found. Please install Node.js.
    pause
    exit /b 1
) else (
    echo [OK] npm found.
)
echo.

REM -----------------------------------------------------------------
REM 3. Python Environment Setup
REM -----------------------------------------------------------------
echo === Python Setup ===

if not exist ".venv" (
    echo Creating virtual environment...
    py -3.12 -m venv .venv
    echo [OK] .venv created.
) else (
    echo [INFO] .venv already exists.
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)
echo [OK] Python dependencies installed.
echo.

REM -----------------------------------------------------------------
REM 4. UI Dependencies
REM -----------------------------------------------------------------
echo === UI Setup ===
set "UI_DIR=%PROJECT_ROOT%\Phase3_work\UI"

if not exist "%UI_DIR%" (
    echo [ERROR] UI directory not found at %UI_DIR%
    pause
    exit /b 1
)

cd /d "%UI_DIR%"
echo Installing npm packages...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install npm packages.
    pause
    exit /b 1
)
echo [OK] UI dependencies installed.
echo.

REM -----------------------------------------------------------------
REM 5. Database Setup
REM -----------------------------------------------------------------
echo === Database Setup ===

REM Navigate to Phase2 logic
cd /d "%PROJECT_ROOT%\Phase2_work"

REM Set Database Env Vars
set GG_USER=root
set DB_NAME=GrantGuruDB
set HOST=localhost

echo Creating Database %DB_NAME%...
python -m src.system_functions.create_db_script
if errorlevel 1 (
    echo [ERROR] Database creation failed.
    pause
    exit /b 1
)
echo [OK] Database created (or already exists).

REM -----------------------------------------------------------------
REM 6. Insert Demo Data
REM -----------------------------------------------------------------
echo.
echo === Inserting Demo Data ===

set "GRANTS_JSON=src\test_suites\grants_data.json"

if not exist "%GRANTS_JSON%" (
    echo [ERROR] Grants data file not found at %GRANTS_JSON%
    pause
    exit /b 1
)

echo Running insertion script...
python -m src.system_functions.insert_cleaned_grant "%GRANTS_JSON%"
if errorlevel 1 (
    echo [ERROR] Data insertion failed.
    pause
    exit /b 1
)
echo [OK] Data inserted successfully.

REM -----------------------------------------------------------------
REM Done
REM -----------------------------------------------------------------
echo.
echo ========================================
echo GrantGuru Setup Complete!
echo ========================================
echo You may now run run.bat to launch the application.
echo.
echo Credentials:
echo User:     %GG_USER%
echo Password: %GG_PASS%
echo Database: %DB_NAME%
echo Host:     %HOST%
pause