/*
  select_grants_by_research_fields.sql
  Author: James Tedder
  Version: 15 November 2025
  Description: Select a grant by the research fields associated with it

  Parameters:
    - research field: The research field of the grant (required)

  Returns:
    All columns of the Grants table for every instance with the research field
*/

SELECT BIN_TO_UUID(grant_id) as grant_id,
    grant_title,
    opportunity_number,
    description,
    research_field,
    expected_award_count,
    eligibility,
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
FROM Grants as g 
WHERE g.research_field = %s;