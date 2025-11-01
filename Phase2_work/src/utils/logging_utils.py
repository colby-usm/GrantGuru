import sys

def log_info(msg):
    print(f"[INFO] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)

def log_warning(msg):
    print(f"[WARNING] {msg}")
