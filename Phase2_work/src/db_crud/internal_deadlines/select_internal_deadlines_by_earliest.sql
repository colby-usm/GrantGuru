/*
    Select Internal Deadlines by Soonest
    Version: 8 December 2025
    Author: Mathieu Poulin
    Description: Retrieves internal deadlines/tasks ordered by deadline date (soonest first)

    Disclaimer: A portion of this code was generated with the assistance of AI.
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
FROM
    InternalDeadlines
ORDER BY
    deadline_date ASC;
