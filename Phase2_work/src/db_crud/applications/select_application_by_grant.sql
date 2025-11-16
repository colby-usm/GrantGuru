/*
Application Selection Script for Applications Table
Version: 10 November 2025
Author: Abdullahi Abdullahi
Description: select all the applications for a specific grant
Parameters:
    - grant_id: The unique identifier of the grant whose applications are to be retrieved (required)
*/
select * from Applications
where grant_id = %(grant_id)s;