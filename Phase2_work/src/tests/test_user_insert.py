"""
    File: test_user_insert.py
    Version: 8 November 2025
    Author: Colby Wirth
    Description:
        Test insert user script using single-statement RETURNING query
"""

import os
import mysql.connector
from hashlib import sha256

SCRIPT_PATH = "src/entity_crud_operations/users_and_research_fields/create_users.sql"

# DB config from environment
DB_CONFIG = {
    "host": os.environ.get("HOST", "localhost"),
    "user": os.environ.get("GG_USER", "root"),
    "password": os.environ.get("GG_PASS", ""),
    "database": os.environ.get("DB_NAME", "GrantGuruDB")
}

# Test user data
test_user = {
    "f_name": "A-New",
    "m_name": None,
    "l_name": "User",
    "institution": "My University",
    "email": "test3@gmail.com",  # must be unique
    "password": sha256("123456".encode()).hexdigest()
}

# Load SQL script
with open(SCRIPT_PATH, "r") as f:
    sql_script = f.read()

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Execute single INSERT ... RETURNING statement
    cursor.execute(sql_script, test_user)


    conn.commit()
    print(f"Inserted test user")

finally:
    cursor.close()
    conn.close()
