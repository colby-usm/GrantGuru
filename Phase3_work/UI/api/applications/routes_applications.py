"""
routes_applications.py

Provides endpoints for working with Application entities.

Endpoints:
- GET /user/<user_id> : Return all applications for a given user_id
- GET /grants : Return all available grants
- POST /create : Create a new application

Note: Authentication/session management is out-of-scope for this patch.
      The endpoint accepts a user_id path parameter (returned by signin).
"""

import os
from datetime import datetime

from flask import request, jsonify
from mysql.connector import connect, Error as MySQLError

from . import applications_bp
from api import DB_NAME, HOST, MYSQL_USER, MYSQL_PASS, PHASE2_ROOT

# Attempt a dynamic import of the Phase2 application operations module so static analyzers
# do not complain about a non-resolvable 'src...' path while still allowing runtime use.
read_applications_by_user = None
create_application = None
ApplicationOperationError = Exception

try:
    import importlib
    import sys

    # If PHASE2_ROOT is set and contains a 'src' folder, add it to sys.path so we can import
    # the application_functions package as a top-level module.
    if PHASE2_ROOT:
        src_path = os.path.join(PHASE2_ROOT, "src")
        if os.path.isdir(src_path) and src_path not in sys.path:
            sys.path.insert(0, src_path)

    module = importlib.import_module("application_functions.application_operations")
    read_applications_by_user = getattr(module, "read_applications_by_user")
    create_application = getattr(module, "create_application")
    ApplicationOperationError = getattr(module, "ApplicationOperationError")
except Exception:
    # If Phase2 path isn't available or import fails, we'll surface an error at runtime
    read_applications_by_user = None
    create_application = None
    ApplicationOperationError = Exception


@applications_bp.route("/user/<user_id>", methods=["GET"])
def get_applications_for_user(user_id: str):
    """Return list of applications for the specified user_id (UUID string).

    Returns JSON list of objects with keys: application_id, user_id, grant_id, status, application_date
    """
    if read_applications_by_user is None:
        return jsonify({"error": "Server not configured to access application operations"}), 500

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                result = read_applications_by_user(None, user_id, user_id, cursor)

        if isinstance(result, ApplicationOperationError):
            return jsonify({"error": str(result)}), 500

        # result is a list of tuples (application_id, user_id, grant_id, status, application_date)
        apps = []
        for row in result:
            apps.append({
                "application_id": row[0],
                "user_id": row[1],
                "grant_id": row[2],
                "status": row[3],
                "application_date": str(row[4]) if row[4] is not None else None,
            })

        return jsonify({"applications": apps}), 200

    except MySQLError as e:
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@applications_bp.route("/grants", methods=["GET"])
def get_grants():
    """Fetch all grants from the database."""
    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                # Get grant_id (UUID binary) and program_title
                cursor.execute("""
                    SELECT BIN_TO_UUID(grant_id) AS grant_id, program_title
                    FROM grants
                    LIMIT 100
                """)
                rows = cursor.fetchall()

        grants = []
        for row in rows:
            grants.append({
                "grant_id": row[0] if isinstance(row, tuple) else row.get("grant_id"),
                "program_title": row[1] if isinstance(row, tuple) else row.get("program_title")
            })

        return jsonify({"grants": grants}), 200

    except MySQLError as e:
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@applications_bp.route("/create", methods=["POST"])
def create_new_application():
    """Create a new application for a grant.

    Expects JSON body with:
    - user_id (UUID string)
    - grant_id (UUID string)
    - status (default: 'pending')
    """
    if create_application is None:
        return jsonify({"error": "Server not configured to create applications"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    user_id = data.get("user_id")
    grant_id = data.get("grant_id")
    status = data.get("status", "pending")
    application_date = datetime.now().strftime("%Y-%m-%d")

    if not all([user_id, grant_id]):
        return jsonify({"error": "Missing required fields: user_id, grant_id"}), 400

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                result = create_application(None, user_id, user_id, cursor, grant_id, status, application_date)

        if isinstance(result, (ApplicationOperationError, MySQLError)):
            return jsonify({"error": str(result)}), 500

        conn.commit()
        return jsonify({"message": "Application created successfully"}), 201

    except MySQLError as e:
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

