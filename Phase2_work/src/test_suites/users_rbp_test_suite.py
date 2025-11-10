"""
users_operations_test_suite.py
Author: Colby Wirth
Version: 9 November 2025
Description:
    Tests for high-level user operations via users_operations.py
    Includes CRUD, password/email updates, and research field associations
    All tests enforce permissions via decorators
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector as connector
from mysql.connector import errorcode, Error

from src.utils.logging_utils import log_info, log_error, log_default
from src.user_functions.users_operations import (
    read_users_fields_by_uuid,
    update_users_fields,
    update_users_password,
    update_users_email,
    delete_a_users_entity,
    add_a_reference_to_research_field,
    delete_a_reference_to_research_field
)
from src.user_functions.view_based_operations import Role
from src.utils.sql_file_parsers import read_sql_helper

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")


def setup_db():
    try:
        cnx = connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cursor = cnx.cursor()
        return cnx, cursor
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log_error(f"Access denied. Check MySQL user/password: {err}")
        else:
            log_error(f"MySQL Error: {err}")
        sys.exit(1)


def insert_test_user(cursor, email="test_user@example.com", password="pw123"):
    """
    Inserts a user via raw SQL for testing purposes.
    Returns the string UUID.
    """
    CREATE_SCRIPT = "src/db_crud/users/create_users.sql"
    sql_script = read_sql_helper(CREATE_SCRIPT)
    if not sql_script:
        log_error("Cannot read create_users.sql")
        return None

    cursor.execute(sql_script, {
        "f_name": "Test",
        "m_name": "M",
        "l_name": "User",
        "institution": "Test University",
        "email": email,
        "password": password
    })
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (email,))
    return cursor.fetchone()[0]


def test_read_users_fields_by_uuid(cursor):
    log_default("Running test_read_users_fields_by_uuid()")

    uid = insert_test_user(cursor, email="read_test@example.com")
    row = read_users_fields_by_uuid(Role.USER, uid, uid, cursor)
    if row and row[5] == "read_test@example.com":
        log_info(" PASS: read_users_fields_by_uuid returned correct row")
    else:
        log_error(" FAIL: read_users_fields_by_uuid returned incorrect data")


def test_update_users_fields(cursor, cnx):
    log_default("Running test_update_users_fields()")
    uid = insert_test_user(cursor, email="update_test@example.com")

    new_fields = {
        "user_id": uid,
        "f_name": "UpdatedFirst",
        "m_name": "UpdatedMiddle",
        "l_name": "UpdatedLast",
        "institution": "Updated University",
        "email": "updated_email@example.com"
    }

    if update_users_fields(Role.USER, uid, uid, cursor, new_fields):
        cursor.execute("SELECT f_name, m_name, l_name, institution, email FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        row = cursor.fetchone()
        expected = ("UpdatedFirst", "UpdatedMiddle", "UpdatedLast", "Updated University", "updated_email@example.com")
        if row == expected:
            log_info(" PASS: update_users_fields persisted changes correctly")
        else:
            log_error(f" FAIL: update_users_fields changes not persisted: {row}")
    else:
        log_error(" FAIL: update_users_fields returned False")


def test_update_users_password(cursor, cnx):
    log_default("Running test_update_users_password()")
    uid = insert_test_user(cursor, email="pw_test@example.com", password="old_pw")

    new_password = "new_pw_hash"
    if update_users_password(Role.USER, uid, uid, cursor, new_password):
        cursor.execute("SELECT password FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        pw = cursor.fetchone()[0]
        if pw == new_password:
            log_info(" PASS: update_users_password changed password correctly")
        else:
            log_error(" FAIL: update_users_password did not update password")
    else:
        log_error(" FAIL: update_users_password returned False")


def test_update_users_email(cursor, cnx):
    log_default("Running test_update_users_email()")
    uid = insert_test_user(cursor, email="old_email@example.com")

    new_email = "new_email@example.com"
    if update_users_email(Role.USER, uid, uid, cursor, new_email):
        cursor.execute("SELECT email FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        email = cursor.fetchone()[0]
        if email == new_email:
            log_info(" PASS: update_users_email updated email correctly")
        else:
            log_error(f" FAIL: update_users_email did not persist: {email}")
    else:
        log_error(" FAIL: update_users_email returned False")


def test_delete_a_users_entity(cursor, cnx):
    log_default("Running test_delete_a_users_entity()")
    uid = insert_test_user(cursor, email="delete_test@example.com")

    if delete_a_users_entity(Role.USER, uid, uid, cursor):
        cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        if cursor.fetchone()[0] == 0:
            log_info(" PASS: delete_a_users_entity removed the user")
        else:
            log_error(" FAIL: delete_a_users_entity did not remove user")
    else:
        log_error(" FAIL: delete_a_users_entity returned False")


def test_research_field_operations(cursor, cnx):
    log_default("Running test_research_field_operations()")
    uid = insert_test_user(cursor, email="research_test@example.com")

    # Add research field
    if add_a_reference_to_research_field(Role.USER, uid, uid, cursor, "AI"):
        log_info(" PASS: add_a_reference_to_research_field succeeded")
    else:
        log_error(" FAIL: add_a_reference_to_research_field failed")

    # Remove research field
    if delete_a_reference_to_research_field(Role.USER, uid, uid, cursor, "AI"):
        log_info(" PASS: delete_a_reference_to_research_field succeeded")
    else:
        log_error(" FAIL: delete_a_reference_to_research_field failed")


if __name__ == "__main__":
    cnx, cursor = setup_db()

    test_read_users_fields_by_uuid(cursor)
    test_update_users_fields(cursor, cnx)
    test_update_users_password(cursor, cnx)
    test_update_users_email(cursor, cnx)
    test_delete_a_users_entity(cursor, cnx)
    test_research_field_operations(cursor, cnx)

    cnx.commit()
    cursor.close()
    cnx.close()
