/*
  delete_grants.sql
  Author: James Tedder
  Version: 13 November 2025
  Description: Delete a grant

  Parameters:
    - grant_id: The UUID of the grant to delete
*/

DELETE FROM Grants
WHERE grant_id = UUID_TO_BIN(%s)