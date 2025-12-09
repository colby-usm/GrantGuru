"""
Backup and Recovery Operations for Applications

This module provides functionality to backup and restore application data,
including related tasks and documents metadata.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error as MySQLError
from src.utils.sql_file_parsers import read_sql_helper
from src.utils.logging_utils import log_error

# Load environment variables from .env file
# Get the directory containing this script and navigate to Phase2_work root
script_dir = Path(__file__).parent.parent.parent  # Go up to Phase2_work root
dotenv_path = script_dir / ".env"

# Load .env file explicitly
load_dotenv(dotenv_path=dotenv_path)

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "password")


def get_db_connection():
    """Create and return a database connection."""
    try:
        return mysql.connector.connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
    except MySQLError as e:
        log_error(f"Failed to connect to database: {e}")
        raise


def execute_sql_query(sql_file_path: str, params: tuple = None) -> List[tuple]:
    """
    Execute a SQL query from a file and return results.

    Args:
        sql_file_path: Path to SQL file
        params: Parameters for the query

    Returns:
        List of result tuples
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql_script = read_sql_helper(sql_file_path)
        cursor.execute(sql_script, params or ())

        results = cursor.fetchall()
        return results
    except MySQLError as e:
        log_error(f"MySQL error executing {sql_file_path}: {e}")
        raise
    finally:
        if conn:
            conn.close()


def execute_sql_command(sql_file_path: str, params: tuple = None) -> Tuple[str, int]:
    """
    Execute a SQL command (INSERT/UPDATE/DELETE) from a file.

    Args:
        sql_file_path: Path to SQL file
        params: Parameters for the command

    Returns:
        Tuple of (message, status_code)
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql_script = read_sql_helper(sql_file_path)
        cursor.execute(sql_script, params or ())

        conn.commit()
        return ("Success", 200)
    except MySQLError as e:
        log_error(f"MySQL error executing {sql_file_path}: {e}")
        return (str(e), 500)
    finally:
        if conn:
            conn.close()


def create_backup_for_user(user_id: str) -> Dict:
    """
    Create a complete backup of all applications for a specific user.

    Args:
        user_id: UUID string of the user

    Returns:
        Dictionary containing:
        - backup_metadata: timestamp, user_id, count
        - applications: list of application data
        - tasks: dict mapping application_id to list of tasks
        - documents: dict mapping application_id to list of documents

    Raises:
        Exception: If database query fails
    """
    backup_data = {
        "backup_metadata": {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "backup_version": "1.0"
        },
        "applications": [],
        "tasks": {},
        "documents": {}
    }

    # Get all applications for the user
    sql_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db_crud',
        'applications',
        'backup_applications_by_user.sql'
    )

    applications_result = execute_sql_query(sql_file, (user_id,))

    if not applications_result:
        backup_data["backup_metadata"]["application_count"] = 0
        return backup_data

    # Process each application
    for app_row in applications_result:
        app_data = {
            "application_id": app_row[0],
            "user_id": app_row[1],
            "grant_id": app_row[2],
            "submission_status": app_row[3],
            "status": app_row[4],
            "application_date": app_row[5].isoformat() if app_row[5] else None,
            "submitted_at": app_row[6].isoformat() if app_row[6] else None,
            "internal_deadline": app_row[7].isoformat() if app_row[7] else None,
            "notes": app_row[8],
            "grant_info": {
                "grant_title": app_row[9],
                "opportunity_number": app_row[10],
                "provider": app_row[11],
                "award_max_amount": app_row[12],
                "award_min_amount": app_row[13]
            },
            "user_info": {
                "email": app_row[14],
                "f_name": app_row[15],
                "l_name": app_row[16],
                "institution": app_row[17]
            }
        }

        backup_data["applications"].append(app_data)

        # Get tasks for this application
        app_id = app_row[0]
        tasks = get_application_tasks(app_id)
        if tasks:
            backup_data["tasks"][app_id] = tasks

        # Get documents for this application
        documents = get_application_documents(app_id)
        if documents:
            backup_data["documents"][app_id] = documents

    backup_data["backup_metadata"]["application_count"] = len(backup_data["applications"])
    backup_data["backup_metadata"]["total_tasks"] = sum(len(tasks) for tasks in backup_data["tasks"].values())
    backup_data["backup_metadata"]["total_documents"] = sum(len(docs) for docs in backup_data["documents"].values())

    return backup_data


def get_application_tasks(application_id: str) -> List[Dict]:
    """
    Get all tasks for a specific application.

    Args:
        application_id: UUID string of the application

    Returns:
        List of task dictionaries
    """
    sql_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db_crud',
        'applications',
        'backup_application_tasks.sql'
    )

    result = execute_sql_query(sql_file, (application_id,))

    if not result:
        return []

    tasks = []
    for row in result:
        task_data = {
            "task_id": row[0],
            "application_id": row[1],
            "task_name": row[2],
            "task_description": row[3],
            "deadline": row[4].isoformat() if row[4] else None,
            "completed": bool(row[5]),
            "created_at": row[6].isoformat() if row[6] else None,
            "updated_at": row[7].isoformat() if row[7] else None
        }
        tasks.append(task_data)

    return tasks


def get_application_documents(application_id: str) -> List[Dict]:
    """
    Get all document metadata for a specific application.

    Args:
        application_id: UUID string of the application

    Returns:
        List of document metadata dictionaries
    """
    sql_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db_crud',
        'applications',
        'backup_application_documents.sql'
    )

    result = execute_sql_query(sql_file, (application_id,))

    if not result:
        return []

    documents = []
    for row in result:
        doc_data = {
            "document_id": row[0],
            "application_id": row[1],
            "document_name": row[2],
            "document_type": row[3],
            "document_size": row[4],
            "upload_date": row[5].isoformat() if row[5] else None
        }
        documents.append(doc_data)

    return documents


def save_backup_to_file(backup_data: Dict, user_id: str, backup_dir: str = "backups") -> str:
    """
    Save backup data to a JSON file.

    Args:
        backup_data: Backup data dictionary
        user_id: User ID for filename
        backup_dir: Directory to save backups (default: "backups")

    Returns:
        Path to the created backup file
    """
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_user_{user_id}_{timestamp}.json"
    filepath = os.path.join(backup_dir, filename)

    # Write backup data to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    return filepath


def load_backup_from_file(filepath: str) -> Dict:
    """
    Load backup data from a JSON file.

    Args:
        filepath: Path to the backup file

    Returns:
        Backup data dictionary

    Raises:
        FileNotFoundError: If backup file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)

    return backup_data


