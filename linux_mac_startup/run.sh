#!/bin/bash
# GrantGuru Launcher Script
# This script:
# 1. Starts the Flask backend (T1)
# 2. Starts the React frontend (T2)
set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to project root (one level up from linux_mac_startup)
PROJECT_ROOT="$SCRIPT_DIR/.."

# Project paths
VENV_PATH="$PROJECT_ROOT/.venv/bin/activate"
PHASE2_DIR="$PROJECT_ROOT/Phase2_work"
PHASE3_DIR="$PROJECT_ROOT/Phase3_work"
UI_DIR="$PHASE3_DIR/UI"

# Environment variables
export DB_NAME="GrantGuruDB"
export HOST="localhost"
export GG_USER="admin"
export GG_PASS="admin"

# Flask variables
export FLASK_APP=api
export FLASK_RUN_APP=api:create_app

echo -e "${BLUE}=== GrantGuru Launcher ===${NC}"
echo -e "${BLUE}Project root: $PROJECT_ROOT${NC}\n"

# Verify virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_PATH${NC}"
    exit 1
fi

# Verify directories exist
if [ ! -d "$PHASE2_DIR" ]; then
    echo -e "${RED}Error: Phase2_work directory not found${NC}"
    exit 1
fi

if [ ! -d "$PHASE3_DIR" ]; then
    echo -e "${RED}Error: Phase3_work directory not found${NC}"
    exit 1
fi

if [ ! -d "$UI_DIR" ]; then
    echo -e "${RED}Error: UI directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All paths verified${NC}\n"

# Step 1: Launch Flask Backend
echo -e "${YELLOW}Step 2: Launching Flask backend (T1)...${NC}"
osascript <<EOF
tell application "Terminal"
    do script "cd '$PHASE3_DIR' && source '$VENV_PATH' && export FLASK_APP=api && export FLASK_RUN_APP=api:create_app && export DB_NAME='$DB_NAME' && export HOST='$HOST' && export GG_USER='$GG_USER' && export GG_PASS='$GG_PASS' && echo 'Flask Backend Starting...' && flask run --host=127.0.0.1 --port=5000"
    activate
end tell
EOF

sleep 2

# Step 3: Launch React Frontend
echo -e "${YELLOW}Step 3: Launching React frontend (T2)...${NC}"
osascript <<EOF
tell application "Terminal"
    do script "cd '$UI_DIR' && echo 'React Frontend Starting...' && npm run dev"
    activate
end tell
EOF

echo -e "\n${GREEN}✓ All services launched successfully!${NC}"
echo -e "${BLUE}Flask backend: http://127.0.0.1:5000${NC}"
echo -e "${BLUE}React frontend: Check T2 for the dev server URL${NC}"
echo -e "\n${BLUE}To stop the servers, close both terminal windows or press Ctrl+C in each.${NC}"
