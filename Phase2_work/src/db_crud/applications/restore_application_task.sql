-- Restore a single application task

INSERT INTO ApplicationTasks (
    task_id,
    application_id,
    task_name,
    task_description,
    deadline,
    completed,
    created_at,
    updated_at
) VALUES (
    UUID_TO_BIN(%s),
    UUID_TO_BIN(%s),
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
ON DUPLICATE KEY UPDATE
    task_name = VALUES(task_name),
    task_description = VALUES(task_description),
    deadline = VALUES(deadline),
    completed = VALUES(completed),
    updated_at = VALUES(updated_at);
