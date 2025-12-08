#!/bin/bash

###############################################################################
# GrantGuru — Reset Environment Script
# Completely resets the local development environment:
# - Activates .venv from GrantGuru/ (if present)
# - Deletes the database using the Phase2 delete_db_script module
# - Removes Python virtual environment (.venv)
# - Removes frontend node_modules
# - Removes Python cache directories
#
# After running this script, run:
#   ./setup.sh
# to rebuild everything from scratch.
###############################################################################

set -e

echo ""
echo "======================================"
echo "   GrantGuru — Reset Environment"
echo "======================================"
echo ""

# Ensure we are in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

###############################################################
# STEP 1: Source virtual environment if it exists
###############################################################
if [ -d ".venv" ]; then
    echo "[+] Activating .venv ..."
    source .venv/bin/activate
else
    echo "[!] No .venv found — skipping activation."
fi

###############################################################
# STEP 2: Run the DB deletion module
###############################################################
if [ -f "Phase2_work/src/system_functions/delete_db_script.py" ]; then
    echo "[+] Running DB deletion script ..."
    # Must be run from inside Phase2_work/src
    pushd Phase2_work >/dev/null
    python -m src.system_functions.delete_db_script
    popd >/dev/null
else
    echo "[!] Database deletion script not found — skipping."
fi

###############################################################
# STEP 3: Remove Python virtual environment
###############################################################
if [ -d ".venv" ]; then
    echo "[+] Removing .venv ..."
    rm -rf .venv
else
    echo "[!] No .venv to remove."
fi

###############################################################
# STEP 4: Remove Node dependencies
###############################################################
FRONTEND_DIR="Phase3_work/UI/frontend/node_modules"

if [ -d "$FRONTEND_DIR" ]; then
    echo "[+] Removing frontend node_modules ..."
    rm -rf "$FRONTEND_DIR"
else
    echo "[!] No node_modules found in frontend."
fi

###############################################################
# STEP 5: Clear Python cache files
###############################################################
echo "[+] Removing Python __pycache__ directories ..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo ""
echo "======================================"
echo " Environment Reset Complete"
echo "======================================"
echo ""
echo "Next steps:"
echo "  → Run ./setup.sh to rebuild everything."
echo ""
