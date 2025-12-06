'''
      applications_entity_test_suite.py
      Author: Generated based on Abdullahi Abdullahi's SQL scripts
      Version: 15 November 2025
      Description: 
            Extensive testing suite for CRUD operations for Applications entities
            Tests all application SQL scripts for correctness and edge cases

      Usage:
        The Database must be empty before running this script
        from root: python -m src.test_suites.applications_entity_test_suite
'''
import os
import mysql.connector
from pathlib import Path
from datetime import date, timedelta
from uuid import uuid4

from dotenv import load_dotenv
import sys
from mysql.connector import errorcode

import mysql.connector as connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.utils.logging_utils import log_info, log_error, log_default


load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")


# SQL Script Paths
CREATE_SCRIPT = "src/db_crud/applications/create_application.sql"
DELETE_BY_ID_SCRIPT = "src/db_crud/applications/delete_application_by_id.sql"
DELETE_BY_USER_GRANT_SCRIPT = "src/db_crud/applications/delete_application_by_grant_and_user.sql"
DELETE_BY_USER_SCRIPT = "src/db_crud/applications/delete_application_by_user.sql"
DELETE_BY_GRANT_SCRIPT = "src/db_crud/applications/delete_application_by_grant.sql"
DELETE_ALL_SCRIPT = "src/db_crud/applications/delete_application.sql"
SELECT_BY_ID_SCRIPT = "src/db_crud/applications/select_application_by_id.sql"
SELECT_BY_USER_SCRIPT = "src/db_crud/applications/select_application_by_user.sql"
SELECT_BY_GRANT_SCRIPT = "src/db_crud/applications/select_application_by_grant.sql"
SELECT_BY_STATUS_SCRIPT = "src/db_crud/applications/select_application_by_status.sql"
UPDATE_STATUS_SCRIPT = "src/db_crud/applications/update_application_status.sql"

cnx = None

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
        log_error(f"Access denied. Check MySQL user and password. Error {err.errno}")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)


def setup_test_data():
    """
    Create test users and grants that applications can reference.
    Returns: (user_id_str, grant_id_str)
    """
    # Create test user
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Test', 'User', 'testuser@example.com', 'pw123')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='testuser@example.com'")
    user_id = cursor.fetchone()[0]
    
    # Create second test user for multi-user tests
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Second', 'User', 'seconduser@example.com', 'pw456')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='seconduser@example.com'")
    user_id_2 = cursor.fetchone()[0]

    # Create test grant
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Test Grant 2025', 'http://example.com/grant1')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Test Grant 2025'")
    grant_id = cursor.fetchone()[0]
    
    # Create second test grant
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Second Test Grant', 'http://example.com/grant2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Second Test Grant'")
    grant_id_2 = cursor.fetchone()[0]

    cnx.commit()
    return user_id, user_id_2, grant_id, grant_id_2


