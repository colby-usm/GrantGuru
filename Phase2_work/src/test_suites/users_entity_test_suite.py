"""
      users_entity_test_suite.py
      Author: Colby Wirth
      Version: 13 November 2025
      Description: 
            Testing suite for Users CRUD operations using users_operations.py functions.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode, Error as MySQLError
from uuid import uuid4

from src.utils.logging_utils import log_info, log_error, log_default
from src.user_functions.users_operations import (
    read_users_fields_by_uuid,
    update_users_fields,
    update_users_password,
    update_users_email,
    delete_a_users_entity,
    add_a_reference_to_research_field,
    delete_a_reference_to_research_field,
    UserOperationError
)
from src.user_functions.view_based_operations import Role

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

# Connection
try:
    log_info("Connecting to MySQL server...")
    cnx = mysql.connector.connect(
        host=HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        database=DB_NAME
    )
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        log_error(f"Access denied: {err}")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)


# Helper for test results
def assert_success(result, description=""):
    if result is None:
        log_info(f" PASS: {description}")
    elif isinstance(result, UserOperationError):
        log_error(f" FAIL: {description} - UserOperationError: {result}")
    elif isinstance(result, MySQLError):
        log_error(f" FAIL: {description} - MySQLError: {result}")


# CREATE & READ TESTS
def create_and_read_users_tests():
    log_default("Running create_and_read_users_tests()")

    # Insert a user via direct SQL (because creation function not implemented yet)
    create_sql_path = Path("src/db_crud/users/create_users.sql")
    sql_script = create_sql_path.read_text()

    def insert_user(user_data):
        try:
            cursor.execute(sql_script, user_data)
            cnx.commit()
            return cursor.lastrowid
        except MySQLError as e:
            cnx.rollback()
            log_error(f" FAIL: Insert user raised MySQLError: {e}")
            return None

    # 1. Valid user
    user_data = {
        "f_name": "Alice",
        "m_name": "M",
        "l_name": "Smith",
        "institution": "MIT",
        "email": "alice@example.com",
        "password": "pw"
    }
    insert_user(user_data)

    # 2. Read user via function
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (user_data["email"],))
    user_id = cursor.fetchone()[0]
    result = read_users_fields_by_uuid(Role.ADMIN, user_id, user_id, cursor)
    assert_success(result, "Read valid user by UUID")


# UPDATE TESTS
def update_users_test_suite():
    log_default("Running update_users_test_suite()")

    # Helper to insert user
    def insert_user(email):
        sql_script = Path("src/db_crud/users/create_users.sql").read_text()
        cursor.execute(sql_script, {
            "f_name": "Update",
            "m_name": None,
            "l_name": "User",
            "institution": "Test University",
            "email": email,
            "password": "pw123"
        })
        cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (email,))
        return cursor.fetchone()[0]

    user_email = "update_test@example.com"
    user_id = insert_user(user_email)

    # 1. Update fields
    new_fields = {
        "user_id": user_id,
        "f_name": "UpdatedFirst",
        "m_name": "UpdatedMiddle",
        "l_name": "UpdatedLast",
        "institution": "Updated University",
        "email": "updated_email@example.com"
    }
    result = update_users_fields(Role.ADMIN, user_id, user_id, cursor, new_fields)
    assert_success(result, "Update allowed fields")

    # 2. Update password
    result = update_users_password(Role.ADMIN, user_id, user_id, cursor, "new_pw")
    assert_success(result, "Update password")

    # 3. Update email
    result = update_users_email(Role.ADMIN, user_id, user_id, cursor, "new_email@example.com")
    assert_success(result, "Update email")


# DELETE TESTS
def delete_users_test_suite():
    log_default("Running delete_users_test_suite()")

    # Insert user
    sql_script = Path("src/db_crud/users/create_users.sql").read_text()
    cursor.execute(sql_script, {
        "f_name": "Delete",
        "m_name": None,
        "l_name": "User",
        "institution": "Test University",
        "email": "delete_test@example.com",
        "password": "pw"
    })
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", ("delete_test@example.com",))
    user_id = cursor.fetchone()[0]

    # Delete user via function
    result = delete_a_users_entity(Role.ADMIN, user_id, user_id, cursor)
    assert_success(result, "Delete existing user")

    # Attempt to delete non-existent user
    fake_user_id = str(uuid4())
    result = delete_a_users_entity(Role.ADMIN, fake_user_id, fake_user_id, cursor)
    assert_success(result, "Delete non-existent user (should be handled)")


# RESEARCH FIELD TESTS
def research_field_test_suite():
    log_default("Running research_field_test_suite()")

    # Insert user
    sql_script = Path("src/db_crud/users/create_users.sql").read_text()
    cursor.execute(sql_script, {
        "f_name": "Research",
        "m_name": None,
        "l_name": "Tester",
        "institution": "Test University",
        "email": "research_test@example.com",
        "password": "pw"
    })
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", ("research_test@example.com",))
    user_id = cursor.fetchone()[0]

    # Add research field
    result = add_a_reference_to_research_field(Role.ADMIN, user_id, user_id, cursor, "AI Research")
    assert_success(result, "Add research field")

    # Delete research field
    result = delete_a_reference_to_research_field(Role.ADMIN, user_id, user_id, cursor, "AI Research")
    assert_success(result, "Delete research field")


# MAIN
if __name__ == "__main__":
    create_and_read_users_tests()
    update_users_test_suite()
    delete_users_test_suite()
    research_field_test_suite()
    cnx.commit()
    cnx.close()
