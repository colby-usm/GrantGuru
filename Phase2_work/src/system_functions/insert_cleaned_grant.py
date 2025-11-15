"""
    File: insert_cleaned_grant.py
    Version: 15 November 2025
    Author: James Tedder

    Made with the help of Gemini

    Description:

"""

import json
from typing import Dict, Any

import os
import sys
import json
from typing import Dict, Any, Union
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import Error as MySQLError

from src.utils.logging_utils import log_info, log_error
from src.utils.sql_file_parsers import read_sql_helper

def format_grant_data_for_insert(raw_data: Dict[str, Any]) -> Dict[str, Any]:

    params = raw_data.copy()

    dates = params.pop('dates', {})

    params['date_posted'] = dates.get('posting_date')
    params['archive_date'] = dates.get('archive_date')
    
    params['date_closed'] = dates.get('response_date')
    params['last_update_date'] = dates.get('last_updated_date')
    
    poc_dict = params.pop('point_of_contact', {})
    
    params['point_of_contact'] = json.dumps(poc_dict)

    params.pop('grant_id', None)
    params.pop('opportunity_number', None) 

    return params

class GrantOperationError(Exception):
    """Custom exception for deletion operation failures."""
    pass

def main (cleaned_grants: list): 
    load_dotenv()
    DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
    HOST = os.getenv("HOST", "localhost")
    MYSQL_USER = os.getenv("GG_USER", "root")
    MYSQL_PASS = os.getenv("GG_PASS", "")

    INSERT_GRANT_SCRIPT = "src/db_crud/create_grants.sql"

    cnx = None
    cursor = None
    successful_insertions = 0

    log_info("Connecting to MySQL server for insertion...")

    try:
        # --- 1. CONNECT TO DATABASE (with DB name specified) ---
        cnx = mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME # Explicitly select the database
        )
        cursor = cnx.cursor()
        
        # --- 2. LOAD SQL Script ---
        log_info(f"Loading insertion script from {INSERT_GRANT_SCRIPT}...")
        sql_insert = read_sql_helper(INSERT_GRANT_SCRIPT)
        
        if sql_insert is None:
            raise GrantOperationError(f"SQL script file not found: {INSERT_GRANT_SCRIPT}")
            
        # --- 3. EXECUTE INSERTION ---
        log_info("Executing grant insertion...")
        
        # Executes the query using the formatted dictionary for parameterized insertion
        for grants in cleaned_grants:
            formatted_params = format_grant_data_for_insert(grants)
            cursor.execute(sql_insert, formatted_params) 
            # Check if the insertion was successful (1 row inserted)
            if cursor.rowcount == 1:
                successful_insertions += 1
            else:
                log_error(f"Insertion of Grant #{i+1} failed (0 rows affected). Rolling back batch.")
                raise GrantOperationError(f"Failed to insert grant at index {i}. Stopping batch.")
            
        
        log_info(f"All {successful_insertions} grants inserted into transaction cache. Committing...")
        cnx.commit()
        log_info(f"Batch insertion successful. Total grants committed: {successful_insertions}")

        

    except MySQLError as e:
        # Rollback changes if a database error occurred
        if cnx and cnx.is_connected():
            cnx.rollback()
            log_error("Transaction rolled back due to MySQL error. No grants were saved.")
        log_error(f"MySQL error during batch insertion: {e}")
        return e
        
    except GrantOperationError as e:
        # This catches our custom error, usually triggered by a failed insertion/file error
        if cnx and cnx.is_connected():
             cnx.rollback()
             log_error("Transaction rolled back due to data/file error. No grants were saved.")
        log_error(f"Grant Operation Error: {e}")
        return e

    except Exception as e:
        # Catch all unexpected errors (Python, network, etc.)
        if cnx and cnx.is_connected():
             cnx.rollback()
        log_error(f"An unexpected error occurred during batch insertion: {e}")
        return GrantOperationError(e)

    finally:
        # --- 5. GUARANTEE CONNECTION CLOSURE ---
        if cursor:
            cursor.close()
            log_info("Cursor closed.")
        if cnx and cnx.is_connected():
            cnx.close()
            log_info("Database connection closed.")
