'''
    File: users_operations.py
    Version: 9 November 2025
    Author: Colby Wirth
    Description:
        - Wraps SQL CRUD operations for User entity with their RessearchField with permissions checking
'''

import os
import sys
import uuid
from dotenv import load_dotenv
import mysql.connector as connector
from mysql.connector import errorcode, Error

from src.utils.logging_utils import log_info, log_error
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


@require_permission('read', Entity.USERS)

def read_users_fields_by_uuid(role: Role, user_id: str, resource_owner_id: str, cursor):
    """
    Fetch a user's fields from the database by their UUID.

    Uses a SQL script to select the user data and returns the first matching row.

    Args:
        role (Role): The role of the caller (used by the decorator for permissions).
        user_id (str): UUID of the user to fetch.
        resource_owner_id (str): UUID of the resource owner (used by decorator).
        cursor: MySQL cursor object for executing queries.

    Returns:
        dict or tuple: The user's data row if found, otherwise None.
    """

    _ = role, resource_owner_id # tell linter to ignore unused params that are needed for the decorator

    if (sql_script := read_sql_helper(SELECT_SCRIPT)) is None: return None

    try:
        cursor.execute(sql_script, (user_id,))
        return cursor.fetchone() # fetch the user's data
    except Error as e:
        log_error(f"Error executing SQL script {SELECT_SCRIPT}: {e}")
        return None


@require_permission('update', Entity.USERS)
def update_users_fields(role: Role, user_id: str, resource_owner_id: str, cursor, new_fields: dict) -> bool:
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
        bool: True if update succeeds, False otherwise.
    """
    _ = role, user_id, resource_owner_id  # for linter

    if (sql_script := read_sql_helper(UPDATE_SCRIPT)) is None:
        return False

    try:
        cursor.execute(sql_script, new_fields)
        return True
    except Exception as e:
        log_error(f"Error executing SQL script {UPDATE_SCRIPT}: {e}")
        return False


@require_permission('update', Entity.USERS)
def update_users_password(role: Role, user_id: str, resource_owner_id: str, cursor, new_password: str) -> bool:
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
        bool: True if update succeeds, False otherwise
    """
    _ = role, resource_owner_id  # for linter

    params = {"user_id": user_id, "password": new_password}

    if (sql_script := read_sql_helper(UPDATE_PW_SCRIPT)) is None:
        return False

    try:
        cursor.execute(sql_script, params)
        return True
    except Error as e:
        log_error(f"Error executing SQL script {UPDATE_PW_SCRIPT}: {e}")
        return False


@require_permission('update', Entity.USERS)
def update_users_email(role: Role, user_id: str, resource_owner_id: str, cursor, new_email: str) -> bool:
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
        bool: True if update succeeds, False otherwise
    """
    _ = role, resource_owner_id  # for linter

    if (sql_script := read_sql_helper(UPDATE_EMAIL_SCRIPT)) is None:
        return False

    try:
        params = {"user_id": user_id, "email": new_email}
        cursor.execute(sql_script, params)
        log_info(f"User {user_id} email updated successfully to {new_email}.")
        return True
    except Error as e:
        log_error(f"Error executing SQL script {UPDATE_EMAIL_SCRIPT}: {e}")
        return False


@require_permission('delete', Entity.USERS)
def delete_a_users_entity(role: Role, user_id: str, resource_owner_id: str, cursor) -> bool:
    """
    Delete a user entity from the database.

    Reads the delete SQL script and executes it for the given user ID.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user to delete
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object

    Returns:
        bool: True if deletion succeeds, False otherwise
    """
    _ = role, resource_owner_id  # for linter

    if (sql_script := read_sql_helper(DELETE_SCRIPT)) is None:
        return False

    try:
        cursor.execute(sql_script, (user_id,))
        return True
    except Error as e:
        log_error(f"Error executing SQL script {DELETE_SCRIPT}: {e}")
        return False


@require_permission('update', Entity.USERS)
def add_a_reference_to_research_field(
    role: Role, user_id: str, resource_owner_id: str, cursor, research_field: str
) -> bool:
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
        bool: True if association succeeds, False otherwise
    """
    _ = role, resource_owner_id  # for linter

    if (sql_script := read_sql_helper(CREATE_RESEARCH_FIELDS)) is None:
        return False

    try:
        # Execute each non-comment, non-empty statement
        for stmt in filter(None, (s.strip() for s in sql_script.split(";"))):
            if not stmt.startswith("--"):
                cursor.execute(stmt, {"user_id": user_id, "research_field": research_field})

        # Verify the research field exists
        if (select_sql := read_sql_helper(SELECT_RESEARCH_FIELDS)) is None:
            return False

        cursor.execute(select_sql, {"research_field": research_field})
        row = cursor.fetchone()
        if not row:
            log_error(f"No research field ID found for '{research_field}'")
            return False

        log_info(f"Associated research field '{research_field}' with user {user_id}")
        return True

    except Error as e:
        log_error(f"Error executing SQL script {CREATE_RESEARCH_FIELDS}: {e}")
        return False


