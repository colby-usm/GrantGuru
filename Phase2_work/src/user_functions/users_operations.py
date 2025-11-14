'''
    File: users_operations.py
    Version: 13 November 2025
    Author: Colby Wirth
    Description:
        - Wraps SQL CRUD operations for User entity with their ResearchField with permissions checking
'''

import uuid
from mysql.connector import Error as MySQLError

from src.utils.logging_utils import log_info, log_error, log_warning
from src.user_functions.view_based_operations import require_permission, Role, Entity
from src.utils.sql_file_parsers import read_sql_helper

# TODO A users entity is created outside of the RBP schema - this will be handeled in Phase 3
# TODO we need to handle when a value such as m_name is set up None: we have a bug where overiding a value with None does not persist

CREATE_SCRIPT = "src/db_crud/users/create_users.sql"
DELETE_SCRIPT = "src/db_crud/users/delete_users.sql"
SELECT_SCRIPT = "src/db_crud/users/select_users_by_uuid.sql"
UPDATE_SCRIPT = "src/db_crud/users/update_users_fields.sql"
UPDATE_PW_SCRIPT = "src/db_crud/users/update_users_password.sql"
UPDATE_EMAIL_SCRIPT = "src/db_crud/users/update_users_email.sql"
CREATE_RESEARCH_FIELDS = "src/db_crud/research_fields/create_research_fields.sql"
SELECT_RESEARCH_FIELDS = "src/db_crud/research_fields/select_a_research_field_by_name.sql"
DELETE_A_USERS_RESEARCH_FIELDS = "src/db_crud/research_fields/delete_a_users_research_fields.sql"


class UserOperationError(Exception):
    """Custom exception for user operation failures."""
    pass


@require_permission('read', Entity.USERS)
def read_users_fields_by_uuid(role: Role, user_id: str, resource_owner_id: str, cursor) -> dict | UserOperationError | MySQLError:
    """
    Fetch a user's fields from the database by their UUID.

    Uses a SQL script to select the user data and returns the first matching row.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions).
        user_id (str): UUID of the user to fetch.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.

    Returns:
        dict on success, UserOperationError on logical failure, MySQLError on DB failure
    """

    _ = role, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(SELECT_SCRIPT)
        cursor.execute(sql_script, (user_id,))
        return cursor.fetchone()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_SCRIPT}: {e}")
        return UserOperationError(e)


@require_permission('update', Entity.USERS)
def update_users_fields(role: Role, user_id: str, resource_owner_id: str, cursor, new_fields: dict) -> None | UserOperationError | MySQLError:
    """
    Update a user's fields in the database.

    Reads a SQL update script and executes it with the provided field values.

    Args:
        role (Role): Role of the caller (used by decorator for permissions).
        user_id (str): UUID of the user to update.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.
        new_fields (dict): Mapping of field names to their new values.

    Returns:
        None on success, UserOperationError on failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    try:
        sql_script = read_sql_helper(UPDATE_SCRIPT)
        cursor.execute(sql_script, new_fields)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {UPDATE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {UPDATE_SCRIPT}: {e}")
        return UserOperationError(e)


@require_permission('update', Entity.USERS)
def update_users_password(role: Role, user_id: str, resource_owner_id: str, cursor, new_password: str) -> None | UserOperationError | MySQLError:
    """
    Update a user's password in the database.

    Reads the password update SQL script and executes it with the new password.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user to update
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        new_password (str): New hashed password

    Returns:
        None on success, UserOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # for linter

    params = {"user_id": user_id, "password": new_password}

    try:
        sql_script = read_sql_helper(UPDATE_PW_SCRIPT)
        cursor.execute(sql_script, params)
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {UPDATE_PW_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {UPDATE_PW_SCRIPT}: {e}")
        return UserOperationError(e)


@require_permission('update', Entity.USERS)
def update_users_email(role: Role, user_id: str, resource_owner_id: str, cursor, new_email: str) -> None | UserOperationError | MySQLError:
    """
    Update a user's email address in the database.

    Reads the email update SQL script and executes it with the new email.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user to update
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        new_email (str): New email address

    Returns:
        None on success, UserOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # for linter

    params = {"user_id": user_id, "email": new_email}
    try:
        sql_script = read_sql_helper(UPDATE_EMAIL_SCRIPT)
        cursor.execute(sql_script, params)
        log_info(f"User {user_id} email updated successfully to {new_email}.")
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {UPDATE_EMAIL_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {UPDATE_EMAIL_SCRIPT}: {e}")
        return UserOperationError(e)


@require_permission('delete', Entity.USERS)
def delete_a_users_entity(role: Role, user_id: str, resource_owner_id: str, cursor) -> None | UserOperationError | MySQLError:
    """
    Delete a user entity from the database.

    Reads the delete SQL script and executes it for the given user ID.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user to delete
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object

    Returns:
        None on success, UserOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # for linter

    try:
        sql_script = read_sql_helper(DELETE_SCRIPT)
        cursor.execute(sql_script, (user_id,))
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_SCRIPT}: {e}")
        return UserOperationError(e)


