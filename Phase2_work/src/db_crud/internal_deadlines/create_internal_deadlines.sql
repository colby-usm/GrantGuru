/*
    create_internal_deadlines.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Insert a new internal deadline with trimmed and normalized fields

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - deadline_name:
            Name of the deadline (required)

        - deadline_date:
            Date and time of the deadline (required)

        - application_id:
            Associated application ID (required)

    Returns:
        The newly created internal_deadline_id as binary UUID
*/

INSERT INTO InternalDeadlines (
    deadline_name,
    deadline_date,
    application_id
) VALUES (
    TRIM(%(deadline_name)s),
    %(deadline_date)s,
    %(application_id)s
);
