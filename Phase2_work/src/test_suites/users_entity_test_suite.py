'''
      users_entity_test_suite.py
      Author: Colby Wirth
      Version: 8 November 2025
      Description: 
            Extensive testing suite for crud operations for Users entities
            Generated with the assistance of AI tools

      Usage:
        The Database must be empty before running this script
        from root: python3 -m src.tests.users_entity_test_suite
'''
import os
import mysql.connector
from pathlib import Path

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


CREATE_SCRIPT = "src/db_crud/users/create_users.sql"
DELETE_SCRIPT = "src/db_crud/users/delete_users.sql"
SELECT_SCRIPT = "src/db_crud/users/select_users_by_uuid.sql"
UPDATE_SCRIPT = "src/db_crud/users/update_users_fields.sql"
UPDATE_PW_SCRIPT = "src/db_crud/users/update_users_password.sql"

cnx  = None

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
        log_error(f"Access denied. Check MySQL user and password.  Error {err.errno}")
    else:
        log_error(f"MySQL Error: {err}")
    sys.exit(2)


def create_users_tests():
    log_default("Running create_users_tests()")

    sql_path = Path(CREATE_SCRIPT)
    with open(sql_path, "r") as f:
        sql_script = f.read()

    def try_insert(user_data, expected_success=True, case_desc=""):

        cnx: MySQLConnection = connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cursor: MySQLCursor = cnx.cursor()
        try:
            cursor.execute(sql_script, user_data)
            cnx.commit()
            if expected_success:
                log_info(f" PASS: {case_desc}")
            else:
                log_error(f" FAIL: {case_desc} (expected failure, got success)")
        except mysql.connector.Error as err:
            cnx.rollback()
            if expected_success:
                log_error(f" FAIL: {case_desc} (unexpected error: {err})")
            else:
                log_info(f" PASS: {case_desc} (expected error: {err})")

    # 1. Valid user
    try_insert({
        "f_name": "Alice",
        "m_name": "M",
        "l_name": "Smith",
        "institution": "MIT",
        "email": "alice@examplemit.com",
        "password": "pw"
    }, True, "Valid user creation")

    # 2. Duplicate email
    try_insert({
        "f_name": "Alice",
        "m_name": "M",
        "l_name": "Smith",
        "institution": "MIT",
        "email": "alice@examplemit.com",
        "password": "pw"
    }, False, "Duplicate email")

    # 3. Missing email
    try_insert({
        "f_name": "Bob",
        "m_name": None,
        "l_name": "Jones",
        "institution": "Stanford",
        "email": None,
        "password": "pw"
    }, False, "Missing email")

    # 4. Missing first name
    try_insert({
        "f_name": None,
        "m_name": None,
        "l_name": "Jones",
        "institution": "Stanford",
        "email": "bob@example.com",
        "password": "pw"
    }, False, "Missing first name")

    # 5. Missing last name
    try_insert({
        "f_name": "Bob",
        "m_name": None,
        "l_name": None,
        "institution": "Stanford",
        "email": "bob2@example.com",
        "password": "pw"
    }, False, "Missing last name")

    # 6. Missing password
    try_insert({
        "f_name": "Bob",
        "m_name": None,
        "l_name": "Jones",
        "institution": "Stanford",
        "email": "bob3@example.com",
        "password": None
    }, False, "Missing password")

    # 7. Optional institution (NULL)
    try_insert({
        "f_name": "Eve",
        "m_name": None,
        "l_name": "OptionalInstitution",
        "institution": None,
        "email": "eve@ex.com",
        "password": "pw"
    }, True, "Optional institution (NULL)")

    # 8. Institution too long
    try_insert({
        "f_name": "Frank",
        "m_name": None,
        "l_name": "TooLongInstitution",
        "institution": "A" * 60,
        "email": "frank@example.com",
        "password": "pw"
    }, False, "Institution exceeds VARCHAR(50) limit")

    # 9. Case-insensitive email uniqueness
    try_insert({
        "f_name": "Alice3",
        "m_name": None,
        "l_name": "CaseTest",
        "institution": "MIT",
        "email": "ALICE@EXAMPLEMIT.COM",  # match first inserted user
        "password": "pw"
    }, False, "Email uniqueness is case-insensitive")


    # 10. Verify UUID generated
    cursor.execute("SELECT user_id FROM Users WHERE email='alice@examplemit.com';")
    uid = cursor.fetchone()
    if uid and len(uid[0]) == 16:
        log_info(" PASS: UUID generated correctly (16-byte binary)")
    else:
        log_error(" FAIL: UUID not generated correctly")

    # 11. Transaction integrity on duplicate
    cursor.execute("SELECT COUNT(*) FROM Users WHERE email='alice@examplemit.com';")
    count = cursor.fetchone()[0]
    if count == 1:
        log_info(" PASS: Transaction rollback successful on duplicate insert")
    else:
        log_error(" FAIL: Duplicate insert created multiple records")


