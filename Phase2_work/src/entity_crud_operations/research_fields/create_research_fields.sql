/*
  update_users_research_field.sql
  Author: Colby Wirth
  Version: 8 November 2025
  Description: Add a new research field for a user, creating it if needed.
               Limits each user to at most 10 research fields.

  Parameters:
    - user_id: The user to associate with
    - research_field: Name of the research field (required, unique)
  
  Returns: research_field_id of the newly created/existing field
*/

-- Check current count
SET @current_count = (
    SELECT COUNT(*)
    FROM UserResearchFields
    WHERE user_id = %(user_id)s
);

-- If user has fewer than 10 fields, insert
IF @current_count < 10 THEN

    -- Insert research field if it doesn't exist
    INSERT INTO ResearchField (research_field)
    VALUES (%(research_field)s)
    ON DUPLICATE KEY UPDATE research_field_id = LAST_INSERT_ID(research_field_id);

    -- Map user to research field
    INSERT INTO UserResearchFields (user_id, research_field_id)
    VALUES (%(user_id)s, LAST_INSERT_ID())
    ON DUPLICATE KEY UPDATE user_id = user_id;

END IF;

-- Return ID of inserted/existing field
SELECT LAST_INSERT_ID() AS research_field_id;
