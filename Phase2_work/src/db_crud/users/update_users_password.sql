/*
  update_users_password.sql
  Author: Colby Wirth
  Version: 30 November 2025
  Description: Update a user's password by UUID. Only updates if the old password matches.

  Parameters:
    - user_id: UUID of the user to update (required)
    - old_password: Current hashed password (required)
    - new_password: New hashed password (required)
*/

UPDATE Users
SET password = %(new_password)s
WHERE user_id = UUID_TO_BIN(%(user_id)s)
  AND password = %(old_password)s;
