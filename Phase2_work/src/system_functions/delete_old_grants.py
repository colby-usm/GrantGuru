"""
    File: delete_old_grants.py
    Version: 15 November 2025
    Author: James Tedder
    Description:

"""
import uuid
from mysql.connector import Error as MySQLError
import os
from dotenv import load_dotenv
import sys
import mysql.connector
from mysql.connector import errorcode
from src.utils.logging_utils import log_info, log_error
from src.utils.sql_file_parsers import read_sql_helper
from typing import List, Tuple, Any

class DeletionOperationError(Exception):
    """Custom exception for deletion operation failures."""
    pass

def main ():
    load_dotenv()
    DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
    HOST = os.getenv("HOST", "localhost")
    MYSQL_USER = os.getenv("GG_USER", "root")
    MYSQL_PASS = os.getenv("GG_PASS", "")

    DELETE_GRANT_SCRIPT = "src/db_crud/grants/delete_grants.sql"
    SELECT_OLD_GRANT_SCRIPT = "src/db_crud/grants/select_grants_archived_no_appplications.sql"

    log_info("Connecting to MySQL server...")
    cnx = mysql.connector.connect(
        host=HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS
    )

    cursor = cnx.cursor()
    try:
        sql_select = read_sql_helper(SELECT_OLD_GRANT_SCRIPT)
        if sql_select is None:
            error_msg = f"SQL script file not found: {SELECT_OLD_GRANT_SCRIPT}"
            log_error(error_msg)
            return DeletionOperationError(error_msg)
        cursor.execute(sql_select)
        to_delete_ids = cursor.fetchall()
    except MySQLError as e:
        log_error(f"MySQL error executing {SELECT_OLD_GRANT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {SELECT_OLD_GRANT_SCRIPT}: {e}")
        return DeletionOperationError(e)

    try:
        sql_delete = read_sql_helper(DELETE_GRANT_SCRIPT) 
        if sql_delete is None:
            error_msg = f"SQL script file not found: {DELETE_GRANT_SCRIPT}"
            log_error(error_msg)
            return DeletionOperationError(error_msg)
        ids_to_delete = [record[0] for record in to_delete_ids] #type: ignore

        

        successful_deletions = 0

        for grant_id in ids_to_delete:
            cursor.execute(sql_delete, (grant_id,)) 
            successful_deletions += cursor.rowcount

        cnx.commit()
        log_info(f"Successfully deleted {successful_deletions} grants.")
    except MySQLError as e:
        log_error(f"MySQL error executing {DELETE_GRANT_SCRIPT}: {e}")
        return e
    except Exception as e:
        log_error(f"Unexpected error executing {DELETE_GRANT_SCRIPT}: {e}")
        return DeletionOperationError(e)