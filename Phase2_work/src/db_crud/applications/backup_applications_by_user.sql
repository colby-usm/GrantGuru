-- Backup all applications for a specific user with related data
-- Returns complete application data including tasks and documents metadata

SELECT
    BIN_TO_UUID(a.application_id) as application_id,
    BIN_TO_UUID(a.user_id) as user_id,
    BIN_TO_UUID(a.grant_id) as grant_id,
    a.submission_status,
    a.status,
    a.application_date,
    a.submitted_at,
    a.internal_deadline,
    a.notes,
    -- Grant information for context
    g.grant_title,
    g.opportunity_number,
    g.provider,
    g.award_max_amount,
    g.award_min_amount,
    -- User information for verification
    u.email,
    u.f_name,
    u.l_name,
    u.institution
FROM Applications a
LEFT JOIN Grants g ON a.grant_id = g.grant_id
LEFT JOIN Users u ON a.user_id = u.user_id
WHERE a.user_id = UUID_TO_BIN(%s)
ORDER BY a.application_date DESC;
