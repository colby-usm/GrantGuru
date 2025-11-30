from src.scraper.make_scrapes import main as scraper_script
from src.scraper.clean_scrapes import main as cleaner_script
from src.system_functions.delete_old_grants import main as deletion_script
from src.system_functions.insert_cleaned_grant import main as insert_script
from src.system_functions.insert_cleaned_grant import format_grant_data_for_insert
from datetime import date, datetime
from src.utils.logging_utils import log_info, log_error
from src.utils.sql_file_parsers import read_sql_helper
import json
from src.utils.logging_utils import log_info
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error as MySQLError
'''
    File: scraping_and_grant_test_for_demonstration.py
    Version: 15 November 2025
    Author: James Tedder

    Made with the help of gemini

    Description:
        - Made to be run with an empty database to show the scraper adding data to the database.
        - will also output the data to a .json file
'''

dirty_grant_dict = scraper_script([
    "--statuses", "forecasted", "posted", "-n", "15"
])

cleaned_grants: list = cleaner_script(dirty_grant_dict, filter_on_dates=100000)

insert_script(cleaned_grants)

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

SELECT_ALL_SCRIPT = "src/db_crud/grants/select_all_grants.sql"

sql_select = read_sql_helper(SELECT_ALL_SCRIPT)

def date_converter(obj):
    # Check if the object is a date or datetime object
    if isinstance(obj, (date, datetime)):
        # Convert it to an ISO 8601 string (e.g., "2025-11-15")
        return obj.isoformat()
    # For any other unsupported type, raise a TypeError
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME # Explicitly select the database
        )
        cursor = cnx.cursor()
        if sql_select != None:
            cursor.execute(sql_select)
            log_info("Sucessfully retrieved grants")
            column_names = [i[0] for i in cursor.description]

            grants_tuples = cursor.fetchall()
            grants_list_of_dicts = []
            date_fields = ['date_posted', 'archive_date', 'date_closed', 'last_update_date']

            for row in grants_tuples:
                grant_dict = dict(zip(column_names, row))
    
                # Manually convert dates to ISO string format
                for field in date_fields:
                    if field in grant_dict and isinstance(grant_dict[field], (date, datetime)):
                        grant_dict[field] = grant_dict[field].isoformat()
            
                grants_list_of_dicts.append(grant_dict)
        
        else :
            log_info("Failed to retrieve grants")
        
        file_path = 'src/test_suites/grants_data.json'

        try:
            with open(file_path, 'w') as json_file:
                json.dump(grants_list_of_dicts, json_file, indent=4)
            print(f"Successfully wrote data to {file_path}")
        except IOError as e:
            print(f"Error writing file: {e}")

except MySQLError as e:
    # Rollback changes if a database error occurred
    if cnx and cnx.is_connected():
        cnx.rollback()
        log_error("Transaction rolled back due to MySQL error. No grants were saved.")
    log_error(f"MySQL error during batch insertion: {e}")

except Exception as e:
    # Catch all unexpected errors (Python, network, etc.)
    if cnx and cnx.is_connected():
        cnx.rollback()
    log_error(f"An unexpected error occurred during batch insertion: {e}")





    
