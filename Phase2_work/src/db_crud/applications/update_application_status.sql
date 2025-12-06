/*
Applications Update Procedure
Version: 15 November 2025 
Author: Abdullahi Abdullahi
Description: Update an existing application's status based on application_id
Parameters:
    - application_id: The unique identifier of the application to be updated (required)
    - status: The new status for the application (required)
*/
UPDATE Applications
SET 
    status = TRIM(%(status)s)
WHERE application_id = UUID_TO_BIN(%(application_id)s);