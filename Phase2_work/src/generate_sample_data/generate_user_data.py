import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
from src.utils.logging_utils import log_info, log_error

"""
    File: generate_user_data.py
    Version: 8 November 2025
    Author: Colby Wirth
    Description:
        - Generates a user entity with their research fields for 5 Users entries
"""

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

def execute_sql_script(cursor, script, params=None):
    """
    Execute multi-statement SQL script safely by splitting on ';'.
    Fetch results if present to avoid 'Unread result found'.
    """
    statements = [s.strip() for s in script.split(';') if s.strip()]
    for stmt in statements:
        cursor.execute(stmt, params or {})
        # Attempt to fetch result if it's a SELECT
        try:
            cursor.fetchall()
        except mysql.connector.InterfaceError:
            # Ignore statements that do not return rows (INSERT/UPDATE)
            pass

# Loop through users
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
        user_id = user_id_result[0]  # UUID string
        
        # 3. Insert research fields safely
        for field in research_fields:
            execute_sql_script(cursor, create_research_sql, {
                "user_id": user_id,
                "research_field": field
            })
        cnx.commit()
        log_info(f"Added research fields for {email}: {', '.join(research_fields)}")
        
    except mysql.connector.Error as e:
        log_error(f"MySQL error for {email}: {e}")
        cnx.rollback()

# Close connection
cursor.close()
cnx.close()
