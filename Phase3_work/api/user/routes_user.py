# routes_user.py
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import connect, Error as MySQLError
from api import PHASE2_ROOT
import re

user_bp = Blueprint("user", __name__)

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

    # Validate input lengths before processing
    if "fName" in data and len(str(data["fName"])) > 100:
        return jsonify({"error": "First name too long (max 100 characters)"}), 400
    if "mName" in data and data["mName"] and len(str(data["mName"])) > 100:
        return jsonify({"error": "Middle name too long (max 100 characters)"}), 400
    if "lName" in data and len(str(data["lName"])) > 100:
        return jsonify({"error": "Last name too long (max 100 characters)"}), 400
    if "institution" in data and len(str(data["institution"])) > 200:
        return jsonify({"error": "Institution name too long (max 200 characters)"}), 400

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

    new_email = data["email"]

    # Validate email length
    if len(new_email) > 255:
        return jsonify({"error": "Email too long (max 255 characters)"}), 400

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, new_email):
        return jsonify({"error": "Invalid email format"}), 400

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        result = update_users_email(
            role=Role.USER,
            user_id=user_id,
            resource_owner_id=user_id,
            cursor=cursor,
            new_email=new_email,
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

    # Validate password lengths
    if len(data["oldPassword"]) > 128 or len(data["newPassword"]) > 128:
        return jsonify({"error": "Password too long (max 128 characters)"}), 400
    if len(data["newPassword"]) < 8:
        return jsonify({"error": "New password must be at least 8 characters"}), 400

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
