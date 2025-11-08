/*
  create_research_field.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Insert a new research field and associate it with the user's id

  Parameters:
    - user_id: The user to associate with
    - research_field: Name of the research field (required, unique)
  
  Returns: The research_field_id of the newly created or existing research field
*/

-- Insert the research field if it doesn't already exist
INSERT INTO ResearchField (research_field)
VALUES (%(research_field)s)
ON DUPLICATE KEY UPDATE research_field_id = LAST_INSERT_ID(research_field_id);

-- Map user to research field
INSERT INTO UserResearchFields (user_id, research_field_id)
VALUES (%(user_id)s, LAST_INSERT_ID())
ON DUPLICATE KEY UPDATE user_id = user_id;

-- Return the ID
SELECT LAST_INSERT_ID() AS research_field_id;
