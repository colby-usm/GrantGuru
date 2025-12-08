# GrantGuru Windows Startup Scripts

## Quick Start

### Easy Method (Recommended)
1. Double-click `start_grantguru.bat`
2. Two windows will open automatically (Flask backend and React frontend)
3. Wait for both servers to start
4. Access the application at the URL shown in the React window (usually http://localhost:5173)

### Manual Method
If you prefer to start servers individually:

1. **Terminal 1 - Flask Backend:**
   - Double-click `start_flask.bat`
   - Wait for "Running on http://127.0.0.1:5000"

2. **Terminal 2 - React Frontend:**
   - Double-click `start_react.bat`
   - Wait for the development server URL

## Files Included

- `start_grantguru.bat` - Main launcher (starts both servers)
- `start_flask.bat` - Flask backend only
- `start_react.bat` - React frontend only
- `README_STARTUP.txt` - This file

## Prerequisites

Before running these scripts, ensure you have:

1. **Python 3.12** installed with virtual environment created
   ```
   python -m venv venv
   pip install -r requirements.txt
   ```

2. **Node.js 23.11.0** installed via nvm-windows
   ```
   nvm install 23.11.0
   cd Phase3_work\UI
   npm install
   ```

3. **MySQL Database** configured with:
   - Username: root
   - Password: 
   - Database: GrantGuruDB
   - Host: 127.0.0.1

## Configuration

To change database credentials, edit `start_flask.bat` and modify these lines:
```batch
set GG_USER=root
set GG_PASS=Kappa20205!
set DB_NAME=GrantGuruDB
set HOST=127.0.0.1
```

## File Placement

All `.bat` files should be placed in the **GrantGuru project root directory**:
```
GrantGuru/
├── start_grantguru.bat
├── start_flask.bat
├── start_react.bat
├── README_STARTUP.txt
├── venv/
├── Phase3_work/
│   ├── api/
│   └── UI/
└── requirements.txt
```

## Troubleshooting

**Flask won't start:**
- Check if virtual environment exists: `venv` folder should be in project root
- Verify all Python dependencies installed: `pip install -r requirements.txt`
- Ensure MySQL is running with correct credentials

**React won't start:**
- Check Node.js version: `node -v` should show v23.11.0
- Run `nvm use 23.11.0` if needed
- Verify npm packages installed: `cd Phase3_work\UI` then `npm install`

**Port already in use:**
- Close any existing Flask/React servers
- Check Task Manager for python.exe or node.exe processes

**Permission errors:**
- Run PowerShell as Administrator and execute:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Stopping the Servers

- Press `CTRL+C` in each terminal window
- Or simply close the terminal windows

## Need Help?

Refer to the main HOWTO.MD for detailed setup instructions.
