/*
Application Selection Script for Applications Table
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: Select all the applications for a specific grant
Parameters:
    - grant_id: The unique identifier of the grant whose applications are to be retrieved (required)
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
WHERE grant_id = UUID_TO_BIN(%(grant_id)s);