def create_application_tests(user_id, grant_id, user_id_2, grant_id_2):
    """
    Test suite for creating applications.
    
    Tests:
        1. Valid application creation
        2. Duplicate application (same user + grant)
        3. Missing required fields
        4. Invalid UUID references
        5. Multiple applications by same user to different grants
        6. Multiple users applying to same grant
        7. Status validation
        8. Date handling
    """
    log_default("Running create_application_tests()")

    with open(CREATE_SCRIPT, "r") as f:
        sql_script = f.read()

    def try_insert(app_data, expected_success=True, case_desc=""):
        test_cnx = connector.connect(
            host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME
        )
        test_cursor = test_cnx.cursor()
        try:
            test_cursor.execute(sql_script, app_data)
            test_cnx.commit()
            if expected_success:
                log_info(f" ✅ PASS: {case_desc}")
            else:
                log_error(f" ❌ FAIL: {case_desc} (expected failure, got success)")
        except mysql.connector.Error as err:
            test_cnx.rollback()
            if expected_success:
                log_error(f" ❌ FAIL: {case_desc} (unexpected error: {err})")
            else:
                log_info(f" ✅ PASS: {case_desc} (expected error: {err.errno})")
        finally:
            test_cursor.close()
            test_cnx.close()

    today = date.today().isoformat()

    # 1. Valid application creation
    try_insert({
        "user_id": user_id,
        "grant_id": grant_id,
        "status": "pending",
        "application_date": today
    }, True, "Valid application creation")

    # 2. Duplicate application (same user + grant) - should fail due to UNIQUE constraint
    try_insert({
        "user_id": user_id,
        "grant_id": grant_id,
        "status": "pending",
        "application_date": today
    }, False, "Duplicate application (same user + grant)")

    # 3. Missing grant_id (NOT NULL constraint)
    try_insert({
        "user_id": user_id,
        "grant_id": None,
        "status": "pending",
        "application_date": today
    }, False, "Missing grant_id")

    # 4. Missing status (has default, should succeed)
    try_insert({
        "user_id": user_id,
        "grant_id": grant_id_2,
        "status": "pending",
        "application_date": today
    }, True, "Valid application to second grant")

    # 5. Missing application_date (NOT NULL constraint)
    try_insert({
        "user_id": user_id_2,
        "grant_id": grant_id,
        "status": "pending",
        "application_date": None
    }, False, "Missing application_date")

    # 6. Invalid user_id (foreign key violation)
    fake_user_id = str(uuid4())
    try_insert({
        "user_id": fake_user_id,
        "grant_id": grant_id,
        "status": "pending",
        "application_date": today
    }, False, "Invalid user_id (foreign key violation)")

    # 7. Invalid grant_id (foreign key violation)
    fake_grant_id = str(uuid4())
    try_insert({
        "user_id": user_id,
        "grant_id": fake_grant_id,
        "status": "pending",
        "application_date": today
    }, False, "Invalid grant_id (foreign key violation)")

    # 8. Multiple users can apply to same grant
    try_insert({
        "user_id": user_id_2,
        "grant_id": grant_id,
        "status": "pending",
        "application_date": today
    }, True, "Multiple users applying to same grant")

    # 9. Status too long (VARCHAR(20) limit)
    try_insert({
        "user_id": user_id_2,
        "grant_id": grant_id_2,
        "status": "this_status_is_way_too_long_for_the_field",
        "application_date": today
    }, False, "Status exceeds VARCHAR(20) limit")

    # 10. Valid different statuses
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Status', 'Tester', 'statustester@example.com', 'pw789')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='statustester@example.com'")
    status_user_id = cursor.fetchone()[0]
    cnx.commit()  # Commit before creating grants
    
    for status in ["approved", "rejected", "submitted"]:
        cursor.execute("""
            INSERT INTO Grants (grant_title, link_to_source)
            VALUES (%s, %s)
        """, (f"Grant for {status}", f"http://example.com/{status}"))
        cnx.commit()  # Commit each grant
        cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title=%s", (f"Grant for {status}",))
        temp_grant_id = cursor.fetchone()[0]
        
        try_insert({
            "user_id": status_user_id,
            "grant_id": temp_grant_id,
            "status": status,
            "application_date": today
        }, True, f"Valid status: {status}")

    # 11. Verify application_id UUID generated
    cursor.execute("SELECT application_id FROM Applications LIMIT 1")
    app_id = cursor.fetchone()
    if app_id and len(app_id[0]) == 16:
        log_info(" ✅ PASS: Application UUID generated correctly (16-byte binary)")
    else:
        log_error(" ❌ FAIL: Application UUID not generated correctly")


