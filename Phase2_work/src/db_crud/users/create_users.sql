/*
  create_users.sql
  Author: Colby Wirth
  Version: 9 November 2025
  Description: Insert a new user with trimmed and normalized fields

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
    TRIM(%(f_name)s),
    TRIM(%(m_name)s),
    TRIM(%(l_name)s),
    TRIM(%(institution)s),
    LOWER(TRIM(%(email)s)),
    %(password)s
);
