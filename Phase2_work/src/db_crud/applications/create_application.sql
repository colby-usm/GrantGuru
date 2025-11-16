/*
Create Application Table
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: insert a new application with necessary fields
*/
INSERT INTO Applications (
    user_id,
    grant_id,
    status,
    application_date
) VALUES (
    UUID_TO_BIN(%(user_id)s),
    UUID_TO_BIN(%(grant_id)s),
    TRIM(%(status)s),
    %(application_date)s
);