@require_permission('delete', Entity.USERS)
def delete_a_reference_to_research_field(
    role: Role, user_id: str, resource_owner_id: str, cursor, research_field: str
) -> bool:
    """
    Delete a user's association with a research field using the field name.

    Args:
        role (Role): Role of the caller (used by decorator)
        user_id (str): UUID of the user
        resource_owner_id (str): UUID of the resource owner (used by decorator)
        cursor: MySQL cursor object
        research_field (str): Name of the research field to remove

    Returns:
        bool: True if deletion succeeds, False otherwise
    """
    _ = role, resource_owner_id  # for linter

    # Fetch research_field_id
    if (select_sql := read_sql_helper(SELECT_RESEARCH_FIELDS)) is None:
        return False

    try:
        cursor.execute(select_sql, {"research_field": research_field})
        row = cursor.fetchone()
        if not row:
            log_error(f"Research field '{research_field}' not found in DB")
            return False
        research_field_id = row[0]

        # Delete the user-research field association
        if (delete_sql := read_sql_helper(DELETE_A_USERS_RESEARCH_FIELDS)) is None:
            return False

        cursor.execute(delete_sql, {
            "user_id": uuid.UUID(user_id).bytes,
            "research_field_id": research_field_id
        })

        if cursor.rowcount == 0:
            log_info(f"No association found for user {user_id} and research field '{research_field}'")
        else:
            log_info(f"Deleted association for user {user_id} and research field '{research_field}'")

        return True

    except Error as e:
        log_error(f"MySQL Error during delete of research field '{research_field}': {e}")
        return False

if __name__ == "__main__":

    UID =  "D115AC4ABDCC11F0B701585DC8D7DDCD"

    load_dotenv()
    DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
    HOST = os.getenv("HOST", "localhost")
    MYSQL_USER = os.getenv("GG_USER", "root")
    MYSQL_PASS = os.getenv("GG_PASS", "")


    cnx  = None
    try:
        log_info("Connecting to MySQL server...")
        cnx = connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )

        cursor = cnx.cursor()

    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log_error(f"Access denied. Check MySQL user and password.  Error {err.errno}")
        else:
            log_error(f"MySQL Error: {err}")
        sys.exit(2)



    #print(read_users_fields_by_uuid(Role.USER, UID, UID, cursor))

    new_fields = {
        "user_id": UID,
        "f_name": "Alison",
        "m_name": "None",
        "l_name": "Johnson",
        "institution": "NorthEastern",
        "email": "Alisons_new_email@gmail.com"
    }
    #print(update_users_fields(Role.USER, UID, UID, cursor, new_fields))
    #cnx.commit()

    #print(update_users_password(Role.USER, UID, UID, cursor, "ira pass"))
    #cnx.commit()

    #print(read_users_fields_by_uuid(Role.USER, UID, UID, cursor))


    #print(delete_a_users_entity(Role.USER, UID, UID, cursor))
    #cnx.commit()
    #print(read_users_fields_by_uuid(Role.USER, UID, UID, cursor))


    #print(read_users_fields_by_uuid(Role.USER, UID, UID, cursor,))
    #print(update_users_email(Role.USER, UID, UID, cursor, "b@yahoo.com"))
    #cnx.commit()
    #print(read_users_fields_by_uuid(Role.USER, UID, UID, cursor,))
    
    #if delete_a_reference_to_research_field(Role.USER, UID, UID, cursor, "EE"):
    #    log_info("deletion executed successfully")
    #    cnx.commit()
