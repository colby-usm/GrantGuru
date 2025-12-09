/*
    select_internal_deadlines_by_application.sql
    Author: Mathieu Poulin
    Version: 8 December 2025
    Description: Select all internal deadlines/tasks for a specific application

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - application_id: The UUID of the application (required)

    Returns:
        All internal deadlines/tasks for the given application, ordered by deadline date
*/

SELECT
    BIN_TO_UUID(internal_deadline_id) AS internal_deadline_id,
    BIN_TO_UUID(application_id) AS application_id,
    deadline_name,
    DATE_FORMAT(deadline_date, '%Y-%m-%d') AS deadline_date,
    task_description,
    completed,
    created_at,
    updated_at
FROM InternalDeadlines
WHERE application_id = UUID_TO_BIN(%s)
ORDER BY deadline_date ASC;
