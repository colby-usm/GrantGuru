
#!/usr/bin/env python3
"""
GrantGuruDB Deleter
- Prompts user for confirmation before deleting the DB
- Aborts safely if DB does not exist
- Uses .env for configuration
"""

import os
import sys
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from  src.utils.logging_utils import log_info, log_warning, log_error

# Load environment variables
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "")


try:
    log_info("Connecting to MySQL server...")
    conn = mysql.connector.connect(
        host=HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS
    )

    with conn.cursor() as cursor:
        # Check if DB exists
        log_info(f"Checking if database '{DB_NAME}' exists...")
        cursor.execute("SHOW DATABASES LIKE %s;", (DB_NAME,))
        if not cursor.fetchone():
            log_warning(f"Database '{DB_NAME}' does not exist. Nothing to delete.")
            sys.exit(0)

        # Confirm deletion
        log_warning(f"!!! You are about to permanently DELETE the database '{DB_NAME}' !!!")
        confirm = input("Type the database name to confirm: ").strip()

        if confirm != DB_NAME:
            log_info("Confirmation failed. Aborting deletion.")
            sys.exit(1)

        # Drop the database
        log_info(f"Dropping database '{DB_NAME}'...")
        cursor.execute(f"DROP DATABASE `{DB_NAME}`;")
        conn.commit()

        log_info(f"Database '{DB_NAME}' deleted successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        log_error("Access denied. Check MySQL user and password.")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)

except KeyboardInterrupt:
    log_info("Aborted by user.")
    sys.exit(3)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
