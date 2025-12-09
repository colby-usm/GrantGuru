/*
    Select Internal Deadlines by Next
    Version: 8 December 2025
    Author: Mathieu Poulin
    Description: Retrieves the next upcoming internal deadline/task (earliest deadline that hasn't passed yet)

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
WHERE
    deadline_date >= CURDATE()
ORDER BY
    deadline_date ASC
LIMIT 1;
