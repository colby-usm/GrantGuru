/*
  create_users.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Insert a new user

  Parameters:
    - f_name: First name (required)
    - m_name: Middle name (optional, can be NULL)
    - l_name: Last name (required)
    - institution: Institution name (optional, can be NULL)
    - email: Email address (required, unique)
    - password: Hashed password (required)
  
  Returns: The newly created user_id as binary UUID
*/

INSERT INTO Users (
    f_name,
    m_name,
    l_name,
    institution,
    email,
    password
) VALUES (
    %(f_name)s,
    %(m_name)s,
    %(l_name)s,
    %(institution)s,
    %(email)s,
    %(password)s
)
