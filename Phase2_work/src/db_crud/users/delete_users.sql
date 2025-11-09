/*
  delete_users.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Delete a user and cascade delete all related research field associations

  Parameters:
    - user_id: The UUID of the user to delete
*/

DELETE FROM Users
WHERE user_id = UUID_TO_BIN(%(user_id)s);
