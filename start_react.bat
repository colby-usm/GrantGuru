@echo off
REM GrantGuru React Frontend Startup Script

echo ======================================
echo Starting GrantGuru React Frontend
echo ======================================
echo.

REM Use correct Node.js version
echo Setting Node.js version to 23.11.0...
call nvm use 23.11.0

REM Navigate to UI directory
echo Navigating to UI directory...
cd Phase3_work\UI

REM Start development server
echo.
echo Starting React development server...
echo Press CTRL+C to stop the server
echo ======================================
echo.
npm run dev

pause
