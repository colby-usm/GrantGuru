/*
  select_grants_open.sql
  Author: James Tedder
  Version: 15 November 2025
  Description: Select the grants that are open

  Returns:
    All of the grants that are open
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
WHERE g.date_closed < CURDATE()