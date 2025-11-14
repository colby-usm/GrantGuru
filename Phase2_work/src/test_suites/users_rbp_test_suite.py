"""
users_operations_test_suite.py
Author: Colby Wirth
Version: 14 November 2025
Description:
    Tests for high-level user operations via users_operations.py
    Includes CRUD, password/email updates, and research field associations
    All tests enforce permissions via decorators
    Generated with the assistance of AI Tools
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector as connector
from mysql.connector import errorcode, Error as MySQLError


from src.utils.logging_utils import log_info, log_error, log_default
from src.user_functions.users_operations import (
    read_users_fields_by_uuid,
    update_users_fields,
    update_users_password,
    update_users_email,
    delete_a_users_entity,
    add_a_reference_to_research_field,
    delete_a_reference_to_research_field,
)
from src.user_functions.view_based_operations import Role
from src.utils.sql_file_parsers import read_sql_helper

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")



CREATE_SCRIPT = "src/db_crud/users/create_users.sql"


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
    except MySQLError as err:
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

    result = read_users_fields_by_uuid(Role.USER, uid, uid, cursor)

    if isinstance(result, tuple) and result[5] == "read_test@example.com":
        log_info(" PASS: read_users_fields_by_uuid returned correct row")
    else:
        log_error(f" FAIL: Unexpected return: {result}")


def test_update_users_fields(cursor):
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

    result = update_users_fields(Role.USER, uid, uid, cursor, new_fields)

    if result is None:
        cursor.execute("SELECT f_name, m_name, l_name, institution, email "
                       "FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        row = cursor.fetchone()
        expected = (
            "UpdatedFirst", "UpdatedMiddle", "UpdatedLast",
            "Updated University", "updated_email@example.com"
        )
        if row == expected:
            log_info(" PASS: update_users_fields persisted changes")
        else:
            log_error(f" FAIL: DB row mismatch: {row}")
    else:
        log_error(f" FAIL: update_users_fields returned error: {result}")


def test_update_users_password(cursor):
    log_default("Running test_update_users_password()")
    uid = insert_test_user(cursor, email="pw_test@example.com", password="old_pw")

    new_password = "new_pw_hash"
    result = update_users_password(Role.USER, uid, uid, cursor, new_password)

    if result is None:
        cursor.execute("SELECT password FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        pw = cursor.fetchone()[0]
        if pw == new_password:
            log_info(" PASS: update_users_password updated correctly")
        else:
            log_error(f" FAIL: password not updated, got {pw}")
    else:
        log_error(f" FAIL: update_users_password returned error: {result}")


def test_update_users_email(cursor):
    log_default("Running test_update_users_email()")
    uid = insert_test_user(cursor, email="old_email@example.com")

    new_email = "new_email@example.com"
    result = update_users_email(Role.USER, uid, uid, cursor, new_email)

    if result is None:
        cursor.execute("SELECT email FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        email = cursor.fetchone()[0]
        if email == new_email:
            log_info(" PASS: update_users_email persisted new email")
        else:
            log_error(f" FAIL: email not updated, got {email}")
    else:
        log_error(f" FAIL: update_users_email returned error: {result}")


def test_delete_a_users_entity(cursor):
    log_default("Running test_delete_a_users_entity()")
    uid = insert_test_user(cursor, email="delete_test@example.com")

    result = delete_a_users_entity(Role.USER, uid, uid, cursor)

    if result is None:
        cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id=UUID_TO_BIN(%s)", (uid,))
        if cursor.fetchone()[0] == 0:
            log_info(" PASS: delete_a_users_entity removed user")
        else:
            log_error(" FAIL: user still exists in DB")
    else:
        log_error(f" FAIL: delete_a_users_entity returned error: {result}")


def test_research_field_operations(cursor):
    log_default("Running test_research_field_operations()")
    uid = insert_test_user(cursor, email="research_test@example.com")

    add_result = add_a_reference_to_research_field(Role.USER, uid, uid, cursor, "AI")
    if add_result is None:
        log_info(" PASS: add_a_reference_to_research_field succeeded")
    else:
        log_error(f" FAIL: add returned error: {add_result}")

    del_result = delete_a_reference_to_research_field(Role.USER, uid, uid, cursor, "AI")
    if del_result is None:
        log_info(" PASS: delete_a_reference_to_research_field succeeded")
    else:
        log_error(f" FAIL: delete returned error: {del_result}")



if __name__ == "__main__":
    cnx, cursor = setup_db()

    test_read_users_fields_by_uuid(cursor)
    test_update_users_fields(cursor)
    test_update_users_password(cursor)
    test_update_users_email(cursor)
    test_delete_a_users_entity(cursor)
    test_research_field_operations(cursor)

    cnx.commit()
    cursor.close()
    cnx.close()
