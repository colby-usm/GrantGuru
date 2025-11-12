/*
  delete_users_research_field.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Remove a research field association for a user

  Parameters:
    - user_id: The user
    - research_field_id: The research field to remove
*/

DELETE FROM UserResearchFields
WHERE user_id = %(user_id)s
  AND research_field_id = %(research_field_id)s;
