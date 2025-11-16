'''
    File: documents_operations.py
    Version: 15 November 2025
    Author: GitHub Copilot (based on users_operations.py template)
    Description:
        - Wraps SQL CRUD operations for Documents entity with permissions checking
        - Follows the same pattern as users_operations.py
'''

from mysql.connector import Error as MySQLError

from src.utils.logging_utils import log_error
from src.user_functions.view_based_operations import require_permission, Role, Entity
from src.utils.sql_file_parsers import read_sql_helper


CREATE_SCRIPT = "src/db_crud/documents/create_documents.sql"
DELETE_SCRIPT = "src/db_crud/documents/delete_documents.sql"
SELECT_SCRIPT = "src/db_crud/documents/select_documents_by_uuid.sql"
UPDATE_SCRIPT = "src/db_crud/documents/update_documents.sql"


class DocumentOperationError(Exception):
    """Custom exception for document operation failures."""
    pass


@require_permission('create', Entity.APPLICATION_DOCUMENTS)
def create_document(role: Role, user_id: str, resource_owner_id: str, cursor, 
                   document_name: str, document_type: str, document_size: int, 
                   upload_date, application_id: str) -> None | DocumentOperationError | MySQLError:
    """
    Create a new document in the database.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        document_name (str): Name of the document
        document_type (str): Type of the document
        document_size (int): Size of the document in bytes
        upload_date: Date and time when the document was uploaded
        application_id (str): Associated application ID

    Returns:
        None on success, DocumentOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    params = {
        "document_name": document_name,
        "document_type": document_type,
        "document_size": document_size,
        "upload_date": upload_date,
        "application_id": application_id
    }

    try:
        sql_script = read_sql_helper(CREATE_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {CREATE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {CREATE_SCRIPT}: {e}")
        return DocumentOperationError(e)


@require_permission('read', Entity.APPLICATION_DOCUMENTS)
def read_document_by_uuid(role: Role, user_id: str, resource_owner_id: str, cursor, 
                         document_id: str) -> tuple | DocumentOperationError | MySQLError:
    """
    Fetch a document's fields from the database by its UUID.

    Uses a SQL script to select the document data and returns the first matching row.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries
        document_id (str): UUID of the document to fetch

    Returns:
        tuple on success, DocumentOperationError on logical failure, MySQLError on DB failure
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(SELECT_SCRIPT)
        cursor.execute(sql_script, (document_id,))
        return cursor.fetchone()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_SCRIPT}: {e}")
        return DocumentOperationError(e)


@require_permission('update', Entity.APPLICATION_DOCUMENTS)
def update_document(role: Role, user_id: str, resource_owner_id: str, cursor, 
                   document_id: str, **fields) -> None | DocumentOperationError | MySQLError:
    """
    Update a document's fields in the database.

    Reads a SQL update script and executes it with the provided field values.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries
        document_id (str): UUID of the document to update
        **fields: Keyword arguments for fields to update (document_name, document_type, 
                 document_size, upload_date, application_id)

    Returns:
        None on success, DocumentOperationError on failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    # Ensure all expected fields are present (with None as default)
    params = {
        "document_id": document_id,
        "document_name": fields.get("document_name"),
        "document_type": fields.get("document_type"),
        "document_size": fields.get("document_size"),
        "upload_date": fields.get("upload_date"),
        "application_id": fields.get("application_id")
    }

    try:
        sql_script = read_sql_helper(UPDATE_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {UPDATE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {UPDATE_SCRIPT}: {e}")
        return DocumentOperationError(e)


@require_permission('delete', Entity.APPLICATION_DOCUMENTS)
def delete_document(role: Role, user_id: str, resource_owner_id: str, cursor, 
                   document_id: str) -> None | DocumentOperationError | MySQLError:
    """
    Delete a document from the database.

    Reads the delete SQL script and executes it for the given document ID.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        document_id (str): UUID of the document to delete

    Returns:
        None on success, DocumentOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    try:
        sql_script = read_sql_helper(DELETE_SCRIPT)
        cursor.execute(sql_script, (document_id,))
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_SCRIPT}: {e}")
        return DocumentOperationError(e)
