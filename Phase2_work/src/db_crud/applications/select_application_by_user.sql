/*
Application Selection Script for Applications Table
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: Select all the applications made by a specific user
Parameters:
    - user_id: The unique identifier of the user whose applications are to be retrieved (required)
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
WHERE user_id = UUID_TO_BIN(%(user_id)s);