def delete_users_test():
    """
    Test suite for deleting users using SQL scripts.

    Tests:
        1. Delete existing user
        2. Delete non-existent user
        3. Delete user with associated research fields (cascade)
    """
    log_default("Running delete_users_test()")


    # Helper function to insert a test user via SQL script
    def insert_test_user(email):
        with open(CREATE_SCRIPT, "r") as f:
            sql_script = f.read()
        cursor.execute(sql_script, {
            "f_name": "Test",
            "m_name": None,
            "l_name": "User",
            "institution": "Test University",
            "email": email,
            "password": "hashedpass123"
        })
        cursor.execute("SELECT user_id FROM Users WHERE email=%s", (email,))
        return cursor.fetchone()[0]

    # 1. Delete existing user
    email1 = "delete_test1@example.com"
    user_id1 = insert_test_user(email1)

    with open(DELETE_SCRIPT, "r") as f:
        delete_sql = f.read()

    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (email1,))
    user_id1 = cursor.fetchone()[0] 
    cursor.execute(delete_sql, (user_id1,))
    cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id=%s", (user_id1,))
    if cursor.fetchone()[0] == 0:
        log_info(" PASS: Successfully deleted existing user")
    else:
        log_error(" FAIL: Existing user was not deleted")

    # 2. Delete non-existent user
    from uuid import uuid4
    fake_user_id = str(uuid4())
    try:
        cursor.execute(delete_sql, (fake_user_id,))
        log_info(" PASS: Deleting non-existent user did not crash")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Deleting non-existent user raised error: {e}")

    # 3. Delete user with research fields
    email2 = "delete_test2@example.com"
    user_id2 = insert_test_user(email2)

    # Add a research field directly
    cursor.execute(
        """
        INSERT INTO ResearchField (research_field) VALUES (%s)
        ON DUPLICATE KEY UPDATE research_field_id = LAST_INSERT_ID(research_field_id)
        """,
        ("Test Field",)
    )
    cursor.execute(
        "INSERT INTO UserResearchFields (user_id, research_field_id) VALUES (%s, LAST_INSERT_ID())",
        (user_id2,)
    )

    # Delete user
    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (email2,))
    user_id2 = cursor.fetchone()[0] 
    cursor.execute(delete_sql, (user_id2,))
    cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id=%s", (user_id2,))
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM UserResearchFields WHERE user_id=%s", (user_id2,))
    field_count = cursor.fetchone()[0]

    if user_count == 0 and field_count == 0:
        log_info(" PASS: Deleted user with research fields; cascade worked")
    else:
        log_error(" FAIL: Cascade delete did not remove all user research fields")

    cnx.commit()


