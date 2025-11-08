#!/usr/bin/env python3
"""

    File: create_db_script.py
    Version: 8 November 2025
    Author: Colby Wirth
    Description:
        Main script to build the empty database
        GrantGuruDB initializer
        Uses context manager for cursor
        Builds the empty database with the info from your local .env

"""

import os
from dotenv import load_dotenv
import sys
import mysql.connector
from mysql.connector import errorcode
from src.utils.logging_utils import log_info, log_error

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")


BUILD_FILES=[
    "src/db_creation/create_relations_commands/01_create_grants_entity.sql",
    "src/db_creation/create_relations_commands/02_create_users_entity.sql",
    "src/db_creation/create_relations_commands/03_create_applications_entity.sql",
    "src/db_creation/create_relations_commands/04_create_documents_entity.sql",
    "src/db_creation/create_relations_commands/05_create_internal_deadlines_entity.sql"
]


cnx  = None
try:
    log_info("Connecting to MySQL server...")
    cnx = mysql.connector.connect(
        host=HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS
    )

    cursor = cnx.cursor()

    log_info(f"Checking if database '{DB_NAME}' exists...")
    cursor.execute("SHOW DATABASES LIKE %s;", (DB_NAME,))
    if cursor.fetchone():
        log_error(f"Database '{DB_NAME}' already exists. Aborting.")
        sys.exit(1)


    log_info(f"Creating database '{DB_NAME}'...")
    cursor.execute(f"CREATE DATABASE `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    log_info(f"Database '{DB_NAME}' created successfully.")


    log_info(f"Switching to database '{DB_NAME}'...")
    cursor.execute(f"USE `{DB_NAME}`;")



    for path in BUILD_FILES:
        try:
            with open(path, "r") as f:
                sql = f.read()

            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for statement in statements:
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as err:
                    log_error(f"MySQL Error in file '{path}' on statement:\n{statement}\nError: {err}")
                    sys.exit(2)
 
            cnx.commit()
            log_info(f"Completed {path}")

        except Exception as e:
            log_error(f"Unexpected error while processing file '{path}': {e}")
            sys.exit(2)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        log_error(f"Access denied. Check MySQL user and password.  Error {err.errno}")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)


finally:
    if cnx:
        cnx.close()
