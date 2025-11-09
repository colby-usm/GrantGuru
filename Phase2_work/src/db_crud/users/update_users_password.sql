/*
  update_users_password.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Update a user's password by UUID. Only the password can be updated.

  Parameters:
    - user_id: UUID of the user to update (required)
    - password: New hashed password (required)
*/

UPDATE Users
SET
    password = %(password)s
WHERE user_id = UUID_TO_BIN(%(user_id)s);