def restore_application_from_backup(app_data: Dict) -> Tuple[bool, str]:
    """
    Restore a single application from backup data.

    Args:
        app_data: Application data dictionary from backup

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sql_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'db_crud',
            'applications',
            'restore_application.sql'
        )

        params = (
            app_data["application_id"],
            app_data["user_id"],
            app_data["grant_id"],
            app_data["submission_status"],
            app_data["status"],
            app_data["application_date"],
            app_data["submitted_at"],
            app_data["internal_deadline"],
            app_data["notes"]
        )

        result = execute_sql_command(sql_file, params)

        if result and result[1] == 200:
            return True, f"Application {app_data['application_id']} restored successfully"
        else:
            return False, f"Failed to restore application: {result[0] if result else 'Unknown error'}"

    except Exception as e:
        return False, f"Error restoring application: {str(e)}"


def restore_task_from_backup(task_data: Dict) -> Tuple[bool, str]:
    """
    Restore a single task from backup data.

    Args:
        task_data: Task data dictionary from backup

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sql_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'db_crud',
            'applications',
            'restore_application_task.sql'
        )

        params = (
            task_data["task_id"],
            task_data["application_id"],
            task_data["task_name"],
            task_data["task_description"],
            task_data["deadline"],
            task_data["completed"],
            task_data["created_at"],
            task_data["updated_at"]
        )

        result = execute_sql_command(sql_file, params)

        if result and result[1] == 200:
            return True, "Task restored successfully"
        else:
            return False, f"Failed to restore task: {result[0] if result else 'Unknown error'}"

    except Exception as e:
        return False, f"Error restoring task: {str(e)}"


def restore_document_from_backup(doc_data: Dict) -> Tuple[bool, str]:
    """
    Restore a single document metadata from backup data.
    Note: This only restores metadata; actual file content must be restored separately.

    Args:
        doc_data: Document data dictionary from backup

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sql_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'db_crud',
            'applications',
            'restore_application_document.sql'
        )

        params = (
            doc_data["document_id"],
            doc_data["application_id"],
            doc_data["document_name"],
            doc_data["document_type"],
            doc_data["document_size"],
            doc_data["upload_date"]
        )

        result = execute_sql_command(sql_file, params)

        if result and result[1] == 200:
            return True, "Document metadata restored successfully"
        else:
            return False, f"Failed to restore document: {result[0] if result else 'Unknown error'}"

    except Exception as e:
        return False, f"Error restoring document: {str(e)}"


def restore_backup_for_user(backup_data: Dict) -> Dict:
    """
    Restore complete backup for a user.

    Args:
        backup_data: Complete backup data dictionary

    Returns:
        Dictionary with restoration results:
        - success: bool
        - applications_restored: int
        - tasks_restored: int
        - documents_restored: int
        - errors: list of error messages
    """
    results = {
        "success": True,
        "applications_restored": 0,
        "tasks_restored": 0,
        "documents_restored": 0,
        "errors": []
    }

    # Restore applications
    for app_data in backup_data.get("applications", []):
        success, message = restore_application_from_backup(app_data)
        if success:
            results["applications_restored"] += 1

            # Restore tasks for this application
            app_id = app_data["application_id"]
            if app_id in backup_data.get("tasks", {}):
                for task_data in backup_data["tasks"][app_id]:
                    task_success, task_msg = restore_task_from_backup(task_data)
                    if task_success:
                        results["tasks_restored"] += 1
                    else:
                        results["errors"].append(task_msg)

            # Restore documents for this application
            if app_id in backup_data.get("documents", {}):
                for doc_data in backup_data["documents"][app_id]:
                    doc_success, doc_msg = restore_document_from_backup(doc_data)
                    if doc_success:
                        results["documents_restored"] += 1
                    else:
                        results["errors"].append(doc_msg)
        else:
            results["errors"].append(message)
            results["success"] = False

    return results


def list_available_backups(backup_dir: str = "backups", user_id: Optional[str] = None) -> List[Dict]:
    """
    List all available backup files.

    Args:
        backup_dir: Directory containing backups
        user_id: Optional filter by user ID

    Returns:
        List of backup file information dictionaries
    """
    if not os.path.exists(backup_dir):
        return []

    backups = []

    for filename in os.listdir(backup_dir):
        if not filename.endswith('.json'):
            continue

        # Filter by user_id if provided
        if user_id and f"user_{user_id}" not in filename:
            continue

        filepath = os.path.join(backup_dir, filename)
        file_stat = os.stat(filepath)

        backup_info = {
            "filename": filename,
            "filepath": filepath,
            "size": file_stat.st_size,
            "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }

        # Try to load metadata from the file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "backup_metadata" in data:
                    backup_info.update(data["backup_metadata"])
        except Exception:
            pass

        backups.append(backup_info)

    # Sort by created date, newest first
    backups.sort(key=lambda x: x.get("created", ""), reverse=True)

    return backups