def select_users_by_uuid_test():
    """
    Test suite for selecting users by UUID using SQL script.

    Tests:
        1. Select existing user by UUID
        2. Attempt to select non-existent user by UUID
        3. Validate all returned columns
    """
    log_default("Running select_users_by_uuid_test()")

    # Helper to insert test user and return string UUID
    def insert_test_user(email):
        with open(CREATE_SCRIPT, "r") as f:
            sql_script = f.read()
        cursor.execute(sql_script, {
            "f_name": "Test",
            "m_name": "M",
            "l_name": "User",
            "institution": "Test University",
            "email": email,
            "password": "hashedpass123"
        })
        # Fetch string UUID
        cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (email,))
        return cursor.fetchone()[0]

    with open(SELECT_SCRIPT, "r") as f:
        select_sql = f.read()

    # 1. Select existing user
    email1 = "select_test1@example.com"
    user_id1 = insert_test_user(email1)

    try:
        cursor.execute(select_sql, (user_id1,))
        row = cursor.fetchone()
        if row and row[5] == email1:  # row[5] = email
            log_info(" PASS: Successfully selected existing user by UUID")
        else:
            log_error(" FAIL: User not returned correctly")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Selecting existing user raised error: {e}")

    # 2. Select non-existent user
    from uuid import uuid4
    fake_user_id = str(uuid4())
    try:
        cursor.execute(select_sql, (fake_user_id,)) 
        row = cursor.fetchone()
        if row is None:
            log_info(" PASS: Selecting non-existent user returned no results")
        else:
            log_error(" FAIL: Non-existent user returned a row")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Selecting non-existent user raised error: {e}")

    # 3. Validate all returned columns
    # row = [user_id, f_name, m_name, l_name, institution, email, password]
    try:
        cursor.execute(select_sql, (user_id1,))
        row = cursor.fetchone()
        expected_columns = ["user_id", "f_name", "m_name", "l_name", "institution", "email", "password"]
        if row and len(row) == len(expected_columns):
            log_info(" PASS: All expected columns returned")
        else:
            log_error(" FAIL: Columns returned do not match expected")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Column validation raised error: {e}")

    cnx.commit()


def update_users_test():
    """
    Test suite for updating users using update_users.sql

    Tests:
        1. Update allowed fields (f_name, m_name, l_name, institution, email)
        2. Attempt to update UUID (should be ignored / fail)
        3. Attempt to update password (should not change)
        4. Check persistence of updates
        5. Email uniqueness check
    """
    log_default("Running update_users_test()")


    # Helper: insert test user
    def insert_test_user(email, password="pw123"):
        with open(CREATE_SCRIPT, "r") as f:
            sql_script = f.read()
        cursor.execute(sql_script, {
            "f_name": "Update",
            "m_name": "M",
            "l_name": "User",
            "institution": "Original University",
            "email": email,
            "password": password
        })
        cursor.execute("SELECT BIN_TO_UUID(user_id), password FROM Users WHERE email=%s", (email,))
        return cursor.fetchone()  # returns (user_id_str, password)

    # 1. Insert test user
    email_orig = "update_test@example.com"
    user_id_str, orig_password = insert_test_user(email_orig)

    # 2. Update allowed fields
    with open(UPDATE_SCRIPT, "r") as f:
        update_sql = f.read()
    try:
        cursor.execute(update_sql, {
            "user_id": user_id_str,
            "f_name": "UpdatedFirst",
            "m_name": "UpdatedMiddle",
            "l_name": "UpdatedLast",
            "institution": "Updated University",
            "email": "updated_email@example.com"
        })
        cnx.commit()
        log_info(" PASS: Updated allowed fields")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" FAIL: Updating allowed fields raised error: {e}")

    # 3. Verify updates persisted
    cursor.execute("SELECT f_name, m_name, l_name, institution, email, password FROM Users WHERE user_id=UUID_TO_BIN(%s)", (user_id_str,))
    row = cursor.fetchone()
    expected = ("UpdatedFirst", "UpdatedMiddle", "UpdatedLast", "Updated University", "updated_email@example.com", orig_password)
    if row == expected:
        log_info(" PASS: Updates persisted correctly; password unchanged")
    else:
        log_error(f" FAIL: Updates did not persist as expected: {row}")

    # 4. Attempt to update UUID (should be ignored / no effect)
    try:
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        cursor.execute(update_sql, {
            "user_id": user_id_str,
            "f_name": None,
            "m_name": None,
            "l_name": None,
            "institution": None,
            "email": None,
            "user_id": fake_uuid  # attempt to overwrite UUID
        })
        cnx.commit()
        cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email='updated_email@example.com'")
        uid_after = cursor.fetchone()[0]
        if uid_after == user_id_str:
            log_info(" PASS: UUID cannot be updated")
        else:
            log_error(" FAIL: UUID was changed")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Attempting to update UUID raised error: {e}")

    # 5. Attempt to update password (should not change via this script)
    try:
        cursor.execute(update_sql, {
            "user_id": user_id_str,
            "f_name": None,
            "m_name": None,
            "l_name": None,
            "institution": None,
            "email": None,
            "password": "new_password"  # attempt to overwrite password
        })
        cnx.commit()
        cursor.execute("SELECT password FROM Users WHERE user_id=UUID_TO_BIN(%s)", (user_id_str,))
        pw_after = cursor.fetchone()[0]
        if pw_after == orig_password:
            log_info(" PASS: Password cannot be updated via update_users.sql")
        else:
            log_error(" FAIL: Password changed unexpectedly")
    except mysql.connector.Error as e:
        log_error(f" FAIL: Attempting to update password raised error: {e}")


