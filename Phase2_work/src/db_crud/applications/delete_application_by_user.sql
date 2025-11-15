/*
Application Deletion Script for Applications Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description:
 Delete all the applications for a specific user
    Parameters:
        - user_id: The unique identifier of the user (required)
*/
DELETE FROM Applications
WHERE user_id = %(user_id)s;

