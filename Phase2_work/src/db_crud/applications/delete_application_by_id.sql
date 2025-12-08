/*
Application Deletion Script for Applications Table
Version: 15 November 2025
Author: Abdullahi Abdullahi
Description:
 Delet based on application_id
 Parameters:
    - application_id: The unique identifier of the application to be deleted (required)
*/
DELETE FROM Applications
WHERE application_id = UUID_TO_BIN(%(application_id)s); 
