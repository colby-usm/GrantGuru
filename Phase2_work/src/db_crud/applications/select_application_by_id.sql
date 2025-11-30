/*
Application Selection Script for Applications Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description: select the application based on application_id
Parameters:
    - application_id: The unique identifier of the application to be retrieved (required)
*/
select * from Applications
where application_id = %(application_id)s;