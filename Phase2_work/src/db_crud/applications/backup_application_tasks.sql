-- Backup all tasks for a specific application

SELECT
    BIN_TO_UUID(task_id) as task_id,
    BIN_TO_UUID(application_id) as application_id,
    task_name,
    task_description,
    deadline,
    completed,
    created_at,
    updated_at
FROM ApplicationTasks
WHERE application_id = UUID_TO_BIN(%s)
ORDER BY deadline ASC;
