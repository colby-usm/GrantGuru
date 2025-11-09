/*
  update_users.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Update a user's information by UUID. All fields except user_id and password can be updated.

  Parameters:
    - user_id: UUID of the user to update (required)
    - f_name: First name (optional)
    - m_name: Middle name (optional)
    - l_name: Last name (optional)
    - institution: Institution name (optional)
    - email: Email address (optional, must remain unique)
*/

UPDATE Users
SET
    f_name = COALESCE(%(f_name)s, f_name),
    m_name = COALESCE(%(m_name)s, m_name),
    l_name = COALESCE(%(l_name)s, l_name),
    institution = COALESCE(%(institution)s, institution),
    email = COALESCE(%(email)s, email)
WHERE user_id = UUID_TO_BIN(%(user_id)s);
