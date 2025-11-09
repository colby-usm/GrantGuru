/*
  select_users_by_email.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Select a user by their email

  Parameters:
    - email: The email of the user (required)

  Returns:
	uuid
*/

SELECT 
    BIN_TO_UUID(user_id) AS user_id
FROM Users
WHERE email = %(email)s;
