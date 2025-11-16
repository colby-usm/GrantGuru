"""
documents_rbp_test_suite.py
Author: GitHub Copilot (based on users_rbp_test_suite.py template)
Version: 15 November 2025
Description:
    Tests for high-level document operations via documents_operations.py
    Includes CRUD operations with permissions enforcement via decorators
    Generated with the assistance of AI Tools
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector as connector
from mysql.connector import errorcode, Error as MySQLError


from src.utils.logging_utils import log_info, log_error, log_default
from src.document_functions.documents_operations import (
    create_document,
    read_document_by_uuid,
    update_document,
    delete_document,
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
    cursor.execute("DELETE FROM Users WHERE email='fixture_user@example.com'")
    cursor.execute("DELETE FROM Grants WHERE grant_title='Fixture Grant'")
    
    uid = insert_test_user(cursor, email="fixture_user@example.com")
    gid = insert_test_grant(cursor, grant_name="Fixture Grant")
    aid = insert_test_application(cursor, uid, gid)
    return uid, gid, aid


def test_create_document(cursor, uid, aid):
    log_default("Running test_create_document()")
    
    upload_date = datetime.now()
    result = create_document(
        Role.USER, uid, uid, cursor,
        document_name="test_document.pdf",
        document_type="PDF",
        document_size=1024,
        upload_date=upload_date,
        application_id=aid
    )
    
    if result is None:
        cursor.execute(
            "SELECT document_name, document_type FROM Documents WHERE application_id=UUID_TO_BIN(%s) AND document_name='test_document.pdf'",
            (aid,)
        )
        row = cursor.fetchone()
        if row and row[0] == "test_document.pdf" and row[1] == "PDF":
            log_info(" PASS: create_document successfully created document")
        else:
            log_error(f" FAIL: Document not found or incorrect: {row}")
    else:
        log_error(f" FAIL: create_document returned error: {result}")


def test_read_document_by_uuid(cursor, uid, aid):
    log_default("Running test_read_document_by_uuid()")
    
    upload_date = datetime.now()
    create_document(
        Role.USER, uid, uid, cursor,
        document_name="read_test_doc.pdf",
        document_type="PDF",
        document_size=2048,
        upload_date=upload_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(document_id) FROM Documents WHERE application_id=UUID_TO_BIN(%s) AND document_name='read_test_doc.pdf'",
        (aid,)
    )
    doc_id = cursor.fetchone()[0]
    
    result = read_document_by_uuid(Role.USER, uid, uid, cursor, doc_id)
    
    if isinstance(result, tuple) and result[1] == "read_test_doc.pdf":
        log_info(" PASS: read_document_by_uuid returned correct row")
    else:
        log_error(f" FAIL: Unexpected return: {result}")


def test_update_document(cursor, uid, aid):
    log_default("Running test_update_document()")
    
    upload_date = datetime.now()
    create_document(
        Role.USER, uid, uid, cursor,
        document_name="original_doc.pdf",
        document_type="PDF",
        document_size=3072,
        upload_date=upload_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(document_id) FROM Documents WHERE application_id=UUID_TO_BIN(%s) AND document_name='original_doc.pdf'",
        (aid,)
    )
    doc_id = cursor.fetchone()[0]
    
    new_fields = {
        "document_name": "updated_doc.pdf",
        "document_type": "DOCX",
        "document_size": 4096
    }
    
    result = update_document(Role.USER, uid, uid, cursor, doc_id, **new_fields)
    
    if result is None:
        cursor.execute(
            "SELECT document_name, document_type, document_size FROM Documents WHERE document_id=UUID_TO_BIN(%s)",
            (doc_id,)
        )
        row = cursor.fetchone()
        expected = ("updated_doc.pdf", "DOCX", 4096)
        if row == expected:
            log_info(" PASS: update_document persisted changes")
        else:
            log_error(f" FAIL: DB row mismatch. Expected {expected}, got {row}")
    else:
        log_error(f" FAIL: update_document returned error: {result}")


def test_delete_document(cursor, uid, aid):
    log_default("Running test_delete_document()")
    
    upload_date = datetime.now()
    create_document(
        Role.USER, uid, uid, cursor,
        document_name="delete_me.pdf",
        document_type="PDF",
        document_size=1024,
        upload_date=upload_date,
        application_id=aid
    )
    
    cursor.execute(
        "SELECT BIN_TO_UUID(document_id) FROM Documents WHERE application_id=UUID_TO_BIN(%s) AND document_name='delete_me.pdf'",
        (aid,)
    )
    doc_id = cursor.fetchone()[0]
    
    result = delete_document(Role.USER, uid, uid, cursor, doc_id)
    
    if result is None:
        cursor.execute(
            "SELECT COUNT(*) FROM Documents WHERE document_id=UUID_TO_BIN(%s)",
            (doc_id,)
        )
        if cursor.fetchone()[0] == 0:
            log_info(" PASS: delete_document removed document")
        else:
            log_error(" FAIL: document still exists in DB")
    else:
        log_error(f" FAIL: delete_document returned error: {result}")


if __name__ == "__main__":
    cnx, cursor = setup_db()

    # Create shared test fixtures
    uid, gid, aid = create_test_fixtures(cursor)
    cnx.commit()

    # Run all document function tests
    test_create_document(cursor, uid, aid)
    cnx.commit()
    
    test_read_document_by_uuid(cursor, uid, aid)
    cnx.commit()
    
    test_update_document(cursor, uid, aid)
    cnx.commit()
    
    test_delete_document(cursor, uid, aid)
    cnx.commit()

    cursor.close()
    cnx.close()
