/*
    update_internal_deadlines.sql
    Author: Mathieu Poulin
    Version: 8 December 2025
    Description: Update an internal deadline/task information by UUID. All fields except internal_deadline_id can be updated.

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - internal_deadline_id:
            UUID of the internal deadline to update (required)

        - deadline_name:
            Name of the deadline/task (optional)

        - deadline_date:
            Date of the deadline (optional)

        - application_id:
            Associated application ID (optional)

        - task_description:
            Detailed description of the task (optional)

        - completed:
            Task completion status (optional)
*/

UPDATE InternalDeadlines
SET
    deadline_name = COALESCE(%(deadline_name)s, deadline_name),
    deadline_date = COALESCE(%(deadline_date)s, deadline_date),
    task_description = COALESCE(%(task_description)s, task_description),
    completed = COALESCE(%(completed)s, completed),
    application_id = COALESCE(
        CASE
            WHEN %(application_id)s IS NOT NULL THEN UUID_TO_BIN(%(application_id)s)
            ELSE NULL
        END,
        application_id
    )
WHERE internal_deadline_id = UUID_TO_BIN(%(internal_deadline_id)s);
