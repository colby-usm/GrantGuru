-- Restore a single application
-- Uses REPLACE to handle conflicts (updates if exists, inserts if not)

INSERT INTO Applications (
    application_id,
    user_id,
    grant_id,
    submission_status,
    status,
    application_date,
    submitted_at,
    internal_deadline,
    notes
) VALUES (
    UUID_TO_BIN(%s),
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
    submission_status = VALUES(submission_status),
    status = VALUES(status),
    application_date = VALUES(application_date),
    submitted_at = VALUES(submitted_at),
    internal_deadline = VALUES(internal_deadline),
    notes = VALUES(notes);