@require_permission('update', Entity.USERS)
def add_a_reference_to_research_field(role: Role, user_id: str, resource_owner_id: str, cursor, research_field: str) -> None | UserOperationError | MySQLError:
    """
    Add a research field and associate it with a user.

    Reads the creation SQL script and executes all statements, then ensures the research field exists.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        research_field (str): Name of the research field to add

    Returns:
        None on success, UserOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # for linter

    try:
        sql_script: str | None = read_sql_helper(CREATE_RESEARCH_FIELDS)
        if not sql_script:
            raise UserOperationError(f"Failed to read SQL script {CREATE_RESEARCH_FIELDS}")

        for stmt in filter(None, (s.strip() for s in sql_script.split(";"))):
            if not stmt.startswith("--"):
                cursor.execute(stmt, {"user_id": user_id, "research_field": research_field})

        select_sql: str | None = read_sql_helper(SELECT_RESEARCH_FIELDS)
        if not select_sql:
            raise UserOperationError(f"Failed to read SQL script {SELECT_RESEARCH_FIELDS}")

        cursor.execute(select_sql, {"research_field": research_field})
        row = cursor.fetchone()
        if not row:
            raise UserOperationError(f"No research field ID found for '{research_field}'")

        log_info(f"Associated research field '{research_field}' with user {user_id}")
        return None

    except MySQLError as e:
        log_error(f"MySQL error adding research field '{research_field}' for user {user_id}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error adding research field '{research_field}' for user {user_id}: {e}")
        return UserOperationError(e)


@require_permission('delete', Entity.USERS)
def delete_a_reference_to_research_field(role: Role, user_id: str, resource_owner_id: str, cursor, research_field: str) -> None | UserOperationError | MySQLError:
    """
    Delete a user's association with a research field using the field name.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        research_field (str): Name of the research field to remove

    Returns:
        None on success, UserOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, resource_owner_id  # for linter

    try:
        select_sql = read_sql_helper(SELECT_RESEARCH_FIELDS)
        cursor.execute(select_sql, {"research_field": research_field})
        row = cursor.fetchone()
        if not row:
            raise UserOperationError(f"Research field '{research_field}' not found in DB")

        research_field_id = row[0]
        delete_sql = read_sql_helper(DELETE_A_USERS_RESEARCH_FIELDS)

        cursor.execute(delete_sql, {
            "user_id": uuid.UUID(user_id).bytes,
            "research_field_id": research_field_id
        })

        if cursor.rowcount == 0:
            log_warning(f"No association found for user {user_id} and research field '{research_field}'")
        else:
            log_info(f"Deleted association for user {user_id} and research field '{research_field}'")

        return None

    except MySQLError as e:
        log_error(f"MySQL error during delete of research field '{research_field}' for user {user_id}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error during delete of research field '{research_field}' for user {user_id}: {e}")
        return UserOperationError(e)
