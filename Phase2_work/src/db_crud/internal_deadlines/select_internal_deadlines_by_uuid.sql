/*
    select_internal_deadlines_by_uuid.sql
    Author: Mathieu Poulin
    Version: 8 December 2025
    Description: Select an internal deadline/task by its UUID

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - internal_deadline_id: The UUID of the internal deadline (required)

    Returns:
        All columns of the InternalDeadlines table for the given internal_deadline_id
*/

SELECT
    BIN_TO_UUID(internal_deadline_id) AS internal_deadline_id,
    BIN_TO_UUID(application_id) AS application_id,
    deadline_name,
    deadline_date,
    task_description,
    completed,
    created_at,
    updated_at
FROM InternalDeadlines
WHERE internal_deadline_id = UUID_TO_BIN(%s);
