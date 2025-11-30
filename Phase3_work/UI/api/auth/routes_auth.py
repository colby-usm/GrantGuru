# routes.py

import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from mysql.connector import connect, Error as MySQLError



BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../Phase2_work"))
sys.path.insert(0, BASE_DIR)
PHASE2_ROOT = os.path.abspath(os.path.join(BASE_DIR))

from src.user_functions.users_operations import create_user_entity, get_password_hashed, UserOperationError
from src.user_functions.view_based_operations import Role
from src.utils.logging_utils import log_info, log_error

from flask_cors import CORS

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")


app = Flask(__name__)
CORS(app) 

@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    f_name = data.get("firstName")
    m_name = data.get("middleName")
    l_name = data.get("lastName")
    email = data.get("email")
    institution= data.get("institutionName")
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

        new_user_id = create_user_entity(
            cursor,
            user_info,
            PHASE2_ROOT

        )
        if isinstance(new_user_id, (UserOperationError, MySQLError)):
            return jsonify({"error": str(new_user_id)}), 500

        conn.commit()
        return jsonify({"user_id": new_user_id}), 201

    except MySQLError as e:
        # Check for duplicate email error (MySQL code 1062)
        if e.errno == 1062 and "email" in str(e):
            return jsonify({"error": "This email already exists"}), 409
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()



from werkzeug.security import check_password_hash

@app.route("/auth/signin", methods=["POST"])
def signin(): 
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Connect to DB
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        # Fetch stored password hash and user_id
        result = get_password_hashed(cursor, email, PHASE2_ROOT)

        if isinstance(result, (UserOperationError, MySQLError)):
            return jsonify({"error": str(result)}), 500

        if result is None:
            return jsonify({"error": "Invalid credentials"}), 401

        user_id, stored_hash = result

        # Verify password
        if not check_password_hash(stored_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Successful login
        return jsonify({"user_id": user_id}), 200

    except MySQLError as e:
        log_error(f"MySQL error during signin: {e}")
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except Exception as e:
        log_error(f"Unexpected error during signin: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/aggregate-grants", methods=["GET"])
def aggregate_grants():
    try:
        conn = connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME)
        cursor = conn.cursor()

        query = """
            SELECT FORMAT(COALESCE(SUM(program_funding), 0), 0) AS total
            FROM grants
            WHERE CURDATE() > date_closed;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        return jsonify({"total": result[0]})

    except MySQLError as e:
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
