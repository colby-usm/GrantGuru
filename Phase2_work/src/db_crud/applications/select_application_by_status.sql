/*
Application Selection Script for Applications Table
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: Select applications based on their status
Parameters:
    - status: The status of the applications to be retrieved (required)
Returns:
    All columns with UUIDs converted to string format
*/
SELECT 
    BIN_TO_UUID(application_id) AS application_id,
    BIN_TO_UUID(user_id) AS user_id,
    BIN_TO_UUID(grant_id) AS grant_id,
    status,
    application_date
FROM Applications
WHERE status = TRIM(%(status)s);