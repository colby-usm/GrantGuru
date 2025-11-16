"""
internal_deadlines_rbp_test_suite.py
Author: GitHub Copilot (based on documents_rbp_test_suite.py template)
Version: 15 November 2025
Description:
    Tests for high-level internal deadline operations via internal_deadlines_operations.py
    Includes CRUD operations with permissions enforcement via decorators
    Generated with the assistance of AI Tools
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import mysql.connector as connector
from mysql.connector import errorcode, Error as MySQLError


from src.utils.logging_utils import log_info, log_error, log_default
from src.db_creation.internal_deadline_functions.internal_deadlines_operations import (
    create_internal_deadline,
    read_internal_deadline_by_uuid,
    update_internal_deadline,
    delete_internal_deadline,
)
from src.user_functions.view_based_operations import Role
from src.utils.sql_file_parsers import read_sql_helper

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")


CREATE_USER_SCRIPT = "src/db_crud/users/create_users.sql"
CREATE_GRANT_SCRIPT = "src/db_crud/grants/create_grants.sql"
CREATE_APPLICATION_SCRIPT = "src/db_crud/applications/create_application.sql"


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
    sql_script = read_sql_helper(CREATE_USER_SCRIPT)
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


def insert_test_grant(cursor, grant_name="Test Grant"):
    """
    Inserts a grant via raw SQL for testing purposes.
    Returns the string UUID.
    """
    sql_script = read_sql_helper(CREATE_GRANT_SCRIPT)
    if not sql_script:
        log_error("Cannot read create_grants.sql")
        return None

    current_date = datetime.now()
    cursor.execute(sql_script, {
        "grant_title": grant_name,
        "description": "Test grant description",
        "research_field": "Computer Science",
        "expected_award_count": 1,
        "eligibility": "Open to all",
        "award_max_amount": 50000,
        "award_min_amount": 10000,
        "program_funding": 100000,
        "provider": "Test Org",
        "link_to_source": "https://example.com/grant",
        "point_of_contact": "test@example.com",
        "date_posted": current_date,
        "archive_date": None,
        "date_closed": None,
        "last_update_date": current_date
    })
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title=%s", (grant_name,))
    return cursor.fetchone()[0]


def insert_test_application(cursor, user_id, grant_id):
    """
    Inserts an application via raw SQL for testing purposes.
    Returns the string UUID.
    """
    sql_script = read_sql_helper(CREATE_APPLICATION_SCRIPT)
    if not sql_script:
        log_error("Cannot read create_application.sql")
        return None

    cursor.execute(sql_script, {
        "status": "pending",
        "user_id": user_id,
        "grant_id": grant_id,
        "application_date": datetime.now()
    })
    cursor.execute(
        "SELECT BIN_TO_UUID(application_id) FROM Applications WHERE user_id=UUID_TO_BIN(%s) AND grant_id=UUID_TO_BIN(%s)",
        (user_id, grant_id)
    )
    return cursor.fetchone()[0]


def create_test_fixtures(cursor):
    """
    Creates a test user, grant, and application for use across all tests.
    Returns (user_id, grant_id, application_id).
    """
    # Clean up any existing test data
    cursor.execute("DELETE FROM Users WHERE email='fixture_user_deadline@example.com'")
    cursor.execute("DELETE FROM Grants WHERE grant_title='Fixture Grant Deadline'")
    
    uid = insert_test_user(cursor, email="fixture_user_deadline@example.com")
    gid = insert_test_grant(cursor, grant_name="Fixture Grant Deadline")
    aid = insert_test_application(cursor, uid, gid)
    return uid, gid, aid


def test_create_internal_deadline(cursor, uid, aid):
    log_default("Running test_create_internal_deadline()")
    
    deadline_date = datetime.now() + timedelta(days=30)
    result = create_internal_deadline(
        Role.USER, uid, uid, cursor,
        deadline_name="Test Deadline",
        deadline_date=deadline_date,
        application_id=aid
    )
    
    if result is None:
        cursor.execute(
            "SELECT deadline_name FROM InternalDeadlines WHERE application_id=UUID_TO_BIN(%s) AND deadline_name='Test Deadline'",
            (aid,)
        )
        row = cursor.fetchone()
        if row and row[0] == "Test Deadline":
            log_info(" PASS: create_internal_deadline successfully created deadline")
        else:
            log_error(f" FAIL: Deadline not found or incorrect: {row}")
    else:
        log_error(f" FAIL: create_internal_deadline returned error: {result}")


def test_read_internal_deadline_by_uuid(cursor, uid, aid):
    log_default("Running test_read_internal_deadline_by_uuid()")
    
    deadline_date = datetime.now() + timedelta(days=45)
    create_internal_deadline(
        Role.USER, uid, uid, cursor,
        deadline_name="Read Test Deadline",
        deadline_date=deadline_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(internal_deadline_id) FROM InternalDeadlines WHERE application_id=UUID_TO_BIN(%s) AND deadline_name='Read Test Deadline'",
        (aid,)
    )
    deadline_id = cursor.fetchone()[0]
    
    result = read_internal_deadline_by_uuid(Role.USER, uid, uid, cursor, deadline_id)
    
    if isinstance(result, tuple) and result[1] == "Read Test Deadline":
        log_info(" PASS: read_internal_deadline_by_uuid returned correct row")
    else:
        log_error(f" FAIL: Unexpected return: {result}")


def test_update_internal_deadline(cursor, uid, aid):
    log_default("Running test_update_internal_deadline()")
    
    deadline_date = datetime.now() + timedelta(days=60)
    create_internal_deadline(
        Role.USER, uid, uid, cursor,
        deadline_name="Original Deadline",
        deadline_date=deadline_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(internal_deadline_id) FROM InternalDeadlines WHERE application_id=UUID_TO_BIN(%s) AND deadline_name='Original Deadline'",
        (aid,)
    )
    deadline_id = cursor.fetchone()[0]
    
    new_date = datetime.now() + timedelta(days=90)
    new_fields = {
        "deadline_name": "Updated Deadline",
        "deadline_date": new_date
    }
    
    result = update_internal_deadline(Role.USER, uid, uid, cursor, deadline_id, **new_fields)
    
    if result is None:
        cursor.execute(
            "SELECT deadline_name, deadline_date FROM InternalDeadlines WHERE internal_deadline_id=UUID_TO_BIN(%s)",
            (deadline_id,)
        )
        row = cursor.fetchone()
        if row and row[0] == "Updated Deadline":
            log_info(" PASS: update_internal_deadline persisted changes")
        else:
            log_error(f" FAIL: DB row mismatch. Expected 'Updated Deadline', got {row}")
    else:
        log_error(f" FAIL: update_internal_deadline returned error: {result}")


def test_delete_internal_deadline(cursor, uid, aid):
    log_default("Running test_delete_internal_deadline()")
    
    deadline_date = datetime.now() + timedelta(days=15)
    create_internal_deadline(
        Role.USER, uid, uid, cursor,
        deadline_name="Delete Me Deadline",
        deadline_date=deadline_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(internal_deadline_id) FROM InternalDeadlines WHERE application_id=UUID_TO_BIN(%s) AND deadline_name='Delete Me Deadline'",
        (aid,)
    )
    deadline_id = cursor.fetchone()[0]
    
    result = delete_internal_deadline(Role.USER, uid, uid, cursor, deadline_id)
    
    if result is None:
        cursor.execute(
            "SELECT COUNT(*) FROM InternalDeadlines WHERE internal_deadline_id=UUID_TO_BIN(%s)",
            (deadline_id,)
        )
        if cursor.fetchone()[0] == 0:
            log_info(" PASS: delete_internal_deadline removed deadline")
        else:
            log_error(" FAIL: deadline still exists in DB")
    else:
        log_error(f" FAIL: delete_internal_deadline returned error: {result}")


if __name__ == "__main__":
    cnx, cursor = setup_db()

    # Create shared test fixtures
    uid, gid, aid = create_test_fixtures(cursor)
    cnx.commit()

    # Run all internal deadline function tests
    test_create_internal_deadline(cursor, uid, aid)
    cnx.commit()
    
    test_read_internal_deadline_by_uuid(cursor, uid, aid)
    cnx.commit()
    
    test_update_internal_deadline(cursor, uid, aid)
    cnx.commit()
    
    test_delete_internal_deadline(cursor, uid, aid)
    cnx.commit()

    cursor.close()
    cnx.close()
