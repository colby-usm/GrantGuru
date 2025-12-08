@echo off
REM GrantGuru Application Launcher
REM This script starts both Flask backend and React frontend in separate windows

echo ======================================
echo GrantGuru Application Launcher
echo ======================================
echo.
echo This will open two windows:
echo 1. Flask Backend (Terminal 1)
echo 2. React Frontend (Terminal 2)
echo.
echo Keep both windows open while using the application.
echo Press CTRL+C in each window to stop the servers.
echo ======================================
echo.

REM Start Flask backend in new window
echo Starting Flask backend...
start "GrantGuru Flask Backend" cmd /k "%~dp0start_flask.bat"

REM Wait a few seconds for Flask to start
timeout /t 3 /nobreak >nul

REM Start React frontend in new window
echo Starting React frontend...
start "GrantGuru React Frontend" cmd /k "%~dp0start_react.bat"

echo.
echo Both servers are starting...
echo Check the opened windows for status.
echo ======================================
echo.
echo You can close this window now.
pause
