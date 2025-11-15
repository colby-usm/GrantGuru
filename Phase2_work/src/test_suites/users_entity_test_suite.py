"""
    File: users_entity_test_suite.py
    Author: Colby Wirth
    Version: 16 November 2025
    Description:
        Runs CRUD tests on Users entity against:
          1) Role.ADMIN
          2) Role.USER as OWNER (actor == target)
          3) Role.USER as NON-OWNER (actor != target)
    Generated with the assistance of AI Tools
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error as MySQLError, IntegrityError
from uuid import uuid4

from src.utils.logging_utils import log_info, log_error
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

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

# DB connection
try:
    log_info("Connecting to MySQL server...")
    cnx = mysql.connector.connect(
        host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME
    )
    cursor = cnx.cursor(buffered=True)
except mysql.connector.Error as err:
    log_error(f"MySQL connection error: {err}")
    sys.exit(2)


# Test statistics
test_stats = {"passed": 0, "failed": 0, "errors": 0}


# Utilities
def unique_email(prefix: str = "user") -> str:
    return f"{prefix}_{uuid4().hex[:10]}@example.test"


def insert_user(email: str | None = None, f_name: str = "Test", m_name=None, l_name: str = "User") -> str:
    """
    Insert a user using the SQL creation script. If email is None, generate a unique one.
    Commits immediately and returns BIN_TO_UUID(user_id).
    """
    sql_script_path = Path("src/db_crud/users/create_users.sql")
    sql_script = sql_script_path.read_text()

    if email is None:
        email = unique_email("user")

    params = {
        "f_name": f_name,
        "m_name": m_name,
        "l_name": l_name,
        "institution": "Test University",
        "email": email,
        "password": "pw",
    }

    try:
        cursor.execute(sql_script, params)
        cnx.commit()
    except IntegrityError as e:
        log_error(f"IntegrityError inserting user {email}: {e}; retrying with unique email.")
        params["email"] = unique_email("retry")
        try:
            cursor.execute(sql_script, params)
            cnx.commit()
        except Exception as e2:
            cnx.rollback()
            log_error(f"Failed to insert user after retry: {e2}")
            raise
    except Exception as e:
        cnx.rollback()
        log_error(f"Failed to insert user: {e}")
        raise

    cursor.execute("SELECT BIN_TO_UUID(user_id) FROM Users WHERE email=%s", (params["email"],))
    row = cursor.fetchone()
    if not row:
        raise RuntimeError("Inserted user not found after insert.")
    return row[0]


def assert_result(role: Role, expected_ok: bool, description: str, callable_fn):
    """
    Runs callable_fn() and interprets the result according to expected_ok.
    callable_fn must be a zero-arg callable which may raise PermissionError.
    Returns tuple of (success: bool, result_description: str).
    """
    try:
        result = callable_fn()

        # Determine result type description
        if result is None:
            result_desc = "None"
        elif isinstance(result, tuple):
            result_desc = f"tuple (len={len(result)})"
        elif isinstance(result, MySQLError):
            result_desc = f"MySQLError: {type(result).__name__}"
        elif isinstance(result, Exception):
            result_desc = f"Error: {type(result).__name__}"
        else:
            result_desc = f"{type(result).__name__}"

        # Check return value for operations that should return None on success
        if expected_ok and result not in (None, tuple):
            if isinstance(result, (MySQLError, Exception)):
                log_error(f"FAIL [{role.name}]: {description} - returned error: {result}")
                test_stats["failed"] += 1
                return False, result_desc

        if expected_ok:
            test_stats["passed"] += 1
            return True, result_desc
        else:
            log_error(f"FAIL [{role.name}]: {description} - expected PermissionError")
            test_stats["failed"] += 1
            return False, result_desc

    except PermissionError as e:
        result_desc = "PermissionError"
        if expected_ok:
            log_error(f"FAIL [{role.name}]: {description} - unexpected PermissionError")
            test_stats["failed"] += 1
            return False, result_desc
        else:
            test_stats["passed"] += 1
            return True, result_desc
    except MySQLError as e:
        result_desc = f"MySQLError: {type(e).__name__}"
        log_error(f"ERROR [{role.name}]: {description} - MySQL error: {e}")
        test_stats["errors"] += 1
        return False, result_desc
    except Exception as e:
        result_desc = f"Exception: {type(e).__name__}"
        log_error(f"ERROR [{role.name}]: {description} - {e}")
        test_stats["errors"] += 1
        return False, result_desc


# Test implementations
def test_read_user(role: Role, actor_id: str, target_id: str):
    """Test reading a user's fields."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def read_fn():
        return read_users_fields_by_uuid(role, actor_id, target_id, cursor)

    success, result_desc = assert_result(role, expected_ok, "Read user fields", read_fn)
    cnx.commit()
    return success, result_desc