def select_application_by_id_tests(user_id, grant_id):
    """
    Test suite for selecting applications by ID.
    
    Tests:
        1. Select existing application
        2. Select non-existent application
        3. Validate all returned columns
        4. UUID conversion correctness
    """
    log_default("Running select_application_by_id_tests()")

    with open(SELECT_BY_ID_SCRIPT, "r") as f:
        select_sql = f.read()

    # Create new test grant to avoid duplicate constraint
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Select Test Grant', 'http://example.com/selecttest')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Select Test Grant'")
    test_grant_id = cursor.fetchone()[0]
    
    # Create test application with new grant
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, test_grant_id, today))
    
    cursor.execute("""
        SELECT BIN_TO_UUID(application_id) 
        FROM Applications 
        WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
    """, (user_id, grant_id))
    app_id = cursor.fetchone()[0]
    cnx.commit()

    # 1. Select existing application
    try:
        cursor.execute(select_sql, {"application_id": app_id})
        row = cursor.fetchone()
        if row and row[0] == app_id:  # row[0] = application_id
            log_info(" ✅ PASS: Successfully selected existing application by ID")
        else:
            log_error(f" ❌ FAIL: Application not returned correctly: {row}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting existing application raised error: {e}")

    # 2. Select non-existent application
    fake_app_id = str(uuid4())
    try:
        cursor.execute(select_sql, {"application_id": fake_app_id})
        row = cursor.fetchone()
        if row is None:
            log_info(" ✅ PASS: Selecting non-existent application returned no results")
        else:
            log_error(f" ❌ FAIL: Non-existent application returned a row: {row}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting non-existent application raised error: {e}")

    # 3. Validate all returned columns
    try:
        cursor.execute(select_sql, {"application_id": app_id})
        row = cursor.fetchone()
        # Expected: application_id, user_id, grant_id, status, application_date
        if row and len(row) == 5:
            log_info(" ✅ PASS: All expected columns returned (5 columns)")
        else:
            log_error(f" ❌ FAIL: Expected 5 columns, got {len(row) if row else 0}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Column validation raised error: {e}")

    # 4. Verify UUIDs are returned as strings, not binary
    try:
        cursor.execute(select_sql, {"application_id": app_id})
        row = cursor.fetchone()
        if row and isinstance(row[0], str) and isinstance(row[1], str) and isinstance(row[2], str):
            log_info(" ✅ PASS: UUIDs returned as strings (BIN_TO_UUID working)")
        else:
            log_error(f" ❌ FAIL: UUIDs not returned as strings: {type(row[0]) if row else None}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: UUID validation raised error: {e}")


def select_application_by_user_tests(user_id, grant_id, grant_id_2):
    """
    Test suite for selecting applications by user.
    
    Tests:
        1. Select all applications for a user with multiple applications
        2. Select applications for user with no applications
        3. Verify correct number of results
    """
    log_default("Running select_application_by_user_tests()")

    with open(SELECT_BY_USER_SCRIPT, "r") as f:
        select_sql = f.read()

    # Create unique grants for this test to avoid duplicates
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('User Test Grant 1', 'http://example.com/usertest1')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='User Test Grant 1'")
    user_test_grant_1 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('User Test Grant 2', 'http://example.com/usertest2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='User Test Grant 2'")
    user_test_grant_2 = cursor.fetchone()[0]
    cnx.commit()

    # Create multiple applications for the same user
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, user_test_grant_1, today))
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'approved', %s)
    """, (user_id, user_test_grant_2, today))
    cnx.commit()

    # 1. Select all applications for user
    try:
        cursor.execute(select_sql, {"user_id": user_id})
        rows = cursor.fetchall()
        if len(rows) >= 2:  # Should have at least 2 applications
            log_info(f" ✅ PASS: Selected {len(rows)} applications for user")
        else:
            log_error(f" ❌ FAIL: Expected at least 2 applications, got {len(rows)}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting applications by user raised error: {e}")

    # 2. Select applications for user with no applications
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('No', 'Apps', 'noapps@example.com', 'pw000')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='noapps@example.com'")
    empty_user_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute(select_sql, {"user_id": empty_user_id})
        rows = cursor.fetchall()
        if len(rows) == 0:
            log_info(" ✅ PASS: User with no applications returned empty result")
        else:
            log_error(f" ❌ FAIL: Expected 0 applications, got {len(rows)}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting applications for empty user raised error: {e}")

    # 3. Verify non-existent user returns empty
    fake_user_id = str(uuid4())
    try:
        cursor.execute(select_sql, {"user_id": fake_user_id})
        rows = cursor.fetchall()
        if len(rows) == 0:
            log_info(" ✅ PASS: Non-existent user returned empty result")
        else:
            log_error(f" ❌ FAIL: Non-existent user returned {len(rows)} rows")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Non-existent user query raised error: {e}")


def select_application_by_grant_tests(user_id, user_id_2, grant_id):
    """
    Test suite for selecting applications by grant.
    
    Tests:
        1. Select all applications for a grant with multiple applicants
        2. Select applications for grant with no applications
        3. Verify correct number of results
    """
    log_default("Running select_application_by_grant_tests()")

    with open(SELECT_BY_GRANT_SCRIPT, "r") as f:
        select_sql = f.read()

    # Create unique grant for this test
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Grant Test Multi User', 'http://example.com/grantmulti')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Grant Test Multi User'")
    grant_test_id = cursor.fetchone()[0]
    cnx.commit()

    # Create multiple applications for the same grant
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, grant_test_id, today))
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'submitted', %s)
    """, (user_id_2, grant_test_id, today))
    cnx.commit()

    # 1. Select all applications for grant
    try:
        cursor.execute(select_sql, {"grant_id": grant_test_id})
        rows = cursor.fetchall()
        if len(rows) >= 2:
            log_info(f" ✅ PASS: Selected {len(rows)} applications for grant")
        else:
            log_error(f" ❌ FAIL: Expected at least 2 applications, got {len(rows)}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting applications by grant raised error: {e}")

    # 2. Select applications for grant with no applications
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Empty Grant', 'http://example.com/empty')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Empty Grant'")
    empty_grant_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute(select_sql, {"grant_id": empty_grant_id})
        rows = cursor.fetchall()
        if len(rows) == 0:
            log_info(" ✅ PASS: Grant with no applications returned empty result")
        else:
            log_error(f" ❌ FAIL: Expected 0 applications, got {len(rows)}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting applications for empty grant raised error: {e}")


