@echo off
REM GrantGuru Flask Backend Startup Script

echo ======================================
echo Starting GrantGuru Flask Backend
echo ======================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Set database environment variables
echo Setting environment variables...
set GG_USER=root
set GG_PASS=Kappa20205!
set DB_NAME=GrantGuruDB
set HOST=127.0.0.1

REM Set Flask environment variables
set FLASK_APP=api
set FLASK_RUN_APP=api:create_app

REM Navigate to Phase3_work directory
echo Navigating to Phase3_work directory...
cd Phase3_work

REM Start Flask server
echo.
echo Starting Flask server on http://127.0.0.1:5000
echo Press CTRL+C to stop the server
echo ======================================
echo.
flask run --host=127.0.0.1 --port=5000

pause
