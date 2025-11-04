import sys

RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BLUE = "\033[34m"

def log_info(msg):
    print(f"{GREEN}[INFO] {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}[WARNING] {msg}{RESET}")

def log_error(msg):
    print(f"{RED}[ERROR] {msg}{RESET}", file=sys.stderr)

def log_debug(msg):
    print(f"{BLUE}[DEBUG] {msg}{RESET}")

def log_default(msg):
    print(f"[LOG] {msg}")
