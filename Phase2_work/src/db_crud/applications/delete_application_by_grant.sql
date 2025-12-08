/*
Application Deletion Script for Applications Table
Version: 15 November 2025
Author: Abdullahi Abdullahi
Description:
 Delete all the applications for a specific grant 
    Parameters:
        - grant_id: The unique identifier of the grant (required)
*/
DELETE FROM Applications
WHERE grant_id = UUID_TO_BIN(%(grant_id)s);
