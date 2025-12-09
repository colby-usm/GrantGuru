# routes_user.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import connect, Error as MySQLError
from api import PHASE2_ROOT
from datetime import datetime
import os

user_bp = Blueprint("user", __name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@user_bp.route("/personal-info", methods=["PUT"])
@jwt_required()
def update_personal_info():

    from api import update_users_fields, Role, UserOperationError, HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Updating personal info for user_id: {user_id}")

    data = request.get_json()
    current_app.logger.info(f"Payload received: {data}")

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    # Map frontend names to SQL parameter names
    field_map = {
        "fName": "f_name",
        "mName": "m_name",
        "lName": "l_name",
        "institution": "institution"
    }

    new_fields = {sql_key: data[frontend_key] 
                  for frontend_key, sql_key in field_map.items() 
                  if frontend_key in data}


    new_fields["user_id"] = user_id

    if not new_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        result = update_users_fields(
            role=Role.USER,
            user_id=user_id,
            resource_owner_id=user_id,
            cursor=cursor,
            new_fields=new_fields,
            base_path=PHASE2_ROOT
        )

        if isinstance(result, (UserOperationError, MySQLError)):
            current_app.logger.error(f"Error updating user fields: {result}")
            return jsonify({"error": str(result)}), 500

        conn.commit()
        return jsonify({"msg": "Personal info updated successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Unexpected error updating personal info")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/email", methods=["PUT"])
@jwt_required()
def update_email():
    from api import update_users_email, Role, UserOperationError, HOST, MYSQL_USER, MYSQL_PASS, DB_NAME, PHASE2_ROOT
    from mysql.connector import connect, Error as MySQLError

    user_id = get_jwt_identity()
    current_app.logger.info(f"Updating email for user_id: {user_id}")

    data = request.get_json()
    current_app.logger.info(f"Payload received: {data}")

    if not data or "email" not in data or not data["email"]:
        return jsonify({"error": "Missing or empty email"}), 400

    new_email_data = {
        "email": data["email"],
        "user_id": user_id
    }

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        result = update_users_email(
            role=Role.USER,
            user_id=user_id,
            resource_owner_id=user_id,
            cursor=cursor,
            new_email=data["email"],
            base_path=PHASE2_ROOT
        )

        if isinstance(result, (UserOperationError, MySQLError)):
            current_app.logger.error(f"Error updating users email: {result}")
            return jsonify({"error": str(result)}), 500

        conn.commit()
        return jsonify({"msg": "Email updated successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Unexpected error updating email")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass




@user_bp.route("/password", methods=["PUT"])
@jwt_required()
def update_password():
    from api import update_users_password, Role, UserOperationError, HOST, MYSQL_USER, MYSQL_PASS, DB_NAME, PHASE2_ROOT
    from mysql.connector import connect, Error as MySQLError

    user_id = get_jwt_identity()
    current_app.logger.info(f"Updating password for user_id: {user_id}")

    data = request.get_json()
    current_app.logger.info(f"Payload received: {data}")

    # Validate payload
    if not data or "oldPassword" not in data or "newPassword" not in data:
        return jsonify({"error": "Missing oldPassword or newPassword"}), 400
    if not data["oldPassword"] or not data["newPassword"]:
        return jsonify({"error": "Empty oldPassword or newPassword"}), 400

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        result = update_users_password(
            role=Role.USER,
            user_id=user_id,
            resource_owner_id=user_id,
            cursor=cursor,
            old_password=data["oldPassword"],
            new_password=data["newPassword"],
            base_path=PHASE2_ROOT
        )

        if isinstance(result, UserOperationError):
            return jsonify({"error": str(result)}), 400
        elif isinstance(result, MySQLError):
            current_app.logger.error(f"Error updating user password: {result}")
            return jsonify({"error": "Database error"}), 500

        conn.commit()
        return jsonify({"msg": "Password updated successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Unexpected error updating password")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_user_applications():
    """Fetch all applications for the authenticated user with grant details."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Fetching applications for user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Join applications with grants to get grant details
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(a.application_id) AS application_id,
                BIN_TO_UUID(a.user_id) AS user_id,
                BIN_TO_UUID(a.grant_id) AS grant_id,
                a.submission_status,
                a.status,
                DATE_FORMAT(a.application_date, '%Y-%m-%d') AS application_date,
                g.grant_title AS grant_name
            FROM Applications a
            JOIN Grants g ON a.grant_id = g.grant_id
            WHERE a.user_id = UUID_TO_BIN(%s)
            ORDER BY a.application_date DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        applications = [
            {
                "application_id": row[0],
                "user_id": row[1],
                "grant_id": row[2],
                "submission_status": row[3],
                "status": row[4],
                "application_date": row[5],
                "grant_name": row[6]
            }
            for row in rows
        ]

        return jsonify({"applications": applications}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error fetching applications: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error fetching applications")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications", methods=["POST"])
@jwt_required()
def create_application():
    """Create a new application for a grant."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME
    from datetime import date, datetime

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "grant_id" not in data:
        return jsonify({"error": "Missing grant_id"}), 400

    grant_id = data["grant_id"]
    submission_status = data.get("submission_status", "started")
    status = data.get("status", "pending")
    application_date = data.get("application_date", str(date.today()))

    current_app.logger.info(f"Creating application for user_id: {user_id}, grant_id: {grant_id}, submission_status: {submission_status}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Check if user already applied to this grant
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE user_id = UUID_TO_BIN(%s) AND grant_id = UUID_TO_BIN(%s)
            """,
            (user_id, grant_id)
        )

        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "You have already applied to this grant"}), 409

        # Insert new application with submission_status
        submitted_at = datetime.now() if submission_status == "submitted" else None
        cursor.execute(
            """
            INSERT INTO Applications (user_id, grant_id, submission_status, status, application_date, submitted_at)
            VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), %s, %s, %s, %s)
            """,
            (user_id, grant_id, submission_status, status, application_date, submitted_at)
        )

        conn.commit()

        # Get the created application with grant details
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(a.application_id) AS application_id,
                BIN_TO_UUID(a.user_id) AS user_id,
                BIN_TO_UUID(a.grant_id) AS grant_id,
                a.submission_status,
                a.status,
                DATE_FORMAT(a.application_date, '%Y-%m-%d') AS application_date,
                g.grant_title AS grant_name
            FROM Applications a
            JOIN Grants g ON a.grant_id = g.grant_id
            WHERE a.user_id = UUID_TO_BIN(%s) AND a.grant_id = UUID_TO_BIN(%s)
            """,
            (user_id, grant_id)
        )

        row = cursor.fetchone()
        application = {
            "application_id": row[0],
            "user_id": row[1],
            "grant_id": row[2],
            "submission_status": row[3],
            "status": row[4],
            "application_date": row[5],
            "grant_name": row[6]
        }

        return jsonify({"message": "Application created successfully", "application": application}), 201

    except MySQLError as e:
        current_app.logger.error(f"Database error creating application: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error creating application")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>", methods=["GET"])
@jwt_required()
def get_single_application(application_id: str):
    """Get a single application with grant details."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Fetching application {application_id} for user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Fetch application with grant details
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(a.application_id) AS application_id,
                BIN_TO_UUID(a.user_id) AS user_id,
                BIN_TO_UUID(a.grant_id) AS grant_id,
                a.submission_status,
                a.status,
                DATE_FORMAT(a.application_date, '%Y-%m-%d') AS application_date,
                g.grant_title AS grant_name,
                DATE_FORMAT(a.internal_deadline, '%Y-%m-%d') AS internal_deadline,
                a.notes
            FROM Applications a
            JOIN Grants g ON a.grant_id = g.grant_id
            WHERE a.application_id = UUID_TO_BIN(%s) AND a.user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Application not found or access denied"}), 404

        application = {
            "application_id": row[0],
            "user_id": row[1],
            "grant_id": row[2],
            "submission_status": row[3],
            "status": row[4],
            "application_date": row[5],
            "grant_name": row[6],
            "internal_deadline": row[7],
            "notes": row[8]
        }

        return jsonify({"application": application}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error fetching application: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error fetching application")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>", methods=["PUT"])
@jwt_required()
def update_application_status(application_id: str):
    """Update a user's application (status, internal_deadline, notes)."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    # Build update fields dynamically
    update_fields = []
    params = []

    if "status" in data:
        new_status = data["status"]
        valid_statuses = ["pending", "in_review", "approved", "rejected"]
        if new_status not in valid_statuses:
            return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        update_fields.append("status = %s")
        params.append(new_status)

    if "submission_status" in data:
        new_submission_status = data["submission_status"]
        valid_submission_statuses = ["started", "submitted"]
        if new_submission_status not in valid_submission_statuses:
            return jsonify({"error": f"Invalid submission_status. Must be one of: {', '.join(valid_submission_statuses)}"}), 400
        update_fields.append("submission_status = %s")
        params.append(new_submission_status)

        # If changing to submitted, set submitted_at timestamp
        if new_submission_status == "submitted":
            from datetime import datetime
            update_fields.append("submitted_at = %s")
            params.append(datetime.now())

    if "internal_deadline" in data:
        update_fields.append("internal_deadline = %s")
        params.append(data["internal_deadline"] if data["internal_deadline"] else None)

    if "notes" in data:
        update_fields.append("notes = %s")
        params.append(data["notes"] if data["notes"] else None)

    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    current_app.logger.info(f"Updating application {application_id} for user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Update the application
        params.extend([application_id, user_id])
        update_query = f"""
            UPDATE Applications
            SET {', '.join(update_fields)}
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
        """
        cursor.execute(update_query, tuple(params))

        conn.commit()

        return jsonify({"message": "Application updated successfully"}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error updating application: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error updating application")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>", methods=["DELETE"])
@jwt_required()
def delete_application(application_id: str):
    """Delete a user's application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Deleting application {application_id} for user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user before deleting
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Delete the application
        cursor.execute(
            """
            DELETE FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        conn.commit()

        return jsonify({"message": "Application deleted successfully"}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error deleting application: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error deleting application")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


# ==================== APPLICATION TASKS ENDPOINTS ====================

@user_bp.route("/applications/<application_id>/tasks", methods=["GET"])
@jwt_required()
def get_application_tasks(application_id: str):
    """Get all tasks for a specific application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Fetching tasks for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Fetch all tasks for this application
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(internal_deadline_id) AS task_id,
                BIN_TO_UUID(application_id) AS application_id,
                deadline_name,
                task_description,
                DATE_FORMAT(deadline_date, '%Y-%m-%d') AS deadline,
                completed,
                created_at,
                updated_at
            FROM InternalDeadlines
            WHERE application_id = UUID_TO_BIN(%s)
            ORDER BY deadline_date ASC
            """,
            (application_id,)
        )

        rows = cursor.fetchall()
        tasks = [
            {
                "task_id": row[0],
                "application_id": row[1],
                "task_name": row[2],
                "task_description": row[3],
                "deadline": row[4],
                "completed": bool(row[5]),
                "created_at": str(row[6]) if row[6] else None,
                "updated_at": str(row[7]) if row[7] else None
            }
            for row in rows
        ]

        return jsonify({"tasks": tasks}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error fetching tasks: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error fetching tasks")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/tasks", methods=["POST"])
@jwt_required()
def create_task(application_id: str):
    """Create a new task for an application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "task_name" not in data or "deadline" not in data:
        return jsonify({"error": "Missing required fields: task_name, deadline"}), 400

    task_name = data["task_name"]
    task_description = data.get("task_description", "")
    deadline = data["deadline"]

    current_app.logger.info(f"Creating task for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user and is started
        cursor.execute(
            """
            SELECT submission_status, grant_id FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Application not found or access denied"}), 404

        submission_status = result[0]
        grant_id_bin = result[1]

        if submission_status == "submitted":
            return jsonify({"error": "Cannot add tasks to a submitted application. Tasks can only be added to applications with 'started' status."}), 400

        # Get grant deadline to validate task deadline
        cursor.execute(
            """
            SELECT date_closed FROM Grants WHERE grant_id = %s
            """,
            (grant_id_bin,)
        )
        grant_result = cursor.fetchone()
        if grant_result and grant_result[0]:
            grant_deadline = grant_result[0]
            if deadline > str(grant_deadline):
                return jsonify({"error": "Task deadline cannot exceed grant deadline"}), 400

        # Insert new task
        cursor.execute(
            """
            INSERT INTO InternalDeadlines (application_id, deadline_name, task_description, deadline_date)
            VALUES (UUID_TO_BIN(%s), %s, %s, %s)
            """,
            (application_id, task_name, task_description, deadline)
        )

        conn.commit()

        # Get the created task
        task_id = cursor.lastrowid
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(internal_deadline_id) AS task_id,
                BIN_TO_UUID(application_id) AS application_id,
                deadline_name,
                task_description,
                DATE_FORMAT(deadline_date, '%Y-%m-%d') AS deadline,
                completed,
                created_at,
                updated_at
            FROM InternalDeadlines
            WHERE application_id = UUID_TO_BIN(%s)
            ORDER BY created_at DESC LIMIT 1
            """,
            (application_id,)
        )

        row = cursor.fetchone()
        task = {
            "task_id": row[0],
            "application_id": row[1],
            "task_name": row[2],
            "task_description": row[3],
            "deadline": row[4],
            "completed": bool(row[5]),
            "created_at": str(row[6]) if row[6] else None,
            "updated_at": str(row[7]) if row[7] else None
        }

        return jsonify({"message": "Task created successfully", "task": task}), 201

    except MySQLError as e:
        current_app.logger.error(f"Database error creating task: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error creating task")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/tasks/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(application_id: str, task_id: str):
    """Update a task (name, description, deadline, completed status)."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT submission_status FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Application not found or access denied"}), 404

        submission_status = result[0]
        if submission_status == "submitted":
            return jsonify({"error": "Cannot modify tasks of a submitted application. Tasks can only be modified for applications with 'started' status."}), 400

        # Build update fields dynamically
        update_fields = []
        params = []

        if "task_name" in data:
            update_fields.append("deadline_name = %s")
            params.append(data["task_name"])

        if "task_description" in data:
            update_fields.append("task_description = %s")
            params.append(data["task_description"])

        if "deadline" in data:
            update_fields.append("deadline_date = %s")
            params.append(data["deadline"])

        if "completed" in data:
            update_fields.append("completed = %s")
            params.append(data["completed"])

        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        # Update the task
        params.extend([task_id, application_id])
        update_query = f"""
            UPDATE InternalDeadlines
            SET {', '.join(update_fields)}
            WHERE internal_deadline_id = UUID_TO_BIN(%s) AND application_id = UUID_TO_BIN(%s)
        """
        cursor.execute(update_query, tuple(params))

        conn.commit()

        return jsonify({"message": "Task updated successfully"}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error updating task: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error updating task")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/tasks/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(application_id: str, task_id: str):
    """Delete a task from an application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user and is started
        cursor.execute(
            """
            SELECT submission_status FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Application not found or access denied"}), 404

        submission_status = result[0]
        if submission_status == "submitted":
            return jsonify({"error": "Cannot delete tasks from a submitted application. Tasks can only be deleted from applications with 'started' status."}), 400

        # Delete the task
        cursor.execute(
            """
            DELETE FROM InternalDeadlines
            WHERE internal_deadline_id = UUID_TO_BIN(%s) AND application_id = UUID_TO_BIN(%s)
            """,
            (task_id, application_id)
        )

        conn.commit()

        return jsonify({"message": "Task deleted successfully"}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error deleting task: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error deleting task")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


# ==================== DOCUMENT UPLOAD ENDPOINTS ====================

@user_bp.route("/applications/<application_id>/documents", methods=["POST"])
@jwt_required()
def upload_documents(application_id: str):
    """Upload documents for an application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME
    from werkzeug.utils import secure_filename
    import uuid

    user_id = get_jwt_identity()
    current_app.logger.info(f"Uploading documents for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT submission_status FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Check if files were uploaded
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist('files')
        document_type = request.form.get('document_type', 'Other')

        if not files or all(f.filename == '' for f in files):
            return jsonify({"error": "No files selected"}), 400

        uploaded_documents = []

        # Create application-specific folder
        app_folder = os.path.join(UPLOAD_FOLDER, application_id)
        os.makedirs(app_folder, exist_ok=True)

        for file in files:
            if file and file.filename:
                # Secure the filename and add unique identifier
                original_filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{original_filename}"
                file_path = os.path.join(app_folder, unique_filename)

                # Save file to disk
                file.save(file_path)
                file_size = os.path.getsize(file_path)

                # Insert document record into database
                cursor.execute(
                    """
                    INSERT INTO Documents (document_name, document_type, document_size, upload_date, application_id)
                    VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s))
                    """,
                    (original_filename, document_type, file_size, datetime.now(), application_id)
                )

                # Get the created document ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT BIN_TO_UUID(document_id) FROM Documents WHERE application_id = UUID_TO_BIN(%s)
                    ORDER BY upload_date DESC LIMIT 1
                    """,
                    (application_id,)
                )
                document_id = cursor.fetchone()[0]

                uploaded_documents.append({
                    "document_id": document_id,
                    "document_name": original_filename,
                    "document_type": document_type,
                    "document_size": file_size
                })

        conn.commit()

        return jsonify({
            "message": f"{len(uploaded_documents)} document(s) uploaded successfully",
            "documents": uploaded_documents
        }), 201

    except MySQLError as e:
        current_app.logger.error(f"Database error uploading documents: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error uploading documents")
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/documents", methods=["GET"])
@jwt_required()
def get_application_documents(application_id: str):
    """Get all documents for a specific application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Fetching documents for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Fetch all documents for this application
        cursor.execute(
            """
            SELECT
                BIN_TO_UUID(document_id) AS document_id,
                document_name,
                document_type,
                document_size,
                upload_date
            FROM Documents
            WHERE application_id = UUID_TO_BIN(%s)
            ORDER BY upload_date DESC
            """,
            (application_id,)
        )

        rows = cursor.fetchall()
        documents = []
        for row in rows:
            doc = {
                "document_id": row[0],
                "document_name": row[1],
                "document_type": row[2],
                "document_size": row[3],
                "upload_date": str(row[4]) if row[4] else None
            }
            documents.append(doc)

        return jsonify({"documents": documents}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error fetching documents: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error fetching documents")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/documents/<document_id>", methods=["DELETE"])
@jwt_required()
def delete_document(application_id: str, document_id: str):
    """Delete a document from an application."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME

    user_id = get_jwt_identity()
    current_app.logger.info(f"Deleting document {document_id} for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Get document info before deleting (for file deletion)
        cursor.execute(
            """
            SELECT document_name FROM Documents
            WHERE document_id = UUID_TO_BIN(%s) AND application_id = UUID_TO_BIN(%s)
            """,
            (document_id, application_id)
        )

        doc_row = cursor.fetchone()
        if not doc_row:
            return jsonify({"error": "Document not found"}), 404

        document_name = doc_row[0]  # type: ignore

        # Delete from database
        cursor.execute(
            """
            DELETE FROM Documents
            WHERE document_id = UUID_TO_BIN(%s) AND application_id = UUID_TO_BIN(%s)
            """,
            (document_id, application_id)
        )

        conn.commit()

        # Try to delete physical file (optional - don't fail if file doesn't exist)
        try:
            app_folder = os.path.join(UPLOAD_FOLDER, application_id)
            if os.path.exists(app_folder):
                # Find and delete the file with UUID prefix
                for filename in os.listdir(app_folder):
                    if filename.endswith(str(document_name)):  # type: ignore
                        file_path = os.path.join(app_folder, filename)
                        os.remove(file_path)
                        break
        except Exception as file_err:
            current_app.logger.warning(f"Could not delete physical file: {file_err}")

        return jsonify({"message": "Document deleted successfully"}), 200

    except MySQLError as e:
        current_app.logger.error(f"Database error deleting document: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error deleting document")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


@user_bp.route("/applications/<application_id>/documents/<document_id>/download", methods=["GET"])
@jwt_required()
def download_document(application_id: str, document_id: str):
    """Download a document file."""
    from api import HOST, MYSQL_USER, MYSQL_PASS, DB_NAME
    from flask import send_file

    user_id = get_jwt_identity()
    current_app.logger.info(f"Downloading document {document_id} for application {application_id}, user_id: {user_id}")

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Verify the application belongs to the user
        cursor.execute(
            """
            SELECT COUNT(*) FROM Applications
            WHERE application_id = UUID_TO_BIN(%s) AND user_id = UUID_TO_BIN(%s)
            """,
            (application_id, user_id)
        )

        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Application not found or access denied"}), 404

        # Get document info
        cursor.execute(
            """
            SELECT document_name FROM Documents
            WHERE document_id = UUID_TO_BIN(%s) AND application_id = UUID_TO_BIN(%s)
            """,
            (document_id, application_id)
        )

        doc_row = cursor.fetchone()
        if not doc_row:
            return jsonify({"error": "Document not found"}), 404

        document_name = doc_row[0]  # type: ignore

        # Find the file in the uploads folder
        app_folder = os.path.join(UPLOAD_FOLDER, application_id)
        if not os.path.exists(app_folder):
            return jsonify({"error": "Document file not found"}), 404

        # Find the file with UUID prefix
        file_path = None
        for filename in os.listdir(app_folder):
            if filename.endswith(str(document_name)):  # type: ignore
                file_path = os.path.join(app_folder, filename)
                break

        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "Document file not found"}), 404

        # Send the file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=str(document_name)  # type: ignore
        )

    except MySQLError as e:
        current_app.logger.error(f"Database error downloading document: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        current_app.logger.exception("Unexpected error downloading document")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
