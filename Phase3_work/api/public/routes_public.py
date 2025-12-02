# routes_public.py

"""

    Version: 29 November 2025
    Author: Colby Wirth

    Description:
        This module defines the public-facing API routes for the application.

        Routes:
            - /aggregate-grants: Returns the total funding of all grants.
            - /fetch_grant_count: Returns the total number of grants in the database.

"""


# routes_public.py
from flask import jsonify
from mysql.connector import connect, Error as MySQLError # type: ignore
from . import public_bp


@public_bp.route("/aggregate-grants", methods=["GET"])
def aggregate_grants():


    from api import DB_NAME, HOST, MYSQL_USER, MYSQL_PASS

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT FORMAT(COALESCE(SUM(program_funding), 0), 0) AS total
                    FROM grants
                """)
                total = cursor.fetchone()[0]
        return jsonify({"total": total})
    except MySQLError as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route("/fetch_grant_count", methods=["GET"])
def fetch_grant_count():
    """Fetch the total number of grants in the database."""

    from api import DB_NAME, HOST, MYSQL_USER, MYSQL_PASS

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total_grants FROM grants")
                total = cursor.fetchone()[0]

        return jsonify({"total": total})

    except MySQLError as e:
        return jsonify({"error": str(e)}), 500
