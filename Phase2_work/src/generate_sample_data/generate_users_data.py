import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
from src.utils.logging_utils import log_info, log_error

"""
    File: generate_users_data.py
    Version: 14 November 2025
    Author: Colby Wirth
    Description:
        - Generates a user entity with their research fields for 6 Users entries
        - For each User 3 Step process: 
            1. Add User to DB
            2. Verify User has been added
            3. Add ResearchField
        - Finally, view joined Users with ResearchField
"""

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

# Paths to SQL scripts
CREATE_USER_SCRIPT = Path("src/db_crud/users/create_users.sql")
SELECT_BY_EMAIL_SCRIPT = Path("src/db_crud/users/select_users_id_by_email.sql")
CREATE_RESEARCH_SCRIPT = Path("src/db_crud/research_fields/create_research_fields.sql")


# view all users with research fields
JOIN_USERS_WITH_RESEARCH_FIELDS = """
    SELECT *
    FROM Users
    NATURAL JOIN UserResearchFields
    NATURAL JOIN ResearchField;
"""


# Connect to MySQL
cnx = mysql.connector.connect(
    host=HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=DB_NAME,
)

# Users and their research fields
users_with_fields = [
    (("Alice", "A", "Anderson", "MIT", "alice@example.com", "password1"), ["AI", "Machine Learning"]),
    (("Bob", "B", "Busch", "Stanford", "bob@example.com", "password2"), ["Robotics"]),
    (("Carol", None, "Clemson", "Harvard", "carol@example.com", "password3"), ["Computer Vision", "Machine Learning"]),
    (("David", "d", "Day", "UCLA", "david@example.com", "password4"), ["Data Science"]),
    (("Eve", None, "Ericson", "Berkeley", "eve@example.com", "password5"), ["Cybersecurity", "Quantum Computing"]),
    (("Fred", None, "Fiddlesticks", "USM", "fred@example.com", "password6"), ["AI", "Biology", "Environmental Sciences"])
]

# Read SQL scripts
with open(CREATE_USER_SCRIPT, "r") as f:
    create_user_sql = f.read()

with open(CREATE_RESEARCH_SCRIPT, "r") as f:
    create_research_sql = f.read()

with open(SELECT_BY_EMAIL_SCRIPT, "r") as f:
    select_by_email_sql = f.read()


def drain_cursor(cursor):
    """Consume all remaining result sets to avoid 'Unread result found'."""
    while True:
        if not cursor.nextset():
            break


if __name__ == "__main__":
    for user_info, research_fields in users_with_fields:
        first_name, middle_name, last_name, institution, email, password = user_info

        print(f"\n\n --- Beginning tests for {first_name} {last_name} ---")
        try:
            with cnx.cursor(buffered=True) as cursor:
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
                user_id_result = cursor.fetchone()  # Fetch BEFORE draining
                drain_cursor(cursor)  # Now drain any remaining result sets

                if not user_id_result:
                    log_error(f"Failed to fetch user ID for {email}")
                    continue
                user_id = user_id_result[0]
                log_info(f"Retrieved user_id: {user_id} for {email}")

                # 3. Insert research fields
                for field in research_fields:
                    cursor.execute(create_research_sql, {
                        "user_id": user_id,
                        "research_field": field
                    })
                    drain_cursor(cursor)  # Drain after each field insertion

                cnx.commit()
                log_info(f"Added research fields for {email}: {', '.join(research_fields)}")

        except mysql.connector.Error as e:
            log_error(f"MySQL error for {email}: {e}")
            cnx.rollback()

    print("\n\n --- Joined Users with Research Fields ---")
    with cnx.cursor(buffered=True) as cursor:
        cursor.execute(JOIN_USERS_WITH_RESEARCH_FIELDS)
        results = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        print(f"Columns: {columns}")
        print()

        for row in results:
            print(row)

    cnx.close()
