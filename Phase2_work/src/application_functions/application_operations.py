'''
    File: application_operations.py
    Version: 15 November 2025
    Author: Generated based on Abdullahi Abdullahi's SQL scripts
    Description:
        - Wraps SQL CRUD operations for Application entity with permissions checking
        - Enforces RBAC using the view_based_operations module
'''

from mysql.connector import Error as MySQLError

from src.utils.logging_utils import log_info, log_error
from src.user_functions.view_based_operations import require_permission, Role, Entity
from src.utils.sql_file_parsers import read_sql_helper

# SQL Script Paths
CREATE_SCRIPT = "src/db_crud/applications/create_application.sql"
DELETE_BY_APP_ID_SCRIPT = "src/db_crud/applications/delete_application_by_id.sql"
DELETE_BY_USER_GRANT_SCRIPT = "src/db_crud/applications/delete_application_by_grant_and_user.sql"
DELETE_BY_USER_SCRIPT = "src/db_crud/applications/delete_application_by_user.sql"
DELETE_BY_GRANT_SCRIPT = "src/db_crud/applications/delete_application_by_grant.sql"
DELETE_ALL_SCRIPT = "src/db_crud/applications/delete_application.sql"
SELECT_BY_APP_ID_SCRIPT = "src/db_crud/applications/select_application_by_id.sql"
SELECT_BY_USER_SCRIPT = "src/db_crud/applications/select_application_by_user.sql"
SELECT_BY_GRANT_SCRIPT = "src/db_crud/applications/select_application_by_grant.sql"
SELECT_BY_STATUS_SCRIPT = "src/db_crud/applications/select_application_by_status.sql"
UPDATE_STATUS_SCRIPT = "src/db_crud/applications/update_application_status.sql"


class ApplicationOperationError(Exception):
    """Custom exception for application operation failures."""
    pass


@require_permission('create', Entity.APPLICATION)
def create_application(role: Role, user_id: str, resource_owner_id: str, cursor, 
                      grant_id: str, status: str, application_date: str) -> None | ApplicationOperationError | MySQLError:
    """
    Create a new application for a grant.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user creating the application.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        grant_id (str): UUID of the grant being applied to.
        status (str): Initial status of the application (default: 'pending').
        application_date (str): Date of application submission (YYYY-MM-DD format).

    Returns:
        None on success, ApplicationOperationError on logical failure, 
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # linter ignore

    params = {
        "user_id": user_id,
        "grant_id": grant_id,
        "status": status,
        "application_date": application_date
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
        return ApplicationOperationError(e)


@require_permission('read', Entity.APPLICATION)
def read_application_by_id(role: Role, user_id: str, resource_owner_id: str, cursor, 
                          application_id: str) -> tuple | ApplicationOperationError | MySQLError:
    """
    Fetch an application by its unique ID.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        application_id (str): UUID of the application to retrieve.

    Returns:
        tuple on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role  # linter ignore

    params = {"application_id": application_id}

    try:
        sql_script = read_sql_helper(SELECT_BY_APP_ID_SCRIPT)
        cursor.execute(sql_script, params)
        return cursor.fetchone()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_APP_ID_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_APP_ID_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('read', Entity.APPLICATION)
def read_applications_by_user(role: Role, user_id: str, resource_owner_id: str, cursor) -> list | ApplicationOperationError | MySQLError:
    """
    Fetch all applications submitted by a specific user.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user whose applications to retrieve.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.

    Returns:
        list of tuples on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role  # linter ignore

    params = {"user_id": user_id}

    try:
        sql_script = read_sql_helper(SELECT_BY_USER_SCRIPT)
        cursor.execute(sql_script, params)
        return cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_USER_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_USER_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('read', Entity.APPLICATION)
def read_applications_by_grant(role: Role, user_id: str, resource_owner_id: str, cursor, 
                               grant_id: str) -> list | ApplicationOperationError | MySQLError:
    """
    Fetch all applications for a specific grant.
    
    Note: Admins can see all applications for a grant. Regular users can only see their own.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        grant_id (str): UUID of the grant whose applications to retrieve.

    Returns:
        list of tuples on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    params = {"grant_id": grant_id}

    try:
        sql_script = read_sql_helper(SELECT_BY_GRANT_SCRIPT)
        cursor.execute(sql_script, params)
        return cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_GRANT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_GRANT_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('read', Entity.APPLICATION)
