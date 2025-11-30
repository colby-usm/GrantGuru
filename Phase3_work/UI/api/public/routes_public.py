# routes_public.py
from flask import jsonify
from mysql.connector import connect, Error
import os

DB_NAME = os.getenv("DB_NAME", "GrantGuruDB")
HOST = os.getenv("HOST", "localhost")
MYSQL_USER = os.getenv("GG_USER", "root")
MYSQL_PASS = os.getenv("GG_PASS", "")

from . import public_bp


@public_bp.route("/aggregate-grants", methods=["GET"])
def aggregate_grants():
    try:
        conn = connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT FORMAT(COALESCE(SUM(program_funding), 0), 0) AS total
            FROM grants
        """)

        total = cursor.fetchone()[0]

        return jsonify({"total": total})

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@public_bp.route("/fetch_grant_count", methods=["GET"])
def fetch_grant_count():
    try:
        conn = connect(
            host=HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS total_grants FROM grants")

        total = cursor.fetchone()[0]

        return jsonify({"total": total})

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
