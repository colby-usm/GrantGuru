# GrantGuru

## Prerequisites

- Python **3.12**
- Node.js **23.11.0**
- Either **nvm** or **fnm** (Node version managers) for Mac/Linux

## Setup & Usage

All scripts must be executed from the `GrantGuru/` directory.

| Task | Mac/Linux | Windows |
|------|-----------|---------|
| **Setup** | `./linux_mac_startup/install.sh` | `.\windows_startup\install.bat` |
| **Run Web App** | `./linux_mac_startup/run.sh` | `.\windows_startup\run.bat` |
| **Reset Environment** | `./linux_mac_startup/reset_environment.sh` | `.\windows_startup\reset_environment.bat` |

### Setup

Installs Python dependencies, initializes the virtual environment, and installs Node packages.

### Running the Web App

Starts both the backend (Flask) and frontend (React) services concurrently.

### Reset Environment

Removes the virtual environment, node_modules, database, and other generated files to reset the project to a clean state.