def test_update_fields(role: Role, actor_id: str, target_id: str):
    """Test updating user fields."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def update_fn():
        return update_users_fields(
            role,
            actor_id,
            target_id,
            cursor,
            {
                "user_id": target_id,
                "f_name": f"Updated_{uuid4().hex[:6]}",
                "m_name": "Test",
                "l_name": "User",
                "institution": "Updated University",
                "email": unique_email("updated"),
            },
        )

    success, result_desc = assert_result(role, expected_ok, "Update user fields", update_fn)
    cnx.commit()
    return success, result_desc


def test_update_password(role: Role, actor_id: str, target_id: str):
    """Test updating user password."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def update_fn():
        return update_users_password(role, actor_id, target_id, cursor, f"new_pw_{uuid4().hex[:8]}")

    success, result_desc = assert_result(role, expected_ok, "Update password", update_fn)
    cnx.commit()
    return success, result_desc


def test_update_email(role: Role, actor_id: str, target_id: str):
    """Test updating user email."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def update_fn():
        return update_users_email(role, actor_id, target_id, cursor, unique_email("newemail"))

    success, result_desc = assert_result(role, expected_ok, "Update email", update_fn)
    cnx.commit()
    return success, result_desc


def test_delete_user(role: Role, actor_id: str, target_id: str):
    """Test deleting a user."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def delete_fn():
        return delete_a_users_entity(role, actor_id, target_id, cursor)

    success, result_desc = assert_result(role, expected_ok, "Delete user", delete_fn)
    cnx.commit()
    return success, result_desc


def test_add_research_field(role: Role, actor_id: str, target_id: str):
    """Test adding a research field."""
    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)
    field_name = f"Field_{uuid4().hex[:8]}"

    def add_fn():
        return add_a_reference_to_research_field(role, actor_id, target_id, cursor, field_name)

    success, result_desc = assert_result(role, expected_ok, f"Add research field", add_fn)
    cnx.commit()
    return success, result_desc


def test_delete_research_field(role: Role, actor_id: str, target_id: str):
    """Test deleting a research field."""
    field_name = f"Field_{uuid4().hex[:8]}"
    try:
        add_a_reference_to_research_field(Role.ADMIN, target_id, target_id, cursor, field_name)
        cnx.commit()
    except Exception as e:
        log_error(f"Pre-test: Failed to add research field: {e}")
        test_stats["errors"] += 1
        return False, f"Exception: {type(e).__name__}"

    expected_ok = (role == Role.ADMIN) or (actor_id == target_id)

    def delete_fn():
        return delete_a_reference_to_research_field(role, actor_id, target_id, cursor, field_name)

    success, result_desc = assert_result(role, expected_ok, f"Delete research field", delete_fn)
    cnx.commit()
    return success, result_desc


# Test runners
def run_test_as_admin(test_func, test_name: str):
    """Run a test as ADMIN (should always succeed)."""
    admin_user = insert_user(unique_email("admin"), f_name="Admin", l_name="User")
    target_user = insert_user(unique_email("target"), f_name="Target", l_name="User")
    success, result_desc = test_func(Role.ADMIN, admin_user, target_user)

    if success:
        log_info(f"{test_name}: Admin success - returned {result_desc}")

    return success


def run_test_as_owner(test_func, test_name: str):
    """Run a test as USER on their own resource (should succeed)."""
    owner_user = insert_user(unique_email("owner"), f_name="Owner", l_name="User")
    success, result_desc = test_func(Role.USER, owner_user, owner_user)

    if success:
        log_info(f"{test_name}: Owner success - returned {result_desc}")

    return success


def run_test_as_non_owner(test_func, test_name: str):
    """Run a test as USER on someone else's resource (should fail)."""
    actor_user = insert_user(unique_email("actor"), f_name="Actor", l_name="User")
    target_user = insert_user(unique_email("target"), f_name="Target", l_name="User")
    success, result_desc = test_func(Role.USER, actor_user, target_user)

    if success:
        log_info(f"{test_name}: Non-Owner success - returned {result_desc}")

    return success


def run_full_test(test_func, test_name: str):
    """Run a test in all three contexts: ADMIN, OWNER, NON-OWNER."""
    admin_ok = run_test_as_admin(test_func, test_name)
    owner_ok = run_test_as_owner(test_func, test_name)
    non_owner_ok = run_test_as_non_owner(test_func, test_name)

    return admin_ok and owner_ok and non_owner_ok


# MAIN
if __name__ == "__main__":
    log_info("Starting User Entity RBAC Test Suite")

    try:
        # Run all tests
        run_full_test(test_read_user, "READ USER")
        run_full_test(test_update_fields, "UPDATE FIELDS")
        run_full_test(test_update_password, "UPDATE PASSWORD")
        run_full_test(test_update_email, "UPDATE EMAIL")
        run_full_test(test_add_research_field, "ADD RESEARCH FIELD")
        run_full_test(test_delete_research_field, "DELETE RESEARCH FIELD")
        run_full_test(test_delete_user, "DELETE USER")

        # Print summary
        log_info(f"Passed: {test_stats['passed']}")
        if test_stats['failed'] > 0:
            log_error(f"Failed: {test_stats['failed']}")
        if test_stats['errors'] > 0:
            log_error(f"Errors: {test_stats['errors']}")

        total = sum(test_stats.values())
        log_info(f"Total: {total}")
 
        if test_stats['failed'] == 0 and test_stats['errors'] == 0:
            log_info("All tests passed")
 
    except Exception as e:
        log_error(f"Fatal error in test runner: {e}")
        import traceback
        traceback.print_exc()
        try:
            cnx.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            cursor.close()
            cnx.close()
        except Exception:
            pass