def select_application_by_status_tests(user_id, grant_id, grant_id_2):
    """
    Test suite for selecting applications by status.
    
    Tests:
        1. Select applications with specific status
        2. Select applications with status that doesn't exist
        3. Case sensitivity of status matching
    """
    log_default("Running select_application_by_status_tests()")

    with open(SELECT_BY_STATUS_SCRIPT, "r") as f:
        select_sql = f.read()

    # Create unique grants for status tests
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Status Test Grant 1', 'http://example.com/statustest1')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Status Test Grant 1'")
    status_grant_1 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Status Test Grant 2', 'http://example.com/statustest2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Status Test Grant 2'")
    status_grant_2 = cursor.fetchone()[0]
    cnx.commit()

    # Create applications with various statuses
    today = date.today().isoformat()
    
    # Create user for status tests
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Status', 'Test', 'statustest@example.com', 'pw111')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='statustest@example.com'")
    status_user = cursor.fetchone()[0]
    cnx.commit()
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'approved', %s)
    """, (status_user, status_grant_1, today))
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'approved', %s)
    """, (user_id, status_grant_2, today))
    cnx.commit()

    # 1. Select applications with 'approved' status
    try:
        cursor.execute(select_sql, {"status": "approved"})
        rows = cursor.fetchall()
        if len(rows) >= 2:
            log_info(f" ✅ PASS: Selected {len(rows)} applications with 'approved' status")
        else:
            log_error(f" ❌ FAIL: Expected at least 2 'approved' applications, got {len(rows)}")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Selecting by status raised error: {e}")

    # 2. Select applications with non-existent status
    try:
        cursor.execute(select_sql, {"status": "nonexistent_status"})
        rows = cursor.fetchall()
        if len(rows) == 0:
            log_info(" ✅ PASS: Non-existent status returned empty result")
        else:
            log_error(f" ❌ FAIL: Non-existent status returned {len(rows)} rows")
    except mysql.connector.Error as e:
        log_error(f" ❌ FAIL: Non-existent status query raised error: {e}")


