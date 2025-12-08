# GrantGuru

## Prerequisites

- Instructions for Mac and Linux Setups

-   Python **3.12**
-   Node.js **23.11.0**
-   Either **nvm** or **fnm** (Node version managers)

## Project Structure

All scripts must be executed from the `GrantGuru/` directory.

## Setup

To set up the project:

``` bash
linux_mac_startup/setup.sh
```

This installs Python dependencies, initializes the virtual environment,
and installs Node packages using whichever Node version manager (`nvm`
or `fnm`) is available.

## Running the Web App

To start the backend (Flask) and frontend (React) together:

``` bash
./linux_mac_startup/run.sh
```

This script automatically launches both services concurrently.

## Cleanup

To reset the environment (remove venv, node_modules, db
etc.):

``` bash
./linux_mac_startup/reset_environment.sh
```
