"""
File: insert_cleaned_grant.py
Version: 15 November 2025
Author: James Tedder

Description:
    Inserts cleaned grants into the database. If a grant already exists (by
    opportunity_number) it will be updated, otherwise inserted.

Usage: call `main(cleaned_grants_list)` where cleaned_grants_list is a list
of dictionaries produced by `clean_scrapes.main()`.
"""

from typing import Dict, Any
import os
import json
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error as MySQLError
import traceback
import json as _json
from datetime import datetime

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
    """Custom exception for insertion operation failures."""
    pass


def main(cleaned_grants: list):
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

    log_info("Connecting to MySQL server for insertion...")

    try:
        # --- 1. CONNECT TO DATABASE (with DB name specified) ---
        cnx = mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME,
        )
        cursor = cnx.cursor()

        # --- 2. LOAD SQL Script ---
        log_info(f"Loading insertion script from {INSERT_GRANT_SCRIPT}...")
        sql_insert = read_sql_helper(INSERT_GRANT_SCRIPT)
        if sql_insert is None:
            raise GrantOperationError(f"SQL script file not found: {INSERT_GRANT_SCRIPT}")

        log_info(f"Loading selection script from {CHECK_IF_ALREADY_IN_DB_SCRIPT}...")
        sql_select = read_sql_helper(CHECK_IF_ALREADY_IN_DB_SCRIPT)
        if sql_select is None:
            raise GrantOperationError(f"SQL script file not found: {CHECK_IF_ALREADY_IN_DB_SCRIPT}")

        log_info(f"Loading update script from {UPDATE_GRANT_SCRIPT}...")
        sql_update = read_sql_helper(UPDATE_GRANT_SCRIPT)
        if sql_update is None:
            raise GrantOperationError(f"SQL script file not found: {UPDATE_GRANT_SCRIPT}")

        # --- 3. EXECUTE INSERTION ---
        log_info("Executing grant insertion...")

        if not cleaned_grants:
            log_info("No cleaned grants to insert. Exiting.")
            return 0

        # Executes the query using the formatted dictionary for parameterized insertion
        for grants in cleaned_grants:
            try:
                formatted_params = format_grant_data_for_insert(grants)

                opportunity_id = (formatted_params.get("opportunity_number"),)

                cursor.execute(sql_select, opportunity_id)
                grant = cursor.fetchone()

                # If the grant is already in the database it will update it with the new information.
                if grant is None:
                    try:
                        cursor.execute(sql_insert, formatted_params)
                        successful_insertions += 1
                        log_info("Grant inserted")
                    except MySQLError as db_e:
                        # Log detailed DB error and failing params for diagnosis, then re-raise to trigger rollback
                        err_info = {
                            "error": str(db_e),
                            "errno": getattr(db_e, 'errno', None),
                            "sqlstate": getattr(db_e, 'sqlstate', None),
                            "opportunity_number": formatted_params.get('opportunity_number'),
                            "param_keys": list(formatted_params.keys()),
                            "desc_len": len((formatted_params.get('description') or ''))
                        }
                        log_error(f"MySQL error inserting grant: {err_info}")
                        tb = traceback.format_exc()
                        log_error(tb)
                        # persist failing params to runtime/failed_inserts.jsonl for off-line inspection
                        try:
                            os.makedirs(os.path.join(os.getcwd(), 'Phase2_work', 'runtime'), exist_ok=True)
                            dump_path = os.path.join(os.getcwd(), 'Phase2_work', 'runtime', 'failed_inserts.jsonl')
                            with open(dump_path, 'a', encoding='utf-8') as fh:
                                fh.write(_json.dumps({
                                    'ts': datetime.utcnow().isoformat(),
                                    'action': 'insert',
                                    'opportunity_number': formatted_params.get('opportunity_number'),
                                    'error': str(db_e),
                                    'params_preview': {k: (v[:200] if isinstance(v, str) else v) for k, v in formatted_params.items()}
                                }, ensure_ascii=False) + '\n')
                        except Exception as dump_e:
                            log_error(f"Failed to write failed insert dump: {dump_e}")
                        raise
                else:
                    try:
                        cursor.execute(sql_update, formatted_params)
                        successful_insertions += 1
                        log_info("Grant updated")
                    except MySQLError as db_e:
                        err_info = {
                            "error": str(db_e),
                            "errno": getattr(db_e, 'errno', None),
                            "sqlstate": getattr(db_e, 'sqlstate', None),
                            "opportunity_number": formatted_params.get('opportunity_number'),
                            "param_keys": list(formatted_params.keys()),
                            "desc_len": len((formatted_params.get('description') or ''))
                        }
                        log_error(f"MySQL error updating grant: {err_info}")
                        tb = traceback.format_exc()
                        log_error(tb)
                        try:
                            os.makedirs(os.path.join(os.getcwd(), 'Phase2_work', 'runtime'), exist_ok=True)
                            dump_path = os.path.join(os.getcwd(), 'Phase2_work', 'runtime', 'failed_inserts.jsonl')
                            with open(dump_path, 'a', encoding='utf-8') as fh:
                                fh.write(_json.dumps({
                                    'ts': datetime.utcnow().isoformat(),
                                    'action': 'update',
                                    'opportunity_number': formatted_params.get('opportunity_number'),
                                    'error': str(db_e),
                                    'params_preview': {k: (v[:200] if isinstance(v, str) else v) for k, v in formatted_params.items()}
                                }, ensure_ascii=False) + '\n')
                        except Exception as dump_e:
                            log_error(f"Failed to write failed update dump: {dump_e}")
                        raise

            except MySQLError:
                # re-raise to allow outer handler to rollback
                raise
            except Exception as e:
                # Non-DB error; log and continue
                try:
                    opp = formatted_params.get('opportunity_number')
                except Exception:
                    opp = None
                log_error(f"Error processing grant {opp}: {e}")
                log_error(traceback.format_exc())
                continue

        log_info(f"All grants processed into transaction cache ({successful_insertions} changes). Committing...")
        cnx.commit()
        log_info(f"Batch insertion successful. {successful_insertions} grants inserted/updated.")
        return successful_insertions

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