def update_application_status_tests(user_id, grant_id):
    """
    Test suite for updating application status.
    
    Tests:
        1. Update status for existing application
        2. Verify other fields unchanged
        3. Update non-existent application
        4. Status trimming
    """
    log_default("Running update_application_status_tests()")

    with open(UPDATE_STATUS_SCRIPT, "r") as f:
        update_sql = f.read()

    # Create unique grant for update tests
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Update Status Test Grant', 'http://example.com/updatetest')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Update Status Test Grant'")
    update_grant_id = cursor.fetchone()[0]
    cnx.commit()

    # Create test application
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, update_grant_id, today))
    
    cursor.execute("""
        SELECT BIN_TO_UUID(application_id)
        FROM Applications
        WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
    """, (user_id, update_grant_id))
    app_id = cursor.fetchone()[0]
    cnx.commit()

    # 1. Update status
    try:
        cursor.execute(update_sql, {"application_id": app_id, "status": "approved"})
        cnx.commit()
        log_info(" ✅ PASS: Status update executed without error")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Updating status raised error: {e}")

    # 2. Verify status updated and other fields unchanged
    cursor.execute("""
        SELECT BIN_TO_UUID(user_id), BIN_TO_UUID(grant_id), status, application_date
        FROM Applications
        WHERE application_id = UUID_TO_BIN(%s)
    """, (app_id,))
    row = cursor.fetchone()
    
    if row and row[2] == "approved" and row[0] == user_id and row[1] == update_grant_id and str(row[3]) == today:
        log_info(" ✅ PASS: Status updated correctly; other fields unchanged")
    else:
        log_error(f" ❌ FAIL: Status update verification failed: {row}")

    # 3. Update non-existent application
    fake_app_id = str(uuid4())
    try:
        cursor.execute(update_sql, {"application_id": fake_app_id, "status": "rejected"})
        cnx.commit()
        log_info(" ✅ PASS: Updating non-existent application did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Updating non-existent application raised error: {e}")

    # 4. Test status trimming (whitespace should be removed)
    try:
        cursor.execute(update_sql, {"application_id": app_id, "status": "  rejected  "})
        cnx.commit()
        cursor.execute("""
            SELECT status FROM Applications WHERE application_id = UUID_TO_BIN(%s)
        """, (app_id,))
        status = cursor.fetchone()[0]
        if status == "rejected":
            log_info(" ✅ PASS: Status trimming works correctly")
        else:
            log_error(f" ❌ FAIL: Status not trimmed: '{status}'")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Status trimming test raised error: {e}")


