#!/bin/bash

###############################################################################
# GrantGuru Full Setup Script
# Sets up Python venv, installs dependencies, configures Node via fnm or npm,
# and installs UI dependencies.
###############################################################################

set -e  # Exit on real errors only

# Colors
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m" # No color

echo -e "${BLUE}=== GrantGuru Initial Setup ===${NC}"

###############################################################################
# 1. Verify prerequisites
###############################################################################

echo -e "\n${BLUE}Checking system prerequisites...${NC}"

# Python 3.12
if ! command -v python >/dev/null 2>&1; then
    echo -e "${RED}✗ Python 3.12 not found. Install Python 3.12 and retry.${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Python 3.12 found${NC}"
fi

# Node / fnm detection
USE_FNM=false
NODE_VERSION="23.11.0"

if command -v fnm >/dev/null 2>&1; then
    echo -e "${GREEN}✓ fnm found, will use fnm to manage Node${NC}"
    USE_FNM=true
elif command -v npm >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ fnm not found, using system-wide npm${NC}"
else
    echo -e "${RED}✗ Neither fnm nor npm found. Install Node.js or fnm first.${NC}"
    exit 1
fi

###############################################################################
# 2. Python environment setup
###############################################################################

echo -e "\n${BLUE}=== Python Environment Setup ===${NC}"

cd "$(dirname "$0")"  # ensure script is run from project root

if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists, skipping${NC}"
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"
# shellcheck disable=SC1091
source .venv/Scripts/activate

echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

###############################################################################
# 3. Node.js setup (fnm or system npm)
###############################################################################

echo -e "\n${BLUE}=== Node.js Environment Setup ===${NC}"

if [ "$USE_FNM" = true ]; then
    if ! fnm list | grep -q "$NODE_VERSION"; then
        echo -e "${YELLOW}Installing Node.js $NODE_VERSION via fnm...${NC}"
        fnm install "$NODE_VERSION"
        echo -e "${GREEN}✓ Node.js $NODE_VERSION installed via fnm${NC}"
    else
        echo -e "${GREEN}✓ Node.js $NODE_VERSION already installed via fnm${NC}"
    fi

    echo -e "${YELLOW}Switching to Node.js $NODE_VERSION via fnm...${NC}"
    eval "$(fnm env)"
    fnm use "$NODE_VERSION"
else
    echo -e "${YELLOW}Using system-wide npm and Node.js${NC}"
    node -v || echo -e "${RED}✗ Node.js not found!${NC}"
fi

###############################################################################
# 4. Install UI dependencies
###############################################################################

echo -e "\n${BLUE}=== Installing UI Dependencies ===${NC}"

UI_DIR="Phase3_work/UI"

if [ ! -d "$UI_DIR" ]; then
    echo -e "${RED}✗ UI directory $UI_DIR not found.${NC}"
    exit 1
fi

cd "$UI_DIR"

echo -e "${YELLOW}Installing npm packages...${NC}"
npm install
echo -e "${GREEN}✓ npm dependencies installed${NC}"

###############################################################################
# DONE
###############################################################################

echo -e "\n${GREEN}=== GrantGuru Setup Complete! ===${NC}"
echo -e "${GREEN}You may now run your launcher or development servers.${NC}"