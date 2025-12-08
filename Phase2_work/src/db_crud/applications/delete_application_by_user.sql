/*
Application Deletion Script for Applications Table
Version: 15 November 2025
Author: Abdullahi Abdullahi
Description:
 Delete all the applications for a specific user
    Parameters:
        - user_id: The unique identifier of the user (required)
*/
DELETE FROM Applications
WHERE user_id = UUID_TO_BIN(%(user_id)s);