def delete_application_by_id_tests(user_id, grant_id):
    """
    Test suite for deleting applications by ID.
    
    Tests:
        1. Delete existing application
        2. Delete non-existent application
        3. Verify deletion
    """
    log_default("Running delete_application_by_id_tests()")

    with open(DELETE_BY_ID_SCRIPT, "r") as f:
        delete_sql = f.read()

    # Create unique grant for delete test
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete By ID Test Grant', 'http://example.com/deleteidtest')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete By ID Test Grant'")
    delete_grant_id = cursor.fetchone()[0]
    cnx.commit()

    # Create test application
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, delete_grant_id, today))
    
    cursor.execute("""
        SELECT BIN_TO_UUID(application_id)
        FROM Applications
        WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
    """, (user_id, delete_grant_id))
    app_id = cursor.fetchone()[0]
    cnx.commit()

    # 1. Delete existing application
    try:
        cursor.execute(delete_sql, {"application_id": app_id})
        cnx.commit()
        
        # Verify deletion
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE application_id = UUID_TO_BIN(%s)
        """, (app_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            log_info(" ✅ PASS: Successfully deleted existing application")
        else:
            log_error(f" ❌ FAIL: Application not deleted (count: {count})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting application raised error: {e}")

    # 2. Delete non-existent application
    fake_app_id = str(uuid4())
    try:
        cursor.execute(delete_sql, {"application_id": fake_app_id})
        cnx.commit()
        log_info(" ✅ PASS: Deleting non-existent application did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting non-existent application raised error: {e}")


def delete_application_by_user_grant_tests(user_id, grant_id):
    """
    Test suite for deleting applications by user and grant.
    
    Tests:
        1. Delete existing application by user_id and grant_id
        2. Delete non-existent combination
        3. Verify specific deletion (doesn't affect other applications)
    """
    log_default("Running delete_application_by_user_grant_tests()")

    with open(DELETE_BY_USER_GRANT_SCRIPT, "r") as f:
        delete_sql = f.read()

    # Create unique grants for this test
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User-Grant Test 1', 'http://example.com/deleteug1')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User-Grant Test 1'")
    delete_ug_grant_1 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User-Grant Test 2', 'http://example.com/deleteug2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User-Grant Test 2'")
    delete_ug_grant_2 = cursor.fetchone()[0]
    cnx.commit()

    # Create multiple test applications
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, delete_ug_grant_1, today))
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, delete_ug_grant_2, today))
    cnx.commit()

    # 1. Delete specific user-grant combination
    try:
        cursor.execute(delete_sql, {"user_id": user_id, "grant_id": delete_ug_grant_1})
        cnx.commit()
        
        # Verify specific deletion
        cursor.execute("""
            SELECT COUNT(*) FROM Applications 
            WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
        """, (user_id, delete_ug_grant_1))
        count = cursor.fetchone()[0]
        
        # Verify other application still exists
        cursor.execute("""
            SELECT COUNT(*) FROM Applications 
            WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
        """, (user_id, delete_ug_grant_2))
        other_count = cursor.fetchone()[0]
        
        if count == 0 and other_count == 1:
            log_info(" ✅ PASS: Successfully deleted specific user-grant application")
        else:
            log_error(f" ❌ FAIL: Deletion incorrect (deleted: {count == 0}, other exists: {other_count == 1})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting by user-grant raised error: {e}")

    # 2. Delete non-existent combination
    fake_user_id = str(uuid4())
    try:
        cursor.execute(delete_sql, {"user_id": fake_user_id, "grant_id": grant_id})
        cnx.commit()
        log_info(" ✅ PASS: Deleting non-existent user-grant combination did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting non-existent combination raised error: {e}")


def delete_applications_by_user_tests(user_id, grant_id, grant_id_2):
    """
    Test suite for deleting all applications by user.
    
    Tests:
        1. Delete all applications for a user with multiple applications
        2. Delete for user with no applications
        3. Verify other users' applications unaffected
    """
    log_default("Running delete_applications_by_user_tests()")

    with open(DELETE_BY_USER_SCRIPT, "r") as f:
        delete_sql = f.read()

    # Create unique grants for this test
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User Test Grant 1', 'http://example.com/delusertest1')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User Test Grant 1'")
    del_user_grant_1 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User Test Grant 2', 'http://example.com/delusertest2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User Test Grant 2'")
    del_user_grant_2 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User Test Grant 3', 'http://example.com/delusertest3')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User Test Grant 3'")
    del_user_grant_3 = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete User Test Grant 4', 'http://example.com/delusertest4')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete User Test Grant 4'")
    del_user_grant_4 = cursor.fetchone()[0]
    cnx.commit()

    # Create test user with multiple applications
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Delete', 'User', 'deleteuser@example.com', 'pw222')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='deleteuser@example.com'")
    delete_user_id = cursor.fetchone()[0]
    
    # Create another user for "other applications" test
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Keep', 'User', 'keepuser@example.com', 'pw223')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='keepuser@example.com'")
    keep_user_id = cursor.fetchone()[0]
    cnx.commit()
    
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (delete_user_id, del_user_grant_1, today))  # ← CHANGED: uses delete_user_id and del_user_grant_1
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (delete_user_id, del_user_grant_2, today))  # ← CHANGED: uses delete_user_id and del_user_grant_2
    
    # Keep track of another user's application with different grant
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (keep_user_id, del_user_grant_3, today))  # ← CHANGED: uses keep_user_id and del_user_grant_3
    cnx.commit()

    # 1. Delete all applications for user
    try:
        cursor.execute(delete_sql, {"user_id": delete_user_id})
        cnx.commit()
        
        # Verify all deleted
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE user_id = UUID_TO_BIN(%s)
        """, (delete_user_id,))
        count = cursor.fetchone()[0]
        
        # Verify other user's application still exists
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE user_id = UUID_TO_BIN(%s)
        """, (keep_user_id,))
        other_count = cursor.fetchone()[0]
        
        if count == 0 and other_count >= 1:
            log_info(" ✅ PASS: Successfully deleted all applications for user; others unaffected")
        else:
            log_error(f" ❌ FAIL: Delete by user failed (user apps: {count}, other apps: {other_count})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting by user raised error: {e}")

    # 2. Delete for user with no applications
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Empty', 'User', 'emptyuser@example.com', 'pw333')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='emptyuser@example.com'")
    empty_user_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute(delete_sql, {"user_id": empty_user_id})
        cnx.commit()
        log_info(" ✅ PASS: Deleting applications for user with no applications did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting for empty user raised error: {e}")

def delete_applications_by_grant_tests(user_id, user_id_2, grant_id):
    """
    Test suite for deleting all applications by grant.
    
    Tests:
        1. Delete all applications for a grant with multiple applicants
        2. Delete for grant with no applications
        3. Verify other grants' applications unaffected
    """
    log_default("Running delete_applications_by_grant_tests()")

    with open(DELETE_BY_GRANT_SCRIPT, "r") as f:
        delete_sql = f.read()

    # Create unique grants for this test
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete Grant Test Main', 'http://example.com/delgrantmain')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete Grant Test Main'")
    delete_grant_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Delete Grant Test Other', 'http://example.com/delgrantother')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Delete Grant Test Other'")
    other_grant_id = cursor.fetchone()[0]
    cnx.commit()
    
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, delete_grant_id, today))
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id_2, delete_grant_id, today))
    
    # Keep another grant's application
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, other_grant_id, today))  # ← FIXED: uses other_grant_id
    cnx.commit()

    # 1. Delete all applications for grant
    try:
        cursor.execute(delete_sql, {"grant_id": delete_grant_id})
        cnx.commit()
        
        # Verify all deleted
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE grant_id = UUID_TO_BIN(%s)
        """, (delete_grant_id,))
        count = cursor.fetchone()[0]
        
        # Verify other grant's application still exists
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE grant_id = UUID_TO_BIN(%s)
        """, (other_grant_id,))  # ← FIXED: uses other_grant_id
        other_count = cursor.fetchone()[0]
        
        if count == 0 and other_count >= 1:
            log_info(" ✅ PASS: Successfully deleted all applications for grant; others unaffected")
        else:
            log_error(f" ❌ FAIL: Delete by grant failed (grant apps: {count}, other apps: {other_count})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting by grant raised error: {e}")

    # 2. Delete for grant with no applications
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Empty Delete Grant', 'http://example.com/emptydelete')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Empty Delete Grant'")
    empty_grant_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute(delete_sql, {"grant_id": empty_grant_id})
        cnx.commit()
        log_info(" ✅ PASS: Deleting applications for grant with no applications did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Deleting for empty grant raised error: {e}")

def cascade_delete_tests(user_id, grant_id):
    """
    Test suite for cascade deletion behavior.
    
    Tests:
        1. Deleting a user cascades to delete their applications
        2. Deleting a grant cascades to delete associated applications
    """
    log_default("Running cascade_delete_tests()")

    today = date.today().isoformat()

    # 1. Test user cascade delete
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Cascade', 'User', 'cascadeuser@example.com', 'pw444')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='cascadeuser@example.com'")
    cascade_user_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (cascade_user_id, grant_id, today))
    cnx.commit()

    try:
        # Delete user
        cursor.execute("DELETE FROM Users WHERE user_id = UUID_TO_BIN(%s)", (cascade_user_id,))
        cnx.commit()
        
        # Verify application was cascade deleted
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE user_id = UUID_TO_BIN(%s)
        """, (cascade_user_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            log_info(" ✅ PASS: Deleting user cascaded to delete their applications")
        else:
            log_error(f" ❌ FAIL: Applications not cascade deleted (count: {count})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: User cascade delete raised error: {e}")

    # 2. Test grant cascade delete
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Cascade Grant', 'http://example.com/cascadegrant')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Cascade Grant'")
    cascade_grant_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, cascade_grant_id, today))
    cnx.commit()

    try:
        # Delete grant
        cursor.execute("DELETE FROM Grants WHERE grant_id = UUID_TO_BIN(%s)", (cascade_grant_id,))
        cnx.commit()
        
        # Verify application was cascade deleted
        cursor.execute("""
            SELECT COUNT(*) FROM Applications WHERE grant_id = UUID_TO_BIN(%s)
        """, (cascade_grant_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            log_info(" ✅ PASS: Deleting grant cascaded to delete associated applications")
        else:
            log_error(f" ❌ FAIL: Applications not cascade deleted (count: {count})")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Grant cascade delete raised error: {e}")


def unique_constraint_tests(user_id, grant_id):
    """
    Test suite for UNIQUE constraint on (user_id, grant_id).
    
    Tests:
        1. User cannot apply to same grant twice
        2. User can apply to different grants
        3. Different users can apply to same grant
    """
    log_default("Running unique_constraint_tests()")

    today = date.today().isoformat()

    # Create unique grant for constraint tests
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Unique Constraint Test Grant', 'http://example.com/uniquetest')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Unique Constraint Test Grant'")
    unique_grant_id = cursor.fetchone()[0]
    cnx.commit()

    # 1. Create initial application
    cursor.execute("""
        INSERT INTO Applications (user_id, grant_id, status, application_date)
        VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
    """, (user_id, unique_grant_id, today))
    cnx.commit()

    # 2. Try to create duplicate (should fail)
    try:
        cursor.execute("""
            INSERT INTO Applications (user_id, grant_id, status, application_date)
            VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'approved', %s)
        """, (user_id, unique_grant_id, today))
        cnx.commit()
        log_error(" ❌ FAIL: Duplicate user-grant application was allowed")
    except mysql.connector.Error as e:
        cnx.rollback()
        if e.errno == 1062:  # Duplicate entry error
            log_info(" ✅ PASS: UNIQUE constraint prevented duplicate user-grant application")
        else:
            log_error(f" ❌ FAIL: Unexpected error on duplicate: {e}")

    # 3. User can apply to different grant
    cursor.execute("""
        INSERT INTO Grants (grant_title, link_to_source)
        VALUES ('Unique Test Grant 2', 'http://example.com/uniquetest2')
    """)
    cursor.execute("SELECT BIN_TO_UUID(grant_id) FROM Grants WHERE grant_title='Unique Test Grant 2'")
    other_grant_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute("""
            INSERT INTO Applications (user_id, grant_id, status, application_date)
            VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
        """, (user_id, other_grant_id, today))
        cnx.commit()
        log_info(" ✅ PASS: User can apply to different grants")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: User applying to different grant raised error: {e}")

    # 4. Different user can apply to same grant
    cursor.execute("""
        INSERT INTO Users (f_name, l_name, email, password)
        VALUES ('Unique', 'User', 'uniqueuser@example.com', 'pw555')
    """)
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='uniqueuser@example.com'")
    other_user_id = cursor.fetchone()[0]
    cnx.commit()

    try:
        cursor.execute("""
            INSERT INTO Applications (user_id, grant_id, status, application_date)
            VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), 'pending', %s)
        """, (other_user_id, unique_grant_id, today))
        cnx.commit()
        log_info(" ✅ PASS: Different users can apply to same grant")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" ❌ FAIL: Different user applying to same grant raised error: {e}")

if __name__ == "__main__":
    try:
        log_info("=" * 60)
        log_info("STARTING APPLICATION ENTITY TEST SUITE")
        log_info("=" * 60)
        
        # Setup test data (users and grants)
        user_id, user_id_2, grant_id, grant_id_2 = setup_test_data()
        log_info(f"Test data created: user_id={user_id}, grant_id={grant_id}")
        
        # Run all test suites
        create_application_tests(user_id, grant_id, user_id_2, grant_id_2)
        select_application_by_id_tests(user_id, grant_id)
        select_application_by_user_tests(user_id, grant_id, grant_id_2)
        select_application_by_grant_tests(user_id, user_id_2, grant_id)
        select_application_by_status_tests(user_id, grant_id, grant_id_2)
        update_application_status_tests(user_id, grant_id)
        delete_application_by_id_tests(user_id, grant_id)
        delete_application_by_user_grant_tests(user_id, grant_id)
        delete_applications_by_user_tests(user_id, grant_id, grant_id_2)
        delete_applications_by_grant_tests(user_id, user_id_2, grant_id)
        cascade_delete_tests(user_id, grant_id)
        unique_constraint_tests(user_id, grant_id)
        
        log_info("=" * 60)
        log_info("APPLICATION ENTITY TEST SUITE COMPLETED")
        log_info("=" * 60)
        
    except Exception as e:
        log_error(f"Fatal error in test suite: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cnx and cnx.is_connected():
            cursor.close()
            cnx.close()
            log_info("Database connection closed")