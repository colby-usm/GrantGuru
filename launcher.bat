@echo off
TITLE GrantGuru Launcher

:: ==========================================
:: GrantGuru Windows Launcher
:: ==========================================

:: Define Colors
set "GREEN=[32m"
set "RED=[31m"
set "YELLOW=[33m"
set "NC=[0m"

echo %GREEN%=== GrantGuru Launcher ===%NC%

:: 1. Setup Paths & Credentials
:: ==========================================
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set "PHASE2_DIR=%PROJECT_ROOT%\Phase2_work"
set "PHASE3_DIR=%PROJECT_ROOT%\Phase3_work"
set "UI_DIR=%PHASE3_DIR%\UI"
set "VENV_ACTIVATE=%PROJECT_ROOT%\.venv\Scripts\activate.bat"

:: DATABASE CONFIGURATION
:: Check if these match your actual MySQL setup!
set "DB_NAME=GrantGuruDB"
set "HOST=localhost"
set "GG_USER=root"
set "GG_PASS=F8F6iVoAlcXnLPll"

:: 2. Verify Prerequisites
:: ==========================================
if not exist "%VENV_ACTIVATE%" (
    echo %RED%Error: Virtual environment not found at .venv\Scripts\activate.bat%NC%
    echo Please run setup.sh first.
    pause
    exit /b 1
)

if not exist "%PHASE2_DIR%" (
    echo %RED%Error: Phase2_work directory not found%NC%
    pause
    exit /b 1
)

echo %GREEN%All paths verified.%NC%

:: 3. Run Database Script
:: ==========================================
echo.
echo %YELLOW%Step 1: Checking/Creating Database...%NC%

call "%VENV_ACTIVATE%"
cd "%PHASE2_DIR%"

:: The script will now see GG_USER and GG_PASS
python -m src.system_functions.create_db_script
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo %RED%Database creation failed.%NC%
    echo.
    echo If the error is "Access denied", check:
    echo 1. Is your MySQL server running?
    echo 2. Is your password actually '%GG_PASS%'?
    echo 3. Does the user '%GG_USER%' exist?
    pause
    exit /b 1
)
echo %GREEN%Database check complete.%NC%

:: 4. Launch Flask Backend (T1)
:: ==========================================
echo.
echo %YELLOW%Step 2: Launching Flask Backend (New Window)...%NC%

:: We pass the variables into the new window specifically
start "GrantGuru Backend" cmd /k "cd /d "%PHASE3_DIR%" && call "%VENV_ACTIVATE%" && set FLASK_APP=api && set FLASK_RUN_APP=api:create_app && set DB_NAME=%DB_NAME% && set HOST=%HOST% && set GG_USER=%GG_USER% && set GG_PASS=%GG_PASS% && echo Starting Flask... && flask run --host=127.0.0.1 --port=5000"

:: Wait 2 seconds
timeout /t 2 /nobreak >nul

:: 5. Launch React Frontend (T2)
:: ==========================================
echo.
echo %YELLOW%Step 3: Launching React Frontend (New Window)...%NC%

start "GrantGuru Frontend" cmd /k "cd /d "%UI_DIR%" && echo Starting React... && npm run dev"

echo.
echo %GREEN%=== Launch Complete! ===%NC%
echo Backend running on http://127.0.0.1:5000
echo Frontend launching in separate window...
echo.