@echo off
setlocal

echo ========================================
echo GrantGuru -- Reset Environment
echo ========================================
echo.

pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"
popd

cd /d "%PROJECT_ROOT%"
echo Working from: %PROJECT_ROOT%
echo.

REM -----------------------------------------------------------------
REM 1. Delete Database
REM -----------------------------------------------------------------
if exist "Phase2_work\src\system_functions\delete_db_script.py" (
    echo [+] Running DB deletion script...
    
    REM Activate venv momentarily to run the python script
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
    )
    
    cd Phase2_work
    REM Ensure env vars are present if needed for connection
    set GG_USER=admin
    set GG_PASS=admin
    set DB_NAME=GrantGuruDB
    set HOST=localhost
    
    python -m src.system_functions.delete_db_script
    cd ..
    
    REM Deactivate isn't strictly necessary as we are about to delete it
) else (
    echo [!] Database deletion script not found -- skipping.
)

REM -----------------------------------------------------------------
REM 2. Remove Python Virtual Environment
REM -----------------------------------------------------------------
if exist ".venv" (
    echo [+] Removing .venv directory...
    rmdir /s /q ".venv"
) else (
    echo [!] No .venv found.
)

REM -----------------------------------------------------------------
REM 3. Remove Node Modules
REM -----------------------------------------------------------------
if exist "Phase3_work\UI\node_modules" (
    echo [+] Removing frontend node_modules...
    rmdir /s /q "Phase3_work\UI\node_modules"
) else (
    echo [!] No node_modules found.
)

REM -----------------------------------------------------------------
REM 4. Remove __pycache__
REM -----------------------------------------------------------------
echo [+] Removing __pycache__ directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo ========================================
echo Environment Reset Complete
echo ========================================
echo.
pause