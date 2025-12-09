@echo off
REM GrantGuru Full Setup Script for Windows
REM Sets up Python venv, installs dependencies, configures Node via nvm,
REM and installs UI dependencies.

setlocal enabledelayedexpansion

echo ========================================
echo GrantGuru Initial Setup
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"
cd ..

REM ###############################################################################
REM Set Database Environment Variables
REM ###############################################################################

echo Setting database environment variables...
set GG_USER=root
set GG_PASS=Kappa20205!
set DB_NAME=GrantGuruDB
set HOST=127.0.0.1
echo [OK] Environment variables set
echo.

REM ###############################################################################
REM 1. Verify prerequisites
REM ###############################################################################

echo Checking system prerequisites...
echo.

REM Check Python 3.12
py -3.12 --version 2>nul | findstr /C:"3.12" >nul
if errorlevel 1 (
    echo [ERROR] Python 3.12 not found. Install Python 3.12 and retry.
    pause
    exit /b 1
) else (
    echo [OK] Python 3.12 found
)

REM Check Node/nvm
nvm version >nul 2>&1
if errorlevel 1 (
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Neither nvm nor npm found. Install Node.js or nvm-windows first.
        pause
        exit /b 1
    ) else (
        echo [WARNING] nvm not found, using system-wide npm
        set USE_NVM=false
    )
) else (
    echo [OK] nvm found, will use nvm to manage Node
    set USE_NVM=true
)

echo.

REM ###############################################################################
REM 2. Python environment setup
REM ###############################################################################

echo ========================================
echo Python Environment Setup
echo ========================================
echo.

if not exist "venv\" (
    echo Creating virtual environment...
    py -3.12 -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists, skipping
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

echo.

REM ###############################################################################
REM 3. Node.js setup (nvm or system npm)
REM ###############################################################################

echo ========================================
echo Node.js Environment Setup
echo ========================================
echo.

set NODE_VERSION=23.11.0

if "%USE_NVM%"=="true" (
    REM Check if Node version is installed
    nvm list | findstr /C:"%NODE_VERSION%" >nul
    if errorlevel 1 (
        echo Installing Node.js %NODE_VERSION% via nvm...
        nvm install %NODE_VERSION%
        if errorlevel 1 (
            echo [ERROR] Failed to install Node.js via nvm
            pause
            exit /b 1
        )
        echo [OK] Node.js %NODE_VERSION% installed via nvm
    ) else (
        echo [OK] Node.js %NODE_VERSION% already installed via nvm
    )
    
    echo.
    echo Switching to Node.js %NODE_VERSION% via nvm...
    nvm use %NODE_VERSION%
    if errorlevel 1 (
        echo [ERROR] Failed to switch Node.js version
        pause
        exit /b 1
    )
) else (
    echo Using system-wide npm and Node.js
    node -v
)

echo.

REM ###############################################################################
REM 4. Create Database
REM ###############################################################################

echo ========================================
echo Creating Database
echo ========================================
echo.

if exist "create_db_script.py" (
    echo Running database creation script...
    python create_db_script.py
    if errorlevel 1 (
        echo [WARNING] Database creation encountered an issue
        echo This may be normal if database already exists
    ) else (
        echo [OK] Database created successfully
    )
) else (
    echo [WARNING] create_db_script.py not found, skipping database creation
    echo You may need to create the database manually
)

echo.

REM ###############################################################################
REM 5. Install UI dependencies
REM ###############################################################################

echo ========================================
echo Installing UI Dependencies
echo ========================================
echo.

set UI_DIR=Phase3_work\UI

if not exist "%UI_DIR%\" (
    echo [ERROR] UI directory %UI_DIR% not found.
    pause
    exit /b 1
)

cd "%UI_DIR%"

echo Installing npm packages...
npm install
if errorlevel 1 (
    echo [ERROR] Failed to install npm dependencies
    cd ..\..
    pause
    exit /b 1
)
echo [OK] npm dependencies installed

cd ..\..

echo.

REM ###############################################################################
REM DONE
REM ###############################################################################

echo ========================================
echo GrantGuru Setup Complete!
echo ========================================
echo.
echo You may now run start_grantguru.bat to launch the application.
echo.

pause