/*
  update_users_email.sql
  Author: Colby Wirth
  Version: 9 November 2025
  Description: Update a user's email by UUID. Only the email can be updated.

  Parameters:
    - user_id: UUID of the user to update (required)
    - email: New email (required)
*/

UPDATE Users
SET
    email = %(email)s
WHERE user_id = UUID_TO_BIN(%(user_id)s);
