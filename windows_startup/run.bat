@echo off
REM ===========================================================================
REM File:        run.bat
REM Description: This script:
REM 1. Starts the Flask backend (T1)
REM 2. Starts the React frontend (T2)
REM Author:      James Tedder
REM Date:        2025-12-08
REM ===========================================================================

setlocal

REM -----------------------------------------------------------------
REM Configure Paths
REM -----------------------------------------------------------------
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"
popd

set "VENV_ACTIVATE=%PROJECT_ROOT%\.venv\Scripts\activate.bat"
set "PHASE3_DIR=%PROJECT_ROOT%\Phase3_work"
set "UI_DIR=%PROJECT_ROOT%\Phase3_work\UI"

REM -----------------------------------------------------------------
REM Set Environment Variables
REM -----------------------------------------------------------------
set DB_NAME=GrantGuruDB
set HOST=localhost
set GG_USER=root

set FLASK_APP=api
set FLASK_RUN_APP=api:create_app

echo ========================================
echo GrantGuru Launcher
echo ========================================
echo Project Root: %PROJECT_ROOT%
echo.

if not exist "%VENV_ACTIVATE%" (
    echo [ERROR] Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM -----------------------------------------------------------------
REM Launch Flask Backend (New Window)
REM -----------------------------------------------------------------
echo Launching Flask Backend...
start "GrantGuru Backend" cmd /k "cd /d %PHASE3_DIR% && call "%VENV_ACTIVATE%" && flask run --host=127.0.0.1 --port=5000"

REM -----------------------------------------------------------------
REM Launch React Frontend (New Window)
REM -----------------------------------------------------------------
echo Launching React Frontend...
REM We wait 2 seconds to let Flask initialize (optional simulation)
timeout /t 2 /nobreak >nul
start "GrantGuru Frontend" cmd /k "cd /d %UI_DIR% && npm run dev"

echo.
echo [OK] Services launched in new windows.
echo To stop servers, close the newly opened terminal windows.
pause