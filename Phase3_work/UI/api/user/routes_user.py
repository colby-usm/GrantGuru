# routes_user.py
import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import connect, Error as MySQLError
from api import PHASE2_ROOT

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
