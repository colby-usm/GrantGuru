/*
Application Selection Script for Applications Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description: select all the applications made by a specific user
Parameters:
    - user_id: The unique identifier of the user whose applications are to be retrieved (required)
*/
select * from Applications
where user_id = %(user_id)s;