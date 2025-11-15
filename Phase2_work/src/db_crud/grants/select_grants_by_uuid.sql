/*
  select_grants_by_uuid.sql
  Author: James Tedder
  Version: 14 November 2025
  Description: Select a grant by their UUID

  Parameters:
    - user_id: The UUID of the grant (required)

  Returns:
    All columns of the Grants table for the given grant_id
*/

SELECT
    BIN_TO_UUID(grant_id) as grant_id,
    grant_title,
    description,
    research_field,
    expected_award_count,
    eligibilty,
    award_max_amount,
    award_min_amount,
    program_funding,
    provider,
    link_to_source,
    point_of_contact,
    date_posted,
    archive_date,
    date_closed,
    last_update_date
FROM Grants
WHERE grant_id = UUID_TO_BIN(%s);