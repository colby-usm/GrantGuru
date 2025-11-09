
#!/usr/bin/env python3
"""
    File: delete_db_script.py
    Version: 1 November 2025
    Author: Colby Wirth
    Description:
        - Script to delete a database based on .env variables
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
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
from src.utils.logging_utils import log_info, log_error

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

# Paths to SQL scripts
CREATE_USER_SCRIPT = Path("src/db_crud/users/create_users.sql")
CREATE_RESEARCH_SCRIPT = Path("src/db_crud/research_fields/create_research_fields.sql")
SELECT_BY_EMAIL_SCRIPT = Path("src/db_crud/users/select_users_id_by_email.sql")

# Connect to MySQL
cnx = mysql.connector.connect(
    host=HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=DB_NAME,
)
cursor = cnx.cursor()

# Users and their research fields
users_with_fields = [
    (("Alice", "M", "Smith", "MIT", "alice@example.com", "password1"), ["AI", "Machine Learning"]),
    (("Bob", "J", "Jones", "Stanford", "bob@example.com", "password2"), ["Robotics"]),
    (("Carol", None, "Taylor", "Harvard", "carol@example.com", "password3"), ["Computer Vision", "NLP"]),
    (("David", "K", "Lee", "UCLA", "david@example.com", "password4"), ["Data Science"]),
    (("Eve", None, "Miller", "Berkeley", "eve@example.com", "password5"), ["Cybersecurity", "Quantum Computing"])
]

# Read SQL scripts
with open(CREATE_USER_SCRIPT, "r") as f:
    create_user_sql = f.read()

with open(CREATE_RESEARCH_SCRIPT, "r") as f:
    create_research_sql = f.read()

with open(SELECT_BY_EMAIL_SCRIPT, "r") as f:
    select_by_email_sql = f.read()

for user_info, research_fields in users_with_fields:
    first_name, middle_name, last_name, institution, email, password = user_info
    
    try:
        # 1. Insert user
        cursor.execute(create_user_sql, {
            "f_name": first_name,
            "m_name": middle_name,
            "l_name": last_name,
            "institution": institution,
            "email": email,
            "password": password
        })
        cnx.commit()
        log_info(f"Inserted user {email}")
        
        # 2. Get user ID (UUID string)
        cursor.execute(select_by_email_sql, {"email": email})
        user_id_result = cursor.fetchone()
        if not user_id_result:
            log_error(f"Failed to fetch user ID for {email}")
            continue
        user_id = user_id_result[0]  # This is a UUID string
        
        # 3. Insert research fields
        for field in research_fields:
            cursor.execute(create_research_sql, {
                "user_id": user_id,
                "research_field": field
            })
            cursor.fetchall()
        cnx.commit()
        log_info(f"Added research fields for {email}: {', '.join(research_fields)}")
        
    except mysql.connector.Error as e:
        log_error(f"MySQL error for {email}: {e}")
        cnx.rollback()

# Close connection
cursor.close()
cnx.close()
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

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
