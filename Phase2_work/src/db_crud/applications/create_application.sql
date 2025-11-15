/*
Create Application Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description: insert a new application with necessary fields
*/
Insert Into Applications (
    user_id,
    grant_id,
    status,
    application_date
) VALUES (
    %(user_id)s,
    %(grant_id)s,
    TRIM(%(status)s),
    %(application_date)s
)

