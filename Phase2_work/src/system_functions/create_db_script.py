#!/usr/bin/env python3
"""
    File: create_db_script.py
    Version: 14 November 2025
    Author: Colby Wirth
    Description:
        Main script to build the empty database GrantGuruDB

        Two steps:
        1. Run INSTANTIATE_DB_COMMAND query to create the db
        2. Run all SQL files in BUILD_DIR
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv 
import mysql.connector
from mysql.connector import errorcode
from src.utils.logging_utils import log_info, log_error

#load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "password")

print(MYSQL_PASS)
INSTANTIATE_DB_COMMAND = f"CREATE DATABASE `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
BUILD_DIR = Path("src/db_creation/create_relations_commands")


def execute_sql_file(cursor, sql_file: Path):
    """Execute all statements in a given SQL file."""
    try:
        sql_content = sql_file.read_text()
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        for stmt in statements:
            if not stmt.startswith("--"):
                cursor.execute(stmt)
    except mysql.connector.Error as err:
        log_error(f"MySQL Error in {sql_file.name}:\n{err}")
        sys.exit(2)
    except Exception as e:
        log_error(f"Unexpected error in {sql_file.name}:\n{e}")
        sys.exit(2)


if __name__ == "__main__":
    cnx = None
    print(MYSQL_PASS)
    try:
        cnx = mysql.connector.connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS)
        cursor = cnx.cursor()

        # Check if DB exists
        cursor.execute("SHOW DATABASES LIKE %s;", (DB_NAME,))
        if cursor.fetchone():
            log_info(f"Database '{DB_NAME}' already exists. Skipping creation.")
            sys.exit(0)
        else:
            cursor.execute(INSTANTIATE_DB_COMMAND)
            log_info(f"Database '{DB_NAME}' created successfully.")
            cursor.execute(f"USE `{DB_NAME}`;")

            # Execute all SQL files in directory (sorted alphanumerically)
            sql_files = sorted(BUILD_DIR.glob("*.sql"))
            if not sql_files:
                log_error(f"No SQL files found in {BUILD_DIR}")
                sys.exit(1)

            for sql_file in sql_files:
                execute_sql_file(cursor, sql_file)
                cnx.commit()
            log_info("All tables built successfully")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log_error(f"Access denied. Check MySQL user and password. Error {err}")
        else:
            log_error(f"MySQL Error: {err}")
        sys.exit(2)

    finally:
        if cnx:
            cnx.close()
