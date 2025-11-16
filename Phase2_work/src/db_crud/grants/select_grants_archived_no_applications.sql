/*
  select_grants_archived_no_applications.sql
  Author: James Tedder
  Version: 15 November 2025
  Description: Select the grants that have been archived and have no applications

  Returns:
    All of the grants that have been archived and have no applications associated with them
*/

SELECT BIN_TO_UUID(grant_id) as grant_id
FROM Grants as g
WHERE g.archive_date < CURDATE() 
    AND g.grant_id NOT IN (
        SELECT grant_id
        FROM applications
        )