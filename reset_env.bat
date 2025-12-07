@echo off

set "GG_PASS=password"
setlocal EnableDelayedExpansion
TITLE GrantGuru Environment Reset

echo ======================================
echo   GrantGuru - Reset Environment
echo ======================================
echo.

:: 1. Setup Paths & Credentials
:: ==========================================
set "PROJECT_ROOT=%~dp0"
:: Remove trailing backslash if present
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set "VENV_DIR=%PROJECT_ROOT%\.venv"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"
set "PHASE2_DIR=%PROJECT_ROOT%\Phase2_work"
set "NODE_MODULES=%PROJECT_ROOT%\Phase3_work\UI\frontend\node_modules"

:: DB CREDENTIALS
set "DB_NAME=GrantGuruDB"
set "HOST=localhost"
set "GG_USER=root"

:: 2. Run DB Deletion Script
:: ==========================================
echo [Step 1] Deleting Database...

if exist "!VENV_ACTIVATE!" (
    call "!VENV_ACTIVATE!"
    
    if exist "!PHASE2_DIR!\src\system_functions\delete_db_script.py" (
        cd "!PHASE2_DIR!"
        echo    Running Python deletion script...
        
        python -m src.system_functions.delete_db_script
        
        if !ERRORLEVEL! EQU 0 (
            echo    Database deleted successfully.
        ) else (
            echo    Database deletion failed ^(or DB did not exist^).
        )
        :: Return to root
        cd "!PROJECT_ROOT!"
    ) else (
        echo    Could not find delete_db_script.py
    )
) else (
    echo    No virtual environment found. Skipping DB deletion.
)

:: 3. Remove Virtual Environment
:: ==========================================
echo.
echo [Step 2] Removing .venv folder...
if exist "!VENV_DIR!" (
    rmdir /s /q "!VENV_DIR!"
    echo    .venv removed.
) else (
    echo    .venv not found.
)

:: 4. Remove Node Modules
:: ==========================================
echo.
echo [Step 3] Removing node_modules...
if exist "!NODE_MODULES!" (
    rmdir /s /q "!NODE_MODULES!"
    echo    node_modules removed.
) else (
    echo    node_modules not found.
)

:: 5. Clear Python Cache
:: ==========================================
echo.
echo [Step 4] Cleaning up __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo    Removing "%%d"
    rd /s /q "%%d"
)
echo    Cache cleared.

echo.
echo ======================================
echo  Environment Reset Complete
echo ======================================
echo.
echo Next steps:
echo    Run setup.sh to rebuild everything.
echo.
pause