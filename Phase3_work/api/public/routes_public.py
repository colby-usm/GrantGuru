# routes_public.py

"""

    Version: 29 November 2025
    Author: Colby Wirth

    Description:
        This module defines the public-facing API routes for the application.

        Routes:
            - /aggregate-grants: Returns the total funding of all grants.
            - /fetch_grant_count: Returns the total number of grants in the database.
            - /search_grants: Search grants by query string with pagination.
            - /grant/<grant_id>: Get full details of a specific grant.

"""


# routes_public.py
from flask import jsonify, request
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
        print(e)
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
        print(e)
        return jsonify({"error": str(e)}), 500


@public_bp.route("/search_grants", methods=["GET"])
def search_grants():
    """Search grants by query string (searches title and description)."""

    from api import DB_NAME, HOST, MYSQL_USER, MYSQL_PASS

    q = request.args.get("q", "").strip()
    # pagination
    try:
        page = int(request.args.get("page", "1"))
        if page < 1:
            page = 1
    except Exception:
        page = 1
    try:
        page_size = int(request.args.get("page_size", "10"))
        if page_size < 1:
            page_size = 10
    except Exception:
        page_size = 10
    offset = (page - 1) * page_size
    like = f"%{q}%"

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                if q:
                    # Search by title or description when query provided
                    # count total matching rows
                    cursor.execute(
                        "SELECT COUNT(*) FROM grants WHERE grant_title LIKE %s OR description LIKE %s",
                        (like, like),
                    )
                    total = cursor.fetchone()[0] or 0
                    cursor.execute(
                        """
                        SELECT
                            BIN_TO_UUID(grant_id) AS grant_id,
                            grant_title,
                            description,
                            provider,
                            DATE_FORMAT(date_closed, '%Y-%m-%d') AS date_closed
                        FROM grants
                        WHERE grant_title LIKE %s OR description LIKE %s
                        ORDER BY grant_title ASC
                        LIMIT %s OFFSET %s
                        """,
                        (like, like, page_size, offset),
                    )
                else:
                    # No query: return first 10 grants alphabetically
                    # count total grants
                    cursor.execute("SELECT COUNT(*) FROM grants")
                    total = cursor.fetchone()[0] or 0
                    cursor.execute(
                        """
                        SELECT
                            BIN_TO_UUID(grant_id) AS grant_id,
                            grant_title,
                            description,
                            provider,
                            DATE_FORMAT(date_closed, '%Y-%m-%d') AS date_closed
                        FROM grants
                        ORDER BY grant_title ASC
                        LIMIT %s OFFSET %s
                        """,
                        (page_size, offset),
                    )

                rows = cursor.fetchall()

        grants = [
            {
                "grant_id": r[0],
                "grant_title": r[1],
                "description": r[2],
                "provider": r[3],
                "date_closed": r[4],
            }
            for r in rows
        ]

        # include pagination metadata
        return jsonify({"grants": grants, "total": total, "page": page, "page_size": page_size})

    except MySQLError as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@public_bp.route("/grant/<grant_id>", methods=["GET"])
def get_grant(grant_id: str):
    """Return full grant details for a given UUID string."""

    from api import DB_NAME, HOST, MYSQL_USER, MYSQL_PASS

    try:
        with connect(host=HOST, user=MYSQL_USER, password=MYSQL_PASS, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        BIN_TO_UUID(grant_id) as grant_id,
                        grant_title,
                        opportunity_number,
                        description,
                        research_field,
                        expected_award_count,
                        eligibility,
                        award_max_amount,
                        award_min_amount,
                        program_funding,
                        provider,
                        link_to_source,
                        point_of_contact,
                        DATE_FORMAT(date_posted, '%Y-%m-%d') as date_posted,
                        DATE_FORMAT(archive_date, '%Y-%m-%d') as archive_date,
                        DATE_FORMAT(date_closed, '%Y-%m-%d') as date_closed,
                        DATE_FORMAT(last_update_date, '%Y-%m-%d') as last_update_date
                    FROM Grants
                    WHERE BIN_TO_UUID(grant_id) = %s
                    LIMIT 1
                    """,
                    (grant_id, ),
                )

                row = cursor.fetchone()

        if not row:
            return jsonify({"error": "not_found"}), 404

        keys = [
            "grant_id",
            "grant_title",
            "opportunity_number",
            "description",
            "research_field",
            "expected_award_count",
            "eligibility",
            "award_max_amount",
            "award_min_amount",
            "program_funding",
            "provider",
            "link_to_source",
            "point_of_contact",
            "date_posted",
            "archive_date",
            "date_closed",
            "last_update_date",
        ]

        grant = {k: v for k, v in zip(keys, row)}
        return jsonify({"grant": grant})

    except MySQLError as e:
        print(e)
        return jsonify({"error": str(e)}), 500
