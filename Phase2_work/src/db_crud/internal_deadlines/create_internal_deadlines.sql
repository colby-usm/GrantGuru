/*
    create_internal_deadlines.sql
    Author: Mathieu Poulin
    Version: 8 December 2025
    Description: Insert a new internal deadline/task with trimmed and normalized fields

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - deadline_name:
            Name of the deadline/task (required)

        - deadline_date:
            Date of the deadline (required)

        - application_id:
            Associated application ID (required)

        - task_description:
            Detailed description of the task (optional)

        - completed:
            Task completion status (optional, defaults to FALSE)

    Returns:
        The newly created internal_deadline_id as binary UUID
*/

INSERT INTO InternalDeadlines (
    application_id,
    deadline_name,
    deadline_date,
    task_description,
    completed
) VALUES (
    UUID_TO_BIN(%(application_id)s),
    TRIM(%(deadline_name)s),
    %(deadline_date)s,
    %(task_description)s,
    COALESCE(%(completed)s, FALSE)
);
