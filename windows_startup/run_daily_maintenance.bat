@echo off
REM Run daily grants maintenance (safe wrapper)
REM Usage: run_daily_maintenance.bat [once]

SETLOCAL ENABLEDELAYEDEXPANSION

REM Resolve script directory as project root
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set "PHASE2_DIR=%PROJECT_ROOT%\Phase2_work"
set "VENV_ACTIVATE=%PROJECT_ROOT%\.venv\Scripts\activate.bat"

if not exist "%PHASE2_DIR%" (
  echo Error: Phase2_work directory not found at "%PHASE2_DIR%"
  pause
  exit /b 1
)

if not exist "%VENV_ACTIVATE%" (
  echo Error: Virtual environment activate script not found at "%VENV_ACTIVATE%"
  echo Please create a virtual environment at %PROJECT_ROOT%\.venv and install dependencies.
  pause
  exit /b 1
)

REM Build timestamp for logfile
for /f "usebackq" %%i in (`powershell -NoProfile -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"`) do set TIMESTAMP=%%i
set "LOGFILE=%PHASE2_DIR%\daily_maintenance_%TIMESTAMP%.log"

echo Starting daily grants maintenance at %DATE% %TIME%
echo Log file: %LOGFILE%

pushd "%PHASE2_DIR%"
call "%VENV_ACTIVATE%"

REM If caller passed "once" as first argument, forward it to the Python script
set "PYARGS="
if /I "%1"=="once" set "PYARGS=--once"

echo Running: python -m src.system_functions.daily_grants_maintenance %PYARGS%
python -m src.system_functions.daily_grants_maintenance %PYARGS% > "%LOGFILE%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

echo.
echo Finished daily grants maintenance with exit code %EXITCODE% at %DATE% %TIME% >> "%LOGFILE%"
echo Finished with exit code %EXITCODE%

popd

if %EXITCODE% NEQ 0 (
  echo There was a problem. See the log at %LOGFILE% for details.
  exit /b %EXITCODE%
)

echo Success. Log saved to %LOGFILE%
exit /b 0
