/*
Application Selection Script for Applications Table
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: Select the application based on application_id
Parameters:
    - application_id: The unique identifier of the application to be retrieved (required)
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
WHERE application_id = UUID_TO_BIN(%(application_id)s);
