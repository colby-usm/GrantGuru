# routes_auth.py

"""

    Version: 29 November 2025
    Author: Colby Wirth

    Description:
        Authentication Routes for GrantGuru API.

        This module provides the signup and signin endpoints for user management.
        It handles user creation, password hashing, and login verification.
        Database credentials and PHASE2_ROOT path are loaded from environment variables
        or imported from the api package.

        Routes:
        - POST /signup : Create a new user account.
        - POST /signin : Authenticate a user and return their user ID.
"""


from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import connect, Error as MySQLError

from . import auth_bp


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Handle user signup.

    Expects JSON body with the following fields:
    - firstName
    - middleName (optional)
    - lastName
    - email
    - institutionName
    - password

    Returns:
    - 201: JSON with 'user_id' if successful
    - 400: JSON with 'error' if missing fields or invalid password
    - 409: JSON with 'error' if email already exists
    - 500: JSON with 'error' for other MySQL errors
    """
    from api import create_user_entity, UserOperationError, PHASE2_ROOT, DB_NAME, HOST, MYSQL_USER, MYSQL_PASS

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    f_name = data.get("firstName")
    m_name = data.get("middleName")
    l_name = data.get("lastName")
    email = data.get("email")
    institution = data.get("institutionName")
    password = data.get("password")

    if not all([f_name, l_name, email, institution, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    user_info = {
        "f_name": f_name,
        "m_name": m_name,
        "l_name": l_name,
        "institution": institution,
        "email": email,
        "password": hashed_password
    }

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        new_user_id = create_user_entity(cursor, user_info, PHASE2_ROOT)

        if isinstance(new_user_id, (UserOperationError, MySQLError)):
            return jsonify({"error": str(new_user_id)}), 500

        conn.commit()
        return jsonify({"user_id": new_user_id}), 201

    except MySQLError as e:
        if e.errno == 1062 and "email" in str(e):
            return jsonify({"error": "This email already exists"}), 409
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()



@auth_bp.route("/signin", methods=["POST"])
def signin():
    """
    Handle user signin.

    Expects JSON body with the following fields:
    - email
    - password

    Returns:
    - 200: JSON with 'user_id' if successful
    - 400: JSON with 'error' if missing fields
    - 401: JSON with 'error' if credentials are invalid
    - 500: JSON with 'error' for MySQL or unexpected errors
    """

    from api import get_password_hashed, UserOperationError, PHASE2_ROOT, DB_NAME, HOST, MYSQL_USER, MYSQL_PASS, log_error

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        result = get_password_hashed(cursor, email, PHASE2_ROOT)

        if isinstance(result, (UserOperationError, MySQLError)):
            return jsonify({"error": str(result)}), 500

        if result is None:
            return jsonify({"error": "Invalid credentials"}), 401

        user_id, stored_hash = result

        if not check_password_hash(stored_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user_id)
        return jsonify({"access_token": access_token}), 200

    except MySQLError as e:
        log_error(f"MySQL error during signin: {e}")
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except Exception as e:
        log_error(f"Unexpected error during signin: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()