def read_applications_by_status(role: Role, user_id: str, resource_owner_id: str, cursor, 
                                status: str) -> list | ApplicationOperationError | MySQLError:
    """
    Fetch all applications with a specific status.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        status (str): Status filter (e.g., 'pending', 'approved', 'rejected').

    Returns:
        list of tuples on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    params = {"status": status}

    try:
        sql_script = read_sql_helper(SELECT_BY_STATUS_SCRIPT)
        cursor.execute(sql_script, params)
        return cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_STATUS_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_STATUS_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('update', Entity.APPLICATION)
def update_application_status(role: Role, user_id: str, resource_owner_id: str, cursor, 
                              application_id: str, new_status: str) -> None | ApplicationOperationError | MySQLError:
    """
    Update the status of an application.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        application_id (str): UUID of the application to update.
        new_status (str): New status value.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    params = {
        "application_id": application_id,
        "status": new_status
    }

    try:
        sql_script = read_sql_helper(UPDATE_STATUS_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {UPDATE_STATUS_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {UPDATE_STATUS_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('delete', Entity.APPLICATION)
def delete_application_by_id(role: Role, user_id: str, resource_owner_id: str, cursor, 
                            application_id: str) -> None | ApplicationOperationError | MySQLError:
    """
    Delete an application by its unique ID.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        application_id (str): UUID of the application to delete.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # linter ignore

    params = {"application_id": application_id}

    try:
        sql_script = read_sql_helper(DELETE_BY_APP_ID_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_BY_APP_ID_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_BY_APP_ID_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('delete', Entity.APPLICATION)
def delete_application_by_user_and_grant(role: Role, user_id: str, resource_owner_id: str, cursor, 
                                        grant_id: str) -> None | ApplicationOperationError | MySQLError:
    """
    Delete an application based on user_id and grant_id.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user who owns the application.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        grant_id (str): UUID of the grant.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # linter ignore

    params = {
        "user_id": user_id,
        "grant_id": grant_id
    }

    try:
        sql_script = read_sql_helper(DELETE_BY_USER_GRANT_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_BY_USER_GRANT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_BY_USER_GRANT_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('delete', Entity.APPLICATION)
def delete_applications_by_user(role: Role, user_id: str, resource_owner_id: str, cursor) -> None | ApplicationOperationError | MySQLError:
    """
    Delete all applications for a specific user.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user whose applications to delete.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # linter ignore

    params = {"user_id": user_id}

    try:
        sql_script = read_sql_helper(DELETE_BY_USER_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_BY_USER_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_BY_USER_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('delete', Entity.APPLICATION)
def delete_applications_by_grant(role: Role, user_id: str, resource_owner_id: str, cursor, 
                                grant_id: str) -> None | ApplicationOperationError | MySQLError:
    """
    Delete all applications for a specific grant.
    
    Note: This is typically an admin-only operation.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        grant_id (str): UUID of the grant whose applications to delete.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    params = {"grant_id": grant_id}

    try:
        sql_script = read_sql_helper(DELETE_BY_GRANT_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_BY_GRANT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_BY_GRANT_SCRIPT}: {e}")
        return ApplicationOperationError(e)


@require_permission('delete', Entity.APPLICATION)
def delete_all_applications(role: Role, user_id: str, resource_owner_id: str, cursor) -> None | ApplicationOperationError | MySQLError:
    """
    Delete all applications in the table.
    
    WARNING: This is a destructive operation and should only be used by admins
    for database maintenance or testing purposes.

    Args:
        role (Role): The role of the caller (used by decorator).
        user_id (str): UUID of the user making the request.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.

    Returns:
        None on success, ApplicationOperationError on logical failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(DELETE_ALL_SCRIPT)
        cursor.execute(sql_script)
        log_info("WARNING: All applications have been deleted from the database")
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_ALL_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_ALL_SCRIPT}: {e}")
        return ApplicationOperationError(e)