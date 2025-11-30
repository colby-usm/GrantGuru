/*
  select_password_by_email.sql
  Author: Colby Wirth
  Version: 22 November 2025
  Description: Select a user's password by their email.  Used for logging in

  Parameters:
    - email: The email of the user (required)

  Returns:
    - The hashed password
*/

SELECT 
    BIN_TO_UUID(user_id) as useer_id,
    password
	
FROM Users
WHERE email = LOWER(TRIM(%s));
