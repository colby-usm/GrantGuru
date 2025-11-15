/*
  select_grants_archived_no_applications.sql
  Author: James Tedder
  Version: 15 November 2025
  Description: Select the grants that have been archived and have no applications

  Returns:
    All of the grants that have been archived and have no applications associated with them
*/

SELECT *
FROM Grants as g
WHERE g.archive_date < CURDATE() 
    AND g.grant_id NOT IN (
        SELECT grant_id
        FROM applications
        )