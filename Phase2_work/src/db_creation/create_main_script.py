#!/usr/bin/env python3
"""
GrantGuruDB initializer
- No password
- Aborts if DB exists
- Executes main.sql
- Uses context manager for cursor
"""

import os
from dotenv import load_dotenv
import sys
import mysql.connector
from mysql.connector import errorcode
from  src.utils.logging_utils import log_info, log_warning, log_error

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")


BUILD_FILES=[
    "src/db_creation/create_relations_commands/01_create_grant_entity.sql",
    "src/db_creation/create_relations_commands/02_create_user_entity.sql",
    "src/db_creation/create_relations_commands/03_create_application_entity.sql",
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
        with open(path, "r") as f:
            sql = f.read()

        statements = [s.strip() for s in sql.split(';') if s.strip()]
        for statement in statements:
            cursor.execute(statement)
 
        cnx.commit()
        log_info(f"Completed {path}")

    log_info(f"Empty Database initalized successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        log_error(f"Access denied. Check MySQL user and password.  Error {err.errno}")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)


finally:
    if cnx:
        cnx.close()
