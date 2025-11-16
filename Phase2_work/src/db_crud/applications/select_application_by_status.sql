/*
Application Selection Script for Applications Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description: select appications based on their status
Parameters:
    - status: The status of the applications to be retrieved (required)
*/
select * from Applications
where status = TRIM(%(status)s);