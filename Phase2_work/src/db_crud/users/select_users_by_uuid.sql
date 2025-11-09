/*
  select_users_by_uuid.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Select a user by their UUID

  Parameters:
    - user_id: The UUID of the user (required)

  Returns:
    All columns of the Users table for the given user_id
*/

SELECT 
    BIN_TO_UUID(user_id) AS user_id,
    f_name,
    m_name,
    l_name,
    institution,
    email,
    password
FROM Users
WHERE user_id = UUID_TO_BIN(%(user_id)s);
