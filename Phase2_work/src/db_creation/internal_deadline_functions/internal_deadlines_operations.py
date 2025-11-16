'''
    File: internal_deadlines_operations.py
    Version: 15 November 2025
    Author: GitHub Copilot (based on users_operations.py template)
    Description:
        - Wraps SQL CRUD operations for InternalDeadlines entity with permissions checking
        - Follows the same pattern as users_operations.py
'''

from mysql.connector import Error as MySQLError

from src.utils.logging_utils import log_error
from src.user_functions.view_based_operations import require_permission, Role, Entity
from src.utils.sql_file_parsers import read_sql_helper


CREATE_SCRIPT = "src/db_crud/internal_deadlines/create_internal_deadlines.sql"
DELETE_SCRIPT = "src/db_crud/internal_deadlines/delete_internal_deadlines.sql"
SELECT_SCRIPT = "src/db_crud/internal_deadlines/select_internal_deadlines_by_uuid.sql"
UPDATE_SCRIPT = "src/db_crud/internal_deadlines/update_internal_deadlines.sql"
SELECT_BY_EARLIEST_SCRIPT = "src/db_crud/internal_deadlines/select_internal_deadlines_by_earliest.sql"
SELECT_BY_NEXT_SCRIPT = "src/db_crud/internal_deadlines/select_internal_deadlines_by_next.sql"


class InternalDeadlineOperationError(Exception):
    """Custom exception for internal deadline operation failures."""
    pass


@require_permission('create', Entity.APPLICATION_DEADLINES)
def create_internal_deadline(role: Role, user_id: str, resource_owner_id: str, cursor,
                            deadline_name: str, deadline_date, 
                            application_id: str) -> None | InternalDeadlineOperationError | MySQLError:
    """
    Create a new internal deadline in the database.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        deadline_name (str): Name of the deadline
        deadline_date: Date and time of the deadline
        application_id (str): Associated application ID

    Returns:
        None on success, InternalDeadlineOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    params = {
        "deadline_name": deadline_name,
        "deadline_date": deadline_date,
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
        return InternalDeadlineOperationError(e)


@require_permission('read', Entity.APPLICATION_DEADLINES)
def read_internal_deadline_by_uuid(role: Role, user_id: str, resource_owner_id: str, cursor,
                                  internal_deadline_id: str) -> tuple | InternalDeadlineOperationError | MySQLError:
    """
    Fetch an internal deadline's fields from the database by its UUID.

    Uses a SQL script to select the deadline data and returns the first matching row.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries
        internal_deadline_id (str): UUID of the internal deadline to fetch

    Returns:
        tuple on success, InternalDeadlineOperationError on logical failure, MySQLError on DB failure
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(SELECT_SCRIPT)
        cursor.execute(sql_script, (internal_deadline_id,))
        return cursor.fetchone()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_SCRIPT}: {e}")
        return InternalDeadlineOperationError(e)


@require_permission('read', Entity.APPLICATION_DEADLINES)
def read_internal_deadlines_by_earliest(role: Role, user_id: str, resource_owner_id: str, 
                                       cursor) -> list | InternalDeadlineOperationError | MySQLError:
    """
    Fetch internal deadlines ordered by earliest date.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries

    Returns:
        list of tuples on success, InternalDeadlineOperationError on logical failure, 
        MySQLError on DB failure
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(SELECT_BY_EARLIEST_SCRIPT)
        cursor.execute(sql_script)
        return cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_EARLIEST_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_EARLIEST_SCRIPT}: {e}")
        return InternalDeadlineOperationError(e)


@require_permission('read', Entity.APPLICATION_DEADLINES)
def read_internal_deadlines_by_next(role: Role, user_id: str, resource_owner_id: str,
                                   cursor) -> list | InternalDeadlineOperationError | MySQLError:
    """
    Fetch next upcoming internal deadlines.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries

    Returns:
        list of tuples on success, InternalDeadlineOperationError on logical failure,
        MySQLError on DB failure
    """
    _ = role, user_id, resource_owner_id  # linter ignore

    try:
        sql_script = read_sql_helper(SELECT_BY_NEXT_SCRIPT)
        cursor.execute(sql_script)
        return cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_BY_NEXT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_BY_NEXT_SCRIPT}: {e}")
        return InternalDeadlineOperationError(e)


@require_permission('update', Entity.APPLICATION_DEADLINES)
def update_internal_deadline(role: Role, user_id: str, resource_owner_id: str, cursor,
                            internal_deadline_id: str, **fields) -> None | InternalDeadlineOperationError | MySQLError:
    """
    Update an internal deadline's fields in the database.

    Reads a SQL update script and executes it with the provided field values.

    Args:
        role (Role): Role of the caller (used by decorator for permissions)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object for executing queries
        internal_deadline_id (str): UUID of the internal deadline to update
        **fields: Keyword arguments for fields to update (deadline_name, deadline_date, application_id)

    Returns:
        None on success, InternalDeadlineOperationError on failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    # Ensure all expected fields are present (with None as default)
    params = {
        "internal_deadline_id": internal_deadline_id,
        "deadline_name": fields.get("deadline_name"),
        "deadline_date": fields.get("deadline_date"),
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
        return InternalDeadlineOperationError(e)


@require_permission('delete', Entity.APPLICATION_DEADLINES)
def delete_internal_deadline(role: Role, user_id: str, resource_owner_id: str, cursor,
                            internal_deadline_id: str) -> None | InternalDeadlineOperationError | MySQLError:
    """
    Delete an internal deadline from the database.

    Reads the delete SQL script and executes it for the given deadline ID.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user making the request
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        internal_deadline_id (str): UUID of the internal deadline to delete

    Returns:
        None on success, InternalDeadlineOperationError on logical/user failure,
        MySQLError on database failure.
    """
    _ = role, user_id, resource_owner_id  # for linter

    try:
        sql_script = read_sql_helper(DELETE_SCRIPT)
        cursor.execute(sql_script, (internal_deadline_id,))
        return None
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_SCRIPT}: {e}")
        return InternalDeadlineOperationError(e)
