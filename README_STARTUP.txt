# GrantGuru Setup and Startup Guide

## First Time Setup (Do This Once)

### Step 1: Install Prerequisites

Before running any scripts, you must install these programs:

1. **Python 3.12**
   - Download from: https://www.python.org/downloads/
   - During installation, CHECK "Add Python to PATH"
   - Verify installation: Open Command Prompt and type `py -3.12 --version`

2. **Node.js** (Choose ONE option):

   **Option A - nvm-windows (Recommended):**
   - Download from: https://github.com/coreybutler/nvm-windows/releases
   - Install the `nvm-setup.exe` file
   - Verify installation: Open Command Prompt and type `nvm version`

   **Option B - Direct Node.js:**
   - Download from: https://nodejs.org/
   - Install version 23.11.0 or latest LTS
   - Verify installation: Open Command Prompt and type `node -v`

3. **MySQL or PostgreSQL Database Server**

   **MySQL (Recommended for Windows):**
   - Download from: https://dev.mysql.com/downloads/installer/
   - Install MySQL Server
   - During setup, create a root password (you'll need this later)
   - Make sure the MySQL service is running

   **PostgreSQL (Alternative):**
   - Download from: https://www.postgresql.org/download/windows/
   - Install and remember your postgres password

### Step 2: Configure Database Credentials

**IMPORTANT:** Before running setup, you MUST update the database password in the scripts.

1. Open `setup.bat` in a text editor (Notepad)
2. Find these lines (around line 21-24):
   ```
   set GG_USER=root
   set GG_PASS=Kappa20205!
   set DB_NAME=GrantGuruDB
   set HOST=127.0.0.1
   ```
3. Change `GG_PASS=Kappa20205!` to match YOUR MySQL root password
4. Save the file

5. Repeat for `launcher.bat` (around line 31):
   ```
   set GG_PASS=F8F6iVoAlcXnLPll
   ```
   Change this to YOUR password

### Step 3: Run Setup Script

1. Open Command Prompt
2. Navigate to the GrantGuru folder: `cd C:\Users\YourName\Desktop\GrantGuru`
3. Run: `setup.bat`
4. Wait for the setup to complete (this may take 5-10 minutes)

The setup script will automatically:
- Create Python virtual environment
- Install all Python dependencies
- Install/configure Node.js
- Create the database
- Install all UI dependencies

### Step 4: Start the Application

After setup completes successfully:

1. Double-click `start_grantguru.bat` (or `launcher.bat`)
2. Two windows will open:
   - Flask Backend (runs on http://127.0.0.1:5000)
   - React Frontend (runs on http://localhost:5173)
3. Wait for both servers to finish starting
4. Open your browser to http://localhost:5173

## Daily Usage (After Initial Setup)

Once you've completed the first-time setup, you only need to:

1. Make sure MySQL service is running (should auto-start)
2. Double-click `start_grantguru.bat` or `launcher.bat`
3. Wait for both servers to start
4. Access at http://localhost:5173

### Alternative: Manual Startup

If you prefer to start servers individually:

1. **Terminal 1 - Flask Backend:**
   - Double-click `start_flask.bat`
   - Wait for "Running on http://127.0.0.1:5000"

2. **Terminal 2 - React Frontend:**
   - Double-click `start_react.bat`
   - Wait for the development server URL

## Project Structure

The GrantGuru project should have this structure:
```
GrantGuru/
├── setup.bat                    # One-time setup script
├── launcher.bat                 # Main application launcher
├── start_grantguru.bat         # Alternative launcher
├── start_flask.bat             # Backend only
├── start_react.bat             # Frontend only
├── README_STARTUP.txt          # This file
├── requirements.txt            # Python dependencies
├── venv/                       # Python virtual environment (created by setup)
├── Phase2_work/                # Database scripts
│   └── src/
│       └── system_functions/
│           └── create_db_script.py
├── Phase3_work/
│   ├── api/                    # Flask backend
│   └── UI/                     # React frontend
└── ...
```

## Troubleshooting

### Setup Issues

**"Python 3.12 not found" error:**
- Install Python 3.12 from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart Command Prompt after installation

**"nvm not found" or "npm not found" error:**
- Install nvm-windows from https://github.com/coreybutler/nvm-windows/releases
- OR install Node.js directly from https://nodejs.org/
- Restart Command Prompt after installation

**"Database creation failed" or "Access denied" error:**
- Make sure MySQL service is running (check Services app in Windows)
- Verify your database password is correct in `setup.bat` and `launcher.bat`
- Test connection manually: `mysql -u root -p` (enter your password)

**Setup script hangs or fails during npm install:**
- Check your internet connection
- Try running `npm install` manually: `cd Phase3_work\UI` then `npm install`
- If on corporate network, you may need to configure npm proxy settings

### Runtime Issues

**Flask won't start:**
- Check if virtual environment exists: `venv` folder should be in project root
- Activate venv and reinstall dependencies:
  ```
  call venv\Scripts\activate.bat
  pip install -r requirements.txt
  ```
- Ensure MySQL is running and credentials in launcher scripts are correct
- Check if port 5000 is already in use

**React won't start:**
- Check Node.js version: `node -v` should show v23.x.x or higher
- If using nvm, run `nvm use 23.11.0`
- Reinstall npm packages: `cd Phase3_work\UI` then `npm install`
- Check if port 5173 is already in use

**"Port already in use" error:**
- Close any existing Flask/React servers
- Open Task Manager (Ctrl+Shift+Esc) and end python.exe or node.exe processes
- Wait a few seconds and try again

**Permission errors:**
- Run Command Prompt as Administrator
- OR run PowerShell as Administrator and execute:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**Application opens but shows connection errors:**
- Make sure BOTH Flask and React servers are running
- Flask should show "Running on http://127.0.0.1:5000"
- Check browser console for errors (F12 in browser)
- Verify database credentials are correct

### Getting Help

**Still having issues?**
1. Read error messages carefully - they often indicate exactly what's wrong
2. Check that all prerequisites are properly installed
3. Verify database credentials match your actual MySQL setup
4. Make sure MySQL service is running
5. Try running `setup.bat` again if setup failed partway through

## Stopping the Servers

- Press `CTRL+C` in each terminal window
- Or simply close the terminal windows
- All data is saved in the database automatically

## Summary

**First time users:**
1. Install Python 3.12, Node.js/nvm, and MySQL
2. Update database password in `setup.bat` and `launcher.bat`
3. Run `setup.bat`
4. Run `launcher.bat` or `start_grantguru.bat`
5. Open browser to http://localhost:5173

**Daily users:**
1. Run `launcher.bat` or `start_grantguru.bat`
2. Open browser to http://localhost:5173
