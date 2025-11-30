# GrantGuru Setup Guide

## Overview

This application requires two terminal sessions running concurrently:

- **Terminal 1 (T1)**: Flask backend server
- **Terminal 2 (T2)**: React development server

> **Note**: These will eventually be combined into a single Python script. For now, separate terminals facilitate debugging and feature development.

---

## Initial Setup (One-Time)

### Prerequisites

- Python 3.12
- Node.js (version 23.11.0)
- nvm (Node Version Manager)

### 1. Python Environment Setup

```bash
# Navigate to project root
cd GrantGuru

# Create virtual environment (choose one method)
python3.12 -m venv venv
# OR using conda:
# conda create -n grantguru python=3.12

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR on Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Node.js Environment Setup

```bash
# Install Node.js version 23.11.0
nvm install 23.11.0

# Navigate to UI directory
cd Phase3_work/UI

# Install npm dependencies
npm install
```

---

## Running the Application

### Terminal 1: Flask Backend

```bash
# Activate Python virtual environment
source venv/bin/activate  # Adjust path if needed

# Set Flask environment variables
export FLASK_APP=api
export FLASK_RUN_APP=api:create_app

# Navigate to UI directory
cd Phase3_work/UI

# Start Flask server
flask run --host=127.0.0.1 --port=5000
```

**Expected output**: Flask server running on `http://127.0.0.1:5000`

---

### Terminal 2: React Development Server

```bash
# Use correct Node.js version
nvm use 23.11.0

# Navigate to UI directory
cd Phase3_work/UI

# Start development server
npm run dev
```

**Expected output**: Development server running (typically on `http://localhost:5173` for Vite)

---

## Troubleshooting

- Ensure both terminals are running simultaneously
- Verify Python virtual environment is activated in T1
- Confirm Node.js version 23.11.0 is active in T2 (`node -v`)
- Check that all dependencies are installed correctly
- Ensure ports 5000 and the dev server port are not already in use
