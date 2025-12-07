"""
    File: insert_cleaned_grant.py
    Version: 15 November 2025
    Author: James Tedder

    Made with the help of Gemini. The format grant data was done by the AI.

    Description: Inserts the cleaned grants into the database. Either as a new
    grant or updating the existing grant already in the database if it has the 
    same opportunity_number. 

    Usage: takes a cleaned list of dictionaries and adds them to the grants relation

"""

import json
from typing import Dict, Any

import os
import sys
import json
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

    INSERT_GRANT_SCRIPT = "src/db_crud/grants/create_grants.sql"
    CHECK_IF_ALREADY_IN_DB_SCRIPT = "src/db_crud/grants/select_grants_by_opportunity_number.sql"
    UPDATE_GRANT_SCRIPT = "src/db_crud/grants/update_grants_by_opportunity_number.sql"

    cnx = None
    cursor = None
    successful_insertions = 0


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
        sql_insert = read_sql_helper(INSERT_GRANT_SCRIPT)
        
        if sql_insert is None:
            raise GrantOperationError(f"SQL script file not found: {INSERT_GRANT_SCRIPT}")
        
        sql_select = read_sql_helper(CHECK_IF_ALREADY_IN_DB_SCRIPT)

        if sql_select is None:
            raise GrantOperationError(f"SQL script file not found: {CHECK_IF_ALREADY_IN_DB_SCRIPT}")
        
        sql_update = read_sql_helper(UPDATE_GRANT_SCRIPT)
        
        if sql_update is None:
            raise GrantOperationError(f"SQL script file not found: {UPDATE_GRANT_SCRIPT}")
        
        # --- 3. EXECUTE INSERTION ---
        
        # Executes the query using the formatted dictionary for parameterized insertion
        for grants in cleaned_grants:
            formatted_params = format_grant_data_for_insert(grants)
            
            opportunity_id = (formatted_params["opportunity_number"],)

            cursor.execute(sql_select, opportunity_id)
            grant = cursor.fetchone()
            # If the grant is already in the database it will update it with the new information.
            if grant == None:
                cursor.execute(sql_insert, formatted_params) 
            else:
                cursor.execute(sql_update, formatted_params)
            
        
        cnx.commit()

        

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
        if cnx and cnx.is_connected():
            cnx.close()




if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python -m src.system_functions.insert_cleaned_grant <path_to_grants_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    try:
        with open(json_path, "r") as f:
            cleaned_grants = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {json_path}: {e}")
        sys.exit(1)

    result = main(cleaned_grants)
    if result is None:
        sys.exit(0)
    else:
        print(f"✗ Grant insertion failed: {result}")
        sys.exit(1)