def update_users_password_test():
    """
    Test suite for updating user passwords using update_users_password.sql

    Tests:
        1. Update password for existing user
        2. Verify other fields are unchanged
        3. Attempt to update non-existent user
    """
    log_default("Running update_users_password_test()")


    # Helper: insert a test user
    def insert_test_user(email, password="original_pw"):
        with open(CREATE_SCRIPT, "r") as f:
            sql_script = f.read()
        cursor.execute(sql_script, {
            "f_name": "Password",
            "m_name": None,
            "l_name": "Tester",
            "institution": "Test University",
            "email": email,
            "password": password
        })
        cursor.execute("SELECT BIN_TO_UUID(user_id), f_name, l_name, institution, email FROM Users WHERE email=%s", (email,))
        return cursor.fetchone()  # returns (user_id, f_name, l_name, institution, email)

    # 1. Insert test user
    email_orig = "pw_test@example.com"
    user_id, f_name_orig, l_name_orig, institution_orig, email_orig = insert_test_user(email_orig)
    old_password = "original_pw"

    # 2. Update password
    new_password = "new_hashed_pw"
    with open(UPDATE_PW_SCRIPT, "r") as f:
        update_pw_sql = f.read()
    try:
        cursor.execute(update_pw_sql, {"user_id": user_id, "password": new_password})
        cnx.commit()
        log_info(" PASS: Password update executed without error")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" FAIL: Updating password raised error: {e}")

    # 3. Verify password updated and other fields unchanged
    cursor.execute(
        "SELECT password, f_name, l_name, institution, email FROM Users WHERE user_id=UUID_TO_BIN(%s)",
        (user_id,)
    )
    row = cursor.fetchone()
    pw, f_name, l_name, institution, email = row
    if pw == new_password and f_name == f_name_orig and l_name == l_name_orig and institution == institution_orig and email == email_orig:
        log_info(" PASS: Password updated correctly; other fields unchanged")
    else:
        log_error(f" FAIL: Password update check failed: {row}")

    # 4. Attempt to update a non-existent user
    from uuid import uuid4
    fake_user_id = str(uuid4())
    try:
        cursor.execute(update_pw_sql, {"user_id": fake_user_id, "password": "pw_fake"})
        cnx.commit()
        log_info(" PASS: Updating non-existent user did not crash")
    except mysql.connector.Error as e:
        cnx.rollback()
        log_error(f" FAIL: Updating non-existent user raised error: {e}")
if __name__ == "__main__":
    create_users_tests()
    delete_users_test()
    select_users_by_uuid_test()
    update_users_test()
    update_users_password_test()

